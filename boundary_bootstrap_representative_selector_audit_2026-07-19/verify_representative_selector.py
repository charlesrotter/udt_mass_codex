#!/usr/bin/env python3
"""Independent fail-closed verification of the representative-selection audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
EXPECTED_DISPOSITIONS = {
    "CONTEXT_CANDIDATE": 914,
    "LOAD_BEARING_CANDIDATE": 29,
    "EXCLUDED_DUPLICATE_RAW_RECORD": 23,
    "PROVENANCE_OR_CONTEXT_ONLY": 729,
    "EXCLUDED_GENERATED_ORGANIZATION": 67,
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
    need(len(items) == 1762 and len({row["path"] for row in items}) == 1762, "census-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "census-hash-shape")
        need(row["matched_tokens"], "census-token")
    need(counts == EXPECTED_DISPOSITIONS, "census-dispositions")
    need("XMAX_RECIPROCITY" in one(items, "path", "xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md")["matched_tokens"], "xmax-token")
    return {"rows": len(items), "dispositions": counts}


def validate_sources(items: list[dict[str, str]], census: list[dict[str, str]]) -> dict[str, object]:
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    need(len(items) == 29 and len({row["path"] for row in items}) == 29, "source-count")
    need({row["path"] for row in items} == expected, "source-coverage")
    need(one(items, "id", "R02")["authority"] == "FOUNDING_LOCKED", "CSN-authority")
    need(one(items, "id", "R06")["authority"] == "OWNER_CLARIFICATION", "Xmax-authority")
    need(one(items, "id", "R27")["authority"] == "ALGEBRA_VALID_PHYSICS_WITHDRAWN", "Xmax-full-frame-grade")
    need(one(items, "id", "R29")["current_affirmative_use"] == "CONDITIONAL_MATH_ONLY", "Xmax-status-use")
    return {"rows": len(items), "exact_coverage": True}


def validate_candidates(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 17 and len({row["id"] for row in items}) == 17, "candidate-count")
    expected_fragments = {
        "C01": "NOT_A_SELECTOR",
        "C03": "DERIVED_PROFILE_SELECTOR",
        "C04": "CONDITIONAL_POST_SCALE_SELECTOR",
        "C05": "NOT_CURRENT_REPRESENTATIVE_SELECTOR",
        "C07": "OPEN_CANDIDATE_OBJECT_NOT_SUPPLIED",
        "C09": "NOT_REPRESENTATIVE_SELECTOR",
        "C10": "EQUIVALENCE_WITNESS_NOT_SELECTOR",
        "C13": "ADMISSIBILITY_TARGET_NOT_SELECTOR_EQUATION",
        "C17": "OPEN_FUTURE_ROUTE",
    }
    for identity, fragment in expected_fragments.items():
        need(fragment in one(items, "id", identity)["ruling"], f"candidate:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected_fragments)}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 14 and len({row["id"] for row in items}) == 14, "status-count")
    expected = {
        "S01": "DERIVED_IN_CANONIZED_SIMPLE_METRIC_SCOPE",
        "S02": "NOT_DERIVED",
        "S03": "REFUTED_IN_BOUNDED_ORBIT",
        "S05": "UNIQUE_CONDITIONAL",
        "S06": "OPEN_NOT_SUPPLIED",
        "S07": "REFUTED_AS_SUFFICIENT",
        "S08": "CONDITIONAL_HYPOTHESIS",
        "S09": "NOT_DERIVED",
        "S10": "CONDITIONAL",
        "S11": "REFUTED_IN_BOUNDED_ORBIT",
        "S12": "OPEN_OBJECT_ABSENT",
        "S13": "SELECTOR_NOT_FOUND_IN_CURRENT_FOUNDATION",
        "S14": "OPEN",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_requirements(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 17 and len({row["id"] for row in items}) == 17, "requirement-count")
    need(one(items, "id", "C03")["result"] == "FAIL_FOR_REPRESENTATIVE; PASS_FOR_PROFILE", "requirement-WRL")
    need(one(items, "id", "C09")["R7_REMOVES_DEGENERACY"] == "NO_HOMOTHETY", "requirement-Xmax")
    need(one(items, "id", "C05")["R3_EQUATION_OR_CLOSURE"] == "NO_CURRENT_FUNCTIONAL", "requirement-bootstrap")
    need(all(not row["result"].startswith("PASS_ALL") for row in items), "requirement-no-selector")
    return {"rows": len(items), "passing_all": 0}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 28, "derivation-checks")
    orbit = result["endpoint_flat_CSN_family"]
    need(orbit["Omega"] == "exp(epsilon*y^2*(1-y)^2)", "bump-profile")
    need("clock-curvature residual" in orbit["changes"], "bump-clock-change")
    xmax = result["xmax_reciprocity"]
    need(xmax["ruling"] == "VALUABLE_DIMENSIONLESS_POSITIONAL_HYPOTHESIS; NOT_A_CURRENT_CSN_REPRESENTATIVE_SELECTOR", "xmax-ruling")
    need("does not remove" in xmax["local_representative"], "xmax-local")
    need(result["bootstrap"]["ruling"].startswith("CURRENT_ON_SHELL_BOOTSTRAP"), "bootstrap-ruling")
    need(result["maximum_conclusion"].startswith("NO_EXISTING_NONCIRCULAR"), "maximum")
    return {"checks": len(result["checks"]), "maximum": result["maximum_conclusion"]}


def independent_algebra() -> dict[str, str]:
    z, e, L = sp.symbols("z e L", positive=True)
    bump = z**2 * (1 - z) ** 2
    need([bump.subs(z, q) for q in (0, 1)] == [0, 0], "independent-endpoints")
    need([sp.diff(bump, z).subs(z, q) for q in (0, 1)] == [0, 0], "independent-endpoint-slopes")

    # Recompute the volume/length responses in a dimensionless coordinate, independently of r.
    dl = sp.integrate(bump / sp.sqrt(1 - z), (z, 0, 1))
    dv = 12 * sp.pi * sp.integrate(z**2 * bump / sp.sqrt(1 - z), (z, 0, 1))
    need(dl == sp.Rational(16, 315), "independent-length")
    need(dv == 1024 * sp.pi / 5005, "independent-volume")

    # Direct conformal optical cancellation in arbitrary symbols.
    Om, H, lapse = sp.symbols("Om H lapse", positive=True)
    need(sp.simplify((Om**2 * H) / (Om * lapse) ** 2 - H / lapse**2) == 0, "independent-optical")

    # Xmax reciprocity and bootstrap see ratios, not the common homothety.
    x, xmax, scale, mass, G, c = sp.symbols("x xmax scale mass G c", positive=True)
    need(sp.simplify(scale * x / (scale * xmax) - x / xmax) == 0, "independent-xmax-ratio")
    chi = G * mass / (c**2 * xmax)
    need(sp.simplify(chi.subs({mass: scale * mass, xmax: scale * xmax}) - chi) == 0, "independent-compactness")
    return {
        "length_response_over_X": str(dl),
        "volume_response_over_X3": str(dv),
        "optical_metric": "INVARIANT",
        "x_over_Xmax": "HOMOTHETY_INVARIANT",
        "compactness": "HOMOTHETY_INVARIANT",
    }


def source_text_checks() -> dict[str, str]:
    canon = (ROOT / "CANON.md").read_text(encoding="utf-8")
    csn = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(encoding="utf-8")
    xmax = (ROOT / "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md").read_text(encoding="utf-8")
    reset = (ROOT / "udt_premise_reset_audit_2026-07-19/PACKAGE_REGRADE.tsv").read_text(encoding="utf-8")
    xstatus = (ROOT / "xmax_reciprocity_audit_2026-07-19/STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    clock = (ROOT / "clock_curvature_selector_audit_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8")
    need("Absolute scale" in canon and "one ruler remains free" in canon, "source-canon")
    need("equivalence class" in csn and "pre-scale bulk law" in csn, "source-CSN")
    need("center and width" in bootstrap and "No nonlocal insertion" in bootstrap, "source-bootstrap")
    need("A second independent native closure is required" in xmax, "source-Xmax")
    need("xmax_reciprocity_audit_2026-07-19\tALGEBRA_VALID_PHYSICS_WITHDRAWN" in reset, "source-reset")
    need("S08\tDoes Xmax fix the CSN representative?" in xstatus and "not local Omega" in xstatus, "source-xstatus")
    need("UNIQUE-CONDITIONAL" in clock and "not presently a native UDT field equation" in clock, "source-clock")
    return {"CANON": "PASS", "CSN": "PASS", "bootstrap": "PASS", "Xmax": "PASS", "premise_reset": "PASS", "Xmax_status": "PASS", "clock": "PASS"}


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except AssertionError:
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    census = rows("SOURCE_CENSUS.tsv")
    sources = rows("SOURCE_ADJUDICATION.tsv")
    candidates = rows("SELECTOR_CANDIDATE_LEDGER.tsv")
    requirements = rows("SELECTOR_REQUIREMENT_MATRIX.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "source_census": validate_census(census),
        "source_adjudication": validate_sources(sources, census),
        "selector_candidates": validate_candidates(candidates),
        "selector_requirements": validate_requirements(requirements),
        "status": validate_status(status),
        "derivation": validate_derivation(derivation),
        "independent_algebra": independent_algebra(),
        "source_text": source_text_checks(),
    }

    catches: dict[str, str] = {}
    catches["missing_census_row_rejected"] = expect_failure("census", lambda: validate_census(census[:-1]))
    mutated = copy.deepcopy(census); mutated[0]["sha256"] = "0" * 63
    catches["malformed_census_hash_rejected"] = expect_failure("hash", lambda: validate_census(mutated))
    catches["missing_load_bearing_source_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1], census))
    mutated = copy.deepcopy(sources); one(mutated, "id", "R27")["authority"] = "CURRENT_PHYSICAL_THEOREM"
    catches["withdrawn_Xmax_physics_promotion_rejected"] = expect_failure("Xmax-source", lambda: validate_sources(mutated, census))
    catches["missing_selector_candidate_rejected"] = expect_failure("candidate", lambda: validate_candidates(candidates[:-1]))
    catches["missing_requirement_row_rejected"] = expect_failure("requirement", lambda: validate_requirements(requirements[:-1]))
    mutated = copy.deepcopy(candidates); one(mutated, "id", "C09")["ruling"] = "DERIVED_CSN_REPRESENTATIVE_SELECTOR"
    catches["Xmax_reciprocity_selector_promotion_rejected"] = expect_failure("Xmax", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(candidates); one(mutated, "id", "C05")["ruling"] = "DERIVED_BOOTSTRAP_SIGMA_MAP"
    catches["bootstrap_map_invention_rejected"] = expect_failure("bootstrap", lambda: validate_candidates(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S02")["status"] = "DERIVED"
    catches["WRL_profile_representative_conflation_rejected"] = expect_failure("profile", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S07")["status"] = "DERIVED_SCALE"
    catches["dimensionless_root_scale_promotion_rejected"] = expect_failure("root", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S11")["status"] = "DERIVED_FULL_REPRESENTATIVE"
    catches["fixed_Xmax_local_selector_promotion_rejected"] = expect_failure("fixed-Xmax", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S13")["status"] = "DERIVED_SELECTOR_FOUND"
    catches["top_level_selector_promotion_rejected"] = expect_failure("top", lambda: validate_status(mutated))
    mutated = copy.deepcopy(status); one(mutated, "id", "S14")["status"] = "DERIVED_COMPLETE_ACTION"
    catches["complete_action_promotion_rejected"] = expect_failure("action", lambda: validate_status(mutated))
    altered = copy.deepcopy(derivation); altered["xmax_reciprocity"]["ruling"] = "DERIVED_SELECTOR"
    catches["Xmax_derivation_result_mutation_rejected"] = expect_failure("Xmax-result", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["endpoint_flat_CSN_family"]["changes"].remove("clock-curvature residual")
    catches["bump_falsifier_erasure_rejected"] = expect_failure("bump", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["maximum_conclusion"] = "COMPLETE_NATIVE_ACTION_DERIVED"
    catches["maximum_conclusion_overreach_rejected"] = expect_failure("maximum", lambda: validate_derivation(altered))

    result = {
        "schema": "udt-boundary-bootstrap-representative-verification-1.0",
        "result": "PASS",
        "groups": groups,
        "catch_proofs": catches,
        "counts": {"census": len(census), "sources": len(sources), "candidates": len(candidates), "requirements": len(requirements), "status": len(status), "catch_proofs": len(catches)},
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "SELECTOR_NOT_FOUND_IN_CURRENT_FOUNDATION; XMAX_RECIPROCITY_RETAINED_AS_CONDITIONAL_DIMENSIONLESS_POSITIONAL_HYPOTHESIS",
        "certification": "VERIFIED-WITH-CAVEATS: independent in-package algebra and source replay; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
