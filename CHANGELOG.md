# Changelog

All notable changes to the **pdf-autofillr-cli** repository are documented here.
Each release also has an entry in `cli/CHANGELOG.md`.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

---

## Packages

| Package | Latest | Changelog |
|---------|--------|-----------|
| pdf-autofillr-cli | 0.3.0 | [cli/CHANGELOG.md](cli/CHANGELOG.md) |

---

## [Unreleased]

### Planned

- `pdf-autofillr-cli logs` — tail logs across all running module servers
- `pdf-autofillr-cli doctor` — extended diagnostics with fix suggestions
- Shell completion for bash, zsh, and fish
- `--output json` flag on all commands for scripting

---

## [cli-0.3.0] — 2026-05-27

### Added

- `extract` — extract field schema from a PDF form, output as JSON
- `validate` — validate a filled PDF against a field schema (`--strict` mode available)
- `mypy`, `flake8`, `flake8-bugbear` added to dev dependencies
- `[tool.mypy]` and `[tool.flake8]` config added to `pyproject.toml`
- Tests: `test_cmd_extract_validate.py` covering both new commands

---

## [cli-0.2.2] — 2026-05-23

### Fixed

- `setup` now copies `usage/` guides into working directory (alongside `configs/` and `.env`)
- Previously only showed the path inside the package — now extracts to your project folder

---

## [cli-0.2.1] — 2026-05-23

### Added

- `usage/` folder bundled inside the package — one guide per command (embed, fill, run, batch, chatbot, doc-upload, mapper, rag, plugins)
- Each guide shows required files, folder structure, minimum `.env`, and exact command with expected output
- `setup` now shows path to `usage/` guides after installation
- `USAGE.md` bundled inside the package so it's always available after `pip install`

### Fixed

- `setup` now correctly finds `USAGE.md` and `usage/` from installed package location

---

## [cli-0.2.0] — 2026-05-23

### Added

- `embed` — top-level command to embed field metadata into a PDF template
- `fill` — top-level command to fill an embedded PDF with JSON data
- `run` — full pipeline: embed + fill in one shot
- `batch` — fill multiple PDFs from a directory of JSON files
- Simplified `status` — checks modules installed + env vars set + `.env` present
- Simplified `setup` — copies `configs/` from SDK samples + creates `.env`

### Changed

- Entry point renamed from `pdf-autofillr` to `pdf-autofillr-cli` to avoid conflict with SDK
- `pdf-autofillr[all]` is now the single hard dependency — installs everything
- All commands now use `PDFPipeline` + `MapperConfig` (correct SDK API)
- `chatbot` uses `chatbotClient(storage, form_config)` + `send_message()` (correct SDK API)
- `doc-upload` uses `DocUploadClient()` + `.run()` (correct SDK API)
- Removed `requirements/` individual module extras — single dep handles all
- Updated author to Engineers Mind / Support@pdffillr.ai
- Fixed `pyproject.toml` license format (SPDX), updated URLs to correct repo

### Fixed

- `chatbot.storage.local` → `chatbot.storage.local_storage` (correct module path)
- `MapperOrchestrator` → `PDFPipeline` + `MapperConfig` (MapperOrchestrator doesn't exist)
- `chatbotClient.from_env()` → `chatbotClient(storage, form_config)` (no from_env)
- `DocUploadClient.from_env()` → `DocUploadClient()` (reads env automatically)
- `client.process()` → `client.run()` (correct method name)
- Removed unused imports flagged by CodeQL

---

## [cli-0.1.1] — 2026-05-23

### Fixed

- Remove unused imports flagged by CodeQL (`os`, `json`, `Optional`, `patch`, `MagicMock`, `sys`)
- Remove `pass` from non-empty `except` block in `cmd_rag.py`
- Remove unused `patch` import from `test_utils.py`

---

## [cli-0.1.0] — 2026-04-30

### Added

- Initial release — `pdf-autofillr` unified CLI for all pdf-autofillr modules
- `status` command — checks installed modules, config files, env vars, connections
- `setup` command — first-time project setup for any or all modules
- `rag` subcommands: `init-vectors`, `predict`, `feedback`, `metrics`, `system-info`, `error-analytics`
- `chatbot` subcommands: `start`, `session`, `sessions`
- `mapper` subcommands: `embed`, `fill`, `start`
- `doc-upload` subcommands: `process`, `start`
- `plugins` subcommands: `list`, `info`
- Lazy imports — CLI loads instantly even when only some modules are installed
- Friendly install hints when a required module is missing
- 69 tests (unit + integration), all passing
- Benchmarking suite for CLI commands across 6 document domains
- Docker deployment configuration
- GitHub Actions CI (test + PyPI publish)
- Full docs: `README.md`, `USAGE.md`, `quickstart.md`