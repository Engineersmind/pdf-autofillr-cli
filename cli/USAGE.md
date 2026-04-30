# pdf-autofillr-cli — Complete Usage Guide

> Full reference for every command, flag, and configuration option.

---

## Table of Contents

1. [Install](#1-install)
2. [First-time setup](#2-first-time-setup)
3. [status — check your installation](#3-status)
4. [rag — RAG field prediction](#4-rag)
5. [chatbot — conversational form filling](#5-chatbot)
6. [mapper — embed and fill PDF templates](#6-mapper)
7. [doc-upload — extract from documents](#7-doc-upload)
8. [plugins — inspect plugins](#8-plugins)
9. [Configuration reference](#9-configuration-reference)
10. [Scripting and CI](#10-scripting-and-ci)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Install

```bash
pip install pdf-autofillr-cli                   # CLI only
pip install "pdf-autofillr-cli[rag]"            # + RAG module
pip install "pdf-autofillr-cli[chatbot]"        # + chatbot module
pip install "pdf-autofillr-cli[mapper]"         # + mapper module
pip install "pdf-autofillr-cli[doc-upload]"     # + doc-upload module
pip install "pdf-autofillr-cli[all]"            # + all modules
pip install "pdf-autofillr-cli[dev]"            # + dev tools (pytest, black, mypy)
```

Verify:

```bash
pdf-autofillr --version
pdf-autofillr --help
```

---

## 2. First-time setup

```bash
# Creates .env, configs/, and data/ in your current directory
pdf-autofillr setup

# Setup a specific module only
pdf-autofillr setup --module rag

# Setup in a different directory
pdf-autofillr setup --path /my/project

# Overwrite existing files
pdf-autofillr setup --force

# Then add your API keys
cp .env.example .env
# edit .env
```

---

## 3. status

Checks everything in one shot: installed modules, required files, env vars, inter-module connections.

```bash
pdf-autofillr status
pdf-autofillr status --path /my/project
```

Output example:

```
════════════════════════════════════════════════════════════════
  pdf-autofillr status
════════════════════════════════════════════════════════════════

Modules
────────────────────────────────────────────────────────────────
  ✅  chatbot        v0.2.9
  ✅  rag            v0.2.3
  ✅  mapper         v1.0.8
  ✅  doc_upload     v0.1.4
  ✅  plugins        v0.1.0

Files
────────────────────────────────────────────────────────────────
  ✅  configs/form_keys.json       (142 top-level keys)
  ✅  configs/mapper_config.ini
  ✅  .env
  ✅  data/rag/vectors/vector_database.json  (12 vectors)

Env configuration
────────────────────────────────────────────────────────────────
  chatbot   LLM: openai/gpt-4o-mini   storage: local   pdf_filler: mapper
  rag       storage: local   embeddings: sentence_transformer   vectors: local

✅  Everything looks good — you're ready to run!
```

---

## 4. rag

**Requires:** `pip install "pdf-autofillr-cli[rag]"`

### init-vectors

Generate embeddings from `vector_source.json`. Run once after setup, and again whenever you add new fields.

```bash
pdf-autofillr rag init-vectors

# With explicit options
pdf-autofillr rag init-vectors \
  --source path/to/my_vector_source.json \
  --backend sentence_transformer \
  --data-path ./data/rag \
  --batch-size 50 \
  --force
```

| Flag | Default | Description |
|---|---|---|
| `--source` | from `.env` | Path to vector source JSON |
| `--backend` | from `.env` | `openai` or `sentence_transformer` |
| `--model` | backend default | Embedding model name |
| `--data-path` | `RAGPDF_DATA_PATH` | Data folder |
| `--force` | `false` | Re-embed all, even existing |
| `--batch-size` | `50` | Vectors per API call |
| `--no-sanity-check` | `false` | Skip self-test after embedding |

### predict

Get RAG predictions for a list of PDF fields.

```bash
pdf-autofillr rag predict \
  --user user_001 \
  --session session_abc \
  --pdf lp_form_q2 \
  --fields data/rag/input/fields/lp_subscription_fields.json \
  --hash abc123def456 \
  --category data/rag/input/pdf_category.json
```

`--category` accepts a file path (recommended on Windows) or inline JSON on Linux/Mac:
```bash
--category '{"category":"Private Markets","sub_category":"PE","document_type":"LP Sub"}'
```

### feedback

Submit corrections after a user fixes wrong field mappings. Triggers re-learning.

```bash
pdf-autofillr rag feedback \
  --user user_001 \
  --session session_abc \
  --pdf lp_form_q2 \
  --errors data/rag/input/sample_errors.json
```

`errors.json` format:
```json
[
  {
    "error_type": "wrong_field_name",
    "field_name": "investor_name",
    "field_type": "text",
    "value": "John Smith",
    "feedback": "Should be full_legal_name",
    "page_number": 1,
    "corners": [[10, 20], [200, 20], [200, 40], [10, 40]]
  }
]
```

### metrics

Get accuracy and coverage metrics at any granularity.

```bash
# Global — LLM vs RAG comparison
pdf-autofillr rag metrics --type global

# Per PDF submission
pdf-autofillr rag metrics --type pdf \
  --user user_001 --session session_abc --pdf lp_form_q2

# By document category
pdf-autofillr rag metrics --type category \
  --category "Private Markets"

# By subcategory
pdf-autofillr rag metrics --type subcategory \
  --category "Private Markets" --subcategory "Private Equity"

# By document type
pdf-autofillr rag metrics --type doctype \
  --category "Private Markets" \
  --subcategory "Private Equity" \
  --doctype "LP Subscription Agreement"

# By PDF hash (all submissions of the same form template)
pdf-autofillr rag metrics --type pdf_hash --pdf-hash abc123def456
```

### system-info

Show vector DB statistics.

```bash
pdf-autofillr rag system-info
```

### error-analytics

Error breakdown with date and category filters.

```bash
pdf-autofillr rag error-analytics \
  --from 2026-01-01T00:00:00Z \
  --to   2026-12-31T23:59:59Z \
  --category "Private Markets"
```

---

## 5. chatbot

**Requires:** `pip install "pdf-autofillr-cli[chatbot]"`

### start

Start the chatbot REST API server.

```bash
pdf-autofillr chatbot start
pdf-autofillr chatbot start --port 9000
pdf-autofillr chatbot start --host 127.0.0.1 --port 8001 --reload
```

Swagger docs available at `http://localhost:{port}/docs`.

### session

Run an interactive chatbot session in the terminal.

```bash
pdf-autofillr chatbot session \
  --pdf data/input/blank_form.pdf \
  --user user_001

# Resume an existing session
pdf-autofillr chatbot session \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --session existing-session-id
```

Type your responses at the prompt. Type `exit` or `quit` to end. The bot fills the PDF automatically once all required fields are collected.

### sessions

List all active sessions.

```bash
pdf-autofillr chatbot sessions
```

---

## 6. mapper

**Requires:** `pip install "pdf-autofillr-cli[mapper]"`

Two-step workflow. Run `embed` once per blank template, then `fill` as many times as needed.

### embed

Analyse and embed a blank PDF form template. Only needed once per unique blank form.

```bash
pdf-autofillr mapper embed \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --id lp_sub_v1
```

### fill

Fill an embedded template with user data.

```bash
# From a JSON file
pdf-autofillr mapper fill \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --id lp_sub_v1 \
  --data user_data.json

# Inline JSON (Linux/Mac)
pdf-autofillr mapper fill \
  --pdf data/input/blank_form.pdf \
  --user user_001 \
  --id lp_sub_v1 \
  --data '{"investor_name": "Jane Smith", "commitment_amount": "500000", "email": "jane@example.com"}'
```

`user_data.json` format:
```json
{
  "investor_name": "Jane Smith",
  "investor_type": "Individual",
  "commitment_amount": "500000",
  "email": "jane@example.com"
}
```

### start

Start the mapper REST API server.

```bash
pdf-autofillr mapper start
pdf-autofillr mapper start --port 8002 --reload
```

---

## 7. doc-upload

**Requires:** `pip install "pdf-autofillr-cli[doc-upload]"`

### process

Extract investor/client data from an uploaded document and fill a PDF form in one step.

```bash
pdf-autofillr doc-upload process \
  --doc investor_data.pdf \
  --pdf data/input/blank_form.pdf \
  --schema configs/form_keys.json \
  --user user_001 \
  --id lp_sub_v1
```

Supported source document formats: `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.txt`, `.md`

```bash
# DOCX source
pdf-autofillr doc-upload process --doc investor.docx ...

# Excel source
pdf-autofillr doc-upload process --doc investor.xlsx ...

# CSV source
pdf-autofillr doc-upload process --doc investor.csv ...
```

### start

Start the doc-upload REST API server.

```bash
pdf-autofillr doc-upload start
pdf-autofillr doc-upload start --port 8003 --reload
```

---

## 8. plugins

**Requires:** `pip install pdf-autofillr-plugins`

### list

List all discovered plugins.

```bash
# All plugins (auto-discovers installed built-ins)
pdf-autofillr plugins list

# Filter by category
pdf-autofillr plugins list --category validator
pdf-autofillr plugins list --category extractor
pdf-autofillr plugins list --category mapper

# Scan a custom plugin directory
pdf-autofillr plugins list --path ./my_plugins/

# JSON output (useful for scripts and CI)
pdf-autofillr plugins list --json
pdf-autofillr plugins list --json --category validator | jq '.'
```

### info

Show detailed metadata for a specific plugin.

```bash
pdf-autofillr plugins info email-validator
pdf-autofillr plugins info invoice-extractor --category extractor
```

---

## 9. Configuration reference

Copy `.env.example` to `.env` and configure the sections for the modules you use.

### RAG variables

| Variable | Default | Description |
|---|---|---|
| `RAGPDF_STORAGE` | `local` | Storage backend: `local`, `s3`, `azure`, `gcs` |
| `RAGPDF_DATA_PATH` | `./data/rag` | Local data directory |
| `RAGPDF_EMBEDDING_BACKEND` | `sentence_transformer` | `sentence_transformer`, `openai`, `litellm`, `noop` |
| `RAGPDF_ST_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformer model |
| `RAGPDF_VECTOR_STORE` | `local` | `local`, `s3`, `pinecone`, `chroma`, `weaviate` |
| `RAGPDF_CORRECTOR_BACKEND` | `noop` | `noop`, `openai`, `anthropic` |
| `RAGPDF_PREDICTION_THRESHOLD` | `0.75` | Min cosine similarity for a match |
| `RAGPDF_TOP_K` | `5` | Candidate vectors returned |
| `RAGPDF_API_KEY` | `dev-key` | Auth key for the RAG server |
| `RAGPDF_SERVER_PORT` | `8000` | RAG server port |
| `OPENAI_API_KEY` | — | OpenAI key (embeddings, corrector) |
| `ANTHROPIC_API_KEY` | — | Anthropic key (corrector) |

### Chatbot variables

| Variable | Default | Description |
|---|---|---|
| `CHATBOT_LLM_MODEL` | `openai/gpt-4o-mini` | LLM for conversation |
| `chatbot_STORAGE` | `local` | Session storage: `local`, `s3` |
| `chatbot_DATA_PATH` | `./data/chatbot` | Session data directory |
| `chatbot_CONFIG_PATH` | `./configs` | Config directory |
| `chatbot_PDF_FILLER` | `none` | `none`, `mapper`, `managed` |
| `chatbot_PDF_PATH` | — | Path to blank PDF template |
| `CHATBOT_SERVER_PORT` | `8001` | Chatbot server port |

### Mapper variables

| Variable | Default | Description |
|---|---|---|
| `CLOUD_PROVIDER` | `local` | `local`, `aws`, `azure`, `gcp` |
| `RAG_ENABLED` | `false` | Enable RAG integration |
| `RAG_MODE` | `inprocess` | `inprocess` or `http` |
| `RAG_API_URL` | — | RAG server URL (when `RAG_MODE=http`) |
| `MAPPER_SERVER_PORT` | `8002` | Mapper server port |

### Doc-upload variables

| Variable | Default | Description |
|---|---|---|
| `DOC_UPLOAD_LLM_MODEL` | `openai/gpt-4.1-mini` | LLM for data extraction |
| `DOC_UPLOAD_STORAGE` | `local` | Storage: `local`, `s3` |
| `DOC_UPLOAD_PDF_FILLER` | `none` | `none`, `mapper`, `managed` |
| `DOC_UPLOAD_SERVER_PORT` | `8003` | Doc-upload server port |

---

## 10. Scripting and CI

All commands exit with code `0` on success and `1` on failure, making them safe to use in scripts and CI pipelines.

```bash
# Exit immediately if any command fails
set -e

pdf-autofillr rag init-vectors --force
pdf-autofillr rag predict \
  --user ci_user --session ci_session --pdf test_pdf \
  --fields tests/fixtures/fields.json \
  --hash abc123 \
  --category tests/fixtures/category.json \
  > /tmp/predictions.json

echo "Predictions saved to /tmp/predictions.json"
```

Use `--json` flag on `plugins list` and pipe to `jq` for machine-readable output:

```bash
pdf-autofillr plugins list --json | jq '.validator[].name'
```

---

## 11. Troubleshooting

**Module not installed error**

```
  Module 'ragpdf' is not installed.
  Install it with:  pip install pdf-autofillr-rag
```

Install the missing module and retry.

**`RAGPDF_EMBEDDING_BACKEND=noop` error on init-vectors**

The `noop` backend generates zero vectors and cannot be used for real embeddings. Set `RAGPDF_EMBEDDING_BACKEND=sentence_transformer` (local, no API key) or `openai`.

**Predictions always empty on first run**

Normal — the vector database is empty until you have processed submissions and called `save_filled_pdf()`. Run `pdf-autofillr rag system-info` to see the current vector count.

**`uvicorn` not found when starting a server**

```bash
pip install uvicorn
```

**Windows: inline JSON not working for `--category` or `--data`**

Use a file path instead:

```bash
# Create the file
echo {"category":"Finance"} > category.json

# Then use the file path
pdf-autofillr rag predict --category category.json ...
```

**Tests failing with embedding errors**

```bash
RAGPDF_EMBEDDING_BACKEND=noop RAGPDF_CORRECTOR_BACKEND=noop pytest tests/unit/ -v
```
