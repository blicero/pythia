#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-02-27 15:05:06 krylon>
#
# /data/code/python/pythia/extractor/pdf.py
# created on 26. 02. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/agpl-3.0

"""
pythia.extractor.pdf

(c) 2024 Benjamin Walkenhorst
"""

from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pythia.data import File
from pythia.extractor.base import Extractor


class PDFExtractor(Extractor):  # pylint: disable-msg=R0903
    """Exctractor for PDF files"""

    def process(self, f: File) -> bool:
        """Attempt to extract metadata from a PDF document."""
        with open(f.path, "rb") as fh:
            parser = PDFParser(fh)
            doc = PDFDocument(parser)
            metadata = {}
            for key, val in doc.info[0].items():
                metadata[key] = val.decode()

            outlines = []
            for i in doc.get_outlines():
                outlines.append(i[1])

            if len(outlines) > 0:
                metadata["chapters"] = outlines

            f.meta = metadata
        f.content = extract_text(f.path)
        return True

# Local Variables: #
# python-indent: 4 #
# End: #
