#!/usr/bin/env python3
"""Independent fail-closed verifier for boundary charge and scale rank."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def one(items: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [row for row in items if row[key] == value]
    need(len(found) == 1, f"one:{key}:{value}")
    return found[0]


def validate_candidates(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 476 and len({row["path"] for row in items}) == 476, "candidate-census")
    need(sum(bool(row["matched_tokens"]) for row in items) == 471, "token-hits")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "candidate-hash")
    expected = {
        "CONTEXT_ONLY": 79,
        "DUPLICATE_OR_AUDIT_RECORD": 41,
        "EXCLUDED_WITH_REASON": 289,
        "LOAD_BEARING": 27,
        "NEGATIVE_CONTROL": 40,
    }
    need(counts == expected, "candidate-dispositions")
    return {"rows": len(items), "token_hits": 471, "dispositions": counts}


def validate_sources(items: list[dict[str, str]], candidates: list[dict[str, str]]) -> dict[str, object]:
    expected = {row["path"] for row in candidates if row["initial_disposition"] == "LOAD_BEARING"}
    need(len(items) == 27 and {row["path"] for row in items} == expected, "source-coverage")
    need(one(items, "path", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")["evidence_grade"] == "FOUNDING", "csn-source")
    need(one(items, "path", "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md")["evidence_grade"] == "WORKING", "bootstrap-source")
    need(one(items, "path", "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md")["evidence_grade"] == "WORKING_LEAD", "xmax-source")
    need(one(items, "path", "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_solution_space_closure.py")["current_use"] == "YES_ALGEBRA_ONLY", "archive-executable")
    return {"rows": len(items), "families": len({row["source_family"] for row in items})}


def validate_charge(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 16 and len({row["id"] for row in items}) == 16, "charge-census")
    need(one(items, "id", "C02")["current_status"] == "DERIVED_METRIC_LIMIT", "finite-flux")
    need(one(items, "id", "C03")["current_status"] == "FAILS_FOR_RAW_FLUX", "not-conserved")
    need(one(items, "id", "C04")["current_status"] == "DERIVED_METRIC_IDENTITY", "bulk-budget")
    need(one(items, "id", "C05")["current_status"] == "OPEN", "action-open")
    need(one(items, "id", "C07")["current_status"] == "OPEN", "boundary-open")
    need(one(items, "id", "C09")["current_status"] == "OPEN", "normalization-open")
    need(one(items, "id", "C16")["current_status"] == "OPEN", "mass-open")
    return {"rows": len(items), "open": sum(row["current_status"] == "OPEN" for row in items)}


def validate_scale(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 20 and len({row["id"] for row in items}) == 20, "scale-census")
    need(one(items, "id", "R01")["status"] == "DERIVED", "determinant")
    need(one(items, "id", "R02")["status"] == "DERIVED_RANK_ONE", "rank-one")
    need("continuum" in one(items, "id", "R02")["information_rank"], "continuum")
    need(one(items, "id", "E05")["status"] == "OPEN", "density-center-open")
    need(one(items, "id", "E07")["status"] == "FOUNDING_NEUTRALITY", "csn-neutral")
    need(one(items, "id", "R04")["status"] == "DERIVED_DIMENSION_COUNT", "cG-dimension")
    need(one(items, "id", "R05")["status"] == "WORKING_COHERENT", "owner-proposal")
    return {"rows": len(items)}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 15 and len({row["id"] for row in items}) == 15, "status-census")
    need(one(items, "id", "S03")["status"] == "REFUTED_IN_WRL_INTERIOR", "raw-conservation")
    need(one(items, "id", "S05")["status"] == "OPEN", "raw-mass-open")
    need(one(items, "id", "S06")["status"] == "REFUTED_AS_SUFFICIENT", "metric-normalization")
    need(one(items, "id", "S09")["status"] == "REFUTED_AS_SUFFICIENT", "linear-pair")
    need(one(items, "id", "S11")["status"] == "OPEN_NOT_SUPPLIED", "csn-selector")
    need(one(items, "id", "S12")["status"] == "OPEN_NOT_SUPPLIED", "bootstrap-center")
    need(one(items, "id", "S14")["status"] == "WORKING_COHERENT", "owner-closure")
    return {"rows": len(items)}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 25, "derivation-checks")
    metric = result["metric_flux"]
    need(metric["profile"] == "Phi_N(r)=-2*pi*r^2/X", "flux-profile")
    need(metric["radial_derivative"].endswith("!= 0"), "flux-not-conserved")
    need(metric["ruling"] == "FINITE_INTEGRATED_CURVATURE_BUDGET; NOT_SURFACE_INDEPENDENT_CHARGE", "flux-ruling")
    ambiguity = result["action_ambiguity"]
    need("rescale" in ambiguity["overall_rescaling"], "action-rescaling")
    need(ambiguity["ruling"] == "METRIC_AND_BULK_EQUATIONS_DO_NOT_FIX_BOUNDARY_GENERATOR_OR_NORMALIZATION", "action-ruling")
    rank = result["scale_rank"]
    need(rank["determinant"] == "1-alpha*gamma", "rank-determinant")
    need("continuum" in rank["consistent_case"], "rank-continuum")
    need(result["maximum_conclusion"] == "RAW_METRIC_CURVATURE_BUDGET_DERIVED; CONSERVED_CHARGE_AND_ABSOLUTE_SCALE_OPEN", "maximum")
    return {"checks": len(result["checks"]), "maximum": result["maximum_conclusion"]}


def independent_algebra() -> dict[str, str]:
    y, X, c, G, alpha, gamma = sp.symbols("y X c G alpha gamma", positive=True)
    A = 1 - y
    N = sp.sqrt(A)
    # Work entirely in dimensionless y=r/X, independently from the derivation implementation.
    dN_dr = sp.diff(N, y) / X
    flux = sp.simplify(4 * sp.pi * (X * y) ** 2 * sp.sqrt(A) * dN_dr)
    need(sp.simplify(flux + 2 * sp.pi * X * y**2) == 0, "independent-flux")
    need(sp.simplify(sp.diff(flux, y) / X + 4 * sp.pi * y) == 0, "independent-flux-gradient")

    M = gamma * c**2 * X / G
    eq1 = X - alpha * G * M / c**2
    need(sp.simplify(eq1 - X * (1 - alpha * gamma)) == 0, "independent-rank")
    determinant = sp.factor(sp.Matrix([[1, -alpha * G / c**2], [-gamma * c**2 / G, 1]]).det())
    need(determinant == 1 - alpha * gamma, "independent-determinant")

    # No monomial c^a G^b has dimensions of length: mass forces b=0, time then a=0, leaving L^0.
    a, b = sp.symbols("a b")
    solution = sp.solve([sp.Eq(-b, 0), sp.Eq(-a - 2 * b, 0), sp.Eq(a + 3 * b, 1)], [a, b], dict=True)
    need(solution == [], "no-length-from-cG")
    mass_per_length = {"L": 2 - 3, "T": -2 - (-2), "M": 1}
    need(mass_per_length == {"L": -1, "T": 0, "M": 1}, "c2-over-G")
    return {
        "flux": "-2*pi*X*y^2",
        "dflux_dr": "-4*pi*y",
        "closure_determinant": str(determinant),
        "cG_length_monomial": "NONE",
    }


def source_text_checks() -> dict[str, str]:
    csn = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(encoding="utf-8")
    xmax = (ROOT / "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    final = (ROOT / "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    wrl = (ROOT / "archive/native_action_chat_2026-07-14_15/UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md").read_text(encoding="utf-8")
    need("What is not decided by this lock" in csn and "normalization identified observationally as $G$" in csn, "source-csn")
    need("center and width" in bootstrap and "No nonlocal insertion" in bootstrap, "source-bootstrap")
    need("A second independent native closure is required" in xmax, "source-xmax")
    need("Normalized finite-cell gravitational charge/mass\tOPEN" in final, "source-final")
    need("radius-dependent" in wrl and "unnormalized" in wrl, "source-wrl")
    return {"CSN": "PASS", "bootstrap": "PASS", "Xmax": "PASS", "final_action": "PASS", "WRL": "PASS"}


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except AssertionError:
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    candidates = rows("CANDIDATE_UNIVERSE.tsv")
    sources = rows("SOURCE_ADJUDICATION.tsv")
    charge = rows("CHARGE_REQUIREMENT_LEDGER.tsv")
    scale = rows("SCALE_CLOSURE_LEDGER.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    checks = {
        "candidate_universe": validate_candidates(candidates),
        "source_adjudication": validate_sources(sources, candidates),
        "charge_requirements": validate_charge(charge),
        "scale_closure": validate_scale(scale),
        "status": validate_status(status),
        "derivation": validate_derivation(derivation),
        "independent_algebra": independent_algebra(),
        "source_text": source_text_checks(),
    }

    catches: dict[str, str] = {}
    catches["missing_candidate_rejected"] = expect_failure("candidate", lambda: validate_candidates(candidates[:-1]))
    catches["missing_source_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1], candidates))
    mutated = copy.deepcopy(charge); one(mutated, "id", "C03")["current_status"] = "DERIVED_CONSERVED"
    catches["raw_flux_conservation_promotion_rejected"] = expect_failure("conservation", lambda: validate_charge(mutated))
    mutated = copy.deepcopy(charge); one(mutated, "id", "C05")["current_status"] = "DERIVED"
    catches["action_gap_erasure_rejected"] = expect_failure("action", lambda: validate_charge(mutated))
    mutated = copy.deepcopy(charge); one(mutated, "id", "C16")["current_status"] = "DERIVED_NATIVE_MASS"
    catches["raw_flux_mass_promotion_rejected"] = expect_failure("mass", lambda: validate_charge(mutated))
    mutated = copy.deepcopy(scale); one(mutated, "id", "R02")["status"] = "DERIVED_FULL_RANK"
    catches["homogeneous_pair_full_rank_rejected"] = expect_failure("rank", lambda: validate_scale(mutated))
    mutated = copy.deepcopy(scale); one(mutated, "id", "E05")["status"] = "DERIVED"
    catches["invented_density_center_rejected"] = expect_failure("density", lambda: validate_scale(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S11")["status"] = "DERIVED_SELECTOR"
    catches["CSN_scale_selection_promotion_rejected"] = expect_failure("CSN", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S12")["status"] = "DERIVED_CENTER"
    catches["bootstrap_center_promotion_rejected"] = expect_failure("bootstrap", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S05")["status"] = "DERIVED_NATIVE"
    catches["status_mass_promotion_rejected"] = expect_failure("status-mass", lambda: validate_status(mutated))
    mutated_result = copy.deepcopy(derivation); mutated_result["action_ambiguity"]["ruling"] = "METRIC_FIXES_CHARGE"
    catches["action_ambiguity_erasure_rejected"] = expect_failure("ambiguity", lambda: validate_derivation(mutated_result))
    mutated_result = copy.deepcopy(derivation); mutated_result["scale_rank"]["consistent_case"] = "isolated positive X"
    catches["scale_continuum_erasure_rejected"] = expect_failure("continuum", lambda: validate_derivation(mutated_result))

    result = {
        "schema": "udt-native-boundary-generator-verification-1.0",
        "result": "PASS",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "candidates": len(candidates), "sources": len(sources), "charge_rows": len(charge),
            "scale_rows": len(scale), "status_rows": len(status), "catch_proofs": len(catches),
        },
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "RAW_METRIC_CURVATURE_BUDGET_DERIVED; CONSERVED_CHARGE_NATIVE_MASS_AND_ABSOLUTE_SCALE_OPEN",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
