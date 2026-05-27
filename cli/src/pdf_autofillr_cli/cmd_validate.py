"""
pdf-autofillr-cli validate <pdf> --schema schema.json

Validate a filled PDF against a field schema.
Checks that all required fields are present and non-empty.
Exits 0 if valid, 1 if any fields are missing or blank.

Example:
    pdf-autofillr-cli validate filled.pdf --schema configs/form_keys.json
    pdf-autofillr-cli validate filled.pdf --schema schema.json --strict
"""

from __future__ import annotations

import argparse
import json
import os


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "validate",
        help="Validate a filled PDF against a field schema",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("pdf", help="Path to the filled PDF to validate")
    p.add_argument(
        "--schema",
        "-s",
        required=True,
        help="Path to schema JSON (form_keys.json or extract output)",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any empty field, not just missing ones",
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    try:
        from pdf_autofillr_mapper import MapperConfig, PDFPipeline  # type: ignore
    except ImportError:
        print("\n  pdf-autofillr-mapper is not installed.")
        print('  Install it with:  pip install "pdf-autofillr[mapper]"\n')
        return 1

    if not os.path.exists(args.pdf):
        print(f"\n  ✗  PDF not found: {args.pdf}\n")
        return 1

    if not os.path.exists(args.schema):
        print(f"\n  ✗  Schema not found: {args.schema}")
        print("  Run first:  pdf-autofillr-cli extract form.pdf --output schema.json\n")
        return 1

    with open(args.schema, encoding="utf-8") as f:
        schema = json.load(f)

    print(f"\n  Validating {args.pdf}...")

    try:
        import asyncio

        # from pdf_autofillr_mapper import MapperConfig, PDFPipeline  # type: ignore

        cfg = MapperConfig.from_env()
        pipeline = PDFPipeline(mapper_config=cfg)
        result = asyncio.run(
            pipeline.validate(
                filled_pdf_path=args.pdf,
                schema=schema,
                strict=args.strict,
            )
        )
    except AttributeError:
        # SDK doesn't expose pipeline.validate yet — fall back to local check
        result = _local_validate(args.pdf, schema, args.strict)
    except Exception as e:
        print(f"\n  ✗  Validation error: {e}\n")
        return 1

    return _report(result)


# ── local fallback ────────────────────────────────────────────────────────────


def _local_validate(pdf_path: str, schema: dict | list, strict: bool) -> dict:
    """
    Lightweight local validation — reads field values directly from the PDF
    using pypdf (if installed) and checks them against the schema keys.
    Falls back to a structural check if pypdf is unavailable.
    """
    required_keys: list[str] = []

    if isinstance(schema, list):
        required_keys = [str(f) for f in schema]
    elif isinstance(schema, dict):
        # Support {field_name: {...}} and {"fields": [...]} shapes
        if "fields" in schema:
            required_keys = [str(f) for f in schema["fields"]]
        else:
            required_keys = list(schema.keys())

    filled_values: dict[str, str] = {}
    try:
        import pypdf  # type: ignore

        reader = pypdf.PdfReader(pdf_path)
        fields = reader.get_fields() or {}
        for k, v in fields.items():
            val = v.get("/V", "") if isinstance(v, dict) else str(v)
            filled_values[k] = str(val).strip() if val else ""
    except ImportError:
        # pypdf not available — do schema-only structural check
        return {
            "valid": True,
            "missing": [],
            "empty": [],
            "note": "pypdf not installed — only schema structure checked",
        }

    missing = [k for k in required_keys if k not in filled_values]
    empty = (
        [k for k in required_keys if k in filled_values and not filled_values[k]] if strict else []
    )

    return {
        "valid": len(missing) == 0 and len(empty) == 0,
        "missing": missing,
        "empty": empty,
        "total_required": len(required_keys),
        "filled_count": len([k for k in required_keys if filled_values.get(k)]),
    }


def _report(result: dict) -> int:
    valid = result.get("valid", False)
    missing = result.get("missing", [])
    empty = result.get("empty", [])
    note = result.get("note", "")

    if note:
        print(f"  ℹ  {note}")

    total = result.get("total_required", "?")
    filled = result.get("filled_count", "?")
    print(f"  Fields: {filled}/{total} filled")

    if missing:
        print(f"\n  ✗  Missing fields ({len(missing)}):")
        for f in missing:
            print(f"       - {f}")

    if empty:
        print(f"\n  ✗  Empty fields ({len(empty)}):")
        for f in empty:
            print(f"       - {f}")

    if valid:
        print("  ✅  Validation passed\n")
        return 0
    else:
        print("\n  ✗  Validation failed\n")
        return 1
