#!/usr/bin/env python3
"""Fail-closed package and source verifier for G146."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    required = (
        "PREREGISTRATION.md",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "OUTCOME_PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_multidirectional_position.py",
        "verify_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_RESULT.json",
        "REVIEW_SELF_CORRECTION.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "EVIDENCE_GATES.md",
    )
    for name in required:
        require((HERE / name).is_file(), f"required_{name}")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    require(production["landing"] == "NONUNIQUE_EXTENSIONS__SCREEN_SOLDER_OPEN",
            "production_landing")
    require(independent["landing"] == production["landing"], "independent_landing")
    require(production["checks_passed"] == 47, "production_47")
    require(independent["checks_passed"] == 31, "independent_31")
    require(production["preregistered_witness"]["mobius"] == ["20/37", "9/37", "0"],
            "mobius_exact_witness")
    require(production["preregistered_witness"]["einstein"] == ["1/2", "sqrt(3)/6", "0"],
            "einstein_exact_witness")
    require(production["preregistered_witness"]["difference"] != ["0", "0", "0"],
            "inequivalent_witness")
    require(all(row["mobius_gap"] != "0" and row["einstein_gap"] != "0"
                for row in production["closure_census"]), "production_closure_gaps_nonzero")
    require("noncollinear_boost_product_not_symmetric" in production["checks"],
            "boost_rotation_control_exercised")
    require("mobius_symbolic_global_gap" in production["checks"],
            "mobius_global_closure_exercised")
    require("einstein_symbolic_global_gap" in production["checks"],
            "einstein_global_closure_exercised")
    require("mobius_reverse_order_defect_nonzero" in production["checks"],
            "mobius_complete_reversal_gap_exercised")
    require("einstein_reverse_order_defect_nonzero" in production["checks"],
            "einstein_complete_reversal_gap_exercised")

    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    require("e3820099" in audit and "9cbb2f64" in audit, "preregistered_commits_recorded")
    require("Two exact smooth rotation-covariant position projections" in audit,
            "nonuniqueness_reported")
    require("Neither control is selected as UDT physics" in audit, "control_scope_guard")
    require("does **not** prove that UDT reciprocal depth is Lorentz rapidity" in exact,
            "lorentz_solder_guard")
    require("no-privileged-center" in exact and "angular anisotropy" in exact,
            "center_isotropy_guard")
    require("physical metric screen transport `U_gamma` remains" in prereg,
            "screen_transport_open_preregistered")
    require("OPEN_SHARPENED_TARGET" in ledger, "open_solder_ledger")
    require("OPEN_UNCHANGED" in ledger, "downstream_open_ledger")
    correction = (HERE / "REVIEW_SELF_CORRECTION.md").read_text(encoding="utf-8")
    require("axis-blind control" in correction, "axis_blind_correction")
    require("reverse-order law" in correction, "reversal_type_correction")
    require("rank-two solder" in correction, "carrier_rank_correction")
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    require("PASS__BOUNDED_TO_NONUNIQUE_POSITION_PROJECTIONS" in review,
            "fresh_adversarial_pass")
    require("47/47" in review and "31/31" in review and "48/48" in review,
            "fresh_rerun_counts")

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 6, "source_count_6")
    for row in rows:
        source = ROOT / row["path"]
        require(source.is_file(), f"source_exists_{row['path']}")
        require(sha256(source) == row["sha256"], f"source_hash_{row['path']}")

    print(f"PASS: {len(checks)}/{len(checks)} G146 package checks")


if __name__ == "__main__":
    main()
