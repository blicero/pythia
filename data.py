#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:03:54 krylon>
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

import json
import mimetypes
import os
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from threading import Lock
from typing import Any, Final, Union


class BlacklistItem:  # pylint: disable-msg=R0903
    """An item in the blacklist"""

    __slots__ = ["iid", "pat", "cnt"]

    iid: int
    pat: re.Pattern
    cnt: int

    def __init__(self, pat: Union[str, re.Pattern], cnt: int = 0, iid: int = 0) -> None:
        self.iid = iid
        self.cnt = cnt
        if isinstance(pat, str):
            self.pat = re.compile(pat)
        else:
            self.pat = pat

    def match(self, s: str) -> bool:
        """Check if the Item's pattern matches the given string."""
        m = self.pat.search(s)
        if m is None:
            return False
        self.cnt += 1
        return True


class Blacklist:  # pylint: disable-msg=R0903
    """A sorted blacklist of patterns to match filenames against."""

    __slots__ = ["patterns", "lock"]

    patterns: list[BlacklistItem]
    lock: Lock

    def __init__(self, *pat: Union[str, re.Pattern, BlacklistItem]) -> None:
        self.patterns = []
        self.lock = Lock()

        for i in pat:
            if isinstance(i, (str, re.Pattern)):
                p = BlacklistItem(i)
                self.patterns.append(p)
            else:
                assert isinstance(i, BlacklistItem)
                self.patterns.append(i)

    def match(self, path: str) -> bool:
        """Check if any of the patterns in the Blacklist match the given string."""
        with self.lock:
            for p in self.patterns:
                if p.match(path):
                    self.__sort()
                    return True
            return False

    def __sort(self) -> None:
        """Sort the BlacklistItems so that the items with the most hits move to the
        front of the list."""
        self.patterns.sort(key=lambda x: -x.cnt)


@dataclass(slots=True, kw_only=True)
class Folder:  # pylint: disable-msg=R0903
    """Folder reprents a directory tree that we might want to scan."""

    fid: int
    path: str
    time_scanned: datetime

    def __init__(self, **fields) -> None:
        self.fid = fields.get("fid", 0)
        self.path = fields["path"]
        self.time_scanned = fields.get("time_scanned", datetime.now())


class FileType(Enum):
    """FileType defines constants for identifying various types of files."""
    Text = auto()
    PDF = auto()
    Image = auto()
    Document = auto()
    Other = auto()


suffix_pat: Final[re.Pattern] = re.compile(r"[.](\w+)$")


class File:  # pylint: disable-msg=R0903,R0902
    """File represents a file and some metadata, plus any text we manage
    to extract from it."""

    __slots__ = [
        "fid",
        "folder_id",
        "path",
        "time_scanned",
        "content_type",
        "mime_type",
        "content",
        "meta",
    ]

    fid: int
    folder_id: int
    path: str
    time_scanned: datetime
    content_type: FileType
    mime_type: str
    content: str
    meta: dict

    def __init__(self, path: str, fields: dict[str, Any]) -> None:
        self.fid = 0
        self.folder_id = fields.get("folder_id", 0)
        self.path = path
        self.time_scanned = fields.get("time_scanned", datetime.now())
        self.content_type = fields.get("content_type", FileType.Other)
        self.meta = fields.get("meta", {})
        # self.mime_type = fields.get("mime_type", "application/octet-stream")
        if "mime_type" in fields:
            self.mime_type = fields["mime_type"]
        else:
            mt = mimetypes.guess_type(path)
            if mt[0] is None:
                self.mime_type = "application/octet-stream"
            else:
                self.mime_type = mt[0]
        self.content = fields.get("content", "")

    def suffix(self) -> str:
        """Return the filename's suffix, if it has one."""
        m = suffix_pat.search(self.path)
        if m is None:
            return ""
        return m[1].lower()

    @classmethod
    def from_db(cls, row: tuple[Any, ...]) -> Any:
        """Recreate a File object from a database record."""
        fields = {
            "folder_id": row[1],
            "time_scanned": datetime.fromtimestamp(row[3]),
            "content_type": FileType(row[5]),
            "mime_type": row[6],
            "meta": json.loads(row[7]),
            "content": row[8],
        }
        f: File = File(row[2], fields)
        f.fid = row[0]
        return f

    def needs_update(self) -> bool:
        """Checks if the file needs to be scanned again."""
        s = os.stat(self.path)
        m = datetime.fromtimestamp(s.st_mtime)
        return m > self.time_scanned

# Local Variables: #
# python-indent: 4 #
# End: #
