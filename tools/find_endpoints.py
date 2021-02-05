#!/bin/python3

import sys
import os
import re
import uuid
import requests

# url = 'http://192.168.143.106'
if (len(sys.argv) < 2):
    print('need url')
url = sys.argv[1]

uuid = str(uuid.uuid4())

# use requests library to follow redirect and get proper url
resp = requests.get(url)
url = resp.url

cmd = 'hakrawler -url {} -linkfinder -plain -depth 3'.format(url)
# print(cmd)
stream = os.popen(cmd)
output = stream.read()
output = output.split('\n')

new_output = []
# clean output
for line in output:
    newurl = ('/'.join(line.split(" from ")[1].split('/')[:-1]) + '/' + line.split(" from ")[0][1:-1]) if " from " in line else line
    newurl = re.sub('\/+', '/', newurl).replace(':/', '://').replace('/./', '/')

    if newurl not in new_output and newurl != '':
        new_output.append(newurl)


# print(new_output)
#output to file
tmp_file_path = '/tmp/{}.txt'.format(uuid)
with open(tmp_file_path, 'w') as f:
    for x in new_output:
        f.write("{}\n".format(x))

# get valid urls
cmd = "cat {}|sort|uniq | httpx -silent -mc 200,302 -status-code -content-length -no-color > {}-output; rm {}".format(tmp_file_path, tmp_file_path, tmp_file_path)
# print(cmd)
stream = os.popen(cmd)
output = stream.read()



# get valid urls
cmd = "cat {}-output |sort| uniq; rm {}-output".format(tmp_file_path, tmp_file_path)
# print(cmd)
stream = os.popen(cmd)
output = stream.read()
print(output)

