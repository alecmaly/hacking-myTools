#!/bin/bash

# smbclient \\\\10.10.10.178\\Users -U c.smith%xRxRxPANCAK3SxRxRx -c 'recurse;ls' > output


echo $@
domain_share_path=$(echo $@ | grep -o '\\\\.*\\\w*')

# # get files from share recursively
# smbclient $@ -c 'recurse;ls' |sed 's/\\/\\\\/g' > output




## download all first,
## then check for ADS, download + output to console
echo "[+] recursively downloading all files"
smbclient $@ -c 'recurse on; prompt off; mget *'



echo "[+] checking for alternative data streams"

while read line; do
    if [[ "$line" == *"\\"* ]]; then
        directory=$line
        path=$domain_share_path$line
        
    fi
    if [[ "$line" == *" A "* ]]; then
        
        file=$(echo $line |awk -F' A ' '{print $1}')
        relativepath=$directory\\$file
        fullpath=$path\\$file

        echo $fullpath
        # print number of streams
        # look for files w/ 2+ streams
        smbclient $@ -c "allinfo \"$relativepath\"" | grep -c 'stream'

        ## download file + alternative data stream

    fi
done <output


# echo $domain_share_path
