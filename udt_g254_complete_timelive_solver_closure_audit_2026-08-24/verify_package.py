#!/usr/bin/env python3
"""No-persistent-output verifier for the G254 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
REQUIRED = {
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULT.json",
    "CLOSURE_CONTRACT.tsv",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW_GPT54.md",
    "INDEPENDENT_VERIFICATION.json",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REVIEW_REQUEST.md",
    "RUN_RECORD.md",
    "SOURCE_MANIFEST.tsv",
    "STATUS_LEDGER.tsv",
    "build_review_intake.py",
    "derive_closure_census.py",
    "run_catch_proofs.py",
    "verify_independent.py",
    "verify_package.py",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run_json(script: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return json.loads(completed.stdout)


def main() -> None:
    present = {path.name for path in PACKAGE.iterdir() if path.is_file()}
    missing = sorted(REQUIRED - present)
    assert not missing, missing

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 16
    for row in sources:
        source = ROOT / row["path"]
        assert source.is_file(), row["path"]
        assert sha256(source) == row["sha256"], row["path"]

    production = run_json("derive_closure_census.py")
    independent = run_json("verify_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert production == json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    assert independent == json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    landing = "NO_OWNED_TIMELIVE_RESIDUAL__ODE_AND_GPU_SOLVES_NOT_YET_DEFINED"
    assert production["landing"] == independent["landing"] == landing
    assert production["owned_active_ambient_evolution_equation_count"] == 0
    assert production["stage_2"] == production["stage_3"] == "GATED_NOT_STARTED"
    assert catches["catch_count"] == 6
    review = (PACKAGE / "EXTERNAL_REVIEW_GPT54.md").read_text(encoding="utf-8")
    assert "G254_VERIFIED_WITH_CAVEATS" in review
    assert "No frozen-source scientific defect" in review
    assert "no evidence-package\nrepair was required" in review

    print(json.dumps({
        "status": "PACKAGE_PASS",
        "required_file_count": len(REQUIRED),
        "source_count": len(sources),
        "landing": landing,
        "independent_curvature_trials": independent["curvature_trials"],
        "hostile_catches": catches["catch_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
