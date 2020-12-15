#!/usr/bin/python3

import collections


def iter_game(nums, iter=2020):
    mem = collections.defaultdict(lambda: collections.deque([None, None], maxlen=2))
    for i, n in enumerate(nums):
        mem[n] = collections.deque([None, i], maxlen=2)
    last = nums[-1]
    for j in range(i+1, iter):
        if last in mem and mem[last][0] is None:
            last = 0
        else:
            diff = mem[last][1] - mem[last][0]
            last = diff
        mem[last].popleft()
        mem[last].append(j)
    return last


def main():
    test_cases = [
        [1,3,2],
        [2,1,3],
        [1,2,3],
        [2,3,1],
        [3,2,1],
        [3,1,2],
        [1,0,15,2,10,13],
    ]
    print(list(map(iter_game, test_cases)))
    print(list(map(lambda x: iter_game(x, 30000000), test_cases)))


if __name__ == "__main__":
    main()
