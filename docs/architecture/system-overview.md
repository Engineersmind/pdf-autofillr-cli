# System Overview — pdf-autofillr-cli

```
pdf-autofillr (CLI entry point)
│
├── cmd_status.py       → pdf-autofillr status
├── cmd_setup.py        → pdf-autofillr setup
├── cmd_rag.py          → pdf-autofillr rag *
│     └── ragpdf (pdf-autofillr-rag)
├── cmd_chatbot.py      → pdf-autofillr chatbot *
│     └── chatbot (pdf-autofillr-chatbot)
├── cmd_mapper.py       → pdf-autofillr mapper *
│     └── pdf_autofillr_mapper (pdf-autofillr-mapper)
├── cmd_doc_upload.py   → pdf-autofillr doc-upload *
│     └── pdf_autofillr_doc_upload (pdf-autofillr-doc-upload)
└── cmd_plugins.py      → pdf-autofillr plugins *
      └── pdf_autofillr_plugins (pdf-autofillr-plugins)
```

All module imports are lazy — the CLI loads instantly even if
only some modules are installed.
