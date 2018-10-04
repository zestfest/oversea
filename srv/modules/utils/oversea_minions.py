# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,modernize-parse-error
#
# The salt-api calls functions with keywords that are not needed
# pylint: disable=unused-argument
"""
The oversea_minions variable is in /srv/pillar/ceph/oversea_minions.sls.  For
those sites with existing Salt minions that should not be storage hosts, this
variable can be customized to any Salt target.
"""

from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import logging
# pylint: disable=import-error,3rd-party-module-not-gated,redefined-builtin
import salt.client

log = logging.getLogger(__name__)


class OverseaMinions(object):
    """
    The oversea_minions pillar variable constrains which minions to use.
    """

    def __init__(self, **kwargs):
        """
        Initialize client and variables
        """
        self.local = salt.client.LocalClient()
        self.oversea_minions = self._query()
        self.matches = self._matches()

    def _query(self):
        """
        Returns the value of oversea_minions
        """
        # When search matches no minions, salt prints to stdout.
        # Suppress stdout.
        _stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        # Relying on side effect - pylint: disable=unused-variable
        ret = self.local.cmd('*', 'saltutil.pillar_refresh')
        minions = self.local.cmd('*', 'pillar.get', ['oversea_minions'],
                                 tgt_type="compound")
        sys.stdout = _stdout
        for minion in minions:
            if minions[minion]:
                return minions[minion]

        log.error("oversea_minions is not set")
        return []

    def _matches(self):
        """
        Returns the list of matched minions
        """
        if self.oversea_minions:
            # When search matches no minions, salt prints to stdout.
            # Suppress stdout.
            _stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            result = self.local.cmd(self.oversea_minions,
                                    'pillar.get',
                                    ['id'],
                                    tgt_type="compound")
            sys.stdout = _stdout
            return list(result.keys())
        return []


def help_():
    """
    Usage
    """
    usage = ('salt-run oversea_minions.show:\n\n'
             '    Displays oversea_minions value\n'
             '\n\n'
             'salt-run oversea_minions.matches:\n\n'
             '    Returns an array of matched minions\n'
             '\n\n')
    print(usage)
    return ""


def show(**kwargs):
    """
    Returns oversea_minions value
    """
    target = OverseaMinions()
    return target.oversea_minions


def matches(**kwargs):
    """
    Returns array of matched minions
    """
    target = OverseaMinions()
    return target.matches


__func_alias__ = {
                 'help_': 'help',
                 }
