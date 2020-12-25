#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np

def partone(nearby, ranges):
    nearby = [n for t in nearby for n in t]
    invalid = filter(lambda n: not check_ranges(n, ranges), nearby)
    return list(invalid)

def parttwo_filter(nearby, ranges):
    invalid = filter(lambda l: all(check_ranges(n, ranges) for n in l), nearby)
    return list(invalid)

def partwo(valids, ranges):
    valids = np.array(valids)
    results = np.zeros((ranges.shape[0],) + valids.shape, dtype=bool)
    for i, x in enumerate(ranges):
        results[i, ...] = (x[0] <= valids) & (valids <= x[1])
    num_headers = ranges.shape[0] // 2
    reshaped_results = results.reshape((num_headers, 2) + valids.shape)
    header_by_field = np.all(np.any(reshaped_results, axis=1), axis=1)
    header_to_field = np.zeros(num_headers, dtype=np.int)
    for _ in range(num_headers):
        # Iteratively, find the only column with one True, and set that entire
        # row to False.
        header, fields = np.nonzero(header_by_field)
        unique_fields, first_occur, match_header_counts = np.unique(
            fields, return_index=True, return_counts=True)
        found_unique_index = np.argmin(match_header_counts)
        found_unique_field = unique_fields[found_unique_index]
        found_unique_header = header[first_occur[found_unique_index]]
        header_to_field[found_unique_header] = found_unique_field
        header_by_field[found_unique_header, :] = False
        header_by_field[:, found_unique_field] = False
    return header_to_field

def check_ranges(num, ranges):
    for a, b in ranges:
        if a <= num <= b:
            return True
    return False

def parse_rules(rules):
    ranges = re.findall(r'\b[0-9]+-[0-9]+\b', rules)
    headers = re.findall(r'(?m)^.*:', rules)
    ranges = np.array([list(map(int, s.split('-'))) for s in ranges])
    return ranges, headers

def main():
    with open('input/16.txt') as f:
        rules, your, nearby = f.read().split('\n\n')
    ranges, headers = parse_rules(rules)
    print(headers)
    your = your.split('\n')[1]
    your = np.array(list(map(int, your.split(','))))
    nearby = nearby.strip().split('\n')
    nearby = [list(map(int, t.split(','))) for t in nearby[1:]]
    print(sum(partone(nearby, ranges)))
    valids = np.array(parttwo_filter(nearby, ranges))
    np.set_printoptions(linewidth=150)
    header_to_field = partwo(valids, ranges)
    print(np.product(your[header_to_field][:6]))



if __name__ == "__main__":
    main()
