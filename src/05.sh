#!/bin/bash

# "Part 1 one-liner:"
# printf '%d\n' $((2#"$(sed 's/[FL]/0/g;s/[BR]/1/g' < ${1} | sort -n | tail -n 1)"))

echo "ibase=2; $(sed 's/[FL]/0/g;s/[BR]/1/g' < ${1} | sort -n)" | bc > 05.txt
MIN=$(head -n 1 05.txt)
MAX=$(tail -n 1 05.txt)
echo $MIN $MAX
seq $MIN $MAX | comm --nocheck-order -23 - 05.dec.txt