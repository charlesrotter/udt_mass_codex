#!/usr/bin/env python3
"""Independent fail-closed verification of the conditional C2 angular reduction."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "dc9aafa2d92db30594eafd28c50f99963472b61d"
EXPECTED_CENSUS = {
    "CONTEXT_CANDIDATE": 1567,
    "LOAD_BEARING_CANDIDATE": 35,
    "EXCLUDED_DUPLICATE_RAW_RECORD": 61,
    "PROVENANCE_OR_COUNTEREXAMPLE_ONLY": 1786,
    "EXCLUDED_GENERATED_ORGANIZATION": 218,
}


def need(condition: bool, message: str) -> None:
    if not bool(condition):
        raise AssertionError(message)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def one(items: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [row for row in items if row[key] == value]
    need(len(found) == 1, f"one:{key}:{value}")
    return found[0]


def validate_census(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 3667 and len({row["path"] for row in items}) == 3667, "census-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "census-hash")
        need(row["matched_tokens"], "census-token")
        need(not row["path"].startswith("c2_angular_reduction_selector_2026-07-20/"), "census-feedback")
    need(counts == EXPECTED_CENSUS, "census-dispositions")
    return {"rows": len(items), "dispositions": counts}


def validate_sources(items: list[dict[str, str]], census: list[dict[str, str]]) -> dict[str, object]:
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    need(len(items) == 35 and len({row["path"] for row in items}) == 35, "source-count")
    need({row["path"] for row in items} == expected, "source-coverage")
    census_by_path = {row["path"]: row for row in census}
    for row in items:
        path = row["path"]
        data = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        need(hashlib.sha256(data).hexdigest() == census_by_path[path]["sha256"], f"source-sha:{path}")
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()
        need(blob == census_by_path[path]["blob"], f"source-blob:{path}")
    need(one(items, "path", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")["audit_ruling"] == "FOUNDING_SELECTOR", "source-CSN")
    need(one(items, "path", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")["audit_ruling"] == "FROZEN_ACTION_STATUS", "source-action")
    need(one(items, "path", "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md")["audit_ruling"] == "METRIC_COMPLETENESS_WARNING", "source-Cartan")
    need(one(items, "path", "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"] == "CARRIER_EXCLUSION", "source-carrier")
    return {"rows": len(items), "base_hashes_replayed": len(items)}


def validate_equations(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 16 and len({row["id"] for row in items}) == 16, "equation-count")
    expected = {
        "E01": "DERIVED_CONDITIONAL", "E02": "DERIVED_CONDITIONAL",
        "E03": "DERIVED_CONDITIONAL", "E04": "DERIVED_DIAGNOSTIC",
        "E05": "DERIVED_DIAGNOSTIC", "E06": "DERIVED_CONDITIONAL",
        "E07": "DERIVED_CONDITIONAL", "E08": "DERIVED_CONDITIONAL",
        "E09": "REFUTED_AS_FULL_SOLUTION", "E10": "DERIVED_CONDITIONAL_SOLUTION",
        "E11": "DERIVED_CONDITIONAL_METRIC_TERM", "E12": "DERIVED_DIAGNOSTIC",
        "E13": "DERIVED_SCOPED", "E14": "OPEN_NOT_AN_EQUATION",
        "E15": "NOT_SUPPLIED", "E16": "OPEN",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"equation:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_branches(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 8 and len({row["id"] for row in items}) == 8, "branch-count")
    expected = {
        "B01": "SURVIVES_CONDITIONALLY",
        "B02": "FALSE_REDUCED_CANDIDATE_REJECTED",
        "B03": "FALSE_PARTIAL_CANDIDATE_REJECTED",
        "B04": "EXCLUDED_IN_FULL_COMPACT_PRODUCT_BACH_SLICE",
        "B05": "OPEN_BOUNDARY_BRANCH",
        "B06": "OPEN_TIME_LIVE_BRANCH",
        "B07": "OPEN_GLOBAL_GEOMETRY_BRANCH",
        "B08": "CONDITIONAL_GEOMETRIC_BRIDGE_ONLY",
    }
    for identity, ruling in expected.items():
        need(one(items, "id", identity)["ruling"] == ruling, f"branch:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_completeness(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 11 and len({row["layer"] for row in items}) == 11, "completeness-count")
    need(one(items, "layer", "external adversarial review")["status"] == "NOT_PERFORMED", "external-review")
    need(one(items, "layer", "carrier and matter")["status"] == "NOT_PART_OF_SOLVE", "matter-scope")
    return {"rows": len(items), "external_review": "NOT_PERFORMED"}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 15 and len({row["id"] for row in items}) == 15, "status-count")
    expected = {
        "S01": "DERIVED_CONDITIONAL", "S02": "DERIVED_CONDITIONAL",
        "S03": "DERIVED_CONDITIONAL", "S04": "OBSERVED_EXACT_FALSE_CANDIDATE",
        "S05": "OBSERVED_EXACT_FALSE_CANDIDATE", "S06": "DERIVED_CONDITIONAL",
        "S07": "REFUTED_IN_SLICE", "S08": "DERIVED_CONDITIONAL",
        "S09": "REFUTED_CONFLATION", "S10": "NOT_DERIVED",
        "S11": "NOT_DERIVED", "S12": "NOT_SUPPLIED",
        "S13": "FALSE_EXCLUDED", "S14": "VERIFIED_WITH_CAVEATS", "S15": "OPEN",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 25, "derivation-checks")
    need(result["general_dimensionless_density"]["C4_squared"] == "4/(3 H^4)*[(k w+4(1-s^2))^2+3 s^2 w^2]", "derive-density")
    need(result["general_dimensionless_density"]["zero_branch"].startswith("H'=0 and s=1"), "derive-zero")
    need(result["reduced_stationarity"]["simultaneous_constant_branch"] == "s=1 only", "derive-reduced")
    need(result["full_Bach_gate"]["nonround_reduced_root_B00_euclidean"] == "-128/75", "derive-Bach")
    need(result["quadratic_expansion"]["test_mode_action_coefficient"] == "256*pi^2/5 per unit dimensionless proper time", "derive-mode")
    need(result["maximum_conclusion"] == "CONDITIONAL_ROUND_ANGULAR_SHAPE_SELECTION_IN_COMPACT_STATIC_PRODUCT_C2_SLICE; CONDITIONAL_TWO_DERIVATIVE_METRIC_SHAPE_TERM; MATERIAL_WEIGHTING_AND_FULL_BRIDGE_OPEN", "derive-maximum")
    return {"checks": len(result["checks"]), "maximum_conclusion": result["maximum_conclusion"]}


def direct_ricci_invariants(Hexpr: sp.Expr, squash_squared: sp.Expr, sample: sp.Expr) -> dict[str, sp.Expr]:
    eta, x1, x2 = sp.symbols("eta x1 x2", real=True)
    c, s = sp.cos(eta), sp.sin(eta); q = c * s
    metric = sp.zeros(3)
    metric[0, 0] = Hexpr**2
    metric[1, 1] = q**2 + squash_squared * c**4
    metric[2, 2] = q**2 + squash_squared * s**4
    metric[1, 2] = metric[2, 1] = -q**2 + squash_squared * c**2 * s**2
    coords = [eta, x1, x2]; inverse = sp.simplify(metric.inv()); n = 3
    gamma = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for left in range(n):
            for right in range(n):
                gamma[upper][left][right] = sp.simplify(sum(
                    inverse[upper, ell] * (
                        sp.diff(metric[ell, right], coords[left]) + sp.diff(metric[ell, left], coords[right])
                        - sp.diff(metric[left, right], coords[ell])
                    ) for ell in range(n)
                ) / 2)
    ricci = sp.zeros(n)
    for i in range(n):
        for j in range(n):
            ricci[i, j] = sp.simplify(sum(
                sp.diff(gamma[k][i][j], coords[k]) - sp.diff(gamma[k][i][k], coords[j])
                + sum(gamma[k][k][ell] * gamma[ell][i][j] - gamma[k][j][ell] * gamma[ell][i][k]
                      for ell in range(n))
                for k in range(n)
            ))
    substitution = {eta: sample}
    inv_point = sp.simplify(inverse.subs(substitution)); ricci_point = sp.simplify(ricci.subs(substitution))
    scalar = sp.simplify(sum(inv_point[i, j] * ricci_point[i, j] for i in range(n) for j in range(n)))
    ricci2 = sp.simplify(sum(inv_point[i, k] * inv_point[j, ell] * ricci_point[i, j] * ricci_point[k, ell]
                             for i in range(n) for j in range(n) for k in range(n) for ell in range(n)))
    tf2 = sp.factor(ricci2 - scalar**2 / 3)
    return {"R": scalar, "Ricci2": ricci2, "TF2": tf2, "C4_squared": sp.factor(2 * tf2)}


def source_syntax_checks() -> dict[str, str]:
    csn = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    need("A native pre-scale bulk law must respect local common-scale neutrality" in csn, "syntax-CSN")
    bootstrap = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(encoding="utf-8")
    need("No nonlocal insertion" in bootstrap, "syntax-bootstrap")
    carrier = (ROOT / "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    need("HISTORICAL WORKING POSIT, now REOPENED" in carrier, "syntax-carrier")
    cartan = (ROOT / "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8")
    need("Cartan geometry faithfully describes a chosen metric's local curvature and transport; it does not choose" in cartan, "syntax-Cartan")
    final = rows_from(ROOT / "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")
    need(one(final, "id", "S11")["status"] == "UNIQUE-CONDITIONAL", "syntax-C2")
    need(one(final, "id", "S23")["status"] == "OPEN", "syntax-action-open")
    return {"CSN": "PASS", "bootstrap": "PASS", "carrier": "PASS", "Cartan": "PASS", "frozen_action": "PASS"}


def rows_from(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def independent_algebra() -> dict[str, object]:
    eta = sp.symbols("eta", real=True)
    explicit_H = 1 + sp.Rational(1, 3) * sp.sin(2 * eta) ** 2
    sample = direct_ricci_invariants(explicit_H, sp.Rational(4, 9), sp.pi / 8)
    need(sample["R"] == sp.Rational(2368, 343), "direct-sample-R")
    need(sample["Ricci2"] == sp.Rational(2366976, 117649), "direct-sample-Ricci2")
    need(sample["C4_squared"] == sp.Rational(2987008, 352947), "direct-sample-C2")

    false_root = direct_ricci_invariants(sp.Integer(1), sp.Rational(1, 5), sp.pi / 8)
    need(false_root["TF2"] == sp.Rational(512, 75), "direct-false-TF")
    need(false_root["C4_squared"] == sp.Rational(1024, 75), "direct-false-C2")
    bach00 = -false_root["TF2"] / 4
    need(bach00 == -sp.Rational(128, 75), "direct-false-Bach00")

    round_branch = direct_ricci_invariants(sp.Integer(1), sp.Integer(1), sp.pi / 8)
    need(round_branch["TF2"] == 0 and round_branch["C4_squared"] == 0, "direct-round")

    # Independently vary the reduced density rather than importing primary roots.
    H, Hp, Hpp, k, q, z = sp.symbols("H Hp Hpp k q z", positive=True)
    density = sp.Rational(4, 3) * z * q / H**5 * (
        (k * Hp + 4 * (1 - z**2) * H) ** 2 + 3 * z**2 * Hp**2
    )
    constant_action = sp.integrate(sp.Rational(64, 3) * z * (1-z**2)**2 * sp.sin(eta)*sp.cos(eta),
                                   (eta, 0, sp.pi/2)) * 4 * sp.pi**2
    derivative_z = sp.factor(sp.diff(constant_action, z))
    need(sp.simplify(derivative_z.subs(z, 1)) == 0, "independent-z-round")
    need(sp.simplify(derivative_z.subs(z, sp.sqrt(sp.Rational(1, 5)))) == 0, "independent-z-false")
    momentum = sp.diff(density, Hp)
    kp, qp = sp.symbols("kp qp", real=True)
    total = sum(sp.diff(momentum, variable) * derivative for variable, derivative in
                ((H, Hp), (Hp, Hpp), (k, kp), (q, qp)))
    EL = sp.factor((total - sp.diff(density, H)).subs({qp: k*q, kp: -4-k**2}))
    ELconstant = sp.factor(EL.subs({H: 1, Hp: 0, Hpp: 0}))
    need(sp.simplify(ELconstant.subs(z, 1)) == 0, "independent-H-round")
    need(sp.simplify(ELconstant.subs(z, sp.sqrt(sp.Rational(1, 3)))) == 0, "independent-H-partial")
    need(sp.simplify(ELconstant.subs(z, sp.sqrt(sp.Rational(1, 5)))) != 0, "independent-H-reject-false")

    # Independent sectional-curvature expansion for the round-orbit H mode.
    e = sp.symbols("e", real=True); h = sp.sin(2*eta)**2; Hmode = 1 + e*h
    K01 = 1/Hmode**2 - sp.tan(eta)*sp.diff(Hmode, eta)/Hmode**3
    K02 = 1/Hmode**2 + sp.cot(eta)*sp.diff(Hmode, eta)/Hmode**3
    K12 = 1/Hmode**2
    lambdas = [K01+K02, K01+K12, K02+K12]
    R = sum(lambdas); TF2 = sp.simplify(sum(value**2 for value in lambdas)-R**2/3)
    volume = Hmode*sp.sin(eta)*sp.cos(eta)
    coefficient = sp.simplify(sp.diff(volume*2*TF2, e, 2).subs(e, 0)/2)
    integrated = sp.integrate(coefficient, (eta, 0, sp.pi/2))*4*sp.pi**2
    need(sp.simplify(integrated-sp.Rational(256, 5)*sp.pi**2) == 0, "independent-mode")
    return {
        "direct_nonround_sample": {key: str(value) for key, value in sample.items()},
        "direct_false_root": {key: str(value) for key, value in false_root.items()},
        "direct_false_Bach00": str(bach00),
        "direct_round_C4_squared": str(round_branch["C4_squared"]),
        "sectional_mode_coefficient": str(integrated),
    }


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except (AssertionError, KeyError, subprocess.CalledProcessError):
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    census = rows("SOURCE_CENSUS.tsv")
    sources = rows("SOURCE_ADJUDICATION.tsv")
    equations = rows("EQUATION_LEDGER.tsv")
    branches = rows("CANDIDATE_BRANCHES.tsv")
    completeness = rows("COMPLETENESS_SCOPE.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "source_census": validate_census(census),
        "source_adjudication": validate_sources(sources, census),
        "equations": validate_equations(equations),
        "branches": validate_branches(branches),
        "completeness": validate_completeness(completeness),
        "status": validate_status(status),
        "derivation": validate_derivation(derivation),
        "source_syntax": source_syntax_checks(),
        "independent_algebra": independent_algebra(),
    }

    catches: dict[str, str] = {}
    catches["missing_census_row_rejected"] = expect_failure("census", lambda: validate_census(census[:-1]))
    altered = copy.deepcopy(census); one(altered, "path", "LIVE.md")["sha256"] = "0"*64
    catches["base_source_mutation_rejected"] = expect_failure("source-hash", lambda: validate_sources(sources, altered))
    catches["missing_source_adjudication_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1], census))
    altered = copy.deepcopy(sources); one(altered, "path", "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"] = "NATIVE_CARRIER"
    catches["carrier_import_rejected"] = expect_failure("carrier", lambda: validate_sources(altered, census))
    catches["missing_equation_rejected"] = expect_failure("equation", lambda: validate_equations(equations[:-1]))
    for identity, bad, label in [
        ("E01", "UNCONDITIONAL_FULL_METRIC", "product"),
        ("E03", "FOUNDING_ROUNDNESS", "roundness"),
        ("E04", "FULL_SOLUTION", "frozen-H"),
        ("E08", "PHYSICAL_FINITE_CELL_THEOREM", "compact-boundary"),
        ("E09", "BACH_SOLUTION", "false-root"),
        ("E11", "CARRIER_L2", "metric-carrier"),
        ("E14", "DERIVED_BOUNDARY_EQUATION", "boundary"),
        ("E15", "BOOTSTRAP_EIGENVALUE_DERIVED", "bootstrap"),
        ("E16", "MATERIAL_WEIGHT_DERIVED", "material"),
    ]:
        altered = copy.deepcopy(equations); one(altered, "id", identity)["status"] = bad
        catches[f"{label}_overclaim_rejected"] = expect_failure(label, lambda altered=altered: validate_equations(altered))
    catches["missing_branch_rejected"] = expect_failure("branch", lambda: validate_branches(branches[:-1]))
    altered = copy.deepcopy(branches); one(altered, "id", "B02")["ruling"] = "SURVIVES"
    catches["partial_false_branch_acceptance_rejected"] = expect_failure("B02", lambda: validate_branches(altered))
    altered = copy.deepcopy(branches); one(altered, "id", "B05")["ruling"] = "EXCLUDED_BY_COMPACT_THEOREM"
    catches["physical_boundary_silent_exclusion_rejected"] = expect_failure("B05", lambda: validate_branches(altered))
    altered = copy.deepcopy(branches); one(altered, "id", "B06")["ruling"] = "SOLVED"
    catches["time_live_completion_invention_rejected"] = expect_failure("B06", lambda: validate_branches(altered))
    catches["missing_status_rejected"] = expect_failure("status", lambda: validate_status(status[:-1]))
    for identity, bad, label in [
        ("S06", "UNCONDITIONAL_UDT_ROUNDNESS", "status-round"),
        ("S07", "PHYSICAL_SCALE_SELECTED", "status-scale"),
        ("S09", "NATIVE_CARRIER_L2", "status-carrier"),
        ("S10", "L2_L4_WEIGHT_DERIVED", "status-weight"),
        ("S11", "PHYSICAL_WALL_DERIVED", "status-wall"),
        ("S12", "BOOTSTRAP_EQUATION_DERIVED", "status-bootstrap"),
        ("S13", "ELECTRON_MASS_INPUT", "status-electron"),
        ("S15", "COMPLETE_ACTION", "status-action"),
    ]:
        altered = copy.deepcopy(status); one(altered, "id", identity)["status"] = bad
        catches[f"{label}_overclaim_rejected"] = expect_failure(label, lambda altered=altered: validate_status(altered))
    altered = copy.deepcopy(derivation); altered["reduced_stationarity"]["simultaneous_constant_branch"] = "s=1/sqrt(5)"
    catches["derivation_partial_root_promotion_rejected"] = expect_failure("derive-root", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["quadratic_expansion"]["test_mode_action_coefficient"] = "native carrier coefficient"
    catches["derivation_metric_carrier_conflation_rejected"] = expect_failure("derive-carrier", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["maximum_conclusion"] = "COMPLETE_NATIVE_MATTER_ACTION_DERIVED"
    catches["maximum_conclusion_overreach_rejected"] = expect_failure("derive-max", lambda: validate_derivation(altered))

    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows({"catch": key, "result": value} for key, value in sorted(catches.items()))

    result = {
        "schema": "udt-conditional-c2-angular-reduction-verification-1.0",
        "result": "PASS", "groups": groups, "catch_proofs": catches,
        "counts": {"census": len(census), "sources": len(sources), "equations": len(equations),
                   "branches": len(branches), "completeness": len(completeness), "status": len(status),
                   "catch_proofs": len(catches)},
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "CONDITIONAL_ROUND_ANGULAR_SHAPE_SELECTION_IN_COMPACT_STATIC_PRODUCT_C2_SLICE; CONDITIONAL_TWO_DERIVATIVE_METRIC_SHAPE_TERM; MATERIAL_WEIGHTING_AND_FULL_BRIDGE_OPEN",
        "certification": "VERIFIED-WITH-CAVEATS: independent coordinate Ricci and sectional-curvature implementation; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches),
                      "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
