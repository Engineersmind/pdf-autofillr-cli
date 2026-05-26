# pdf-autofillr-cli

> Unified command-line interface for all **pdf-autofillr** modules.

One install. One command. All modules.

```bash
pip install "pdf-autofillr-cli[all]"
pdf-autofillr status
```

---

## What is this?

`pdf-autofillr-cli` wraps the five pdf-autofillr packages — **chatbot**, **mapper**, **rag**, **doc-upload**, and **plugins** — under a single `pdf-autofillr` terminal command. Instead of learning four separate CLIs, you get one consistent interface.

| Without this package | With this package |
|---|---|
| `ragpdf predict ...` | `pdf-autofillr rag predict ...` |
| `chatbot-cli ...` | `pdf-autofillr chatbot session ...` |
| `pdf-mapper-server` | `pdf-autofillr mapper start` |
| No unified status check | `pdf-autofillr status` |

---

## Install

```bash
# Minimal — CLI only (modules installed separately)
pip install pdf-autofillr-cli

# CLI + all modules
pip install "pdf-autofillr-cli[all]"

# CLI + specific modules
pip install "pdf-autofillr-cli[rag]"
pip install "pdf-autofillr-cli[chatbot]"
pip install "pdf-autofillr-cli[mapper]"
pip install "pdf-autofillr-cli[doc-upload]"
```

The CLI loads instantly regardless of which modules are installed. If you run a command for a module that isn't installed, you get a friendly hint — not a crash.

---

## Quick start

```bash
# 1. First-time setup
pdf-autofillr setup

# 2. Add API keys to .env
cp .env.example .env

# 3. Check everything is configured
pdf-autofillr status
```

→ See [quickstart.md](quickstart.md) for a 3-step walkthrough.

---

## Commands

### `pdf-autofillr status`

Shows which modules are installed, config files present, env vars, and inter-module connections.

```bash
pdf-autofillr status
pdf-autofillr status --path /path/to/project
```

---

### `pdf-autofillr setup`

First-time setup — creates `.env`, `configs/`, and `data/` skeleton.

```bash
pdf-autofillr setup                    # all installed modules
pdf-autofillr setup --module rag       # rag only
pdf-autofillr setup --force            # overwrite existing files
```

---

### `pdf-autofillr rag`

RAG field prediction commands. Requires `pip install "pdf-autofillr-cli[rag]"`.

```bash
# Generate vector embeddings (run once after setup)
pdf-autofillr rag init-vectors
pdf-autofillr rag init-vectors --backend openai --force

# Predict field mappings
pdf-autofillr rag predict \
  --user u1 --session s1 --pdf p1 \
  --fields fields.json \
  --hash abc123 \
  --category pdf_category.json

# Submit corrections (triggers re-learning)
pdf-autofillr rag feedback \
  --user u1 --session s1 --pdf p1 \
  --errors errors.json

# Accuracy and coverage metrics
pdf-autofillr rag metrics --type global
pdf-autofillr rag metrics --type pdf --user u1 --session s1 --pdf p1
pdf-autofillr rag metrics --type category --category "Private Markets"

# Vector DB overview
pdf-autofillr rag system-info

# Error analytics with date filters
pdf-autofillr rag error-analytics --from 2026-01-01T00:00:00Z
```

---

### `pdf-autofillr chatbot`

Conversational form-filling commands. Requires `pip install "pdf-autofillr-cli[chatbot]"`.

```bash
# Start the REST API server (default port 8001)
pdf-autofillr chatbot start
pdf-autofillr chatbot start --port 9000 --reload

# Run an interactive session in the terminal
pdf-autofillr chatbot session \
  --pdf data/input/blank_form.pdf \
  --user user_001

# Resume an existing session
pdf-autofillr chatbot session \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --session existing-session-id

# List all active sessions
pdf-autofillr chatbot sessions
```

---

### `pdf-autofillr mapper`

PDF template embedding and filling. Requires `pip install "pdf-autofillr-cli[mapper]"`.

Two-step workflow: embed once per blank form template, then fill many times.

```bash
# Step 1 — embed the blank template (run once per form)
pdf-autofillr mapper embed \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --id lp_sub_v1

# Step 2 — fill with user data (JSON file)
pdf-autofillr mapper fill \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --id lp_sub_v1 \
  --data user_data.json

# Step 2 — fill with inline JSON (Linux/Mac)
pdf-autofillr mapper fill \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --id lp_sub_v1 \
  --data '{"investor_name": "Jane Smith", "commitment_amount": "500000"}'

# Start the mapper API server (default port 8002)
pdf-autofillr mapper start
pdf-autofillr mapper start --port 8002 --reload
```

---

### `pdf-autofillr doc-upload`

Extract data from uploaded documents (PDF, DOCX, XLSX, CSV, JSON, TXT, MD) and fill a PDF form. Requires `pip install "pdf-autofillr-cli[doc-upload]"`.

```bash
# Extract from document and fill PDF in one step
pdf-autofillr doc-upload process \
  --doc investor_data.pdf \
  --pdf data/input/blank_form.pdf \
  --schema configs/form_keys.json \
  --user user_001 \
  --id lp_sub_v1

# Supported source formats: PDF, DOCX, XLSX, CSV, JSON, TXT, MD
pdf-autofillr doc-upload process --doc investor.xlsx ...
pdf-autofillr doc-upload process --doc investor.csv  ...

# Start the doc-upload API server (default port 8003)
pdf-autofillr doc-upload start
```

---

### `pdf-autofillr plugins`

Inspect installed plugins. Requires `pip install pdf-autofillr-plugins`.

```bash
# List all discovered plugins
pdf-autofillr plugins list

# Filter by category
pdf-autofillr plugins list --category validator
pdf-autofillr plugins list --category extractor

# Scan a specific directory
pdf-autofillr plugins list --path ./my_plugins/

# Output as JSON (useful for scripting)
pdf-autofillr plugins list --json

# Show detailed info for one plugin
pdf-autofillr plugins info email-validator
pdf-autofillr plugins info invoice-extractor --category extractor
```

---

## Configuration

Copy `.env.example` to `.env` and fill in the values for your setup:

```bash
cp .env.example .env
```

Key variables:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | OpenAI API key (chatbot, mapper, rag corrector) |
| `ANTHROPIC_API_KEY` | — | Anthropic API key (alternative LLM) |
| `RAGPDF_STORAGE` | `local` | RAG storage: `local`, `s3`, `azure`, `gcs` |
| `RAGPDF_EMBEDDING_BACKEND` | `sentence_transformer` | `sentence_transformer`, `openai`, `litellm` |
| `RAGPDF_VECTOR_STORE` | `local` | `local`, `pinecone`, `chroma`, `weaviate` |
| `RAGPDF_CORRECTOR_BACKEND` | `noop` | `noop`, `openai`, `anthropic` |
| `RAGPDF_API_KEY` | `dev-key` | Auth key for the RAG server |

Full reference in [.env.example](.env.example).

---

## For developers

### Run from source

```bash
git clone https://github.com/Engineersmind/pdf-autofillr.git
cd pdf-autofillr/packages/cli

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -e ".[dev]"

# Verify the entry point works
pdf-autofillr --version
pdf-autofillr --help
```

### Project layout

```
packages/cli/
├── src/
│   └── pdf_autofillr_cli/
│       ├── __init__.py          # version
│       ├── main.py              # entry point — builds parser, dispatches
│       ├── utils.py             # module availability checks
│       ├── cmd_status.py        # pdf-autofillr status
│       ├── cmd_setup.py         # pdf-autofillr setup
│       ├── cmd_rag.py           # pdf-autofillr rag *
│       ├── cmd_chatbot.py       # pdf-autofillr chatbot *
│       ├── cmd_mapper.py        # pdf-autofillr mapper *
│       ├── cmd_doc_upload.py    # pdf-autofillr doc-upload *
│       └── cmd_plugins.py       # pdf-autofillr plugins *
├── tests/
│   ├── conftest.py
│   ├── unit/                    # mocked, no modules needed
│   └── integration/             # full parser wiring tests
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── all.txt
├── .env.example
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
├── README.md
├── USAGE.md
├── quickstart.md
└── pyproject.toml
```

### Adding a new subcommand

1. Create `src/pdf_autofillr_cli/cmd_mymodule.py` with `add_parser(subparsers)` and `run(args) -> int`
2. Import and register it in `main.py` alongside the existing commands
3. Add tests under `tests/unit/` and `tests/integration/`

### Run tests

```bash
pip install -e ".[dev]"

# All tests
pytest tests/ -v

# Unit only (no modules needed — everything mocked)
pytest tests/unit/ -v

# Integration only (parser wiring)
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=src/pdf_autofillr_cli --cov-report=term-missing
```

### Publish a new version

```bash
# 1. Bump version in pyproject.toml and src/pdf_autofillr_cli/__init__.py
# 2. Add entry to CHANGELOG.md
# 3. Build
pip install build
python -m build
# 4. Upload
pip install twine
twine upload dist/*
```

---

## Related packages

| Package | PyPI | Description |
|---|---|---|
| `pdf-autofillr` | [![PyPI](https://img.shields.io/pypi/v/pdf-autofillr)](https://pypi.org/project/pdf-autofillr/) | Umbrella package |
| `pdf-autofillr-rag` | [![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-rag)](https://pypi.org/project/pdf-autofillr-rag/) | RAG prediction engine |
| `pdf-autofillr-chatbot` | [![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-chatbot)](https://pypi.org/project/pdf-autofillr-chatbot/) | Conversational onboarding |
| `pdf-autofillr-mapper` | [![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-mapper)](https://pypi.org/project/pdf-autofillr-mapper/) | Semantic PDF field mapper |
| `pdf-autofillr-doc-upload` | [![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-doc-upload)](https://pypi.org/project/pdf-autofillr-doc-upload/) | Document extraction |
| `pdf-autofillr-plugins` | [![PyPI](https://img.shields.io/pypi/v/pdf-autofillr-plugins)](https://pypi.org/project/pdf-autofillr-plugins/) | Plugin framework |

---

## License

MIT — see [LICENSE](LICENSE).
