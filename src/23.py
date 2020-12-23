#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import tqdm


def step_game(cups):
    choose_cup = cups[0]
    min_cup = min(cups[4:])
    insert_cup = choose_cup - 1 if choose_cup-1 >= min_cup else max(cups[4:])
    while True:
        try:
            insert_after = cups.index(insert_cup, 4)
            break
        except ValueError:
            insert_cup -= 1
            continue
    new_cups = cups[4:insert_after+1]
    new_cups.extend(cups[1:4])
    new_cups.extend(cups[insert_after+1:])
    new_cups.append(choose_cup)
    return new_cups

def iter_game(cups, steps=100):
    for _ in range(steps):
        cups = step_game(cups)
    return cups

class Cup(object):

    def __str__(self):
        return f"Cup({self.v})"
    
    def __repr__(self):
        return f"Cup({self.v}, {self.prev!s}, {self.next!s}, {self.dec!s})"
    
    def __init__(self, value, prev_node=None, next_node=None, dec_node=None):
        self.v = value
        self.prev = prev_node
        if self.prev is not None:
            self.prev.next = self
        self.next = next_node
        if self.next is not None:
            self.next.prev = self
        self.dec = dec_node
    
    def __hash__(self):
        return hash(self.v)
    
    def insert_after(self, node):
        self.prev = node
        self.next = node.next
        node.next = self
        if self.next is not None:
            self.next.prev = self
    
    def pop(self):
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        return self
    
    def append(self, value):
        self.next = Cup(value, self, None)
        return self.next

def pop_cups(node, num=1):
    popped = []
    for _ in range(num):
        popped.append(node.pop())
        node = node.next
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

def find_value_backwards(start_at, value):
    while start_at.v != value:
        start_at = start_at.next
        if start_at is None:
            return None
    return start_at

def find_value_simul(start_at, value):
    if start_at is None:
        return None
    if start_at.v == value:
        return None
    forward = start_at.next
    backward = start_at.prev
    while forward.v != value and backward.v != value:
        forward = forward.next
        backward = backward.prev
    if forward.v == value:
        return forward
    return backward

def search_at(starting_pos, value):
    for c in starting_pos:
        if c.v == value:
            return c
    visited = set(starting_pos)
    forwards = list(starting_pos)
    backwards = list(starting_pos)
    new_forwards = []
    new_backwards = []
    while True:
        new_forwards.clear()
        new_backwards.clear()
        if not forwards and not backwards:
            return None
        for c in forwards:
            if c.next in visited:
                continue
            if c.next.v == value:
                return c.next
            visited.add(c.next)
            new_forwards.append(c.next)
        for c in backwards:
            if c.prev in visited:
                continue
            if c.prev.v == value:
                return c.prev
            visited.add(c.prev)
            new_backwards.append(c.prev)
        forwards, new_forwards = new_forwards, forwards
        backwards, new_backwards = new_backwards, backwards
        # print(forwards, backwards)


def big_game(start_cup, min_val=1, max_val=1000000, steps=10000000):
    for _ in tqdm.tqdm(range(steps)):
        popped = pop_cups(start_cup.next, 3)
        insert_at = start_cup.dec
        while insert_at in popped:
            insert_at = insert_at.dec
        insert_cups(insert_at, popped)
        start_cup = start_cup.next
    return start_cup


def main():
    # puzzle_input = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    puzzle_input = [7, 8, 9, 4, 6, 5, 1, 2, 3]
    # print(iter_game(puzzle_input, 100))
    # result = iter_game(puzzle_input, 10000000)
    # one_is_at = result.index(1)
    # print(result[one_is_at+1:one_is_at+3])
    # print(result[one_is_at+1] * result[one_is_at+2])
    start_node = Cup(puzzle_input[0])
    end_node = start_node
    for i in itertools.chain(puzzle_input[1:], range(10, 1000001)):
        next_node = end_node.append(i)
        next_node.dec = end_node
        end_node = next_node
    print(i)
    next_node = start_node
    the_one = None
    for _ in range(len(puzzle_input)+1):
        value = next_node.v
        if value == 1:
            the_one = next_node
            next_node = next_node.next
            continue
        next_node.dec = find_value(start_node, value-1)
        next_node = next_node.next
    end_node.next = start_node
    start_node.prev = end_node
    the_one.dec = end_node
    next_node = start_node
    _ = big_game(start_node)
    print(puzzle_input)
    print(the_one.next, the_one.next.next)
    print(the_one.next.v * the_one.next.next.v)





if __name__ == "__main__":
    main()
