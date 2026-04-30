"""
pdf-autofillr mapper <command>

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
            "  1. pdf-autofillr mapper embed --pdf form.pdf --user u1 --id lp_v1\n"
            "  2. pdf-autofillr mapper fill  --pdf form.pdf --user u1 --id lp_v1 --data data.json\n"
        ),
    )
    sub = p.add_subparsers(dest="mapper_command", metavar="COMMAND")

    # ── embed ─────────────────────────────────────────────────────────────
    emb = sub.add_parser("embed", help="Embed a blank PDF template (run once per form)")
    emb.add_argument("--pdf",    required=True, help="Path to blank PDF form")
    emb.add_argument("--user",   required=True, help="User ID")
    emb.add_argument("--id",     required=True, dest="pdf_doc_id", help="Document ID")

    # ── fill ──────────────────────────────────────────────────────────────
    fil = sub.add_parser("fill", help="Fill an embedded PDF with user data")
    fil.add_argument("--pdf",    required=True, help="Path to blank PDF form")
    fil.add_argument("--user",   required=True, help="User ID")
    fil.add_argument("--id",     required=True, dest="pdf_doc_id", help="Document ID")
    fil.add_argument("--data",   required=True,
                     help="Path to JSON file with user_data dict, or inline JSON string")

    # ── start (API server) ────────────────────────────────────────────────
    srv = sub.add_parser("start", help="Start the mapper API server")
    srv.add_argument("--host",   default="0.0.0.0")
    srv.add_argument("--port",   default=8001, type=int)
    srv.add_argument("--reload", action="store_true")

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module
    require_module("pdf_autofillr_mapper", "pip install pdf-autofillr-mapper")

    if not args.mapper_command:
        print("Usage: pdf-autofillr mapper <command>")
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
    from pdf_autofillr_mapper import MapperOrchestrator  # type: ignore

    orch = MapperOrchestrator.from_env()
    result = orch.make_embed_file(
        pdf_path=args.pdf,
        user_id=args.user,
        pdf_doc_id=args.pdf_doc_id,
    )
    print(f"\n  ✅  Embedded: {result.embedded_pdf_path}\n")
    return 0


def _fill(args: argparse.Namespace) -> int:
    import os
    from pdf_autofillr_mapper import MapperOrchestrator  # type: ignore

    # Load user_data from file or inline JSON
    if os.path.exists(args.data):
        with open(args.data, encoding="utf-8") as fh:
            user_data = json.load(fh)
    else:
        user_data = json.loads(args.data)

    orch = MapperOrchestrator.from_env()
    result = orch.fill_pdf(
        pdf_path=args.pdf,
        user_id=args.user,
        pdf_doc_id=args.pdf_doc_id,
        user_data=user_data,
    )
    print(f"\n  ✅  Filled PDF: {result.filled_pdf_path}\n")
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
