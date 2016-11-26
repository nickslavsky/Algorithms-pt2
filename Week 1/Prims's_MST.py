"""
Your task is to run Prim's minimum spanning tree algorithm on this graph.
You should report the overall cost of a minimum spanning tree --- an integer,
which may or may not be negative --- in the box below.
"""
import heapq
from collections import defaultdict
from itertools import count
from math import inf


class Heap:
    """
    heap data structure with removing based on
    https://docs.python.org/3.5/library/heapq.html#priority-queue-implementation-notes
    need to add counter as a hack, otherwise when comparing [math.inf, '<removed-task>'], [math.inf, 4]
    Python will error out:
    http://stackoverflow.com/questions/16373809/python-huffman-coding-exception-unorderable-types
    """

    def __init__(self, heap=[]):
        heapq.heapify(heap)
        self.heap = heap  # list of entries arranged in a heap
        self.entry_finder = {i[-1]: i for i in heap}  # mapping of nodes to entries (score, node)
        self.REMOVED = '<removed-node>'  # placeholder for a removed node
        self.counter = count()  # a hack

    def add_node(self, node, score=0):
        """Add a new node or update the Dijkstra score of an existing node"""
        if node in self.entry_finder:
            self.remove_node(node)
        cnt = next(self.counter)
        entry = [score, cnt, node]
        self.entry_finder[node] = entry
        heapq.heappush(self.heap, entry)

    def remove_node(self, node):
        """Mark an existing node as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED

    def get_score(self, node):
        """Get node's old score in O(1) time before updating it"""
        return self.entry_finder[node][0]

    def pop_node(self):
        """Remove and return the node with the lowest Dijkstra score. Raise KeyError if empty."""
        while self.heap:
            score, junk, node = heapq.heappop(self.heap)
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return score, node
        raise KeyError('pop from an empty priority queue')


def load_graph(file_name):
    res = defaultdict(set)
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # split the lines
    lines = file_contents.split('\n')
    # pop n and m, we'll not use them
    lines.pop(0)
    for line in lines:
        spl = line.split()
        if spl:
            node1, node2, cost = map(int, spl)
            res[node1].add((node2, cost))
            res[node2].add((node1, cost))
    return res


def create_heap(graph):
    # create a list to serve as heap, assign the source(first) vertex the score of 0, infinity for the rest
    counter = count()
    to_be_heap = [[0 if node == 1 else inf, next(counter), node] for node in graph]
    return Heap(to_be_heap)


def calculate_prims_mst(graph, heap):
    explored = set()
    unexplored = set(node for node in graph)
    total_mst_cost = 0
    while len(unexplored) > 0:
        # we pop next vertex w
        new_score, new_vertex = heap.pop_node()
        explored.add(new_vertex)
        unexplored.remove(new_vertex)
        total_mst_cost += new_score
        # make sure we pay the piper
        for node, edge_cost in graph[new_vertex]:  # for each v of edges (w, v)
            if node in unexplored:  # if it's a crossing edge
                current_score = heap.get_score(node)  # set its score to the min{(its current score), (C(w, v))}
                heap.remove_node(node)
                score = min(current_score, edge_cost)
                heap.add_node(node, score)
    return total_mst_cost


if __name__ == '__main__':
    gr = load_graph('edges.txt')
    h = create_heap(gr)
    print('Total length of  MST: {0}'.format(calculate_prims_mst(gr, h)))
