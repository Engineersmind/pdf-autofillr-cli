# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |

## Reporting a vulnerability

**GitHub Security Advisories (preferred):**
https://github.com/Engineersmind/pdf-autofillr-cli/security/advisories/new

**Email:** Security@pdffillr.ai
Subject: `[SECURITY] <brief description>`

We respond within 48 hours and follow coordinated disclosure.

## Security best practices

```bash
# Never commit .env — use .env.example
cp .env.example .env && echo ".env" >> .gitignore

# Scan dependencies
pip-audit

# Scan source
bandit -r packages/cli/src/
```
