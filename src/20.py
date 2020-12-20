#!/usr/bin/python3

import collections
import copy
import functools
import itertools
import operator as op
import re

import numpy as np
import scipy.signal as signal


def str_img(img):
    return '\n'.join(''.join('#' if px else '.' for px in r) for r in img)

def read_tile(tile):
    tlines = tile.split('\n')
    idnum = int(re.sub(r'Tile (\d+):', r'\1', tlines[0]))
    tile_array = np.array([[px == '#' for px in l] for l in tlines[1:]])
    edges = [
        tuple(tile_array[0]),
        tuple(tile_array[-1]),
        tuple(tile_array[:, 0]),
        tuple(tile_array[:, -1]),
    ]
    return idnum, tile_array, edges

def flip_edges(edges):
    return [tuple(reversed(e)) for e in edges]


CORNER_EDGE_MATCH = dict({
    (1, 3): 0,
    (1, 2): 1,
    (0, 3): 2,
    (0, 2): 3,
})

def find_corner_ids(id_to_edges, tile_edges):
    corner_ids = []
    which_corner = []
    for i, edges in id_to_edges.items():
        count = 0
        which_edges = []
        for j, e in enumerate(edges):
            if tile_edges[e] - {i}:
                count += 1
                which_edges.append(j)
        if count == 2:
            which_edges.sort()
            which_corner.append(CORNER_EDGE_MATCH[tuple(which_edges)])
            corner_ids.append(i)
    return corner_ids, which_corner


def find_top_edge_match(id_to_match, edge, tile_edges, tile_arrays):
    found_array_id = tile_edges[tuple(edge)] - {id_to_match}
    if not found_array_id:
        return None
    found_array_id = found_array_id.pop()
    found_array = tile_arrays[found_array_id]
    # print(found_array)
    if np.all(edge == found_array[0]):
        flipped_array = found_array
    elif np.all(edge == found_array[0, ::-1]):
        flipped_array = found_array[::1, ::-1]
    elif np.all(edge == found_array[-1]):
        flipped_array = found_array[::-1, ::1]
    elif np.all(edge == found_array[-1, ::-1]):
        flipped_array = found_array[::-1, ::-1]
    elif np.all(edge == found_array.T[0]):
        flipped_array = found_array.T
    elif np.all(edge == found_array.T[0, ::-1]):
        flipped_array = found_array.T[::1, ::-1]
    elif np.all(edge == found_array.T[-1]):
        flipped_array = found_array.T[::-1, ::1]
    elif np.all(edge == found_array.T[-1]):
        flipped_array = found_array.T[::-1, ::-1]
    bottom_edge = flipped_array[-1]
    right_edge = flipped_array[:, -1]
    return found_array_id, flipped_array[1:-1, 1:-1], bottom_edge, right_edge


def find_left_edge_match(id_to_match, edge, tile_edges, tile_arrays):
    found_array_id = tile_edges[tuple(edge)] - {id_to_match}
    if not found_array_id:
        return None
    found_array_id = found_array_id.pop()
    found_array = tile_arrays[found_array_id]
    # print(found_array)
    if np.all(edge == found_array[:, 0]):
        flipped_array = found_array
    elif np.all(edge == found_array[::-1, 0]):
        flipped_array = found_array[::-1, ::1]
    elif np.all(edge == found_array[:, -1]):
        flipped_array = found_array[::1, ::-1]
    elif np.all(edge == found_array[::-1, -1]):
        flipped_array = found_array[::-1, ::-1]
    if np.all(edge == found_array.T[:, 0]):
        flipped_array = found_array.T
    elif np.all(edge == found_array.T[::-1, 0]):
        flipped_array = found_array.T[::-1, ::1]
    elif np.all(edge == found_array.T[:, -1]):
        flipped_array = found_array.T[::1, ::-1]
    elif np.all(edge == found_array.T[::-1, -1]):
        flipped_array = found_array.T[::-1, ::-1]
    right_edge = flipped_array[:, -1]
    return found_array_id, flipped_array[1:-1, 1:-1], right_edge
    

def solve_jigsaw(topleft_id, tile_arrays, tile_edges):
    id_left = set(tile_arrays.keys())
    starting_tile = tile_arrays[topleft_id]
    block_array = [[starting_tile[1:-1, 1:-1]]]
    right_edges = [(topleft_id, starting_tile[:, -1])]
    last_id = topleft_id
    id_left.remove(topleft_id)
    last_bottom_edge = starting_tile[-1]
    while True:
        # print(last_id, last_bottom_edge)
        result = find_top_edge_match(last_id, last_bottom_edge, tile_edges, tile_arrays)
        if result is None:
            break
        last_id, flipped_array, last_bottom_edge, right_edge = result
        id_left.remove(last_id)
        block_array.append([flipped_array])
        right_edges.append((last_id, right_edge))
    for row, (last_id, last_right_edge) in zip(block_array, right_edges):
        while True:
            result = find_left_edge_match(last_id, last_right_edge, tile_edges, tile_arrays)
            if result is None:
                break
            last_id, flipped_array, last_right_edge = result
            id_left.remove(last_id)
            row.append(flipped_array)
    if id_left:
        raise ValueError()
    return np.block(block_array)


SEA_MONSTER = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
])
MONSTER_SUM = np.sum(SEA_MONSTER)

def hicne_sunt_dracones(img):
    return np.sum(
        signal.correlate2d(img, SEA_MONSTER, "valid") == MONSTER_SUM)


def dihedral_yeet(img):
    for i, j in itertools.product([1, -1], repeat=2):
        yield img[::i, ::j]
        yield img.T[::i, ::j]


def main():
    with open('input/20.txt') as f:
        tiles = f.read().split('\n\n')
    tile_arrays = dict()
    id_to_edges = dict()
    tile_edges = collections.defaultdict(set)
    for t in tiles:
        idnum, tile_array, edges = read_tile(t)
        tile_arrays[idnum] = tile_array
        id_to_edges[idnum] = edges
        for e in edges:
            tile_edges[e].add(idnum)
        for e in flip_edges(edges):
            tile_edges[e].add(idnum)
    corner_ids, which_corner = find_corner_ids(id_to_edges, tile_edges)
    print(np.product(corner_ids))
    whole_picture = solve_jigsaw(
        corner_ids[which_corner.index(0)],
        tile_arrays,
        tile_edges,
    )
    for flipped in dihedral_yeet(whole_picture):
        if (monster_count := hicne_sunt_dracones(flipped)) > 0:
            break
    print(np.sum(whole_picture) - monster_count * MONSTER_SUM)


if __name__ == "__main__":
    main()
