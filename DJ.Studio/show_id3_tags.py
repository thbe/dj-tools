#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:35:33 CET 2023

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against local mp3 pool

Purpose:      Script to show the ID3 tags of mp3 files in a
              given directory
"""

import os
import sys
import glob
from mutagen.id3 import ID3

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <directory_path>')
    sys.exit(1)

directory_path = sys.argv[1]

mp3_filenames = []
for mp3_filename in glob.glob(os.path.join(directory_path, "*.mp3")):
    mp3_full_path_name = os.path.join(directory_path, mp3_filename)
    mp3_filenames.append(mp3_full_path_name)
    id3_filename = ID3(mp3_full_path_name)

    print('-----------------------------------------')
    print(f'FILE={mp3_filename}')
    print(id3_filename.pprint())
    print('')

print(f'Read tags from {len(mp3_filenames)} mp3 files')
