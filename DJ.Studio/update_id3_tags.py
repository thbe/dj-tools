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

from datetime import datetime
import glob
from mutagen.id3 import ID3, TRCK, GRP1, TALB, TDRC, TCMP
import os
import re
import sys

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

directory_path = sys.argv[1]

mp3_files = []
for mp3_file in glob.glob(os.path.join(directory_path, "*.mp3")):
    mp3_full_path_name = os.path.join(directory_path, mp3_file)
    mp3_files.append(mp3_full_path_name)

mp3_files_count = len(mp3_files)

for mp3_file in mp3_files:
    id3_file = ID3(mp3_file)
    mp3_filename = os.path.basename(mp3_file)

    track_number_raw = re.findall(r"\d{3}", mp3_filename)[0]
    track_number = re.sub(r"^0+", "", track_number_raw)

    id3_file.add(TRCK(encoding=3, text=u''+track_number+''))
    id3_file.add(TDRC(encoding=3, text=u''+ALBUM_DATE+''))
    id3_file.add(TALB(encoding=3, text=u''+ALBUM_TITLE+''))
    id3_file.add(TCMP(encoding=3, text=u''+COMPILATION+''))
    id3_file.add(GRP1(encoding=3, text=u''+COMPILATION_GROUPING+''))
    id3_file.save(mp3_file)

    print('-----------------------------------------')
    print(f'FILE={mp3_file}')
    print(id3_file.pprint())
    print('')
