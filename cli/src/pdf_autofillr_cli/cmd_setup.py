"""
pdf-autofillr-cli setup

First-time setup:
  1. Copies configs/ from mapper's bundled samples
  2. Creates .env from .env.example (if not already present)
  3. Shows USAGE.md path

Example:
    pdf-autofillr-cli setup
"""
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "setup",
        help="First-time setup: create configs/, .env, and show usage",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    print("\n  pdf-autofillr-cli setup")
    print("  " + "-" * 50)

    # Step 0: copy mapper configs
    try:
        from pdf_autofillr_mapper import copy_sample_configs  # type: ignore
        if not Path("configs").exists():
            copy_sample_configs(".")
            print("\n  OK  Created configs/ directory")
        else:
            print("\n  OK  configs/ already exists -- skipping")
    except ImportError:
        print("\n  WARN  pdf-autofillr-mapper not installed -- skipping configs setup")
        print('        Install with:  pip install "pdf-autofillr[mapper]"')

    # Step 1: create .env
    env_file = Path(".env")
    env_example = _find_env_example()

    if env_file.exists():
        print("\n  OK  .env already exists -- skipping")
    elif env_example:
        shutil.copy(env_example, env_file)
        print(f"\n  OK  Created .env from {env_example}")
        print("  --> Open .env and add your API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)")
    else:
        env_file.write_text(
            "# Add your LLM API key\n"
            "OPENAI_API_KEY=your_key_here\n"
            "\n"
            "# Noise suppression\n"
            "LITELLM_LOG=ERROR\n"
            "MAPPER_LOG_LEVEL=ERROR\n"
            "RAGPDF_LOG_LEVEL=WARNING\n"
        )
        print("\n  OK  Created minimal .env")
        print("  --> Open .env and add your API key")

    # Step 2: show usage guides
    usage_dir = _find_usage_dir()
    if usage_dir:
        print(f"\n  Usage guides: {usage_dir}")
        print("  One file per command — embed, fill, run, batch, chatbot, doc-upload, rag, mapper, plugins")
        print(f"  Example: open {usage_dir / 'run.md'}")
    else:
        print("\n  Quick start:")
        print("    pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json")
        print("    pdf-autofillr-cli fill form.pdf --data data.json")
        print("    pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json")

    print("\n  Run 'pdf-autofillr-cli status' to verify everything is ready.\n")
    return 0


def _find_env_example() -> Path | None:
    candidates = [
        Path(".env.example"),
        Path(__file__).parent.parent.parent / ".env.example",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _find_usage() -> Path | None:
    candidates = [
        Path("USAGE.md"),
        Path(__file__).parent / "USAGE.md",
        Path(__file__).parent.parent.parent / "USAGE.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _find_usage_dir() -> Path | None:
    candidates = [
        Path(__file__).parent / "usage",   # bundled in package
        Path(__file__).parent.parent.parent / "usage",  # dev install
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return None
