#!/bin/python3


import sys
import requests
from statistics import mode

if len(sys.argv) != 2:
    print('Missing parameter for url')
    sys.exit()

url = sys.argv[1]
url = url + '/index'
# url = 'http://192.168.80.65/index'

# check .asp and .aspx pages?..
potential_extensions = ['', '.php', '.jsp', '.html', '.htm', '.asp', '.aspx']


results = []
for extension in potential_extensions:
    resp = requests.get(url+extension)
    results.append({'extension': extension, 'code':resp.status_code, 'size': len(resp.text)})

# print(mode([x['code'] for x in results]))
mode_code = mode([x['code'] for x in results])
mode_size = mode([x['size'] for x in results])

extensions = [x['extension'] for x in results if (x['code'] != mode_code or x['size'] != mode_size) and x['code'] == 200 ]

extensions.append('.txt')


print(','.join(extensions), end='')