# Contributing to pdf-autofillr-cli

Thank you for your interest in contributing. This document covers everything you need to open a great pull request.

---

## Important Rules

- Never push directly to `main`
- All changes must go through Pull Requests
- Every contribution must start from a dedicated branch
- Commit messages must follow the convention below

---

## 1. Setup

```bash
git clone https://github.com/Engineersmind/pdf-autofillr-cli.git
cd pdf-autofillr-cli/cli

python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env    # add your API keys
```

---

## 2. Branch Naming Convention

**Format:**

```
<type>/<module>-<short-description>
```

**Examples:**

```
feature/cli-add-batch-command
fix/cli-status-crash
docs/cli-update-usage-guide
test/cli-rag-command-tests
chore/cli-update-gitignore
```

**Allowed types:**

| Type | Use for |
|------|---------|
| `feature` | New functionality |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `chore` | Maintenance, config, tooling |
| `perf` | Performance improvements |
| `bug` | Reporting/fixing a confirmed bug |

```bash
git checkout main
git pull origin main
git checkout -b feature/cli-add-batch-command
```

---

## 3. Commit Convention

**Format:**

```
<type>/<module>: short description
```

**Examples:**

```bash
git commit -m "feature/cli: add batch fill command"
git commit -m "fix/cli: handle missing module gracefully"
git commit -m "docs/cli: update usage guide"
git commit -m "test/cli: add rag command edge case tests"
git commit -m "chore/cli: update .gitignore"
```

**Allowed types:** `feature/` · `fix/` · `bug/` · `docs/` · `test/` · `chore/` · `perf/`

Any other format will be rejected by CI.

---

## 4. Running Tests

```bash
cd cli
pytest tests/ -v --tb=short          # all 69 tests
pytest tests/unit/ -v                 # unit only (no modules needed — everything mocked)
pytest tests/integration/ -v          # parser integration only
pytest tests/ --cov=src/pdf_autofillr_cli --cov-report=term-missing  # with coverage
```

All 69 tests must pass before opening a PR.

---

## 5. PR Checklist

- [ ] Branch named correctly — `<type>/<module>-<short-description>`
- [ ] All commit messages follow `<type>/<module>: description`
- [ ] PR title follows the same format
- [ ] No direct commits to `main`
- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `pytest tests/` passes locally
- [ ] New commands have tests in both `tests/unit/` and `tests/integration/`
- [ ] `.env.example` updated if new env vars referenced
- [ ] `cli/CHANGELOG.md` entry added
- [ ] `cli/USAGE.md` updated if new flags or commands added
- [ ] No build artifacts, `.env`, `__pycache__`, or `.egg-info` included

---

## 6. Adding a New Subcommand

1. Create `cli/src/pdf_autofillr_cli/cmd_mymodule.py`
   - Must define `add_parser(subparsers)` and `run(args) -> int`
2. Import and register it in `cli/src/pdf_autofillr_cli/main.py`
3. Add unit tests in `cli/tests/unit/`
4. Add integration tests in `cli/tests/integration/test_parser_integration.py`
5. Document the new command in `cli/USAGE.md` and `cli/README.md`

---

## 7. Releasing to PyPI

1. Bump `version` in `cli/pyproject.toml`
2. Add entry to `cli/CHANGELOG.md`
3. Add entry to root `CHANGELOG.md`
4. Merge to `main` via PR
5. Push version tag — CI publishes to PyPI automatically

```bash
git tag cli-v0.2.1 && git push origin cli-v0.2.1
```

| Tag | PyPI package |
|-----|-------------|
| `cli-v*` | pdf-autofillr-cli |

---

## Questions?

Open an issue on the [repository](https://github.com/Engineersmind/pdf-autofillr-cli).