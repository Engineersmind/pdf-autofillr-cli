"""
pdf-autofillr-cli run <pdf> --schema form_keys.json --data data.json

Full pipeline: extract fields, map with LLM, embed, then fill — all in one command.
Use this the first time you process a template.

Example:
    pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json
    pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json --output filled.pdf
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import tempfile


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "run",
        help="Full pipeline: embed + fill in one shot",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("pdf", help="Path to blank PDF form")
    p.add_argument("--schema", "-s", required=True, help="Path to form_keys.json")
    p.add_argument("--data", "-d", required=True, help="JSON file path or inline JSON string")
    p.add_argument("--output", "-o", default=None, help="Output path (default: <name>_filled.pdf)")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    try:
        from pdf_autofillr_mapper import MapperConfig, PDFPipeline  # type: ignore
    except ImportError:
        print("\n  pdf-autofillr-mapper is not installed.")
        print('  Install it with:  pip install "pdf-autofillr[mapper]"\n')
        return 1

    if not os.path.exists(args.pdf):
        print(f"\n  ✗  PDF not found: {args.pdf}\n")
        return 1
    if not os.path.exists(args.schema):
        print(f"\n  ✗  Schema not found: {args.schema}")
        print("  Run: pdf-autofillr-cli setup  to create configs/\n")
        return 1

    # Resolve data
    data_path = _resolve_data(args.data)
    if data_path is None:
        return 1

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)

    print(f"\n  Running full pipeline on {args.pdf}...")
    print("  Step 1/4  Extracting fields...")
    print("  Step 2/4  Mapping with LLM...")
    print("  Step 3/4  Embedding metadata...")
    print("  Step 4/4  Filling PDF...\n")

    result = asyncio.run(
        pipeline.run_all(
            input_pdf_path=args.pdf,
            input_data_path=data_path,
            output_path=args.output,
            keep_intermediates=True,
        )
    )

    timing = result.get("timing", {})
    total = timing.get("total_pipeline_seconds", "?")
    print(f"  ✅  Done in {total}s: {result['final_output']}\n")
    return 0


def _resolve_data(data: str) -> str | None:
    if os.path.exists(data):
        return data
    try:
        parsed = json.loads(data)
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(parsed, tmp)
        tmp.close()
        # Note: caller is responsible for cleanup — file persists for duration of process
        return tmp.name
    except json.JSONDecodeError as e:
        print("\n  ✗  Invalid data: not a file path and not valid JSON")
        print(f"     {e}\n")
        return None
