#!/usr/bin/python3

import collections
import itertools
import functools
import operator as op
import re

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


def iter_seats(seats, step_func):
    old_seats = seats
    new_seats = step_func(seats)
    while new_seats != old_seats:
        old_seats = new_seats
        new_seats = step_func(old_seats)
    return new_seats


def main():
    with open("../input/11.txt") as f:
        seats = [list(l.strip()) for l in f.readlines()]
    print(sum(r.count('#') for r in iter_seats(seats, step_seat)))
    print(sum(r.count('#') for r in iter_seats(seats, step_seat2)))
    

if __name__ == "__main__":
    main()
