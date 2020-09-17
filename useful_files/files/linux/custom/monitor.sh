#!/bin/bash


while true
do
	ps -aux |awk '{$3=$4=""; print $0}' |grep -iv "\[kworker"|grep -iv "\$3=\$4"|grep -iv "ps -aux"|grep -iv "+++ tmp2"> tmp 
	diff -u tmp tmp2 | grep -E "^\+" >> output
	cp tmp tmp2
	sleep 2
done


