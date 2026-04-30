# pdf-autofillr-cli — Benchmarks

Benchmarking suite for measuring CLI command performance across document domains.

## Dataset domains

| Domain | Description |
|---|---|
| `financial` | LP subscription agreements, fund documents |
| `government` | Government forms, regulatory filings |
| `hr` | HR onboarding, employee forms |
| `insurance` | Insurance applications, claims |
| `legal` | Legal agreements, contracts |
| `medical` | Medical intake, patient forms |

Each domain contains:
- `pdfs/` — test PDF files (add your own)
- `ground_truth/` — expected extraction results
- `schema_keys/` — field schema definitions

## Running benchmarks

```bash
# Run all CLI benchmarks
python benchmarks/run_benchmark.py

# Run for a specific domain
python benchmarks/run_benchmark.py --domain financial

# Run with a specific model config
python benchmarks/run_benchmark.py --model benchmarks/models/claude-3-5-sonnet.yaml
```

## Results

Results are written to `benchmarks/results/` (gitignored).
