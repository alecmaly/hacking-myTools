if [ -z $1 ]; then
    echo "Usage: ./tftp_snmp_scan.sh <ip>"
    exit
fi
ip=$1

echo "[+] scanning for snmp common community strings"
onesixtyone $ip -c /opt/hacking-myTools/wordlists/snmp_comm_strings.txt | grep -e "^" -e "\[.*\]" --color=always

printf "\n\n"

echo "[+] Checking tftp"
tmp=$(echo "get /sfsodhf" | tftp $ip)

# "256: file not found" error code indicates service is active
if [[ "$tmp" == *"256"* ]]; then 
    echo "[+] tftp may be active" | grep ".*" --color=always
else
    echo "[-] tftp probably not active"
fi

# clean up tftp file
rm sfsodhf