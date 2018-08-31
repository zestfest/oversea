
base:
  pkgrepo.managed:
    - humanname: Ceph Mimic
    - name: deb https://download.ceph.com/debian-mimic/ bionic main
    - dist: bionic
    - gpgcheck: 1
    - key_url: https://download.ceph.com/keys/release.asc
