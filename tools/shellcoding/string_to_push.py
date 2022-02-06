#!/bin/python3

import sys
import math


# exit if no parameter
if len(sys.argv) != 2:
    print("Requires a string")
    print("Usage: python3 string_to_push.py 'STRING'")
    sys.exit()

num_chars = len(sys.argv[1])
reversed_str = sys.argv[1][::-1]
index = math.ceil(len(sys.argv[1]) / 4) * 4


output = ""
hex_str = ""
dangerous = False
for i in range(0, index):
    if i < len(reversed_str):
        hex_str += hex(ord(reversed_str[i])).replace('0x', '')
    else:
        hex_str += "00"
        dangerous = True

    if (i + 1) % 4 == 0 and hex_str:
        output += "push 0x" + hex_str + "\t\t; \"" + reversed_str[(i + 1)-4:i+1] + "\"\n"
        hex_str = ""

# output to console and copy to clipboard
print(output)

if dangerous:
    print("WARNING, PADDING WITH NULLS, MAY WANT TO CHANGE YOUR STRING\n")
