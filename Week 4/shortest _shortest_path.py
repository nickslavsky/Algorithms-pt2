"""
Your task is to compute the "shortest shortest path". Precisely, you must first identify which, if any,
of the three graphs have no negative cycles. For each such graph, you should compute all-pairs shortest paths and
remember the smallest one (i.e., compute min u,v d(u,v), where d(u,v) denotes the shortest-path distance from u to v).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box below.
If exactly one graph has no negative-cost cycles, then enter the length of its shortest shortest path in the box below.
If two or more of the graphs have no negative-cost cycles, then enter the smallest of the lengths of their shortest
shortest paths in the box below.
"""

import heapq
import math
from collections import defaultdict
import logging
import sys
import numpy as np


class Heap:
    """
    heap data structure with removing based on
    https://docs.python.org/3.5/library/heapq.html#priority-queue-implementation-notes
    need to mark deleted -1, otherwise when comparing [math.inf, '<removed-task>'], [math.inf, 4]
    Python will error out:
    http://stackoverflow.com/questions/16373809/python-huffman-coding-exception-unorderable-types
    """

    def __init__(self, graph, source):
        # create a list to serve as heap, assign the source vertex the score of 0, infinity for the rest
        heap = [[0 if node == source else math.inf, node] for node in graph.keys()]
        heapq.heapify(heap)
        self.heap = heap  # list of entries arranged in a heap
        self.entry_finder = {i[-1]: i for i in heap}  # mapping of nodes to entries (score, node)
        self.REMOVED = -1  # placeholder for a removed node

    def add_node(self, node, score=0):
        """Add a new node or update the Dijkstra score of an existing node"""
        if node in self.entry_finder:
            self.remove_node(node)
        entry = [score, node]
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
            score, node = heapq.heappop(self.heap)
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return score, node
        raise KeyError('pop from an empty priority queue')


def run_dijkstra(edges_dict, heap):
    length = len(edges_dict)  # the number of vertices n
    explored = set()
    unexplored = set(node for node in edges_dict.keys())
    shortest_paths = np.zeros(length)
    while len(explored) < length:
        new_score, new_vertex = heap.pop_node()  # we pop next vertex w
        explored.add(new_vertex)
        unexplored.remove(new_vertex)
        shortest_paths[new_vertex-1] = new_score
        for node, edge_length in edges_dict[new_vertex]:  # for each v of edges (w, v)
            if node in unexplored:  # if it's a crossing edge
                current_score = heap.get_score(node)  # set its score to the min{(its current score), (A[w] + L(w, v))}
                heap.remove_node(node)
                score = min(current_score, new_score + edge_length)
                heap.add_node(node, score)
    return shortest_paths


def load_graph_from_file(file_name):
    """
    The first line indicates the number of vertices and edges, respectively. Each subsequent line describes an edge
    (the first two numbers are its tail and head, respectively) and its length (the third number).
    NOTE: some of the edge lengths are negative.
    NOTE: These graphs may or may not have negative-cost cycles.
    """
    graph = defaultdict(set)
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    lines = file_contents.split('\n')
    # pop the n and m
    number_of_vertices, number_of_edges = map(int, lines.pop(0).split())
    for line in lines:
        spl = line.split()
        if spl:
            tail, head, length = map(int, spl)
            graph[tail].add((head, length))
    return graph, number_of_vertices


def solve_assignment():
    file_names = ['g{0}.txt'.format(i) for i in range(1, 4)]
    answer = np.inf
    for name in file_names:
        logger.info('Solving {0}'.format(name))
        g, n = load_graph_from_file(name)
        logger.info('Data loaded from file')
        tmp = run_johnson(g, n)
        try:
            answer = min(answer, tmp)
        except TypeError:  # when there's a negative cycle and tmp == None
            pass
        logger.info('Shortest shortest path is: {0}'.format(tmp))
    logger.info('Assignment answer: {0}'.format(answer))


def run_bellman_ford(graph, number_of_vertices, source):
    # switch to 0-based arrays:
    source -= 1
    a_previous = np.zeros(number_of_vertices)
    a_current = np.zeros(number_of_vertices)
    mask = np.ones(number_of_vertices, dtype=bool)
    mask[source] = False
    a_current[mask] = np.inf
    tmp = np.zeros(number_of_vertices)
    # outer loop of BF, iterate from 0 to n-2 (or from 1 to n-1)
    for i in range(number_of_vertices):
        np.copyto(a_previous, a_current)
        tmp[:] = np.inf
        for tail in graph.keys():
            for head, length in graph[tail]:
                # we're talking about 0-based numpy arrays here
                tmp[head - 1] = min(tmp[head - 1], a_previous[tail - 1] + length)
        a_current = np.fmin(a_previous, tmp)
        # stopping early
        if np.array_equal(a_current, a_previous):
            logger.info('Stopping Early')
            return a_current
    # if on the n-th iteration the shortest paths are not the same as on the previous, there was a negative cycle
    if not np.array_equal(a_current, a_previous):
        logger.info('Negative cycle detected')
        return None
    return a_current


def run_johnson(graph, number_of_vertices):
    # add vertex 0 to G
    vertices = set(range(1, number_of_vertices + 1))
    graph[number_of_vertices + 1] = {(i, 0) for i in vertices}
    # calculate shortest paths from 0 to every vertex in G or report a negative cycle
    b_f_shortest_paths = run_bellman_ford(graph, number_of_vertices + 1, number_of_vertices + 1)
    if b_f_shortest_paths is None:
        return None
    graph_updated = defaultdict(set)
    for tail in vertices:
        graph_updated[tail] = {(head, length + b_f_shortest_paths[tail-1] - b_f_shortest_paths[head-1])
                               for head, length in graph[tail]}
    # all edges are non-negative, ready to run Dijkstra
    tmp = np.inf
    for source in vertices:
        heap = Heap(graph_updated, source)
        shortest_paths_shifted = run_dijkstra(graph_updated, heap)
        shortest_paths = shortest_paths_shifted + b_f_shortest_paths[:-1] - b_f_shortest_paths[source - 1]
        tmp = min(tmp, min(shortest_paths))
    return tmp


if __name__ == '__main__':
    # initialize logging to console
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s] %(message)s',
                                  datefmt='%Y-%m-%d\t%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # actual start
    logger.info('Program started')
    solve_assignment()
    logger.info('Done')