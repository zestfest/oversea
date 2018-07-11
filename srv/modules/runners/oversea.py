# -*- coding: utf-8 -*-
"""
This runner implements helper functions for OverSea in general
"""

from __future__ import absolute_import
import re

OVERSEA_VERSION = 'DEVVERSION'


# pylint: disable=redefined-builtin
def version(**kwargs):
    """
    Returns the OverSea version info currently installed
    """
    format_ = kwargs['format'] if 'format' in kwargs else 'plain'

    if format_ == 'json':
        ver = re.findall(r'^\d\.\d\.?\d?', OVERSEA_VERSION)
        offset = re.findall(r'\+\d+', OVERSEA_VERSION)
        hash_ = re.findall(r'[\w]{7,8}$', OVERSEA_VERSION)

        return {'full_version': OVERSEA_VERSION,
                'version': ver[0] if ver else '0.0.0',
                'git_offset': offset[0].lstrip('+') if offset else '0',
                'git_hash': hash_[0][-7:] if hash_ else ''}

    return OVERSEA_VERSION
