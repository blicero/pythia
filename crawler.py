#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-24 18:40:00 krylon>
#
# /data/code/python/pythia/crawler.py
# created on 22. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.crawler

(c) 2024 Benjamin Walkenhorst
"""

import logging
import os
from datetime import datetime
from queue import SimpleQueue
from threading import Lock, Thread

from pythia import common, database
from pythia.data import Blacklist, File, Folder


class Crawler:
    """Crawler traverses directory trees and inspects files."""

    __slots__ = [
        "log",
        "db",
        "blacklist",
        "folders",
        "fileq",
        "lock",
        "active",
        "workers",
    ]

    log: logging.Logger
    db: database.Database
    blacklist: Blacklist
    folders: list[str]
    fileq: SimpleQueue
    lock: Lock
    active: bool
    workers: list[Thread]

    def __init__(self, *folders: str) -> None:
        self.log = common.get_logger("crawler")
        self.db = database.Database()
        self.folders = list(folders)
        self.fileq = SimpleQueue()
        self.lock = Lock()
        self.active = False
        self.workers = []

    def is_active(self) -> bool:
        """Returns the Crawler's active flag."""
        with self.lock:
            return self.active

    def stop(self) -> None:
        """Tell the Crawler to stop."""
        with self.lock:
            self.active = False

    def traverse(self) -> None:
        """Start walking the directory tree(s)."""
        with self.lock:
            self.active = True
            for tree in self.folders:
                worker: Thread = Thread(target=self.__worker, args=(tree, ))
                worker.start()
                self.workers.append(worker)

    def __worker(self, tree: str) -> None:
        self.log.debug("Process folder %s", tree)
        db = database.Database()
        fldr = db.folder_get_by_path(tree)
        if fldr is None:
            fldr = Folder(path=tree)
            with db:
                db.folder_add(fldr)

        for folder, subfolders, files in os.walk(tree):
            self.log.debug("Process folder %s", folder)
            subfolders[:] = [x for x in subfolders if not self.blacklist.match(x)]
            for f in files:
                if self.blacklist.match(f):
                    continue
                full_path = os.path.join(folder, f)
                fob = db.file_get_by_path(full_path)
                if fob is None:
                    fob = File(
                        full_path,
                        {
                            "folder_id": fldr.fid,
                            "time_scanned": datetime.now(),
                        }
                    )
                    with db:
                        db.file_add(f)


# Local Variables: #
# python-indent: 4 #
# End: #
