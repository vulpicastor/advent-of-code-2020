#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import tqdm


class Cup(object):

    def __str__(self):
        return f"Cup({self.v})"

    def __repr__(self):
        return f"Cup({self.v}, {self.next!s}, {self.dec!s})"

    def __init__(self, value, next_node=None, dec_node=None):
        self.v = value
        self.next = next_node
        self.dec = dec_node

    def __iter__(self):
        current = self
        yield current
        while current.next is not None and current.next is not self:
            current = current.next
            yield current

    def insert_after(self, node):
        self.next = node.next
        node.next = self

    def pop_after(self):
        popped = self.next
        self.next = popped.next
        return popped

    def append(self, value):
        self.next = Cup(value, self, None)
        return self.next

def pop_cups_after(node, num=1):
    popped = []
    for _ in range(num):
        popped.append(node.pop_after())
    return popped

def insert_cups(insert_after, cups):
    for c in cups:
        c.insert_after(insert_after)
        insert_after = c

def find_value(start_at, value):
    while start_at.v != value:
        start_at = start_at.next
        if start_at is None:
            return None
    return start_at


def big_game(start_cup, min_val=1, max_val=1000000, steps=10000000):
    for _ in tqdm.tqdm(range(steps)):
        # print("".join(str(c.v) for c in start_cup))
        popped = pop_cups_after(start_cup, 3)
        insert_at = start_cup.dec
        while insert_at in popped:
            insert_at = insert_at.dec
        insert_cups(insert_at, popped)
        start_cup = start_cup.next
    # print("".join(str(c.v) for c in start_cup))
    return start_cup


def create_list(from_list, total=None):
    if total is None:
        total = len(from_list)
    start_node = Cup(from_list[0])
    end_node = start_node
    for i in itertools.chain(from_list[1:], range(len(from_list)+1, total+1)):
        next_node = end_node.append(i)
        next_node.dec = end_node
        end_node = next_node
    end_node.next = start_node
    next_node = start_node
    the_one = None
    for _ in range(len(from_list)+1):
        value = next_node.v
        if value == 1:
            the_one = next_node
            if total == len(from_list):
                the_one.dec = find_value(start_node, max(from_list))
            else:
                the_one.dec = end_node
            next_node = next_node.next
            continue
        next_node.dec = find_value(start_node, value-1)
        next_node = next_node.next
    return start_node, the_one


def main():
    # puzzle_input = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    puzzle_input = [7, 8, 9, 4, 6, 5, 1, 2, 3]
    start_node, the_one = create_list(puzzle_input)
    _ = big_game(start_node, max_val=max(puzzle_input), steps=100)
    print(puzzle_input)
    print("".join(str(c.v) for c in the_one))

    start_node, the_one = create_list(puzzle_input, total=1000000)
    _ = big_game(start_node, steps=10000000)
    print(the_one.next, the_one.next.next, the_one.next.v * the_one.next.next.v)


if __name__ == "__main__":
    main()
