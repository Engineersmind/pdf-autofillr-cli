# Changelog

All notable changes to `pdf-autofillr-cli` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.3.0] - 2026-05-27

### Added
- `extract` — extract field schema from a PDF form, writes to JSON
  - `--output` to specify destination path (default: `<name>_schema.json`)
  - `--pretty` flag for indented JSON output
  - Creates output directory automatically if it doesn't exist
- `validate` — validate a filled PDF against a field schema
  - `--schema` required — accepts `form_keys.json` or `extract` output
  - `--strict` flag to also fail on empty (not just missing) fields
  - Local fallback validation via `pypdf` when SDK method unavailable
- `mypy`, `flake8`, `flake8-bugbear` added to `[dev]` optional dependencies
- `[tool.mypy]` and `[tool.flake8]` config sections added to `pyproject.toml`
- Tests for `extract` and `validate` — `test_cmd_extract_validate.py`

### Changed
- Version bumped `0.2.2` → `0.3.0`
- `main.py` updated: `extract` and `validate` registered in parser (quick commands block)
- `__init__.py` updated: version string and docstring updated with new commands

---

## [0.2.2] - 2026-05-23

### Fixed
- `setup` now copies `usage/` guides into working directory (alongside `configs/` and `.env`)
- Previously only showed the path inside the package — now extracts to your project folder

---

## [0.2.1] - 2026-05-23

### Added
- `usage/` folder bundled inside the package — one guide per command (embed, fill, run, batch, chatbot, doc-upload, mapper, rag, plugins)
- Each guide shows required files, folder structure, minimum `.env`, and exact command with expected output
- `setup` now shows path to `usage/` guides after installation
- `USAGE.md` bundled inside the package so it's always available after `pip install`

### Fixed
- `setup` now correctly finds `USAGE.md` and `usage/` from installed package location

---

## [0.2.0] - 2026-05-23

### Added
- `embed` — top-level command to embed field metadata into a PDF template
- `fill` — top-level command to fill an embedded PDF with JSON data
- `run` — top-level command: embed + fill in one shot
- `batch` — fill multiple PDFs from a directory of JSON files
- Simplified `status` — clean output showing installed modules and versions
- Simplified `.env.example` — just API key and optional paths
- New `USAGE.md` — dead simple copy-paste examples

### Changed
- Entry point renamed from `pdf-autofillr` to `pdf-autofillr-cli` to avoid conflict with SDK
- `pdf-autofillr[all]` is now the single hard dependency — installs everything
- Removed `requirements/` folder — `pyproject.toml` handles all deps
- Fixed `pyproject.toml` license format (SPDX), updated URLs to correct repo
- Updated author to Engineers Mind / Support@pdffillr.ai

### Fixed
- Remove unused imports flagged by CodeQL
- Remove `pass` from non-empty `except` block in `cmd_rag.py`

---

## [0.1.1] - 2026-05-23

### Fixed
- Remove unused imports flagged by CodeQL (`os`, `json`, `Optional`, `patch`, `MagicMock`, `sys`)
- Remove `pass` from non-empty `except` block in `cmd_rag.py`
- Remove unused `patch` import from `test_utils.py`

---

## [0.1.0] - 2026-04-30

### Added
- Initial release of the unified CLI for all pdf-autofillr modules
- `pdf-autofillr-cli` entry point — single command for the entire suite
- `status`, `setup`, `rag`, `chatbot`, `mapper`, `doc-upload`, `plugins` subcommands
- Lazy module imports — CLI loads instantly even when only some modules are installed
- Full test suite: 69 tests across unit and integration

---

## [Unreleased]

### Planned
- `pdf-autofillr-cli logs` — tail logs across running module servers
- `pdf-autofillr-cli doctor` — extended diagnostics with fix suggestions
- Shell completion for bash, zsh, and fish
- `--output json` flag on all commands for scripting