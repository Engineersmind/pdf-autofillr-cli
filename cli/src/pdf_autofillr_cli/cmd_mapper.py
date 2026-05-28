"""
pdf-autofillr-cli mapper <command>

Wraps the mapper module: embed a blank PDF form, then fill it with data.
"""

from __future__ import annotations

import argparse
import json


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "mapper",
        help="Mapper commands: embed and fill PDF forms",
        description=(
            "Two-step workflow:\n"
            "  1. pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json\n"
            "  2. pdf-autofillr-cli mapper fill  --pdf form.pdf --data data.json\n"
        ),
    )
    sub = p.add_subparsers(dest="mapper_command", metavar="COMMAND")

    # ── embed ─────────────────────────────────────────────────────────────
    emb = sub.add_parser("embed", help="Embed a blank PDF template (run once per form)")
    emb.add_argument("--pdf", required=True, help="Path to blank PDF form")
    emb.add_argument("--schema", default="configs/form_keys.json", help="Path to form_keys.json")
    emb.add_argument("--user", default="default", help="User ID (default: default)")

    # ── fill ──────────────────────────────────────────────────────────────
    fil = sub.add_parser("fill", help="Fill an embedded PDF with user data")
    fil.add_argument("--pdf", required=True, help="Path to blank PDF form")
    fil.add_argument("--user", default="default", help="User ID (default: default)")

    fil.add_argument(
        "--data", required=True, help="Path to JSON file with user_data dict, or inline JSON string"
    )

    # ── start (API server) ────────────────────────────────────────────────
    srv = sub.add_parser("start", help="Start the mapper API server")
    srv.add_argument("--host", default="0.0.0.0")
    srv.add_argument("--port", default=8001, type=int)
    srv.add_argument("--reload", action="store_true")

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module

    require_module("pdf_autofillr_mapper", 'pip install "pdf-autofillr[mapper]"')

    if not args.mapper_command:
        print("Usage: pdf-autofillr-cli mapper <command>")
        print("Commands: embed, fill, start")
        return 1

    if args.mapper_command == "embed":
        return _embed(args)
    elif args.mapper_command == "fill":
        return _fill(args)
    elif args.mapper_command == "start":
        return _start_server(args)

    return 0


def _embed(args: argparse.Namespace) -> int:
    import asyncio

    from pdf_autofillr_mapper import MapperConfig, PDFPipeline  # type: ignore

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)
    # schema path required — use --schema or default form_keys.json
    schema = getattr(args, "schema", "configs/form_keys.json")
    result = asyncio.run(
        pipeline.run_all(
            input_pdf_path=args.pdf,
            input_data_path=schema,
            keep_intermediates=True,
        )
    )
    print(f"\n  ✅  Embedded: {result['all_outputs']['embedded_pdf']}\n")
    return 0


def _fill(args: argparse.Namespace) -> int:
    import asyncio
    import os
    import tempfile
    from pathlib import Path

    from pdf_autofillr_mapper import MapperConfig, PDFPipeline  # type: ignore

    # Load user_data and write to temp file if inline JSON
    if os.path.exists(args.data):
        data_path = args.data
    else:
        user_data = json.loads(args.data)
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(user_data, tmp)
        tmp.close()
        data_path = tmp.name  # cleaned up by OS on process exit

    # Find embedded pdf
    p = Path(args.pdf)
    embedded = p.parent / f"{p.stem}_embedded.pdf"
    if not embedded.exists():
        print(f"\n  ✗  No embedded PDF found: {embedded}")
        print(
            "  Run first:  pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json\n"
        )
        return 1

    cfg = MapperConfig.from_env()
    pipeline = PDFPipeline(mapper_config=cfg)
    result = asyncio.run(
        pipeline.fill(
            embedded_pdf_path=str(embedded),
            input_data_path=data_path,
        )
    )
    print(f"\n  ✅  Filled PDF: {result['output_file']}\n")
    return 0


def _start_server(args: argparse.Namespace) -> int:
    try:
        import uvicorn
        from pdf_autofillr_mapper.entrypoints.fastapi_app import app  # type: ignore

        print(f"\n  Starting mapper server on http://{args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
    except ImportError:
        print("  uvicorn not installed. Run: pip install uvicorn")
        return 1
    return 0
