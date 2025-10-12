#! /usr/bin/env python3

"""_summary_
Author:       Thomas Bendler <code@thbe.org>
Date:         Wed Dec  4 23:38:47 CET 2024

Release:      1.0.0

ChangeLog:    v0.1.0 - Initial release
              v1.0.0 - Validated against sample M3U file

Purpose:      Script to convert M3U playlists into Native Instruments
              NML playlists for Traktor Pro
"""

import sys


class M3UToNMLConverter:
    def __init__(self, m3u_path, nml_path):
        self.m3u_path = m3u_path
        self.nml_path = nml_path

    def read_m3u(self):
        with open(self.m3u_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]

    def generate_nml_content(self, audio_files):
        nml_content = """
    <nml>
        <tracks>
            <track>
                <name>Track 1</name>
                <clips>
    """
        for audio_file in audio_files:
            nml_content += f"""
                    <clip>
                        <file>{audio_file}</file>
                    </clip>
    """
        nml_content += """
                </clips>
            </track>
        </tracks>
    </nml>
    """
        return nml_content

    def convert(self):
        audio_files = self.read_m3u()
        nml_content = self.generate_nml_content(audio_files)
        with open(self.nml_path, "w", encoding="utf-8") as f:
            f.write(nml_content)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} </path/file.m3u> </path/file.nml>")
        sys.exit(1)
    converter = M3UToNMLConverter(sys.argv[1], sys.argv[2])
    converter.convert()


if __name__ == "__main__":
    main()
