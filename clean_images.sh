#!/bin/bash
set -x
disk_usage=`df -h |grep /dev/vdb |awk '{print $5}'| cut -d % -f 1`
echo disk_usage: $disk_usage
if [ $disk_usage -gt 80 ]; then

  docker images |awk '{print $1":"$2}' |xargs docker rmi

fi
