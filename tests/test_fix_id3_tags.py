"""
Tests for DJ_Studio/Fix_id3_tags.py

Author:       Thomas Bendler <code@thbe.org>
Purpose:      Unit tests for ID3TagFixer class
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from DJ_Studio.Fix_id3_tags import ID3TagFixer


class TestID3TagFixerInit:
    """Tests for ID3TagFixer initialization."""

    def test_init_with_valid_directory(self, tmp_mp3_dir: Path) -> None:
        """Test initialization with a valid directory."""
        fixer = ID3TagFixer(tmp_mp3_dir)
        assert fixer.directory_path == tmp_mp3_dir
        assert fixer.mp3_files == []

    def test_init_with_nonexistent_directory(self, tmp_path: Path) -> None:
        """Test initialization with a non-existent directory raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent"
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            ID3TagFixer(nonexistent)

    def test_init_with_file_instead_of_directory(self, tmp_path: Path) -> None:
        """Test initialization with a file path raises ValueError."""
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")
        with pytest.raises(ValueError, match="Path is not a directory"):
            ID3TagFixer(file_path)

    def test_album_title_format(self, tmp_mp3_dir: Path) -> None:
        """Test that album title is correctly formatted."""
        fixer = ID3TagFixer(tmp_mp3_dir)
        assert fixer.album_title.startswith("DJ.Studio Pre-Mix ")
        assert fixer.compilation_grouping == fixer.album_title


class TestID3TagFixerFindFiles:
    """Tests for MP3 file discovery."""

    def test_find_mp3_files_empty_directory(self, tmp_mp3_dir: Path) -> None:
        """Test finding MP3 files in an empty directory."""
        fixer = ID3TagFixer(tmp_mp3_dir)
        assert fixer.mp3_files == []

    def test_find_mp3_files_with_files(self, tmp_mp3_dir: Path) -> None:
        """Test finding MP3 files in a directory with MP3 files."""
        # Create dummy MP3 files (just empty files for testing discovery)
        (tmp_mp3_dir / "track1.mp3").touch()
        (tmp_mp3_dir / "track2.mp3").touch()
        (tmp_mp3_dir / "track3.mp3").touch()

        fixer = ID3TagFixer(tmp_mp3_dir)
        assert len(fixer.mp3_files) == 3
        assert all(f.suffix == ".mp3" for f in fixer.mp3_files)

    def test_find_mp3_files_ignores_other_extensions(self, tmp_mp3_dir: Path) -> None:
        """Test that non-MP3 files are ignored."""
        (tmp_mp3_dir / "track1.mp3").touch()
        (tmp_mp3_dir / "image.jpg").touch()
        (tmp_mp3_dir / "document.txt").touch()

        fixer = ID3TagFixer(tmp_mp3_dir)
        assert len(fixer.mp3_files) == 1

    def test_find_mp3_files_sorted(self, tmp_mp3_dir: Path) -> None:
        """Test that MP3 files are returned sorted."""
        (tmp_mp3_dir / "z_track.mp3").touch()
        (tmp_mp3_dir / "a_track.mp3").touch()
        (tmp_mp3_dir / "m_track.mp3").touch()

        fixer = ID3TagFixer(tmp_mp3_dir)
        names = [f.name for f in fixer.mp3_files]
        assert names == ["a_track.mp3", "m_track.mp3", "z_track.mp3"]


class TestID3TagFixerFixTags:
    """Tests for the fix_tags method."""

    def test_fix_tags_empty_directory(self, tmp_mp3_dir: Path, capsys) -> None:
        """Test fix_tags with no MP3 files."""
        fixer = ID3TagFixer(tmp_mp3_dir)
        result = fixer.fix_tags()

        assert result == 0
        captured = capsys.readouterr()
        assert "No MP3 files found" in captured.out

    @patch("DJ_Studio.Fix_id3_tags.ID3")
    def test_fix_tags_processes_files(self, mock_id3, tmp_mp3_dir: Path) -> None:
        """Test that fix_tags processes all MP3 files."""
        # Create dummy MP3 files
        (tmp_mp3_dir / "track1.mp3").touch()
        (tmp_mp3_dir / "track2.mp3").touch()

        # Mock ID3 behavior
        mock_id3_instance = MagicMock()
        mock_id3_instance.pprint.return_value = "ID3 tags"
        mock_id3.return_value = mock_id3_instance

        fixer = ID3TagFixer(tmp_mp3_dir)
        result = fixer.fix_tags()

        assert result == 2
        assert mock_id3.call_count == 2
        assert mock_id3_instance.save.call_count == 2


class TestID3TagFixerConstants:
    """Tests for class constants."""

    def test_class_constants(self, tmp_mp3_dir: Path) -> None:
        """Test that class constants are correctly defined."""
        assert ID3TagFixer.ALBUM_ARTIST == "DJ.Studio"
        assert ID3TagFixer.COMPOSER == "DJ.Studio"
        assert ID3TagFixer.COMPILATION == "1"
