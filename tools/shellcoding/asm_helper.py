#!/bin/usr/python3
import argparse
import os
import sys
import re
from pwn import *

parser = argparse.ArgumentParser()
parser.add_argument('--mode', '-m', required=True, choices=['asm', 'disasm'], help='asm | diasm (disassembles shellcode) -- dump-shellcode - dump shellcode from ELF')
parser.add_argument('--arch', '-a', default='i386', choices=['aarch64', 'alpha', 'amd64', 'arm', 'avr', 'cris', 'i386', 'ia64', 'm68k', 'mips', 'mips64', 'msp430', 'none', 'powerpc', 'powerpc64', 'riscv', 's390', 'sparc', 'sparc64', 'thumb', 'vax'], help='architecture: i386, aarch64, amd64, arm, mips')
#architectures= {'aarch64': {'bits': 64, 'endian': 'little'}, 'alpha': {'bits': 64, 'endian': 'little'}, 'amd64': {'bits': 64, 'endian': 'little'}, 'arm': {'bits': 32, 'endian': 'little'}, 'avr': {'bits': 8, 'endian': 'little'}, 'cris': {'bits': 32, 'endian': 'little'}, 'i386': {'bits': 32, 'endian': 'little'}, 'ia64': {'bits': 64, 'endian': 'big'}, 'm68k': {'bits': 32, 'endian': 'big'}, 'mips': {'bits': 32, 'endian': 'little'}, 'mips64': {'bits': 64, 'endian': 'little'}, 'msp430': {'bits': 16, 'endian': 'little'}, 'none': {}, 'powerpc': {'bits': 32, 'endian': 'big'}, 'powerpc64': {'bits': 64, 'endian': 'big'}, 'riscv': {'bits': 32, 'endian': 'little'}, 's390': {'bits': 32, 'endian': 'big'}, 'sparc': {'bits': 32, 'endian': 'big'}, 'sparc64': {'bits': 64, 'endian': 'big'}, 'thumb': {'bits': 32, 'endian': 'little'}, 'vax': {'bits': 32, 'endian': 'little'}}
parser.add_argument('--os', '-o', default='linux', choices= ['android', 'baremetal', 'cgc', 'freebsd', 'linux', 'windows'], help="operating system")
parser.add_argument('--input', '-i', required=False,default=(None if sys.stdin.isatty() else sys.stdin.readline().decode('utf-8')), help='shellcode, assembly instructions, or filepath. Accepts strings, not bytes (echo/printf decode and do not work, use -i)')
# parser.add_argument('--input', '-i', required=False,default=(None if sys.stdin.isatty() else sys.stdin.buffer.read()), help='shellcode, assembly instructions, or filepath')

args = parser.parse_args()
# print(args)
# set pwntools context
context.os = args.os
context.arch = args.arch

if args.mode == 'asm':
    if os.path.exists(args.input):
        args.input = open(args.input, 'r').read()

    # replace comments from assembly
    # args.input = re.sub(r';.*', '', args.input)

    print("\n[+] assembly")
    print(disasm(asm(args.input)))
    print('\n[+] shellcode')
    print(asm(args.input))

    print(f"\n[+] Shellcode Length: {len(asm(args.input))}")

    if b'\x00' in asm(args.input):
        print("\n[!] Beware, shellcode includes null bytes!") 
    else: 
        print("\n[+] No NULL bytes detected in shellcode... nice!") 
    

if args.mode == 'disasm':
    if os.path.exists(args.input):
        args.input = open(args.input, 'rb').read()
    else:
        # remove characters: \x, 0x, " 
        args.input = re.sub(r'\\x|0x|\"| ', '', args.input)
        args.input = unhex(args.input)

        
    print("\n[+] Disassembly")
    print(disasm(args.input))

    print(f"\n[+] Length: {len(args.input)}")

    if b"\x00" in args.input:
        print("[!] You have nulls, try again.")
    else: 
        print("\n[+] No NULL bytes detected in shellcode... nice!") 
