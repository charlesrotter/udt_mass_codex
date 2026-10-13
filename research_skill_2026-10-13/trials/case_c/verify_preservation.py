"""Verify Case C input byte preservation; this is not a theorem test.

Exact command (from any working directory):
python3 /tmp/udt-research-skill-2026-10-13/case_c/output/verify_preservation.py

All writes stay in this script's output directory. No repository operations.
"""
from pathlib import Path
import hashlib
import json
import sys

output = Path(__file__).resolve().parent
root = output.parent
snapshot = json.loads((output / "INPUT_SNAPSHOT.json").read_text())["sha256"]
current = {
    str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(root.rglob("*"))
    if path.is_file() and "output" not in path.relative_to(root).parts
}
result = {
    "check": "input byte preservation only; no scientific certification",
    "python_version": sys.version,
    "command": "python3 /tmp/udt-research-skill-2026-10-13/case_c/output/verify_preservation.py",
    "input_count": len(snapshot),
    "changed": [name for name in snapshot if name in current and current[name] != snapshot[name]],
    "missing": sorted(set(snapshot) - set(current)),
    "unexpected": sorted(set(current) - set(snapshot)),
}
result["pass"] = not any(result[key] for key in ("changed", "missing", "unexpected"))
payload = json.dumps(result, indent=2) + "\n"
(output / "PRESERVATION_CHECK.json").write_text(payload)
print(payload, end="")
# Logs from shell redirection may still be open here. The manifest intentionally
# includes only settled files and excludes itself and those runtime logs.
manifest_files = sorted(
    path for path in output.iterdir()
    if path.is_file() and path.name not in {"SHA256SUMS", "verify.stdout", "verify.stderr"}
)
(output / "SHA256SUMS").write_text("".join(
    f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
    for path in manifest_files
))
raise SystemExit(0 if result["pass"] else 1)
