{% set shared_secret = salt['cmd.run']('cat /proc/sys/kernel/random/uuid') %}
/etc/salt/master.d/sharedsecret.conf:
  file.managed:
    - source:
      - salt://ceph/salt-api/files/sharedsecret.conf.j2
    - template: jinja
    - user: {{ salt['oversea.user']() }}
    - group: {{ salt['oversea.group']() }}
    - mode: 600
    - replace: False
    - context:
      shared_secret: {{ shared_secret }}
