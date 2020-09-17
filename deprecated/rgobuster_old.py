
import argparse
import os
from myUtil import str2bool
from termcolor import colored 




class RecursiveGobuster():
    def __init__(self):
        os.system('mkdir ./scans 2>/dev/null')
        os.system('mkdir ./scans/gobuster 2>/dev/null')
        self.save_path = './scans/gobuster'

        self.url = ''
        self.wordlist = '/usr/share/seclists/Discovery/Web-Content/common.txt'
        self.extensions = ''
        self.cookies = ''
        self.recursive = False
        self.params = ''


    def configure_and_run(self):
        # self.dateTime = os.system('date +%Y%m%d-%H:%M')
        print('Use , to specify previous input')
        tmp = input('Enter URL ({}): '.format(self.url))
        if tmp != ',': self.url = tmp if tmp != '' else "''"

        tmp = input('Enter wordlist ({}): '.format(self.wordlist))
        if tmp != ',': self.wordlist = tmp if tmp != '' else "''"

        os.system('cat ./scans/nmap.nmap')
        tmp = input("[?] Please select extensions based on nmap http header (e.g. 'php,html')({}):".format(self.extensions))
        if tmp != ',': self.extensions = tmp if tmp != '' else "''"

        tmp = input('Enter cookies ({}): '.format(self.cookies))
        if tmp != ',': self.cookies = tmp if tmp != '' else "''"

        tmp = input('Recursive (y/n)? ({}): '.format(self.recursive))
        if tmp != ',': 
            self.recursive = True if tmp == 'y' else False
    
        tmp = input('Extra params ({}): '.format(self.params))
        if tmp != ',': self.params = tmp 


        self.run_gobuster(self.url, self.extensions, self.cookies, self.wordlist, self.recursive, self.params)


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
        url = url.replace('/', '\/')
        os.system("sed -i 's/{} /{} {} /' {}/all.txt".format(url, url, colored('spidered', 'green'), self.save_path))


    def reset_spidered(self):
        os.system("sed -i 's/ spidered / /' {}/all.txt".format(self.save_path))




    def run_gobuster(self, url, extensions="''", cookies="''", wordlist='/usr/share/seclists/Discovery/Web-Content/common.txt', recursive=False, params=""):
        # -k to ignore self signed certs
        cmd = "gobuster dir -u {} -c {} -t 50 -w {} -x {} -k -e -o {}/gobuster.txt {}"\
            .format(url, cookies, wordlist, extensions, self.save_path, params)
        os.system(cmd)
        # print(cmd)

        self.collect_urls()
        self.mark_url_as_spidered(url)

        if (recursive == True):
            endpoints = self.get_spiderable_endpoints()
            if (len(endpoints) > 0):
                self.run_gobuster(endpoints[0], extensions, cookies, wordlist, recursive, params)
            return





# ## Step 3: gobuster
# # if port == 80 || port == 443
# # gobuster dir -u https://mysite.com/path/to/folder -c 'session=123456' -t 50 -w common-files.txt -x .php,.html
# # gobuster dir -u $address -c 'session=123456' -t 50 -w /usr/share/seclists/Discovery/Web-Content/common.txt -x .php,.html
# # check cgi-bin directory
# # gobuster dir -u $address/cgi-bin -c 'session=123456' -t 50 -w /usr/share/seclists/Discovery/Web-Content/common.txt -x .sh 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python recon.py -a <ip address> -c <cookie string> -r <recursive>')
    parser.add_argument('-a', '--address', help='ip address', required=True)
    parser.add_argument('-c', '--cookies', help='cookies', required=False)
    parser.add_argument("-r", '--recursive', type=str2bool, nargs='?',
                            const=True, default=False,
                            help="Activate recursive mode.")
    args = parser.parse_args()

    print(args)
    rec_gobuster = RecursiveGobuster()
    rec_gobuster.configure_and_run()
