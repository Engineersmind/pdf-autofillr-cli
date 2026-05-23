# pdf-autofillr-cli chatbot

Conversational PDF form-filling — collects investor data through a chat session.

---

## Files you need

```
your-project/
├── form.pdf                    ← your blank PDF form (required)
├── configs/
│   ├── form_keys_individual.json    ← field schemas per investor type
│   ├── form_keys_trust.json
│   └── mapper_config.ini
├── data/                       ← session data stored here automatically
└── .env                        ← API key (required)
```

---

## Minimum .env

```env
CHATBOT_LLM_API_KEY=sk-...      ← or OPENAI_API_KEY
CHATBOT_LLM_MODEL=openai/gpt-4o-mini

# Noise suppression (recommended)
LITELLM_LOG=ERROR
MAPPER_LOG_LEVEL=ERROR
```

---

## Commands

```bash
# Start an interactive terminal session
pdf-autofillr-cli chatbot session --pdf form.pdf --user investor_001

# Resume an existing session
pdf-autofillr-cli chatbot session --pdf form.pdf --user investor_001 --session session-id-here

# List active sessions
pdf-autofillr-cli chatbot sessions

# Start the REST API server (for web integrations)
pdf-autofillr-cli chatbot start
pdf-autofillr-cli chatbot start --port 8000 --reload
```

## Session example

```
Session: abc-123
PDF: form.pdf
Type 'exit' to quit.

You: hello
Bot: Hello! I'll help you fill out this subscription form. Are you investing as an Individual or Entity?
You: Individual
Bot: Great. What is your full legal name?
...
✅  Form complete.
```
