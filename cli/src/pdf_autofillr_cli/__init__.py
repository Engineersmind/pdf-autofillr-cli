"""
pdf-autofillr-cli

Unified command-line interface for all pdf-autofillr modules.

Install:
    pip install "pdf-autofillr-cli"

Usage:
    pdf-autofillr-cli --help
    pdf-autofillr-cli extract form.pdf --output schema.json
    pdf-autofillr-cli embed form.pdf --schema configs/form_keys.json
    pdf-autofillr-cli fill form.pdf --data data.json
    pdf-autofillr-cli validate filled.pdf --schema schema.json
    pdf-autofillr-cli run form.pdf --schema configs/form_keys.json --data data.json
    pdf-autofillr-cli batch --template form.pdf --schema configs/form_keys.json --input data/ --output output/
    pdf-autofillr-cli chatbot session --pdf form.pdf --user u1
    pdf-autofillr-cli doc-upload process --doc investor.pdf --pdf form.pdf --schema form_keys.json
    pdf-autofillr-cli mapper embed --pdf form.pdf --schema configs/form_keys.json
    pdf-autofillr-cli rag predict --user u1 --session s1 --pdf p1 --fields fields.json --hash abc
    pdf-autofillr-cli plugins list
    pdf-autofillr-cli status
"""

__version__ = "0.3.0"
__all__ = ["main"]
