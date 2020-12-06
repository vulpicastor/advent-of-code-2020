#!/usr/bin/python3

import re

import numpy as np


def main():
    with open("../input/06.txt") as f:
        lines = f.read()
    groups = lines.split('\n\n')
    all_count = []
    for g in groups:
        ps = g.split()
        count = 0
        for i in "abcdefghijklmnopqrstuvwxyz":
            if all(i in p for p in ps):
                count += 1
        all_count.append(count)
    groups = [l.replace('\n', '') for l in groups]
    count = [np.unique(list(i)) for i in groups]
    print(count)
    print(sum(map(len, count)))
    print(all_count)
    print(sum(all_count))

if __name__ == "__main__":
    main()
