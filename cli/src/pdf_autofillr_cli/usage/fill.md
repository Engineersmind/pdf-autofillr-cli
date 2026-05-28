# pdf-autofillr-cli fill

Fill an already-embedded PDF template with JSON data.
Run `embed` first — then use `fill` as many times as you want.

---

## Files you need

```
your-project/
├── form.pdf                    ← your blank PDF form
├── form_embedded.pdf           ← created by: pdf-autofillr-cli embed
├── data.json                   ← your investor/user data (required)
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
# Fill using a JSON file
pdf-autofillr-cli fill form.pdf --data data.json

# Fill using inline JSON
pdf-autofillr-cli fill form.pdf --data '{"first_name": "Jane", "last_name": "Doe"}'

# Specify output path
pdf-autofillr-cli fill form.pdf --data data.json --output output/filled.pdf
```

## Output

Creates `form_filled.pdf` next to your `form.pdf` (or at `--output` path).

---

## data.json format

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "ssn": "123-45-6789",
  "investment_amount": "500000"
}
```

Keys must match the keys in your `form_keys.json` used during `embed`.
