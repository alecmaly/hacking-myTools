#!/bin/python

# # reference for updates
# # https://github.com/rkhal101/nmapAutomator/blob/master/nmapAutomator.sh


import argparse
import os

parser = argparse.ArgumentParser(description='python recon.py -a <ip address> -i <interface>')
parser.add_argument('-i', '--interface', help='interface', required=True)
parser.add_argument('-a', '--address', help='ip address', required=True)
args = parser.parse_args()

print(args)









## STEP 1: run masscan

print('[+] scanning all tcp ports')
os.system('mkdir scans')
cmd = 'nmap {} -T4 --min-rate=700 --max-retries=3 -p- -oN ./scans/_full_tcp_ports_nmap.txt '.format(args.address)
print('running: ' + cmd)
os.system(cmd)



# If source is namp output
ports = [x.split(' ')[0].split('/')[0] for x in content if '/tcp' in x or '/udp' in x and 'filtered' not in x]
ports = list(dict.fromkeys(ports))




# # TCP scan
print('[+] TCP nmap scan on ports {}'.format(ports))
os.system('mkdir scans/nmap')
cmd = 'nmap {} -T4 -sU -min-rate=700 --max-retries=3 -p- {} -e {} -oN ./scans/_full_udp_ports_namp.txt'.format(','.join(ports), args.address, args.interface)
print('running: ' + cmd)
os.system(cmd)








