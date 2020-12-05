#!/bin/bash

# Part 1 one-liner:
# printf '%d\n' $((2#"$(sed 's/[FL]/0/g;s/[BR]/1/g' < ${1} | sort -n | tail -n 1)"))

# `sed` replaces characters 'F' or 'L' with 0 and 'B' or 'R' with 1, turning
# seating into binary numbers. `ibase=2` tells the calculator `bc` that input
# numbers are binary.
echo "ibase=2; $(sed 's/[FL]/0/g;s/[BR]/1/g' < ${1} | sort -n)" | bc > 05.txt
MIN=$(head -n 1 05.txt)
MAX=$(tail -n 1 05.txt)
echo $MIN $MAX
# Because the input file is contiguous except for one number, use `seq` to
# generate a list of numbers to be compared by `comm`. `comm` complains when
# the input file is not in lexicographic order, so `--nocheck-order` suppresses
# the error.
seq $MIN $MAX | comm --nocheck-order -23 - 05.txt