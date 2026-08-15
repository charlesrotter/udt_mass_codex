#!/usr/bin/env python3
"""Fail-closed verifier for the reciprocal-kernel release-candidate package."""

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


def run_json(name: str) -> dict:
    output = subprocess.check_output([sys.executable, str(HERE / name)], text=True)
    return json.loads(output)


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 18
    for row in rows:
        path = REPO / row["path"]
        assert path.is_file(), f"missing source: {path}"
        assert sha256(path) == row["sha256"], f"source hash mismatch: {path}"

    primary = run_json("derive_release_candidate.py")
    saved_primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert primary == saved_primary
    assert primary["all_checks_pass"] and len(primary["checks"]) == 16

    independent = run_json("verify_release_candidate_independent.py")
    saved_independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    for key in ("all_checks_pass", "checks", "regular", "sensitivities", "terminal_composition_residual", "terminal_reversal_residual"):
        assert independent[key] == saved_independent[key]
    assert independent["all_checks_pass"] and len(independent["checks"]) == 12

    catch = subprocess.check_output([sys.executable, str(HERE / "run_catch_proofs.py")], text=True)
    assert catch.strip() == "PASS: 9 hostile interface/semantic mutations caught"
    catch_saved = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert catch_saved["all_catches_pass"] and catch_saved["count"] == 9

    with (HERE / "SNE_INTERFACE_AUDIT.tsv").open(encoding="utf-8", newline="") as handle:
        sne = {row["layer"]: row for row in csv.DictReader(handle, delimiter="\t")}
    assert len(sne) == 17
    assert sne["release_readiness"]["current_status"] == "GEOMETRIC_SNE_QUERY_READY_CONDITIONALLY"
    assert sne["physical_metric_query_history"]["current_status"] == "OPEN"
    assert sne["physical_flux_source_law"]["current_status"] == "OPEN"

    print("PASS: 18 source hashes, 16 primary checks, 12 independent checks, 9 catches, 17 SNe interface rows")


if __name__ == "__main__":
    main()
