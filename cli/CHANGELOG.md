# Changelog

All notable changes to `pdf-autofillr-cli` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

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
- `pdf-autofillr-cli` is the CLI command (not `pdf-autofillr`)
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
