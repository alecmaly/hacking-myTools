#!/bin/python3

import requests
import argparse
from bs4 import BeautifulSoup
from bs4 import Comment
import re
from termcolor import colored 

parser = argparse.ArgumentParser(description='python extract_comments.py -u url -c "PHPSession=test"')
parser.add_argument('-u', '--url', default='', required=True)
parser.add_argument('-c', '--cookies', required=False)
# not implemeted 
# parser.add_argument('-m', '--method', default='GET', required=False)
args = parser.parse_args()




# cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

# r = requests.get('http://cronos.htb/js/app.js', cookies=args.cookies)
r = requests.get(args.url, cookies=args.cookies)
html = r.text.encode('utf-8')
# print(html)

delimiter = "==================================================="
###### INPUT = HTML FILE



def print_banner(str, color='white'):
    print(colored(f"{delimiter}\n\t{str}\n{delimiter}\n", color))


# output
print_banner(args.url, 'green')


soup = BeautifulSoup(html, 'html.parser')

comments = soup.find_all(string=lambda text: isinstance(text, Comment))
if len(comments) > 0:
    print_banner('HTML COMMENTS', 'yellow')
for c in comments:
    print(c)
    print("{}".format(delimiter))
    c.extract()




###### INPUT = JS FILE
soup = BeautifulSoup(html, 'lxml')
regex = rb'(\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$)'
# regex = r'//.*'
comments = re.findall(regex, html, re.M)
comments = [x[0].decode('utf-8') for x in comments]

if len(comments) > 0:
    print_banner("CSS/JS/OTHER COMMENTS", 'yellow')
for c in comments:
    print(c)
    print(f"{delimiter}")




