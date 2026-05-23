"""
pdf-autofillr-cli doc-upload <command>

Extract data from uploaded documents (PDF, DOCX, XLSX, CSV …) and fill a PDF form.
"""
from __future__ import annotations

import argparse


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "doc-upload",
        help="Doc-upload commands: extract data from documents and fill PDFs",
        description=(
            "Extract investor/client data from any document type and fill a PDF form.\n\n"
            "Supported source formats: PDF, DOCX, XLSX, CSV, JSON, TXT, MD\n\n"
            "Example:\n"
            "  pdf-autofillr-cli doc-upload process \\\n"
            "    --doc investor_data.pdf \\\n"
            "    --pdf blank_form.pdf \\\n"
            "    --schema configs/form_keys.json \\\n"
            "    --user user_001 --id lp_sub_v1\n"
        ),
    )
    sub = p.add_subparsers(dest="doc_command", metavar="COMMAND")

    # ── process ───────────────────────────────────────────────────────────
    pr = sub.add_parser(
        "process",
        help="Extract from a document and fill a PDF in one step",
    )
    pr.add_argument("--doc",    required=True, help="Source document (PDF, DOCX, XLSX, CSV …)")
    pr.add_argument("--pdf",    required=True, help="Blank PDF form to fill")
    pr.add_argument("--schema", required=True, dest="schema_keys_path",
                    help="Path to form_keys.json")
    pr.add_argument("--user",   required=True, dest="user_id")
    pr.add_argument("--id",     required=True, dest="pdf_doc_id", help="Document ID")

    # ── start (API server) ────────────────────────────────────────────────
    srv = sub.add_parser("start", help="Start the doc-upload API server")
    srv.add_argument("--host",   default="0.0.0.0")
    srv.add_argument("--port",   default=8002, type=int)
    srv.add_argument("--reload", action="store_true")

    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    from pdf_autofillr_cli.utils import require_module
    require_module("pdf_autofillr_doc_upload", "pip install pdf-autofillr-doc-upload")

    if not args.doc_command:
        print("Usage: pdf-autofillr-cli doc-upload <command>")
        print("Commands: process, start")
        return 1

    if args.doc_command == "process":
        return _process(args)
    elif args.doc_command == "start":
        return _start_server(args)

    return 0


def _process(args: argparse.Namespace) -> int:
    import uuid
    from pdf_autofillr_doc_upload import DocUploadClient  # type: ignore

    # DocUploadClient() reads all config from env vars automatically
    client = DocUploadClient()
    job_id = str(uuid.uuid4())

    result = client.run(
        document_path=args.doc,
        schema_path=args.schema_keys_path,
        job_id=job_id,
    )

    output_flat = result.get("output_flat", {})
    print(f"\n  Extracted fields: {len(output_flat)}")
    print(f"  Success: {result.get('success', '?')}")
    if result.get("filled_pdf_path"):
        print(f"  Filled PDF: {result['filled_pdf_path']}")
    print()
    return 0


def _start_server(args: argparse.Namespace) -> int:
    try:
        import uvicorn
        from pdf_autofillr_doc_upload.entrypoints.fastapi_app import app  # type: ignore
        print(f"\n  Starting doc-upload server on http://{args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
    except ImportError:
        print("  uvicorn not installed. Run: pip install uvicorn")
        return 1
    return 0
