"""
Module availability helpers.

Each function returns (available: bool, version: str, error: str).
We do lazy imports so the CLI still loads even if only some modules are installed.
"""
from __future__ import annotations

from typing import Tuple


def _try_import(module: str) -> Tuple[bool, str, str]:
    try:
        mod = __import__(module)
        ver = getattr(mod, "__version__", "?")
        return True, ver, ""
    except ImportError as e:
        return False, "", str(e)


def chatbot_available() -> Tuple[bool, str, str]:
    return _try_import("chatbot")


def rag_available() -> Tuple[bool, str, str]:
    return _try_import("ragpdf")


def mapper_available() -> Tuple[bool, str, str]:
    return _try_import("pdf_autofillr_mapper")


def doc_upload_available() -> Tuple[bool, str, str]:
    return _try_import("pdf_autofillr_doc_upload")


def plugins_available() -> Tuple[bool, str, str]:
    return _try_import("pdf_autofillr_plugins")


def require_module(name: str, install_hint: str) -> None:
    """Exit with a helpful message if a module is not installed."""
    import sys
    available, _, err = _try_import(name)
    if not available:
        print(f"\n  Module '{name}' is not installed.")
        print(f"  Install it with:  {install_hint}\n")
        sys.exit(1)
