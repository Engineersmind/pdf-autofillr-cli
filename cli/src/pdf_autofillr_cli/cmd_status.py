"""
pdf-autofillr status

Checks which modules are installed and how they are configured.
Delegates to the status checker in the umbrella package (packages/pdf_autofillr).
"""
from __future__ import annotations

import argparse


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "status",
        help="Show which modules are installed and their configuration",
        description=(
            "Checks all pdf-autofillr modules and prints a summary of:\n"
            "  - Which modules are installed\n"
            "  - Config files present\n"
            "  - Env variable settings\n"
            "  - Inter-module connection status"
        ),
    )
    p.add_argument(
        "--path",
        default=".",
        help="Project directory to check (default: current directory)",
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    try:
        from pdf_autofillr.status import run_status
        run_status(args.path)
    except ImportError:
        # Fallback: do it ourselves if umbrella package not installed
        _fallback_status()
    return 0


def _fallback_status() -> None:
    """Minimal status when umbrella package is not present."""
    from pdf_autofillr_cli.utils import (
        chatbot_available,
        rag_available,
        mapper_available,
        doc_upload_available,
        plugins_available,
    )

    print("\n" + "=" * 60)
    print("  pdf-autofillr status")
    print("=" * 60)
    print("\nModules")
    print("-" * 60)

    checks = [
        ("chatbot",    chatbot_available,    "pip install pdf-autofillr-chatbot"),
        ("rag",        rag_available,        "pip install pdf-autofillr-rag"),
        ("mapper",     mapper_available,     "pip install pdf-autofillr-mapper"),
        ("doc_upload", doc_upload_available, "pip install pdf-autofillr-doc-upload"),
        ("plugins",    plugins_available,    "pip install pdf-autofillr-plugins"),
    ]

    for label, checker, hint in checks:
        ok, ver, _ = checker()
        if ok:
            print(f"  ✅  {label:<12} v{ver}")
        else:
            print(f"  ✗   {label:<12} not installed  →  {hint}")

    print()
