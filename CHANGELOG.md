# Changelog

All notable changes to the **pdf-autofillr-cli** repository are documented here.
Each release also has an entry in `cli/CHANGELOG.md`.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

---

## Packages

| Package | Latest | Changelog |
|---------|--------|-----------|
| pdf-autofillr-cli | 0.1.1 | [cli/CHANGELOG.md](cli/CHANGELOG.md) |

---

## [Unreleased]

### Planned

- `pdf-autofillr logs` — tail logs across all running module servers
- `pdf-autofillr doctor` — extended diagnostics with fix suggestions
- Shell completion for bash, zsh, and fish
- `--output json` flag on all commands for scripting

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