
{% set label = "multiple" %}

Remove Update Destroyed for 0:
  salt.state:
    - tgt: I@roles:storage
    - sls: ceph.tests.replace.update_destroyed
    - tgt_type: compound

Remove Update Destroyed for 1:
  salt.state:
    - tgt: I@roles:storage
    - sls: ceph.tests.replace.update_destroyed1
    - tgt_type: compound

Remove Disengage {{ label }}:
  salt.runner:
    - name: disengage.safety

Remove Multiple arguments:
  salt.runner:
    - name: remove.osd
    - arg:
      - 0
      - 1

Remove Check OSDs {{ label }}:
  salt.state:
    - tgt: {{ salt['master.minion']() }}
    - sls: ceph.tests.remove.check_absent

Remove Restore OSDs {{ label }}:
  salt.state:
    - tgt: 'I@roles:storage'
    - sls: ceph.tests.remove.restore_osds
    - tgt_type: compound

Remove Wait for Ceph {{ label }}:
  salt.state:
    - tgt: {{ salt['master.minion']() }}
    - sls: ceph.wait.until.OK

