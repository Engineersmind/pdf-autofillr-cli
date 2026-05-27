"""
pdf-autofillr-cli extract <pdf> --output schema.json

Extract field metadata from a PDF form and write it as a JSON schema.
Use the output as the --schema argument for embed, run, and batch.

Example:
    pdf-autofillr-cli extract form.pdf
    pdf-autofillr-cli extract form.pdf --output configs/form_keys.json
    pdf-autofillr-cli extract form.pdf --output schema.json --pretty
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "extract",
        help="Extract field schema from a PDF form",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("pdf", help="Path to the PDF form to inspect")
    p.add_argument(
        "--output",
        "-o",
        default=None,
        help="Where to write the schema JSON (default: <name>_schema.json)",
    )
    p.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output (indent=2)",
    )
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

    # Resolve output path
    out_path = args.output or _default_output(args.pdf)

    # Ensure output directory exists
    out_dir = Path(out_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)

    print(f"\n  Extracting fields from {args.pdf}...")

    try:
        import asyncio

        result = asyncio.run(pipeline.extract(input_pdf_path=args.pdf))
        schema = result.get("fields") or result.get("schema") or result
    except Exception as e:
        print(f"\n  ✗  Extraction failed: {e}\n")
        return 1

    indent = 2 if args.pretty else None
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=indent)

    field_count = len(schema) if isinstance(schema, (dict, list)) else "?"
    print(f"  ✅  Extracted {field_count} fields  →  {out_path}\n")
    return 0


def _default_output(pdf_path: str) -> str:
    p = Path(pdf_path)
    return str(p.parent / f"{p.stem}_schema.json")
