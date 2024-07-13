#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:52:38 CET 2023

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against my local mp3 pool

Purpose:      Script to add missing ID3 tags after exporting from
              DJ.Studio to pre-listen the mix in Apple Music
"""

import os
import sys
import re
import glob
from datetime import datetime
from mutagen.id3 import ID3, GRP1, TALB, TDRC, TCMP, TCOM, TPE2, TRCK

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <directory_path>')
    sys.exit(1)

now = datetime.now()
date_full = now.strftime("%d/%m/%Y %H:%M:%S")
date_year = now.strftime("%Y")

ALBUM_DATE = date_year
ALBUM_TITLE = 'DJ.Studio Pre-Mix ' + date_full
COMPILATION = '1'
COMPILATION_GROUPING = 'DJ.Studio Pre-Mix ' + date_full
ALBUM_ARTIST = 'DJ.Studio'
COMPOSER = 'DJ.Studio'

directory_path = sys.argv[1]

mp3_files = []
for mp3_file in sorted(glob.glob(os.path.join(directory_path, "*.mp3"))):
    mp3_file_full_path = os.path.join(directory_path, mp3_file)
    mp3_files.append(mp3_file_full_path)

mp3_files_total_count = len(mp3_files)

i = 0
for mp3_file in mp3_files:
    i = i + 1
    id3_attributes = ID3(mp3_file)
    id3_attributes_track_number = str(i) + '/' + str(mp3_files_total_count)

    id3_attributes.add(TRCK(encoding=3, text=id3_attributes_track_number))
    id3_attributes.add(TDRC(encoding=3, text=ALBUM_DATE))
    id3_attributes.add(TALB(encoding=3, text=ALBUM_TITLE))
    id3_attributes.add(TCMP(encoding=3, text=COMPILATION))
    id3_attributes.add(GRP1(encoding=3, text=COMPILATION_GROUPING))
    id3_attributes.add(TCOM(encoding=3, text=COMPOSER))
    id3_attributes.add(TPE2(encoding=3, text=ALBUM_ARTIST))
    id3_attributes.save(mp3_file)

    print('-----------------------------------------')
    print(f'FILE={mp3_file}')
    print(id3_attributes.pprint())
    print('')
