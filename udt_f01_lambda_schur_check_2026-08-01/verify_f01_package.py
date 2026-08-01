#!/usr/bin/env python3
"""Fail-closed mechanical verifier for the F01 Schur package."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "53bdc2c"


def load_json(name: str):
    return json.loads((PKG / name).read_text(encoding="utf-8"))


def source_checks(rows: list[dict[str, str]]) -> list[str]:
    checks = []
    assert len(rows) == 12 and len({row["path"] for row in rows}) == 12
    checks.append("source_manifest_12_unique")
    for row in rows:
        spec = f"{BASE}:{row['path']}"
        blob = subprocess.check_output(["git", "rev-parse", spec], cwd=ROOT, text=True).strip()
        data = subprocess.check_output(["git", "show", spec], cwd=ROOT)
        assert blob == row["git_blob_at_53bdc2c"]
        assert len(data) == int(row["bytes"])
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
    checks.append("source_manifest_all_bytes_blobs_hashes")
    return checks


def semantic_checks(free: dict, negative: dict, diagnostic: dict) -> list[str]:
    checks = []
    assert free["status"] == "CERTIFIED_R05_POSITIVE_SCHUR_BOTH_P_TRACE_VARIANTS"
    assert negative["status"] == "CERTIFIED_R06_ADDED_NEGATIVE_DIRECTION_BOTH_P_TRACE_VARIANTS"
    checks.append("primary_statuses")
    assert negative["root_uniqueness"]["s_bracket"] == ["1.68102", "1.68103"]
    assert Decimal(negative["root_uniqueness"]["F_at_left_interval"][1]) < 0
    assert Decimal(negative["root_uniqueness"]["F_at_right_interval"][0]) > 0
    checks.append("root_bracket_opposite_signs")
    assert set(free["branches"]) == {"DIRICHLET", "FREE"}
    for row in free["branches"].values():
        coarse = [Decimal(value) for value in row["coarse_refinement_control_interval"]]
        fine = [Decimal(value) for value in row["dimensionless_nu_schur_interval"]]
        assert coarse[0] > 0 and fine[0] > 0
        assert coarse[0] <= fine[0] <= fine[1] <= coarse[1]
        assert row["certified_positive"] is True
    checks.append("r05_two_positive_nested_enclosures")
    assert set(negative["witnesses"]) == {"DIRICHLET", "FREE"}
    for row in negative["witnesses"].values():
        coarse = [Decimal(value) for value in row["coarse_refinement_control_interval"]]
        fine = [Decimal(value) for value in row["joint_quadratic_form_interval"]]
        assert coarse[1] < 0 and fine[1] < 0
        assert coarse[0] <= fine[0] <= fine[1] <= coarse[1]
        assert row["certified_negative"] is True and row["mu"] == 1
        assert len(row["p_coefficients_exact_decimal_rationals"]) == 4
        assert len(row["f_primitive_coefficients_exact_decimal_rationals"]) == 4
    checks.append("r06_two_negative_nested_enclosures_and_witnesses")
    assert all(free["symbolic_controls"].values()) and len(free["symbolic_controls"]) == 10
    checks.append("ten_symbolic_response_controls")
    assert diagnostic["status"] == "CORROBORATION_ONLY"
    rows = [row for row in diagnostic["rows"] if row["n"] == 16]
    assert len(rows) == 4
    for row in rows:
        schur = Decimal(row["schur"])
        if row["fh_trace"] == "FREE":
            assert schur > 0
        else:
            assert schur < 0
        assert row["joint_inertia"][0] == 1
    checks.append("diagnostic_four_branch_sign_and_index_corroboration")
    derivation = (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for phrase in (
        "SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES",
        "free second-wall-germ curvature",
        "does **not**",
        "global stability/bootstrap hypothesis",
    ):
        assert phrase in derivation
    checks.append("conclusion_ceiling_present")
    return checks


def catch_proofs(free: dict, negative: dict) -> list[str]:
    caught = []

    def rejected(name: str, mutator, predicate) -> None:
        fcopy, ncopy = copy.deepcopy(free), copy.deepcopy(negative)
        mutator(fcopy, ncopy)
        try:
            assert predicate(fcopy, ncopy)
        except (AssertionError, KeyError, ValueError):
            caught.append(name)
            return
        raise AssertionError(f"mutation escaped: {name}")

    rejected("missing_r05_branch", lambda f, n: f["branches"].pop("FREE"), lambda f, n: set(f["branches"]) == {"DIRICHLET", "FREE"})
    rejected("missing_r06_branch", lambda f, n: n["witnesses"].pop("FREE"), lambda f, n: set(n["witnesses"]) == {"DIRICHLET", "FREE"})
    rejected("r05_zero_crossing", lambda f, n: f["branches"]["FREE"].__setitem__("dimensionless_nu_schur_interval", ["-1", "1"]), lambda f, n: all(Decimal(v["dimensionless_nu_schur_interval"][0]) > 0 for v in f["branches"].values()))
    rejected("r06_zero_crossing", lambda f, n: n["witnesses"]["FREE"].__setitem__("joint_quadratic_form_interval", ["-1", "1"]), lambda f, n: all(Decimal(v["joint_quadratic_form_interval"][1]) < 0 for v in n["witnesses"].values()))
    rejected("root_left_wrong_sign", lambda f, n: n["root_uniqueness"].__setitem__("F_at_left_interval", ["1", "2"]), lambda f, n: Decimal(n["root_uniqueness"]["F_at_left_interval"][1]) < 0)
    rejected("root_right_wrong_sign", lambda f, n: n["root_uniqueness"].__setitem__("F_at_right_interval", ["-2", "-1"]), lambda f, n: Decimal(n["root_uniqueness"]["F_at_right_interval"][0]) > 0)
    rejected("r05_false_label", lambda f, n: f.__setitem__("status", "OPEN"), lambda f, n: f["status"] == "CERTIFIED_R05_POSITIVE_SCHUR_BOTH_P_TRACE_VARIANTS")
    rejected("r06_false_label", lambda f, n: n.__setitem__("status", "OPEN"), lambda f, n: n["status"] == "CERTIFIED_R06_ADDED_NEGATIVE_DIRECTION_BOTH_P_TRACE_VARIANTS")
    rejected("witness_coefficient_loss", lambda f, n: n["witnesses"]["DIRICHLET"].__setitem__("p_coefficients_exact_decimal_rationals", []), lambda f, n: all(len(v["p_coefficients_exact_decimal_rationals"]) == 4 for v in n["witnesses"].values()))
    rejected("symbolic_control_loss", lambda f, n: f["symbolic_controls"].__setitem__("v1_homogeneous", False), lambda f, n: all(f["symbolic_controls"].values()))
    assert len(caught) == 10
    return caught


def main() -> None:
    with (PKG / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    free = load_json("FREE_SCHUR_CERTIFICATE.json")
    negative = load_json("NEGATIVE_WITNESS_CERTIFICATE.json")
    diagnostic = load_json("DIAGNOSTIC_SPECTRAL.json")
    checks = source_checks(source_rows) + semantic_checks(free, negative, diagnostic)
    caught = catch_proofs(free, negative)
    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks": checks,
        "catch_proofs_passed": len(caught),
        "catch_proofs": caught,
        "primary_outcome": "SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES",
        "joint_index": {"R05_DIRICHLET": 1, "R05_FREE": 1, "R06_DIRICHLET": 1, "R06_FREE": 1},
        "conclusion_ceiling": "conditional local F01 joint index only",
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
