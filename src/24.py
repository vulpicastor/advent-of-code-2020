#!/usr/bin/python3

import numpy as np


MOVEMENT = {
    "e": np.array([1, 0]),
    "w": np.array([-1, 0]),
    "ne": np.array([0, 1]),
    "sw": np.array([0, -1]),
    "nw": np.array([-1, 1]),
    "se": np.array([1, -1]),
}


def parse_tile(line):
    save = ""
    pos = np.zeros(2, dtype=np.int)
    for c in line:
        if c == "n" or c == "s":
            save = c
            continue
        if c == "e" or c == "w":
            pos += MOVEMENT[save+c]
            save = ""
    return pos


def step_conway(grid):
    new_shape = np.array(grid.shape) + np.array([2, 2])
    new_grid = np.zeros(new_shape, dtype=bool)
    new_grid[1:-1, 1:-1] = grid
    count_neigh = np.zeros_like(new_grid, dtype=np.int)
    for dx, dy in MOVEMENT.values():
        count_neigh[1+dy:new_shape[0]-1+dy,
                    1+dx:new_shape[1]-1+dx] += grid
    new_grid = (new_grid & (0 < count_neigh) & (count_neigh <= 2)) | (~new_grid & (count_neigh == 2))
    return new_grid, count_neigh


def iter_conway(init_grid, iter, step_func=step_conway):
    new_grid = init_grid
    for _ in range(iter):
        new_grid, _ = step_func(new_grid)
    return new_grid


def main():
    with open("input/24.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    black = set()
    for l in lines:
        pos = tuple(parse_tile(l))
        if pos in black:
            black.remove(pos)
        else:
            black.add(pos)
    print(len(black))

    init_offset = np.array([max(abs(p[1]) for p in black), max(abs(p[0]) for p in black)])
    initial_size = init_offset * 2 + 1
    init_grid = np.zeros(initial_size, dtype=bool)
    for pos in black:
        index = np.array(list(reversed(pos))) + init_offset
        init_grid[tuple(index)] = True
    print(np.sum(iter_conway(init_grid, 100)))


if __name__ == "__main__":
    main()
