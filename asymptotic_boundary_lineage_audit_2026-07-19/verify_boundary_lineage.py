#!/usr/bin/env python3
"""Independent fail-closed verifier for the boundary-lineage audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ALLOWED_GRADES = {
    "DERIVED_METRIC_LIMIT",
    "DERIVED_CONDITIONAL_ON_STATED_PREMISES",
    "CANONICAL_STRUCTURE_OR_BOUNDARY_DECLARATION",
    "COORDINATE_OR_CHART_ENDPOINT_ONLY",
    "INTERPRETATION_NOT_DERIVED",
    "COUNTEREXAMPLE_OR_NEGATIVE_CONTROL",
    "CONFLICTED_SEMANTICS",
    "OUT_OF_SCOPE_CONTEXT",
}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def one(items: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [row for row in items if row[key] == value]
    require(len(found) == 1, f"one-row:{key}:{value}")
    return found[0]


def validate_candidates(items: list[dict[str, str]]) -> dict[str, object]:
    require(len(items) == 1061, "candidate-count")
    require(len({row["path"] for row in items}) == 1061, "candidate-unique")
    require(sum(bool(row["matched_tokens"]) for row in items) == 1046, "token-hit-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        require(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "candidate-hashes")
    expected = {
        "CONTEXT_ONLY": 99,
        "DUPLICATE_SNAPSHOT": 88,
        "EXCLUDED_WITH_REASON": 457,
        "LOAD_BEARING": 67,
        "NEGATIVE_CONTROL": 350,
    }
    require(counts == expected, "candidate-dispositions")
    return {"rows": len(items), "token_hits": 1046, "dispositions": counts}


def validate_sources(items: list[dict[str, str]], candidates: list[dict[str, str]]) -> dict[str, object]:
    expected_paths = {row["path"] for row in candidates if row["initial_disposition"] == "LOAD_BEARING"}
    require(len(items) == 67 and len({row["path"] for row in items}) == 67, "source-count")
    require({row["path"] for row in items} == expected_paths, "source-coverage")
    require(all(row["primary_evidence_grade"] in ALLOWED_GRADES for row in items), "source-grade")
    for row in items:
        if row["provenance_era"] == "PRE_JULY1" and row["path"] != "CANON.md":
            require(row["affirmative_current_use"] != "YES", "pre-firewall-promotion")
    require(one(items, "path", "native_dilation_weight_derivation_results.md")["affirmative_current_use"] == "NO", "old-mass-weight")
    require(one(items, "path", "simple_metric_mass_xmax_cascade.md")["affirmative_current_use"] == "NO", "MS-promotion")
    return {"rows": len(items), "families": len({row["family"] for row in items})}


def validate_objects(items: list[dict[str, str]]) -> dict[str, object]:
    require(len(items) == 8 and len({row["id"] for row in items}) == 8, "object-count")
    fold = one(items, "id", "B01")
    wall = one(items, "id", "B03")
    xmax = one(items, "id", "B07")
    require("phi=0; A=1" in fold["defining_data"], "fold-values")
    require("A=1-r/X" in wall["defining_data"] and "phi=-ln(A)/2" in wall["defining_data"], "wall-values")
    require(fold["surface_identity"] == "CMB_FOLD" and wall["surface_identity"] == "WRL_WALL", "surface-identities")
    require("supplied positive family parameter" in wall["scale_status"], "input-X-disclosure")
    require(xmax["surface_identity"] == "GLOBAL_XMAX" and "Derived output target" in xmax["scale_status"], "global-X-output")
    require("MS wall value" in wall["mass_status"] and "native mass open" in wall["mass_status"], "mass-readout-disclosure")
    return {"rows": len(items), "fold": fold["surface_identity"], "wall": wall["surface_identity"]}


def validate_quantities(items: list[dict[str, str]]) -> dict[str, object]:
    require(len({(row["surface_id"], row["quantity"]) for row in items}) == len(items), "quantity-unique")
    require({row["surface_id"] for row in items} == {f"B{i:02d}" for i in range(1, 9)}, "quantity-object-coverage")
    def q(surface: str, quantity: str) -> dict[str, str]:
        found = [row for row in items if row["surface_id"] == surface and row["quantity"] == quantity]
        require(len(found) == 1, f"quantity:{surface}:{quantity}")
        return found[0]
    require(q("B01", "phi")["limit_or_value"] == "0", "fold-phi")
    require(q("B01", "A=e^-2phi")["limit_or_value"] == "1", "fold-A")
    require(q("B03", "phi")["limit_or_value"] == "+infinity", "wall-phi")
    require(q("B03", "A=e^-2phi")["limit_or_value"] == "0", "wall-A")
    require(q("B03", "proper radial reach")["limit_or_value"] == "2X", "proper-distance")
    require(q("B03", "optical/tortoise reach")["limit_or_value"] == "+infinity", "optical-distance")
    require(q("B03", "raw lapse flux")["limit_or_value"] == "-2*pi*X", "raw-lapse-flux")
    require(q("B03", "raw lapse flux")["status"] == "DERIVED_METRIC_LIMIT", "raw-flux-not-mass")
    require(q("B03", "crossability")["limit_or_value"] == "regular ingoing and timelike curves exist", "horizon-extension")
    require(q("B03", "native total mass")["limit_or_value"] == "OPEN", "native-mass-open")
    return {"rows": len(items), "surfaces": 8}


def validate_identity_matrix(items: list[dict[str, str]]) -> dict[str, object]:
    require(len({(row["left_id"], row["right_id"]) for row in items}) == len(items), "identity-unique")
    fold_wall = [row for row in items if (row["left_id"], row["right_id"]) == ("B01", "B03")]
    require(len(fold_wall) == 1 and fold_wall[0]["ruling"] == "DERIVED_DISTINCT_IN_RECORDED_MODELS", "fold-wall-distinct")
    wall_xmax = [row for row in items if (row["left_id"], row["right_id"]) == ("B03", "B07")]
    require(len(wall_xmax) == 1 and wall_xmax[0]["ruling"] == "OPEN", "wall-xmax-open")
    return {"rows": len(items)}


def validate_mass(items: list[dict[str, str]]) -> dict[str, object]:
    require(len(items) == 10 and len({row["id"] for row in items}) == 10, "mass-count")
    require(one(items, "id", "M01")["status"] == "CONDITIONAL_REFERENCE_ONLY", "MS-status")
    require(one(items, "id", "M07")["status"] == "OPEN", "native-charge-open")
    require(one(items, "id", "M08")["status"] == "OBSERVED", "anchors-observed")
    require(one(items, "id", "M09")["status"] == "WORKING_HYPOTHESIS", "mass-X-hypothesis")
    require(one(items, "id", "M10")["status"] == "OPEN", "asymptotic-mass-open")
    return {"rows": len(items)}


def validate_closure(items: list[dict[str, str]]) -> dict[str, object]:
    require(len(items) == 20 and len({row["id"] for row in items}) == 20, "closure-count")
    require(one(items, "id", "K01")["current_status"] == "KNOWN", "c-known")
    require(one(items, "id", "K02")["current_status"] == "KNOWN", "G-known")
    require(one(items, "id", "E02")["current_status"] == "WORKING_HYPOTHESIS", "dimensional-form-not-derived")
    require(one(items, "id", "E04")["current_status"] == "OPEN", "mass-functional-open")
    require(one(items, "id", "E05")["current_status"] == "OPEN", "boundary-equation-open")
    require(one(items, "id", "E07")["current_status"] == "OPEN", "homothety-break-open")
    require(one(items, "id", "R02")["current_status"] == "WORKING_HYPOTHESIS_COHERENT", "conditional-closure")
    require(one(items, "id", "R03")["current_status"] == "DERIVED_DIMENSION_COUNT", "cG-mass-per-length-only")
    return {"rows": len(items), "known_anchors": 2, "open_load_bearing_equations": 2}


def direct_tensor_audit() -> dict[str, str]:
    t, r, th, ph, X = sp.symbols("t r theta varphi X", positive=True)
    coords = (t, r, th, ph)
    A = 1 - r / X
    g = sp.diag(-A, 1 / A, r**2, r**2 * sp.sin(th) ** 2)
    gi = sp.simplify(g.inv())
    n = 4
    Gamma = [[[
        sp.simplify(sum(gi[a, d] * (sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c]) - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
        for c in range(n)] for b in range(n)] for a in range(n)]
    Rmix = [[[[
        sp.simplify(
            sp.diff(Gamma[a][b][d], coords[c]) - sp.diff(Gamma[a][b][c], coords[d])
            + sum(Gamma[a][e][c] * Gamma[e][b][d] - Gamma[a][e][d] * Gamma[e][b][c] for e in range(n))
        ) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(Rmix[a][b][a][d] for a in range(n))))
    scalar = sp.factor(sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    require(sp.simplify(scalar - 6 / (X * r)) == 0, "direct-Ricci")
    K = sp.S.Zero
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    lowered = g[a, a] * Rmix[a][b][c][d]
                    K += gi[a, a] * gi[b, b] * gi[c, c] * gi[d, d] * lowered**2
    K = sp.factor(sp.trigsimp(sp.simplify(K)))
    require(sp.simplify(K - 8 / (X**2 * r**2)) == 0, "direct-Kretschmann")
    require(sp.limit(scalar, r, X, dir="-") == 6 / X**2, "direct-wall-R")
    require(sp.limit(K, r, X, dir="-") == 8 / X**4, "direct-wall-K")
    return {"Ricci": str(scalar), "Kretschmann": str(K), "method": "direct Christoffel-Riemann contraction"}


def source_text_checks() -> dict[str, str]:
    fold = (ROOT / "universe_cell_fold_jc_sigma_results.md").read_text(encoding="utf-8")
    canon = (ROOT / "CANON.md").read_text(encoding="utf-8")
    finite = (ROOT / "archive/native_action_chat_2026-07-14_15/UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md").read_text(encoding="utf-8")
    final = (ROOT / "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md").read_text(encoding="utf-8")
    xmax = (ROOT / "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    require("φ(r_s) = 0" in fold and "ρ'(r_s) = 0" in fold, "source-fold-pins")
    require("Horizon, not hard edge of space" in canon, "source-horizon-precision")
    require("The canonical static odd fold obeys" in finite and "The WR-L macro wall obeys" in finite, "source-object-split")
    require("normalized boundary charge/mass are `OPEN`" in final, "source-mass-open")
    require("X_{\\max}=\\alpha" in xmax and "Dimensional analysis does not determine" in xmax, "source-dimensional-lead")
    return {
        "fold_pins": "PASS",
        "horizon_precision": "PASS",
        "object_split": "PASS",
        "mass_open": "PASS",
        "dimensional_lead": "PASS",
    }


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except AssertionError:
        return "PASS"
    raise AssertionError(f"catch-proof-did-not-fail:{label}")


def main() -> None:
    candidates = rows("CANDIDATE_UNIVERSE.tsv")
    sources = rows("SOURCE_ADJUDICATION.tsv")
    objects = rows("BOUNDARY_OBJECT_LEDGER.tsv")
    quantities = rows("QUANTITY_LIMIT_LEDGER.tsv")
    identities = rows("SURFACE_IDENTITY_MATRIX.tsv")
    mass = rows("MASS_PROVENANCE_LEDGER.tsv")
    closure = rows("GLOBAL_CLOSURE_EQUATION_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    checks = {
        "candidate_universe": validate_candidates(candidates),
        "source_adjudication": validate_sources(sources, candidates),
        "boundary_objects": validate_objects(objects),
        "quantity_limits": validate_quantities(quantities),
        "surface_identity": validate_identity_matrix(identities),
        "mass_provenance": validate_mass(mass),
        "global_closure": validate_closure(closure),
        "direct_tensor": direct_tensor_audit(),
        "source_text": source_text_checks(),
    }
    require(derivation["result"] == "PASS" and len(derivation["checks"]) == 24, "derivation-result")
    require(derivation["join_result"] == "CMB_FOLD_AND_WRL_WALL_DISTINCT_IN_RECORDED_MODELS; GLOBAL_XMAX_JOIN_OPEN", "derivation-join")

    catches: dict[str, str] = {}
    mutated = copy.deepcopy(candidates[:-1])
    catches["missing_candidate_rejected"] = expect_failure("missing-candidate", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(candidates) + [copy.deepcopy(candidates[0])]
    catches["duplicate_candidate_rejected"] = expect_failure("duplicate-candidate", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(sources)
    one(mutated, "path", "native_dilation_weight_derivation_results.md")["affirmative_current_use"] = "YES"
    catches["pre_firewall_mass_promotion_rejected"] = expect_failure("pre-firewall", lambda: validate_sources(mutated, candidates))
    mutated = copy.deepcopy(objects)
    one(mutated, "id", "B01")["defining_data"] = "phi=+infinity; A=0"
    catches["fold_phi_swap_rejected"] = expect_failure("fold-phi", lambda: validate_objects(mutated))
    mutated = copy.deepcopy(objects)
    one(mutated, "id", "B03")["surface_identity"] = "CMB_FOLD"
    catches["notation_only_surface_join_rejected"] = expect_failure("surface-join", lambda: validate_objects(mutated))
    mutated = copy.deepcopy(objects)
    one(mutated, "id", "B03")["scale_status"] = "X derived as global output"
    catches["input_X_output_promotion_rejected"] = expect_failure("input-X", lambda: validate_objects(mutated))
    mutated = copy.deepcopy(quantities)
    for row in mutated:
        if row["surface_id"] == "B03" and row["quantity"] == "proper radial reach":
            row["limit_or_value"] = "+infinity"
    catches["proper_optical_confusion_rejected"] = expect_failure("distance-swap", lambda: validate_quantities(mutated))
    mutated = copy.deepcopy(mass)
    one(mutated, "id", "M01")["status"] = "DERIVED_NATIVE"
    catches["MS_native_mass_promotion_rejected"] = expect_failure("MS-native", lambda: validate_mass(mutated))
    mutated = copy.deepcopy(mass)
    one(mutated, "id", "M10")["status"] = "DERIVED"
    catches["mass_dilation_boundary_promotion_rejected"] = expect_failure("mass-boundary", lambda: validate_mass(mutated))
    mutated = copy.deepcopy(quantities)
    for row in mutated:
        if row["surface_id"] == "B03" and row["quantity"] == "raw lapse flux":
            row["status"] = "DERIVED_NATIVE_MASS"
    catches["raw_flux_mass_promotion_rejected"] = expect_failure(
        "raw-flux-mass", lambda: validate_quantities(mutated)
    )
    mutated = copy.deepcopy(closure)
    one(mutated, "id", "E02")["current_status"] = "DERIVED"
    catches["dimensional_analysis_as_derivation_rejected"] = expect_failure("dimensional", lambda: validate_closure(mutated))
    mutated = [row for row in copy.deepcopy(closure) if row["id"] != "R02"]
    catches["missing_mass_structure_closure_rejected"] = expect_failure("closure", lambda: validate_closure(mutated))

    result = {
        "schema": "udt-asymptotic-boundary-lineage-verification-1.0",
        "result": "PASS",
        "checks": checks,
        "derivation_result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "catch_proofs": catches,
        "counts": {
            "candidates": len(candidates),
            "load_bearing_sources": len(sources),
            "boundary_objects": len(objects),
            "quantity_limits": len(quantities),
            "surface_pairs": len(identities),
            "mass_rows": len(mass),
            "closure_rows": len(closure),
            "catch_proofs": len(catches),
        },
        "verdict": "CMB_FOLD_AND_WRL_WALL_DISTINCT; WRL_IS_REGULAR_CROSSABLE_STATIC_HORIZON; XMAX_AND_NATIVE_MASS_JOIN_OPEN",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
