import io
import re
import numpy as np

def count_trees(maze, dx, dy):
    limit = len(maze)
    y_lim = len(maze[0])
    move = np.array([dx, dy])
    start = np.copy(move)
    num_trees = 0
    while start[0] < limit:
        x = start[0]
        y = start[1] % y_lim
        if maze[x][y] == '#':
            num_trees += 1
        start += move
    return num_trees


def main():
    with open("03.txt") as f:
        maze = f.readlines()
    maze = [s.strip() for s in maze]
    check_list = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1],
    ]
    print(count_trees(maze, 1, 3))
    print(np.product([count_trees(maze, *l) for l in check_list]))

main()