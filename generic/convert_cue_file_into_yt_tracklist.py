#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Tue Jan  2 00:04:41 CET 2024

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against sample cue file

Purpose:      Script to convert cue files into YT track lists
"""


import re
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <directory_path>')
    sys.exit(1)

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    file_content = f.read()

artist_pattern = re.compile(r'[\t\t| +]PERFORMER "(.*)"')
title_pattern = re.compile(r'[\t\t| +]TITLE "(.*)"')
index_pattern = re.compile(r'[\t\t| +]INDEX \d\d (.*)')

artists = re.findall(artist_pattern, file_content)
titles = re.findall(title_pattern, file_content)
indices = re.findall(index_pattern, file_content)

tracklist = ''
for i in range(len(titles)):
    title = titles[i]
    artist = artists[i]
    time = indices[i]

    tracklist += f'{time} : {artist} - {title}\n'

print(tracklist)
