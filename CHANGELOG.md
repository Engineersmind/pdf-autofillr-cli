# Changelog

All notable changes to the **pdf-autofillr-cli** repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [0.1.0] - 2026-04-30

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
