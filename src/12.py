#!/usr/bin/python3

import numpy as np


CMD_MAP = {
    "N": np.array([0, 1]),
    "S": np.array([0, -1]),
    "E": np.array([1, 0]),
    "W": np.array([-1, 0]),
}

HEADING_MAP = {
    0: "E",
    90: "N",
    180: "W",
    270: "S",
}


def step_cmd(pos, b, cmd, val):
    if cmd == "L" or cmd == "R":
        sign = +1 if cmd == "L" else -1
        b = (b + sign * val) % 360
        return pos, b
    if cmd == "F":
        pos += CMD_MAP[HEADING_MAP[b]] * val
        return pos, b
    pos += CMD_MAP[cmd] * val
    return pos, b

def iter_cmd(cmds):
    pos = np.zeros(2, dtype=float)
    b = 0
    for cmd, val in cmds:
        pos, b = step_cmd(pos, b, cmd, val)
        # print(pos, b)
    return pos, b


def rot_mat(angle):
    angle = np.radians(angle)
    sinA = np.sin(angle)
    cosA = np.cos(angle)
    return np.array([[cosA, -sinA],
                     [sinA, cosA]])

def step_cmd2(pos, way, cmd, val):
    if cmd == "L" or cmd == "R":
        sign = +1 if cmd == "L" else -1
        way = rot_mat(sign * val) @ way
        return pos, way
    if cmd == "F":
        pos += way * val
        return pos, way
    way += CMD_MAP[cmd] * val
    return pos, way

def iter_cmd2(cmds):
    pos = np.zeros(2, dtype=float)
    way = np.array([10., 1.])
    for cmd, val in cmds:
        pos, way = step_cmd2(pos, way, cmd, val)
        # print(pos, way)
    return pos, way


def main():
    with open("input/12.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    cmds = [(l[0], int(l[1:])) for l in lines]
    pos, _ = iter_cmd(cmds)
    print(np.sum(np.abs(pos)))
    pos, _ = iter_cmd2(cmds)
    print(np.sum(np.abs(pos)))


if __name__ == "__main__":
    main()
