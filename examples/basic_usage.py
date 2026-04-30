"""
Basic usage — run pdf-autofillr CLI commands from Python.
"""
import subprocess

def run(cmd):
    result = subprocess.run(["pdf-autofillr"] + cmd, capture_output=True, text=True)
    print(result.stdout)
    return result.returncode

# Check status
run(["status"])

# RAG system info
run(["rag", "system-info"])

# List plugins
run(["plugins", "list"])
