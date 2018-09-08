# -*- coding: utf-8 -*-
# pylint: disable=modernize-parse-error,too-few-public-methods
# pylint: disable=visually-indented-line-with-same-indent-as-next-logical-line
# pylint: disable=fixme,no-self-use
"""
"""

from __future__ import absolute_import
from __future__ import print_function
import logging
import ipaddress
import json
import os
from os.path import dirname
import re
import sys
import glob
from subprocess import Popen, PIPE
import pprint


log = logging.getLogger(__name__)

def popen(cmd):
    """
    Return stdout, stderr of cmd
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
    """
    rc, out, err = popen("ceph fs dump --format=json".split())
    #pprint.pprint(out[1])
    data = json.loads(out[1])
    return data['filesystems'][0]['mdsmap']['fs_name']

def ranks_in():
    """
    """
    rc, out, err = popen("ceph fs dump --format=json".split())
    #pprint.pprint(out[1])
    data = json.loads(out[1])
    return len(data['filesystems'][0]['mdsmap']['in'])
