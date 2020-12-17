#!/usr/bin/python3

import numpy as np


def run_code(instructions):
    pc = 0
    acc = 0
    length = len(instructions)
    visited = np.zeros(length+1, dtype=bool)
    while not visited[pc]:
        if pc >= length:
            break
        visited[pc] = True
        opcode, arg = instructions[pc]
        arg = int(arg)
        # print(opcode, arg)
        if opcode == 'acc':
            acc += arg
            pc += 1
            continue
        elif opcode == 'jmp':
            pc += arg
            continue
        elif opcode == 'nop':
            pc += 1
            continue
    return pc, acc


def main():
    with open("input/08.txt") as f:
        lines = [l.strip().split() for l in f.readlines()]
    length = len(lines)
    print(run_code(lines))
    for i, l in enumerate(lines):
        if l[0] == 'nop':
            new_code = list(lines)
            new_code[i] = ('jmp', l[1])
        if l[0] == 'jmp':
            new_code = list(lines)
            new_code[i] = ('nop', l[1])
        pc, acc = run_code(new_code)
        if pc == length:
            print(i, pc, acc)
            break


if __name__ == "__main__":
    main()
