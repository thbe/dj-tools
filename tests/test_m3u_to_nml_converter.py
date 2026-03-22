"""
Tests for Traktor/M3U_to_NML_converter.py

Author:       Thomas Bendler <code@thbe.org>
Purpose:      Unit tests for M3UToNMLConverter class
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from Traktor.M3U_to_NML_converter import M3UToNMLConverter


class TestM3UToNMLConverterInit:
    """Tests for M3UToNMLConverter initialization."""

    def test_init_with_valid_file(self, tmp_m3u_file: Path, tmp_path: Path) -> None:
        """Test initialization with a valid M3U file."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        assert converter.m3u_path == tmp_m3u_file
        assert converter.nml_path == nml_path

    def test_init_with_nonexistent_file(self, tmp_path: Path) -> None:
        """Test initialization with non-existent M3U file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.m3u"
        nml_path = tmp_path / "output.nml"

        with pytest.raises(FileNotFoundError, match="M3U file not found"):
            M3UToNMLConverter(nonexistent, nml_path)

    def test_init_with_directory_instead_of_file(self, tmp_path: Path) -> None:
        """Test initialization with a directory raises ValueError."""
        nml_path = tmp_path / "output.nml"

        with pytest.raises(ValueError, match="Path is not a file"):
            M3UToNMLConverter(tmp_path, nml_path)


class TestM3UToNMLConverterReadM3U:
    """Tests for M3U file reading."""

    def test_read_m3u_extracts_audio_files(
        self, tmp_m3u_file: Path, tmp_path: Path
    ) -> None:
        """Test that read_m3u extracts audio file paths."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        audio_files = converter.read_m3u()

        assert len(audio_files) == 3
        assert audio_files[0] == "/path/to/track1.mp3"
        assert audio_files[1] == "/path/to/track2.mp3"
        assert audio_files[2] == "/path/to/track3.mp3"

    def test_read_m3u_ignores_comments(
        self, tmp_m3u_file: Path, tmp_path: Path
    ) -> None:
        """Test that M3U comments and metadata are ignored."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        audio_files = converter.read_m3u()

        # Should not include lines starting with #
        for f in audio_files:
            assert not f.startswith("#")

    def test_read_m3u_ignores_empty_lines(self, tmp_path: Path) -> None:
        """Test that empty lines are ignored."""
        m3u_content = """/path/to/track1.mp3

/path/to/track2.mp3

"""
        m3u_file = tmp_path / "sparse.m3u"
        m3u_file.write_text(m3u_content, encoding="utf-8")
        nml_path = tmp_path / "output.nml"

        converter = M3UToNMLConverter(m3u_file, nml_path)
        audio_files = converter.read_m3u()

        assert len(audio_files) == 2

    def test_read_m3u_empty_file(self, tmp_path: Path) -> None:
        """Test reading an empty M3U file."""
        m3u_file = tmp_path / "empty.m3u"
        m3u_file.write_text("", encoding="utf-8")
        nml_path = tmp_path / "output.nml"

        converter = M3UToNMLConverter(m3u_file, nml_path)
        audio_files = converter.read_m3u()

        assert audio_files == []


class TestM3UToNMLConverterGenerateNML:
    """Tests for NML content generation."""

    def test_generate_nml_content_structure(
        self, tmp_m3u_file: Path, tmp_path: Path
    ) -> None:
        """Test that generated NML has correct structure."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        audio_files = ["/path/to/track.mp3"]
        nml_content = converter.generate_nml_content(audio_files)

        assert "<nml>" in nml_content
        assert "</nml>" in nml_content
        assert "<tracks>" in nml_content
        assert "</tracks>" in nml_content
        assert "<clip>" in nml_content
        assert "<file>/path/to/track.mp3</file>" in nml_content

    def test_generate_nml_content_multiple_files(
        self, tmp_m3u_file: Path, tmp_path: Path
    ) -> None:
        """Test NML generation with multiple audio files."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        audio_files = ["/path/to/track1.mp3", "/path/to/track2.mp3"]
        nml_content = converter.generate_nml_content(audio_files)

        assert nml_content.count("<clip>") == 2
        assert "<file>/path/to/track1.mp3</file>" in nml_content
        assert "<file>/path/to/track2.mp3</file>" in nml_content


class TestM3UToNMLConverterConvert:
    """Tests for the convert method."""

    def test_convert_creates_nml_file(self, tmp_m3u_file: Path, tmp_path: Path) -> None:
        """Test that convert creates the NML output file."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        result = converter.convert()

        assert nml_path.exists()
        assert result == 3

    def test_convert_returns_zero_for_empty(self, tmp_path: Path, capsys) -> None:
        """Test that convert returns 0 for empty M3U file."""
        m3u_file = tmp_path / "empty.m3u"
        m3u_file.write_text("", encoding="utf-8")
        nml_path = tmp_path / "output.nml"

        converter = M3UToNMLConverter(m3u_file, nml_path)
        result = converter.convert()

        assert result == 0
        captured = capsys.readouterr()
        assert "No audio files found" in captured.out

    def test_convert_nml_content_is_valid(
        self, tmp_m3u_file: Path, tmp_path: Path
    ) -> None:
        """Test that converted NML file contains expected content."""
        nml_path = tmp_path / "output.nml"
        converter = M3UToNMLConverter(tmp_m3u_file, nml_path)

        converter.convert()

        nml_content = nml_path.read_text(encoding="utf-8")
        assert "<nml>" in nml_content
        assert "/path/to/track1.mp3" in nml_content
        assert "/path/to/track2.mp3" in nml_content
        assert "/path/to/track3.mp3" in nml_content
