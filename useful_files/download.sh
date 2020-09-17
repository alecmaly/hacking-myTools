#!/bin/bash

# cat /opt/myTools/useful_files/util/_files_to_download_linux.txt | xargs wget -N -P /opt/myTools/useful_files/files/linux


# cat /opt/myTools/useful_files/util/_files_to_download_windows.txt | xargs wget -N -P /opt/myTools/useful_files/files/windows

mkdir cd /opt/myTools/useful_files/files/windows/github 2>/dev/null
cat /opt/myTools/useful_files/util/_github_windows.txt | xargs -I{} sh -c "cd /opt/myTools/useful_files/files/windows/github; git clone {}"
