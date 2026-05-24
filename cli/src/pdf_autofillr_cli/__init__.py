"""
pdf-autofillr-cli

Unified command-line interface for all pdf-autofillr modules:
  chatbot, mapper, rag, doc-upload

Install:
    pip install pdf-autofillr-cli

Usage:
    pdf-autofillr --help
    pdf-autofillr status
    pdf-autofillr setup
    pdf-autofillr chatbot start
    pdf-autofillr rag predict ...
    pdf-autofillr mapper embed ...
    pdf-autofillr doc-upload process ...
"""

__version__ = "0.1.1"
__all__ = ["main"]
