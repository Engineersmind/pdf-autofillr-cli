"""
pdf-autofillr-cli batch --template form.pdf --schema form_keys.json --input data/ --output output/

Fill multiple PDFs from a directory of JSON files.
The template is embedded once, then each JSON file produces one filled PDF.

Example:
    pdf-autofillr-cli batch --template form.pdf --schema configs/form_keys.json --input data/ --output output/
"""

from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "batch",
        help="Fill multiple PDFs from a directory of JSON files",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--template", "-t", required=True, help="Path to blank PDF form")
    p.add_argument("--schema", "-s", required=True, help="Path to form_keys.json")
    p.add_argument("--input", "-i", required=True, help="Directory containing JSON data files")
    p.add_argument("--output", "-o", required=True, help="Directory to write filled PDFs")
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    try:
        from pdf_autofillr_mapper import MapperConfig, PDFPipeline  # type: ignore
    except ImportError:
        print("\n  pdf-autofillr-mapper is not installed.")
        print('  Install it with:  pip install "pdf-autofillr[mapper]"\n')
        return 1

    if not os.path.exists(args.template):
        print(f"\n  ✗  Template not found: {args.template}\n")
        return 1
    if not os.path.exists(args.schema):
        print(f"\n  ✗  Schema not found: {args.schema}\n")
        return 1

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(input_dir.glob("*.json"))
    if not json_files:
        print(f"\n  No JSON files found in {args.input}\n")
        return 1

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)

    print(f"\n  Batch: {len(json_files)} files  →  {args.output}\n")

    # Step 1: embed once
    print("  Embedding template (once)...")
    embed_result = asyncio.run(
        pipeline.run_all(
            input_pdf_path=args.template,
            input_data_path=args.schema,
            keep_intermediates=True,
        )
    )
    embedded_pdf = embed_result["all_outputs"]["embedded_pdf"]
    print(f"  ✅  Embedded: {embedded_pdf}\n")

    # Step 2: fill each JSON file
    success = 0
    failed = 0

    for json_file in json_files:
        out_path = str(output_dir / f"{json_file.stem}_filled.pdf")
        try:
            result = asyncio.run(
                pipeline.fill(
                    embedded_pdf_path=embedded_pdf,
                    input_data_path=str(json_file),
                    output_path=out_path,
                )
            )
            print(f"  ✅  {json_file.name}  →  {result['output_file']}")
            success += 1
        except Exception as e:
            print(f"  ✗   {json_file.name}  →  {e}")
            failed += 1

    print(f"\n  Done: {success} filled, {failed} failed\n")
    return 0 if failed == 0 else 1
