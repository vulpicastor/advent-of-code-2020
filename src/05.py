#!/usr/bin/python3

import re

import numpy as np


def decode_seat(seat):
    seat = re.sub(r'[BR]', '1', seat)
    seat = re.sub(r'[FL]', '0', seat)
    return int(seat, base=2)

def main():
    with open("input/05.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    seats = [
        'BFFFBBFRRR',
        'FFFBBBFRRR',
        'BBFFBBFRLL',
    ]
    print(list(map(decode_seat, seats)))
    # print(list(map(decode_seat, lines)))
    ids = list(map(decode_seat, lines))
    ids = np.sort(ids)
    print("Part 1:")
    print(ids[-1])
    print("Part 2:")
    print(ids[:-1][np.diff(ids) == 2] + 1)
    

if __name__ == "__main__":
    main()
