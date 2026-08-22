#!/usr/bin/env python3
"""G212 manifest and no-write replay verifier."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT = ROOT / "PACKAGE_VERIFICATION_RESULT.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_json(script: str) -> dict[str, object]:
    environment = os.environ.copy()
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(ROOT / script)],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    return json.loads(completed.stdout)


def main() -> None:
    required = (
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "WHITEBOARD_SYNTHESIS.md",
        "VERIFICATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "verify_history_bridge.py",
        "verify_history_bridge_independent.py",
    )
    for name in required:
        if not (ROOT / name).is_file():
            raise FileNotFoundError(name)

    rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for row in rows:
        relative, expected, _role = row.split("\t", 2)
        actual = sha256(REPO / relative)
        if actual != expected:
            raise AssertionError(f"source hash mismatch: {relative}")

    symbolic_saved = json.loads((ROOT / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    independent_saved = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    symbolic_replay = run_json("verify_history_bridge.py")
    independent_replay = run_json("verify_history_bridge_independent.py")
    if symbolic_saved != symbolic_replay:
        raise AssertionError("symbolic replay mismatch")
    if independent_saved != independent_replay:
        raise AssertionError("independent replay mismatch")

    result = {
        "status": "PASS",
        "source_manifest_rows": len(rows),
        "symbolic_checks": symbolic_replay["check_count"],
        "independent_trials": independent_replay["trials"],
        "independent_assertions": independent_replay["assertions"],
        "core_no_write_replay": True,
        "whiteboard_roles": 3,
        "required_repairs": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
