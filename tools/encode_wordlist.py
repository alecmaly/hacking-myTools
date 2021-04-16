#!/bin/python3
import base64
import urllib.parse
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-s', '--source', required=True)
parser.add_argument('-u' , '--urlencode', type=str2bool, nargs='?', const=True, default=False, help="URL Encode wordlist.")
parser.add_argument('-b' , '--base64encode', type=str2bool, nargs='?', const=True, default=False, help="Base64 encode wordlist.")
args = parser.parse_args()



counter = 1
filepath = args.source
with open(filepath, 'rb') as fp:
    lines = fp.readlines()
    for line in lines:
        line = line.strip()
        if args.base64encode:
            line = base64.b64encode(line)
        if args.urlencode:
            line = urllib.parse.quote(line)
        else:
            line = line.decode('utf-8')
        print(line) 

