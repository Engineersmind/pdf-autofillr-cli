# PyPI Release Guide

Step-by-step instructions for publishing `pdf-autofillr-cli` to PyPI.

---

## First-time setup

### 1. Create a PyPI account

Go to https://pypi.org/account/register/ and create an account.

Verify your email before continuing.

### 2. Enable 2FA (required by PyPI since 2024)

Go to https://pypi.org/manage/account/ and enable two-factor authentication.

### 3. Create an API token

Go to https://pypi.org/manage/account/token/

- Token name: `pdf-autofillr-cli-publish`
- Scope: **Entire account** for first upload, then switch to project-scoped after first release
- Click **Add token** and copy it immediately — you won't see it again

### 4. Store the token

**Option A — `.pypirc` file (local machine)**

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

```bash
chmod 600 ~/.pypirc
```

**Option B — Environment variable**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-TOKEN-HERE
```

**Option C — GitHub Actions secret (for CI)**

Go to your repo → Settings → Secrets and variables → Actions → New repository secret

- Name: `PYPI_API_TOKEN`
- Value: `pypi-YOUR-TOKEN-HERE`

---

## Releasing a new version

### Step 1 — Bump the version

Edit **both** of these files and change the version number:

```
packages/cli/pyproject.toml
    version = "0.1.0"  →  "0.2.2"

packages/cli/src/pdf_autofillr_cli/__init__.py
    __version__ = "0.1.0"  →  "0.2.2"
```

Version format follows [Semantic Versioning](https://semver.org/):
- `MAJOR` — breaking changes
- `MINOR` — new commands or features, backwards compatible
- `PATCH` — bug fixes only

### Step 2 — Update CHANGELOG.md

Add an entry under `## [Unreleased]` in `packages/cli/CHANGELOG.md` and the root `CHANGELOG.md`:

```markdown
## [0.2.2] - 2026-05-15

### Added
- `pdf-autofillr doctor` command — extended diagnostics

### Fixed
- `rag metrics` no longer crashes when no vectors exist
```

### Step 3 — Run tests

```bash
cd packages/cli
pip install -e ".[dev]"
pytest tests/ -v
```

All 69 tests must pass before releasing.

### Step 4 — Build the distribution

```bash
cd packages/cli

# Install build tools if not already installed
pip install build twine

# Build source distribution + wheel
python -m build
```

This creates:
```
packages/cli/dist/
├── pdf_autofillr_cli-0.2.2.tar.gz      ← source distribution
└── pdf_autofillr_cli-0.2.2-py3-none-any.whl  ← wheel
```

### Step 5 — Check the distribution

```bash
twine check packages/cli/dist/*
```

Fix any warnings before uploading.

### Step 6 — Upload to PyPI

```bash
twine upload packages/cli/dist/*
```

If using `.pypirc` this will upload automatically.
If prompted: username is `__token__`, password is your API token.

### Step 7 — Verify on PyPI

```bash
# Wait ~60 seconds then install from PyPI to verify
pip install "pdf-autofillr-cli==0.2.2" --force-reinstall
pdf-autofillr --version
```

Check the PyPI page: https://pypi.org/project/pdf-autofillr-cli/

### Step 8 — Tag the release

```bash
git add packages/cli/pyproject.toml packages/cli/src/pdf_autofillr_cli/__init__.py
git add packages/cli/CHANGELOG.md CHANGELOG.md
git commit -m "release: pdf-autofillr-cli v0.2.2"
git tag cli-v0.2.2
git push origin main --tags
```

---

## Automated release via GitHub Actions

After the first manual release, all future releases can be done by just pushing a tag.
The workflow at `.github/workflows/publish-pypi.yml` handles the rest.

```bash
# 1. Bump version + update CHANGELOG + commit
git commit -m "release: pdf-autofillr-cli v0.2.2"

# 2. Tag and push — CI does the rest
git tag cli-v0.2.2
git push origin main --tags
```

The workflow triggers on tags matching `cli-v*`, builds the package, and publishes to PyPI automatically using the `PYPI_API_TOKEN` secret.

---

## Test PyPI (optional — for testing the release process)

Before publishing to the real PyPI, you can test on https://test.pypi.org/

```bash
# Upload to Test PyPI
twine upload --repository testpypi packages/cli/dist/*

# Install from Test PyPI to verify
pip install --index-url https://test.pypi.org/simple/ pdf-autofillr-cli
```

---

## Version history

| Version | Date | PyPI |
|---------|------|------|
| 0.2.2 | 2026-04-30 | https://pypi.org/project/pdf-autofillr-cli/0.2.2/ |

---

## Troubleshooting

**`Invalid distribution` error from twine check**

The long description (README.md) has invalid RST/Markdown. Run:
```bash
pip install readme-renderer
twine check dist/* --strict
```

**`File already exists` error from PyPI**

PyPI does not allow re-uploading the same version. Bump the version number and rebuild.

**`403 Forbidden` from twine**

Your API token is wrong or expired. Generate a new one at https://pypi.org/manage/account/token/

**Package installs but `pdf-autofillr` command not found**

The entry point wasn't registered. Make sure `pyproject.toml` has:
```toml
[project.scripts]
pdf-autofillr = "pdf_autofillr_cli.main:main"
```
Then reinstall: `pip install --force-reinstall pdf-autofillr-cli`
