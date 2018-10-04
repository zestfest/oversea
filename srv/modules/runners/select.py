# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,modernize-parse-error
"""
The list of minions related to a Salt target is often needed for operations.
"""

from __future__ import absolute_import
from __future__ import print_function
import logging
import os
import sys
import re
# pylint: disable=import-error,3rd-party-module-not-gated,redefined-builtin
import salt.client

log = logging.getLogger(__name__)


def help_():
    """
    Usage
    """
    usage = ('salt-run select.minions key=value [key=value...]:\n'
             'salt-run select.minions host=True key=value [key=value...]:\n\n'
             'salt-run select.minions host=True format="{}" key=value [key=value...]:\n\n'
             '    Return an array of minions based on the target criteria\n'
             '    possibly formatted with format string\n'
             '    Note that the format string must contain exactly one {}\n'
             '\n\n'
             'salt-run select.one_minion key=value [key=value...]:\n\n'
             '    Return a random single minion that meets the critieria\n'
             '\n\n'
             'salt-run select.public_addresses key=value [key=value...]:\n'
             'salt-run select.public_addresses tuples=True key=value [key=value...]:\n'
             'salt-run select.public_addresses tuples=True host=True key=value [key=value...]:\n\n'
             '    Returns an array of public addresses for the specified criteria\n'
             '\n\n'
             'salt-run select.attr attr=value key=value [key=value...]:\n'
             'salt-run select.attr host=True attr=value key=value [key=value...]:\n\n'
             '    Returns an array of pillar values for the specified criteria\n'
             '\n\n'
             'salt-run select.from pillar=var role=default_role attr=value1,value2 :\n\n'
             '    Returns an array of grain values that matches the pillar variable.\n'
             '    Defaults to role if variable is not found.\n'
             '\n\n')
    print(usage)
    return ""


def _grain_host(client, minion):
    """
    Return the host grain for a given minion, for use a short hostname
    """
    return list(client.cmd(minion, 'grains.item', ['host']).values())[0]['host']


def minions(host=False, format='{}', **kwargs):
    """
    Some targets needs to match all minions within a search criteria.
    """
    if not isinstance(format, str):
        raise TypeError("format argument is not a string")
    criteria = []
    for key in kwargs:
        if key[0] == "_":
            continue
        values = kwargs[key]
        if not isinstance(values, list):
            values = [values]
        for value in values:
            criteria.append("I@{}:{}".format(key, value))

    search = " and ".join(criteria)

    # When search matches no minions, salt prints to stdout.  Suppress stdout.
    _stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    local = salt.client.LocalClient()
    _minions = local.cmd(search, 'pillar.get', ['id'], tgt_type="compound")

    sys.stdout = _stdout

    if host:
        return [format.format(_grain_host(local, k)) for k in _minions.keys()]
    return [format.format(m) for m in _minions.keys()]


def one_minion(**kwargs):
    """
    Some steps only need to be run once, but on any minion in a specific
    search.  Return the first matching key.
    """
    ret = [None]
    ret = minions(**kwargs)
    return ret[0]


def first(**kwargs):
    """
    Some steps only need to be run once, but on any minion in a specific
    search.  Return the first matching key.
    """
    ret = sorted(minions(**kwargs))
    if ret:
        return ret[0]
    return ""


def public_addresses(tuples=False, host=False, **kwargs):
    """
    Returns an array of public addresses matching the search critieria.
    Can also return an array of tuples with fqdn or short name.
    """
    criteria = []
    for key in kwargs:
        if key[0] == "_":
            continue
        criteria.append("I@{}:{}".format(key, kwargs[key]))

    search = " and ".join(criteria)

    # When search matches no minions, salt prints to stdout.  Suppress stdout.
    _stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    local = salt.client.LocalClient()
    result = local.cmd(search, 'public.address', [], tgt_type="compound")

    sys.stdout = _stdout

    if tuples:
        if host:
            addresses = [[_grain_host(local, k), v] for k, v in result.items()]
        else:
            addresses = [[k, v] for k, v in result.items()]
    else:
        addresses = []
        for entry in result:
            addresses.append(result[entry])
    return addresses


def attr(host=False, **kwargs):
    """
    Return a paired list of minions and a given attribute
    """
    criteria = []
    attribute = None
    for key in kwargs:
        if key[0] == "_":
            continue
        if key == 'attr':
            attribute = kwargs['attr']
            continue
        criteria.append("I@{}:{}".format(key, kwargs[key]))

    search = " and ".join(criteria)

    # When search matches no minions, salt prints to stdout.  Suppress stdout.
    _stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    local = salt.client.LocalClient()
    _minions = local.cmd(search, 'pillar.get', [attribute], tgt_type="compound")

    sys.stdout = _stdout

    if host:
        pairs = [[_grain_host(local, k), v] for k, v in _minions.items()]
    else:
        pairs = [[k, v] for k, v in _minions.items()]
    return pairs


def from_(pillar, role, *args, **kwargs):
    """
    Return a list of roles and corresponding grains for the provided pillar
    argument or role argument.

    salt-run select.from rgw_configurations rgw host fqdn
    salt-run select.from pillar=data, role=rgw, attr="host, fqdn"

    Note: Support the second form because Jinja hates us.
    """

    if 'attr' in kwargs:
        args = re.split(r',\s*', kwargs['attr'])

    # When search matches no minions, salt prints to stdout.  Suppress stdout.
    _stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    local = salt.client.LocalClient()
    search = "I@roles:master"
    try:
        roles = list(local.cmd(search, 'pillar.get', [pillar], tgt_type="compound").values())[0]
    # pylint: disable=bare-except
    except:
        roles = []

    sys.stdout = _stdout

    if not roles:
        # With no pillar variable, check for minions with assigned role
        result = minions(roles=role)
        if result:
            roles = [role]

    results = []
    for _role in roles:
        minion_list = minions(roles=_role)
        for minion in minion_list:
            grains_result = list(local.cmd(minion, 'grains.item', list(args)).values())[0]
            small = [_role]
            for arg in list(args):
                small.append(grains_result[arg])
            results.append(small)

    if results:
        return results
    return [[None] * (1 + len(args))]

__func_alias__ = {
                 'from_': 'from',
                 'help_': 'help',
                 }
