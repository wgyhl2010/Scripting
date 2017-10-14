# /usr/bin
baidupcs set --list_page_size=10000
olddir=$(baidupcs pwd)
downpath=$2
baidupcs cd $1
files=$(baidupcs ls | awk '{a[NR]=$5}END{for(i=3;i<NR-2;i++)print a[i]}')
for file in $files
	do 
		echo "start download $file"
		if [ ! $downpath ];then
			baidupcs download $file ${file##*/}
		else
			baidupcs download $file "$2${file##*/}"
		fi
	done
baidupcs cd $olddir
