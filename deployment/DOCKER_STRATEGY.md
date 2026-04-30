# Docker Strategy — pdf-autofillr-cli

The CLI image is a lightweight wrapper. It installs `pdf-autofillr-cli[all]`
and exposes the `pdf-autofillr` entry point.

## Image

- Base: `python:3.12-slim`
- Size target: < 200MB with all modules
- Entry point: `pdf-autofillr`

## Use cases

- CI pipelines that need the CLI to run benchmarks or integration checks
- Containerised automation scripts
