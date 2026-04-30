# Changelog

All notable changes to `pdf-autofillr-cli` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-04-30

### Added
- Initial release of the unified CLI for all pdf-autofillr modules
- `pdf-autofillr` entry point — single command for the entire suite
- `status` — checks installed modules, config files, and env variables
- `setup` — first-time setup wizard for any or all modules
- `rag` — full RAG subcommand: `init-vectors`, `predict`, `feedback`, `metrics`, `system-info`, `error-analytics`
- `chatbot` — chatbot subcommand: `start` (API server), `session` (interactive terminal), `sessions` (list)
- `mapper` — mapper subcommand: `embed`, `fill`, `start` (API server)
- `doc-upload` — doc-upload subcommand: `process`, `start` (API server)
- `plugins` — plugin inspection: `list`, `info`
- Lazy module imports — CLI loads instantly even when only some modules are installed
- Friendly install hints when a required module is missing
- Full test suite: 69 tests across unit and integration

---

## Unreleased

### Planned
- `pdf-autofillr logs` — tail logs across all running module servers
- `pdf-autofillr doctor` — extended diagnostics with fix suggestions
- Shell completion for bash, zsh, and fish
- `--output json` flag on all commands for scripting
