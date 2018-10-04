
{% set label = "force" %}

Remove Update Destroyed {{ label }}:
  salt.state:
    - tgt: I@roles:storage
    - sls: ceph.tests.replace.update_destroyed
    - tgt_type: compound

Remove Disengage {{ label }}:
  salt.runner:
    - name: disengage.safety

Remove forced removal:
  salt.runner:
    - name: remove.osd
    - arg:
      - 0
    - kwarg:
      force: True

Remove Check OSDs {{ label }}:
  salt.state:
    - tgt: {{ salt['master.minion']() }}
    - sls: ceph.tests.remove.check_0

Remove Restore OSDs {{ label }}:
  salt.state:
    - tgt: I@roles:storage
    - sls: ceph.tests.remove.restore_osds
    - tgt_type: compound

Remove Wait for Ceph {{ label }}:
  salt.state:
    - tgt: {{ salt['master.minion']() }}
    - sls: ceph.wait.until.OK

