"""
pdf-autofillr-cli embed <pdf> --schema form_keys.json

Embed field metadata into a blank PDF template.
Run this once per template — creates an embedded PDF ready for filling.

Example:
    pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json
    pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json --output form.embedded.pdf
"""
from __future__ import annotations

import argparse
import asyncio
import os


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "embed",
        help="Embed field metadata into a PDF template (run once per form)",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("pdf", help="Path to blank PDF form")
    p.add_argument("--schema", "-s", required=True,
                   help="Path to form_keys.json (field schema)")
    p.add_argument("--output", "-o", default=None,
                   help="Output path (default: <name>_embedded.pdf)")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    try:
        from pdf_autofillr_mapper import PDFPipeline, MapperConfig  # type: ignore
    except ImportError:
        print("\n  pdf-autofillr-mapper is not installed.")
        print("  Install it with:  pip install \"pdf-autofillr[mapper]\"\n")
        return 1

    if not os.path.exists(args.pdf):
        print(f"\n  ✗  PDF not found: {args.pdf}\n")
        return 1
    if not os.path.exists(args.schema):
        print(f"\n  ✗  Schema not found: {args.schema}")
        print("  Run: pdf-autofillr-cli setup  to create configs/\n")
        return 1

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)

    print(f"\n  Embedding {args.pdf}...")
    result = asyncio.run(pipeline.run_all(
        input_pdf_path=args.pdf,
        input_data_path=args.schema,
        keep_intermediates=True,
    ))

    embedded = result["all_outputs"]["embedded_pdf"]
    print(f"  ✅  Embedded PDF: {embedded}\n")
    return 0
