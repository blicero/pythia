#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-23 18:38:06 krylon>
#
# /data/code/python/pythia/test_database.py
# created on 23. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.test_database

(c) 2024 Benjamin Walkenhorst
"""

import unittest

from krylib import isdir

TEST_ROOT: str = "/tmp/"

# On my main development machines, I have a RAM disk mounted at /data/ram.
# If it's available, I'd rather use that than /tmp which might live on disk.
if isdir("/data/ram"):
    TEST_ROOT = "/data/ram"


class DatabaseTest(unittest.TestCase):
    """Test the damn database."""

# Local Variables: #
# python-indent: 4 #
# End: #
