#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Tue Jan  2 00:04:41 CET 2024

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against sample cue file

Purpose:      Script to convert CUE export into human readable
              text track list (e.g., for YouTube description)
"""


import re
import sys
import datetime


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <directory_path>")
    sys.exit(1)

with open(sys.argv[1], "r", encoding="utf-8") as f:
    file_content = f.read()

artist_pattern = re.compile(r'[\t\t| +]PERFORMER "(.*)"')
title_pattern = re.compile(r'[\t\t| +]TITLE "(.*)"')
index_pattern = re.compile(r'[\t\t| +]INDEX \d\d (.*)')

artists = artist_pattern.findall(file_content)
titles = title_pattern.findall(file_content)
indices = index_pattern.findall(file_content)

for i, dataset in enumerate(zip(indices, artists, titles)):
    split_minutes, split_seconds, split_frames = dataset[0].split(':')
    total_seconds = int(split_minutes) * 60 + \
        int(split_seconds) + int(split_frames) / 75
    timedelta_object = datetime.timedelta(seconds=total_seconds)
    delta_hours = timedelta_object.seconds // 3600
    delta_minutes = (timedelta_object.seconds % 3600) // 60
    delta_seconds = timedelta_object.seconds % 60
    formatted_time = f"{delta_hours:02d}:{delta_minutes:02d}:{delta_seconds:02d}"
    trackinfo = formatted_time + ' : ' + dataset[1] + ' - ' + dataset[2]
    print(trackinfo)
