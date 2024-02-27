#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:04:58 krylon>
#
# /home/krylon/code/python/pythia/extractor/audio.py
# created on 27. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.extractor.audio

(c) 2024 Benjamin Walkenhorst
"""

import os.path
import re
from typing import Final

import mutagen

from pythia.data import File
from pythia.extractor.base import Extractor

AUDIO_PAT: Final[re.Pattern] = \
    re.compile("[.](?:mp3|og[ga]|opus|m4b|aac|flac)", re.I)
DISC_NO_PAT: Final[re.Pattern] = re.compile("(\\d+)\\s*/\\s*(\\d+)")


class AudioExtractor(Extractor):  # pylint: disable-msg=R0903
    """Extracts metadata from audio files"""

    def process(self, f: File) -> bool:
        f.meta = read_tags(f.path)
        f.content = ""
        return True


def read_tags(path: str) -> dict[str, str]:  # pylint: disable-msg=R0912
    """Attempt to extract metadata from an audio file.

    path is expected to be the full, absolute path.
    """
    try:
        meta = mutagen.File(path)
    except mutagen.MutagenError:
        return {}

    tags: dict[str, str] = {
        "artist": "",
        "album": "",
        "title": "",
        "ord1": "0",
        "ord2": "0",
    }

    if "artist" in meta:
        tags["artist"] = meta["artist"][0]
    elif "TPE1" in meta:
        tags["artist"] = meta["TPE1"].text[0]

    if "album" in meta:
        tags["album"] = meta["album"][0]
    elif "TALB" in meta:
        tags["album"] = meta["TALB"].text[0]
    else:
        tags["album"] = os.path.basename(os.path.dirname(path))

    if "title" in meta:
        tags["title"] = meta["title"][0]
    elif "TIT2" in meta:
        tags["title"] = meta["TIT2"].text[0]

    if "tracknumber" in meta:
        tags["ord2"] = meta["tracknumber"][0]
    elif "TRCK" in meta:
        tags["ord2"] = meta["TRCK"].text[0]

    if "discnumber" in meta:
        tags["ord1"] = meta["discnumber"][0]
    elif "TPOS" in meta:
        tags["ord1"] = meta["TPOS"].text[0]

    m1 = DISC_NO_PAT.search(tags["ord1"])
    if m1 is not None:
        tags["ord1"] = m1[1]

    m2 = DISC_NO_PAT.search(tags["ord2"])
    if m2 is not None:
        tags["ord2"] = m2[1]

    return tags


# Local Variables: #
# python-indent: 4 #
# End: #
