#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-22 18:27:13 krylon>
#
# /data/code/python/pythia/database.py
# created on 22. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.database

(c) 2024 Benjamin Walkenhorst
"""

import logging
import sqlite3
from enum import Enum, auto
from threading import Lock
from typing import Final, Optional

import krylib

from pythia import common

OPEN_LOCK: Final[Lock] = Lock()

INIT_QUERIES: Final[list[str]] = [
    """
CREATE TABLE IF NOT EXISTS folder (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    time_scanned INTEGER NOT NULL DEFAULT 0
) STRICT
    """,
    """
CREATE TABLE IF NOT EXISTS file (
    id INTEGER PRIMARY KEY,
    folder_id INTEGER NOT NULL,
    path TEXT UNIQUE NOT NULL,
    time_scanned INTEGER NOT NULL,
    mtime INTEGER NOT NULL,
    content_type TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    meta TEXT,
    content TEXT NOT NULL,
    FOREIGN KEY (folder_id) REFERENCES folder (id),
    CHECK (json_valid(meta))
) STRICT
    """,
    "CREATE UNIQUE INDEX IF NOT EXISTS file_path_idx ON file (path)",
    "CREATE INDEX IF NOT EXISTS file_scan_time_idx ON file (time_scanned)",
]


class Query(Enum):
    """Symbolic constants to identify database queries"""
    FolderAdd = auto()
    FolderUpdateScan = auto()
    FolderGetByPath = auto()
    FolderGetAll = auto()
    FileAdd = auto()
    FileGetByPath = auto()
    FileGetByID = auto()
    FileGetByFolder = auto()
    FileUpdate = auto()
    FileDelete = auto()


db_queries: Final[dict[Query, str]] = {
    Query.FolderAdd: "INSERT INTO folder (path) VALUES (?)",
    Query.FolderUpdateScan: "UPDATE folder SET time_scanned = ? WHERE id = ?",
    Query.FolderGetByPath:
    "SELECT id, time_scanned FROM folder WHERE path = ?",
    Query.FolderGetAll: """
SELECT
    id,
    path,
    time_scanned
FROM folder
ORDER BY path
    """,
    Query.FileAdd: """
INSERT INTO file
    (folder_id, path, time_scanned, mtime, content_type, mime_type, meta, content)
VALUES
    (        ?,    ?,            ?,     ?,            ?,         ?,    ?,       ?)
    """,
    Query.FileGetByPath: """
SELECT
    id,
    folder_id,
    time_scanned,
    mtime,
    content_type,
    mime_type,
    meta,
    content
FROM file
WHERE path = ?
    """,
    Query.FileGetByID: """
SELECT
    folder_id,
    path,
    time_scanned,
    mtime,
    content_type,
    mime_type,
    meta,
    content
FROM file
WHERE id = ?
    """,
    Query.FileGetByFolder: """
SELECT
    id,
    path,
    time_scanned,
    mtime,
    content_type,
    mime_type,
    meta,
    content
FROM file
WHERE folder_id = ?
ORDER BY path
    """,
    Query.FileUpdate: """
UPDATE file SET
    time_scanned = ?, mtime = ?, content_type = ?, mime_type = ?, meta = ?, content = ?
WHERE id = ?
    """,
    Query.FileDelete: "DELETE FROM file WHERE id = ?",
}


class Database:
    """Database provides a wrapper around the, uh, database connection
    and exposes the operations to be performed on it."""

    __slots__ = [
        "db",
        "log",
        "path",
    ]

    db: sqlite3.Connection
    log: logging.Logger
    path: str

    def __init__(self, path: Optional[str] = None) -> None:
        if path is None:
            self.path = common.path.db()
        else:
            self.path = path
        self.log = common.get_logger("database")
        self.log.debug("Open database at %s", path)
        with OPEN_LOCK:
            exist: Final[bool] = krylib.fexist(self.path)
            self.db = sqlite3.connect(self.path)
            self.db.isolation_level = None

            cur: Final[sqlite3.Cursor] = self.db.cursor()
            cur.execute("PRAGMA foreign_keys = true")
            cur.execute("PRAGMA journal_mode = WAL")

            if not exist:
                self.__create_db()

    def __create_db(self) -> None:
        """Initialize a freshly created database"""
        self.log.debug("Initialize fresh database at %s", self.path)
        with self.db:
            for query in INIT_QUERIES:
                cur: sqlite3.Cursor = self.db.cursor()
                cur.execute(query)
        self.log.debug("Database initialized successfully.")

    def __enter__(self) -> None:
        self.db.__enter__()

    def __exit__(self, ex_type, ex_val, traceback):
        return self.db.__exit__(ex_type, ex_val, traceback)

# Local Variables: #
# python-indent: 4 #
# End: #
