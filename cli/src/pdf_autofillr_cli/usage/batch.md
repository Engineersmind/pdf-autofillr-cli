# pdf-autofillr-cli batch

Fill multiple PDFs from a directory of JSON files.
Embeds the template once, then fills one PDF per JSON file.

---

## Files you need

```
your-project/
├── form.pdf                    ← your blank PDF form (required)
├── configs/
│   └── form_keys.json          ← your field schema (required)
├── data/
│   ├── investor_001.json       ← one JSON file per person
│   ├── investor_002.json
│   └── investor_003.json
├── output/                     ← will be created automatically
└── .env                        ← API key (required)
```

---

## Minimum .env

```env
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Command

```bash
pdf-autofillr-cli batch \
  --template form.pdf \
  --schema configs/form_keys.json \
  --input data/ \
  --output output/
```

## What happens

```
Batch: 3 files  →  output/

Embedding template (once)...
✅  Embedded: form_embedded.pdf

✅  investor_001.json  →  output/investor_001_filled.pdf
✅  investor_002.json  →  output/investor_002_filled.pdf
✅  investor_003.json  →  output/investor_003_filled.pdf

Done: 3 filled, 0 failed
```

## Output

```
output/
├── investor_001_filled.pdf
├── investor_002_filled.pdf
└── investor_003_filled.pdf
```

Each JSON file produces one filled PDF named `<filename>_filled.pdf`.
