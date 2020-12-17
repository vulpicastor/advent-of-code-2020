#!/usr/bin/python3

import collections
import itertools
import functools
import operator as op
import re
import timeit

import numpy as np


def find_earliest(depart, bus):
    mod = depart % bus
    # quo = depart // bus
    if mod == 0:
        mod = bus
    return bus - mod, bus

def invmod(a, m):
    res = 1
    for _ in range(m-2):
        res *= a
        res %= m
    return res

def chinese_remainder(pairs):
    primes = []
    remainders = []
    for a, n in pairs:
        primes.append(n)
        remainders.append(a)
    bigN = functools.reduce(op.mul, primes)
    ys = [bigN//n for n in primes]
    zs = [invmod(y, n) for y, n in zip(ys, primes)]
    res = 1
    for a, y, z in zip(remainders, ys, zs):
        print(a, y, z)
        res += a * y * z
        res %= bigN
    return res

def main():
    with open("input/13try.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    # departure = int(lines[0])
    buses = []
    for i, b in enumerate(lines[1].split(',')):
        if b == "x":
            continue
        buses.append((i, int(b)))
    # a, b = min(find_earliest(departure, b) for b in buses)
    # print(a*b)
    print(chinese_remainder(buses))



if __name__ == "__main__":
    main()
