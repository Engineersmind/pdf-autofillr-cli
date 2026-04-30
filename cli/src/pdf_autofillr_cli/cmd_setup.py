"""
pdf-autofillr setup

Runs first-time setup — creates .env, config files, and data directories.
Delegates to each module's own setup routine.
"""
from __future__ import annotations

import argparse


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "setup",
        help="First-time setup: create .env, configs, and data directories",
        description=(
            "Run once after install. Creates:\n"
            "  - .env with all environment variable defaults\n"
            "  - configs/ directory with form_keys.json and mapper_config.ini\n"
            "  - data/ directory skeleton\n"
        ),
    )
    p.add_argument(
        "--path",
        default=".",
        help="Directory to set up (default: current directory)",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    p.add_argument(
        "--module",
        choices=["rag", "chatbot", "mapper", "doc-upload", "all"],
        default="all",
        help="Which module to set up (default: all)",
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    import os
    os.chdir(args.path) if args.path != "." else None

    modules = (
        ["rag", "chatbot", "mapper", "doc-upload"]
        if args.module == "all"
        else [args.module]
    )

    ran_any = False

    if "rag" in modules:
        try:
            from ragpdf.entrypoints.setup import main as rag_setup
            print("\n── RAG setup ──────────────────────────────────────")
            rag_setup()
            ran_any = True
        except ImportError:
            print("  rag module not installed, skipping.")

    if "chatbot" in modules:
        try:
            from chatbot.entrypoints.cli import setup as chatbot_setup
            print("\n── Chatbot setup ───────────────────────────────────")
            chatbot_setup(force=args.force)
            ran_any = True
        except (ImportError, AttributeError):
            # chatbot has no standalone setup — just note it
            print("  chatbot: no standalone setup needed (configure via .env)")

    if "mapper" in modules:
        try:
            from pdf_autofillr_mapper.entrypoints.cli import setup as mapper_setup
            print("\n── Mapper setup ────────────────────────────────────")
            mapper_setup(force=args.force)
            ran_any = True
        except (ImportError, AttributeError):
            print("  mapper: no standalone setup needed (configure via .env)")

    if "doc-upload" in modules:
        try:
            from pdf_autofillr_doc_upload.entrypoints.cli import setup as doc_setup
            print("\n── Doc Upload setup ────────────────────────────────")
            doc_setup(force=args.force)
            ran_any = True
        except (ImportError, AttributeError):
            print("  doc-upload: no standalone setup needed (configure via .env)")

    if not ran_any:
        print(
            "\n  No modules are installed.\n"
            "  Install everything:  pip install pdf-autofillr[all]\n"
        )
        return 1

    print("\n✅  Setup complete. Edit .env then run: pdf-autofillr status\n")
    return 0
