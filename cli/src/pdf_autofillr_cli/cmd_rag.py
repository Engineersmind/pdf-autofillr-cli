"""
pdf-autofillr-cli rag <command>

Wraps the ragpdf CLI with all its subcommands:
  init-vectors, predict, feedback, metrics, system-info, error-analytics
"""
from __future__ import annotations

import argparse
import json
import os
import sys
# from typing import Optional


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "rag",
        help="RAG field prediction commands",
        description="Self-learning RAG field prediction. Run 'pdf-autofillr-cli rag --help'.",
    )
    sub = p.add_subparsers(dest="rag_command", metavar="COMMAND")

    # ── init-vectors ──────────────────────────────────────────────────────
    iv = sub.add_parser("init-vectors", help="Generate embeddings from vector_source.json")
    iv.add_argument("--source",     default="", help="Path to vector source JSON")
    iv.add_argument("--backend",    default="", choices=["openai", "sentence_transformer"])
    iv.add_argument("--model",      default="", help="Embedding model name")
    iv.add_argument("--data-path",  default="", dest="data_path")
    iv.add_argument("--force",      action="store_true", help="Re-embed all vectors")
    iv.add_argument("--batch-size", default=50, type=int, dest="batch_size")
    iv.add_argument("--no-sanity-check", action="store_true", dest="no_sanity")

    # ── predict ───────────────────────────────────────────────────────────
    p2 = sub.add_parser("predict", help="Run RAG predictions on PDF fields")
    p2.add_argument("--user",     required=True)
    p2.add_argument("--session",  required=True)
    p2.add_argument("--pdf",      required=True)
    p2.add_argument("--fields",   required=True, help="Path to JSON file with fields list")
    p2.add_argument("--hash",     required=True, help="PDF hash (md5/sha)")
    p2.add_argument("--category", default="{}", help="File path or inline JSON for pdf_category")

    # ── feedback ──────────────────────────────────────────────────────────
    fb = sub.add_parser("feedback", help="Submit user feedback/corrections")
    fb.add_argument("--user",    required=True)
    fb.add_argument("--session", required=True)
    fb.add_argument("--pdf",     required=True)
    fb.add_argument("--errors",  required=True, help="Path to JSON file with errors list")

    # ── metrics ───────────────────────────────────────────────────────────
    m = sub.add_parser("metrics", help="Get accuracy and coverage metrics")
    m.add_argument("--type", required=True, dest="metric_type",
                   choices=["pdf", "category", "subcategory", "doctype",
                            "global", "compare", "pdf_hash"])
    m.add_argument("--user",        default=None)
    m.add_argument("--session",     default=None)
    m.add_argument("--pdf",         default=None)
    m.add_argument("--category",    default=None)
    m.add_argument("--subcategory", default=None)
    m.add_argument("--doctype",     default=None)
    m.add_argument("--pdf-hash",    default=None, dest="pdf_hash")

    # ── system-info ───────────────────────────────────────────────────────
    sub.add_parser("system-info", help="Show vector DB stats")

    # ── error-analytics ───────────────────────────────────────────────────
    ea = sub.add_parser("error-analytics", help="Get error breakdown with filters")
    ea.add_argument("--from",     default=None, dest="date_from")
    ea.add_argument("--to",       default=None, dest="date_to")
    ea.add_argument("--category", default=None)

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module
    require_module("ragpdf", "pip install pdf-autofillr-rag")

    if not args.rag_command:
        print("Usage: pdf-autofillr-cli rag <command>")
        print("Commands: init-vectors, predict, feedback, metrics, system-info, error-analytics")
        return 1

    # ── init-vectors (no client needed) ───────────────────────────────────
    if args.rag_command == "init-vectors":
        return _init_vectors(args)

    # ── all other commands need a client ──────────────────────────────────
    from ragpdf import RAGPDFClient
    client = RAGPDFClient.from_env()

    if args.rag_command == "predict":
        return _predict(args, client)
    elif args.rag_command == "feedback":
        return _feedback(args, client)
    elif args.rag_command == "metrics":
        return _metrics(args, client)
    elif args.rag_command == "system-info":
        print(json.dumps(client.get_system_info(), indent=2))
    elif args.rag_command == "error-analytics":
        return _error_analytics(args, client)

    return 0


def _init_vectors(args: argparse.Namespace) -> int:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # Optional dependency: continue if python-dotenv is not installed.
        # pass
        print("INFO: python-dotenv not installed; skipping .env loading.", file=sys.stderr)

    from ragpdf.init_vectors import run_init_vectors
    from ragpdf.config.settings import (
        RAGPDF_DATA_PATH, RAGPDF_EMBEDDING_BACKEND,
        RAGPDF_ST_MODEL, RAGPDF_OPENAI_EMBEDDING_MODEL,
    )

    data_path = args.data_path or RAGPDF_DATA_PATH
    backend   = args.backend   or RAGPDF_EMBEDDING_BACKEND
    model     = args.model     or (
        RAGPDF_OPENAI_EMBEDDING_MODEL if backend == "openai" else RAGPDF_ST_MODEL
    )

    if backend == "noop":
        print("ERROR: noop backend cannot generate real embeddings.", file=sys.stderr)
        return 1

    result = run_init_vectors(
        data_path=data_path,
        source_path=args.source or None,
        backend=backend,
        model=model,
        force=args.force,
        batch_size=args.batch_size,
        verbose=True,
        sanity_check=not args.no_sanity,
    )
    print(f"\n  vectors_total:    {result['vectors_total']}")
    print(f"  vectors_embedded: {result['vectors_embedded']}")
    print(f"  vectors_skipped:  {result['vectors_skipped']}")
    print(f"  model_used:       {result['model_used']}")
    return 0


def _load_category(value: str) -> dict:
    if not value or value == "{}":
        return {}
    if os.path.exists(value):
        with open(value, encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(value)


def _predict(args: argparse.Namespace, client) -> int:
    with open(args.fields, encoding="utf-8") as fh:
        fields = json.load(fh)
    if isinstance(fields, dict) and "fields" in fields:
        fields = fields["fields"]
    cat = _load_category(args.category)
    result = client.get_predictions(args.user, args.session, args.pdf, fields, args.hash, cat)
    print(json.dumps(result, indent=2))
    return 0


def _feedback(args: argparse.Namespace, client) -> int:
    with open(args.errors, encoding="utf-8") as fh:
        errors = json.load(fh)
    if isinstance(errors, dict) and "errors" in errors:
        errors = errors["errors"]
    print(json.dumps(client.submit_feedback(args.user, args.session, args.pdf, errors), indent=2))
    return 0


def _metrics(args: argparse.Namespace, client) -> int:
    raw = {k: v for k, v in vars(args).items()
           if k not in ("func", "command", "rag_command", "metric_type") and v is not None}
    remap = {"user": "user_id", "session": "session_id", "pdf": "pdf_id"}
    kwargs = {remap.get(k, k): v for k, v in raw.items()}
    print(json.dumps(client.get_metrics(args.metric_type, **kwargs), indent=2))
    return 0


def _error_analytics(args: argparse.Namespace, client) -> int:
    print(json.dumps(
        client.get_error_analytics(
            date_from=args.date_from,
            date_to=args.date_to,
            category=getattr(args, "category", None),
        ),
        indent=2
    ))
    return 0
