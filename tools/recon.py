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

print('[+] scanning all ports with masscan')
os.system('mkdir scans')
cmd = 'masscan -p1-65535,U:1-65535 {} --rate=1000 -e {} > ./scans/masscan.txt'.format(args.address, args.interface)
print('running: ' + cmd)
os.system(cmd)



# collect port numbers
with open('./scans/masscan.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
ports = [x.split(' ')[3].split('/')[0] for x in content] 
ports = list(dict.fromkeys(ports))
# # get tcp ports and remove duplicates
# tcp_ports = [x.split('/')[0] for x in ports if 'tcp' in x]
# tcp_ports = list(dict.fromkeys(tcp_ports))

# # get udp ports and remove duplicates
# udp_ports = [x.split('/')[0] for x in ports if 'udp' in x]
# udp_ports = list(dict.fromkeys(udp_ports))





# If source is namp output
#  ports = [x.split(' ')[0].split('/')[0] for x in content if '/tcp' in x or '/udp' in x and 'filtered' not in x]
# ports = list(dict.fromkeys(ports))




# # TCP scan
print('[+] TCP/UDP nmap scan on ports {}'.format(ports))
os.system('mkdir scans/nmap')
cmd = 'nmap -p {} -sU -sT -A -T4 {} -e {} -oA ./scans/nmap/initial'.format(','.join(ports), args.address, args.interface)
print('running: ' + cmd)
os.system(cmd)








