# pdf-autofillr-cli rag

Self-learning RAG field prediction — improves mapping accuracy over time.

---

## Files you need

```
your-project/
├── data/
│   └── rag/
│       └── vector_source.json  ← field vectors for embedding (auto-created or custom)
└── .env                        ← API key + RAG config (required)
```

---

## Minimum .env

```env
OPENAI_API_KEY=sk-...

# RAG storage (local by default)
RAGPDF_STORAGE=local
RAGPDF_DATA_PATH=./data/rag

# Embedding backend
RAGPDF_EMBEDDING_BACKEND=sentence_transformer
RAGPDF_ST_MODEL=all-MiniLM-L6-v2

# Noise suppression
RAGPDF_LOG_LEVEL=WARNING
```

---

## Commands

```bash
# Step 1: Generate embeddings (run once after setup)
pdf-autofillr-cli rag init-vectors

# Step 2: Predict field mappings
pdf-autofillr-cli rag predict \
  --user u1 --session s1 --pdf p1 \
  --fields data/fields.json \
  --hash abc123

# Submit corrections to improve future predictions
pdf-autofillr-cli rag feedback \
  --user u1 --session s1 --pdf p1 \
  --errors data/errors.json

# View accuracy metrics
pdf-autofillr-cli rag metrics --type global
pdf-autofillr-cli rag metrics --type pdf --user u1 --session s1 --pdf p1

# Vector DB stats
pdf-autofillr-cli rag system-info

# Error analytics
pdf-autofillr-cli rag error-analytics --from 2026-01-01T00:00:00Z
```

## fields.json format

```json
[
  {"field_id": "f1", "field_name": "investor_name"},
  {"field_id": "f2", "field_name": "commitment_amount"}
]
```
