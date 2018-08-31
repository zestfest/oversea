
stage prep dependencies ubuntu:
  pkg.installed:
    - pkgs:
      - lsscsi
      - pciutils
      - gdisk
      - python3-boto
      - python3-rados
      - iperf
      - jq
      - hwinfo
    - fire_event: True
    - refresh: True

