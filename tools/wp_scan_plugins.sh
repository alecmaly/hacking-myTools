#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: wp_scan_plugins.sh <url>"
    exit 1
fi


wpurl=$1


#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: wp_scan_plugins.sh <url>"
    exit 1
fi


wpurl=$1

mkdir wp_scan_results 2>/dev/null

# vulnerable plugin SCAN
echo RUNNING VULNERABLE PLUGINS SCAN \(1/3\)
wpscan --url $wpurl -e u,vp,t --plugins-detection mixed --format json --output ./wp_scan_results/wp_vuln_plugins.json 
/root/.cargo/bin/wpscan-analyze -f ./wp_scan_results/wp_vuln_plugins.json
cat ./wp_scan_results/wp_vuln_plugins.json  |jq .plugins[] | jq '"\(.slug)  \(.version.number)  confidence: \(.version.confidence)"' | xargs -L1 -I{} sh -c "printf '\n\n>>>> {} <<<< \n'; printf '{}' | cut -d' ' -f1 | tr '-' ' ' | xargs -I {l} sh -c 'searchsploit -s {l}'"
echo Users:; cat ./wp_scan_results/wp_vuln_plugins.json  |jq .users | jq 'keys' >> ./wp_scan_results/wp_users.txt; cat ./wp_scan_results/wp_users.txt


# p - plugins ;  ap - all plugins  ; vp - vulnerable plugins
echo RUNNING POPULAR PLUGINS SCAN \(2/3\)
wpscan --url $wpurl -e p --plugins-detection mixed --format json --output ./wp_scan_results/wp_plugins.json
/root/.cargo/bin/wpscan-analyze -f ./wp_scan_results/wp_plugins.json
cat ./wp_scan_results/wp_plugins.json  |jq .plugins[] | jq '"\(.slug)  \(.version.number)  confidence: \(.version.confidence)"' | xargs -L1 -I{} sh -c "printf '\n\n>>>> {} <<<< \n'; printf '{}' | cut -d' ' -f1 | tr '-' ' ' | xargs -I {l} sh -c 'searchsploit -s {l}'"

# All plugin scan
echo RUNNING ALL PLUGINS SCAN \(3/3\)
wpscan --url $wpurl -e ap --plugins-detection mixed --format json --output ./wp_scan_results/wp_all_plugins.json
/root/.cargo/bin/wpscan-analyze -f ./wp_scan_results/wp_all_plugins.json
cat ./wp_scan_results/wp_all_plugins.json  |jq .plugins[] | jq '"\(.slug)  \(.version.number)  confidence: \(.version.confidence)"' | xargs -L1 -I{} sh -c "printf '\n\n>>>> {} <<<< \n'; printf '{}' | cut -d' ' -f1 | tr '-' ' ' | xargs -I {l} sh -c 'searchsploit -s {l}'"
