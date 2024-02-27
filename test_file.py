#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:04:20 krylon>
#
# /data/code/python/pythia/test_file.py
# created on 26. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.test_file

(c) 2024 Benjamin Walkenhorst
"""

import unittest

from pythia.data import File


class FileTest(unittest.TestCase):
    """Tests for the File."""

    def test_find_suffix(self) -> None:
        """Test extracting the suffix from file names."""
        test_cases = (
            ("/data/Documents/report2022.pdf", "pdf"),
            ("/home/somebody/image.jpg", "jpg"),
            ("/data/Curriculum_Vitae.docx", "docx"),
            ("/home/krylon/.emacs", "emacs"),
            ("/home/krylon/abobo", ""),
        )

        for c in test_cases:
            f = File(c[0], {})
            suffix = f.suffix()
            self.assertEqual(suffix, c[1])

# Local Variables: #
# python-indent: 4 #
# End: #
