#!/usr/bin/env python3
"""Fail-closed verifier for the bounded mu crosswalk package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_json(script: str) -> dict:
    output = subprocess.check_output([sys.executable, str(HERE / script)], text=True)
    return json.loads(output)


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert rows, "empty source manifest"
    for row in rows:
        path = REPO / row["path"]
        assert path.is_file(), f"missing source: {path}"
        assert sha256(path) == row["sha256"], f"hash mismatch: {path}"

    primary = run_json("derive_crosswalk.py")
    saved_primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert primary == saved_primary
    assert primary["all_checks_pass"]

    independent = run_json("verify_independent.py")
    saved_independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    for key in ("all_checks_pass", "checks", "exact_witness"):
        assert independent[key] == saved_independent[key]
    assert independent["all_checks_pass"]

    catch_output = subprocess.check_output(
        [sys.executable, str(HERE / "run_catch_proofs.py")], text=True
    )
    assert catch_output.startswith("PASS: 4 hostile mutations caught")
    catch_saved = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert catch_saved["all_catches_pass"] and catch_saved["count"] == 4

    print(
        "PASS: 10 source hashes, 14 primary checks, 9 independent checks, "
        "and 4 hostile mutations"
    )


if __name__ == "__main__":
    main()
