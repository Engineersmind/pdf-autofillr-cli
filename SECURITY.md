# Security Policy

## Supported Versions

| Package | Version | Supported |
|---------|---------|-----------|
| pdf-autofillr-cli | 0.2.0 | ✅ |
| Any previous version | < latest | ❌ |

---

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**
Public issues expose users to 0-days before a fix is available.

### Preferred — GitHub Security Advisories (private)

<https://github.com/Engineersmind/pdf-autofillr-cli/security/advisories/new>

GitHub keeps this completely private until a fix is released.

### Alternative — Email

**security@engineersmind.com**
Subject: `[SECURITY] <brief description>`

---

## Response Timeline

| Severity | First Response | Patch Target |
|----------|---------------|--------------|
| Critical | 24 hours | 7 days |
| High | 48 hours | 14 days |
| Medium / Low | 5 business days | Next release |

We follow coordinated disclosure — we'll work with you on timing before anything is made public.

---

## Scope

Areas most relevant for security research in this codebase:

- **File path handling** — `--pdf`, `--doc`, `--schema`, `--data` flags accept user-supplied paths
- **Subprocess execution** — mapper and chatbot commands invoke underlying module CLIs
- **JSON parsing** — inline JSON accepted via `--data` and `--category` flags
- **API key exposure** — `.env` handling passed through to underlying modules
- **Module import chain** — lazy imports could be abused if a malicious package shadows a module name

---

## Security Best Practices (for contributors)

```bash
# Never commit .env — always use .env.example
cp cli/.env.example .env
echo ".env" >> .gitignore

# Scan dependencies for known CVEs
pip-audit

# Static analysis
bandit -r cli/src/
```

- Never log API keys or raw user input
- Always validate file paths before passing to subprocesses
- `.env` files are in `.gitignore` and must never be committed

---

## After Reporting

Once a vulnerability is confirmed:

1. We open a private GitHub Security Advisory
2. We develop and test a fix on a private branch
3. We coordinate a disclosure date with the reporter
4. We release the patch and publish the advisory simultaneously
5. Reporter is credited in the advisory (unless they prefer anonymity)