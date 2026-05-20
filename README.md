[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-pdffillr.ai-blue)](https://pdffillr.ai)

<div align="center">

# pdf-autofillr CLI

**Fill PDF forms from your terminal using any LLM — batch processing, scriptable, CI-friendly.**

[**Quick Start**](#quick-start) · [**Python SDK**](https://github.com/EngineersMind/pdf-autofillr-python-sdk) · [**Node.js SDK**](https://github.com/EngineersMind/pdf-autofillr-node-sdk) · [**Live Platform**](https://pdffillr.ai)

</div>

---

> **Status:** Under active development. For production use today, see the [Python SDK](https://github.com/EngineersMind/pdf-autofillr-python-sdk) or the [live platform at pdffillr.ai](https://pdffillr.ai).
>
> **Note:** The CLI is published as standalone packages. This repository tracks design, issues, and roadmap. See installation instructions below for the published packages.

## What it does

`pdf-autofillr-cli` lets you fill PDF forms from the command line — embed field metadata into a template once, then fill it with JSON data on every run. Works with OpenAI, Anthropic, Google, and local Ollama models.

## Installation

**Python (recommended):**

```bash
pip install pdf-autofillr-cli
```

**npm:**

```bash
npm install -g @engineersmind/pdf-autofillr-cli
```

## Quick Start

```bash
# Step 1: Embed metadata into a PDF template (run once per template)
pdf-autofillr embed form.pdf --keys first_name last_name dob --output form.embedded.pdf

# Step 2: Fill a template with JSON data
pdf-autofillr fill form.embedded.pdf --data data.json --output filled.pdf

# Step 3: Run the full pipeline in one shot
pdf-autofillr run form.pdf --data data.json --output filled.pdf
```

## Batch Processing

```bash
# Fill multiple PDFs from a directory of JSON files
pdf-autofillr batch --template form.embedded.pdf --input data/ --output output/

# Use a specific LLM model
pdf-autofillr embed form.pdf --keys name email --model claude-3-5-haiku-latest
```

## Supported LLMs

| Provider | Model examples |
|----------|---------------|
| OpenAI | `gpt-4o`, `gpt-4o-mini` |
| Anthropic | `claude-3-5-haiku-latest`, `claude-3-5-sonnet-latest` |
| Google | `gemini-1.5-flash`, `gemini-1.5-pro` |
| Ollama (local) | `llama3.1`, `mistral`, `phi3` |

## Configuration

```bash
# Set API key via environment variable
export PDF_AUTOFILLR_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here  # or ANTHROPIC_API_KEY, etc.

# Or persist via config command
pdf-autofillr config --api-key your_key
```

## All Commands

| Command | Description |
|---------|-------------|
| `embed` | Extract and embed field metadata into a PDF template |
| `fill` | Fill an embedded PDF template with JSON data |
| `run` | Full pipeline: embed + fill in one command |
| `batch` | Fill multiple PDFs from a data directory |
| `status` | Check configuration and connectivity |
| `config` | Set API keys and default options |

## Related

| Package | Description |
|---------|-------------|
| [pdf-autofillr-python-sdk](https://github.com/EngineersMind/pdf-autofillr-python-sdk) | Python library for programmatic use |
| [pdf-autofillr-node-sdk](https://github.com/EngineersMind/pdf-autofillr-node-sdk) | Node.js/TypeScript SDK |
| [pdf-autofillr-plugins](https://github.com/EngineersMind/pdf-autofillr-plugins) | Custom extractors and LLM adapters |

## Contributing

Open an [issue](https://github.com/EngineersMind/pdf-autofillr-cli/issues) to report a bug or suggest a feature.

## License

MIT — see [LICENSE](LICENSE)
