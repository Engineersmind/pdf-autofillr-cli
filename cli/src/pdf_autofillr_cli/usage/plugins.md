# pdf-autofillr-cli plugins

Inspect installed pdf-autofillr plugins.

---

## Files you need

Just the plugin package installed:

```bash
pip install pdf-autofillr-plugins
pip install my-custom-plugin     # any plugin package
```

---

## No .env required

Plugins don't need API keys to inspect.

---

## Commands

```bash
# List all discovered plugins
pdf-autofillr-cli plugins list

# Filter by category
pdf-autofillr-cli plugins list --category extractor
pdf-autofillr-cli plugins list --category validator
pdf-autofillr-cli plugins list --category mapper

# Scan a specific directory for plugins
pdf-autofillr-cli plugins list --path ./my_plugins/

# Output as JSON (for scripting)
pdf-autofillr-cli plugins list --json

# Show detailed info for one plugin
pdf-autofillr-cli plugins info my-plugin-name
pdf-autofillr-cli plugins info invoice-extractor --category extractor
```

## Plugin categories

| Category | Description |
|----------|-------------|
| `extractor` | Custom PDF field extractors |
| `mapper` | Custom field mapping strategies |
| `validator` | Field value validators |
| `filler` | Custom PDF fillers |
| `transformer` | Data transformers |
| `chunker` | Custom chunking strategies |
| `embedder` | Custom embedding strategies |
