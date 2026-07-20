#!/usr/bin/env python3
"""Independent fail-closed verifier for the scale-breaking closure census."""

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
BASE = "ff1df31c10303ae8deb8438f36ce66f76130c819"
EXPECTED_DISPOSITIONS = {
    "CONTEXT_CANDIDATE": 1633,
    "LOAD_BEARING_CANDIDATE": 33,
    "EXCLUDED_DUPLICATE_RAW_RECORD": 55,
    "PROVENANCE_OR_CONTEXT_ONLY": 1845,
    "EXCLUDED_GENERATED_ORGANIZATION": 262,
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def one(items: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [row for row in items if row[key] == value]
    need(len(found) == 1, f"one:{key}:{value}")
    return found[0]


def validate_census(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 3828 and len({row["path"] for row in items}) == 3828, "census-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "census-hash-shape")
        need(row["matched_tokens"], "census-token")
        need(not row["path"].startswith("scale_breaking_closure_census_2026-07-20/"), "generated-census-feedback")
    need(counts == EXPECTED_DISPOSITIONS, "census-dispositions")
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
    need(one(items, "id", "R02")["current_ruling"] == "AFFIRMATIVE_NEUTRALITY_NOT_SELECTOR", "source-CSN")
    need(one(items, "id", "R23")["current_ruling"] == "CONDITIONAL_COMPATIBILITY_HYPOTHESIS", "source-Xmax")
    need(one(items, "id", "R28")["authority"] == "HARD_FROZEN", "source-frozen")
    need(one(items, "id", "R31")["current_ruling"] == "CONDITIONAL_PARTICLE_READOUT", "source-particle")
    return {"rows": len(items), "base_hashes_replayed": len(items)}


def validate_weights(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 22 and len({row["id"] for row in items}) == 22, "weight-count")
    expected = {
        "W01": ("0", "HOMOTHETY_INVARIANT_DIMENSIONLESS"),
        "W03": ("0", "HOMOTHETY_INVARIANT_DIMENSIONLESS"),
        "W06": ("3", "HOMOGENEOUS_NOT_SCALE_SELECTING"),
        "W10": ("1", "HOMOGENEOUS_NOT_SCALE_SELECTING"),
        "W13": ("-2", "HOMOGENEOUS_NOT_SCALE_SELECTING"),
        "W14": ("0", "HOMOTHETY_INVARIANT_DIMENSIONLESS"),
        "W19": ("-2 target if available", "COULD_SELECT_IF_INDEPENDENT_VALUE_DERIVED"),
        "W22": ("0 global endpoint scale; functional local freedom", "LOCAL_REPRESENTATIVE_DEGENERACY"),
    }
    for identity, (weight, classification) in expected.items():
        row = one(items, "id", identity)
        need(row["scale_weight_under_Hlambda"] == weight and row["classification"] == classification, f"weight:{identity}")
    return {"rows": len(items), "anchors_checked": len(expected)}


def validate_candidates(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 21 and len({row["id"] for row in items}) == 21, "candidate-count")
    expected = {
        "C02": "HOMOTHETY_INVARIANT_DIMENSIONLESS",
        "C04": "HOMOGENEOUS_NOT_SCALE_SELECTING",
        "C07": "HOMOGENEOUS_NOT_SCALE_SELECTING",
        "C11": "OPEN_OBJECT_ABSENT",
        "C13": "HOMOTHETY_INVARIANT_DIMENSIONLESS",
        "C15": "COULD_SELECT_IF_INDEPENDENT_VALUE_DERIVED",
        "C19": "CONDITIONAL_OR_IMPORTED_READOUT",
        "C21": "HOMOTHETY_INVARIANT_DIMENSIONLESS",
    }
    allowed = {
        "HOMOTHETY_INVARIANT_DIMENSIONLESS", "HOMOGENEOUS_NOT_SCALE_SELECTING",
        "COULD_SELECT_IF_INDEPENDENT_VALUE_DERIVED", "CONDITIONAL_OR_IMPORTED_READOUT",
        "OPEN_OBJECT_ABSENT",
    }
    need(all(row["classification"] in allowed for row in items), "candidate-class-enum")
    need(all(row["classification"] != "NONCIRCULAR_SCALE_BREAKER_FOUND" for row in items), "candidate-no-breaker")
    for identity, classification in expected.items():
        need(one(items, "id", identity)["classification"] == classification, f"candidate:{identity}")
    return {"rows": len(items), "noncircular_scale_breakers": 0}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 16 and len({row["id"] for row in items}) == 16, "status-count")
    expected = {
        "S02": "CONDITIONAL_HYPOTHESIS",
        "S03": "NOT_DERIVED",
        "S04": "REFUTED_BY_DIMENSION_AND_RANK",
        "S05": "REFUTED_AS_SUFFICIENT",
        "S07": "REFUTED_AS_INDEPENDENT",
        "S08": "OPEN_NOT_SUPPLIED",
        "S09": "CONDITIONAL_FUTURE_ROUTE",
        "S10": "NOT_DERIVED",
        "S13": "REFUTED_IN_BOUNDED_ORBIT",
        "S14": "NOT_FOUND_IN_AUDITED_CURRENT_FOUNDATION",
        "S15": "OPEN",
        "S16": "DERIVED_SCOPED_DIMENSIONAL_THEOREM",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 41, "derivation-checks")
    need(result["homothety"]["available_log_rank"] == 1, "derivation-rank")
    need(result["homothety"]["null_direction"] == [1, 1], "derivation-null")
    need(result["xmax_reciprocity"]["status"] == "CONDITIONAL_HYPOTHESIS_RETAINED", "derivation-Xmax-status")
    need(result["xmax_reciprocity"]["scale_weight"] == 0, "derivation-Xmax-weight")
    need(result["current_closure"]["noncircular_scale_breaker_found"] is False, "derivation-breaker")
    need(result["dimensional_theorem"]["dimension_matrix_rank"] == 3, "derivation-dimension-rank")
    need(result["dimensional_theorem"]["dimensionless_nullspace"] == [1, -1, -2, 1], "derivation-dimension-null")
    need(result["dimensional_theorem"]["c_E_and_G_obs_form_length"] is False, "derivation-no-length")
    need(result["local_representative"]["ruling"].startswith("GLOBAL_XMAX_SELECTION_WOULD_NOT"), "derivation-local")
    need(result["maximum_conclusion"] == "NO_NONCIRCULAR_SCALE_BREAKER_FOUND_IN_AUDITED_CURRENT_FOUNDATION", "derivation-maximum")
    return {"checks": len(result["checks"]), "available_log_rank": 1}


def independent_algebra() -> dict[str, object]:
    s, L, m, c0, g0, a, b, kv, u, v = sp.symbols("s L m c0 g0 a b kv u v", positive=True)
    def S(expr: sp.Expr) -> sp.Expr:
        return sp.simplify(expr.subs({L: s * L, m: s * m, u: s * u}, simultaneous=True))

    xi = u / L
    mobius = (xi + v) / (1 + xi * v)
    need(sp.simplify(S(xi) - xi) == 0, "independent-xi")
    need(sp.simplify(S(mobius) - mobius) == 0, "independent-mobius")
    chi = g0 * m / (c0**2 * L)
    rho = m / (kv * L**3)
    delta = g0 * rho * L**2 / c0**2
    need(sp.simplify(S(chi) - chi) == 0, "independent-compactness")
    need(sp.simplify(S(rho) - rho / s**2) == 0, "independent-density-weight")
    need(sp.simplify(delta - chi / kv) == 0, "independent-density-dependence")
    matrix = sp.Matrix([[1, -a * g0 / c0**2], [-b * c0**2 / g0, 1]])
    need(sp.simplify(matrix.det() - (1 - a * b)) == 0, "independent-pair-det")
    need(matrix.subs(b, 1 / a).rank() == 1, "independent-pair-rank")
    existing = sp.Matrix([[1, -1], [-1, 1]])
    with_density = sp.Matrix([[1, -1], [-3, 1]])
    need(existing.rank() == 1 and with_density.rank() == 2, "independent-log-ranks")
    units = sp.Matrix([[0, 1, 1, 3], [1, 0, 0, -1], [0, 0, -1, -2]])
    need(units.rank() == 3 and units.nullspace() == [sp.Matrix([1, -1, -2, 1])], "independent-units")
    z = sp.symbols("z", real=True)
    bump = z**2 * (1 - z)**2
    need(bump.subs(z, 0) == bump.subs(z, 1) == 0, "independent-local-bump")
    need(sp.integrate(z**2 * bump / sp.sqrt(1-z), (z, 0, 1)) == sp.Rational(256, 15015), "independent-volume-integral")
    return {
        "xmax_reciprocity": "HOMOTHETY_INVARIANT",
        "existing_log_rank": existing.rank(),
        "rank_with_independent_density_center": with_density.rank(),
        "dimensionless_density": "DEPENDENT_ON_COMPACTNESS",
        "local_CSN_family": "SURVIVES_FIXED_ENDPOINT",
    }


def source_text_checks() -> dict[str, str]:
    canon = (ROOT / "CANON.md").read_text(encoding="utf-8")
    csn = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(encoding="utf-8")
    scale = (ROOT / "native_boundary_generator_scale_audit_2026-07-19/SCALE_CLOSURE_LEDGER.tsv").read_text(encoding="utf-8")
    parent = (ROOT / "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8")
    xstat = (ROOT / "xmax_reciprocity_audit_2026-07-19/STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    action = (ROOT / "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    need("Absolute scale" in canon and "one ruler remains free" in canon, "text-canon")
    need("equivalence class" in csn and "pre-scale bulk law" in csn, "text-CSN")
    need("center and width" in bootstrap and "No nonlocal insertion" in bootstrap, "text-bootstrap")
    need("DERIVED_RANK_ONE" in scale and "c_E^2/G_obs has dimensions mass/length" in scale, "text-scale")
    need("XMAX_RECIPROCITY = CONDITIONAL_DIMENSIONLESS_POSITIONAL_HYPOTHESIS" in parent, "text-parent-Xmax")
    need("S08\tDoes Xmax fix the CSN representative?" in xstat, "text-Xmax-status")
    need("S25\tNormalized finite-cell gravitational charge/mass\tOPEN" in action, "text-action")
    return {"CANON": "PASS", "CSN": "PASS", "bootstrap": "PASS", "scale": "PASS", "parent": "PASS", "Xmax": "PASS", "action": "PASS"}


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except (AssertionError, subprocess.CalledProcessError):
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    census = rows("SOURCE_CENSUS.tsv")
    sources = rows("SOURCE_ADJUDICATION.tsv")
    weights = rows("SCALE_WEIGHT_LEDGER.tsv")
    candidates = rows("CANDIDATE_CLOSURE_LEDGER.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "source_census": validate_census(census),
        "source_adjudication": validate_sources(sources, census),
        "scale_weights": validate_weights(weights),
        "candidate_closures": validate_candidates(candidates),
        "status": validate_status(status),
        "derivation": validate_derivation(derivation),
        "independent_algebra": independent_algebra(),
        "source_text": source_text_checks(),
    }

    catches: dict[str, str] = {}
    catches["missing_census_row_rejected"] = expect_failure("census", lambda: validate_census(census[:-1]))
    mutated = copy.deepcopy(census); mutated[0]["sha256"] = "0" * 63
    catches["malformed_census_hash_rejected"] = expect_failure("hash", lambda: validate_census(mutated))
    catches["missing_source_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1], census))
    mutated = copy.deepcopy(sources); one(mutated, "id", "R23")["current_ruling"] = "DERIVED_PHYSICAL_XMAX_LAW"
    catches["Xmax_hypothesis_promotion_rejected"] = expect_failure("Xmax-source", lambda: validate_sources(mutated, census))
    mutated = copy.deepcopy(sources); one(mutated, "id", "R31")["current_ruling"] = "NATIVE_GLOBAL_MASS"
    catches["conditional_particle_mass_promotion_rejected"] = expect_failure("particle", lambda: validate_sources(mutated, census))
    catches["missing_weight_row_rejected"] = expect_failure("weight", lambda: validate_weights(weights[:-1]))
    mutated = copy.deepcopy(weights); one(mutated, "id", "W14")["scale_weight_under_Hlambda"] = "2"
    catches["dimensionless_density_weight_mutation_rejected"] = expect_failure("density-weight", lambda: validate_weights(mutated))
    catches["missing_candidate_rejected"] = expect_failure("candidate", lambda: validate_candidates(candidates[:-1]))
    mutated = copy.deepcopy(candidates); one(mutated, "id", "C02")["classification"] = "NONCIRCULAR_SCALE_BREAKER_FOUND"
    catches["Xmax_reciprocity_scale_promotion_rejected"] = expect_failure("Xmax-candidate", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(candidates); one(mutated, "id", "C07")["classification"] = "NONCIRCULAR_SCALE_BREAKER_FOUND"
    catches["rank_one_pair_promotion_rejected"] = expect_failure("rank", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(candidates); one(mutated, "id", "C13")["classification"] = "NONCIRCULAR_SCALE_BREAKER_FOUND"
    catches["dependent_density_promotion_rejected"] = expect_failure("density", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(candidates); one(mutated, "id", "C19")["classification"] = "NONCIRCULAR_SCALE_BREAKER_FOUND"
    catches["conditional_carrier_promotion_rejected"] = expect_failure("carrier", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S03")["status"] = "DERIVED_XMAX"
    catches["physical_Xmax_promotion_rejected"] = expect_failure("Xmax-status", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S07")["status"] = "INDEPENDENT_CLOSURE"
    catches["density_definition_independence_rejected"] = expect_failure("density-status", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S10")["status"] = "NATIVE_TOTAL_MASS"
    catches["raw_flux_mass_promotion_rejected"] = expect_failure("flux", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S13")["status"] = "FULL_REPRESENTATIVE_SELECTED"
    catches["global_scale_local_section_conflation_rejected"] = expect_failure("local", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S14")["status"] = "SCALE_BREAKER_FOUND"
    catches["top_level_overclaim_rejected"] = expect_failure("top", lambda: validate_status(mutated))
    altered = copy.deepcopy(derivation); altered["current_closure"]["noncircular_scale_breaker_found"] = True
    catches["derivation_scale_breaker_invention_rejected"] = expect_failure("derive-breaker", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["xmax_reciprocity"]["scale_weight"] = 1
    catches["derivation_Xmax_weight_mutation_rejected"] = expect_failure("derive-Xmax", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["maximum_conclusion"] = "COMPLETE_NATIVE_ACTION_AND_MASS_DERIVED"
    catches["maximum_conclusion_overreach_rejected"] = expect_failure("maximum", lambda: validate_derivation(altered))

    result = {
        "schema": "udt-scale-breaking-closure-verification-1.0",
        "result": "PASS",
        "groups": groups,
        "catch_proofs": catches,
        "counts": {
            "census": len(census), "sources": len(sources), "weights": len(weights),
            "candidates": len(candidates), "status": len(status), "catch_proofs": len(catches),
        },
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "NO_NONCIRCULAR_SCALE_BREAKER_FOUND_IN_AUDITED_CURRENT_FOUNDATION; XMAX_RECIPROCITY_RETAINED_AS_CONDITIONAL_DIMENSIONLESS_COMPATIBILITY",
        "certification": "VERIFIED-WITH-CAVEATS: independent in-package algebra/source replay; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
