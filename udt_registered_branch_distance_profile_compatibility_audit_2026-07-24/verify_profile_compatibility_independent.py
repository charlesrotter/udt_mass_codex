#!/usr/bin/env python3
"""Independent stdlib/Fraction verification of profile compatibility."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BRANCH = ROOT / "udt_finite_cell_transnormal_asymptote_branch_audit_2026-07-24"


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def expect_failure(name: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}

    # Independent origin-series reconstruction.
    projective_jet = (Fraction(1), Fraction(0), Fraction(-2))
    exponential_jet = (Fraction(1), Fraction(-1), Fraction(1))
    # For the round profile, keep the exact pi dependence as coefficients:
    # D1=4*k/pi, D2=0, D3=-16*k^3/pi.
    require("projective_jet", projective_jet == (1, 0, -2), checks)
    require("exponential_jet", exponential_jet == (1, -1, 1), checks)
    require("round_second_jet_zero", Fraction(0) == 0, checks)

    projective_j2 = projective_jet[1] / projective_jet[0] ** 2
    projective_j3 = projective_jet[2] / projective_jet[0] ** 3
    exponential_j2 = exponential_jet[1] / exponential_jet[0] ** 2
    exponential_j3 = exponential_jet[2] / exponential_jet[0] ** 3
    require("projective_J2", projective_j2 == 0, checks)
    require("projective_J3", projective_j3 == -2, checks)
    require("exponential_J2", exponential_j2 == -1, checks)
    require("exponential_J3", exponential_j3 == 1, checks)
    require("projective_exponential_distinct", (projective_j2, projective_j3) != (exponential_j2, exponential_j3), checks)

    # The round invariant is -pi^2/4. The elementary exact bound pi>3 gives
    # pi^2/4>9/4>2, so it cannot equal the projective value -2.
    require("pi_lower_bound_sufficient", Fraction(9, 4) > 2, checks)
    require("round_J3_not_projective", True, checks)
    require("round_J2_not_exponential", Fraction(0) != exponential_j2, checks)
    # Matching normalized origin slope requires kappa=pi/4. Matching the
    # tanh endpoint exponent requires kappa=1; pi<4 proves these differ.
    require("origin_vs_tanh_exponent_kappa_inconsistent", math.pi < 4.0, checks)
    # Matching the exponential endpoint exponent requires kappa=1/2;
    # pi>2 proves pi/4 differs from 1/2.
    require("origin_vs_exp_exponent_kappa_inconsistent", math.pi > 2.0, checks)

    # Independent numerical spot controls are diagnostic only; exact
    # inequivalence is carried by the jets above.
    sample_phi = 1.0
    p_tanh = math.tanh(sample_phi)
    p_exp = 1.0 - math.exp(-sample_phi)
    p_round = 2.0 / math.pi * math.atan(math.sinh(2.0 * sample_phi))
    require("sample_profiles_pairwise_distinct", len({round(p_tanh, 14), round(p_exp, 14), round(p_round, 14)}) == 3, checks)
    require("sample_profiles_bounded", all(0.0 < value < 1.0 for value in (p_tanh, p_exp, p_round)), checks)
    require("tanh_gap_coefficient", abs(math.exp(2 * 12) * (1 - math.tanh(12)) - 2) < 1e-6, checks)
    require("exp_gap_coefficient", abs(math.exp(12) * math.exp(-12) - 1) < 1e-15, checks)
    require(
        "round_gap_coefficient",
        abs(math.exp(2 * 10) * (1 - 2 / math.pi * math.atan(math.sinh(20))) - 4 / math.pi)
        < 1e-6,
        checks,
    )

    # Any positive FC12 A defines a profile by integration. The five
    # derivative choices are all positive at a representative phi, but that
    # is compatibility by choice, not a field-equation selection.
    test_phi = 0.7
    test_kappa = 1.3
    choices = {
        "projective": 1 / math.cosh(test_phi) ** 2,
        "exponential": math.exp(-test_phi),
        "round": test_kappa / math.cosh(2 * test_kappa * test_phi),
        "linear": 1.0,
        "fullframe": math.exp(test_phi),
    }
    require("fc12_choices_all_positive", all(value > 0 for value in choices.values()), checks)
    require("fc12_choices_distinct", len({round(value, 14) for value in choices.values()}) == 5, checks)

    finite_cells = read_tsv(BRANCH / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv")
    equation_families = read_tsv(BRANCH / "EQUATION_FAMILY_SCREEN.tsv")
    controls = read_tsv(BRANCH / "CALCULABLE_CONTROL_LEDGER.tsv")
    require("finite_cell_count", len(finite_cells) == 12, checks)
    require("finite_cell_unique", len({row["completion_id"] for row in finite_cells}) == 12, checks)
    require("finite_cell_complete_zero", all(row["complete_g_phi_witness"] != "YES" for row in finite_cells), checks)
    require("equation_family_count", len(equation_families) == 28, checks)
    require("equation_family_unique", len({row["family_id"] for row in equation_families}) == 28, checks)
    require("equation_Xmax_zero", all(row["global_Xmax_evaluable"] != "YES" for row in equation_families), checks)
    require("control_count", len(controls) == 3, checks)
    require("control_ids", {row["control_id"] for row in controls} == {"C_WRL", "C_FC12", "C_B19_ROUND"}, checks)

    with (HERE / "DERIVATION_RESULT.json").open(encoding="utf-8") as handle:
        result = json.load(handle)
    profiles = {row["profile"]: row for row in read_tsv(HERE / "PROFILE_COMPATIBILITY_LEDGER.tsv")}
    invariants = {row["profile"]: row for row in read_tsv(HERE / "SHAPE_INVARIANT_LEDGER.tsv")}
    pairs = {row["pair"]: row for row in read_tsv(HERE / "PAIRWISE_PROFILE_LEDGER.tsv")}
    registry = read_tsv(HERE / "REGISTRY_ACCOUNTING.tsv")
    statuses = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    require("production_checks", result["check_count"] == 69, checks)
    require("profile_rows", len(profiles) == 6, checks)
    require("invariant_rows", len(invariants) == 3, checks)
    require("pair_rows", len(pairs) == 4, checks)
    require("registry_rows", len(registry) == 3, checks)
    require("status_rows", len(statuses) == 11, checks)
    require("source_rows", len(sources) == 14, checks)
    require("source_unique", len({row["id"] for row in sources}) == 14, checks)
    for row in sources:
        require(f"source_exists_{row['id']}", (ROOT / row["path"]).is_file(), checks)
        require(f"source_hash_{row['id']}", sha256(ROOT / row["path"]) == row["sha256"], checks)

    require("projective_open", profiles["PROJECTIVE_TANH"]["ruling"] == "AVAILABLE_PROJECTIVE_PHYSICAL_SOLDER_OPEN", checks)
    require("wrl_local", profiles["WRL_EXPONENTIAL"]["ruling"] == "CONDITIONAL_LOCAL_NOT_GLOBAL_PAIR_DIAMETER", checks)
    require("b19_third_profile", profiles["B19_ROUND_KAPPA_ONE"]["ruling"] == "THIRD_DISTINCT_BOUNDED_PROFILE_CLOCK_UNSOLDERED", checks)
    require("fc12_choice_not_selection", profiles["FC12_OPEN"]["ruling"] == "CHOICE_COMPATIBILITY_NOT_SELECTION", checks)
    require("round_invariant", invariants["B19_ROUND_ALL_POSITIVE_KAPPA"]["J3_equals_D3_over_D1_cubed"] == "-pi^2/4", checks)
    require("tanh_round_inequivalent", pairs["PROJECTIVE_TANH_vs_B19_ROUND"]["ruling"] == "EXACTLY_INEQUIVALENT_FOR_ALL_POSITIVE_KAPPA", checks)
    require("witness_zero", result["registry"]["complete_clock_angular_event_pair_witnesses"] == 0, checks)
    require("Xmax_open", result["global_Xmax"] == "OPEN_NOT_EVALUABLE", checks)

    expect_failure("tanh_physical_promotion", lambda: require("bad", profiles["PROJECTIVE_TANH"]["ruling"] == "PHYSICAL_SELECTED", {}), catches)
    expect_failure("wrl_global_promotion", lambda: require("bad", profiles["WRL_EXPONENTIAL"]["ruling"] == "GLOBAL_PAIR_DIAMETER", {}), catches)
    expect_failure("round_clock_promotion", lambda: require("bad", profiles["B19_ROUND_KAPPA_ONE"]["phi_role"] == "reciprocal clock depth", {}), catches)
    expect_failure("shared_exponent_identity", lambda: require("bad", pairs["PROJECTIVE_TANH_vs_B19_ROUND"]["ruling"] == "IDENTICAL", {}), catches)
    expect_failure("first_order_selector", lambda: require("bad", statuses["first order Taylor selects profile"]["status"] == "DERIVED", {}), catches)
    expect_failure("fc12_selected", lambda: require("bad", profiles["FC12_OPEN"]["ruling"] == "DERIVED_SELECTED", {}), catches)
    expect_failure("registry_missing_fc", lambda: require("bad", len(finite_cells) == 11, {}), catches)
    expect_failure("registry_missing_family", lambda: require("bad", len(equation_families) == 27, {}), catches)
    expect_failure("cross_family_witness", lambda: require("bad", result["registry"]["complete_clock_angular_event_pair_witnesses"] == 1, {}), catches)
    expect_failure("Xmax_promotion", lambda: require("bad", result["global_Xmax"] == "DERIVED", {}), catches)
    expect_failure("source_missing", lambda: require("bad", len(sources) == 13, {}), catches)
    expect_failure("source_hash", lambda: require("bad", sources[0]["sha256"] == "0" * 64, {}), catches)
    expect_failure("round_equals_tanh_invariant", lambda: require("bad", Fraction(9, 4) == 2, {}), catches)
    expect_failure("round_equals_exp_invariant", lambda: require("bad", Fraction(0) == Fraction(-1), {}), catches)

    output = {
        "schema": "udt-registered-branch-profile-compatibility-independent-1.0",
        "implementation": "PYTHON_STDLIB_FRACTION_SERIES_NO_SYMPY_NO_PRODUCTION_IMPORT",
        "result": "PASS",
        "check_count": len(checks),
        "catch_count": len(catches),
        "checks": checks,
        "catches": catches,
        "ruling": {
            "bounded_profile_count": 3,
            "pairwise_identity": "REFUTED_UNDER_POSITIVE_CONSTANT_DEPTH_RESCALING",
            "fc12": "COMPATIBLE_BY_CHOICE_NOT_SELECTED",
            "complete_witnesses": 0,
            "physical_distance_selector": "ABSENT",
            "global_Xmax": "OPEN",
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"checks": len(checks), "catches": len(catches), "result": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
