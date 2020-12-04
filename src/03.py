import numpy as np
import timeit

def count_trees(maze, dx, dy):
    x_lim = len(maze)
    y_lim = len(maze[0])
    x = dx
    y = dy
    num_trees = 0
    while x < x_lim:
        if maze[x][y % y_lim] == '#':
            num_trees += 1
        x += dx
        y += dy
    return num_trees


def main():
    with open("../input/03.txt") as f:
        maze = f.readlines()
    maze = [s.strip() for s in maze]
    check_list = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1],
    ]
    timeit_num = 1000
    print(
        timeit.timeit(lambda: count_trees(maze, 1, 3), number=timeit_num)
        / timeit_num)
    print(count_trees(maze, 1, 3))
    print(timeit.timeit(
        lambda: np.product([count_trees(maze, *l) for l in check_list]),
        number=1000,
    ) / timeit_num)
    print(np.product([count_trees(maze, *l) for l in check_list]))

main()
