#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-24 15:24:39 krylon>
#
# /data/code/python/pythia/test_database.py
# created on 23. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.test_database

(c) 2024 Benjamin Walkenhorst
"""

import os
import sqlite3
import unittest
from datetime import datetime
from typing import Final

from krylib import isdir

from pythia import common, database
from pythia.data import File, FileType, Folder

TEST_ROOT: str = "/tmp/"

# On my main development machines, I have a RAM disk mounted at /data/ram.
# If it's available, I'd rather use that than /tmp which might live on disk.
if isdir("/data/ram"):
    TEST_ROOT = "/data/ram"


class DatabaseTest(unittest.TestCase):
    """Test the damn database."""

    folder: str
    db: database.Database

    @classmethod
    def setUpClass(cls) -> None:
        stamp = datetime.now()
        folder_name = \
            stamp.strftime("pythia_test_database_%Y%m%d_%H%M%S")
        cls.folder = os.path.join(TEST_ROOT,
                                  folder_name)
        common.set_basedir(cls.folder)

    @classmethod
    def tearDownClass(cls) -> None:
        os.system(f"/bin/rm -rf {cls.folder}")

    def __get_db(self) -> database.Database:  # pylint: disable-msg=W0238
        """Get the shared database instance."""
        return self.__class__.db

    def test_01_db_open(self) -> None:
        """Try to create a fresh database, is all."""
        try:
            self.__class__.db = database.Database(common.path.db())
        except Exception as e:  # pylint: disable-msg=W0718
            self.fail(f"Failed to open database: {e}")
        finally:
            self.assertIsNotNone(self.__class__.db)

    def test_02_db_folder_add(self) -> None:
        """Try adding some folders."""
        f: Final[Folder] = Folder(path="/home/capybara/Documents")  # pylint: disable-msg=E1125
        db = self.__get_db()
        with db:
            db.folder_add(f)
            self.assertNotEqual(f.fid, 0)

        f2: Final[Folder] = Folder(path="/home/capybara/Documents")
        with db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.folder_add(f2)

    def test_03_db_folder_get_all(self) -> None:
        """Try to load all folders from the database."""
        db = self.__get_db()
        folders = db.folder_get_all()
        self.assertEqual(len(folders), 1)
        self.assertEqual(folders[0].path, "/home/capybara/Documents")

    def test_04_db_folder_get_by_path(self) -> None:
        """Try to get a folder by its path. Also, try to get a folder we know
        does not exist."""
        db = self.__get_db()
        f = db.folder_get_by_path("/home/capybara/Documents")
        self.assertIsNotNone(f)
        self.assertIsInstance(f, Folder)

        f = db.folder_get_by_path("/spam")
        self.assertIsNone(f)

    def test_05_file_add(self):
        """Try adding a file to the database."""
        db = self.__get_db()
        f = File("/home/capybara/Documents/sunset.jpg",
                 {"folder_id": 1,
                  "time_scanned": datetime(2024, 2, 24, 15, 2, 22),
                  "mtime": datetime(2024, 2, 7, 18, 21, 14),
                  "content_type": FileType.Image,
                  "meta": {},
                  "content": "",
                  })
        with db:
            db.file_add(f)
            self.assertNotEqual(f.fid, 0)

        f2 = File("/home/krylon/code/python/pythia/database.py",
                  {"folder_id": 42,
                   "time_scanned": datetime(2024, 2, 24, 15, 2, 22),
                   "mtime": datetime(2024, 2, 7, 18, 21, 14),
                   "content_type": FileType.Image,
                   "meta": {},
                   "content": "",
                   })
        with db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.file_add(f2)

# Local Variables: #
# python-indent: 4 #
# End: #
