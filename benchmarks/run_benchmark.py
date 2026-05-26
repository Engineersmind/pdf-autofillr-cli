"""
pdf-autofillr-cli benchmark runner.

Runs CLI commands against test PDFs in benchmarks/datasets/
and measures latency, accuracy, and reliability.

Usage:
    python benchmarks/run_benchmark.py
    python benchmarks/run_benchmark.py --domain financial
    python benchmarks/run_benchmark.py --model benchmarks/models/claude-3-5-sonnet.yaml
"""
import argparse
import json
# import os
import subprocess
import time
from pathlib import Path

DOMAINS = ["financial", "government", "hr", "insurance", "legal", "medical"]
RESULTS_DIR = Path("benchmarks/results")


def run_cli(cmd: list) -> dict:
    """Run a pdf-autofillr CLI command and capture result."""
    start = time.time()
    try:
        result = subprocess.run(
            ["pdf-autofillr"] + cmd,
            capture_output=True, text=True, timeout=60,
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_s": round(time.time() - start, 3),
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "error": "timeout", "duration_s": 60.0}


def benchmark_status():
    """Benchmark: pdf-autofillr status"""
    result = run_cli(["status"])
    return {"command": "status", **result}


def main():
    parser = argparse.ArgumentParser(description="pdf-autofillr-cli benchmarks")
    parser.add_argument("--domain", choices=DOMAINS + ["all"], default="all")
    parser.add_argument("--model", default=None, help="Model config YAML")
    parser.add_argument("--output", default=str(RESULTS_DIR / "benchmark_results.json"))
    args = parser.parse_args()

    RESULTS_DIR.mkdir(exist_ok=True)

    print(f"\npdf-autofillr-cli benchmark")
    print(f"Domain: {args.domain}")
    print(f"{'─' * 40}")

    results = []

    # Always benchmark status
    r = benchmark_status()
    results.append(r)
    status = "✅" if r["exit_code"] == 0 else "✗"
    print(f"  {status}  status  ({r['duration_s']}s)")

    # Save results
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {args.output}\n")


if __name__ == "__main__":
    main()
