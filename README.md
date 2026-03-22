# dj-tools

Scripts and tools that help organize DJ workflows across multiple platforms (DJ.Studio, Rekordbox, Traktor).

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

### Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install only runtime dependencies
pip install mutagen
```

## Tools

### DJ_Studio

#### Fix_id3_tags.py

Script to add missing ID3 tags after exporting from DJ.Studio to pre-listen the mix in Apple Music.

**Features:**
- Adds track numbers, album title, compilation grouping
- Sets album artist and composer to "DJ.Studio"
- Automatically timestamps the album with current date/time

**Usage:**
```bash
python DJ_Studio/Fix_id3_tags.py "/path/to/mp3/directory"
```

### Generic

#### Display_Id3_Tags.py

Script to display the ID3 tags of MP3 files in a given directory.

**Usage:**
```bash
python Generic/Display_Id3_Tags.py "/path/to/mp3/directory"
```

### Rekordbox

#### CUE_Converter.py

Script to convert CUE exports into human-readable text track lists (e.g., for YouTube descriptions).

**Usage:**
```bash
python Rekordbox/CUE_Converter.py "/path/to/file.cue"
```

**Output Format:**
```
00:00:00 - Artist Name - Track Title
03:45:00 - Another Artist - Another Track
```

### Traktor

#### M3U_to_NML_converter.py

Script to convert M3U playlists into Native Instruments NML playlists for Traktor Pro.

**Usage:**
```bash
python Traktor/M3U_to_NML_converter.py "/path/to/playlist.m3u" "/path/to/output.nml"
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_cue_converter.py
```

### Code Style

```bash
# Check formatting
black . --check

# Auto-format
black .

# Lint
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Project Structure

```
dj-tools/
├── DJ_Studio/
│   └── Fix_id3_tags.py
├── Generic/
│   └── Display_Id3_Tags.py
├── Rekordbox/
│   └── CUE_Converter.py
├── Traktor/
│   └── M3U_to_NML_converter.py
├── tests/
│   ├── conftest.py
│   ├── test_fix_id3_tags.py
│   ├── test_display_id3_tags.py
│   ├── test_cue_converter.py
│   └── test_m3u_to_nml_converter.py
├── AGENTS.md
├── README.md
├── pytest.ini
└── requirements.txt
```

## License

See [LICENSE](LICENSE) for details.
