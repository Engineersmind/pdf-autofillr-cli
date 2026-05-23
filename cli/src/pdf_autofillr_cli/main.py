"""
pdf-autofillr-cli — unified CLI for all pdf-autofillr modules.

Quick commands:
    pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json dob
    pdf-autofillr-cli fill form.pdf --data data.json --output filled.pdf
    pdf-autofillr-cli run form.pdf --data data.json --output filled.pdf
    pdf-autofillr-cli batch --template form.pdf --input data/ --output output/

Module commands:
    pdf-autofillr-cli chatbot session --pdf form.pdf --user u1
    pdf-autofillr-cli doc-upload process --doc investor.pdf --pdf form.pdf --schema keys.json
    pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json
    pdf-autofillr-cli rag predict --user u1 --session s1 --pdf p1 --fields f.json --hash abc
    pdf-autofillr-cli plugins list
    pdf-autofillr-cli status
"""
from __future__ import annotations

import argparse
import sys

from pdf_autofillr_cli import __version__
from pdf_autofillr_cli import (
    cmd_embed,
    cmd_fill,
    cmd_run,
    cmd_batch,
    cmd_chatbot,
    cmd_doc_upload,
    cmd_mapper,
    cmd_rag,
    cmd_plugins,
    cmd_status,
    cmd_setup,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-autofillr-cli",
        description=(
            "pdf-autofillr-cli CLI\n\n"
            "Quick commands:\n"
            "  embed    Embed field metadata into a PDF template (once per template)\n"
            "  fill     Fill an embedded PDF with JSON data\n"
            "  run      Full pipeline: embed + fill in one shot\n"
            "  batch    Fill multiple PDFs from a data directory\n\n"
            "Module commands:\n"
            "  chatbot     Conversational PDF form-filling\n"
            "  doc-upload  Extract from documents and fill PDFs\n"
            "  mapper      Low-level mapper commands\n"
            "  rag         RAG field prediction\n"
            "  plugins     List and inspect plugins\n"
            "  status      Check installed modules\n"
            "  setup       Create .env and show usage\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"pdf-autofillr-cli {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── quick commands ────────────────────────────────────────────────────
    cmd_embed.add_parser(subparsers)
    cmd_fill.add_parser(subparsers)
    cmd_run.add_parser(subparsers)
    cmd_batch.add_parser(subparsers)

    # ── module commands ───────────────────────────────────────────────────
    cmd_chatbot.add_parser(subparsers)
    cmd_doc_upload.add_parser(subparsers)
    cmd_mapper.add_parser(subparsers)
    cmd_rag.add_parser(subparsers)
    cmd_plugins.add_parser(subparsers)
    cmd_status.add_parser(subparsers)
    cmd_setup.add_parser(subparsers)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if hasattr(args, "func"):
        exit_code = args.func(args)
        sys.exit(exit_code or 0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
