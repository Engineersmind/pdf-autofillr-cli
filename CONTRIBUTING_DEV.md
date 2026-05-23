# Developer Guide — pdf-autofillr-cli

Internal reference for the Engineersmind team. Covers local setup, testing, and the release process.

---

## Repository Layout

```
pdf-autofillr-cli/
├── cli/                  → pdf-autofillr-cli package (source of truth)
│   ├── src/pdf_autofillr_cli/
│   ├── tests/
│   ├── pyproject.toml
│   └── CHANGELOG.md
├── benchmarks/           → CLI benchmarking suite (6 document domains)
├── deployment/           → Docker configs
├── docs/                 → architecture and guides
└── examples/             → usage examples
```

---

## Local Setup

```bash
git clone https://github.com/Engineersmind/pdf-autofillr-cli.git
cd pdf-autofillr-cli/cli

python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

---

## Running Tests

```bash
cd cli
pytest tests/ -v --tb=short          # all tests
pytest tests/unit/ -v                 # unit only
pytest tests/integration/ -v          # integration only
pytest tests/ --cov=src/pdf_autofillr_cli --cov-report=term-missing
```

---

## Branch Reference

| Branch | Purpose |
|--------|---------|
| `main` | Stable — never push directly |
| `feature/cli-<name>` | New commands or flags |
| `fix/cli-<name>` | Bug fixes |
| `docs/cli-<name>` | Documentation only |
| `test/cli-<name>` | Test additions |
| `chore/cli-<name>` | Maintenance / tooling |
| `perf/cli-<name>` | Performance improvements |

**Nobody pushes directly to `main`** — no exceptions for internal team.

---

## PR Checklist

- [ ] `pip install -e ".[dev]"` succeeds cleanly
- [ ] `pytest tests/` passes with no failures
- [ ] New behaviour has test coverage
- [ ] `.env.example` updated if new env vars added
- [ ] `cli/CHANGELOG.md` entry added
- [ ] Root `README.md` updated if commands or flags changed
- [ ] No build artifacts, `.env`, `__pycache__`, or `.egg-info` committed

---

## Release Process

### Steps

1. Bump `version` in `cli/pyproject.toml`
2. Add an entry to `cli/CHANGELOG.md`
3. Update the versions table in root `README.md` and root `CHANGELOG.md`
4. Merge to `main` via PR
5. Push the version tag — CI publishes to PyPI automatically

### Current versions

| Tag | PyPI package | Version |
|-----|-------------|---------|
| `cli-v*` | pdf-autofillr-cli | **0.2.0** |

### Tagging a release

```bash
git tag cli-v0.2.0 && git push origin cli-v0.2.0
```

CI will:

1. Run all tests across Python 3.9–3.12
2. Verify `pyproject.toml` version matches the tag
3. Build the wheel and sdist
4. Publish to PyPI via Trusted Publishing (OIDC)
5. Update root `CHANGELOG.md` automatically

---

## PyPI Trusted Publishing Setup

Before the first release, set up Trusted Publishing on PyPI:

1. Go to <https://pypi.org/manage/account/publishing/>
2. Add a new publisher:
   - **Owner**: `Engineersmind`
   - **Repository**: `pdf-autofillr-cli`
   - **Workflow**: `publish-pypi.yml`
   - **Environment**: `pypi`
3. On GitHub, create the `pypi` environment at:
   `https://github.com/Engineersmind/pdf-autofillr-cli/settings/environments`

---

## Adding a New `.env` Variable

1. Add it to `cli/.env.example` with a comment explaining it
2. Document it in `cli/USAGE.md` under Configuration Reference
3. Add a `cli/CHANGELOG.md` entry

---

## CHANGELOG_BOT_TOKEN Secret

The `update-changelog.yml` workflow uses `CHANGELOG_BOT_TOKEN` to push back to `main` after a release tag.

Set this up at:
`https://github.com/Engineersmind/pdf-autofillr-cli/settings/secrets/actions`

Use a fine-grained PAT with **Contents: write** permission on this repo only.