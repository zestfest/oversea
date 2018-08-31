{% set master = salt['master.minion']() %}

{% if salt['saltutil.runner']('validate.setup') == False %}

validate failed:
  salt.state:
    - name: test.fail_without_changes
    - tgt: {{ master }}
    - failhard: True

{% endif %}

sync master:
  salt.state:
    - tgt: {{ master }}
    - sls: ceph.sync

salt-api:
  salt.state:
    - tgt: {{ master }}
    - sls: ceph.salt-api

{% set notice = salt['saltutil.runner']('advise.salt_run') %}

repo master:
  salt.state:
    - tgt: {{ master }}
    - sls: ceph.repo

metapackage master:
  salt.state:
    - tgt: {{ master }}
    - sls: ceph.metapackage

prepare master:
  salt.state:
    - tgt: {{ master }}
    - sls: ceph.updates

{% set kernel= grains['kernelrelease'] | replace('-default', '')  %}

unlock:
  salt.runner:
    - name: filequeue.remove
    - queue: 'master'
    - item: 'lock'

restart master:
  salt.state:
    - tgt: {{ master }}
    - sls: ceph.updates.restart

complete marker:
  salt.runner:
    - name: filequeue.enqueue
    - queue: 'master'
    - item: 'complete'

ready:
  salt.runner:
    - name: minions.ready
    - timeout: {{ salt['pillar.get']('ready_timeout', 300) }}

