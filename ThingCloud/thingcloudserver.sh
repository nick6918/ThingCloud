#!/bin/bash
case "$1" in
start|st)
	echo "Starting uwsgi..."
	#/home/weifanding/bin/gunicorn -c gunicorn.conf thingcloud.ini
	/home/weifanding/bin/gunicorn -c guncloud.conf ThingCloud.wsgi:application
	echo "Done!"
	;;
restart|rt)
	echo "Restarting..."
	kill -HUP `/var/log/gunicorn/thingcloudserver.pid`
	echo "Done!"
	;;
stop|sp)
	echo "Stop ..."
	kill -9 `cat /var/log/gunicorn/thingcloudserver.pid`
	echo "Done!"
	;;
*)
	echo "[start][restart][stop]"
	;;
esac
