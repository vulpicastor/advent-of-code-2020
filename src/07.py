#!/usr/bin/python3

import collections
import re
import secrets


class Node(collections.UserDict):

    def __init__(self):
        self.data = dict()
        self.key = secrets.token_bytes(8)

    def __hash__(self):
        return hash(self.key)


def dfs_visit(node, visited=set()):
    visited.add(node)
    for n in node:
        if n not in visited:
            dfs_visit(n, visited)
    return visited


def dfs_count(node, visited=dict()):
    if node in visited:
        return visited[node]
    if len(node) == 0:
        visited[node] = 1
        return 1
    counts = sum(d * dfs_count(n, visited) for n, d in node.items()) + 1
    visited[node] = counts
    return counts


def main():
    with open("input/07.txt") as f:
        lines = [l.strip().split(' contain ') for l in f.readlines()]
    graph1 = collections.defaultdict(Node)
    graph2 = collections.defaultdict(Node)
    for outer, inners in lines:
        outer = outer[:-5]
        inners = re.findall(r'(\d+) (\b.*?\b \b.*?\b) bags?[,.]', inners)
        for n, c in inners:
            graph1[c][graph1[outer]] = int(n)
            graph2[outer][graph2[c]] = int(n)
    print(len(dfs_visit(graph1['shiny gold'])) - 1)
    print(dfs_count(graph2['shiny gold']) - 1)


if __name__ == "__main__":
    main()
