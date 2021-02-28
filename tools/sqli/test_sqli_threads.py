import Burpee.burpee as burpee
import requests
import argparse
import statistics
import re
import logging
import math
import logging
import queue
import threading
from threading import Thread, Lock
lock = Lock()
logging.basicConfig(level=logging.INFO)

# https://github.com/xscorp/Burpee

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#  parse args
parser = argparse.ArgumentParser(description='python testsqli.py -u url -r request.req -w wordlist')
parser.add_argument('-u', '--url', default='', required=True)
parser.add_argument('-r', '--request', required=True)
parser.add_argument('-w', '--wordlist', default='/opt/SecLists/Fuzzing/SQLi/Generic-SQLi.txt',required=False)
parser.add_argument('-t', '--threads', default=3,required=False)

args = parser.parse_args()
args.url = re.sub('/*$', '', args.url)  # strip trailing / on url





# build wordlist
payloads = queue.Queue()
with open(args.wordlist) as my_file:
    for line in my_file:
        payloads.put(line.strip())


# parse burp .req
headers , post_data = burpee.parse_request(args.request)
method_name , resource_name = burpee.get_method_and_resource(args.request)


def update(obj, payload):
    for key in obj.keys():
        obj[key] = obj[key].replace('FUZZ', payload)
    return obj

proxies = {}



# get outliers
time_threashold = .2



responses = []
num_payloads = payloads.qsize()

def worker(lock, responses):
    while True:
        payload = payloads.get()
        
        logging.info('Completed {} / {}'.format(num_payloads - payloads.qsize(), num_payloads))
        

        ## for each param in post data
        # for key in burp0_data.keys():
        modified_resource_name = resource_name.replace('FUZZ', payload)
        modified_headers = update(headers, payload)
        modified_post_data = post_data.replace('FUZZ', payload)


        if method_name.lower() == "get":
            r = requests.get(url = args.url + modified_resource_name , headers = modified_headers , proxies = proxies , verify = False)
        elif method_name.lower() == "post":
            r = requests.post(url = args.url + modified_resource_name, headers = modified_headers , data = modified_post_data , proxies = proxies , verify = False)

        if r.elapsed.total_seconds() > time_threashold:
            lock.acquire()

            responses.append({
                'status': r.status_code,
                'size': len(r.text), 
                'time': r.elapsed.total_seconds(),
                'payload': payload
            })

            for x in [x for x in responses if int(x['time']) >= time_threashold]:
                logging.info(f'{bcolors.FAIL}{x}{bcolors.ENDC}')

            lock.release()
        payloads.task_done()

for x in range(0, int(args.threads)):
    threading.Thread(target=worker, args=(lock, responses),daemon=True).start()


payloads.join()
print(responses)
print('done')

# print output
print('\nTime anomolies')
for x in [x for x in responses if int(x['time']) >= time_threashold]:
    print(f'{bcolors.FAIL}{x}{bcolors.ENDC}')


# counter = 0
# # make requests

# # proxies = {'http': 'http://localhost:8080'}
# for payload in payloads:
#     ## for each param in post data
#     # for key in burp0_data.keys():
#     modified_resource_name = resource_name.replace('FUZZ', payload)
#     modified_headers = update(headers, payload)
#     modified_post_data = post_data.replace('FUZZ', payload)


#     if method_name.lower() == "get":
#         r = requests.get(url = args.url + modified_resource_name , headers = modified_headers , proxies = proxies , verify = False)
#     elif method_name.lower() == "post":
#         r = requests.post(url = args.url + modified_resource_name, headers = modified_headers , data = modified_post_data , proxies = proxies , verify = False)


#     responses.append({
#         'status': r.status_code,
#         'size': len(r.text), 
#         'time': r.elapsed.total_seconds(),
#         'payload': payload
#     })
#     #print("code: {}, size: {}, time: {}, payload: {}".format(r.status_code, len(r.text), r.elapsed.total_seconds(), payload))
#     print(f"{counter}/{len(payloads)}")
#     counter += 1 


#     # print output
#     print('\nTime anomolies')
#     for x in [x for x in responses if int(x['time']) >= time_threashold]:
#         print(f'{bcolors.FAIL}{x}{bcolors.ENDC}')







# print(headers)



