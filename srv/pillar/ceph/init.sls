
{% include 'ceph/cluster/' + grains['id'] + '.sls' ignore missing %}

{% include 'ceph/oversea_minions.sls' ignore missing %}


