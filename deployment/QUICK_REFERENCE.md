# Quick Reference — pdf-autofillr-cli

```bash
# Install
pip install "pdf-autofillr-cli[all]"

# Setup
pdf-autofillr setup

# Status
pdf-autofillr status

# RAG
pdf-autofillr rag init-vectors
pdf-autofillr rag predict --user u1 --session s1 --pdf p1 --fields f.json --hash abc

# Chatbot
pdf-autofillr chatbot start

# Mapper
pdf-autofillr mapper embed --pdf blank.pdf --user u1 --id lp_v1
pdf-autofillr mapper fill  --pdf blank.pdf --user u1 --id lp_v1 --data data.json

# Doc Upload
pdf-autofillr doc-upload process --doc investor.pdf --pdf blank.pdf --schema form_keys.json --user u1 --id lp_v1

# Plugins
pdf-autofillr plugins list
pdf-autofillr plugins info email-validator

# Build & publish
make build && make publish
```
