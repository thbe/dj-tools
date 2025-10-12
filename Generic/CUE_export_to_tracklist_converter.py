#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Tue Jan  2 00:04:41 CET 2024

Release:      1.2.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against sample cue file
              v1.2.0 - Refactored code for clarity and maintainability

Purpose:      Script to convert CUE export into human readable
              text track list (e.g., for YouTube description)
"""

import re
import sys


class CueConverter:
    def __init__(self, cue_file_path):
        self.cue_file_path = cue_file_path
        self.file_content = self._read_file()
        self.time_pattern = re.compile(r'[\t| +]INDEX \d\d (.*)')
        self.track_pattern = re.compile(r'[\t| +]TRACK (\d\d) AUDIO')
        self.artist_pattern = re.compile(r'[\t| +]PERFORMER "(.*)"')
        self.title_pattern = re.compile(r'[\t| +]TITLE "(.*)"')

    def _read_file(self):
        with open(self.cue_file_path, "r", encoding="utf-8") as f:
            return f.read()

    def parse(self):
        times = self.time_pattern.findall(self.file_content)
        tracks = self.track_pattern.findall(self.file_content)
        artists = self.artist_pattern.findall(self.file_content)
        titles = self.title_pattern.findall(self.file_content)
        return list(zip(times, tracks, artists, titles))

    def print_tracklist(self):
        for time, track, artist, title in self.parse():
            print(f"{time} {track} {artist} - {title}")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <cue_file_path>")
        sys.exit(1)
    converter = CueConverter(sys.argv[1])
    converter.print_tracklist()


if __name__ == "__main__":
    main()
