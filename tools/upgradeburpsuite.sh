#!/bin/bash


latest_url="$(curl https://portswigger.net/burp/releases/community/latest -s -L | grep 'burp'|awk -F'href="' '{print $2}'|cut -d '?' -f1 | grep releases | grep community | sed 's#"/>##g' | tr -d '\n' | tr -d '\r')"
download_url="$(curl $latest_url -s |grep "jar"|grep download|grep community|awk -F 'href=' '{print $2}'|cut -d' ' -f1|sed 's/amp;//g' | grep -oP "^.*?jar")"

wget $download_url -O burpsuite
chmod +x burpsuite

mv burpsuite /usr/bin/burpsuite

echo [+] burpsuite has been updated
