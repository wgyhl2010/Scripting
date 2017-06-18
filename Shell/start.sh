#!/bin/sh
pkg="$2"; 
echo $pkg; 
start(){ 
 
        java -Xms512m -Xmx1024m -jar /usr/websync/WebSiteCheck/$pkg/WebSiteCheck.jar & 
        echo "WebSiteCheck start ..." 
} 
 
stop(){ 
 
        echo "WebSiteCheck stop ..."     
 
        ps -ef|grep WebSiteCheck.jar|awk '{print $2}'|while read pid 
        do 
		echo "kill -9 $pid ..." 
		kill -9 $pid 
	done 
} 
 
case "$1" in 
 
start) 
 
  start 
 
  ;;

stop)

  stop

  ;;

restart)

  stop

  start

  ;;

*)
  printf 'Usage: %s {start|stop|restart}\n' "$prog"
  exit 1
  ;;
esac
exit 0
