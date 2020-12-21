#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np


def find_suspects(all_allergens, all_ingredients, pairs):
    suspects = set()
    dangerous = dict()
    for allergen in all_allergens:
        to_eliminate = all_ingredients.copy()
        for a, i in pairs:
            if allergen in a:
                to_eliminate &= i
        suspects |= to_eliminate
        dangerous[allergen] = to_eliminate
    return suspects, dangerous


def final_match(dangerous):
    final_dangerous = dict()
    eliminated = set()
    while dangerous:
        for k, v in dangerous.items():
            v -= eliminated
            if len(v) == 1:
                break
        found = v.pop()
        final_dangerous[found] = k
        eliminated.add(found)
        del dangerous[k]
    return final_dangerous


def parse_ingredients(line):
    separate = line.split(' (contains ')
    ingredients = set(separate[0].split())
    if len(separate) == 2:
        allergens = set(separate[1][:-1].split(', '))
    elif len(separate) == 1:
        allergens = set() 
    return allergens, ingredients


def main():
    with open('input/21.txt') as f:
        lines = [l.strip() for l in f.readlines()]
    pairs = [parse_ingredients(l) for l in lines]
    all_allergens = set()
    all_ingredients = set()
    ingredients_repeat = []
    for a, i in pairs:
        all_allergens |= a
        all_ingredients |= i
        ingredients_repeat.append(i)
    suspects, dangerous = find_suspects(all_allergens, all_ingredients, pairs)
    not_suspect = all_ingredients - suspects
    occurrences = sum([i in not_suspect for i in itertools.chain.from_iterable(ingredients_repeat)])
    print(occurrences)
    dangerous_match = final_match(dangerous)
    dangerous_list = list(dangerous_match.keys())
    dangerous_list.sort(key=lambda k: dangerous_match[k])
    print(','.join(dangerous_list))


if __name__ == "__main__":
    main()
