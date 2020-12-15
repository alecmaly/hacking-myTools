#!/usr/bin/python

from boofuzz import *

host = '192.168.1.19'	#windows VM
port = 9999		#vulnserver port


session = Session(target = Target(connection = SocketConnection(host, port, proto='tcp')))

s_initialize("STATS")	#just giving our session a name, "STATS"

s_string("STATS", fuzzable = False)	#these strings are fuzzable by default, so here instead of blank, we specify 'false'
s_delim(" ", fuzzable = False)		#we don't want to fuzz the space between "STATS" and our arg
s_string("FUZZ")			#This value is arbitrary as we did not specify 'False' for fuzzable. Boofuzz will fuzz this string now

session.connect(s_get("STATS"))		#having our 'session' variable connect following the guidelines we established in "STATS"
session.fuzz()				#calling this function actually performs the fuzzing

