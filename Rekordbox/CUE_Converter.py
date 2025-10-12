#! /usr/bin/env python3

"""
Author:       Thomas Bendler <code@thbe.org>
Date:         Tue Jan  2 00:04:41 CET 2024

Release:      1.3.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against sample cue file
              v1.2.0 - Refactored code for clarity and maintainability
              v1.3.0 - Optimized with pathlib and simplified regex

Purpose:      Script to convert CUE export into human readable
              text track list (e.g., for YouTube description)
"""

import re
import sys
from pathlib import Path


class CueConverter:
    TIME_PATTERN = re.compile(r'^\s*INDEX \d\d (\d{2}:\d{2}:\d{2})')
    TRACK_PATTERN = re.compile(r'^\s*TRACK (\d\d) AUDIO')
    ARTIST_PATTERN = re.compile(r'^\s*PERFORMER "(.*)"')
    TITLE_PATTERN = re.compile(r'^\s*TITLE "(.*)"')

    def __init__(self, cue_file_path: Path):
        self.cue_file_path = cue_file_path
        self.file_content = self._read_file()

    def _read_file(self) -> str:
        return self.cue_file_path.read_text(encoding="utf-8")

    def parse(self) -> list[tuple[str, str, str, str]]:
        lines = self.file_content.splitlines()
        tracklist = []

        global_artist = None
        global_title = None

        current_track_number = None
        current_artist = None
        current_title = None

        for line in lines:
            artist_match = self.ARTIST_PATTERN.match(line)
            if artist_match:
                artist = artist_match.group(1).strip()
                if current_track_number is None:
                    global_artist = artist
                else:
                    current_artist = artist
                continue

            title_match = self.TITLE_PATTERN.match(line)
            if title_match:
                title = title_match.group(1).strip()
                if current_track_number is None:
                    global_title = title
                else:
                    current_title = title
                continue

            track_match = self.TRACK_PATTERN.match(line)
            if track_match:
                current_track_number = track_match.group(1)

                current_artist = None
                current_title = None
                continue

            time_match = self.TIME_PATTERN.match(line)
            if time_match and current_track_number is not None:
                current_time = time_match.group(1)

                artist_to_use = current_artist if current_artist else global_artist
                title_to_use = current_title if current_title else "Untitled"

                tracklist.append((
                    current_time,
                    current_track_number,
                    artist_to_use,
                    title_to_use
                ))
                current_track_number = None
                current_artist = None
                current_title = None

        return tracklist

    def print_tracklist(self):
        tracklist = self.parse()
        if not tracklist:
            print(f"No tracklist found in {self.cue_file_path.name}.")
            return

        print(f"--- Tracklist for {self.cue_file_path.name} ---")

        for time, track, artist, title in tracklist:
            artist_display = f"{artist} - " if artist else ""
            print(f"{time} - {artist_display}{title}")

        print("-----------------------------------------")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <cue_file_path>")
        sys.exit(1)

    cue_file_path = Path(sys.argv[1])

    if not cue_file_path.is_file():
        print(f"Error: File '{cue_file_path}' not found.")
        sys.exit(1)

    try:
        converter = CueConverter(cue_file_path)
        converter.print_tracklist()

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error reading file encoding: {e}")
        print("Please ensure the file is correctly encoded (e.g., UTF-8).")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
