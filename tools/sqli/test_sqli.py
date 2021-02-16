import Burpee.burpee as burpee
import requests
import argparse
import statistics
import re
# https://github.com/xscorp/Burpee


#  parse args
parser = argparse.ArgumentParser(description='python testsqli.py -u url -r request.req -w wordlist')
parser.add_argument('-u', '--url', default='', required=True)
parser.add_argument('-r', '--request', required=True)
parser.add_argument('-w', '--wordlist', default='/opt/SecLists/Fuzzing/SQLi/Generic-SQLi.txt',required=False)
args = parser.parse_args()
args.url = re.sub('/*$', '', args.url)  # strip trailing / on url


args = {}
args['url'] = 'http://192.168.69.63:450/'
args['request'] = 'login.req'
args['wordlist'] = '/opt/SecLists/Fuzzing/SQLi/Generic-SQLi.txt'


# build wordlist
payloads = []
with open(args['wordlist']) as my_file:
    for line in my_file:
        payloads.append(line.strip())



# parse burp .req
headers , post_data = burpee.parse_request(args['request'])
method_name , resource_name = burpee.get_method_and_resource(args['request'])


def update(obj, payload):
    for key in obj.keys():
        obj[key] = obj[key].replace('FUZZ', payload)
    return obj

proxies = {}


def normal_request_size():
    if method_name.lower() == "get":
        r = requests.get(url = args['url'] + resource_name , headers = headers , proxies = proxies , verify = False)
    elif method_name.lower() == "post":
        r = requests.post(url = args['url'] + resource_name, headers = headers , data = post_data , proxies = proxies , verify = False)

    return len(r.text)

n_size = normal_request_size()


# make requests
responses = []
# proxies = {'http': 'http://localhost:8080'}
for payload in payloads:
    ## for each param in post data
    # for key in burp0_data.keys():
    modified_resource_name = resource_name.replace('FUZZ', payload)
    modified_headers = update(headers, payload)
    modified_post_data = post_data.replace('FUZZ', payload)


    if method_name.lower() == "get":
        r = requests.get(url = args['url'] + modified_resource_name , headers = modified_headers , proxies = proxies , verify = False)
    elif method_name.lower() == "post":
        r = requests.post(url = args['url'] + modified_resource_name, headers = modified_headers , data = modified_post_data , proxies = proxies , verify = False)


    responses.append({
        'status': r.status_code,
        'size': len(r.text), 
        'time': r.elapsed.total_seconds(),
        'payload': payload
    })
    print("code: {}, size: {}, time: {}, payload: {}".format(r.status_code, len(r.text), r.elapsed.total_seconds(), payload))




# get outliers
mode_code = statistics.mode([x['status'] for x in responses])
mode_size = statistics.mode([x['size'] for x in responses])
time_threashold = .2





print('\nSize anomolies')
for size in sorted(set([x['size'] for x in responses if x['size'] != mode_size])):
    items = [x for x in responses if x['size'] == size]
    print('size: {}'.format(size), len(items))
    for x in items:
        print(x)



# # group by size
# print('\nSize anomolies')
# for x in [x for x in responses if x['size'] != mode_size]:
#     print(x)


print('\nStatus anomolies')
for x in [x for x in responses if x['status'] != mode_code]:
    print(x)

print('\nTime anomolies')
for x in [x for x in responses if int(x['time']) >= time_threashold]:
    print(x)

## anonmolies: check for response headers: Set-Cookie
# cookies



for x in [x for x in responses if int(x['size']) > n_size-100 and int(x['size']) < n_size+100]:
    print(x)






# print(headers)



