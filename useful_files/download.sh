#!/bin/bash

##  download linux
# files
cat /opt/myTools/useful_files/util/_files_to_download_linux.txt | xargs wget -N -P /opt/myTools/useful_files/files/linux
# mkdir cd /opt/myTools/useful_files/files/linux/github 2>/dev/null
# cat /opt/myTools/useful_files/util/_github_linux.txt | xargs -I{} sh -c "cd /opt/myTools/useful_files/files/linux/github; git clone {}"


##  download windows
# files
cat /opt/myTools/useful_files/util/_files_to_download_windows.txt | xargs wget -N -P /opt/myTools/useful_files/files/windows
# github
mkdir cd /opt/myTools/useful_files/files/windows/github 2>/dev/null
cat /opt/myTools/useful_files/util/_github_windows.txt | xargs -I{} sh -c "cd /opt/myTools/useful_files/files/windows/github; git clone {}"



##  download all
# github
mkdir cd /opt/myTools/useful_files/files/all 2>/dev/null
mkdir cd /opt/myTools/useful_files/files/all/github 2>/dev/null
cat /opt/myTools/useful_files/util/_github_all.txt | xargs -I{} sh -c "cd /opt/myTools/useful_files/files/all/github; git clone {}"
