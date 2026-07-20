#!/usr/bin/env python3
"""Independent, fail-closed verifier for the angular derivative-weight audit."""

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
BASE = "f571842106f0a341e2b8db4e7dd64fc3e4ac03cc"
EXPECTED_CENSUS = {
    "CONTEXT_CANDIDATE": 1604,
    "LOAD_BEARING_CANDIDATE": 33,
    "EXCLUDED_DUPLICATE_RAW_RECORD": 62,
    "PROVENANCE_OR_COUNTEREXAMPLE_ONLY": 1888,
    "EXCLUDED_GENERATED_ORGANIZATION": 238,
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
    need(len(items) == 3825 and len({row["path"] for row in items}) == 3825, "census-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "census-hash-shape")
        need(row["matched_tokens"], "census-token")
        need(not row["path"].startswith("angular_derivative_weight_selector_2026-07-20/"), "census-feedback")
    need(counts == EXPECTED_CENSUS, "census-dispositions")
    return {"rows": len(items), "dispositions": counts}


def validate_sources(items: list[dict[str, str]], census: list[dict[str, str]]) -> dict[str, object]:
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    need(len(items) == 33 and len({row["path"] for row in items}) == 33, "source-count")
    need({row["path"] for row in items} == expected, "source-coverage")
    census_by_path = {row["path"]: row for row in census}
    for row in items:
        path = row["path"]
        data = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        need(hashlib.sha256(data).hexdigest() == census_by_path[path]["sha256"], f"source-sha:{path}")
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()
        need(blob == census_by_path[path]["blob"], f"source-blob:{path}")
    need(one(items, "path", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")["audit_ruling"] == "FOUNDING_SELECTOR_ONLY", "source-csn")
    need(one(items, "path", "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md")["audit_ruling"] == "ON_SHELL_REQUIREMENT_ONLY", "source-bootstrap")
    need(one(items, "path", "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"] == "CARRIER_EXCLUSION_GATE", "source-carrier")
    need(one(items, "path", "noNull_energy.py")["audit_ruling"] == "CONDITIONAL_COMPARISON_ONLY", "source-action")
    return {"rows": len(items), "base_hashes_replayed": len(items)}


def validate_invariants(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 18 and len({row["id"] for row in items}) == 18, "invariant-count")
    expected = {
        "I02": "CONDITIONAL_EXCLUSION_DERIVED",
        "I03": "COMPATIBLE_NOT_SELECTED",
        "I04": "CONDITIONAL_COMPATIBLE_NOT_SELECTED",
        "I05": "CONDITIONAL_POST_SCALE",
        "I06": "UNIQUE_CONDITIONAL_PRESERVED",
        "I10": "CONDITIONAL_COUNTERFAMILY_ONLY",
        "I12": "FORM_ONLY",
        "I14": "TOPOLOGY_FIXED_LOCAL_NORM_OPEN",
        "I15": "SQUASHING_NOT_SELECTED",
        "I16": "NOT_A_COEFFICIENT_SELECTOR",
        "I17": "NOT_YET_A_COEFFICIENT_SELECTOR",
        "I18": "WORKING_CONDITIONAL_ROUTE",
    }
    for identity, ruling in expected.items():
        need(one(items, "id", identity)["ruling"] == ruling, f"invariant:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_counterfamilies(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 8 and len({row["id"] for row in items}) == 8, "counterfamily-count")
    need(one(items, "id", "C04")["varied_freedom"].startswith("H_epsilon="), "counter-H")
    need("a/b" in one(items, "id", "C05")["varied_freedom"], "counter-squash")
    need("arbitrary dimensionless f" in one(items, "id", "C07")["varied_freedom"], "counter-X")
    return {"rows": len(items), "load_bearing": ["C01", "C04", "C05", "C07", "C08"]}


def validate_completeness(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 11 and len({row["layer"] for row in items}) == 11, "completeness-count")
    need(one(items, "layer", "external adversarial review")["status"] == "NOT_PERFORMED", "external-review")
    need(one(items, "layer", "numerics")["status"] == "NOT_RUN_BY_DESIGN", "gpu-scope")
    return {"rows": len(items), "external_review": "NOT_PERFORMED"}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 18 and len({row["id"] for row in items}) == 18, "status-count")
    expected = {
        "S01": "REFUTED_IN_BOUNDED_BRANCH",
        "S02": "DERIVED_SCOPED",
        "S03": "REFUTED_AS_SUFFICIENT",
        "S04": "UNIQUE_CONDITIONAL_PRESERVED",
        "S05": "NOT_DERIVED",
        "S06": "REFUTED_AS_AN_ALGEBRAIC_IMPLICATION",
        "S07": "CONDITIONAL_COUNTERMODEL",
        "S08": "DERIVED_CONDITIONAL",
        "S09": "REFUTED_IN_CONDITIONAL_FAMILY",
        "S10": "REFUTED_AS_SUFFICIENT",
        "S11": "NOT_DERIVED",
        "S12": "NOT_SUPPLIED",
        "S13": "FORM_ONLY",
        "S14": "VERIFIED_WITH_CAVEATS",
        "S15": "NOT_SELECTED_IN_CURRENT_FOUNDATION",
        "S16": "WORKING_CONDITIONAL_ROUTE",
        "S17": "EXCLUDED_AS_INPUT_REMAINS_CONDITIONAL",
        "S18": "OPEN",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 38, "derivation-checks")
    need(result["carrier_neutral_csn"]["ruling"] == "NONZERO_CONSTANT_K2_EXCLUDED_PRE_SCALE_IN_THIS_BRANCH; QUARTIC_FAMILY_COMPATIBLE_NOT_SELECTED", "derive-csn")
    need(result["pure_metric_branch"]["ruling"] == "C2_BACH_REMAINS_UNIQUE_CONDITIONAL; NORMALIZATION_AND_COMPLETE_ACTION_OPEN", "derive-C2")
    need(result["two_stage_bridge"]["ruling"] == "STRUCTURALLY_PROMISING_CONDITIONAL_ROUTE; EXACT_METRIC_REDUCTION_AND_SELECTION_MISSING", "derive-bridge")
    need(result["conditional_hopf_route"]["nonround_counterexample"]["Rbase_over_F2"] == "9/7", "derive-H")
    need(result["squashing"]["common_scale_invariant_modulus"] == "a/b", "derive-squash")
    need(result["xmax"]["ruling"].startswith("FORM_ONLY"), "derive-X")
    need(result["maximum_conclusion"] == "PRE_SCALE_DERIVATIVE_ORDER_SEPARATION_DERIVED_IN_NEUTRAL_BRANCH; NONZERO_RELATIVE_WEIGHT_NOT_SELECTED_IN_CURRENT_FOUNDATION", "derive-maximum")
    return {"checks": len(result["checks"]), "maximum_conclusion": result["maximum_conclusion"]}


def source_syntax_checks() -> dict[str, str]:
    csn = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    need("A native pre-scale bulk law must respect local common-scale neutrality" in csn, "syntax-CSN-law")
    need("derivative order and time-live degrees of freedom" in csn, "syntax-CSN-nonconsequence")
    need("how common-scale neutrality is broken or fixed in the material phase" in csn, "syntax-CSN-bridge-open")
    bootstrap = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(encoding="utf-8")
    need("No nonlocal insertion" in bootstrap and "separately derived global variational condition" in bootstrap, "syntax-bootstrap")
    carrier = (ROOT / "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    need("HISTORICAL WORKING POSIT, now REOPENED" in carrier, "syntax-carrier")
    xmax = (ROOT / "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    need("working posit" in xmax and "origin and value are reopened" in xmax, "syntax-Xmax")
    final = rows_from(ROOT / "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")
    need(one(final, "id", "S11")["status"] == "UNIQUE-CONDITIONAL", "syntax-C2-status")
    need(one(final, "id", "S14")["status"] == "CONDITIONAL", "syntax-EH-status")
    need(one(final, "id", "S16")["status"] == "CONDITIONAL / CHOSE", "syntax-L2L4-status")
    need(one(final, "id", "S23")["status"] == "OPEN", "syntax-action-open")
    return {"CSN": "PASS", "bootstrap": "PASS", "carrier": "PASS", "Xmax": "PASS", "frozen_action_status": "PASS"}


def rows_from(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def scalar_curvature(metric: sp.Matrix, coords: list[sp.Symbol]) -> sp.Expr:
    n = len(coords)
    inverse = sp.simplify(metric.inv())
    gamma = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                gamma[k][i][j] = sp.simplify(sum(
                    inverse[k, ell] * (
                        sp.diff(metric[ell, j], coords[i]) + sp.diff(metric[ell, i], coords[j])
                        - sp.diff(metric[i, j], coords[ell])
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
    return sp.trigsimp(sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(n) for j in range(n))))


def independent_algebra() -> dict[str, object]:
    # Recount weights without importing the primary implementation.
    spacetime_dimension = 4
    need(spacetime_dimension - 2 == 2, "independent-K2-weight")
    need(spacetime_dimension - 4 == 0, "independent-K4-weight")

    # Direct coordinate-tensor computation of the nonround quotient geometry.
    u, v = sp.symbols("u v", real=True)
    H = 1 + sp.Rational(1, 3) * sp.sin(2 * u) ** 2
    q = sp.sin(u) * sp.cos(u)
    g2 = sp.diag(H**2, q**2)
    scalar2 = scalar_curvature(g2, [u, v])
    inv2 = sp.simplify(g2.inv())
    F = sp.zeros(2)
    F[0, 1] = -2 * q
    F[1, 0] = 2 * q
    normF = sp.simplify(sum(inv2[i, k] * inv2[j, ell] * F[i, j] * F[k, ell]
                              for i in range(2) for j in range(2) for k in range(2) for ell in range(2)))
    point = {u: sp.pi / 8}
    scalar_sample = sp.simplify(scalar2.subs(point))
    norm_sample = sp.simplify(normF.subs(point))
    need(scalar_sample == sp.Rational(2592, 343), "independent-quotient-R")
    need(norm_sample == sp.Rational(288, 49), "independent-quotient-F2")
    need(sp.simplify(scalar_sample / norm_sample) == sp.Rational(9, 7), "independent-quotient-ratio")
    flux = sp.integrate(-2 * q, (u, 0, sp.pi / 2)) * 2 * sp.pi
    need(sp.simplify(flux + 2 * sp.pi) == 0, "independent-flux")

    # Direct 3D coordinate computation of two smooth Berger members.
    x1, x2 = sp.symbols("x1 x2", real=True)

    def berger_metric(aa: sp.Expr, bb: sp.Expr) -> sp.Matrix:
        cu, su = sp.cos(u), sp.sin(u)
        qq = cu * su
        out = sp.zeros(3)
        out[0, 0] = bb**2
        out[1, 1] = bb**2 * qq**2 + aa**2 * cu**4
        out[2, 2] = bb**2 * qq**2 + aa**2 * su**4
        out[1, 2] = out[2, 1] = -bb**2 * qq**2 + aa**2 * cu**2 * su**2
        return out

    round_R = scalar_curvature(berger_metric(sp.Integer(1), sp.Integer(1)), [u, x1, x2])
    squashed_R = scalar_curvature(berger_metric(sp.Integer(2), sp.Integer(3)), [u, x1, x2])
    need(sp.trigsimp(round_R - 6) == 0, "independent-round-S3")
    need(sp.trigsimp(squashed_R - sp.Rational(64, 81)) == 0, "independent-Berger")

    # Independent Derrick and global-form checks.
    rr, p, qcoef, shape2, shape4 = sp.symbols("rr p qcoef shape2 shape4", positive=True)
    energy = p * shape2 * rr + qcoef * shape4 / rr
    roots = sp.solve(sp.diff(energy, rr), rr)
    need(len(roots) == 1 and sp.simplify(roots[0] - sp.sqrt(qcoef * shape4 / (p * shape2))) == 0, "independent-Derrick")
    XX, ff, scale = sp.symbols("XX ff scale", positive=True)
    form = XX**2 * ff
    need(sp.simplify(form.subs(XX, scale * XX) / form - scale**2) == 0, "independent-X-form")
    return {
        "neutral_density_weights": {"K2": 2, "K4": 0},
        "nonround_quotient": {"R": str(scalar_sample), "F2": str(norm_sample), "ratio": "9/7", "flux": str(flux)},
        "Berger_direct_coordinate": {"round_R": str(round_R), "a2_b3_R": str(squashed_R)},
        "Derrick_root": str(roots[0]),
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
    invariants = rows("INVARIANT_LEDGER.tsv")
    counterfamilies = rows("COUNTERFAMILY_LEDGER.tsv")
    completeness = rows("COMPLETENESS_SCOPE.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "source_census": validate_census(census),
        "source_adjudication": validate_sources(sources, census),
        "invariants": validate_invariants(invariants),
        "counterfamilies": validate_counterfamilies(counterfamilies),
        "completeness": validate_completeness(completeness),
        "status": validate_status(status),
        "derivation": validate_derivation(derivation),
        "source_syntax": source_syntax_checks(),
        "independent_algebra": independent_algebra(),
    }

    catches: dict[str, str] = {}
    catches["missing_census_row_rejected"] = expect_failure("census", lambda: validate_census(census[:-1]))
    altered = copy.deepcopy(census); one(altered, "path", "LIVE.md")["sha256"] = "0" * 64
    catches["base_source_mutation_rejected"] = expect_failure("source-sha", lambda: validate_sources(sources, altered))
    catches["missing_source_adjudication_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1], census))
    altered = copy.deepcopy(sources); one(altered, "path", "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"] = "NATIVE_CARRIER"
    catches["carrier_import_rejected"] = expect_failure("carrier", lambda: validate_sources(altered, census))
    catches["missing_invariant_rejected"] = expect_failure("invariant", lambda: validate_invariants(invariants[:-1]))
    altered = copy.deepcopy(invariants); one(altered, "id", "I02")["ruling"] = "PRE_SCALE_INVARIANT"
    catches["neutral_K2_pre_scale_promotion_rejected"] = expect_failure("K2", lambda: validate_invariants(altered))
    altered = copy.deepcopy(invariants); one(altered, "id", "I03")["ruling"] = "UNIQUE_NATIVE_ACTION"
    catches["quartic_uniqueness_invention_rejected"] = expect_failure("K4", lambda: validate_invariants(altered))
    altered = copy.deepcopy(invariants); one(altered, "id", "I06")["ruling"] = "COMPLETE_NATIVE_ACTION"
    catches["C2_complete_action_promotion_rejected"] = expect_failure("C2", lambda: validate_invariants(altered))
    altered = copy.deepcopy(invariants); one(altered, "id", "I12")["ruling"] = "NUMERICAL_RATIO_SELECTED"
    catches["Xmax_form_overclaim_rejected"] = expect_failure("Xmax", lambda: validate_invariants(altered))
    catches["missing_counterfamily_rejected"] = expect_failure("counter", lambda: validate_counterfamilies(counterfamilies[:-1]))
    altered = copy.deepcopy(counterfamilies); one(altered, "id", "C04")["varied_freedom"] = "round H only"
    catches["nonround_depth_family_erasure_rejected"] = expect_failure("H", lambda: validate_counterfamilies(altered))
    altered = copy.deepcopy(counterfamilies); one(altered, "id", "C05")["varied_freedom"] = "a=b fixed"
    catches["squashing_freedom_erasure_rejected"] = expect_failure("squash", lambda: validate_counterfamilies(altered))
    altered = copy.deepcopy(counterfamilies); one(altered, "id", "C07")["varied_freedom"] = "f=1"
    catches["dimensionless_state_function_erasure_rejected"] = expect_failure("f", lambda: validate_counterfamilies(altered))
    catches["missing_status_rejected"] = expect_failure("status", lambda: validate_status(status[:-1]))
    for identity, bad, label in [
        ("S01", "DERIVED_PRE_SCALE_K2", "K2-status"),
        ("S04", "COMPLETE_NATIVE_ACTION", "C2-status"),
        ("S06", "DERIVED_BRIDGE", "gauge-bridge"),
        ("S09", "ROUNDNESS_DERIVED", "roundness"),
        ("S10", "SQUASHING_FIXED", "squash-status"),
        ("S11", "COEFFICIENT_SELECTED", "boundary"),
        ("S12", "LOCAL_COUPLING_DERIVED", "bootstrap"),
        ("S13", "NUMERICAL_RATIO_DERIVED", "X-status"),
        ("S15", "RELATIVE_WEIGHT_DERIVED", "relative-weight"),
        ("S17", "NATIVE_CARRIER_AND_ACTION", "carrier-action"),
    ]:
        altered = copy.deepcopy(status); one(altered, "id", identity)["status"] = bad
        catches[f"{label}_overclaim_rejected"] = expect_failure(label, lambda altered=altered: validate_status(altered))
    altered = copy.deepcopy(derivation); altered["xmax"]["ruling"] = "NUMERICAL_RATIO_SELECTED"
    catches["derivation_Xmax_overclaim_rejected"] = expect_failure("derive-X", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["two_stage_bridge"]["ruling"] = "COMPLETE_BRIDGE_DERIVED"
    catches["derivation_bridge_overclaim_rejected"] = expect_failure("derive-bridge", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["maximum_conclusion"] = "COMPLETE_NATIVE_MATTER_ACTION_DERIVED"
    catches["maximum_conclusion_overreach_rejected"] = expect_failure("derive-max", lambda: validate_derivation(altered))

    catch_rows = [{"catch": key, "result": value} for key, value in sorted(catches.items())]
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catch_rows)

    result = {
        "schema": "udt-angular-derivative-weight-verification-1.0",
        "result": "PASS",
        "groups": groups,
        "catch_proofs": catches,
        "counts": {"census": len(census), "sources": len(sources), "invariants": len(invariants),
                   "counterfamilies": len(counterfamilies), "completeness": len(completeness),
                   "status": len(status), "catch_proofs": len(catches)},
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "PRE_SCALE_DERIVATIVE_ORDER_SEPARATION_DERIVED_IN_NEUTRAL_BRANCH; NONZERO_RELATIVE_WEIGHT_NOT_SELECTED_IN_CURRENT_FOUNDATION",
        "certification": "VERIFIED-WITH-CAVEATS: independent coordinate-tensor algebra and base-source replay; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
