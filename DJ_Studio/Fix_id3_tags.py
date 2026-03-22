#! /usr/bin/env python3

"""
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec 27 19:52:38 CET 2023

Release:      1.3.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against my local mp3 pool
              v1.2.0 - Refactored for improved readability
              v1.3.0 - Migrated to pathlib, added type hints and error handling

Purpose:      Script to add missing ID3 tags after exporting from
              DJ.Studio to pre-listen the mix in Apple Music
"""

import sys
from datetime import datetime
from pathlib import Path

try:
    from mutagen.id3 import ID3, GRP1, TALB, TDRC, TCMP, TCOM, TPE2, TRCK
except ImportError:
    print("Error: The 'mutagen' library is not installed.")
    print("Please install it with 'pip install mutagen'.")
    sys.exit(1)


class ID3TagFixer:
    """Fix and add missing ID3 tags for DJ.Studio exported MP3 files."""

    ALBUM_ARTIST = "DJ.Studio"
    COMPOSER = "DJ.Studio"
    COMPILATION = "1"

    def __init__(self, directory_path: Path) -> None:
        """Initialize the ID3TagFixer with a directory path.

        Args:
            directory_path: Path to the directory containing MP3 files.

        Raises:
            FileNotFoundError: If the directory does not exist.
            ValueError: If the path is not a directory.
        """
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")

        self.directory_path = directory_path
        self.now = datetime.now()
        self.date_full = self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.date_year = self.now.strftime("%Y")
        self.album_date = self.date_year
        self.album_title = f"DJ.Studio Pre-Mix {self.date_full}"
        self.compilation_grouping = f"DJ.Studio Pre-Mix {self.date_full}"
        self.mp3_files = self._find_mp3_files()

    def _find_mp3_files(self) -> list[Path]:
        """Find all MP3 files in the directory.

        Returns:
            Sorted list of Path objects for MP3 files.
        """
        return sorted(self.directory_path.glob("*.mp3"))

    def fix_tags(self) -> int:
        """Fix ID3 tags for all MP3 files in the directory.

        Returns:
            Number of files successfully processed.
        """
        if not self.mp3_files:
            print(f"No MP3 files found in: {self.directory_path}")
            return 0

        mp3_files_total_count = len(self.mp3_files)
        success_count = 0

        for i, mp3_file in enumerate(self.mp3_files, start=1):
            try:
                id3_attributes = ID3(mp3_file)
                track_number = f"{i}/{mp3_files_total_count}"

                id3_attributes.add(TRCK(encoding=3, text=track_number))
                id3_attributes.add(TDRC(encoding=3, text=self.album_date))
                id3_attributes.add(TALB(encoding=3, text=self.album_title))
                id3_attributes.add(TCMP(encoding=3, text=self.COMPILATION))
                id3_attributes.add(GRP1(encoding=3, text=self.compilation_grouping))
                id3_attributes.add(TCOM(encoding=3, text=self.COMPOSER))
                id3_attributes.add(TPE2(encoding=3, text=self.ALBUM_ARTIST))
                id3_attributes.save(mp3_file)

                print("-----------------------------------------")
                print(f"FILE={mp3_file}")
                print(id3_attributes.pprint())
                print("")
                success_count += 1

            except Exception as e:
                print("-----------------------------------------")
                print(f"FILE={mp3_file}")
                print(f"Error processing file: {e}")
                print("")

        print(f"Processed {success_count}/{mp3_files_total_count} files successfully.")
        return success_count


def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory_path>")
        sys.exit(1)

    directory_path = Path(sys.argv[1])

    try:
        fixer = ID3TagFixer(directory_path)
        fixer.fix_tags()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
