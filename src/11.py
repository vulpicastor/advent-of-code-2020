#!/usr/bin/python3

import collections
import itertools
import functools
import operator as op
import re
import timeit

import numpy as np


def step_seat(seats):
    nrows = len(seats)
    ncols = len(seats[0])
    new_seats = []
    for i, row in enumerate(seats):
        new_row = []
        for j, s in enumerate(row):
            if s == '.':
                new_row.append('.')
                continue
            occupied = 0
            for di, dj in itertools.product([-1, 0, 1], repeat=2):
                if di == 0 and dj == 0:
                    continue
                if 0 <= (i+di) < nrows and 0 <= (j+dj) < ncols:
                    # print(seats[i+di])
                    if seats[i+di][j+dj] == '#':
                        occupied += 1
            if s == 'L' and occupied == 0:
                t = '#'
            elif s == '#' and occupied >= 4:
                t = 'L'
            else:
                t = s
            new_row.append(t)
        new_seats.append(new_row)
    return new_seats

def step_seat2(seats):
    nrows = len(seats)
    ncols = len(seats[0])
    new_seats = []
    for i, row in enumerate(seats):
        new_row = []
        for j, s in enumerate(row):
            if s == '.':
                new_row.append('.')
                continue
            occupied = 0
            for di, dj in itertools.product([-1, 0, 1], repeat=2):
                if di == 0 and dj == 0:
                    continue
                newi = i + di
                newj = j + dj
                while 0 <= newi < nrows and 0 <= newj < ncols:
                    if seats[newi][newj] == '.':
                        newi += di
                        newj += dj
                        continue
                    if seats[newi][newj] == '#':
                        occupied += 1
                    break
            if s == 'L' and occupied == 0:
                t = '#'
            elif s == '#' and occupied >= 5:
                t = 'L'
            else:
                t = s
            new_row.append(t)
        new_seats.append(new_row)
    return new_seats

def parse_seats(seats):
    nrows = len(seats)
    ncols = len(seats[0])
    seats_array  = np.zeros((nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            if seats[i][j] == '#':
                seats_array[i, j] = 1
                continue
            if seats[i][j] == 'L':
                seats_array[i, j] = 0
                continue
            if seats[i][j] == '.':
                seats_array[i, j] = -1
                continue
    return seats_array

def step_seat_fast(seats, out=None):
    if out is None:
        count_occupied = np.zeros_like(seats)
    else:
        count_occupied = out
    tmp_seats = seats > 0
    for left, right in zip(
        itertools.product([slice(-1), slice(None), slice(1, None)], repeat=2),
        itertools.product([slice(1, None), slice(None), slice(-1)], repeat=2),
    ):
        if left == (slice(None), slice(None)) and right == (slice(None), slice(None)):
            continue
        count_occupied[left] += tmp_seats[right]
    count_occupied[seats>0] = count_occupied[seats>0] < 4
    count_occupied[seats==0] = count_occupied[seats==0] == 0
    count_occupied[seats<0] = -1
    return count_occupied

def gen_check_indices_2(seats):
    nrows, ncols = seats.shape
    indices = [[([], []) for _ in range(ncols)] for _ in range(nrows)]
    with np.nditer(seats, flags=['multi_index']) as it:
        for x in it:
            if x < 0:
                continue
            i, j = it.multi_index
            for di, dj in itertools.product(range(-1, 2), repeat=2):
                if di == 0 and dj == 0:
                    continue
                newi = i + di
                newj = j + dj
                while 0 <= newi < nrows and 0 <= newj < ncols:
                    if seats[newi, newj] >= 0:
                        indices[newi][newj][0].append(i)
                        indices[newi][newj][1].append(j)
                        break
                    newi += di
                    newj += dj
    return indices

def step_seat2_fast(seats, check_indices, out=None):
    if out is None:
        count_occupied = np.zeros_like(seats)
    else:
        count_occupied = out
    for i, row in enumerate(check_indices):
        for j, indices in enumerate(row):
            if indices:
                count_occupied[i, j] = np.sum(seats[indices])
    count_occupied[seats>0] = count_occupied[seats>0] < 5
    count_occupied[seats==0] = count_occupied[seats==0] == 0
    return count_occupied


def iter_seats(seats, step_func):
    old_seats = seats
    new_seats = step_func(seats)
    while np.any(new_seats != old_seats):
        old_seats = new_seats
        new_seats = step_func(old_seats)
    return new_seats

def iter_seats_fast(seats, step_func):
    old_seats = np.copy(seats)
    new_seats = step_func(seats)
    while np.any(new_seats != old_seats):
        new_seats, old_seats = old_seats, new_seats
        step_func(old_seats, new_seats)
    return new_seats

def iter_seats2_fast(seats):
    check_indices = gen_check_indices_2(seats)
    # print(check_indices)
    old_seats = np.copy(seats)
    new_seats = step_seat2_fast(seats, check_indices)
    while np.any(new_seats != old_seats):
        new_seats, old_seats = old_seats, new_seats
        step_seat2_fast(old_seats, check_indices, new_seats)
    return new_seats

def main():
    with open("input/11.txt") as f:
        seats = [list(l.strip()) for l in f.readlines()]
    long_repeat = 1
    short_repeat = 1
    print(
        timeit.timeit(
            lambda: sum(r.count('#') for r in iter_seats(seats, step_seat)),
            number=long_repeat,
        ) / long_repeat,
        "seconds;",
        long_repeat,
        "loops"
    )
    parsed_seats = parse_seats(seats)
    print(
        timeit.timeit(
            lambda: np.sum(iter_seats_fast(parsed_seats, step_seat_fast) > 0),
            number=short_repeat,
        ) / short_repeat,
        "seconds;",
        short_repeat,
        "loops"
    )

    print(
        timeit.timeit(
            lambda: sum(r.count('#') for r in iter_seats(seats, step_seat2)),
            number=long_repeat,
        ) / long_repeat,
        "seconds;",
        long_repeat,
        "loops"
    )

    print(
        timeit.timeit(
            lambda: np.sum(iter_seats2_fast(parsed_seats) > 0),
            number=short_repeat,
        ) / short_repeat,
        "seconds;",
        short_repeat,
        "loops"
    )
    

if __name__ == "__main__":
    main()
