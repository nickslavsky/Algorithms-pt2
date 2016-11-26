"""
In this assignment you will implement one or more algorithms for the traveling salesman problem,
such as the dynamic programming algorithm covered in the video lectures.
"""
import numpy as np
import time
import itertools
from collections import defaultdict
from scipy.spatial import distance
import logging
import sys


def load_data(file_name):
    """
    reads the file and returns a numpy array of shape (n, 2)
    The first line indicates the number of cities. Each city is a point in the plane,
    and each subsequent line indicates the x- and y-coordinates of a single city.
    The distance between two cities is defined as the Euclidean distance --- that is,
    two cities at locations (x,y) and (z,w) have distance (x−z)2+(y−w)2 between them.
    """
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # split the lines
    lines = file_contents.split('\n')
    # pop the total number of cities
    cities_count = int(lines.pop(0))
    cities = np.zeros((cities_count, 2), dtype='float32')
    i = 0
    for line in lines:
        spl = line.split()
        if spl:
            cities[i][0], cities[i][1] = map(float, spl)
            i += 1
    logger.info('Data loaded')
    return cities_count, cities


def subset_without_city(city_id, subset):
    return subset ^ (1 << city_id)


def solve_tsp(cities_count, cities):
    dist = distances(cities)
    full_set = 2 ** cities_count - 1
    A = np.empty((2 ** cities_count, cities_count), dtype='float32')
    A[:] = np.inf
    A[0][0] = 0
    for i in range(1, cities_count):
        s = (1 << i) + 1
        A[s][i] = dist[0][i]
    powers = defaultdict(int)
    for e in range(cities_count-1):
        powers[1 << e] = e
    # since the city #0 is always there, the rightmost bit is always set
    # also, to be able to get min over k!=j, need to have at least 3 cities in subset
    for m in range(2, cities_count):
        logger.info('Subset size: {0}'.format(m))
        sets = bit_sets(powers, m)
        for s, bits in sets.items():  # generate subset of size m
            subset = (s << 1) + 1  # the actual subset has city #0 in the rightmost bit
            for j in bits:  # all the cities that there are in S
                A[subset][j+1] = min(A[subset_without_city(j+1, subset)] + dist[j+1])
    tour = np.inf
    for j in range(1, cities_count):
        tour = min(tour, A[full_set][j] + dist[0][j])
    return tour


def distances(points):
    result = distance.cdist(points, points, 'euclidean')
    np.fill_diagonal(result, np.inf)
    return result


def bit_sets(powers, k):
    result = defaultdict(set)
    for bits in itertools.combinations(powers.keys(), k):
        result[sum(bits)] = {powers[bit] for bit in bits}
    # logger.info('Generated bit sets')
    return result

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
    logger.info('Start')
    n, array = load_data('tsp.txt')
    t1 = time.time()
    logger.info('Optimal TSP tour length is: {0:.2f}'.format(solve_tsp(n, array)))
    logger.info('Solved in {0:.3f}s'.format(time.time() - t1))
