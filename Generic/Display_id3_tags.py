#! /usr/bin/env python3

"""
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:35:33 CET 2023

Release:      1.3.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against local mp3 pool
              v1.2.0 - Refactored for improved readability
              v1.3.0 - Optimized with pathlib and improved error handling

Purpose:      Script to display the ID3 tags of a set of mp3
              files in a given directory
"""

import sys
from pathlib import Path

try:
    from mutagen.id3 import ID3
    from mutagen.id3 import ID3NoHeaderError
except ImportError:
    print("Error: The 'mutagen' library is not installed. Please install it with 'pip install mutagen'.")
    sys.exit(1)


class ID3TagDisplay:
    def __init__(self, directory_path: Path):
        self.directory_path = directory_path
        self.mp3_files = self._find_mp3_files()

    def _find_mp3_files(self) -> list[Path]:
        pattern = "*.mp3"
        return sorted(self.directory_path.glob(pattern))

    def display_tags(self):
        if not self.mp3_files:
            print(
                f"No mp3 files found in the specified directory: {self.directory_path}")
            return

        failed_count = 0

        for mp3_file in self.mp3_files:
            try:
                id3_attributes = ID3(mp3_file)

                print('-----------------------------------------')
                print(f'FILE={mp3_file}')

                if id3_attributes:
                    print(id3_attributes)
                else:
                    print('No ID3 tags found.')

            except ID3NoHeaderError as e:
                failed_count += 1
                print('-----------------------------------------')
                print(f'FILE={mp3_file}')
                print(f'Error reading ID3 tags (No Header): {e}')

            except Exception as e:
                failed_count += 1
                print('-----------------------------------------')
                print(f'FILE={mp3_file}')
                print(f'Unexpected error reading ID3 tags: {e}')

        print(
            f'Read tags from {len(self.mp3_files)} mp3 files, {failed_count} failed.')


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <directory_path>')
        sys.exit(1)

    directory_path = Path(sys.argv[1])

    if not directory_path.is_dir():
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    try:
        displayer = ID3TagDisplay(directory_path)
        displayer.display_tags()

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
