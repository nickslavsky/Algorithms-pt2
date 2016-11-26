"""
In this question your task is again to run the clustering algorithm from lecture, but on a MUCH bigger graph.
So big, in fact, that the distances (i.e., edge costs) are only defined implicitly,
rather than being provided as an explicit list.

The question is: what is the largest value of k such that there is a k-clustering with spacing at least 3?
That is, how many clusters are needed to ensure that no pair of nodes with all but 2 bits in common
get split into different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably can't write it out explicitly,
let alone sort the edges by cost. So you will have to be a little creative to complete this part of the question.
For example, is there some way you can find the smallest distances without explicitly looking at every pair of nodes?
"""
from collections import defaultdict
import time


class UnionFind:
    """A fast implementation with lazy unions, ranks and path compression"""

    def __init__(self, nodes):
        self.__nodes = defaultdict(list)
        for node in nodes:
            self.__nodes[node] = [node, 0]

    def union(self, node_i, node_j):
        parent_i = self.find(node_i)
        parent_j = self.find(node_j)
        if parent_i != parent_j:
            if self.__nodes[parent_i][1] > self.__nodes[parent_j][1]:
                self.__nodes[parent_j][0] = parent_i
            else:
                self.__nodes[parent_i][0] = parent_j
                # only if the ranks are equal, the new parent will have its rank increased
                if self.__nodes[parent_i][1] == self.__nodes[parent_j][1]:
                    self.__nodes[parent_j][1] += 1

    def find(self, node):
        # remember all traversed nodes
        traversed = set()
        while self.__nodes[node][0] != node:
            node = self.__nodes[node][0]
            traversed.add(node)
        # compress paths
        for vertex in traversed:
            self.__nodes[vertex][0] = node
        return node

    @property
    def cluster_count(self):
        node_set = set(self.find(value[0]) for value in self.__nodes.values())
        return len(node_set)


def load_data(file_name):
    """reads the file and returns the set of vertices"""
    res = set()
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # split the lines
    lines = file_contents.split('\n')
    # pop n to initialize union find
    lines.pop(0)
    for line in lines:
        s = line.split()
        if s:
            res.add(int(''.join(s), 2))
    return res


def calculate_max_k(vertices):
    uf = UnionFind(vertices)
    # union all vertices with distance 1
    for vertex in vertices:
        for offset in range(24):
            flipped = toggle_bit(vertex, offset)
            if flipped in vertices:
                uf.union(vertex, flipped)
    # union all vertices with distance 2
    for vertex in vertices:
        for i in range(24):
            for j in range(i, 24):
                flipped = toggle_bit(vertex, i)
                flipped = toggle_bit(flipped, j)
                if flipped in vertices:
                    uf.union(vertex, flipped)
    return uf.cluster_count


def toggle_bit(int_type, offset):
    mask = 1 << offset
    return int_type ^ mask


if __name__ == '__main__':
    v = load_data('clustering_big.txt')
    t1 = time.time()
    print('Maximum number of clusters for spacing 3 is {0}'.format(calculate_max_k(v)))
    print(time.time() - t1)
