#!/usr/bin/env python3
"""Aggregate no-write verifier for the bounded G331 package."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LANDING = (
    "UNIFORM_RICCI_GAP_PRESERVES_GLOBAL_SMOOTH_EIGENLINE"
    "__ARBITRARILY_CLOSE_NONHOMOGENEOUS_METRICS_CAN_HAVE_IRREGULAR_NONCLOSED_RICCI_EIGENFLOW"
    "__HOPF_FIBRATION_AND_G330_PERIOD_NORMALIZATION_ARE_NOT_PERTURBATION_OPEN"
    "__LOCAL_DYNAMIC_CARRY_REMAINS_CONSTRAINT_COMPATIBLE_AND_GAP_CONDITIONAL"
)


def run(script, output):
    result = subprocess.run(
        ["python3", "-S", str(ROOT / script), "--output", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script} failed: {result.stderr or result.stdout}")
    return json.loads(output.read_text(encoding="utf-8")), result.stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="PACKAGE_VERIFICATION_RESULT.json")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    with tempfile.TemporaryDirectory(prefix="g331_package_") as tmp:
        tmp_path = Path(tmp)
        production, production_stdout = run("derive_nonsymmetric_eigenline.py", tmp_path / "production.json")
        independent, independent_stdout = run(
            "verify_nonsymmetric_eigenline_independent.py", tmp_path / "independent.json"
        )
        catches, catches_stdout = run("run_catch_proofs.py", tmp_path / "catches.json")

        require(production["all_passed"] and production["check_count"] == 59,
                "production_59_exact")
        require(independent["all_passed"] and independent["check_count"] == 44,
                "independent_44_exact")
        require(catches["all_caught"] and catches["catch_count"] == 10,
                "hostile_10_of_10")
        require(production["landing"] == LANDING, "landing_exact")
        require(not production["explicit_bump_constraint_compatible"],
                "bump_not_constraint_promoted")
        require(not production["weighted_family_constraint_compatible"],
                "weighted_family_not_constraint_promoted")
        require(not production["common_closed_fibre_period"], "no_common_period")
        require(not production["g330_period_normalized_integer_available"],
                "g330_integer_unavailable")
        require(not production["historical_carrier_used"], "no_historical_carrier")
        require(not production["historical_action_used"], "no_historical_action")
        require(not production["stability_claimed"], "no_stability_claim")
        require(not production["history_selected"], "no_history_selection")
        require(not production["scale_selected"] and not production["Xmax_selected"],
                "no_scale_or_xmax")
        require(not independent["imports_production_code"] and not independent["reads_production_output"],
                "independent_separation")
        require(not independent["constraint_embedding_proved"], "independent_constraint_scope")
        require("59 exact checks" in production_stdout, "production_stdout")
        require("44 exact checks" in independent_stdout, "independent_stdout")
        require("10/10 caught" in catches_stdout, "hostile_stdout")

        registered = (
            ("DERIVATION_RESULT.json", production),
            ("INDEPENDENT_VERIFICATION.json", independent),
            ("CATCH_PROOF_RESULT.json", catches),
        )
        for filename, replay in registered:
            path = ROOT / filename
            require(path.is_file(), f"registered_{filename}_exists")
            require(json.loads(path.read_text(encoding="utf-8")) == replay,
                    f"registered_{filename}_byte_content")

    required_files = (
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md",
        "EXECUTION_NOTE.md", "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md", "EVIDENCE_GATES.md", "COMMANDS.md", "RUN_RECORD.md",
        "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
    )
    for filename in required_files:
        require((ROOT / filename).is_file(), f"document_{filename}")

    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    execution = (ROOT / "EXECUTION_NOTE.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    external = (ROOT / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require("EIGENLINE_IS_GAP_OPEN__HOPF_FIBRATION_NEEDS_EXTRA_ORBIT_STRUCTURE" in prereg,
            "candidate_two_preregistered")
    require("stronger metric counterfamily discovered during derivation" in execution,
            "post_prereg_chronology_visible")
    require("weaker preregistered conclusion" in execution,
            "external_falsification_fallback")
    require("Neither explicit metric family has been proved to solve the" in audit,
            "constraint_scope_in_audit")
    require("does not claim this weighted family has been embedded" in exact,
            "constraint_scope_in_derivation")
    require("weighted_contact_metric_family\tfree-and-explored_MATHEMATICAL_CONTROL" in ledger,
            "weighted_family_provenance")
    require("Sasaki_curvature_identity\tIMPORTED_MATHEMATICAL_METHOD" in ledger,
            "sasaki_method_provenance")
    require(external.rstrip().endswith("ACCEPT__G331_BOUNDED_EIGENLINE_FIBRATION_BOUNDARY"),
            "external_review_acceptance")

    for script in ("derive_nonsymmetric_eigenline.py", "verify_nonsymmetric_eigenline_independent.py"):
        source = (ROOT / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
        require("udt_g330" not in source, f"{script}_no_production_import")

    payload = {
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "registered_outputs_replayed": True,
        "package_mutated": False,
        "landing": LANDING,
        "external_review_pending": False,
        "external_verdict": "ACCEPT__G331_BOUNDED_EIGENLINE_FIBRATION_BOUNDARY",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G331 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
