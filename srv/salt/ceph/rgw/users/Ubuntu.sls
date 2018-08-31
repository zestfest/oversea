
install rgw:
  pkg.installed:
    - pkgs:
      - radosgw
      - libs3-2
    - refresh: True

add users:
  module.run:
    - name: rgw.add_users
