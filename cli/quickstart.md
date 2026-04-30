# pdf-autofillr-cli — Quick Start

Get up and running in 3 steps.

## Step 1 — Install

```bash
# CLI only (you need at least one module too)
pip install pdf-autofillr-cli

# CLI + everything
pip install "pdf-autofillr-cli[all]"

# CLI + specific modules
pip install "pdf-autofillr-cli[rag]"
pip install "pdf-autofillr-cli[chatbot]"
pip install "pdf-autofillr-cli[mapper]"
pip install "pdf-autofillr-cli[doc-upload]"
```

## Step 2 — Set up

```bash
# Creates .env, configs/, and data/ directories
pdf-autofillr setup

# Then edit .env and add your API keys
cp .env.example .env
# set OPENAI_API_KEY=sk-... (or ANTHROPIC_API_KEY)
```

## Step 3 — Verify and use

```bash
# See what's installed and configured
pdf-autofillr status

# RAG: generate embeddings from your vector source
pdf-autofillr rag init-vectors

# RAG: predict field mappings
pdf-autofillr rag predict \
  --user user_001 --session s1 --pdf p1 \
  --fields data/rag/input/fields/lp_subscription_fields.json \
  --hash abc123 \
  --category data/rag/input/pdf_category.json

# Chatbot: start the API server
pdf-autofillr chatbot start

# Mapper: embed a blank form (run once per template)
pdf-autofillr mapper embed \
  --pdf data/input/blank_form.pdf \
  --user user_001 --id lp_sub_v1

# Mapper: fill with user data
pdf-autofillr mapper fill \
  --pdf data/input/blank_form.pdf \
  --user user_001 --id lp_sub_v1 \
  --data '{"investor_name": "Jane Smith", "commitment_amount": "500000"}'

# Doc Upload: extract from a document and fill a PDF
pdf-autofillr doc-upload process \
  --doc investor_data.pdf \
  --pdf data/input/blank_form.pdf \
  --schema configs/form_keys.json \
  --user user_001 --id lp_sub_v1
```

## All commands

```
pdf-autofillr --help
pdf-autofillr status
pdf-autofillr setup
pdf-autofillr rag --help
pdf-autofillr chatbot --help
pdf-autofillr mapper --help
pdf-autofillr doc-upload --help
pdf-autofillr plugins --help
```

→ Full reference: [USAGE.md](USAGE.md)
