"""
In this programming problem and the next you'll code up the clustering algorithm from lecture
for computing a max-spacing k-clustering.

Your task in this problem is to run the clustering algorithm from lecture on this data set,
where the target number k of clusters is set to 4. What is the maximum spacing of a 4-clustering?
"""


class UnionFind:
    """A fast implementation with lazy unions, ranks and path compression"""

    def __init__(self, size):
        # a zero-based list of nodes' parents
        self.__parents = list(range(size))
        # a zero-based list of their ranks, initially all ranks are 0
        self.__ranks = [0] * size

    def union(self, node_i, node_j):
        parent_i = self.find(node_i)
        parent_j = self.find(node_j)
        if self.__ranks[parent_i] > self.__ranks[parent_j]:
            self.__parents[parent_j] = parent_i
        else:
            self.__parents[parent_i] = parent_j
            # only if the ranks are equal, the new parent will have its rank increased
            if self.__ranks[parent_i] == self.__ranks[parent_j]:
                self.__ranks[parent_j] += 1

    def find(self, node):
        # remember all traversed nodes
        traversed = set()
        while self.__parents[node] != node:
            node = self.__parents[node]
            traversed.add(node)
        # compress paths
        for vertex in traversed:
            self.__parents[vertex] = node
        return node


def load_data(file_name):
    """reads the file and returns the number of vertices size and a 0-based list of tuples(node1, node2, edge_cost)"""
    res = []
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # split the lines
    lines = file_contents.split('\n')
    # pop n to initialize union find
    size = int(lines.pop(0))
    for line in lines:
        spl = line.split()
        if spl:
            node1, node2, cost = map(int, spl)
            res.append((node1, node2, cost))
    res = [(i - 1, j - 1, c) for (i, j, c) in res]
    return size, res


def kruskals_k_clustering(size, k, edge_list):
    uf = UnionFind(size)
    edges = sorted(edge_list, key=lambda t: t[2], reverse=True)
    n = size
    while n > k:
        # pop the tuple with the smallest weight
        u, v, w = edges.pop()
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            n -= 1
    # now pop from the list until we come across disjoint points
    spacing = 0
    while spacing == 0:
        u, v, w = edges.pop()
        if uf.find(u) != uf.find(v):
            spacing = w
    return spacing


if __name__ == '__main__':
    size, gr = load_data('clustering1.txt')
    print('Maximum spacing is: {0}'.format(kruskals_k_clustering(size, 4, gr)))
