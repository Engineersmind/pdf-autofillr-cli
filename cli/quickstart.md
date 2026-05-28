# pdf-autofillr-cli — Quick Start

Get up and running in 5 minutes.

---

## 1. Install

```bash
pip install pdf-autofillr-cli
```

---

## 2. First-time setup

```bash
pdf-autofillr-cli setup
```

This creates `configs/` (with mapper config) and `.env` in your current directory.

---

## 3. Add your API key

Open `.env` and set your LLM key:

```env
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 4. Verify everything is ready

```bash
pdf-autofillr-cli status
```

---

## 5. Fill a PDF

```bash
# Embed your blank template once
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json

# Fill it with data
pdf-autofillr-cli fill form.pdf --data data.json

# Or do both in one command
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json
```

---

## Batch fill

```bash
pdf-autofillr-cli batch \
  --template form.pdf \
  --schema configs/form_keys.json \
  --input data/ \
  --output output/
```

---

## All commands at a glance

```
pdf-autofillr-cli --help

pdf-autofillr-cli setup
pdf-autofillr-cli status

pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json
pdf-autofillr-cli fill  form.pdf --data data.json
pdf-autofillr-cli run   form.pdf --schema configs/form_keys.json --data data.json
pdf-autofillr-cli batch --template form.pdf --schema configs/form_keys.json --input data/ --output output/

pdf-autofillr-cli chatbot session --pdf form.pdf --user u1
pdf-autofillr-cli doc-upload process --doc investor.pdf --pdf form.pdf --schema configs/form_keys.json --user u1 --id lp_v1
pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json
pdf-autofillr-cli rag init-vectors
pdf-autofillr-cli plugins list
```

→ Full reference: [USAGE.md](USAGE.md)
