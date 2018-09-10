#!/bin/bash

/tmp/bootstrap-salt -M || /tmp/boostrap-salt -M
count=0
while [ `ls /etc/salt/pki/master/minions|wc -l` -ne "$1" ]
do
    salt-key -A -y
    sleep 5
    count=$((count + 1))
    if [ $count -gt 30 ]
    then
        echo "Giving up" >&2
        exit 1
    fi
done

