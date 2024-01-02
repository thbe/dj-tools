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
    print(f"Usage: {sys.argv[0]} <directory_path>")
    sys.exit(1)

with open(sys.argv[1], "r", encoding="utf-8") as f:
    file_content = f.read()

artist_pattern = re.compile(r"\t\tPERFORMER \"\w+\.?\w*\"")
title_pattern = re.compile(r"\t\tTITLE \"\w+\.?\w*\"")
index_pattern = re.compile(r"\t\tINDEX \d+ (\d+) (.*)")

artists = artist_pattern.findall(file_content)
titles = title_pattern.findall(file_content)
indices = index_pattern.findall(file_content)

tracklist = ""
for i, (title, artist, time) in enumerate(zip(titles, artists, indices)):
    tracklist += f"{time:02d} : {artist} - {title}\n"

print(tracklist)
