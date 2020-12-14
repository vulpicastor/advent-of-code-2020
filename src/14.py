#!/usr/bin/python3

import collections
import itertools
import functools
import operator as op
import re
import timeit

import numpy as np

def bitmask(mask):
    or_mask = int(re.sub(r'[X0]', '0', mask), base=2)
    and_mask = int(re.sub(r'[X1]', '1', mask), base=2)
    return or_mask, and_mask

def step_prog(cmd, val, mem, or_mask, and_mask):
    if cmd == 'mask':
       or_mask, and_mask = bitmask(val)
       return mem, or_mask, and_mask
    addr = int(re.sub(r'mem\[([0-9]+)\]', r'\1', cmd))
    val = int(val)
    mem[addr] = (val | or_mask) & and_mask
    return mem, or_mask, and_mask

def iter_prog(prog):
    or_mask = 0
    and_mask = ~0
    mem = dict()
    for cmd, val in prog:
        mem, or_mask, and_mask = step_prog(cmd, val, mem, or_mask, and_mask)
    return mem, or_mask, and_mask


def bitmask2(mask):
    or_mask = int(re.sub(r'[X0]', '0', mask), base=2)
    and_mask = re.sub(r'[01]', '1', mask)
    and_mask = int(re.sub(r'X', '0', and_mask), base=2)
    floating = []
    for i, n in enumerate(reversed(mask)):
        if n == 'X':
            floating.append(2**i)
    return or_mask, and_mask, floating

def step_prog2(cmd, val, mem, or_mask, and_mask, floating):
    if cmd == 'mask':
       or_mask, and_mask, floating = bitmask2(val)
       return mem, or_mask, and_mask, floating
    addr = int(re.sub(r'mem\[([0-9]+)\]', r'\1', cmd))
    val = int(val)
    new_addr = (addr | or_mask) & and_mask
    if floating:
        for bits in itertools.product([0, 1], repeat=len(floating)):
            mem[new_addr + sum(x*y for x, y in zip(bits, floating))] = val
    else:
        mem[new_addr] = val
    return mem, or_mask, and_mask, floating

def iter_prog2(prog):
    or_mask = 0
    and_mask = ~0
    floating = []
    mem = dict()
    for cmd, val in prog:
        mem, or_mask, and_mask, floating = step_prog2(cmd, val, mem, or_mask, and_mask, floating)
    return mem, or_mask, and_mask, floating

def main():
    with open("../input/14.txt") as f:
        lines = [l.strip().split(' = ') for l in f.readlines()]
    mem, _, _ = iter_prog(lines)
    print(sum(mem.values()))
    mem, _, _, _ = iter_prog2(lines)
    print(sum(mem.values()))


if __name__ == "__main__":
    main()
