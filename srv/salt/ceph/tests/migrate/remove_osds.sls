
Removing OSDs:
  test.nop

{% for id in salt['osd.list']() %}

updating/removing {{ id }}:
  module.run:
    - name: osd.remove
    - osd_id: {{ id }}

removing {{ id }}:
  module.run:
    - name: osd.remove
    - osd_id: {{ id }}

{% endfor %}


