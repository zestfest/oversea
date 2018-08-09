
install_ganesha:
  pkg.installed:
    - pkgs:
        - nfs-ganesha
        - nfs-ganesha-ceph
    - fire_event: True
