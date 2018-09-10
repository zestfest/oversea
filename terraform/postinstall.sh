#!/bin/bash

hostnamectl set-hostname $1.ceph

# ZeroTier
dpkg -i /tmp/zerotier-one_1.2.12_amd64.deb
apt-get install -f
zerotier-cli join $2
cat /tmp/hosts >> /etc/hosts
ip address add `awk '/'$1'/ {print $1}' /etc/hosts` dev zt2lrufmtu

# Loopback
if [ "${1##data}" != "$1" ]
then
    chmod +x /tmp/create_disks.sh
    /tmp/create_disks.sh
fi

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

# OverSea
if [ "$1" == "admin" ]
then
  wget https://github.com/zestfest/oversea/releases/download/unstable/oversea_0unstable0_all.deb
  dpkg -i oversea_0unstable0_all.deb
  apt-get install -f
  mkdir -p /srv/pillar/ceph/stack/ceph
  mkdir -p /srv/pillar/ceph/proposals
  mv /tmp/oversea_minions.sls /srv/pillar/ceph/
  mv /tmp/cluster.yml /srv/pillar/ceph/stack/ceph
  mv /tmp/policy.cfg /srv/pillar/ceph/proposals/

  systemctl restart salt-master
  salt '*' test.ping

  set -x
  salt-run state.orch ceph.stage.0
  salt-run state.orch ceph.stage.1
  salt-run state.orch ceph.stage.2
  salt-run state.orch ceph.stage.3
  salt-run state.orch ceph.stage.4

  salt-run state.orch ceph.smoketests
  set +x
fi
