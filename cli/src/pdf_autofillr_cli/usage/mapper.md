# pdf-autofillr-cli mapper

Low-level mapper commands — embed and fill PDF forms directly.
For most users, use `embed`, `fill`, or `run` instead.

---

## Files you need

```
your-project/
├── form.pdf                    ← your blank PDF form (required)
├── configs/
│   └── form_keys.json          ← field schema (required)
│   └── mapper_config.ini       ← auto-created by: pdf-autofillr-cli setup
├── data.json                   ← user data for filling
└── .env                        ← API key (required)
```

---

## Minimum .env

```env
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# Noise suppression
MAPPER_LOG_LEVEL=ERROR
LITELLM_LOG=ERROR
```

---

## Commands

```bash
# Step 1: Embed a blank PDF template (once per form)
pdf-autofillr-cli mapper embed \
  --pdf form.pdf \
  --schema configs/form_keys.json

# Step 2: Fill with data
pdf-autofillr-cli mapper fill \
  --pdf form.pdf \
  --data data.json

# Fill with inline JSON
pdf-autofillr-cli mapper fill \
  --pdf form.pdf \
  --data '{"investor_name": "Jane Smith", "commitment_amount": "500000"}'

# Start the mapper API server
pdf-autofillr-cli mapper start
pdf-autofillr-cli mapper start --port 8001 --reload
```
