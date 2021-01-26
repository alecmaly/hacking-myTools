#!/bin/python3

import requests
import argparse
from bs4 import BeautifulSoup
from bs4 import Comment
import re
from termcolor import colored 

parser = argparse.ArgumentParser(description='python extract_comments.py -u url -c "PHPSession=test"')
parser.add_argument('-u', '--url', default='', required=False)
parser.add_argument('-f', '--file', default='', required=False)
parser.add_argument('-c', '--cookies', required=False)
# not implemeted 
# parser.add_argument('-m', '--method', default='GET', required=False)
args = parser.parse_args()
if args.url == "" and args.file == "":
    parser.error("--url or --file is required")



def scanurl(url):
        

    cookies = dict(PHPSESSID="51adc8f5da18e5854e658f4019eeeec6")

    # r = requests.get('http://cronos.htb/js/app.js', cookies=args.cookies)
    r = requests.get(url, cookies=args.cookies, verify=False)
    html = r.text.encode('utf-8')
    # print(html)

    delimiter = "==================================================="
    ###### INPUT = HTML FILE



    def print_banner(str, color='white'):
        print(colored(f"{delimiter}\n\t{str}\n{delimiter}\n", color))


    # output
    print_banner(url, 'green')


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




if args.url:
    scanurl(args.url)

if args.file:
    with open(args.file) as f:
        for line in f:
            try:
                scanurl(line.strip())
            except:
                print(f"Could not scan: {line.strip()}")
