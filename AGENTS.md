# AGENTS.md

## 🚀 Project Context
**dj-tools** is a collection of Python automation scripts designed to optimize DJ workflows across multiple platforms (DJ.Studio, Rekordbox, Traktor). The codebase consists of standalone utilities organized by the target software they support.

## 🛠️ Environment & Commands

### Setup
The project relies on Python 3 and a few dependencies.
```bash
# Install dependencies
pip install -r requirements.txt
```

### Execution
Scripts are standalone and executed via CLI.
```bash
# Example: Fix ID3 tags for DJ.Studio export
python DJ_Studio/Fix_id3_tags.py "/absolute/path/to/mp3s"

# Example: Convert CUE file to tracklist
python Rekordbox/CUE_Converter.py "/absolute/path/to/file.cue"
```

### Testing
Currently, there is no formal test suite. Agents should:
1.  **Create Tests:** When modifying scripts, create a corresponding `test_scriptname.py` using `pytest` conventions if possible.
2.  **Manual Verification:** If automated tests are not feasible, describe the manual verification steps clearly.
```bash
# Recommended command if tests are added
pytest tests/
# Run single test file
pytest tests/test_specific_script.py
```

### Linting & Formatting
Follow standard Python guidelines.
```bash
# Recommended style enforcement
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
black . --check
```

## 🔍 Git & Version Control
### Commit Messages
Follow the **Conventional Commits** specification.
*   `feat: add M3U to NML converter`
*   `fix: resolve encoding issue in CUE parser`
*   `refactor: migrate os.path to pathlib in Fix_id3_tags`
*   `docs: update AGENTS.md with style guides`
*   `style: format code with black`

### Branching
*   Create feature branches for significant changes: `feature/description`.
*   Keep main branch stable.

## 📐 Code Style Guidelines

### 1. General Philosophy
*   **Modern Python:** Use Python 3.10+ features (e.g., modern type hinting `list[str]` instead of `List[str]`).
*   **Path Handling:** ALWAYS use `pathlib.Path` instead of `os.path` or string manipulation for file paths. This is a strict requirement for all new code and refactoring.
*   **Object-Oriented:** Encapsulate script logic in Classes (e.g., `ID3TagFixer`, `CueConverter`) rather than loose functions.
*   **Statelessness:** Scripts should be runnable multiple times without side effects (idempotency) where possible.

### 2. Formatting & Structure
*   **Indentation:** 4 spaces (standard).
*   **Line Length:** 88 characters (Black default).
*   **Imports:** Sorted and grouped (Standard Library -> Third Party -> Local).
    *   Avoid wildcard imports (`from module import *`).
    *   Remove unused imports immediately.
    ```python
    import sys
    import logging
    from pathlib import Path
    
    from mutagen.id3 import ID3  # 3rd party
    ```

### 3. Naming Conventions
*   **Classes:** `PascalCase` (e.g., `M3UToNMLConverter`).
*   **Functions/Methods:** `snake_case` (e.g., `generate_nml_content`).
*   **Variables:** `snake_case` (descriptive, avoiding single letters like `x`, `i` unless in short loops).
*   **Constants:** `UPPER_CASE` (e.g., `TIME_PATTERN`, `DEFAULT_ENCODING`).
*   **Files:** `Snake_Case` or `snake_case` (maintain consistency with directory). Prefer `snake_case` for new files.

### 4. Type Hinting
*   **Mandatory:** Public methods and classes must have type hints.
*   **Return Types:** Explicitly state return types, including `None`.
*   **Collections:** Use built-in types (`list`, `dict`, `tuple`) instead of `typing` module counterparts where possible.
    ```python
    def _read_file(self) -> str:
        return self.cue_file_path.read_text(encoding="utf-8")
        
    def get_tracks(self) -> list[dict[str, str]]:
        # ...
    ```

### 5. Documentation
*   **Module Level:** Every script must have a top-level docstring with `Author`, `Date`, `Purpose`, and `ChangeLog`.
*   **Method Level:** Concise docstrings for complex logic. Use imperative mood ("Returns the list..." not "Returning...").
    ```python
    """
    Author:       [Name]
    Date:         [Date]
    Purpose:      [Short description]
    """
    ```
*   **Comments:** Use comments to explain *why*, not *what*. Code should be self-documenting.

### 6. Error Handling
*   **Graceful Exit:** Catch expected errors (FileNotFound, DecodeError) and print user-friendly messages to `stdout` before `sys.exit(1)`.
*   **Tracebacks:** Avoid raw stack traces for known error conditions.
*   **Specific Exceptions:** Catch specific exceptions (`FileNotFoundError`) rather than bare `Exception`.

## 📦 Dependencies & Refactoring
### adding Dependencies
*   If a new library is required, add it to `requirements.txt`.
*   Prefer standard library solutions where feasible (e.g., `argparse` over `click` for simple scripts, unless complex CLI is needed).

### Refactoring Legacy Code
When touching existing files, apply the "Boy Scout Rule": leave the code cleaner than you found it.
1.  **Switch to `pathlib`:** Replace `os.path.join`, `glob.glob` (string-based) with `Path.glob`.
2.  **Add Type Hints:** If missing, add them to function signatures.
3.  **Clean Imports:** Remove unused or deprecated imports.

## ⚠️ Anti-Patterns (Do Not Use)
*   **String Path Manipulation:** `path = folder + "/" + filename`. USE `Path / filename`.
*   **Magic Numbers/Strings:** Extract them to constants.
*   **Global State:** Avoid global variables; use class attributes.
*   **Bare Excepts:** `except:` without an exception type is forbidden.
*   **Print Debugging:** Remove `print("here")` before committing. Use `logging` if debug output is needed permanently.

## 🤖 Agent Protocol
1.  **Analysis:** Read the specific script and its dependencies before editing. Understand the class structure.
2.  **Refactoring:** If modifying legacy code (e.g., using `os.path`), refactor it to `pathlib` as part of the task.
3.  **Safety:** Verify file operations (Read/Write) with `ls` or `Read` checks before execution.
4.  **Output:** When generating lists or reports, ensure the format matches existing CLI output styles.
5.  **Testing:** Since no CI exists, YOU are the CI. Verify syntax with `python -m py_compile script.py` if unsure, or run the script with `--help` or sample data to ensure it doesn't crash on import.
