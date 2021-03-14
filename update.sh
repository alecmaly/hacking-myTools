




# build wordlists
echo [+] updating seclists
cd /opt/Seclists
git pull

# LFI
echo [+] building LFI wordlist
wlk /opt/hacking-myTools/wordlists/custom-base/lfi-linux-custom.txt /opt/hacking-myTools/wordlists/custom-base/lfi-linux-hacktricks.txt  /opt/SecLists/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt > /opt/hacking-myTools/wordlists/lfi-known-linux.txt

# Directory Fuzzing
echo [+] building largeRaftPlus2.3Medium-lowercase.txt wordlist
wlk /opt/hacking-myTools/wordlists/custom-base/directory-brute.txt /opt/SecLists/Discovery/Web-Content/raft-large-words-lowercase.txt /opt/SecLists/Discovery/Web-Content/common.txt /opt/SecLists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt > /opt/hacking-myTools/wordlists/largeRaftPlus2.3Medium-lowercase.txt
