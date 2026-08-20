#!/usr/bin/env python3
"""Rebuild and verify the bounded G191 evidence package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def run(script: str, no_write: bool):
    env = os.environ.copy()
    if no_write:
        env["G191_NO_WRITE"] = "1"
    result = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    run("derive_nonconformal_timelive_mixing.py", args.no_write)
    run("verify_nonconformal_timelive_mixing_independent.py", args.no_write)
    run("run_catch_proofs.py", args.no_write)
    run("build_source_manifest.py", args.no_write)

    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))

    assert production["frequency_residual"] == "0"
    assert production["jacobi_residual"] == [["0", "0"], ["0", "0"]]
    assert production["branch_classification"]["frequency_turns"] == 0
    assert production["branch_classification"]["post_vertex_caustics"] == 0
    assert production["branch_classification"]["cross_response"].startswith("strictly_positive")
    assert independent["status"] == "PASS"
    assert independent["assertions"] == 387680
    assert independent["maximum_jacobi_error"] < independent["registered_tolerance"]
    assert catches["status"] == "PASS" and catches["caught"] == 15
    assert len(source_rows) == 8
    for row in source_rows:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]

    premise_verifier = ROOT / "verify_current_scientific_premises.py"
    if premise_verifier.is_file():
        premise = subprocess.run(
            [sys.executable, str(premise_verifier)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if premise.returncode:
            raise SystemExit(premise.stdout + premise.stderr)
        premise_gate = "PASS"
    else:
        # The bounded review intake freezes the exact registry row set and source hashes but does
        # not duplicate the repository-wide startup surface audited by this verifier.  Repository
        # package runs still execute the full premise gate above.
        premise_gate = "SEALED_INTAKE_NOT_APPLICABLE"

    adjudication_path = PACKAGE / "EXTERNAL_REVIEW_ADJUDICATION.md"
    if adjudication_path.is_file() and "G191_ACCEPTED_WITH_STATED_BOUNDS" in adjudication_path.read_text(encoding="utf-8"):
        external_hashes = {
            "EXTERNAL_REVIEW_RAW.md": "2b25e78856decb8cbdf1a4d8a56d44aa4dbb844d2f261bb04f140afc13ce871d",
            "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz": "9400170f7786dbc714f953e9c31da04eee5d527bddf135757bf7dbd32aa75776",
            "EXTERNAL_FOLLOWUP_REVIEW_RAW.md": "048063b93a63db1e8147bc639a7723a992e4289ebb147dceab7dafca22edab3e",
            "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt.gz": "9e18372cdde90f7927fd1e3b71f7aacbb05b545fe7dab7a9639658e891bd8a0a",
        }
        for name, expected in external_hashes.items():
            path = PACKAGE / name
            assert path.is_file(), name
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
        external_grade = "G191_ACCEPTED_WITH_STATED_BOUNDS"
        package_grade = "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS"
    else:
        external_grade = "PENDING"
        package_grade = "VERIFIED_WITH_CAVEATS_PENDING_EXTERNAL_REVIEW"

    result = {
        "status": "PASS",
        "grade": package_grade,
        "no_write_replay": args.no_write,
        "source_rows": len(source_rows),
        "independent_assertions": independent["assertions"],
        "maximum_jacobi_error": independent["maximum_jacobi_error"],
        "mutation_catches": catches["caught"],
        "repository_premise_gate": premise_gate,
        "external_review": external_grade,
    }
    if not args.no_write:
        (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
