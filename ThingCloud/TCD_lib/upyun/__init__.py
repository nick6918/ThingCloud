#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .upyun import UpYun, UpYunServiceException, UpYunClientException
from .upyun import ED_AUTO, ED_TELECOM, ED_CNC, ED_CTT, __version__

__title__ = 'upyun'
__author__ = 'Monkey Zhang (timebug)'
__license__ = 'MIT License: http://www.opensource.org/licenses/mit-license.php'
__copyright__ = 'Copyright 2015 UPYUN'

__all__ = [
    'UpYun', 'UpYunServiceException', 'UpYunClientException',
    'ED_AUTO', 'ED_TELECOM', 'ED_CNC', 'ED_CTT', '__version__'
]
