#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:10:50 krylon>
#
# /data/code/python/pythia/inspector.py
# created on 26. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.inspector

(c) 2024 Benjamin Walkenhorst
"""


from pythia import common
from pythia.data import File
from pythia.extractor.base import Extractor
from pythia.extractor.pdf import PDFExtractor
from pythia.extractor.audio import AudioExtractor


class Inspector:  # pylint: disable-msg=R0903
    """Inspector deals with file content."""

    def __init__(self) -> None:
        self.log = common.get_logger("Inspector")

    def get_extractor(self, f: File) -> Extractor:
        """Attempt to find the right Extractor for the given File."""
        match f.suffix():
            case "pdf":
                return PDFExtractor()
            case "mp3" | "ogg" | "flac" | "opus":
                return AudioExtractor()


# Local Variables: #
# python-indent: 4 #
# End: #
