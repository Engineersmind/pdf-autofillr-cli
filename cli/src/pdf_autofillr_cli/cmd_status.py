"""
pdf-autofillr-cli status

Checks:
  1. All pdf-autofillr modules are installed
  2. Required environment variables are set

Example:
    pdf-autofillr-cli status
"""
from __future__ import annotations

import argparse
import importlib
import os


MODULES = [
    ("pdf_autofillr_mapper",     "mapper",     "pip install \"pdf-autofillr[mapper]\""),
    ("chatbot",                  "chatbot",    "pip install \"pdf-autofillr[chatbot]\""),
    ("pdf_autofillr_doc_upload", "doc-upload", "pip install \"pdf-autofillr[doc-upload]\""),
    ("ragpdf",                   "rag",        "pip install \"pdf-autofillr[rag]\""),
    ("pdf_autofillr_plugins",    "plugins",    "pip install pdf-autofillr-plugins"),
]

# At least one of these API key vars must be set
LLM_KEY_VARS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GROQ_API_KEY",
]


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "status",
        help="Check installed modules and environment variables",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    print("\n  pdf-autofillr-cli status")
    print("  " + "─" * 50)

    # ── modules ───────────────────────────────────────────────────────────
    print("\n  Modules")
    print("  " + "─" * 50)
    modules_ok = True
    for module, name, hint in MODULES:
        try:
            mod = importlib.import_module(module)
            ver = getattr(mod, "__version__", "?")
            print(f"  ✅  {name:<14} {ver}")
        except ImportError:
            print(f"  ✗   {name:<14} not installed  →  {hint}")
            modules_ok = False

    # ── environment ───────────────────────────────────────────────────────
    print("\n  Environment")
    print("  " + "─" * 50)
    env_ok = False
    for var in LLM_KEY_VARS:
        val = os.environ.get(var, "")
        if val and val != "your_openai_key_here":
            print(f"  ✅  {var}")
            env_ok = True
        else:
            print(f"  ✗   {var}  not set")

    if not env_ok:
        print("\n  No LLM API key found.")
        print("  Run: pdf-autofillr-cli setup\n")
        return 1

    # ── .env file ─────────────────────────────────────────────────────────
    print("\n  Config")
    print("  " + "─" * 50)
    if os.path.exists(".env"):
        print("  ✅  .env file found")
    else:
        print("  ✗   .env not found  →  run: pdf-autofillr-cli setup")

    print()
    if modules_ok and env_ok:
        print("  Everything looks good. Ready to go!\n")
    else:
        print("  Fix the issues above then run: pdf-autofillr-cli status\n")

    return 0 if (modules_ok and env_ok) else 1
