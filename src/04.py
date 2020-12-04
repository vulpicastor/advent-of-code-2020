import collections
import functools
import itertools
import operator as op
import os
import sys
import re
import timeit

import numpy as np

def check(passport):
    for f, g in FIELDS.items():
        if f not in passport:
            return False
        if not g(passport[f]):
            return False
        print(f, passport[f])
    return True

def parse(line):
    return {k: v for k, v in (p.split(':') for p in line.split())}

def hgt_check(hgt):
    if len(hgt) < 3:
        return False
    if hgt[-2:] == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    if hgt[-2:] == 'in':
        return 59 <= int(hgt[:-2]) <= 76
    return False

FIELDS = {
    "byr": lambda s: True if 1920 <= int(s) <= 2002 else False,
    "iyr": lambda s: True if 2010 <= int(s) <= 2020 else False,
    "eyr": lambda s: True if 2020 <= int(s) <= 2030 else False,
    "hgt": hgt_check,
    "hcl": lambda s: re.match(r'^#[0-9a-f]{6}$', s),
    "ecl": lambda s: s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    "pid": lambda s: re.match(r'^[0-9]{9}$', s),
    # "cid",
}

def main():
    with open("../input/04.txt") as f:
    # with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    passports = []
    buffer = []
    for l in lines:
        if not l:
            if buffer:
                passports.append(" ".join(buffer))
                buffer = []
            continue
        buffer.append(l)
    if buffer:
        passports.append(" ".join(buffer))
    # print(passports)
    print(parse(l))
    results = [check(parse(l)) for l in passports]
    print('\n'.join(map(str, zip(results, passports))))
    print(len(passports))
    print(sum(results))

if __name__ == "__main__":
    main()
