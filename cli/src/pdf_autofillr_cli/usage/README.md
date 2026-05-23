# pdf-autofillr-cli — Usage Guides

One file per command. Each shows exactly what files you need, where to place them, and minimum env vars.

| Command | Guide |
|---------|-------|
| `embed` | [embed.md](embed.md) |
| `fill` | [fill.md](fill.md) |
| `run` | [run.md](run.md) |
| `batch` | [batch.md](batch.md) |
| `chatbot` | [chatbot.md](chatbot.md) |
| `doc-upload` | [doc-upload.md](doc-upload.md) |
| `mapper` | [mapper.md](mapper.md) |
| `rag` | [rag.md](rag.md) |
| `plugins` | [plugins.md](plugins.md) |

---

## Typical workflow

```
1. pdf-autofillr-cli setup          → creates configs/ and .env
2. Edit .env                        → add your API key
3. pdf-autofillr-cli status         → verify everything is ready
4. pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json
```
