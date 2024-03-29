#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:02:38 krylon>
#
# /data/code/python/pythia/extractor/base.py
# created on 24. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.extractor.base

(c) 2024 Benjamin Walkenhorst
"""

import logging
from abc import ABC, abstractmethod

from pythia import common
from pythia.data import File


class Extractor(ABC):  # pylint: disable-msg=R0903
    """Abstract base class for the various extractors."""

    __slots__ = [
        "name",
        "log",
    ]

    log: logging.Logger
    name: str

    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.log = common.get_logger(self.name)

    @abstractmethod
    def process(self, f: File) -> bool:
        """Process a file, attempt to extract content and metadata."""


# Local Variables: #
# python-indent: 4 #
# End: #
