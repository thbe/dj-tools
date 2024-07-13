#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:35:33 CET 2023

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against local mp3 pool

Purpose:      Script to display the ID3 tags of a set of mp3
              files in a given directory
"""

import os
import sys
import glob
from mutagen.id3 import ID3

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <directory_path>')
    sys.exit(1)

directory_path = sys.argv[1]

mp3_files = []
for mp3_file in sorted(glob.glob(os.path.join(directory_path, "*.mp3"))):
    mp3_file_full_path = os.path.join(directory_path, mp3_file)
    mp3_files.append(mp3_file_full_path)
    id3_attributes = ID3(mp3_file)

    print('-----------------------------------------')
    print(f'FILE={mp3_file}')
    print(id3_attributes.pprint())
    print('')

print(f'Read tags from {len(mp3_files)} mp3 files')
