# pdf-autofillr-cli embed

Embed field metadata into a blank PDF template.
Run this **once per template** — creates an embedded PDF ready for filling.

---

## Files you need

```
your-project/
├── form.pdf                    ← your blank PDF form (required)
├── configs/
│   └── form_keys.json          ← your field schema (required)
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
pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json
```

## Output

Creates `form_embedded.pdf` next to your `form.pdf`.

```
your-project/
├── form.pdf
├── form_embedded.pdf           ← created by embed
```

---

## form_keys.json format

```json
{
  "first_name": "First name of the investor",
  "last_name": "Last name of the investor",
  "date_of_birth": "Date of birth (YYYY-MM-DD)",
  "ssn": "Social security number",
  "investment_amount": "Total investment amount in USD"
}
```

Keys are the field identifiers. Values are descriptions that help the LLM map them.
