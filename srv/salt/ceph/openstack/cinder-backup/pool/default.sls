{% set prefix = pillar['openstack_prefix'] + "-" if 'openstack_prefix' in pillar else "" %}
{{ prefix }}cinder-backup pool:
  cmd.run:
    - name: "ceph osd pool create {{ prefix }}cloud-backups 128"
    - unless: "ceph osd pool ls | grep -q '^{{ prefix }}cloud-backups$'"
    - fire_event: True

{{ prefix }}cinder-backup pool enable application:
  cmd.run:
    - name: "ceph osd pool application enable {{ prefix }}cloud-backups rbd || :"

