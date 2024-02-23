#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-23 13:31:15 krylon>
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
from queue import SimpleQueue
from threading import Lock, Thread

from pythia import common, database


class Crawler:
    """Crawler traverses directory trees and inspects files."""

    __slots__ = [
        "log",
        "db",
        "folders",
        "fileq",
        "lock",
        "active",
        "workers",
    ]

    log: logging.Logger
    db: database.Database
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
        # db = database.Database()
        # for folder, subfolders, files in os.walk(tree):
        #     pass

# Local Variables: #
# python-indent: 4 #
# End: #
