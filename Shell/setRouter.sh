#!/bin/sh
#if tailed by 250
networksetup -getinfo "USB 10/100/1000 LAN" | grep "Router: 10" | grep -q "250$"
if [ $? -eq 0 ];then
#echo "250"
	sudo networksetup -setmanual "USB 10/100/1000 LAN" 10.10.20.121 255.255.255.0 10.10.20.20
else
#	echo "20"
	sudo networksetup -setmanual "USB 10/100/1000 LAN" 10.10.20.121 255.255.255.0 10.10.20.250
fi
