import re

import numpy as np


def check(passport):
    valid_field = True
    for f, g in FIELDS.items():
        if f not in passport:
            return False, False
        if not g(passport[f]):
            valid_field = False
    return True, valid_field

def parse(line):
    return {k: v for k, v in (p.split(':') for p in line.split())}


def hgt_check(hgt):
    if (m := re.fullmatch(r'([0-9]+)(in|cm)', hgt)) is None:
        return False
    v, u = m.group(1, 2)
    if u == 'cm':
        return 150 <= int(v) <= 193
    if u  == 'in':
        return 59 <= int(v) <= 76
    return False

def range_check(low, high):
    return lambda s: low <= int(s) <= high

def re_check(regex):
    return lambda s: re.fullmatch(regex, s) is not None

FIELDS = {
    "byr": range_check(1920, 2002),
    "iyr": range_check(2010, 2020),
    "eyr": range_check(2020, 2030),
    "hgt": hgt_check,
    "hcl": re_check(r'#[0-9a-f]{6}'),
    "ecl": lambda s: s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    "pid": re_check(r'[0-9]{9}'),
    # "cid",
}


def main():
    with open("../input/04.txt") as f:
        text = f.read()
    passports = re.split(r'\n\n+', text)
    results = [check(parse(l)) for l in passports]
    print("Total #:", len(passports))
    part1, part2 = np.sum(np.array(results), axis=0)
    print(f"Valid for Part 1: {part1}")
    print(f"Valid for Part 2: {part2}")

if __name__ == "__main__":
    main()
