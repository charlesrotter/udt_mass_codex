#!/usr/bin/env python3
"""End-to-end package verifier for G190."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def run(script: str, no_write: bool):
    environment = os.environ.copy()
    if no_write:
        environment["G190_NO_WRITE"] = "1"
    subprocess.run([sys.executable, str(PACKAGE / script)], cwd=ROOT, env=environment, check=True)


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    no_write = "--no-write" in sys.argv[1:]
    unknown = [argument for argument in sys.argv[1:] if argument != "--no-write"]
    if unknown:
        raise SystemExit(f"unknown arguments: {unknown}")
    required = [
        "PREREGISTRATION.md",
        "PONDER_MAP.md",
        "PREMISE_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "derive_timelive_frequency_screen.py",
        "verify_timelive_frequency_screen_independent.py",
        "run_catch_proofs.py",
        "build_source_manifest.py",
    ]
    missing = [name for name in required if not (PACKAGE / name).is_file()]
    if missing:
        raise AssertionError(f"missing package files: {missing}")

    run("derive_timelive_frequency_screen.py", no_write)
    run("verify_timelive_frequency_screen_independent.py", no_write)
    run("run_catch_proofs.py", no_write)
    run("build_source_manifest.py", no_write)

    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    if production["landing"] != "COMPLETED_PAIR_TIMELIVE_FREQUENCY_SCREEN_JOINT_EVALUATOR_DERIVED_CONDITIONALLY":
        raise AssertionError(production["landing"])
    if any(production["scope"].values()):
        raise AssertionError(production["scope"])
    if independent["status"] != "PASS" or independent["reads_production_artifact"]:
        raise AssertionError(independent)
    if catches["status"] != "PASS" or catches["caught"] < 14:
        raise AssertionError(catches)

    manifest_rows = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    if len(manifest_rows) != 10:
        raise AssertionError(f"source row count {len(manifest_rows)}")
    for row in manifest_rows:
        relative, expected, size = row.split("\t")
        path = ROOT / relative
        if sha256(path) != expected or path.stat().st_size != int(size):
            raise AssertionError(relative)

    adjudication_path = PACKAGE / "EXTERNAL_REVIEW_ADJUDICATION.md"
    if adjudication_path.is_file():
        external_required = [
            "EXTERNAL_REVIEW_RAW.md",
            "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
            "TRANSMISSION_RECORD.md",
        ]
        missing_external = [name for name in external_required if not (PACKAGE / name).is_file()]
        if missing_external:
            raise AssertionError(f"missing external evidence: {missing_external}")
        adjudication = adjudication_path.read_text(encoding="utf-8")
        raw = PACKAGE / "EXTERNAL_REVIEW_RAW.md"
        transcript = PACKAGE / "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz"
        if "G190_ACCEPTED_WITH_STATED_BOUNDS" not in adjudication:
            raise AssertionError("external grade absent")
        if sha256(raw) != "d77582a36b1a589017f82fb367c75b4103cd2f5d7706ab13c48fd80a8c24fb44":
            raise AssertionError("external raw hash mismatch")
        if sha256(transcript) != "32b1fee2d2dd74fcb544694e6503f3b41d3546e209dd99347de07b5095eb95f6":
            raise AssertionError("external transcript hash mismatch")
        external_grade = "G190_ACCEPTED_WITH_STATED_BOUNDS"
    else:
        external_grade = "PENDING"

    premise_verifier = ROOT / "verify_current_scientific_premises.py"
    if premise_verifier.is_file() and not no_write:
        subprocess.run([sys.executable, str(premise_verifier)], cwd=ROOT, check=True)
        premise_gate = "PASS"
    else:
        # A sealed review intake contains only the exact registered scientific sources, not the
        # repository-wide startup surface.  The repository run above remains the premise gate.
        premise_gate = "SEALED_INTAKE_NOT_APPLICABLE"
    result = {
        "status": "PASS",
        "source_rows": len(manifest_rows),
        "independent_assertions": independent["assertions"],
        "mutation_catches": catches["caught"],
        "repository_premise_gate": premise_gate,
        "external_review": external_grade,
    }
    result["no_write_replay"] = no_write
    if not no_write:
        (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
