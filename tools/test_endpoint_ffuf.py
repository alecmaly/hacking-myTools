
import subprocess
import argparse
from argparse import RawTextHelpFormatter
import requests
import re
import Burpee.burpee as burpee
import json
import statistics
import copy
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
parser = argparse.ArgumentParser(description='python testsqli.py -u url -r request.req -w wordlist',formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', default='', required=True)
parser.add_argument('-r', '--request', required=True)
parser.add_argument('-w', '--wordlist', default='/opt/SecLists/Fuzzing/SQLi/Generic-SQLi.txt', required=False)
parser.add_argument('-s', '--scan-type', default='all', required=False, help='s - sqli\na - api action\no - api object\nh - headers\ns - swap GET/POST\nall - all')
parser.add_argument('-p', '--params', default='', required=False, help='Comma seperated params to fuzz.')
parser.add_argument('-t', '--time-threshold', default=4000, required=False, help='Time threshold in miliseconds (ms).')


args = parser.parse_args()
args.url = re.sub('/*$', '', args.url)  # strip trailing / on url
args.scan_type = [x.strip() for x in args.scan_type.split(',')] # parse scan-type args

## modifiable config
proxies = {}





# parse burp .req
headers , post_data = burpee.parse_request(args.request)
method_name , resource_name = burpee.get_method_and_resource(args.request)



### loop through and make all iterations of requests 





##### ---------------------------

def test(req_obj, wordlist=args.wordlist, test_title='', output_file='tmp.json'):
    print(f"\n{bcolors.BOLD}{bcolors.HEADER}{test_title}{bcolors.ENDC}{bcolors.ENDC}")
    headers_str = ''
    for header in req_obj['headers']:
        headers_str += f"-H '{header}: {req_obj['headers'][header]}' "

    # # # STEP 1: RUN FFUF
    # update User-Agent header
    cmd = ''
    if req_obj['method_name'].lower() == "get":
        cmd = f"/opt/ffuf/ffuf -s -mc all -ic -X {req_obj['method_name']} -u '{req_obj['url']}' {headers_str} -w {wordlist} -of json -o {output_file}"
    elif req_obj['method_name'].lower() == "post":
        # update content type (application/x-www-form-urlencoded)
        cmd = f"/opt/ffuf/ffuf -s -mc all -ic -X {req_obj['method_name']} -u '{req_obj['url']}' -d '{req_obj['post_data']}' {headers_str} -w {wordlist} -of json -o {output_file}"


    # cmd = f'ffuf -ic -u {args.url} -request {args.request} -w {args.wordlist} -of json -o {output_file}'
    print(f'{bcolors.WARNING}{cmd}{bcolors.ENDC}')

    #start and process things, then wait
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # print("Happens while running")
    p.communicate() #now wait plus that you can send commands to process
    # print('done.')



    # STEP 2: read data
    # FUZZ,url,redirectlocation,position,status_code,content_length,content_words,content_lines,resultfile


    with open(output_file) as f:
      data = json.load(f)

        
    print(f'{bcolors.OKCYAN}')
    print('headers:', '\n', req_obj['headers'])
    print('method_name:', '\n', req_obj['method_name'])
    print('url:', '\n', req_obj['url'])
    print('resource_name:', '\n', req_obj['resource_name'])
    print('post_data:', '\n', req_obj['post_data'])
    print(f'{bcolors.ENDC}')

    if data['results']:
        # get outliers
        print(f'{bcolors.FAIL}')
        mode_code = statistics.mode([x['status'] for x in data['results']])
        mode_size = statistics.mode([x['length'] for x in data['results']])


        print(f'\nSize anomolies (mode: {mode_size})')
        for size in sorted(set([x['length'] for x in data['results'] if x['length'] != mode_size])):
            items = [x for x in data['results'] if x['length'] == size]
            # print('size: {}'.format(size), len(items))
            for x in items:
                print({
                    'status': x['status'],
                    'size': x['length'], 
                    'payload': x['input']['FUZZ']
                })

        print(f'\nStatus anomolies (mode: {mode_code})')
        for x in [x for x in data['results'] if x['status'] != mode_code]:
            print({
                'status': x['status'],
                'size': x['length'], 
                'payload': x['input']['FUZZ']
            })

        
        print(f'\nTime anomolies (threshold: {args.time_threshold})')
        time_anomolies = [x for x in data['results'] if x['responsetime'] >= int(args.time_threshold)]  
        for x in sorted(time_anomolies, key = lambda i: i['responsetime'], reverse=True)[:5]:
        # for x in [x for x in data['results'] if x['responsetime'] >= int(args.time_threshold)]:
            print({
                'status': x['status'],
                'size': x['length'], 
                'payload': x['input']['FUZZ'],
                'time': x['responsetime']
            })

        print(f'{bcolors.ENDC}')




def swap(req_obj):
    req_obj = copy.deepcopy(req_obj)
    if req_obj['method_name'].lower() == 'get':
        req_obj['method_name'] = 'POST' 
        
        params = req_obj['resource_name'].split('?')[1] if len(req_obj['resource_name'].split('?')) > 1 else ''
        req_obj['post_data'] = params

        req_obj['resource_name'] = req_obj['resource_name'].split('?')[0]

        req_obj['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

        req_obj['url'] = req_obj['url'].replace(params, '').replace('?', '')
        # print(req_obj)
        return req_obj
    if req_obj['method_name'].lower() == 'post':
        req_obj['method_name'] = 'GET'
        
        req_obj['resource_name'] += ('?' + req_obj['post_data']) if len(req_obj['post_data']) > 0 else ''

        if 'Content-Type' in req_obj['headers']: del req_obj['headers']['Content-Type']     

        req_obj['url'] += ('?' + req_obj['post_data']) if len(req_obj['post_data']) > 0 else ''
        # print(req_obj)
        return req_obj


def get_actions(req_obj):
    actions = []
    params = ''
    if req_obj['method_name'].lower() == 'get':
        params = req_obj['resource_name'].split('?')[1] if len(req_obj['resource_name'].split('?')) > 1 else ''
    if req_obj['method_name'].lower() == 'post':
        params = req_obj['post_data']

    # print(params)
    for param in params.split('&'):
        actions.append(param.split('=')[0])

    # print(req_obj)
    # print(actions)
    return actions



req_obj_orig = {
    'method_name': method_name,
    'headers': headers,
    'post_data': post_data,
    'url': args.url,
    'resource_name': resource_name
}


# # test all params
# # swap request type
# # test all params


def test_actions(req_obj):
    ### FUZZ ACTIONS
    actions = args.params.split(',') if args.params else get_actions(req_obj)

    # original request
    for action in actions:
        if action not in get_actions(req_obj):
            continue 
        req_obj_tmp = copy.deepcopy(req_obj)
        req_obj_tmp['url'] = req_obj_tmp['url'].replace(action+'=', 'FUZZ=')
        req_obj_tmp['post_data'] = req_obj_tmp['post_data'].replace(action+'=', 'FUZZ=')
        req_obj_tmp['resource_name'] = req_obj_tmp['resource_name'].replace(action+'=', 'FUZZ=')

        # test(req_obj_tmp, wordlist='/opt/SecLists/Discovery/Web-Content/api/actions.txt')
        test(req_obj_tmp, wordlist='/opt/hacking-myTools/wordlists/api-all.txt', test_title=f"TESTING Actions (param) - All ({action})")
        ## test SQLI if needed



def replace_object(s, action):
    chunks = s.split('=')
    for i in range(0, len(chunks)):
        if(chunks[i].endswith('&'+action) or chunks[i].endswith('?'+action) or chunks[i] == action):
            suffex = ('&' + chunks[i+1].split('&')[1]) if '&' in chunks[i+1] else ''
            chunks[i+1] = 'FUZZ' + suffex
    return '='.join(chunks)


def test_objects(req_obj):
    # TO DO: TEST ARITHMATIC INJECTIONS

    ### FUZZ ACTIONS
    actions = args.params.split(',') if args.params else get_actions(req_obj)

    # original request
    for action in actions: 
        if action not in get_actions(req_obj):
            continue 
        req_obj_tmp = copy.deepcopy(req_obj)
        req_obj_tmp['url'] = replace_object(req_obj_tmp['url'], action)
        req_obj_tmp['post_data'] = replace_object(req_obj_tmp['post_data'], action)
        req_obj_tmp['resource_name'] = replace_object(req_obj_tmp['resource_name'], action)

        # print(req_obj_tmp)
        # test(req_obj_tmp, wordlist='/opt/SecLists/Discovery/Web-Content/api/objects.txt')
        test(req_obj_tmp, wordlist='/opt/hacking-myTools/wordlists/api-all.txt', test_title=f"TESTING Objects (value) - All ({action})")
        test_arithmetict(req_obj_tmp)
        test(req_obj_tmp, wordlist='/opt/SecLists/Fuzzing/SQLi/Generic-SQLi.txt', test_title="TESTING SQLI ({action}=)")




def test_arithmetict(req_obj):
    print(f"\n{bcolors.BOLD}{bcolors.HEADER}TESTING ARITHMATIC{bcolors.ENDC}{bcolors.ENDC}")
    # TO DO: TEST ARITHMATIC INJECTIONS
    # 133225
    payloads = [
        '365*365',
        '${365*365}',
        '%{365*365}',
        '@(365*365)'
    ]

    for payload in payloads:
        req_obj_arithmetic = copy.deepcopy(req_obj)
        req_obj_arithmetic['url'] = req_obj_arithmetic['url'].replace('FUZZ', payload)
        req_obj_arithmetic['post_data'] = req_obj_arithmetic['post_data'].replace('FUZZ', payload)
        req_obj_arithmetic['resource_name'] = req_obj_arithmetic['resource_name'].replace('FUZZ', payload)

        if method_name.lower() == "get":
            resp = requests.get(url = req_obj_arithmetic['url'] , headers = req_obj_arithmetic['headers'] , proxies = proxies , verify = False)
        
        elif method_name.lower() == "post":
            resp = requests.post(url = req_obj_arithmetic['url'] , headers = req_obj_arithmetic['headers'] , data = req_obj_arithmetic['post_data'] , proxies = proxies , verify = False)
        
        if '133225' in resp.text:
            print(f'{bcolors.FAIL}[!] Found reflected payload: {payload}\n{req_obj_arithmetic}{bcolors.ENDC}')





test_actions(req_obj_orig)
test_objects(req_obj_orig)

test_actions(swap(req_obj_orig))
test_objects(swap(req_obj_orig))


# test(req_obj)
os.remove("tmp.json")
