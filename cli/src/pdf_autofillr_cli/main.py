"""
pdf-autofillr — unified CLI for all pdf-autofillr modules.

Usage:
    pdf-autofillr --help
    pdf-autofillr status
    pdf-autofillr setup
    pdf-autofillr rag <command>
    pdf-autofillr chatbot <command>
    pdf-autofillr mapper <command>
    pdf-autofillr doc-upload <command>
    pdf-autofillr plugins <command>
"""
from __future__ import annotations

import argparse
import sys

from pdf_autofillr_cli import __version__
from pdf_autofillr_cli import (
    cmd_status,
    cmd_setup,
    cmd_rag,
    cmd_chatbot,
    cmd_mapper,
    cmd_doc_upload,
    cmd_plugins,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-autofillr",
        description=(
            "Unified CLI for pdf-autofillr.\n\n"
            "Available commands:\n"
            "  status       Check installed modules and config\n"
            "  setup        First-time setup (creates .env, configs, data/)\n"
            "  rag          RAG field prediction\n"
            "  chatbot      Conversational form-filling\n"
            "  mapper       PDF template embedding and filling\n"
            "  doc-upload   Extract from documents and fill PDFs\n"
            "  plugins      List and inspect plugins\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"pdf-autofillr-cli {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    cmd_status.add_parser(subparsers)
    cmd_setup.add_parser(subparsers)
    cmd_rag.add_parser(subparsers)
    cmd_chatbot.add_parser(subparsers)
    cmd_mapper.add_parser(subparsers)
    cmd_doc_upload.add_parser(subparsers)
    cmd_plugins.add_parser(subparsers)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Each subcommand sets args.func = run
    if hasattr(args, "func"):
        exit_code = args.func(args)
        sys.exit(exit_code or 0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
