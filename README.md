[![Build Status](https://travis-ci.org/zestfest/oversea.svg?branch=master)](https://travis-ci.org/zestfest/oversea)

# OverSea
This is a fork of [DeepSea](https://github.com/SUSE/DeepSea).  The focus is to allow anyone to try Ceph reasonably quickly.  

# Other Solutions
While OverSea is Salt and python based, those considering [Kubernetes](https://github.com/kubernetes/kubernetes) should check out [Rook](https://github.com/rook/rook).  For those interested in Ansible rather than Salt should visit [Ceph-Ansible](https://github.com/ceph/ceph-ansible).

# What is it? 
A collection of [Salt](https://saltstack.com/salt-open-source/) files, modules and orchestrations for deploying and managing [Ceph](https://ceph.com/).  Salt is an automation framework and configuration management tool that is popular with devops strategies of managing equipment.  Ceph is a software defined storage solution permitting the use of commodity hardware.

# Prerequisite
The main prerequisite is a Salt cluster which can be hosted on physical or virtual machines.  While the bare minimum is 4 nodes, many OverSea and Ceph features are practical in clusters of a dozen nodes or more.  

Provisioning hardware or virtual machines can be most time consuming.  For development environments, see [Vagrant-Ceph](https://github.com/openSUSE/vagrant-ceph).  

# Installation
Coming soon...



