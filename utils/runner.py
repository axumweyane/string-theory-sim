"""Execute engineer-generated simulation code in a subprocess.

Code is written to simulations/round_<n>.py and run with the current
interpreter, cwd=simulations/, so figures land in simulations/outputs/.
The script's contract: print one line `RESULT_JSON: {...}` with its metrics.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent / "simulations"
RESULT_RE = re.compile(r"^RESULT_JSON:\s*(\{.*\})\s*$", re.MULTILINE)


def run_simulation(code: str, round_no: int | str, timeout: int = 300) -> dict:
    (SIM_DIR / "outputs").mkdir(parents=True, exist_ok=True)
    path = SIM_DIR / f"round_{round_no}.py"
    path.write_text(code)
    try:
        proc = subprocess.run(
            [sys.executable, path.name],
            cwd=SIM_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timed out after {timeout}s", "stdout": "", "stderr": "", "metrics": None}

    metrics = None
    m = RESULT_RE.search(proc.stdout)
    if m:
        try:
            metrics = json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return {
        "ok": proc.returncode == 0 and metrics is not None,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
        "metrics": metrics,
        "code_path": str(path),
    }
