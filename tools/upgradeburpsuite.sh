#!/bin/bash


latest_url="https://portswigger.net$(curl https://portswigger.net/burp/releases/community/latest -s | grep 'burp'|awk -F'href="' '{print $2}'|cut -d '?' -f1)"
download_url="http://portswigger.net$(curl $latest_url -s |grep "jar"|grep download|grep community|awk -F 'href=' '{print $2}'|cut -d' ' -f1|sed 's/amp;//g')"

wget $download_url -O burpsuite
chmod +x burpsuite

mv burpsuite /usr/bin/burpsuite

echo [+] burpsuite has been updated