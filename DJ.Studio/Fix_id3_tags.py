#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:52:38 CET 2023

Release:      1.2.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against my local mp3 pool
              v1.2.0 - Refactored for improved readability

Purpose:      Script to add missing ID3 tags after exporting from
              DJ.Studio to pre-listen the mix in Apple Music
"""

import os
import sys
import glob
from datetime import datetime
from mutagen.id3 import ID3, GRP1, TALB, TDRC, TCMP, TCOM, TPE2, TRCK


class ID3TagFixer:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.now = datetime.now()
        self.date_full = self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.date_year = self.now.strftime("%Y")
        self.ALBUM_DATE = self.date_year
        self.ALBUM_TITLE = 'DJ.Studio Pre-Mix ' + self.date_full
        self.COMPILATION = '1'
        self.COMPILATION_GROUPING = 'DJ.Studio Pre-Mix ' + self.date_full
        self.ALBUM_ARTIST = 'DJ.Studio'
        self.COMPOSER = 'DJ.Studio'
        self.mp3_files = self._find_mp3_files()

    def _find_mp3_files(self):
        pattern = os.path.join(self.directory_path, "*.mp3")
        return sorted(glob.glob(pattern))

    def fix_tags(self):
        mp3_files_total_count = len(self.mp3_files)
        for i, mp3_file in enumerate(self.mp3_files, start=1):
            id3_attributes = ID3(mp3_file)
            id3_attributes_track_number = f"{i}/{mp3_files_total_count}"

            id3_attributes.add(
                TRCK(encoding=3, text=id3_attributes_track_number))
            id3_attributes.add(TDRC(encoding=3, text=self.ALBUM_DATE))
            id3_attributes.add(TALB(encoding=3, text=self.ALBUM_TITLE))
            id3_attributes.add(TCMP(encoding=3, text=self.COMPILATION))
            id3_attributes.add(
                GRP1(encoding=3, text=self.COMPILATION_GROUPING))
            id3_attributes.add(TCOM(encoding=3, text=self.COMPOSER))
            id3_attributes.add(TPE2(encoding=3, text=self.ALBUM_ARTIST))
            id3_attributes.save(mp3_file)

            print('-----------------------------------------')
            print(f'FILE={mp3_file}')
            print(id3_attributes.pprint())
            print('')


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <directory_path>')
        sys.exit(1)
    fixer = ID3TagFixer(sys.argv[1])
    fixer.fix_tags()


if __name__ == "__main__":
    main()
