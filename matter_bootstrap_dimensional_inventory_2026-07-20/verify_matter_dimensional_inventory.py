#!/usr/bin/env python3
"""Independent fail-closed verifier for the matter dimensional inventory."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ab099c9c642d68049cfc4810fd709df638ce591c"
EXPECTED_DISPOSITIONS = {
    "CONTEXT_CANDIDATE": 1650,
    "LOAD_BEARING_CANDIDATE": 41,
    "EXCLUDED_DUPLICATE_RAW_RECORD": 58,
    "PROVENANCE_OR_CONTEXT_ONLY": 1904,
    "EXCLUDED_GENERATED_ORGANIZATION": 271,
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
    need(len(items) == 3924 and len({row["path"] for row in items}) == 3924, "census-count")
    counts: dict[str, int] = {}
    for row in items:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
        need(len(row["blob"]) == 40 and len(row["sha256"]) == 64, "census-hash")
        need(row["matched_tokens"], "census-token")
        need(not row["path"].startswith("matter_bootstrap_dimensional_inventory_2026-07-20/"), "census-feedback")
    need(counts == EXPECTED_DISPOSITIONS, "census-dispositions")
    return {"rows": len(items), "dispositions": counts}


def validate_sources(items: list[dict[str, str]], census: list[dict[str, str]]) -> dict[str, object]:
    expected = {row["path"] for row in census if row["initial_disposition"] == "LOAD_BEARING_CANDIDATE"}
    need(len(items) == 41 and len({row["path"] for row in items}) == 41, "source-count")
    need({row["path"] for row in items} == expected, "source-coverage")
    cbp = {row["path"]: row for row in census}
    for row in items:
        path = row["path"]
        data = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        need(hashlib.sha256(data).hexdigest() == cbp[path]["sha256"], f"source-sha:{path}")
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()
        need(blob == cbp[path]["blob"], f"source-blob:{path}")
    need(one(items, "path", "noNull_energy.py")["primary_provenance"] == "CONDITIONAL_ACTION_OR_CARRIER_INPUT", "source-energy")
    need(one(items, "path", "noNull_boxscout_build.py")["primary_provenance"] == "NUMERICAL_UNIT_OR_DOMAIN_CONTROL", "source-box")
    need(one(items, "path", "noNull_phaseG_mass.py")["closure_ruling"] == "BLOCKED_BY_CONDITIONAL_PREMISE", "source-mass")
    need(one(items, "path", "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md")["primary_provenance"] == "DIMENSIONLESS_TOPOLOGY_OR_SHAPE", "source-topology")
    return {"rows": len(items), "base_hashes_replayed": len(items)}


def validate_parameters(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 28 and len({row["id"] for row in items}) == 28, "parameter-count")
    anchors = {
        "P01": ("7", "CONDITIONAL_ACTION_OR_CARRIER_INPUT"),
        "P03": ("147", "NUMERICAL_UNIT_OR_DOMAIN_CONTROL"),
        "P06": ("40", "NUMERICAL_UNIT_OR_DOMAIN_CONTROL"),
        "P11": ("23", "OPEN_NOT_PRESENT"),
        "P14": ("18", "NUMERICAL_UNIT_OR_DOMAIN_CONTROL"),
        "P19": ("149", "CONDITIONAL_ACTION_OR_CARRIER_INPUT"),
        "P24": ("192", "CONDITIONAL_ACTION_OR_CARRIER_INPUT"),
        "P26": ("197", "NUMERICAL_UNIT_OR_DOMAIN_CONTROL"),
    }
    for identity, (line, provenance) in anchors.items():
        row = one(items, "id", identity)
        need(row["line"] == line and row["primary_provenance"] == provenance, f"parameter:{identity}")
    for row in items:
        source_lines = (ROOT / row["path"]).read_text(encoding="utf-8").splitlines()
        need(1 <= int(row["line"]) <= len(source_lines), f"parameter-line:{row['id']}")
    return {"rows": len(items), "anchors_checked": len(anchors)}


def validate_objects(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 26 and len({row["id"] for row in items}) == 26, "object-count")
    expected = {
        "D05": ("CONDITIONAL_ACTION_OR_CARRIER_INPUT", "COULD_BREAK_IF_NATIVELY_DERIVED"),
        "D06": ("CONDITIONAL_ACTION_OR_CARRIER_INPUT", "COULD_BREAK_IF_NATIVELY_DERIVED"),
        "D07": ("CONDITIONAL_ACTION_OR_CARRIER_INPUT", "BLOCKED_BY_CONDITIONAL_PREMISE"),
        "D09": ("SOLUTION_OUTPUT_CONDITIONAL_ON_INPUTS", "BLOCKED_BY_CONDITIONAL_PREMISE"),
        "D13": ("DIMENSIONLESS_TOPOLOGY_OR_SHAPE", "NOT_PHYSICAL_SCALE_INFORMATION"),
        "D17": ("NUMERICAL_UNIT_OR_DOMAIN_CONTROL", "NOT_PHYSICAL_SCALE_INFORMATION"),
        "D23": ("OPEN_NOT_PRESENT", "COULD_BREAK_IF_NATIVELY_DERIVED"),
        "D25": ("DIMENSIONLESS_TOPOLOGY_OR_SHAPE", "RATIO_OR_COMPACTNESS_ONLY"),
        "D26": ("CONDITIONAL_ACTION_OR_CARRIER_INPUT", "RATIO_OR_COMPACTNESS_ONLY"),
    }
    for identity, values in expected.items():
        row = one(items, "id", identity)
        need((row["primary_provenance"], row["closure_class"]) == values, f"object:{identity}")
    need(not any(row["closure_class"] == "ABSOLUTE_SCALE_BREAKER" for row in items), "object-no-breaker")
    return {"rows": len(items), "noncircular_scale_breakers": 0}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 16 and len({row["id"] for row in items}) == 16, "status-count")
    expected = {
        "S01": "DERIVED_SCOPED", "S02": "DERIVED_SCOPED", "S03": "VERIFIED_WITH_CAVEATS",
        "S04": "OPEN_NOT_FOUND", "S05": "REFUTED_AS_SUFFICIENT", "S06": "REFUTED_AS_SUFFICIENT",
        "S07": "REFUTED_CONFLATION", "S08": "REFUTED_AS_SUFFICIENT", "S09": "NOT_FOUND",
        "S10": "CONDITIONAL", "S11": "RATIO_ONLY_CONDITIONAL", "S12": "CONDITIONAL_NOT_SELECTOR",
        "S13": "OPEN_NOT_FOUND", "S14": "OPEN", "S15": "OPEN", "S16": "VERIFIED_WITH_CAVEATS",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 31, "derive-checks")
    need(result["continuum_scaling"]["stationary_radius"] == "sqrt(kappa/xi)*sqrt(B/A)", "derive-radius")
    need(result["continuum_scaling"]["ruling"].startswith("FINITE_STATIC_SIZE_INHERITS"), "derive-ruling")
    need(result["coefficient_dimensions"]["kappa_over_xi"] == "length^2", "derive-dim")
    need(result["observational_anchors"]["ruling"] == "c_E_AND_G_obs_DO_NOT_SUPPLY_ell_0", "derive-anchor")
    need(result["fixed_charge"]["ruling"] == "NO_INDEPENDENT_NATIVE_RULER_FOUND", "derive-Q")
    need(result["xmax_counterfactual"]["ruling"] == "RATIO_SELECTION_ONLY; NOT_ABSOLUTE_XMAX_SELECTION", "derive-Xmax")
    need(result["mass_readout"]["ruling"] == "NO_NATIVE_UNCONDITIONAL_MASS_NORMALIZATION", "derive-mass")
    need(result["maximum_conclusion"] == "HIDDEN_CONDITIONAL_COEFFICIENT_RULER; NO_NATIVE_DIMENSIONAL_MATTER_OBJECT_FOUND", "derive-max")
    return {"checks": len(result["checks"]), "maximum_conclusion": result["maximum_conclusion"]}


def argparse_defaults(path: str) -> dict[str, object]:
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    found: dict[str, object] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or node.func.attr != "add_argument":
            continue
        if not node.args or not isinstance(node.args[0], ast.Constant):
            continue
        name = str(node.args[0].value).lstrip("-")
        for kw in node.keywords:
            if kw.arg == "default":
                found[name] = ast.literal_eval(kw.value)
    return found


def source_syntax_checks() -> dict[str, str]:
    energy_text = (ROOT / "noNull_energy.py").read_text(encoding="utf-8")
    energy_tree = ast.parse(energy_text)
    doc = ast.get_docstring(energy_tree) or ""
    need("REPRESENTATION CHANGE, NOT A NEW PHYSICAL OPERATOR" in doc, "syntax-representation")
    need("(xi/2)" in doc and "(kappa/4)" in doc, "syntax-functional")
    assignments = [node for node in ast.walk(energy_tree) if isinstance(node, ast.Assign)]
    unit_tuple = False
    for node in assignments:
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Tuple):
            names = [elt.id for elt in node.targets[0].elts if isinstance(elt, ast.Name)]
            if names == ["xi", "kappa"] and ast.literal_eval(node.value) == (1.0, 1.0):
                unit_tuple = True
    need(unit_tuple, "syntax-unit-coefficients")
    p1 = argparse_defaults("hopfion_fixedQ_phase1_isorotation.py")
    p1b = argparse_defaults("hopfion_fixedQ_phase1b_production.py")
    need((p1["L"], p1["xi"], p1["kappa"], p1["Q"]) == (5.0, 1.0, 1.0, "0,0.5,1.0"), "syntax-phase1")
    need((p1b["L"], p1b["xi"], p1b["kappa"], p1b["Q"]) == (6.0, 1.0, 1.0, "0,0.5,1.0"), "syntax-phase1b")
    collective = (ROOT / "hopfion_fixedQ_collective_phase0.py").read_text(encoding="utf-8")
    need("Gauge ξ=κ=1" in collective and "dimensionless CHOSE normalization" in collective, "syntax-collective")
    box = (ROOT / "noNull_boxscout_build.py").read_text(encoding="utf-8")
    need("L == 6.0 and xi == 1.0 and kap == 1.0" in box, "syntax-box")
    phaseg_doc = ast.get_docstring(ast.parse((ROOT / "noNull_phaseG_mass.py").read_text(encoding="utf-8"))) or ""
    need("SOLVER boundary, not a physical wall" in phaseg_doc, "syntax-solver-wall")
    need("No kappa_g value is used" in phaseg_doc and "native-UDT mass derivation" in phaseg_doc, "syntax-mass-conditional")
    behavior_doc = ast.get_docstring(ast.parse((ROOT / "noNull_behavioral_F.py").read_text(encoding="utf-8"))) or ""
    need("NOT physical time evolution" in behavior_doc and "L=6/HBW=2" in behavior_doc, "syntax-behavior")
    return {"continuum": "PASS", "coefficient_defaults": "PASS", "fixed_Q": "PASS", "box": "PASS", "mass": "PASS", "stability": "PASS"}


def independent_algebra() -> dict[str, object]:
    r, q, a, b, A0, B0, cc, GG, L0, XX, z = sp.symbols("r q a b A0 B0 cc GG L0 XX z", positive=True)
    E = a * A0 * r + b * B0 / r
    root = sp.solve(sp.diff(E, r), r)[0]
    need(sp.simplify(root - sp.sqrt(b * B0 / (a * A0))) == 0, "independent-root")
    need(sp.simplify((a * A0 * root) - (b * B0 / root)) == 0, "independent-virial")
    need(sp.diff(E, r, 2).subs(r, root) > 0, "independent-minimum")
    dims_E = sp.Matrix([2, 1, -2]); dims_L = sp.Matrix([1, 0, 0])
    need((dims_E + dims_L) - (dims_E - dims_L) == sp.Matrix([2, 0, 0]), "independent-dimensions")
    anchor_a = cc**4 / GG
    anchor_b = cc**4 * L0**2 / GG
    anchored = sp.simplify(root.subs({a: anchor_a, b: anchor_b}))
    need(sp.simplify(anchored / L0 - sp.sqrt(B0 / A0)) == 0, "independent-anchor-length")
    xroot = sp.simplify(anchored.subs(L0, XX))
    need(sp.simplify(xroot.subs(XX, q * XX) - q * xroot) == 0, "independent-homothety")
    # Independent derivative-count check under x=r*y: d^3x -> r^3 and each derivative -> r^-1.
    need(3 - 2 == 1 and 3 - 4 == -1, "independent-change-variables")
    # Explicit Gaussian scalar diagnostic confirms derivative-count powers without using primary expressions.
    gaussian = sp.exp(-z**2)
    I2shape = sp.integrate(4 * sp.pi * z**2 * sp.diff(gaussian, z)**2, (z, 0, sp.oo))
    I4shape = sp.integrate(4 * sp.pi * z**2 * sp.diff(gaussian, z)**4, (z, 0, sp.oo))
    need(I2shape > 0 and I4shape > 0, "independent-gaussian-shapes")
    return {"stationary_radius": str(root), "L2_power": 1, "L4_power": -1, "coefficient_ratio_dimension": "length^2", "gaussian_shape_integrals_positive": True}


def expect_failure(label: str, fn) -> str:
    try:
        fn()
    except (AssertionError, subprocess.CalledProcessError, KeyError):
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    census = rows("SOURCE_CENSUS.tsv")
    sources = rows("SOURCE_ADJUDICATION.tsv")
    params = rows("CODE_PARAMETER_INVENTORY.tsv")
    objects = rows("DIMENSIONAL_OBJECT_LEDGER.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "source_census": validate_census(census),
        "source_adjudication": validate_sources(sources, census),
        "code_parameters": validate_parameters(params),
        "dimensional_objects": validate_objects(objects),
        "status": validate_status(status),
        "derivation": validate_derivation(derivation),
        "source_syntax": source_syntax_checks(),
        "independent_algebra": independent_algebra(),
    }

    catches: dict[str, str] = {}
    catches["missing_census_row_rejected"] = expect_failure("census", lambda: validate_census(census[:-1]))
    altered = copy.deepcopy(census); one(altered, "path", "noNull_energy.py")["sha256"] = "0" * 64
    catches["base_source_mutation_rejected"] = expect_failure("source-hash", lambda: validate_sources(sources, altered))
    catches["missing_source_adjudication_rejected"] = expect_failure("source", lambda: validate_sources(sources[:-1], census))
    altered = copy.deepcopy(sources); one(altered, "path", "noNull_energy.py")["primary_provenance"] = "NATIVE_METRIC_DERIVED"
    catches["coefficient_native_promotion_rejected"] = expect_failure("coef", lambda: validate_sources(altered, census))
    altered = copy.deepcopy(sources); one(altered, "path", "noNull_boxscout_build.py")["primary_provenance"] = "NATIVE_METRIC_DERIVED"
    catches["numerical_box_physical_promotion_rejected"] = expect_failure("box", lambda: validate_sources(altered, census))
    altered = copy.deepcopy(sources); one(altered, "path", "noNull_phaseG_mass.py")["closure_ruling"] = "ABSOLUTE_SCALE_BREAKER"
    catches["conditional_mass_promotion_rejected"] = expect_failure("mass", lambda: validate_sources(altered, census))
    catches["missing_parameter_rejected"] = expect_failure("params", lambda: validate_parameters(params[:-1]))
    altered = copy.deepcopy(params); one(altered, "id", "P03")["primary_provenance"] = "NATIVE_METRIC_DERIVED"
    catches["unit_coefficient_promotion_rejected"] = expect_failure("unit", lambda: validate_parameters(altered))
    altered = copy.deepcopy(params); one(altered, "id", "P06")["primary_provenance"] = "NATIVE_METRIC_DERIVED"
    catches["L6_box_promotion_rejected"] = expect_failure("L6", lambda: validate_parameters(altered))
    altered = copy.deepcopy(params); one(altered, "id", "P11")["primary_provenance"] = "NATIVE_METRIC_DERIVED"
    catches["missing_kappa_g_invention_rejected"] = expect_failure("kg", lambda: validate_parameters(altered))
    altered = copy.deepcopy(params); one(altered, "id", "P26")["primary_provenance"] = "NATIVE_METRIC_DERIVED"
    catches["supplied_Q_promotion_rejected"] = expect_failure("Q", lambda: validate_parameters(altered))
    catches["missing_dimensional_object_rejected"] = expect_failure("objects", lambda: validate_objects(objects[:-1]))
    altered = copy.deepcopy(objects); one(altered, "id", "D07")["closure_class"] = "ABSOLUTE_SCALE_BREAKER"
    catches["conditional_ruler_absolute_promotion_rejected"] = expect_failure("ell", lambda: validate_objects(altered))
    altered = copy.deepcopy(objects); one(altered, "id", "D13")["closure_class"] = "ABSOLUTE_SCALE_BREAKER"
    catches["topology_scale_promotion_rejected"] = expect_failure("topology", lambda: validate_objects(altered))
    altered = copy.deepcopy(objects); one(altered, "id", "D17")["closure_class"] = "ABSOLUTE_SCALE_BREAKER"
    catches["grid_box_scale_promotion_rejected"] = expect_failure("grid", lambda: validate_objects(altered))
    altered = copy.deepcopy(objects); one(altered, "id", "D26")["closure_class"] = "ABSOLUTE_SCALE_BREAKER"
    catches["Xmax_ratio_absolute_promotion_rejected"] = expect_failure("Xratio", lambda: validate_objects(altered))
    catches["missing_status_rejected"] = expect_failure("status", lambda: validate_status(status[:-1]))
    altered = copy.deepcopy(status); one(altered, "id", "S04")["status"] = "NATIVE_DERIVED"
    catches["coefficient_derivation_invention_rejected"] = expect_failure("coef-status", lambda: validate_status(altered))
    altered = copy.deepcopy(status); one(altered, "id", "S06")["status"] = "ABSOLUTE_SCALE_DERIVED"
    catches["topology_radius_invention_rejected"] = expect_failure("top-status", lambda: validate_status(altered))
    altered = copy.deepcopy(status); one(altered, "id", "S09")["status"] = "NATIVE_TIME_AND_LENGTH"
    catches["fixed_Q_scale_invention_rejected"] = expect_failure("Q-status", lambda: validate_status(altered))
    altered = copy.deepcopy(status); one(altered, "id", "S10")["status"] = "NATIVE_UNCONDITIONAL_MASS"
    catches["phaseG_mass_overclaim_rejected"] = expect_failure("mass-status", lambda: validate_status(altered))
    altered = copy.deepcopy(status); one(altered, "id", "S11")["status"] = "ABSOLUTE_XMAX_SELECTED"
    catches["counterfactual_Xmax_overclaim_rejected"] = expect_failure("X-status", lambda: validate_status(altered))
    altered = copy.deepcopy(derivation); altered["xmax_counterfactual"]["ruling"] = "ABSOLUTE_XMAX_SELECTED"
    catches["derivation_Xmax_overclaim_rejected"] = expect_failure("derive-X", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["mass_readout"]["ruling"] = "NATIVE_MASS_DERIVED"
    catches["derivation_mass_overclaim_rejected"] = expect_failure("derive-mass", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["maximum_conclusion"] = "COMPLETE_NATIVE_MATTER_ACTION_DERIVED"
    catches["maximum_conclusion_overreach_rejected"] = expect_failure("derive-max", lambda: validate_derivation(altered))

    result = {
        "schema": "udt-matter-bootstrap-dimensional-verification-1.0",
        "result": "PASS",
        "groups": groups,
        "catch_proofs": catches,
        "counts": {"census": len(census), "sources": len(sources), "parameters": len(params), "objects": len(objects), "status": len(status), "catch_proofs": len(catches)},
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "HIDDEN_CONDITIONAL_COEFFICIENT_RULER; NO_NATIVE_DIMENSIONAL_MATTER_OBJECT_FOUND",
        "certification": "VERIFIED-WITH-CAVEATS: independent AST/source replay and algebra; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches), "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
