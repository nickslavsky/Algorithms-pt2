"""
In this programming problem and the next you'll code up the knapsack algorithm from lecture.
You can assume that all numbers are positive. You should assume that item weights and the knapsack capacity are integers.

In the box below, type in the value of the optimal solution.
"""
import numpy as np
import time


def load_data(file_name):
    """
    reads the file and returns 2 numpy arrays of weights and values
    [knapsack_size][number_of_items]
    [value_1] [weight_1]
    [value_2] [weight_2]
    ...
    """
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # split the lines
    lines = file_contents.split('\n')
    # pop the size and the total number of items to initialize
    knapsack_size, number_of_items = map(int, lines.pop(0).split())
    weights, values = np.zeros(number_of_items), np.zeros(number_of_items)
    i = 0
    for line in lines:
        spl = line.split()
        if spl:
            values[i], weights[i] = map(int, spl)
            i += 1
    return knapsack_size, weights, values


def solve_knapsack_problem(knapsack_size, weights, values):
    a_current = np.zeros(knapsack_size+1)
    a_previous = np.zeros(knapsack_size+1)
    n = len(weights)
    for i in range(1, n+1):
        a_current[:weights[i-1]] = a_previous[:weights[i-1]]
        a_current[weights[i-1]:] = np.fmax(
            a_previous[weights[i-1]:],
            a_previous[:knapsack_size + 1 - weights[i-1]] + values[i-1]
        )
        np.copyto(a_previous, a_current)
    return a_current[knapsack_size]

if __name__ == '__main__':
    W, w, v = load_data('knapsack1.txt')
    t1 = time.time()
    print('Maximum knapsack value is: {0:.0f}'.format(solve_knapsack_problem(W, w, v)))
    print('Solved in {0:.3f}s'.format(time.time() - t1))
