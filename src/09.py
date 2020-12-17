#!/usr/bin/python3

import collections
import numpy as np

def checksum(prev, num):
    presort = list(prev)
    presort.sort()
    found = False
    for i, x in enumerate(presort[:-1]):
        for y in presort[i+1:]:
            if num == x + y:
                found = True
                break
        if found:
            break
    return found

def checklist(nums, use=25):
    buffer = collections.deque(nums[:use])
    for n in nums[use:]:
        if not checksum(buffer, n):
            return n
        buffer.popleft()
        buffer.append(n)
    return None

def rollsum(nums, sumto):
    for i, x in enumerate(nums[:-1]):
        tmpsum = x
        for j, y in enumerate(nums[i+1:]):
            tmpsum += y
            if tmpsum == sumto:
                return i, i+j+1



def main():
    with open("input/09.txt") as f:
        lines = [int(l.strip()) for l in f.readlines()]
    weaksum = checklist(lines, 25)
    print(weaksum)

    start, end = rollsum(lines, weaksum)
    weaknums = lines[start:end]
    print(min(weaknums) + max(weaknums))



if __name__ == "__main__":
    main()
