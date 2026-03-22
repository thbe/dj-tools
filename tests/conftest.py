"""
Pytest configuration and shared fixtures for dj-tools tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_mp3_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for MP3 test files."""
    mp3_dir = tmp_path / "mp3s"
    mp3_dir.mkdir()
    return mp3_dir


@pytest.fixture
def tmp_m3u_file(tmp_path: Path) -> Path:
    """Create a temporary M3U file for testing."""
    m3u_file = tmp_path / "playlist.m3u"
    m3u_content = """#EXTM3U
#EXTINF:180,Artist 1 - Track 1
/path/to/track1.mp3
#EXTINF:200,Artist 2 - Track 2
/path/to/track2.mp3
#EXTINF:220,Artist 3 - Track 3
/path/to/track3.mp3
"""
    m3u_file.write_text(m3u_content, encoding="utf-8")
    return m3u_file


@pytest.fixture
def tmp_cue_file(tmp_path: Path) -> Path:
    """Create a temporary CUE file for testing."""
    cue_file = tmp_path / "mix.cue"
    cue_content = """PERFORMER "DJ Mix"
TITLE "Summer Mix 2024"
FILE "mix.wav" WAVE
  TRACK 01 AUDIO
    TITLE "First Track"
    PERFORMER "Artist One"
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Second Track"
    PERFORMER "Artist Two"
    INDEX 01 03:45:00
  TRACK 03 AUDIO
    TITLE "Third Track"
    PERFORMER "Artist Three"
    INDEX 01 07:30:00
"""
    cue_file.write_text(cue_content, encoding="utf-8")
    return cue_file


@pytest.fixture
def sample_cue_content() -> str:
    """Return sample CUE file content for parsing tests."""
    return """PERFORMER "Global Artist"
TITLE "Album Title"
FILE "audio.wav" WAVE
  TRACK 01 AUDIO
    TITLE "Song One"
    PERFORMER "Artist A"
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Song Two"
    INDEX 01 04:20:00
"""
