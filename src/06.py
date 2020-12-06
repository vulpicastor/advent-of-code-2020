#!/usr/bin/python3

import functools
import operator as op

def main():
    with open("../input/06.txt") as f:
        lines = f.read()
    groups = lines.split('\n\n')
    bits = []
    for g in groups:
        ps = g.split()
        bits.append([
            sum(
                # This is essentially a counting sort of the answered questions
                1 << (ord(c) - ord('a')) for c in p
            ) for p in ps
        ])
    print([[bin(b) for b in a] for a in bits])
    # Counting if any person answered yes is bitwise or.
    part1 = (bin(b).count("1") for b in (functools.reduce(op.or_, a) for a in bits))
    print(sum(part1))
    # Counting if all persons answered yes is bitwise and.
    part2 = (bin(b).count("1") for b in (functools.reduce(op.and_, a) for a in bits))
    print(sum(part2))

if __name__ == "__main__":
    main()
