#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np

def str_conway(grid):
    output = []
    lenz = grid.shape[0]
    for z, layer in enumerate(grid):
        output.append(f"z={z - lenz//2}")
        for row in layer:
            output.append(''.join('#' if v else '.' for v in row))
    return '\n'.join(output)

def step_conway(grid):
    new_shape = np.array(grid.shape) + 2
    new_grid = np.zeros(new_shape, dtype=bool)
    new_grid[1:-1, 1:-1, 1:-1] = grid
    count_neigh = np.zeros_like(new_grid, dtype=np.int)
    for dz, dy, dx in itertools.product([-1, 0, 1], repeat=3):
        if dz == 0 and dy == 0 and dx == 0:
            continue
        count_neigh[1+dz:new_shape[0]-1+dz,
                    1+dy:new_shape[1]-1+dy,
                    1+dx:new_shape[2]-1+dx] += grid
    new_grid = (new_grid & (2 <= count_neigh) & (count_neigh <= 3)) | (~new_grid & (count_neigh == 3))
    return new_grid, count_neigh

def step_conway_4d(grid):
    new_shape = np.array(grid.shape) + 2
    new_grid = np.zeros(new_shape, dtype=bool)
    new_grid[1:-1, 1:-1, 1:-1, 1:-1] = grid
    count_neigh = np.zeros_like(new_grid, dtype=np.int)
    for dw, dz, dy, dx in itertools.product([-1, 0, 1], repeat=4):
        if dw == 0 and dz == 0 and dy == 0 and dx == 0:
            continue
        count_neigh[1+dw:new_shape[0]-1+dw,
                    1+dz:new_shape[1]-1+dz,
                    1+dy:new_shape[2]-1+dy,
                    1+dx:new_shape[3]-1+dx] += grid
    new_grid = (new_grid & (2 <= count_neigh) & (count_neigh <= 3)) | (~new_grid & (count_neigh == 3))
    return new_grid, count_neigh

def iter_conway(init_grid, iter, step_func=step_conway):
    new_grid = init_grid
    for _ in range(iter):
        new_grid, _ = step_func(new_grid)
    return new_grid

def main():
    with open('input/17.txt') as f:
        lines = [[s == '#' for s in l.strip()] for l in f.readlines()]
    init_state = np.array([lines])
    new_state = iter_conway(init_state, 6)
    print(np.sum(new_state))
    init_state = np.array([init_state])
    new_state = iter_conway(init_state, 6, step_conway_4d)
    print(np.sum(new_state))


if __name__ == "__main__":
    main()
