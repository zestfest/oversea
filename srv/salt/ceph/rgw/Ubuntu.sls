
include:
  - .keyring

install rgw:
  pkg.installed:
    - name: radosgw
    - refresh: True

{% for role in salt['rgw.configurations']() %}

start {{ role }}:
  service.running:
    - name: ceph-radosgw@{{ role + "." + grains['host'] }}
    - enable: True

{% endfor %}

