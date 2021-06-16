#!/bin/bash

### GET FUNCTIONS : greppass / grepdb
### add grepdb to output files
### 
C=$(printf '\033')
RED="${C}[1;31m"
GREEN="${C}[1;32m"
Y="${C}[1;33m"
B="${C}[1;34m"
LG="${C}[1;37m" #LightGray
DG="${C}[1;90m" #DarkGray
NC="${C}[0m"
UNDERLINED="${C}[5m"
ITALIC="${C}[3m"

# test if sed supports -E or -r
E=E
echo | sed -${E} 's/o/a/' 2>/dev/null
if [ $? -ne 0 ] ; then
	echo | sed -r 's/o/a/' 2>/dev/null
	if [ $? -eq 0 ] ; then
		E=r
	else
		echo "${Y}WARNING: No suitable option found for extended regex with sed. Continuing but the results might be unreliable.${NC}"
	fi
fi

echo_not_found (){
  printf $DG"$1 Not Found\n"$NC
}

function myprint {
    C=$(printf '\033')
    red="${C}[1;31m"
    yellow="${C}[1;33m"
    reset="${C}[0m,"

    echo "${yellow}"$1"${reset}"
}


myprint "[+] OS Info"
uname -a 
printf '\n'
lsb_release -a 2>/dev/null
printf '\n\n'


myprint "[+] sudo -l (no password) (also check /etc/sudoers & /etc/sudoers.d)"
echo '' | sudo -S -l 
printf '\n\n'


myprint "[+] SUID Binaries"
myprint "cmd:  find / -perm -4000 2>/dev/null"
echo
find / -perm -4000 2>/dev/null
printf '\n\n'


myprint "[+] Vulnerable software installed"
printf "${RED}Copy/paste below command on attacker machine${reset}\n"
echo 'printf "'$(apt list --upgradeable 2>/dev/null | sed 's#/.*from: #   #g' | tr -d "]" | sed ':a;N;$!ba;s/\n/\\n/g' | sed ':a;N;$!ba;s/\n/\\n/g')'" | xargs -I{} sh -c "echo; printf \"SEARCHING: {}\n\"; searchsploit \$(echo {} | cut -d\" \" -f1)" | grep -v "No Results"'
printf '\n\n'


myprint "[+] hostname"
hostname
printf '\n\n'


#-- UI) Sudo tokens
myprint "[+] Checking sudo tokens"
ptrace_scope="`cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null`"


if [ "$ptrace_scope" ] && [ "$ptrace_scope" -eq 0 ]; then echo "/proc/sys/kernel/yama/ptrace_scope is enabled (0)" | sed "s,0,${C}[1;31m&${C}[0m,g";
else echo "/proc/sys/kernel/yama/ptrace_scope is not enabled ($ptrace_scope)" | sed "s,is not enabled,${C}[1;32m&${C}[0m,g";
fi


if [ "$ptrace_scope" ] && [ "$ptrace_scope" -eq 0 ] && [ "$is_gdb" ]; then
  echo "Check for sudo tokens in other shells owned by current user"
  printf $B"[i] "$Y"https://book.hacktricks.xyz/linux-unix/privilege-escalation#reusing-sudo-tokens\n"$NC

  is_gdb="`command -v gdb 2>/dev/null`"
  if [ "$is_gdb" ]; then echo "gdb was found in PATH" | sed -${E} "s,.*,${C}[1;31m&${C}[0m,g";
  else echo "gdb wasn't found in PATH, try transfering it." | sed "s,gdb,${C}[1;32m&${C}[0m,g";
  fi

  echo "Try this: https://github.com/nongiach/sudo_inject" | grep -e "^.*" --color=always
fi



myprint "[+] Readable files belonging to root and readable by me but not world readable"
(find / -type f -user root ! -perm -o=r 2>/dev/null | grep -v "\.journal" | while read f; do if [ -r "$f" ]; then ls -l "$f" 2>/dev/null | sed -${E} "s,/.*,${C}[1;31m&${C}[0m,"; fi; done) || echo_not_found
printf '\n\n'


myprint "[+] Hidden files owned by curent user: $(whoami)"
find / -name ".*" -user `whoami` 2>/dev/null
printf '\n\n'


myprint "[+] Files in \$HOME but owned by other user"
find $HOME ! -user `whoami` 2>/dev/null
printf '\n\n'


myprint "[+] Interesting Groups"
id | grep -E "^|wheel|shadow|disk|video|docker|lxd|root|lxc|adm" --color=always
printf '\n\n'

myprint "[+] printing group files"
groups | tr ' ' '\n' | xargs -I{} sh -c "echo; echo Looking for files in group: {}; find / -group {} -type f 2>/dev/null | head -n 25" 
printf '\n\n'

myprint "[+] Users with shell"
cat /etc/passwd | grep "sh$" --color=never | grep "^[^:]*"
printf '\n\n'

myprint "[+] .htpasswd files"
find / -name .htpasswd 2>/dev/null | grep -e "^" --color=always 
printf '\n\n'

myprint "[+] Wriable cron files"
find /etc/init.d /etc/cron* /etc/crontab /etc/cron.allow /etc/cron.d /etc/cron.deny /etc/cron.daily /etc/cron.hourly /etc/cron.monthly /etc/cron.weekly /etc/sudoers /etc/exports /etc/anacrontab /var/spool/cron /var/spool/cron/crontabs/root -writable 2>/dev/null
printf '\n\n'

myprint "[+] cronjobs"
crontab -l
cat /etc/init.d /etc/cron* /etc/at* /etc/sudoers /etc/exports /etc/anacrontab /var/spool/cron /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#" |grep -e "^" -e root --color=always
# ADDITIONAL: Finding writable cron paths
myprint "Writable cron paths:"; cat /etc/init.d /etc/cron* /etc/at* /etc/sudoers /etc/exports /etc/anacrontab /var/spool/cron /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#"  |grep PATH| cut -d'=' -f2|sed 's/:/\n/g'|xargs -L1 -I{} sh -c "find {} -writable |grep '.*' --color=always"
# ADDITIONAL: Finding possible exploitable crons
myprint "Possible Crons:"; cat /etc/init.d /etc/cron* /etc/at* /etc/sudoers /etc/exports /etc/anacrontab /var/spool/cron /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#"  |grep "*" |grep -e "^" -e "root" --color=always |grep -v anacron
printf '\n\n'

myprint "[+] Interesting File Locations"
ls /opt /tmp /var/www /home /srv /usr/local/bin
printf '\n\n' 

myprint "[+] passwd files"
cat /etc/passwd /etc/shadow /etc/master /var/log/auth.log
printf '\n\n'

myprint "[+] writable passwd files"
if [ -w /etc/passwd ]; then
    echo Writable
fi
[ -w /etc/passwd ] && echo "/etc/passwd Writable" | grep -e ".*" --color=always
[ -w /etc/shadow ] && echo "/etc/shadow Writable" | grep -e ".*" --color=always
[ -w /etc/master ] && echo "/etc/master Writable" | grep -e ".*" --color=always
[ -w /var/log/auth.log ] && echo "/var/logauth.log Writable" | grep -e ".*" --color=always
printf '\n\n'
 
myprint "[+] Open Ports"
netstat -ano 2>/dev/null |grep LISTEN | grep -e "^\|0.0.0.0\|127.0.0.1\|localhost" --color=always
printf '\n\n'
 

myprint "[+] Mounts/drives"
df -h
printf '\n\n'
 

myprint "[+] Useful software"
which nmap aws nc ncat netcat nc.traditional wget curl ping gcc g++ make gdb base64 socat python python2 python3 python2.7 python2.6 python3.6 python3.7 perl php ruby xterm doas sudo fetch docker lxc rkt kubectl 2>/dev/null 
printf '\n\n'

myprint "[+] Installed compilers"
(dpkg --list 2>/dev/null | grep "compiler" | grep -v "decompiler\|lib" 2>/dev/null || yum list installed 'gcc*' 2>/dev/null | grep gcc 2>/dev/null; which gcc g++ 2>/dev/null || locate -r "/gcc[0-9\.-]\+$" 2>/dev/null | grep -v "/doc/")
printf '\n\n'

myprint "[+] .ssh keys"
find / -name authorized_keys 2> /dev/null | grep -e "^" --color=always
find / -name id_rsa 2> /dev/null | grep -e "^" --color=always
printf '\n\n'

myprint "[+] capabilities"
getcap -r / 2>/dev/null
printf '\n\n'

myprint "[+] Backup files"
find /var /etc /bin /sbin /home /usr/local/bin /usr/local/sbin /usr/bin /usr/games /usr/sbin /root /tmp -type f \( -name "*backup*" -o -name "*\.bak" -o -name "*\.bck" -o -name "*\.bk" \) 2>/dev/null
myprint "[+] Backup directories"
find /var /etc /bin /sbin /home /usr/local/bin /usr/local/sbin /usr/bin /usr/games /usr/sbin /root /tmp -type d \( -name "*backup*" -o -name "*\.bak" -o -name "*\.bck" -o -name "*\.bk" \) 2>/dev/null
printf '\n\n'

myprint "[+] No root squash (priv esc)"
cat /etc/exports | grep "no.*squash" --color=always
printf '\n\n'

myprint "[+] /etc/sudoers"
cat cat /etc/sudoers 2>/dev/null | grep -e "^" -e "ALL" 
printf '\n\n'

myprint "[+] .bash_history files"
find / -name *.bash_history 2>/dev/null | head -n 25
printf '\n\n'

myprint "[+] SUID Binary – so injection"
myprint "look for non-errors & 'no such file or directory' -- can mkdir and insert the mallicious import"
find / -type f -perm -04000 2>/dev/null | xargs -I{} sh -c "strace {} 2>&1 | grep -i -E 'open|access|no such file' | cut -d'\"' -f2 | sed 's|\(.*\)/.*|\1|'"|sort|uniq | xargs -I{} sh -c 'find {} -prune -type d -writable 2>/dev/null' | head -n 25
printf '\n\n'

myprint "[+] Shared Library"
myprint "any paths inside: /etc/ld.so.conf"
cat /etc/ld.so.conf 2>/dev/null | sed 's/include //g'| sed 's/^#.*//g'|sed '/^$/d'|xargs -L1 -I{} sh -c "find {} -writable 2>/dev/null"
echo
myprint "any file inside: ls /etc/ld.so.conf.d/"
ls /etc/ld.so.conf.d 2>/dev/null | xargs -L1 -I{} sh -c "find /etc/ld.so.conf.d/{} -writable 2>/dev/null"
echo
myprint "any folder indicated inside any config file: /etc/ld.so.conf.d/*.conf"
cat /etc/ld.so.conf.d/*.conf 2>/dev/null | sed 's/^#.*//g'|sed '/^$/d'|xargs -L1 -I{} sh -c "find {} -writable 2>/dev/null"
printf '\n\n'


myprint "[+] writable .service files"
find / -name *.service -writable 2>/dev/null| xargs -L1 -I{} sh -c "echo {}; cat {} 2>/dev/null | grep Exec --color=always" | head -n 25
printf '\n\n'

myprint "[+] Writable executables in .service files"
find / -name *.service -writable 2>/dev/null| xargs -I{} sh -c "cat {} 2>/dev/null | grep -v '#'| grep Exec|cut -d ' ' -f1| cut -d'=' -f2| grep -v 'yes\|true'| sed 's/-\|\+\|://g'| xargs -I{l} sh -c 'find {l} -writable 2>/dev/null'" | head -n 25
printf '\n\n'

# TO DO: Replace /home with /etc/passwd users (users w/ shell)
myprint "[+] Readable files owned by other users"
ls /home | xargs -I{} sh -c "if [ {} != `whoami` ]; then echo -------- READABLE FILES OWNED BY: {} --------; find / -user {} -readable 2>/dev/null; fi" 
printf '\n\n'

myprint "[+] World writable files"
find / -writable ! -user `whoami` -type f ! -path "/proc/*" ! -path "/sys/*" -exec ls -al {} \; 2>/dev/null | head -n 25
printf '\n\n'

myprint "[+] Can read other user's files"
find /home -readable ! -user `whoami` ! -user root 2>/dev/null | head -n 25
printf '\n\n'

myprint "[+] Readable hidden files"
find /etc /opt /var /home /root /srv -type f -iname ".*" -readable 2>/dev/null | head -n 25
printf '\n\n'

myprint "[+] Files modified last 5 min"
find / -type f -mmin -5 ! -path "/proc/*" ! -path "/sys/*" ! -path "/run/*" ! -path "/dev/*" ! -path "/var/lib/*" 2>/dev/null | head -n 25
printf '\n\n'



myprint "[+] Possibly custom binaries"
# using dkpg
if [ ! -z $(which "dpkg" 2>/dev/null) ]; then 
    find / -type f -executable -exec file -i '{}' \; 2>/dev/null | grep -v "/snap/" | grep "charset=binary" | grep "x-.*sharedlib\|x-.*executable"  | grep -v "\.so" | cut -d':' -f1 | xargs -I{} sh -c "echo {}; dpkg -S {}; echo" | grep -B1 -A1 "no path found"
fi
# using rpm
if [ ! -z $(which rpm 2>/dev/null) ]; then
    # rpm
    # find all executables, except .so files
    find / -type f -executable -exec file -i '{}' \; 2>/dev/null | grep "charset=binary" | grep "x-.*sharedlib\|x-.*executable"  | grep -v "\.so" | cut -d':' -f1 | xargs -I{} sh -c "echo {}; ls -la {}; rpm -q --whatprovides {}; echo" | grep -B2 -A1 "not owned" --color=always
fi
printf '\n\n'




printf "..DONE.."
