"""
pdf-autofillr-cli fill <pdf> --data data.json

Fill an already-embedded PDF template with JSON data.
The PDF must have been embedded first (run `pdf-autofillr-cli embed` once).

Example:
    pdf-autofillr-cli fill form.pdf --data data.json
    pdf-autofillr-cli fill form.pdf --data data.json --output filled.pdf
    pdf-autofillr-cli fill form.pdf --data '{"first_name": "Jane", "last_name": "Doe"}'
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "fill",
        help="Fill an embedded PDF with JSON data",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("pdf", help="Path to blank PDF form")
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

    # Resolve data — file path or inline JSON written to a temp file
    data_path = _resolve_data(args.data)
    if data_path is None:
        return 1

    # Find embedded pdf — look for <name>_embedded.pdf next to the source pdf
    embedded_pdf = _find_embedded(args.pdf)
    if not embedded_pdf:
        print(f"\n  ✗  No embedded PDF found for {args.pdf}")
        print("  Run first:  pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json\n")
        return 1

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)

    print(f"\n  Filling {embedded_pdf}...")
    result = asyncio.run(
        pipeline.fill(
            embedded_pdf_path=embedded_pdf,
            input_data_path=data_path,
            output_path=args.output,
        )
    )

    print(f"  ✅  Filled PDF: {result['output_file']}\n")
    return 0


def _find_embedded(pdf_path: str) -> str | None:
    """Look for <name>_embedded.pdf next to the source PDF."""
    p = Path(pdf_path)
    candidate = p.parent / f"{p.stem}_embedded.pdf"
    if candidate.exists():
        return str(candidate)
    return None


def _resolve_data(data: str) -> str | None:
    """Return a file path to the JSON data — handle file or inline JSON."""
    import tempfile

    if os.path.exists(data):
        return data
    # Try parsing as inline JSON and write to temp file
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
