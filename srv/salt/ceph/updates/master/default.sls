update deepsea:
  pkg.latest:
    - pkgs:
      - oversea
      - salt-master
      - salt-minion
    - dist-upgrade: True
