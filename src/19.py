#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np


def build_rule(key, in_dict, cache=dict()):
    if key in cache:
        return cache[key]
    rule = in_dict[key]
    if rule[0] == '"':
        token = rule[1]
        cache[key] = token
        return token
    tokens = rule.split()
    parsed = ["|" if t == "|" else build_rule(t, in_dict, cache) for t in tokens]
    if "|" in parsed:
        i = parsed.index("|")
        left = ''.join(parsed[:i])
        right = ''.join(parsed[i+1:])
        if left == right:
            new_rule = left
        else:
            new_rule = f"({left}|{right})"
    else:
        new_rule = "".join(parsed)
    cache[key] = new_rule
    return new_rule


def build_rule2(key, in_dict, cache=dict()):
    if key in cache:
        return cache[key]
    rule = in_dict[key]
    if rule[0] == '"':
        token = rule[1]
        cache[key] = token
        return token
    tokens = rule.split()
    if key == "8":
        base_rule = build_rule2(tokens[0], in_dict, cache)
        new_rule = f"({base_rule})+"
        cache[key] = new_rule
        return new_rule
    elif key == "11":
        base_left = build_rule2(tokens[0], in_dict, cache)
        base_right = build_rule2(tokens[1], in_dict, cache)
        new_rule = base_left + base_right
        # There's nothing a **finite** automaton can't handle if the input is
        # also finite!
        for i in range(3):
                new_rule = f"{base_left}({new_rule})?{base_right}"
        cache[key] = new_rule
        return new_rule
    parsed = ["|" if t == "|" else build_rule2(t, in_dict, cache) for t in tokens]
    if "|" in parsed:
        i = parsed.index("|")
        left = ''.join(parsed[:i])
        right = ''.join(parsed[i+1:])
        if left == right:
            new_rule = left
        else:
            new_rule = f"({left}|{right})"
    else:
        new_rule = "".join(parsed)
    cache[key] = new_rule
    return new_rule


def parse_rules(rules):
    rules_dict = dict()
    for r in rules:
        num, rule = r.split(': ')
        rules_dict[num] = rule
    return rules_dict


def main():
    with open('input/19.txt') as f:
        rules, msgs = f.read().split('\n\n')
    rules_dict = parse_rules(rules.split('\n'))
    msgs = msgs.split('\n')
    part_one = re.compile(build_rule("0", rules_dict))
    results = [False if re.fullmatch(part_one, m) is None else True for m in msgs]
    print(sum(results))
    part_two = re.compile(build_rule2("0", rules_dict))
    results = [False if re.fullmatch(part_two, m) is None else True for m in msgs]
    print(sum(results))
    


if __name__ == "__main__":
    main()
