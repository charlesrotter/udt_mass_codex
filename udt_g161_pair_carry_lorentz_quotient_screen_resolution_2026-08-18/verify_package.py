#!/usr/bin/env python3
"""Fail-closed package verification for G161."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTCOME_CLASS = (
    "LORENTZ_QUOTIENT_AND_UNIQUE_BPLUS2_SECTION_DERIVED__SWEEP_FIXES_"
    "QUOTIENT_NOT_VERTICAL_RAPIDITY__NORMAL_TRANSPORT_INDEPENDENT__"
    "EXTRINSIC_SIMPLE_SPECTRUM_CONDITIONALLY_FIXES_FLAG"
)
LANDING = (
    "PAIR_FIRST_JET_IS_EXACT_LORENTZ_STABILIZER_QUOTIENT__POSITIVE_BPLUS2_"
    "IS_UNIQUE_TIME_ORIENTED_GAUGE_SECTION_ON_FUTURE_TIMELIKE_CLOCK_STRATUM__"
    "DISTANCE_SWEEP_FIXES_QUOTIENT_PATH_AND_FIRST_JET_NOT_VERTICAL_RAPIDITY__"
    "SCREEN_NORMAL_TRANSPORT_DOES_NOT_UNIVERSALLY_RESOLVE_TANGENT_BOOST__"
    "NORMAL_GAUGE_INVARIANT_EXTRINSIC_SIMPLE_CAUSAL_SPECTRUM_CONDITIONALLY_"
    "FIXES_PAIR_FLAG__DEGENERATE_NULL_AND_GLOBAL_STRATA_OPEN__PHYSICAL_"
    "CARRY_HISTORY_QUERY_AND_COMPLETION_OPEN"
)
BASE_REQUIRED = {
    "PREREGISTRATION.md", "SOURCE_FREEZE.md", "SOURCE_MANIFEST.tsv",
    "derive_lorentz_quotient.py", "DERIVATION_RESULT.json",
    "verify_lorentz_quotient_independent.py", "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py", "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "WITNESS_ATLAS.tsv",
    "EVIDENCE_GATES.md", "RUN_RECORD.md", "ADVERSARIAL_REVIEW_REQUEST.md",
    "FRESH_ADVERSARIAL_REVIEW.md", "verify_package.py",
}
FINAL_REQUIRED = {"PREMISE_VERIFIER_OUTPUT.txt", "REPOSITORY_TEST_OUTPUT.txt"}


def main() -> None:
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    assert not (BASE_REQUIRED - present), sorted(BASE_REQUIRED - present)

    for script in (
        "derive_lorentz_quotient.py",
        "verify_lorentz_quotient_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True,
                       stdout=subprocess.DEVNULL)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["registered_outcome_class"] == independent["registered_outcome_class"] == OUTCOME_CLASS
    assert production["source_count"] == independent["source_count"] == 10
    assert production["exact_checks"] == len(production["exact_check_names"]) == 11
    assert independent["fraction_trials"] == 700
    assert independent["raw_admissible_reconstruction_trials"] == 700
    assert independent["lorentz_quotient_trials"] == 700
    assert independent["unique_bplus2_reconstruction_trials"] == 700
    assert independent["live_vertical_first_jet_trials"] == 700
    assert independent["normal_rotation_CII_trials"] == 700
    assert catches["catch_count"] == 12 and all(item["caught"] for item in catches["caught"])
    assert catches["algebra_mutation_count"] == 5
    assert catches["metadata_guard_mutation_count"] == 7
    assert catches["metadata_guards_are_independent_semantic_proofs"] is False

    for result in (production, independent):
        assert result["finite_pair_metric_fiber"] == "left_SOplus(h)_orbit_on_time_oriented_component"
        assert result["first_jet_vertical_dimensions"] == 2
        assert result["positive_bplus2_unique_quotient_section"] is True
        assert result["positive_bplus2_is_physical_carry_selector"] is False
        assert result["smooth_distance_sweep_fixes_quotient_path"] is True
        assert result["smooth_distance_sweep_fixes_vertical_rapidity"] is False
        assert result["screen_normal_transport_universally_resolves_tangent_boost"] is False
        assert result["extrinsic_CII_simple_causal_spectrum_conditionally_fixes_flag"] is True
        assert result["pair_immersion_is_required_to_own_II"] is True
        assert result["metric_plus_bare_pair_plane_owns_II"] is False
        assert result["null_and_degenerate_strata_closed"] is False
        assert result["physical_carry_derived"] is False
        assert result["physical_history_derived"] is False

    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    assert "Verdict: `PASS`" in review or "Verdict: `PASS_WITH_CAVEATS`" in review

    final_ready = not (FINAL_REQUIRED - present)
    if final_ready:
        premise = (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text(encoding="utf-8")
        tests = (HERE / "REPOSITORY_TEST_OUTPUT.txt").read_text(encoding="utf-8")
        assert "PASS:" in premise
        assert "passed" in tests

    result = {
        "status": "PASS" if final_ready else "PRELIMINARY_PASS",
        "required_files": len(BASE_REQUIRED | (FINAL_REQUIRED if final_ready else set())),
        "source_count": 10,
        "exact_checks": 11,
        "independent_trials_per_family": 700,
        "algebra_mutation_count": 5,
        "metadata_guard_mutation_count": 7,
        "fresh_adversarial": "PASS_OR_PASS_WITH_CAVEATS",
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
