#!/bin/bash

for i in {0..3}
do
  dd if=/dev/zero of=/root/disk$i bs=1G count=2
  losetup -f /root/disk$i
done
