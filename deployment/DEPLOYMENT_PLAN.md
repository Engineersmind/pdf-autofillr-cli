# pdf-autofillr-cli — Deployment Plan

## PyPI release

```bash
make build
make publish       # requires PYPI_API_TOKEN in env
```

## Docker

```bash
docker build -f deployment/docker/cli/Dockerfile -t pdf-autofillr-cli:latest .
docker run pdf-autofillr-cli:latest pdf-autofillr --help
```

## CI/CD

Tags matching `cli-v*` trigger the PyPI publish workflow automatically.

```bash
git tag cli-v0.3.0 && git push origin cli-v0.3.0
```
