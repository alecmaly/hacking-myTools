#!/usr/bin/python3
import magic
import sys

if not len(sys.argv) == 2 or sys.argv[1] == '':
    print(f"Usage: {sys.argv[0]} <file>")
    sys.exit()

try:

    print("File: \t" + sys.argv[1])
    print("From file: \t" + magic.from_file(sys.argv[1]))
    print("From Buffer: \t" + magic.from_buffer(open(sys.argv[1], "rb").read(2048)))
    print("MIME type: \t"  + magic.from_file(sys.argv[1], mime=True))
except Exception as e:
    print(e)
finally:
    print("")