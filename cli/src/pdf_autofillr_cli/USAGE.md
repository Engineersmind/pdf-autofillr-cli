# pdf-autofillr-cli CLI — Usage Guide

## Install

```bash
pip install pdf-autofillr-cli
cp .env.example .env   # add your API key
```

---

## Quick Start

```bash
# Step 0: First time only — creates configs/ and .env
pdf-autofillr-cli setup

# Step 1: Embed field metadata into your blank PDF (run once per template)
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json

# Step 2: Fill it with data
pdf-autofillr-cli fill form.pdf --data data.json --output filled.pdf

# Or do both in one shot
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json --output filled.pdf
```

---

## All Commands

### embed — prepare a template

```bash
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json --output form.embedded.pdf
```

### fill — fill a prepared template

```bash
pdf-autofillr-cli fill form.pdf --data data.json
pdf-autofillr-cli fill form.pdf --data '{"first_name": "Jane", "last_name": "Doe"}'
pdf-autofillr-cli fill form.pdf --data data.json --output output/filled.pdf
```

### run — embed + fill in one command

```bash
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json --output filled.pdf
```

### batch — fill many PDFs at once

```bash
# Folder of JSON files → folder of filled PDFs
pdf-autofillr-cli batch --template form.pdf --schema configs/form_keys.json --input data/ --output output/
```

### chatbot — conversational form filling

```bash
pdf-autofillr-cli chatbot session --pdf form.pdf --user u1
pdf-autofillr-cli chatbot start --port 8000
```

### doc-upload — extract from a document and fill

```bash
pdf-autofillr-cli doc-upload process \
  --doc investor.pdf \
  --pdf blank_form.pdf \
  --schema configs/form_keys.json \
  --user u1 --id lp_sub_v1
```

### mapper — low-level mapper control

```bash
pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json
pdf-autofillr-cli mapper fill  --pdf form.pdf --data data.json
pdf-autofillr-cli mapper start --port 8001
```

### rag — field prediction

```bash
pdf-autofillr-cli rag init-vectors
pdf-autofillr-cli rag predict --user u1 --session s1 --pdf p1 --fields fields.json --hash abc
pdf-autofillr-cli rag metrics --type global
pdf-autofillr-cli rag system-info
```

### plugins — inspect installed plugins

```bash
pdf-autofillr-cli plugins list
pdf-autofillr-cli plugins list --json
pdf-autofillr-cli plugins info my-plugin
```

### setup — first-time setup

```bash
pdf-autofillr-cli setup
```

### status — check what's installed

```bash
pdf-autofillr-cli status
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

Set the API key for whichever provider you use in `.env`:

| Provider | Env var |
|----------|---------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Ollama (local) | no key needed |
