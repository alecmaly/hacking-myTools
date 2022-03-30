


# build wordlists
echo [+] updating seclists
cd /opt/SecLists
git pull

# LFI (windows + linux)
echo [+] building LFI wordlists
wlk /opt/hacking-myTools/wordlists/custom-base/lfi-linux-custom.txt /opt/hacking-myTools/wordlists/custom-base/lfi-linux-hacktricks.txt  /opt/SecLists/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt > /opt/hacking-myTools/wordlists/lfi-known-linux.txt
wlk /opt/hacking-myTools/wordlists/custom-base/lfi-windows-custom.txt /opt/SecLists/Fuzzing/LFI/LFI-gracefulsecurity-windows.txt > /opt/hacking-myTools/wordlists/lfi-known-windows.txt

echo [+] building snmp common community strings wordlist
wlk /opt/SecLists/Discovery/SNMP/common-snmp-community-strings.txt /opt/SecLists/Discovery/SNMP/common-snmp-community-strings-onesixtyone.txt /usr/share/doc/onesixtyone/dict.txt > /opt/hacking-myTools/wordlists/snmp_comm_strings.txt

# Directory Fuzzing
echo [+] building largeRaftPlus2.3Medium-lowercase.txt wordlist
wlk /opt/hacking-myTools/wordlists/custom-base/directory-brute.txt /opt/SecLists/Discovery/Web-Content/raft-large-words-lowercase.txt /opt/SecLists/Discovery/Web-Content/common.txt /opt/SecLists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt > /opt/hacking-myTools/wordlists/largeRaftPlus2.3Medium-lowercase.txt

# password wordlist
echo [+] building fasttrack common-creds darkweb-top10000 wordlist
# download fasttrack.txt
wget -q "https://raw.githubusercontent.com/drtychai/wordlists/master/fasttrack.txt" -O /usr/share/wordlists/fasttrack_backup.txt
wlk /usr/share/wordlists/fasttrack_backup.txt /opt/SecLists/Passwords/Common-Credentials/best1050.txt /opt/SecLists/Passwords/darkweb2017-top10000.txt > /opt/hacking-myTools/wordlists/top1000_1050_fasttrack.txt




