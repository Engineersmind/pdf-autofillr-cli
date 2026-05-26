"""
Mapper workflow: embed a blank form, then fill it.

Requires: pip install "pdf-autofillr-cli[mapper]"
"""
import subprocess

def cli(*args):
    r = subprocess.run(["pdf-autofillr"] + list(args), capture_output=True, text=True)
    print(r.stdout)
    return r.returncode

# Step 1: embed the blank template (run once per form)
# cli("mapper", "embed",
#     "--pdf", "data/input/blank_form.pdf",
#     "--user", "user_001",
#     "--id", "lp_sub_v1")

# Step 2: fill with user data
# cli("mapper", "fill",
#     "--pdf", "data/input/blank_form.pdf",
#     "--user", "user_001",
#     "--id", "lp_sub_v1",
#     "--data", "user_data.json")
