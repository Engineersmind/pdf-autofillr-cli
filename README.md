# pdf-autofillr-cli

> Unified command-line interface for all pdf-autofillr modules.

[![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-cli)](https://pypi.org/project/pdf-autofillr-cli/)
[![Python](https://img.shields.io/pypi/pyversions/pdf-autofillr-cli)](https://pypi.org/project/pdf-autofillr-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/Engineersmind/pdf-autofillr-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/Engineersmind/pdf-autofillr-cli/actions)

One install. One command. All modules.

```bash
pip install "pdf-autofillr-cli[all]"
pdf-autofillr status
```

## What is this?

`pdf-autofillr-cli` wraps the five pdf-autofillr packages — **chatbot**, **mapper**, **rag**, **doc-upload**, and **plugins** — under a single `pdf-autofillr` terminal command.

```
pdf-autofillr status
pdf-autofillr setup
pdf-autofillr rag predict --user u1 --session s1 --pdf p1 --fields fields.json --hash abc123
pdf-autofillr chatbot start
pdf-autofillr mapper embed --pdf blank.pdf --user u1 --id lp_v1
pdf-autofillr doc-upload process --doc investor.pdf --pdf blank.pdf --schema form_keys.json --user u1 --id lp_v1
pdf-autofillr plugins list
```

## Install

```bash
pip install pdf-autofillr-cli                   # CLI only
pip install "pdf-autofillr-cli[rag]"            # + RAG module
pip install "pdf-autofillr-cli[chatbot]"        # + chatbot module
pip install "pdf-autofillr-cli[mapper]"         # + mapper module
pip install "pdf-autofillr-cli[doc-upload]"     # + doc-upload module
pip install "pdf-autofillr-cli[all]"            # + all modules
```

## Quick start

```bash
pdf-autofillr setup          # creates .env, configs/, data/
pdf-autofillr status         # verify everything is configured
pdf-autofillr --help         # see all commands
```

→ See [packages/cli/quickstart.md](packages/cli/quickstart.md) for a 3-step walkthrough.
→ See [packages/cli/USAGE.md](packages/cli/USAGE.md) for full command reference.

## Repository layout

```
pdf-autofillr-cli/
├── packages/
│   └── cli/                  ← the PyPI package (pdf-autofillr-cli)
├── benchmarks/               ← CLI benchmarking suite
├── deployment/               ← Docker configs
├── docs/                     ← architecture and guides
├── examples/                 ← usage examples
├── .github/workflows/        ← CI: tests + PyPI publish
└── CHANGELOG.md
```

## Development

```bash
git clone https://github.com/Engineersmind/pdf-autofillr-cli.git
cd pdf-autofillr-cli/packages/cli
pip install -e ".[dev]"
pytest tests/ -v              # 69 tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contributor guide.

## Related packages

| Package | Description |
|---|---|
| [`pdf-autofillr`](https://pypi.org/project/pdf-autofillr/) | Umbrella package |
| [`pdf-autofillr-rag`](https://pypi.org/project/pdf-autofillr-rag/) | RAG prediction engine |
| [`pdf-autofillr-chatbot`](https://pypi.org/project/pdf-autofillr-chatbot/) | Conversational onboarding |
| [`pdf-autofillr-mapper`](https://pypi.org/project/pdf-autofillr-mapper/) | Semantic PDF field mapper |
| [`pdf-autofillr-doc-upload`](https://pypi.org/project/pdf-autofillr-doc-upload/) | Document extraction |
| [`pdf-autofillr-plugins`](https://pypi.org/project/pdf-autofillr-plugins/) | Plugin framework |

## License

MIT — see [LICENSE](LICENSE).
