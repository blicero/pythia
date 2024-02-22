#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-22 19:21:46 krylon>
#
# /data/code/python/pythia/data.py
# created on 21. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.data

(c) 2024 Benjamin Walkenhorst

This modules defines data types used throughout the application.
"""

import os
import stat
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any


@dataclass(slots=True)
class Folder:  # pylint: disable-msg=R0903
    """Folder reprents a directory tree that we might want to scan."""

    fid: int
    path: str
    time_scanned: datetime


class FileType(Enum):
    """FileType defines constants for identifying various types of files."""
    Text = auto()
    PDF = auto()
    Image = auto()
    Document = auto()
    Other = auto()


class File:  # pylint: disable-msg=R0903,R0902
    """File represents a file and some metadata, plus any text we manage
    to extract from it."""

    __slots__ = [
        "fid",
        "folder_id",
        "path",
        "time_scanned",
        "mtime",
        "content_type",
        "mime_type",
        "content",
        "meta",
    ]

    fid: int
    folder_id: int
    path: str
    time_scanned: datetime
    mtime: datetime
    content_type: FileType
    mime_type: str
    content: str
    meta: dict

    def __init__(self, path: str, fields: dict[str, Any]) -> None:
        self.fid = 0
        self.folder_id = fields.get("folder_id", 0)
        self.path = path
        self.time_scanned = fields.get("time_scanned", datetime.now())
        if "time_modified" in fields:
            self.mtime = fields["time_modified"]
        else:
            st = os.stat(path)
            mtime = datetime.fromtimestamp(st[stat.ST_MTIME])
            self.mtime = mtime
        self.content_type = fields.get("content_type", FileType.Other)
        self.meta = fields.get("meta", {})
        self.content = fields.get("content", "")

# Local Variables: #
# python-indent: 4 #
# End: #
