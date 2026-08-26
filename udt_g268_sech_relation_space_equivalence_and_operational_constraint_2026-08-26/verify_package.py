#!/usr/bin/env python3
"""Dependency-aware, no-persistent-output G268 package verifier."""

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
    "FINITE_REGULAR_SECH_STATE_IS_EXACTLY_EQUIVALENT_TO_THE_RECIPROCAL_RELATION_SPACE__"
    "COMPACT_ENDPOINTS_FORM_ONLY_A_PARTIAL_NONGROUP_CLOSURE__"
    "INDEPENDENT_M_WOULD_GIVE_A_CONDITIONAL_CROSS_READOUT_LAW__"
    "NO_RELATION_NETWORK_HISTORY_DISTANCE_OR_XMAX_SELECTION"
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
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "derive_relation_equivalence.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_package.py",
    )
    assert all((ROOT / name).is_file() for name in required)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 10
    for row in sources:
        resolve_source(row["path"], row["sha256"])

    recorded_paths = (
        ROOT / "DERIVATION_RESULT.json",
        ROOT / "INDEPENDENT_VERIFICATION.json",
        ROOT / "CATCH_PROOF_RESULT.json",
    )
    before = {path.name: sha256(path) for path in recorded_paths}
    production = run_json("derive_relation_equivalence.py")
    independent = run_json("verify_independent.py")
    catches = run_json("run_catch_proofs.py")
    after = {path.name: sha256(path) for path in recorded_paths}
    assert before == after

    assert production == json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    assert independent == json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["expected_landing"] == LANDING
    assert production["relation_space_landing"] == "R0__EXACT_EQUIVALENCE_ONLY"
    assert production["boundary_landing"] == "R2__BOUNDARY_ONLY_CHANGE"
    assert production["operational_landing"] == "O1__CONDITIONAL_CROSS_READOUT_LAW"
    assert production["owned_operational_protocol"] is False
    assert production["regular_relation_rejections"] == 0
    assert production["finite_network_rejections"] == 0
    assert production["history_rejections"] == 0
    assert production["compact_closure_total_group"] is False
    assert production["exact_checks"] == 41
    assert production["global_interior_diffeomorphism"] is True
    assert production["analytic_scope_conclusions_not_counted_as_symbolic_checks"] == {
        "finite_network_rejections": 0,
        "history_rejections": 0,
        "owned_operational_protocol": False,
        "regular_relation_rejections": 0,
    }
    forbidden_symbolic_keys = {
        "existing_relation_rejections",
        "finite_network_rejections",
        "global_interior_diffeomorphism",
        "history_rejections",
        "owned_operational_protocol",
        "regular_relation_rejections",
    }
    assert forbidden_symbolic_keys.isdisjoint(production["checks"])
    assert independent["ratio_cases"] == 1100
    assert independent["composition_cases"] == 6000
    assert independent["associativity_cases"] == 2000
    assert independent["network_cases"] == 1200
    assert independent["network_edge_checks"] == 34742
    assert independent["assertions"] == 95617
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert catches["catches"] == 8 and not catches["missed"]
    assert catches["baseline_failures"] == []
    assert catches["shared_validator_exercised"] is True
    expected_mutation_failures = {
        "loss_of_chi_sign": "reversal_sign",
        "wrong_inverse_r": "inverse_reconstruction",
        "multiplicative_m": "composition_law",
        "deleted_composition_denominator": "composition_law",
        "off_circle_state_accepted": "off_circle_rejection",
        "opposite_endpoints_called_regular": "opposite_endpoint_rejection",
        "history_rejection_injected": "zero_history_selection",
        "operational_ownership_injected": "open_protocol_ownership",
    }
    assert set(catches["mutations"]) == set(expected_mutation_failures)
    for name, targeted_failure in expected_mutation_failures.items():
        mutation = catches["mutations"][name]
        assert mutation["caught"] is True
        assert mutation["targeted_caught"] is True
        assert mutation["targeted_failure"] == targeted_failure
        assert targeted_failure in mutation["failures"]
    assert "fc9b13ca" in (ROOT / "PREREGISTRATION_EXECUTION_NOTE.md").read_text()
    premise_text = (ROOT / "PREMISE_LEDGER.tsv").read_text()
    assert "SUPPLIED_PROVISIONAL_CANDIDATE" in premise_text
    assert "OPEN/HYPOTHETICAL_CONDITIONAL" in premise_text
    assert "EXTERNAL_ACCEPT_WITH_REPAIRS__REPAIRS_IMPLEMENTED_AWAITING_FOLLOWUP" in (
        ROOT / "EVIDENCE_GATES.md"
    ).read_text()

    print(json.dumps({
        "status": "PASS",
        "grade": "EXTERNAL_ACCEPT_WITH_REPAIRS__REPAIRS_IMPLEMENTED_AWAITING_FOLLOWUP",
        "landing": LANDING,
        "relation_space_landing": production["relation_space_landing"],
        "boundary_landing": production["boundary_landing"],
        "operational_landing": production["operational_landing"],
        "owned_operational_protocol": production["owned_operational_protocol"],
        "exact_checks": production["exact_checks"],
        "independent_assertions": independent["assertions"],
        "mutation_catches": catches["catches"],
        "source_count": len(sources),
        "regular_relation_rejections": production["regular_relation_rejections"],
        "finite_network_rejections": production["finite_network_rejections"],
        "history_rejections": production["history_rejections"],
        "recorded_artifacts_unchanged": before == after,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
