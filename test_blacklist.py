#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-23 15:51:46 krylon>
#
# /data/code/python/pythia/test_blacklist.py
# created on 23. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.test_blacklist

(c) 2024 Benjamin Walkenhorst
"""


import unittest

from pythia.data import Blacklist, BlacklistItem


class BlacklistTest(unittest.TestCase):
    """Test the blacklist."""

    def test_blacklist(self):
        """Test individual items."""
        bl = Blacklist(
            BlacklistItem("[.]git"),
            BlacklistItem("bak[.]"),
            BlacklistItem("[.]bak$"),
            BlacklistItem("#$"),
        )

        test_cases = (
            ("/home/username/code/.git", True),
            ("/home/username/.config/bak.fish", True),
            ("/home/username/.zshrc", False),
            ("/home/username/Documents/Manual.pdf", False),
            ("/home/username/Videos/cat_chasing_vacuum_cleaner.pdf", False),
            ("/home/username/.emacs.d/init.el", False),
            ("/home/username/.emacs.d/#init.el#", True),
        )

        for t in test_cases:
            m = bl.match(t[0])
            self.assertEqual(m, t[1], f"Unexpected result from bl.match({t[0]}) - {m}")


# Local Variables: #
# python-indent: 4 #
# End: #
