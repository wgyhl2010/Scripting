#!/bin/sh
echo "===`date`===" >> /Users/paradox/Log/netLog.log

#open wi-fi
sudo networksetup -setairportpower en0 on
if [ $? -eq 0 ];then
	echo "en0 device opened successfully" >> /Users/paradox/Log/netLog.log
else
	echo "en0 device opened failed" >> /Users/paradox/Log/netLog.log
	exit 1
fi

#wait until wi-fi complete restarting or timeout
#if the string behind th -z contains space, it must be warped in double quotes
count=0
while [ -z "`airport -s`" -a $count -le 50 ]
	do
#		count=$(($count+1))
		((count++))
		sleep 0.1
#		echo $count >> /Users/paradox/Log/netLog.log
	done 
test $count -gt 0 && (((count*=100));time="$count"ms;echo "wifi starts completely after $time" >> /Users/paradox/Log/netLog.log) 
class=`airport -s | grep @PHICOMM_D0 | wc -l`
#usb model
model=0
#wifi model
#model=1

if [ ${class//[[:space:]]} -gt 0 ]; then
	if [ $model -eq 0 ];then
		echo "enter usb model" >> /Users/paradox/Log/netLog.log 
		sudo networksetup -setairportpower en0 off && echo "close wifi" >> /Users/paradox/Log/netLog.log
	else 
		echo "enter wifi manual" >> /Users/paradox/Log/netLog.log 
		sudo networksetup -setmanual wi-fi 10.10.20.121 255.255.255.0 10.10.20.250 
		sudo networksetup -setdnsservers wi-fi 114.114.114.114 114.114.115.115
		echo "set wifi manuallly success" >> /Users/paradox/Log/netLog.log 
	fi
	sudo open /Applications/Synergy.app/ && echo "open synergy sucessfully" >> /Users/paradox/Log/netLog.log || echo "open synergy failed" >> /Users/paradox/Log/netLog.log
else
	echo "enter wifi dhcp" >> /Users/paradox/Log/netLog.log
    sudo networksetup -setdhcp "Wi-Fi" && echo "set wifi dhcp sucessfully" >> /Users/paradox/Log/netLog.log || echo "set wifi dhcp failed" >> /Users/paradox/Log/netLog.log
fi

