[![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-cli)](https://pypi.org/project/pdf-autofillr-cli/)
[![Python](https://img.shields.io/pypi/pyversions/pdf-autofillr-cli)](https://pypi.org/project/pdf-autofillr-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/Engineersmind/pdf-autofillr-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/Engineersmind/pdf-autofillr-cli/actions/workflows/tests.yml)
[![Platform](https://img.shields.io/badge/platform-pdffillr.ai-blue)](https://pdffillr.ai)

<div align="center">

# pdf-autofillr-cli

**Fill PDF forms from your terminal using any LLM — one command, all modules.**

[**Quick Start**](#quick-start) · [**Python SDK**](https://github.com/EngineersMind/pdf-autofillr-python-sdk) · [**Live Platform**](https://pdffillr.ai)

</div>

---

> **Status:** Under active development. For production use today, see the [Python SDK](https://github.com/EngineersMind/pdf-autofillr-python-sdk) or the [live platform at pdffillr.ai](https://pdffillr.ai).

## What it does

`pdf-autofillr-cli` is a unified terminal interface for all pdf-autofillr modules. One install gives you `embed`, `fill`, `run`, `batch`, `chatbot`, `doc-upload`, `rag`, `mapper`, and `plugins` — all under one command.

| Without CLI | With CLI |
|---|---|
| `ragpdf predict ...` | `pdf-autofillr-cli rag predict ...` |
| `chatbot-cli ...` | `pdf-autofillr-cli chatbot session ...` |
| `pdf-mapper ...` | `pdf-autofillr-cli mapper embed ...` |
| `doc-upload-cli ...` | `pdf-autofillr-cli doc-upload process ...` |
| No unified pipeline | `pdf-autofillr-cli run form.pdf --schema keys.json --data data.json` |

---

## Installation

```bash
pip install pdf-autofillr-cli
```

This installs the full SDK (`pdf-autofillr[all]`) alongside the CLI automatically.

---

## Quick Start

```bash
# Step 1: First-time setup — creates configs/ and .env
pdf-autofillr-cli setup

# Step 2: Add your API key to .env
# OPENAI_API_KEY=sk-...  or  ANTHROPIC_API_KEY=sk-ant-...

# Step 3: Check everything is ready
pdf-autofillr-cli status

# Step 4: Embed your blank PDF template (run once per form)
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json

# Step 5: Fill it with data
pdf-autofillr-cli fill form.pdf --data data.json

# Or do steps 4+5 in one shot
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json
```

---

## All Commands

### Quick commands

```bash
# Embed field metadata into a blank PDF template (once per template)
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json

# Fill an embedded PDF with JSON data
pdf-autofillr-cli fill form.pdf --data data.json
pdf-autofillr-cli fill form.pdf --data '{"first_name": "Jane", "last_name": "Doe"}'

# Full pipeline: embed + fill in one shot
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json --output filled.pdf

# Batch fill from a directory of JSON files
pdf-autofillr-cli batch --template form.pdf --schema configs/form_keys.json --input data/ --output output/
```

### Chatbot

```bash
pdf-autofillr-cli chatbot session --pdf form.pdf --user u1
pdf-autofillr-cli chatbot start --port 8000
pdf-autofillr-cli chatbot sessions
```

### Doc Upload

```bash
pdf-autofillr-cli doc-upload process \
  --doc investor.pdf \
  --pdf blank_form.pdf \
  --schema configs/form_keys.json \
  --user u1 --id lp_sub_v1
```

### Mapper (low-level)

```bash
pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json
pdf-autofillr-cli mapper fill  --pdf form.pdf --data data.json
pdf-autofillr-cli mapper start --port 8001
```

### RAG

```bash
pdf-autofillr-cli rag init-vectors
pdf-autofillr-cli rag predict --user u1 --session s1 --pdf p1 --fields fields.json --hash abc123
pdf-autofillr-cli rag metrics --type global
pdf-autofillr-cli rag system-info
pdf-autofillr-cli rag feedback --user u1 --session s1 --pdf p1 --errors errors.json
pdf-autofillr-cli rag error-analytics --from 2026-01-01T00:00:00Z
```

### Plugins

```bash
pdf-autofillr-cli plugins list
pdf-autofillr-cli plugins list --json
pdf-autofillr-cli plugins list --category extractor
pdf-autofillr-cli plugins info my-plugin
```

### Status & Setup

```bash
pdf-autofillr-cli status    # check modules + env vars
pdf-autofillr-cli setup     # create configs/ and .env
```

---

## data.json format

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "ssn": "123-45-6789"
}
```

---

## Supported LLMs

Set the API key in `.env` for whichever provider you use:

| Provider | Env var |
|---|---|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Ollama (local) | no key needed |

---

## Repository Layout

```
pdf-autofillr-cli/
├── cli/                  ← this package
│   ├── src/pdf_autofillr_cli/
│   ├── tests/
│   ├── pyproject.toml
│   └── CHANGELOG.md
├── benchmarks/
├── deployment/
├── docs/
└── examples/
```

---

## Development

```bash
git clone https://github.com/Engineersmind/pdf-autofillr-cli.git
cd pdf-autofillr-cli/cli
pip install -e ".[dev]"
pytest tests/ -v
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide.

---

## Related

| Package | Description |
|---|---|
| [pdf-autofillr-python-sdk](https://github.com/EngineersMind/pdf-autofillr-python-sdk) | Python SDK — programmatic use |
| [pdf-autofillr](https://pypi.org/project/pdf-autofillr/) | Umbrella PyPI package |
| [pdf-autofillr-mapper](https://pypi.org/project/pdf-autofillr-mapper/) | Semantic PDF field mapper |
| [pdf-autofillr-chatbot](https://pypi.org/project/pdf-autofillr-chatbot/) | Conversational onboarding |
| [pdf-autofillr-rag](https://pypi.org/project/pdf-autofillr-rag/) | RAG prediction engine |
| [pdf-autofillr-doc-upload](https://pypi.org/project/pdf-autofillr-doc-upload/) | Document extraction |

---

## License

MIT — see [LICENSE](LICENSE).
