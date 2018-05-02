
{% set label = "delay" %}

Replace Update Destroyed:
  salt.state:
    - tgt: I@roles:storage
    - sls: ceph.tests.replace.update_destroyed
    - tgt_type: compound

Replace Disengage {{ label }}:
  salt.runner:
    - name: disengage.safety
    - failhard: True

Replace keyword arguments:
  salt.runner:
    - name: replace.osd
    - arg:
      - 0
    - kwarg:
      delay: 1
      timeout: 1
    - failhard: True

Replace Check OSDs {{ label }}:
  salt.state:
    - tgt: {{ salt['master.minion']() }}
    - sls: ceph.tests.replace.check_0
    - failhard: True

Replace Restore OSDs {{ label }}:
  salt.state:
    - tgt: I@roles:storage
    - sls: ceph.tests.replace.restore_osds
    - tgt_type: compound
    - failhard: True

Replace Wait for Ceph {{ label }}:
  salt.state:
    - tgt: {{ salt['master.minion']() }}
    - sls: ceph.wait.until.OK
    - failhard: True

