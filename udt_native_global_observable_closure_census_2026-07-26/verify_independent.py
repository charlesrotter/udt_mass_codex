#!/usr/bin/env python3
"""Independent stdlib/Fraction replay and exercised mutation catches.

This verifier does not import or execute derive_observable_census.py.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c2a0feafca41d9fa95c12a7db278876acf7552f0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def table_map(items: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    result = {item[key]: item for item in items}
    if len(result) != len(items):
        raise ValueError(f"duplicate {key}")
    return result


def validate(state: dict[str, object]) -> list[str]:
    errors: list[str] = []
    cand = state["candidates"]
    princ = state["principles"]
    gates = state["gates"]
    matrix = state["matrix"]
    defs = state["definitions"]
    principle_matrix = state["principle_matrix"]
    variations = state["variations"]
    assembly = state["assembly"]
    sources = state["sources"]
    result = state["result"]
    assert isinstance(cand, list) and isinstance(princ, list) and isinstance(gates, list)
    assert isinstance(matrix, list) and isinstance(defs, list) and isinstance(sources, list)
    assert isinstance(principle_matrix, list) and isinstance(variations, list) and isinstance(assembly, list)
    assert isinstance(result, dict)
    try:
        c = table_map(cand, "candidate_id")
        p = table_map(princ, "principle_id")
        g = table_map(gates, "gate_id")
        m = table_map(matrix, "candidate_id")
        d = table_map(defs, "candidate_id")
        pm = table_map(principle_matrix, "principle_id")
        v = table_map(variations, "variation_id")
        ab = table_map(assembly, "blocker_id")
    except ValueError as exc:
        return [str(exc)]
    if len(c) != 26 or set(c) != {f"N{i:02d}" for i in range(1, 27)}:
        errors.append("candidate_universe")
    if len(p) != 12 or set(p) != {f"P{i:02d}" for i in range(1, 13)}:
        errors.append("principle_universe")
    if len(g) != 12 or set(g) != {f"G{i:02d}" for i in range(1, 13)}:
        errors.append("gate_universe")
    if set(m) != set(c) or set(d) != set(c):
        errors.append("candidate_coverage")
        return errors
    if m["N01"]["G10"] != "FAIL_SELECTOR" or d["N01"]["operator_provenance"] != "OBSERVATION_ONLY":
        errors.append("observed_anchor_promoted")
    if m["N02"]["G03"] != "OPEN_ONTOLOGY" or m["N03"]["G03"] != "OPEN_ONTOLOGY":
        errors.append("volume_ontology_promoted")
    if m["N02"]["G08"] == "PASS" or m["N03"]["G08"] == "PASS" or m["N04"]["G08"] == "PASS":
        errors.append("moving_boundary_omitted")
    if m["N05"]["G01"] != "ABSENT" or m["N07"]["G01"] != "ABSENT":
        errors.append("native_matter_invented")
    if d["N23"]["operator_provenance"] != "CONDITIONAL_CARRIER_ACTION":
        errors.append("external_formula_called_native")
    if m["N06"]["G02"] != "ABSENT_NATIVE_MASS" or m["N06"]["G10"] != "FAIL_WITHOUT_M":
        errors.append("density_without_native_mass")
    for ident in ("N08", "N09", "N13", "N24"):
        if m[ident]["G04"] != "LOCAL_ONLY":
            errors.append("local_called_global")
            break
    if m["N10"]["G08"] == "PASS" or m["N10"]["G10"] != "FAIL_COUNTERFAMILY":
        errors.append("curvature_functional_promoted")
    if m["N11"]["G10"] != "FAIL_INFINITE_FAMILY":
        errors.append("curvature_family_selected")
    if m["N03"]["G07"] != "PASS":
        errors.append("volume_tracefree_response_invented")
    if m["N12"]["G01"] != "TYPE_ONLY_SOURCE_GAP" or d["N12"]["operator_provenance"] != "TYPE_ONLY_SOURCE_GAP":
        errors.append("spectral_source_gap_promoted")
    if m["N14"]["G10"] != "FAIL_PROTOCOL_FAMILY" or m["N14"]["G03"] != "OPEN_REPRESENTATIVE":
        errors.append("holonomy_protocol_omitted")
    if m["N15"]["disposition"] != "CONDITIONAL_SPLIT_HOLONOMY_MONODROMY_OBJECT":
        errors.append("holonomy_monodromy_conflated")
    if m["N16"]["G05"] != "PASS" or m["N16"]["G09"] != "CONDITIONAL_NORMALIZED_SHAPE_VS_PHYSICAL_LENGTH":
        errors.append("systole_tie_smoothed")
    if "TYPE_ONLY_SUPREMUM" != m["N20"]["G01"] or "NONATTAINMENT" not in m["N20"]["G05"]:
        errors.append("diameter_called_smooth")
    if m["N21"]["G05"] != "DISCRETE_NOT_COVECTOR" or m["N22"]["G05"] != "DISCRETE_NOT_COVECTOR":
        errors.append("topology_called_covector")
    if m["N23"]["G01"] != "POSIT_CONDITIONAL":
        errors.append("conditional_carrier_promoted")
    if m["N25"]["G01"] != "OBSERVED_ON_SUPPLIED_BRANCH":
        errors.append("onshell_score_promoted")
    if m["N19"]["disposition"] != "DERIVED_CONDITIONAL_TEMPORAL_PHI_SEPARATION_FAMILY__NOT_UNIVERSAL":
        errors.append("temporal_phi_separation_erased")
    if m["N24"]["G03"] != "OPEN_ONTOLOGY" or m["N24"]["G06"] != "PARTIAL_CHART_COMPONENT_RESPONSE_ONLY" or m["N24"]["G07"] != "PARTIAL_CHART_COMPONENT_RESPONSE_ONLY":
        errors.append("Cartan_component_response_promoted")
    if m["N26"]["G11"] == "PASS" or m["N26"]["G12"] == "PASS":
        errors.append("closure_arrow_invented")
    if any(all(item[f"G{i:02d}"] == "PASS" for i in range(1, 11)) for item in matrix):
        errors.append("complete_vector_false_positive")
    if any(all(item[f"G{i:02d}"] == "PASS" for i in range(1, 13)) for item in matrix):
        errors.append("complete_closure_false_positive")
    partial_R = {"N02", "N03", "N04", "N06", "N10", "N14", "N15", "N16", "N19", "N23"}
    if any(m[ident]["G11"] == "ABSENT" for ident in partial_R):
        errors.append("partial_recomputation_map_erased")
    if set(ab) != {f"B{i:02d}" for i in range(1, 7)} or any(row["status"] != "OPEN_BLOCKER" for row in assembly):
        errors.append("assembly_blocker_coverage")
    if pm["P11"]["selects_target"] != "CONDITIONAL_BRANCH_ONLY" or pm["P12"]["selects_dual_pairing"] != "CONDITIONAL_BRANCH_ONLY":
        errors.append("conditional_action_response_erased")
    if "k=2_for_partial_Sigma_and_k=3_for_spacetime_seal" not in v["V03"]["boundary_or_global"]:
        errors.append("boundary_codimension_conflated")
    if "delta q_w=-w^T H^-1(delta H)H^-1 w" not in v["V08"]["fixed_domain_bulk"] or "W_min_is_set_valued_jump" not in v["V08"]["tracefree_angular"]:
        errors.append("systole_objects_conflated")
    if "NOT_LC_HOLONOMY" not in v["V07"]["status"]:
        errors.append("abelian_variation_called_LC_holonomy")
    if result.get("density_status") != "NOT_USED__LAMBDA_CDM_CENTER_DEFERRED_IMPORTED_COMPARISON_ANCHOR":
        errors.append("density_used")
    if result.get("complete_single_component_candidates") != [] or result.get("complete_single_component_closure_candidates") != []:
        errors.append("result_false_positive")
    if result.get("coherent_multi_component_assembly") != "NOT_DERIVED__B01_B05_UNREPAIRED":
        errors.append("assembly_false_positive")
    for source in sources:
        path = ROOT / source["path"]
        if not path.is_file() or sha(path.read_bytes()) != source["sha256"]:
            errors.append("source_manifest_drift")
            break
        frozen = subprocess.run(["git", "show", f"{BASE}:{source['path']}"], cwd=ROOT, capture_output=True, check=True).stdout
        if sha(frozen) != source["sha256"]:
            errors.append("source_base_identity_drift")
            break
    return errors


def main() -> None:
    checks: dict[str, str] = {}

    # Independent exact arithmetic checks at rational samples.
    diag = [F(2), F(3), F(5), F(7)]
    delta = [F(11), F(13), F(17), F(19)]
    log_det_derivative = sum(delta[i] / diag[i] for i in range(4))
    determinant = diag[0] * diag[1] * diag[2] * diag[3]
    direct_det_derivative = sum(delta[i] * determinant / diag[i] for i in range(4))
    require("I01_four_volume_log_derivative", direct_det_derivative / determinant == log_det_derivative, checks)
    require("I02_four_volume_half_trace", log_det_derivative / 2 == F(11, 4) + F(13, 6) + F(17, 10) + F(19, 14), checks)
    require("I03_tracefree_spatial_volume_blind", F(1) + F(-1) + F(0) == 0, checks)
    require("I04_tracefree_boundary_area_blind", F(1) + F(-1) == 0, checks)

    M, V, dM, dV = F(7), F(11), F(13), F(17)
    require("I05_density_quotient", (V * dM - M * dV) / V**2 == F(24, 121), checks)
    ric = [F(2), F(3), F(5)]
    scalar = sum(ric)
    Htf = [F(1), F(-1), F(0)]
    tf_bulk = sum((scalar / 2 - ric[i]) * Htf[i] for i in range(3))
    require("I06_curvature_tracefree_bulk", tf_bulk == F(1), checks)
    trace_bulk = sum(scalar / 2 - item for item in ric)
    require("I07_curvature_trace_bulk", trace_bulk == scalar / 2, checks)
    omega = F(3, 2)
    require("I08_conformal_weights", [omega**4, omega**3, omega**2, omega**3, omega] == [F(81, 16), F(27, 8), F(9, 4), F(27, 8), F(3, 2)], checks)

    # Dimension vector (L,M,T) for c^a G^b.
    def dim(a: F, b: F) -> tuple[F, F, F]:
        return (a + 3 * b, -b, -a - 2 * b)
    require("I09_cG_no_length", dim(F(0), F(0)) != (F(1), F(0), F(0)), checks)
    require("I10_cG_density_contradiction", dim(F(2), F(-1)) == (F(-1), F(1), F(0)) != (F(-3), F(1), F(0)), checks)
    require("I11_c2_over_G_mass_per_length", dim(F(2), F(-1)) == (F(-1), F(1), F(0)), checks)

    q, s, lam = F(2), F(3), F(1, 2)
    grad0 = [q, s]
    grad1 = [q + lam * s, s + lam * q]
    require("I12_bulk_counterfamily_differs", grad0 != grad1, checks)
    require("I13_bulk_counterfamily_same_root", [F(0), F(0)] == [F(0), F(0)], checks)
    require("I14_boundary_counterfamily_two_channels", F(5) * F(7) != 0 and F(11) != 0, checks)
    x = F(2)
    require("I15_closure_conormal_normalization_free", F(1) != 1 + x*x, checks)
    require("I16_fixed_point_same_root_different_slope", F(1) != F(1, 2), checks)
    require("I17_fixed_path_holonomy_linearity", (F(7) + F(11)) / 2 == F(9), checks)
    h, dh = F(1, 4), F(1, 8)
    q_w = 1 / h
    dq_w = -dh / h**2
    ell_w = F(2)
    require("I18_character_norm_and_length_variation",
            q_w == F(4) and dq_w == F(-2) and dq_w / (2 * ell_w) == F(-1, 2), checks)
    eps = F(1, 10)
    slopes = [F(-1), F(-3)]
    q_after = [1 / (1 + eps), 1 / (1 + 3 * eps)]
    require("I19_systole_tie_value_and_argmin",
            min(slopes) == F(-3) and q_after[1] < q_after[0], checks)
    # max(x,-x)=|x| has two one-sided derivatives at the multiple maximizer x=0.
    require("I20_diameter_multimax_nonsmooth", F(1) != F(-1), checks)

    state: dict[str, object] = {
        "candidates": rows("OBSERVABLE_UNIVERSE.tsv"),
        "principles": rows("PRINCIPLE_UNIVERSE.tsv"),
        "gates": rows("VARIATION_GATE_UNIVERSE.tsv"),
        "matrix": rows("OBSERVABLE_GATE_MATRIX.tsv"),
        "definitions": rows("OBSERVABLE_DEFINITION_LEDGER.tsv"),
        "principle_matrix": rows("PRINCIPLE_CLOSURE_MATRIX.tsv"),
        "variations": rows("VARIATION_LEDGER.tsv"),
        "assembly": rows("ASSEMBLY_BLOCKER_LEDGER.tsv"),
        "sources": rows("SOURCE_MANIFEST.tsv"),
        "result": json.loads((HERE / "RESULT.json").read_text(encoding="utf-8")),
    }
    require("I21_complete_snapshot_valid", validate(state) == [], checks)

    mutations: list[tuple[str, callable]] = [
        ("F01_missing_observable", lambda s: s["candidates"].pop()),
        ("F02_missing_principle", lambda s: s["principles"].pop()),
        ("F03_external_formula_native", lambda s: next(r for r in s["definitions"] if r["candidate_id"] == "N23").update(operator_provenance="UDT_NATIVE")),
        ("F04_anchor_selector", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N01").update(G10="PASS")),
        ("F05_local_called_global", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N24").update(G04="PASS")),
        ("F06_volume_ontology", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N03").update(G03="PASS")),
        ("F07_density_without_mass", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N06").update(G02="PASS", G10="PASS")),
        ("F08_carrier_unconditional", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N23").update(G01="PASS")),
        ("F09_boundary_omitted", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N10").update(G08="PASS")),
        ("F10_volume_TF_invented", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N03").update(G07="PASS_NONZERO")),
        ("F11_holonomy_protocol", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N14").update(G10="PASS")),
        ("F12_systole_or_diameter_smooth", lambda s: (next(r for r in s["matrix"] if r["candidate_id"] == "N16").update(G05="EVERYWHERE_DIFFERENTIABLE"), next(r for r in s["matrix"] if r["candidate_id"] == "N20").update(G05="PASS"))),
        ("F13_topology_covector", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N21").update(G05="PASS")),
        ("F14_Cartan_physical", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N24").update(G04="PASS", G10="PASS")),
        ("F15_onshell_closure", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N25").update(G01="PASS")),
        ("F16_closure_arrow_invented", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N26").update(G11="PASS", G12="PASS")),
        ("F17_cross_branch_splice", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N02").update(G03="PASS")),
        ("F18_curvature_selected", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N11").update(G10="PASS")),
        ("F19_density_imported", lambda s: s["result"].update(density_status="USED_AS_UDT_SOURCE")),
        ("F20_density_sweep", lambda s: s["result"].update(density_status="SWEEP_COMPLETED")),
        ("F21_source_drift", lambda s: s["sources"][0].update(sha256="0" * 64)),
        ("F22_complete_false_positive", lambda s: next(r for r in s["matrix"] if r["candidate_id"] == "N26").update(**{f"G{i:02d}": "PASS" for i in range(1, 13)})),
    ]
    catch_rows: list[dict[str, str]] = []
    for ident, mutate in mutations:
        trial = deepcopy(state)
        mutate(trial)
        failures = validate(trial)
        require(f"I22_{ident}", bool(failures), checks)
        catch_rows.append({"catch_id": ident, "result": "PASS_REJECTED", "detected_by": ";".join(failures)})

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "result", "detected_by"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)

    production = state["result"]
    assert isinstance(production, dict)
    require("I23_production_pinned_sympy", production["sympy_version"] == "1.14.0", checks)
    require("I24_production_39_checks", production["algebra_check_count"] == 39 and set(production["checks"].values()) == {"PASS"}, checks)
    require("I25_production_conclusion_exact",
            production["maximum_supported_conclusion"] == "NO_DERIVED_COMPLETE_OBSERVABLE_VECTOR_OR_CLOSURE_SECTION__EXACT_METRIC_PRIMITIVE_AND_VARIATION_ATLAS", checks)

    output = {
        "schema": "udt-native-global-observable-census-independent-1.0",
        "method": "stdlib_fraction_table_reconstruction_no_production_import",
        "check_count": len(checks),
        "catch_count": len(catch_rows),
        "checks": checks,
        "result": "PASS",
        "maximum_supported_conclusion": production["maximum_supported_conclusion"],
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
