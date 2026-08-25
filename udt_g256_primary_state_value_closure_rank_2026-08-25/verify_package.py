#!/usr/bin/env python3
"""No-write verifier for the G256 evidence package."""

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
LANDING = (
    "FUNCTION_VALUED_PRIMARY_STATE_REMAINS__"
    "ANGULAR_INTERLOCK_IS_TOMOGRAPHIC_NOT_PROPAGATING__NO_ODE_GPU"
)
REQUIRED = {
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULT.json",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
    "EXTERNAL_REVIEW_GPT54.md",
    "HERMITE_REALIZATION_ATLAS.tsv",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "OWNER_CENSUS.tsv",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REPAIR_PREREGISTRATION.md",
    "REVIEW_REQUEST.md",
    "RUN_RECORD.md",
    "SECOND_REPAIR_PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "STATUS_LEDGER.tsv",
    "VALUE_CLOSURE_CONTRACT.tsv",
    "VALUE_CLOSURE_RANK.tsv",
    "build_review_intake.py",
    "derive_value_closure.py",
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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run_json(script: str) -> dict[str, object]:
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.parse_args()

    present = {path.name for path in PACKAGE.iterdir() if path.is_file()}
    missing = sorted(REQUIRED - present)
    assert not missing, missing

    manifest = read_tsv(PACKAGE / "SOURCE_MANIFEST.tsv")
    owners = read_tsv(PACKAGE / "OWNER_CENSUS.tsv")
    assert len(manifest) == len(owners) == 18
    assert {row["path"] for row in manifest} == {row["source"] for row in owners}
    for row in manifest:
        source = ROOT / row["path"]
        assert source.is_file(), row["path"]
        assert sha256(source) == row["sha256"], row["path"]

    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    independent = run_json("verify_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert independent == json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["landing"] == independent["landing"] == LANDING
    assert production["status"] == independent["status"] == "PASS"
    assert production["ownership"] == {
        "owned_nonidentity_value_law_count": 0,
        "source_count": 18,
    }
    assert production["graph_sweep"]["complete_graph_anchored_dimension_formula"] == "N-1"
    assert production["graph_sweep"]["record_count"] == independent["graph_trials"] == 43
    assert production["graph_sweep"]["arbitrary_N_proof"] == (
        "connected_incidence_kernel_is_span_of_all_ones"
    )
    assert production["angular_interlock"]["owned_residual_count"] == 0
    assert production["angular_interlock"]["jet_jacobian_determinant"] == "-exp(-4*phi)"
    assert production["angular_interlock"]["classification"] == (
        "LOCAL_TOMOGRAPHIC_BIJECTION_NOT_VALUE_PROPAGATION"
    )
    assert production["solver_gate"]["owned_residual_count"] == 0
    assert set(production["solver_gate"].values()) == {0, "GATED_NOT_DEFINED"}
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert catches["catch_count"] == 7

    ranks = read_tsv(PACKAGE / "VALUE_CLOSURE_RANK.tsv")
    hermite = read_tsv(PACKAGE / "HERMITE_REALIZATION_ATLAS.tsv")
    assert len(ranks) == 43
    assert len(hermite) == 14
    for row in ranks:
        assert int(row["incidence_rank"]) == int(row["N"]) - 1
        assert int(row["anchored_state_dimension"]) == int(row["N"]) - 1
    for row in hermite:
        assert int(row["matrix_rank"]) == int(row["condition_count"]) == 3 * int(row["N"])
        assert row["all_jets_exact"] == "True"
    production_hermite = (
        production["radial_hermite"]["records"]
        + production["timelive_carry"]["records"]
    )
    assert len(production_hermite) == len(hermite) == 14
    for saved, row in zip(production_hermite, hermite):
        assert set(saved) == set(row)
        for key, value in saved.items():
            assert str(value) == row[key]

    report = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    assert LANDING in report and LANDING in exact

    print(json.dumps({
        "status": "PACKAGE_PASS_R2_FOLLOWUP_PENDING",
        "required_file_count": len(REQUIRED),
        "source_count": len(manifest),
        "rank_rows": len(ranks),
        "hermite_rows": len(hermite),
        "independent_graph_trials": independent["graph_trials"],
        "independent_angular_trials": independent["angular_trials"],
        "hostile_catches": catches["catch_count"],
        "landing": LANDING,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
