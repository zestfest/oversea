
{% set custom = salt['pillar.get']('ganesha_install', 'not a file') %}
{% from 'ceph/macros/os_switch.sls' import os_switch with context %}

include:
  - .{{ os_switch(custom) }}
