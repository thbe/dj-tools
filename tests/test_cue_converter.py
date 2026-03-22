"""
Tests for Rekordbox/CUE_Converter.py

Author:       Thomas Bendler <code@thbe.org>
Purpose:      Unit tests for CueConverter class
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Rekordbox.CUE_Converter import CueConverter


class TestCueConverterInit:
    """Tests for CueConverter initialization."""

    def test_init_with_valid_file(self, tmp_cue_file: Path) -> None:
        """Test initialization with a valid CUE file."""
        converter = CueConverter(tmp_cue_file)
        assert converter.cue_file_path == tmp_cue_file
        assert len(converter.file_content) > 0


class TestCueConverterParse:
    """Tests for CUE file parsing."""

    def test_parse_extracts_tracks(self, tmp_cue_file: Path) -> None:
        """Test that parse extracts all tracks."""
        converter = CueConverter(tmp_cue_file)
        tracklist = converter.parse()

        assert len(tracklist) == 3

    def test_parse_extracts_correct_times(self, tmp_cue_file: Path) -> None:
        """Test that parse extracts correct timestamps."""
        converter = CueConverter(tmp_cue_file)
        tracklist = converter.parse()

        times = [track[0] for track in tracklist]
        assert times == ["00:00:00", "03:45:00", "07:30:00"]

    def test_parse_extracts_track_numbers(self, tmp_cue_file: Path) -> None:
        """Test that parse extracts correct track numbers."""
        converter = CueConverter(tmp_cue_file)
        tracklist = converter.parse()

        track_numbers = [track[1] for track in tracklist]
        assert track_numbers == ["01", "02", "03"]

    def test_parse_extracts_artists(self, tmp_cue_file: Path) -> None:
        """Test that parse extracts correct artists."""
        converter = CueConverter(tmp_cue_file)
        tracklist = converter.parse()

        artists = [track[2] for track in tracklist]
        assert artists == ["Artist One", "Artist Two", "Artist Three"]

    def test_parse_extracts_titles(self, tmp_cue_file: Path) -> None:
        """Test that parse extracts correct titles."""
        converter = CueConverter(tmp_cue_file)
        tracklist = converter.parse()

        titles = [track[3] for track in tracklist]
        assert titles == ["First Track", "Second Track", "Third Track"]

    def test_parse_uses_global_artist_as_fallback(self, tmp_path: Path) -> None:
        """Test that global artist is used when track artist is missing."""
        cue_content = """PERFORMER "Global Artist"
TITLE "Album"
FILE "audio.wav" WAVE
  TRACK 01 AUDIO
    TITLE "Song Without Artist"
    INDEX 01 00:00:00
"""
        cue_file = tmp_path / "test.cue"
        cue_file.write_text(cue_content, encoding="utf-8")

        converter = CueConverter(cue_file)
        tracklist = converter.parse()

        assert len(tracklist) == 1
        assert tracklist[0][2] == "Global Artist"

    def test_parse_empty_file(self, tmp_path: Path) -> None:
        """Test parsing an empty CUE file."""
        cue_file = tmp_path / "empty.cue"
        cue_file.write_text("", encoding="utf-8")

        converter = CueConverter(cue_file)
        tracklist = converter.parse()

        assert tracklist == []


class TestCueConverterPrintTracklist:
    """Tests for tracklist printing."""

    def test_print_tracklist_output(self, tmp_cue_file: Path, capsys) -> None:
        """Test that print_tracklist produces correct output."""
        converter = CueConverter(tmp_cue_file)
        converter.print_tracklist()

        captured = capsys.readouterr()
        assert "Tracklist for" in captured.out
        assert "00:00:00" in captured.out
        assert "Artist One" in captured.out
        assert "First Track" in captured.out

    def test_print_tracklist_empty_file(self, tmp_path: Path, capsys) -> None:
        """Test print_tracklist with empty CUE file."""
        cue_file = tmp_path / "empty.cue"
        cue_file.write_text("", encoding="utf-8")

        converter = CueConverter(cue_file)
        converter.print_tracklist()

        captured = capsys.readouterr()
        assert "No tracklist found" in captured.out


class TestCueConverterPatterns:
    """Tests for regex patterns."""

    def test_time_pattern_matches(self) -> None:
        """Test TIME_PATTERN matches valid index lines."""
        pattern = CueConverter.TIME_PATTERN

        assert pattern.match("    INDEX 01 00:00:00")
        assert pattern.match("  INDEX 02 12:34:56")
        assert not pattern.match('TITLE "Something"')

    def test_track_pattern_matches(self) -> None:
        """Test TRACK_PATTERN matches valid track lines."""
        pattern = CueConverter.TRACK_PATTERN

        assert pattern.match("  TRACK 01 AUDIO")
        assert pattern.match("    TRACK 99 AUDIO")
        assert not pattern.match('TITLE "Something"')

    def test_artist_pattern_matches(self) -> None:
        """Test ARTIST_PATTERN matches valid performer lines."""
        pattern = CueConverter.ARTIST_PATTERN

        match = pattern.match('  PERFORMER "Artist Name"')
        assert match
        assert match.group(1) == "Artist Name"

    def test_title_pattern_matches(self) -> None:
        """Test TITLE_PATTERN matches valid title lines."""
        pattern = CueConverter.TITLE_PATTERN

        match = pattern.match('  TITLE "Song Title"')
        assert match
        assert match.group(1) == "Song Title"
