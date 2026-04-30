# Contributing to pdf-autofillr-cli

## Setup

```bash
git clone https://github.com/Engineersmind/pdf-autofillr-cli.git
cd pdf-autofillr-cli

cd packages/cli
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env    # add your API keys
```

## Tests

```bash
# All tests (unit + integration)
pytest tests/ -v

# Unit only (no modules needed — everything mocked)
pytest tests/unit/ -v

# Integration only (parser wiring)
pytest tests/integration/ -v

# With coverage
pytest tests/ --cov=src/pdf_autofillr_cli --cov-report=term-missing
```

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Stable — never push directly |
| `dev` | All PRs merge here |
| `feature/<name>` | Feature work |
| `fix/<name>` | Bug fixes |

## PR checklist

- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `pytest tests/` passes (all 69 tests)
- [ ] New commands have tests in both `tests/unit/` and `tests/integration/`
- [ ] `.env.example` updated if new env vars referenced
- [ ] `CHANGELOG.md` entry added under `## Unreleased`
- [ ] `USAGE.md` updated if new flags or commands added

## Adding a new subcommand

1. Create `packages/cli/src/pdf_autofillr_cli/cmd_mymodule.py`
   - Must define `add_parser(subparsers)` and `run(args) -> int`
2. Import and register it in `packages/cli/src/pdf_autofillr_cli/main.py`
3. Add unit tests in `packages/cli/tests/unit/`
4. Add integration (parser) tests in `packages/cli/tests/integration/test_parser_integration.py`
5. Document the new command in `packages/cli/USAGE.md` and `packages/cli/README.md`

## Releasing to PyPI

1. Bump `version` in `packages/cli/pyproject.toml` and `packages/cli/src/pdf_autofillr_cli/__init__.py`
2. Add entry to `packages/cli/CHANGELOG.md`
3. Add entry to root `CHANGELOG.md`
4. Merge to `main`
5. Push version tag — CI publishes to PyPI automatically

```bash
git tag cli-v0.2.0 && git push origin cli-v0.2.0
```

| Tag | PyPI package |
|-----|-------------|
| `cli-v0.1.0` | pdf-autofillr-cli |
