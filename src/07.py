#!/usr/bin/python3

import re

import graph


DFS_MEMO = dict()
def dfs_count(node):
    if node in DFS_MEMO:
        return DFS_MEMO[node]
    if len(node) == 0:
        DFS_MEMO[node] = 1
        return 1
    counts = sum(d * dfs_count(n) for n, d in node.items()) + 1
    DFS_MEMO[node] = counts
    return counts

def main():
    with open("../input/07.txt") as f:
        lines = [l.strip().split(' contain ') for l in f.readlines()]
    edges = []
    edges2 = []
    for container, contains in lines:
        contain_color = container[:-5]
        contents = re.findall(r'(\d+) (\b.*?\b \b.*?\b) bags?[,.]', contains)
        for n, c in contents:
            edges.append((c, contain_color, int(n)))
            edges2.append((contain_color, c, int(n)))
    g = graph.Digraph(edges)
    _, parents = g['shiny gold'].dfs()
    print(len(parents) - 1)
    f = graph.Digraph(edges2)
    print(dfs_count(f['shiny gold']) - 1)

if __name__ == "__main__":
    main()
