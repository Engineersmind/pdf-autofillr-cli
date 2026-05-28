# pdf-autofillr-cli run

Full pipeline: extract fields → map with LLM → embed → fill.
Use this the **first time** you process a template. Combines `embed` + `fill` in one shot.

---

## Files you need

```
your-project/
├── form.pdf                    ← your blank PDF form (required)
├── configs/
│   └── form_keys.json          ← your field schema (required)
├── data.json                   ← your investor/user data (required)
├── .env                        ← API key (required)
└── configs/
    └── mapper_config.ini       ← auto-created by: pdf-autofillr-cli setup
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
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json

# With custom output path
pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json --output filled.pdf
```

## What happens

```
Step 1/4  Extracting fields from PDF...
Step 2/4  Mapping fields with LLM...      ← uses your API key
Step 3/4  Embedding metadata into PDF...
Step 4/4  Filling PDF with data...
✅  Done in 12.3s: form_filled.pdf
```

## Output

Creates intermediate files + final filled PDF:

```
your-project/
├── form.pdf
├── form_extracted.json         ← extracted field data
├── form_mapped.json            ← LLM field mappings
├── form_radio.json             ← radio button groups
├── form_embedded.pdf           ← reusable for future fills
└── form_filled.pdf             ← final output
```

Tip: After the first `run`, use `fill` for subsequent fills — much faster, skips the LLM step.
