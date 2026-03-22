"""
Tests for Generic/Display_Id3_Tags.py

Author:       Thomas Bendler <code@thbe.org>
Purpose:      Unit tests for ID3TagDisplay class
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Generic.Display_Id3_Tags import ID3TagDisplay


class TestID3TagDisplayInit:
    """Tests for ID3TagDisplay initialization."""

    def test_init_with_valid_directory(self, tmp_mp3_dir: Path) -> None:
        """Test initialization with a valid directory."""
        displayer = ID3TagDisplay(tmp_mp3_dir)
        assert displayer.directory_path == tmp_mp3_dir
        assert displayer.mp3_files == []


class TestID3TagDisplayFindFiles:
    """Tests for MP3 file discovery."""

    def test_find_mp3_files_empty_directory(self, tmp_mp3_dir: Path) -> None:
        """Test finding MP3 files in an empty directory."""
        displayer = ID3TagDisplay(tmp_mp3_dir)
        assert displayer.mp3_files == []

    def test_find_mp3_files_with_files(self, tmp_mp3_dir: Path) -> None:
        """Test finding MP3 files in a directory with MP3 files."""
        (tmp_mp3_dir / "track1.mp3").touch()
        (tmp_mp3_dir / "track2.mp3").touch()

        displayer = ID3TagDisplay(tmp_mp3_dir)
        assert len(displayer.mp3_files) == 2

    def test_find_mp3_files_sorted(self, tmp_mp3_dir: Path) -> None:
        """Test that MP3 files are returned sorted."""
        (tmp_mp3_dir / "z_track.mp3").touch()
        (tmp_mp3_dir / "a_track.mp3").touch()

        displayer = ID3TagDisplay(tmp_mp3_dir)
        names = [f.name for f in displayer.mp3_files]
        assert names == ["a_track.mp3", "z_track.mp3"]


class TestID3TagDisplayTags:
    """Tests for the display_tags method."""

    def test_display_tags_empty_directory(self, tmp_mp3_dir: Path, capsys) -> None:
        """Test display_tags with no MP3 files."""
        displayer = ID3TagDisplay(tmp_mp3_dir)
        displayer.display_tags()

        captured = capsys.readouterr()
        assert "No mp3 files found" in captured.out

    @patch("Generic.Display_Id3_Tags.ID3")
    def test_display_tags_shows_file_info(
        self, mock_id3, tmp_mp3_dir: Path, capsys
    ) -> None:
        """Test that display_tags shows file information."""
        (tmp_mp3_dir / "track1.mp3").touch()

        mock_id3_instance = MagicMock()
        mock_id3.return_value = mock_id3_instance

        displayer = ID3TagDisplay(tmp_mp3_dir)
        displayer.display_tags()

        captured = capsys.readouterr()
        assert "track1.mp3" in captured.out
        assert "Read tags from 1 mp3 files" in captured.out
