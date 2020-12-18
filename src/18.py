#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np


OP_MAP = {
    "+": op.add,
    "*": op.mul,
}

OP_PREC = {
    "+": 3,
    "*": 2,
}

OP_PREC_1 = {
    "+": 2,
    "*": 2,
}


def eval_postfix(stack):
    out_stack = []
    for token in stack:
        if token in "123456789":
            out_stack.append(int(token))
            continue
        x = out_stack.pop()
        y = out_stack.pop()
        out_stack.append(OP_MAP[token](x, y))
    return out_stack


def parse_postfix(expr, precedence=OP_PREC):
    stack = []
    shunting = []
    for token in expr:
        if token == " ":
            continue
        if token == "(":
            shunting.append(token)
        elif token == ")":
            while shunting:
                if (op_token := shunting.pop()) == "(":
                    break
                stack.append(op_token)
        elif token in "+*":
            while shunting:
                op_token = shunting.pop()
                if op_token == "(" or precedence[op_token] < precedence[token]:
                    shunting.append(op_token)
                    break
                stack.append(op_token)
            shunting.append(token)
        elif token in "123456789":
            stack.append(token)
    while shunting:
        stack.append(shunting.pop())
    return stack


def main():
    with open('input/18.txt') as f:
        lines = [l.strip() for l in f.readlines()]
    print(np.sum([eval_postfix(parse_postfix(l, precedence=OP_PREC_1)) for l in lines]))
    print(np.sum([eval_postfix(parse_postfix(l)) for l in lines]))


if __name__ == "__main__":
    main()
