#!/usr/bin/python3

import itertools

MODULUS = 20201227

def dh(base, sk):
    pk = 1
    for _ in range(sk):
        pk *= base
        pk %= MODULUS
    return pk

def brute(base, pk):
    value = 1
    for sk in itertools.count(0):
        if value == pk:
            return sk
        value *= base
        value %= MODULUS

def main():
    pk_card = 10604480
    pk_door = 4126658
    sk_card = brute(7, pk_card)
    # print(sk_card)
    # print(dh(7, sk_card))
    print(dh(pk_door, sk_card))

if __name__ == "__main__":
    main()
