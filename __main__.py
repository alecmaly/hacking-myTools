import os
import rgobuster

def help():
    print("\n\n")
    print("1) Perform Recon")
    print("2) Gobuster")
    print("3) Extract comments from webpage")
    print("q) quit")



def switch(argument):
    switcher = {
        1: perform_recon,
        2: perform_recon,
        3: extract_comments
    }
    func = switcher.get(argument, "Invalid entry")
    func()


def perform_recon():
    args = input('Enter args: -i <interface> -a <address>\n')
    os.system('python recon.py {}'.format(args))

def extract_comments():
    args = input('Enter args: -u <url>\n')
    os.system('python extract_comments.py {}'.format(args))

def gobuster():

    with open('./scans/masscan.txt') as f:
        content = f.readlines()
    
    if (" /80 " in content):
        print("port 80 found")
    if (" /443 " in content):
        print("port 443 found")
        
    print(" /80 " in content)
    # run gobuster
    extensions = input("[?] port 80 detected, running gobuster with common.txt wordlist. Please select extensions based on http header (e.g. '.php,.html'): ")

    args = input('Enter args: -u <url>\n')
    os.system('python extract_comments.py {}'.format(args))









while True: 
    help()
    cmd = input("Enter command: ")
    if cmd == 'q':
        break
    elif cmd == '':
        continue


    try:
        switch(int(cmd))
        input('Press ENTER to continue')
    except:
        print('\n\n')
        os.system(cmd)


