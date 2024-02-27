#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:02:54 krylon>
#
# /data/code/python/pythia/extractor/odt.py
# created on 26. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.extractor.odt

(c) 2024 Benjamin Walkenhorst
"""

from pythia.data import File
from pythia.extractor.base import Extractor


class ODTExtractor(Extractor):  # pylint: disable-msg=R0903
    """Extractor for ODF text documents"""

    def process(self, f: File) -> bool:
        """Attempt to extract metadata from ODF Documents"""
        return False

# Local Variables: #
# python-indent: 4 #
# End: #
