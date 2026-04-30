FROM python:3.12-slim

WORKDIR /app

# Install pdf-autofillr-cli with all modules
RUN pip install --no-cache-dir "pdf-autofillr-cli[all]"

# Default command
ENTRYPOINT ["pdf-autofillr"]
CMD ["--help"]
