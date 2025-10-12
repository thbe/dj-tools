#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:35:33 CET 2023

Release:      1.2.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against local mp3 pool
              v1.2.0 - Refactored for improved readability

Purpose:      Script to display the ID3 tags of a set of mp3
              files in a given directory
"""

import os
import sys
import glob
from mutagen.id3 import ID3


class ID3TagDisplayer:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.mp3_files = self._find_mp3_files()

    def _find_mp3_files(self):
        pattern = os.path.join(self.directory_path, "*.mp3")
        return sorted(glob.glob(pattern))

    def display_tags(self):
        for mp3_file in self.mp3_files:
            id3_attributes = ID3(mp3_file)
            print('-----------------------------------------')
            print(f'FILE={mp3_file}')
            print(id3_attributes.pprint())
            print('')
        print(f'Read tags from {len(self.mp3_files)} mp3 files')


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <directory_path>')
        sys.exit(1)
    displayer = ID3TagDisplayer(sys.argv[1])
    displayer.display_tags()


if __name__ == "__main__":
    main()
