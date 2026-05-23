# pdf-autofillr-cli doc-upload

Extract structured data from a document (PDF, DOCX, XLSX, CSV, JSON, TXT) and fill a PDF form.

---

## Files you need

```
your-project/
├── investor.pdf                ← source document to extract from (required)
├── form.pdf                    ← blank PDF form to fill (required)
├── configs/
│   └── form_keys.json          ← field schema (required)
└── .env                        ← API key (required)
```

---

## Minimum .env

```env
OPENAI_API_KEY=sk-...
# or
DOC_UPLOAD_LLM_API_KEY=sk-...

# Noise suppression (recommended)
LITELLM_LOG=ERROR
MAPPER_LOG_LEVEL=ERROR
```

---

## Command

```bash
pdf-autofillr-cli doc-upload process \
  --doc investor.pdf \
  --pdf form.pdf \
  --schema configs/form_keys.json \
  --user u1 \
  --id lp_sub_v1
```

## Supported source formats

| Format | Example |
|--------|---------|
| PDF | `investor.pdf` |
| Word | `investor.docx` |
| Excel | `data.xlsx` |
| CSV | `data.csv` |
| JSON | `data.json` |
| Text | `notes.txt` |
| Markdown | `profile.md` |

## Output

```
Extracted fields: 24
Success: True
Filled PDF: data/doc_upload/u1/lp_sub_v1_filled.pdf
```

## Start the API server

```bash
pdf-autofillr-cli doc-upload start
pdf-autofillr-cli doc-upload start --port 8002
```
