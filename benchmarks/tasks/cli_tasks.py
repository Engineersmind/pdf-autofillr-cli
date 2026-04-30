"""CLI benchmark tasks — run pdf-autofillr commands and time them."""
import subprocess, time

def run_status_task():
    start = time.time()
    r = subprocess.run(["pdf-autofillr", "status"], capture_output=True, text=True)
    return {"task": "status", "exit_code": r.returncode, "duration_s": round(time.time()-start, 3)}

def run_rag_system_info_task():
    start = time.time()
    r = subprocess.run(["pdf-autofillr", "rag", "system-info"], capture_output=True, text=True)
    return {"task": "rag_system_info", "exit_code": r.returncode, "duration_s": round(time.time()-start, 3)}
