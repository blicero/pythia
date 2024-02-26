#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-26 09:41:06 krylon>
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

from pythia import common
from pythia.extractor.base import BaseExtractor


class ODTExtractor(BaseExtractor):
    """Extractor for ODF text documents"""

    def __init__(self):
        self._log = common.get_logger("ODTExtractor")

# Local Variables: #
# python-indent: 4 #
# End: #
