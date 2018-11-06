# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,modernize-parse-error
"""
Runner to remove a single osd
"""

from __future__ import absolute_import
from __future__ import print_function
import logging
# pylint: disable=import-error,3rd-party-module-not-gated,redefined-builtin
import salt.client
import salt.runner

log = logging.getLogger(__name__)


def help_():
    """
    Usage
    """
    usage = ('salt-run remove.osd id [id ...][force=True]:\n\n'
             '    Removes an OSD\n'
             '\n\n')
    print(usage)
    return ""


def osd(*args, **kwargs):
    """
    Remove an OSD gracefully or forcefully.  Always attempt to remove
    ID from Ceph even if OSD has been removed from the minion.
    """
    result = __salt__['replace.osd'](*args, called=True, **kwargs)

    # Replace OSD exited early
    if not result:
        return ""

    master_minion = result['master_minion']
    osds = result['osds']

    local = salt.client.LocalClient()

    for osd_id in osds:
        cmds = ['ceph osd crush remove osd.{}'.format(osd_id),
                'ceph auth del osd.{}'.format(osd_id),
                'ceph osd rm {}'.format(osd_id)]

        print("Removing osd {} from Ceph".format(osd_id))
        for cmd in cmds:
            local.cmd(master_minion, 'cmd.run', [cmd], tgt_type='compound')

    return ""


__func_alias__ = {
                 'help_': 'help',
                 }
