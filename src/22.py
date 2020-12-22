#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np


def play_round(player1, player2):
    one = player1.popleft()
    two = player2.popleft()
    if one > two:
        player1.append(one)
        player1.append(two)
    elif one < two:
        player2.append(two)
        player2.append(one)
    return player1, player2

def play_game(player1, player2):
    player1 = collections.deque(player1)
    player2 = collections.deque(player2)
    while player1 and player2:
        player1, player2 = play_round(player1, player2)
    if player1:
        return player1
    elif player2:
        return player2

def recurse_combat(player1, player2, game=1):
    # this_game = game
    cache = set()
    cache.add((player1, player2))
    player1_deck = collections.deque(player1)
    player2_deck = collections.deque(player2)
    while player1_deck and player2_deck:
        one = player1_deck.popleft()
        two = player2_deck.popleft()
        new_tuple1 = tuple(player1_deck)
        new_tuple2 = tuple(player2_deck)
        if (new_tuple1, new_tuple2) in cache:
            return True, player1_deck, game
        cache.add((new_tuple1, new_tuple2))
        if len(player1_deck) >= one and len(player2_deck) >= two:
            game += 1
            does_one_win, _, game = recurse_combat(new_tuple1[:one], new_tuple2[:two], game)
        else:
            does_one_win = one > two
        # print("Game", this_game, ":", one, player1_deck, two, player2_deck, does_one_win)
        if does_one_win:
            player1_deck.append(one)
            player1_deck.append(two)
        else:
            player2_deck.append(two)
            player2_deck.append(one)
    if player1_deck:
        return True, player1_deck, game
    elif player2_deck:
        return False, player2_deck, game
    raise ValueError()

def main():
    with open('input/22.txt') as f:
        players = f.read().split('\n\n')
    player1 = list(map(int, (players[0].split('\n'))[1:]))
    player2 = list(map(int, (players[1].split('\n'))[1:]))
    result = play_game(player1, player2)
    print(sum(i*j for i, j in zip(reversed(list(result)), range(1, len(result)+1))))
    _, result2, num_games = recurse_combat(tuple(player1), tuple(player2))
    print(sum(i*j for i, j in zip(reversed(list(result2)), range(1, len(result2)+1))))
    print("Number of subgames played:", num_games)



if __name__ == "__main__":
    main()
