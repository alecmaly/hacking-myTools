#!/bin/bash

cat /opt/myTools/useful_files/util/_files_to_download_linux.txt | xargs wget -N -P /opt/myTools/useful_files/files/linux
cat /opt/myTools/useful_files/util/_files_to_download_windows.txt | xargs wget -N -P /opt/myTools/useful_files/files/windows

