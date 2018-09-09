
run test state:
  salt.state:
    - tgt: '{{ salt['pillar.get']('oversea_minions') }}'
    - tgt_type: compound
    - sls: ceph.tests.os_switch

