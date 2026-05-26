"""
Full RAG workflow from Python:
  1. init-vectors
  2. predict
  3. feedback
  4. metrics

Requires: pip install "pdf-autofillr-cli[rag]"
"""
# import subprocess, json
import subprocess

def cli(*args):
    r = subprocess.run(["pdf-autofillr"] + list(args), capture_output=True, text=True)
    print(r.stdout)
    return r.returncode

# 1. Generate embeddings
cli("rag", "init-vectors")

# 2. Predict (requires fields JSON and category JSON files)
# cli("rag", "predict",
#     "--user", "u1", "--session", "s1", "--pdf", "p1",
#     "--fields", "data/rag/input/fields/lp_subscription_fields.json",
#     "--hash", "abc123",
#     "--category", "data/rag/input/pdf_category.json")

# 3. Global metrics
cli("rag", "metrics", "--type", "global")
