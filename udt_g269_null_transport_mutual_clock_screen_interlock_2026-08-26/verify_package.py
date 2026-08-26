#!/usr/bin/env python3
"""Fail-closed, no-persistent-output G269 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = (
    "METRIC_OWNS_A_QUERY_RELATIVE_NULL_TRANSPORT_MUTUAL_CLOCK_SCALAR__"
    "M_PT_IS_BOUNDED_ABOVE_BY_SECH_DELTA__"
    "EQUALITY_IFF_THE_TARGET_CLOCK_IS_IN_THE_TRANSPORTED_NULL_PAIR_PLANE__"
    "NONZERO_SCREEN_MISMATCH_MAKES_THE_INEQUALITY_STRICT__"
    "NO_QUERY_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(name: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / name), "--no-write"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def resolve_source(relative: str, expected: str) -> Path:
    for candidate in (REPO / relative, REPO / "private_sources" / relative):
        if candidate.is_file() and sha256(candidate) == expected:
            return candidate
    raise AssertionError(f"sealed source absent or changed: {relative}")


def main() -> None:
    required = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_transport_interlock.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_transport_independent.py",
    )
    assert all((ROOT / name).is_file() for name in required)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 11
    for row in sources:
        resolve_source(row["path"], row["sha256"])

    recorded_paths = (
        ROOT / "DERIVATION_RESULT.json",
        ROOT / "INDEPENDENT_VERIFICATION.json",
        ROOT / "CATCH_PROOF_RESULT.json",
    )
    before = {path.name: sha256(path) for path in recorded_paths}
    production = run_json("derive_transport_interlock.py")
    independent = run_json("verify_transport_independent.py")
    catches = run_json("run_catch_proofs.py")
    after = {path.name: sha256(path) for path in recorded_paths}
    assert before == after

    assert production == json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    assert independent == json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["expected_landing"] == LANDING
    assert production["selected_alternative"] == "N2__SCREEN_INTERLOCK"
    assert production["exact_checks"] == 34
    assert production["sharp_bound"] == "0<M_PT<=sech(delta_AB)"
    assert production["equality_condition"] == "M_PT=sech(delta_AB) iff ||W_AB||^2=0"
    assert production["query_population"] == "OPEN_NOT_SELECTED"
    assert production["history_distance_xmax"] == "OPEN_NOT_TESTED"
    assert production["off_planar_witness"] == {
        "M_PT": "4/9",
        "r": "2",
        "screen_component": "1",
        "sech_delta": "4/5",
    }

    assert independent["cases"] == 12000
    assert independent["assertions"] == 143715
    assert independent["planar_cases"] == 387
    assert independent["transverse_cases"] == 11613
    assert independent["fixed_r_distinct_mutual_values"] == 101
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False

    expected_mutations = {
        "reversed_frequency_ratio": "frequency_ratio_orientation",
        "missing_inverse_mutual": "inverse_gamma_readout",
        "wrong_longitudinal_sign": "frequency_contraction",
        "deleted_screen_term": "screen_interlock",
        "negative_screen_norm": "screen_nonnegative",
        "universal_nonplanar_equality": "nonplanar_equality_rejection",
        "reversal_not_even": "reversal_evenness",
        "affine_scale_leak": "affine_invariance",
        "jacobi_area_conflation": "no_jacobi_area_conflation",
        "query_history_promotion": "no_query_history_selection",
    }
    assert catches["baseline_failures"] == []
    assert catches["catches"] == 10 and catches["missed"] == []
    assert catches["shared_validator_exercised"] is True
    assert set(catches["mutations"]) == set(expected_mutations)
    for name, target in expected_mutations.items():
        item = catches["mutations"][name]
        assert item["caught"] is True
        assert item["targeted_caught"] is True
        assert item["targeted_failure"] == target
        assert target in item["failures"]

    assert "c79f29e6" in (ROOT / "PREREGISTRATION_EXECUTION_NOTE.md").read_text()
    premise_text = (ROOT / "PREMISE_LEDGER.tsv").read_text()
    assert "WORKING_OPERATIONAL_READOUT" in premise_text
    assert "OPEN_OMITTED" in premise_text
    gates_text = (ROOT / "EVIDENCE_GATES.md").read_text()
    assert "FRESH_EXTERNAL_REVIEW_ACCEPTED_NO_REPAIRS__VERIFIED_WITH_CAVEATS" in gates_text
    review_text = (ROOT / "EXTERNAL_REVIEW.md").read_text()
    assert "ACCEPT_NO_REPAIRS" in review_text
    assert "No defects found in the permitted sealed-intake scope." in review_text

    print(json.dumps({
        "status": "PASS",
        "grade": "FRESH_EXTERNAL_REVIEW_ACCEPTED_NO_REPAIRS__VERIFIED_WITH_CAVEATS",
        "landing": LANDING,
        "selected_alternative": production["selected_alternative"],
        "exact_checks": production["exact_checks"],
        "independent_cases": independent["cases"],
        "independent_assertions": independent["assertions"],
        "mutation_catches": catches["catches"],
        "source_count": len(sources),
        "off_planar_witness": production["off_planar_witness"],
        "recorded_artifacts_unchanged": before == after,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
