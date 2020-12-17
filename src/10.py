#!/usr/bin/python3

import collections
import functools
import operator as op
import re
import secrets

import numpy as np


class Node(collections.UserDict):

    def __init__(self):
        self.data = dict()
        self.key = secrets.token_bytes(8)

    def __hash__(self):
        return hash(self.key)


@functools.lru_cache(maxsize=None)
def dfs_visit(node, dest):
    visited = 0
    for n in node:
        if n is dest:
            visited += 1
            continue
        visited += dfs_visit(n, dest)
    return visited


def main():
    with open("input/10.txt") as f:
        lines = [int(l.strip()) for l in f.readlines()]
    lines.append(0)
    lines.sort()
    lines.append(lines[-1] + 3)
    jolts = np.array(lines)
    g = collections.defaultdict(Node)
    length = len(jolts)
    for i, j in enumerate(jolts):
        for k in range(1, 4):
            if i + k < length and jolts[i+k] - j <= 3:
                # g.adde(j, jolts[i+k])
                g[j][g[jolts[i+k]]] = 1
            else:
                break

    djolts = np.diff(jolts)
    print(sum(djolts == 1) * (sum(djolts == 3)))
    print(dfs_visit(g[0], dest=g[jolts[-1]]))


if __name__ == "__main__":
    main()
