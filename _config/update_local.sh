#!/bin/bash


# update autorecon config
mkdir ~/.config 2>/dev/null
mkdir ~/.config/AutoRecon 2>/dev/null
cp /opt/hacking-myTools/_config/AutoReconConfig/AutoRecon/* ~/.config/AutoRecon/


mkdir /home/kali/.config 2>/dev/null
mkdir /home/kali/.config/AutoRecon 2>/dev/null
cp /opt/hacking-myTools/_config/AutoReconConfig/AutoRecon/* /home/kali/.config/AutoRecon/


# .myrc
cp /opt/hacking-myTools/_config/files/.myrc /etc/.myrc