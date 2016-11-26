"""
Your task is to determine which of the 6 instances are satisfiable, and which are unsatisfiable.
In the box below, enter a 6-bit string, where the ith bit should be 1 if the ith instance is satisfiable,
and 0 otherwise. For example, if you think that the first 3 instances are satisfiable and the last 3 are not,
then you should enter the string 111000 in the box below.
"""
import logging
import sys
from collections import deque, defaultdict


class Kosaraju:
    def __init__(self, graph, rev_graph):
        self.__graph, self.__rev_graph = graph, rev_graph
        self.__current_leader = None
        self.__leaders = defaultdict(set)
        self.__done, self.__explored = set(), set()
        self.__order = deque()

    def __dfs(self, graph, node):
        # stack realization
        stack = deque([node])
        while stack:
            vertex = stack.pop()
            if vertex not in self.__explored:
                self.__explored.add(vertex)
                # on the first pass __current_leader == None
                if self.__current_leader is not None:
                    self.__leaders[self.__current_leader].add(vertex)
                # vertex will be popped after all its adjacent vertices
                stack.append(vertex)
                to_add = graph[vertex] - self.__explored if vertex in graph else set()
                if len(to_add) > 0:
                    stack.extend(to_add)
            # it's the second time we pop vertex from stack
            else:
                if vertex not in self.__done:
                    self.__done.add(vertex)
                    self.__order.appendleft(vertex)

    def __calculate_magic_numbers(self):
        for node in self.__rev_graph.keys():
            if node not in self.__explored:
                self.__dfs(self.__rev_graph, node)

    def __calculate_leaders(self):
        self.__calculate_magic_numbers()
        self.__explored = set()
        for node in self.__order:
            if node not in self.__explored:
                self.__current_leader = node
                self.__dfs(self.__graph, node)

    @property
    def leaders(self):
        self.__calculate_leaders()
        return self.__leaders


def load_data(file_name):
    """
    In each instance, the number of variables and the number of clauses is the same,
    and this number is specified on the first line of the file.
    Each subsequent line specifies a clause via its two literals, with a number denoting the variable
    and a "-" sign denoting logical "not". For example, the second line of the first data file is "-16808 75250",
    which indicates the clause ¬x16808 OR x75250.
    """
    graph, rev_graph = defaultdict(set), defaultdict(set)
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # build both graph and reversed graph in one go
    lines = file_contents.split('\n')
    lines.pop(0)
    for line in lines:
        spl = line.split()
        if spl:
            var1, var2 = map(int, spl)
            graph[-var1].add(var2)
            graph[-var2].add(var1)
            rev_graph[var2].add(-var1)
            rev_graph[var1].add(-var2)
    return graph, rev_graph


def check_2_sat(scc_dictionary):
    for leader in scc_dictionary.keys():
        for variable in scc_dictionary[leader]:
            tmp = scc_dictionary[leader]
            tmp.add(leader)
            if -variable in tmp:
                return False
    return True


def solve_assignment():
    file_names = ['2sat{0}.txt'.format(i) for i in range(1, 7)]
    answer = str()
    for name in file_names:
        logger.info('Solving {0}'.format(name))
        g1, g2 = load_data(name)
        logger.info('Data loaded from file')
        # initialize our Kosaraju object
        kosaraju = Kosaraju(g1, g2)
        logger.info('Kosaraju initialized')
        # calculate leaders
        leaders_dict = kosaraju.leaders
        # check if instance is satisfiable
        answer += '1' if check_2_sat(leaders_dict) else '0'
        logger.info('Checked if 2 SAT is satisfiable: {0}'.format(check_2_sat(leaders_dict)))
    logger.info('Assignment answer: {0}'.format(answer))

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
