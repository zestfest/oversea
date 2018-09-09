# -*- coding: utf-8 -*-
# pylint: disable=modernize-parse-error,too-few-public-methods
# pylint: disable=visually-indented-line-with-same-indent-as-next-logical-line
# pylint: disable=fixme,no-self-use
"""
Functions that parse `ceph fs dump`
"""

from __future__ import absolute_import
from __future__ import print_function
import logging
import json
from subprocess import Popen, PIPE

log = logging.getLogger(__name__)


def popen(cmd):
    """
    Return rc, stdout, stderr of cmd
    """
    stdout = []
    stderr = []
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    for line in proc.stdout:
        line = line.decode('ascii')
        stdout.append(line.rstrip('\n'))
    for line in proc.stderr:
        line = line.decode('ascii')
        stderr.append(line.rstrip('\n'))
    proc.wait()
    return (proc.returncode, stdout, stderr)


def fs_name():
    """
    Return the fs_name
    """
    _, out, _ = popen("ceph fs dump --format=json".split())
    data = json.loads(out[1])
    return data['filesystems'][0]['mdsmap']['fs_name']


def ranks_in():
    """
    Return the number of mds entries
    """
    _, out, _ = popen("ceph fs dump --format=json".split())
    data = json.loads(out[1])
    return len(data['filesystems'][0]['mdsmap']['in'])
