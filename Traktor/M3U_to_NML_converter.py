#! /usr/bin/env python3

"""
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec  4 23:38:47 CET 2024

Release:      1.1.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against sample M3U file
              v1.1.0 - Migrated to pathlib, added type hints and error handling

Purpose:      Script to convert M3U playlists into Native Instruments
              NML playlists for Traktor Pro
"""

import sys
from pathlib import Path


class M3UToNMLConverter:
    """Convert M3U playlists to Native Instruments NML format for Traktor Pro."""

    def __init__(self, m3u_path: Path, nml_path: Path) -> None:
        """Initialize the converter with input and output paths.

        Args:
            m3u_path: Path to the source M3U file.
            nml_path: Path for the output NML file.

        Raises:
            FileNotFoundError: If the M3U file does not exist.
            ValueError: If the M3U path is not a file.
        """
        if not m3u_path.exists():
            raise FileNotFoundError(f"M3U file not found: {m3u_path}")
        if not m3u_path.is_file():
            raise ValueError(f"Path is not a file: {m3u_path}")

        self.m3u_path = m3u_path
        self.nml_path = nml_path

    def read_m3u(self) -> list[str]:
        """Read and parse the M3U file.

        Returns:
            List of audio file paths from the M3U file.
        """
        content = self.m3u_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        # Filter out empty lines and M3U metadata lines (starting with #)
        return [
            line.strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]

    def generate_nml_content(self, audio_files: list[str]) -> str:
        """Generate NML content from audio file list.

        Args:
            audio_files: List of audio file paths.

        Returns:
            NML formatted XML string.
        """
        clips = "\n".join(
            f"                    <clip>\n                        <file>{audio_file}</file>\n                    </clip>"
            for audio_file in audio_files
        )

        nml_content = f"""<nml>
    <tracks>
        <track>
            <name>Track 1</name>
            <clips>
{clips}
            </clips>
        </track>
    </tracks>
</nml>
"""
        return nml_content

    def convert(self) -> int:
        """Convert M3U to NML and write to output file.

        Returns:
            Number of audio files included in the NML.
        """
        audio_files = self.read_m3u()

        if not audio_files:
            print(f"No audio files found in: {self.m3u_path}")
            return 0

        nml_content = self.generate_nml_content(audio_files)
        self.nml_path.write_text(nml_content, encoding="utf-8")

        print(f"Converted {len(audio_files)} entries from {self.m3u_path.name}")
        print(f"Output written to: {self.nml_path}")
        return len(audio_files)


def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} </path/file.m3u> </path/file.nml>")
        sys.exit(1)

    m3u_path = Path(sys.argv[1])
    nml_path = Path(sys.argv[2])

    try:
        converter = M3UToNMLConverter(m3u_path, nml_path)
        converter.convert()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error reading file encoding: {e}")
        print("Please ensure the M3U file is correctly encoded (e.g., UTF-8).")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
