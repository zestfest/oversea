#!/bin/bash

hostnamectl set-hostname $1.ceph

# ZeroTier
dpkg -i /tmp/zerotier-one_1.2.12_amd64.deb
apt-get install -f
zerotier-cli join $2
cat /tmp/hosts >> /etc/hosts
ip address add `awk '/'$1'/ {print $1}' /etc/hosts` dev zt2lrufmtu

# SaltStack
curl -L https://bootstrap.saltstack.com > /tmp/bootstrap-salt
chmod +x /tmp/bootstrap-salt

if [ "$1" == "admin" ]
then
  chmod +x /tmp/install_salt_master.sh
  /tmp/install_salt_master.sh $3
else
  /tmp/bootstrap-salt || /tmp/bootstrap-salt
fi
