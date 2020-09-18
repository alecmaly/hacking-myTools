
import argparse
import os
from myUtil import str2bool
from termcolor import colored 
import sys


## note, first set environment alias
# alias rgobuster="python3 /opt/hacking-myTools/tools/rgobuster.py"




class RecursiveGobuster():
    def __init__(self):
        os.system('mkdir ./scans 2>/dev/null')
        os.system('mkdir ./scans/gobuster 2>/dev/null')
        self.save_path = './scans/gobuster'

    def set_savePath(self, path):
        self.save_path = path

    def collect_urls(self):
        os.system('touch {}/all.txt'.format(self.save_path))
        f = open("{}/gobuster.txt".format(self.save_path), "r+")

        print('{}/all.txt'.format(self.save_path))
        
        with open('{}/all.txt'.format(self.save_path), 'r+') as all_endpoints:
            for line in f:
                for endpoint in all_endpoints:
                    if line == endpoint:
                        break
                else: # not found
                    all_endpoints.write(line)


        f.close()

    def get_spiderable_endpoints(self):
        f = open("{}/all.txt".format(self.save_path), "r+")

        arr = []
        for line in f:
            line = line.strip()
            if '.' not in line.split(' ')[0].split('/')[-1:][0] and 'spidered' not in line:
                arr.append(line.split(' ')[0])
        return arr


    def mark_url_as_spidered(self, url):
        url = url.replace('/', r'\/')
        os.system("sed -i 's/{} /{} {} /' {}/all.txt".format(url, url, colored('spidered', 'green'), self.save_path))


    def reset_spidered(self):
        os.system("sed -i 's/ spidered / /' {}/all.txt".format(self.save_path))


    def run_gobuster(self, args):
        # -k to ignore self signed certs
        args = sys.argv[1:]
        
        try:
            url = args[args.index('-u')+1]
            cmd = "gobuster {} -e -o {}/gobuster.txt".format(' '.join(args), self.save_path)
            os.system(cmd)

            
            self.collect_urls()
            self.mark_url_as_spidered(url)
            
            endpoints = self.get_spiderable_endpoints()
            
            if (len(endpoints) > 0):
                new_url = endpoints[0]
                args[args.index('-u')+1] = new_url
                # NOTE, must map rgobuster script as alias
                print('rgobuster {}'.format(' '.join(args)))
                os.system('python3 /opt/hacking-myTools/tools/rgobuster.py {}'.format(' '.join(args)))
        except Exception as e:
            cmd = "gobuster {} ".format(' '.join(args))
            os.system(cmd)
        





# ## Step 3: gobuster
# # if port == 80 || port == 443
# # gobuster dir -u https://mysite.com/path/to/folder -c 'session=123456' -t 50 -w common-files.txt -x .php,.html
# # gobuster dir -u $address -c 'session=123456' -t 50 -w /usr/share/seclists/Discovery/Web-Content/common.txt -x .php,.html
# # check cgi-bin directory
# # gobuster dir -u $address/cgi-bin -c 'session=123456' -t 50 -w /usr/share/seclists/Discovery/Web-Content/common.txt -x .sh 



if __name__ == '__main__':
    args = sys.argv
    if (len(args) > 1):
        rec_gobuster = RecursiveGobuster()
        rec_gobuster.run_gobuster(args)
