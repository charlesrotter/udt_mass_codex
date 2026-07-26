#!/usr/bin/env python3
"""Fail-closed semantic and provenance verifier for the response-map audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GATES = [
    "G1_premise_entailment", "G2_complete_configuration_domain",
    "G3_off_shell_differentiability", "G4_local_tracefree_angular_response",
    "G5_same_solution_native_mass_volume", "G6_finite_cell_boundary_global_response",
    "G7_reciprocity_frame_ontology_compatibility", "G8_noncircular_selection",
]
ALLOWED = {"PASS", "CONDITIONAL", "ABSENT", "INCOMPATIBLE", "OUT_OF_SCOPE", "PROVENANCE_BLOCKED"}
DISPOSITIONS = {
    "DERIVED_COMPLETE_RESPONSE_MAP", "DERIVED_CONDITIONAL_RESPONSE_SKELETON",
    "ON_SHELL_ONLY", "TYPE_INCOMPLETE", "NOT_SELECTED", "PROVENANCE_BLOCKED",
}
EXPECTED_IDS = [f"R{i:02d}" for i in range(1, 10)]


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(matrix, universe, premises, channels, closure, semantics, algebra, sources) -> list[str]:
    errors: list[str] = []
    ids = [row.get("candidate_id", "") for row in matrix]
    if ids != EXPECTED_IDS or [row.get("candidate_id", "") for row in universe] != EXPECTED_IDS:
        errors.append("candidate universe mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate")
    by_universe = {row["candidate_id"]: row for row in universe}
    for row in matrix:
        cid = row.get("candidate_id", "")
        if cid not in by_universe or row.get("map_type") != by_universe[cid]["map_type"]:
            errors.append(f"generated or relabeled candidate: {cid}")
        invalid = {row.get(gate, "") for gate in GATES} - ALLOWED
        if invalid:
            errors.append(f"invalid gate: {cid}")
        if row.get("disposition") not in DISPOSITIONS:
            errors.append(f"invalid disposition: {cid}")
        all_pass = all(row.get(gate) == "PASS" for gate in GATES)
        if (row.get("disposition") == "DERIVED_COMPLETE_RESPONSE_MAP") != all_pass:
            errors.append(f"complete-survivor equivalence: {cid}")
    by_id = {row["candidate_id"]: row for row in matrix}
    if by_id.get("R01", {}).get("G3_off_shell_differentiability") != "ABSENT" or by_id.get("R01", {}).get("disposition") != "ON_SHELL_ONLY":
        errors.append("window promoted off shell")
    if by_id.get("R01", {}).get("G7_reciprocity_frame_ontology_compatibility") != "CONDITIONAL":
        errors.append("density window ontology promoted")
    if by_id.get("R02", {}).get("G4_local_tracefree_angular_response") == "PASS":
        errors.append("volume trace promoted to native angular response")
    if by_id.get("R03", {}).get("G5_same_solution_native_mass_volume") == "PASS":
        errors.append("unsupplied mass promoted native")
    if by_id.get("R04", {}).get("G1_premise_entailment") == "PASS" or by_id.get("R04", {}).get("G8_noncircular_selection") == "PASS":
        errors.append("multiobservable possibility promoted selected")
    if by_id.get("R05", {}).get("G7_reciprocity_frame_ontology_compatibility") != "CONDITIONAL":
        errors.append("ontology fork removed")
    if by_id.get("R07", {}).get("G6_finite_cell_boundary_global_response") != "ABSENT":
        errors.append("boundary data promoted to differentiable response")
    if by_id.get("R09", {}).get("disposition") != "PROVENANCE_BLOCKED" or by_id.get("R09", {}).get("G8_noncircular_selection") != "INCOMPATIBLE":
        errors.append("downstream action used circularly")

    premise = {row["premise_id"]: row for row in premises}
    if premise.get("P11", {}).get("status") != "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED":
        errors.append("strong CSN promoted")
    if premise.get("P09", {}).get("status") != "OBSERVED_ANCHOR" or premise.get("P10", {}).get("status") != "OBSERVED_ANCHOR":
        errors.append("observed anchor promoted selector")
    channel = {row["channel_id"]: row for row in channels}
    if set(channel) != {f"C{i:02d}" for i in range(1, 8)}:
        errors.append("multiobservable channel universe mismatch")
    if channel.get("C01", {}).get("owner_status") != "OWNER_NAMED_POSSIBLE_BOOTSTRAP_PARAMETER":
        errors.append("energy channel lost or promoted")
    if channel.get("C03", {}).get("owner_status") != "OWNER_NAMED_POSSIBLE_BOOTSTRAP_PARAMETER":
        errors.append("curvature channel lost or promoted")
    if channel.get("C07", {}).get("owner_status") != "OWNER_EXPLICITLY_OPEN":
        errors.append("other-parameter channel closed")
    closure_by_id = {row.get("arrow_id", ""): row for row in closure}
    if set(closure_by_id) != {f"GL{i:02d}" for i in range(1, 6)}:
        errors.append("global-local closure universe mismatch")
    if closure_by_id.get("GL01", {}).get("current_status") != "WORKING_TYPE_NOT_DERIVED":
        errors.append("global-to-local arrow promoted")
    if closure_by_id.get("GL02", {}).get("current_status") != "CONDITIONAL_TYPE_NOT_COMPLETE":
        errors.append("local-to-global arrow promoted")
    if closure_by_id.get("GL03", {}).get("current_status") != "WORKING_BOOTSTRAP_HYPOTHESIS":
        errors.append("fixed-point hypothesis promoted")
    if closure_by_id.get("GL04", {}).get("current_status") != "OPEN_STRONGER_PREMISE":
        errors.append("scalar extremization promoted without objective")
    if closure_by_id.get("GL04", {}).get("direction") != "scalar_extremization_realization":
        errors.append("scalar extremization label regressed")
    semantic_by_term = {row.get("term", ""): row for row in semantics}
    if set(semantic_by_term) != {"TUNING_OR_CLOSURE", "SCALAR_EXTREMIZATION_REALIZATION"}:
        errors.append("optimization semantics universe mismatch")
    if semantic_by_term.get("TUNING_OR_CLOSURE", {}).get("status") != "WORKING_BOOTSTRAP_HYPOTHESIS":
        errors.append("owner tuning hypothesis lost")
    if semantic_by_term.get("SCALAR_EXTREMIZATION_REALIZATION", {}).get("status") != "OPEN_STRONGER_PREMISE":
        errors.append("scalar extremization promoted")

    required_rulings = {
        "density_window": "ON_SHELL_ADMISSIBILITY_NO_INTERIOR_RESPONSE",
        "tracefree_angular_channel": "NATIVE_MASS_VARIATION_OR_OTHER_CLOSURE_COMPONENT_REQUIRED",
        "multiobservable_bootstrap": "EXACT_COUPLED_TWO_ARROW_SKELETON_WITH_UNSELECTED_BRANCH_MAP_RECOMPUTATION_MAP_JACOBIAN_AND_DUAL_COVECTOR",
        "minimum_missing_object": "DIFFERENTIABLE_COUPLED_GLOBAL_LOCAL_CLOSURE_SECTION_PLUS_NATIVE_DUAL_PAIRING_AND_BRANCH_REGULARITY",
        "curvature_candidate": "TRACEFREE_BULK_RESPONSE_MATHEMATICALLY_AVAILABLE_BUT_NOT_SELECTED_NATIVE_CLOSURE_COMPONENT",
    }
    if algebra.get("sympy_version") != "1.14.0" or algebra.get("check_count") != 38 or set(algebra.get("checks", {}).values()) != {"PASS"}:
        errors.append("pinned algebra replay invalid")
    for key, value in required_rulings.items():
        if algebra.get("structural_rulings", {}).get(key) != value:
            errors.append(f"algebra ruling mismatch: {key}")

    if len(sources) != 15 or len({row.get("source_id") for row in sources}) != 15:
        errors.append("source manifest cardinality")
    for row in sources:
        path = ROOT / row.get("path", "")
        if not path.is_file():
            errors.append(f"missing source: {row.get('source_id')}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != row.get("sha256"):
            errors.append(f"source hash mismatch: {row.get('source_id')}")
            continue
        blob = subprocess.run(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
                              check=True, text=True, capture_output=True).stdout.strip()
        if blob != row.get("git_blob"):
            errors.append(f"source blob mismatch: {row.get('source_id')}")
    return errors


def rejected(name, matrix, universe, premises, channels, closure, semantics, algebra, sources, mutate) -> dict[str, object]:
    items = [deepcopy(matrix), deepcopy(universe), deepcopy(premises), deepcopy(channels), deepcopy(closure), deepcopy(semantics), deepcopy(algebra), deepcopy(sources)]
    mutate(*items)
    errors = validate(*items)
    return {"name": name, "rejected": bool(errors), "first_error": errors[0] if errors else ""}


def main() -> None:
    matrix = tsv(HERE / "CANDIDATE_RESPONSE_MAP_MATRIX.tsv")
    universe = tsv(HERE / "CANDIDATE_MAP_UNIVERSE.tsv")
    premises = tsv(HERE / "PREMISE_LEDGER.tsv")
    channels = tsv(HERE / "PREREGISTERED_PARAMETER_CHANNELS.tsv")
    closure = tsv(HERE / "GLOBAL_LOCAL_CLOSURE_LEDGER.tsv")
    semantics = tsv(HERE / "OPTIMIZATION_SEMANTICS.tsv")
    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    sources = tsv(HERE / "SOURCE_MANIFEST.tsv")
    errors = validate(matrix, universe, premises, channels, closure, semantics, algebra, sources)
    row = lambda data, cid: next(item for item in data if item["candidate_id"] == cid)
    premise = lambda data, pid: next(item for item in data if item["premise_id"] == pid)
    channel = lambda data, cid: next(item for item in data if item["channel_id"] == cid)
    arrow = lambda data, aid: next(item for item in data if item["arrow_id"] == aid)
    term = lambda data, name: next(item for item in data if item["term"] == name)
    common = (matrix, universe, premises, channels, closure, semantics, algebra, sources)
    proofs = [
        rejected("missing_candidate", *common, lambda m,u,p,c,g,o,a,s: m.pop()),
        rejected("duplicate_candidate", *common, lambda m,u,p,c,g,o,a,s: m.append(deepcopy(m[0]))),
        rejected("generated_candidate", *common, lambda m,u,p,c,g,o,a,s: m.__setitem__(0, {**m[0], "candidate_id": "R10"})),
        rejected("nonpass_complete_survivor", *common, lambda m,u,p,c,g,o,a,s: row(m,"R04").__setitem__("disposition", "DERIVED_COMPLETE_RESPONSE_MAP")),
        rejected("window_called_Euler", *common, lambda m,u,p,c,g,o,a,s: row(m,"R01").__setitem__("G3_off_shell_differentiability", "PASS")),
        rejected("on_shell_called_response", *common, lambda m,u,p,c,g,o,a,s: row(m,"R01").__setitem__("disposition", "DERIVED_CONDITIONAL_RESPONSE_SKELETON")),
        rejected("density_window_ontology_promoted", *common, lambda m,u,p,c,g,o,a,s: row(m,"R01").__setitem__("G7_reciprocity_frame_ontology_compatibility", "PASS")),
        rejected("volume_called_angular", *common, lambda m,u,p,c,g,o,a,s: row(m,"R02").__setitem__("G4_local_tracefree_angular_response", "PASS")),
        rejected("external_mass_called_native", *common, lambda m,u,p,c,g,o,a,s: row(m,"R03").__setitem__("G5_same_solution_native_mass_volume", "PASS")),
        rejected("density_number_called_derivative", *common, lambda m,u,p,c,g,o,a,s: a["structural_rulings"].__setitem__("tracefree_angular_channel", "DENSITY_NUMBER_SUFFICIENT")),
        rejected("seal_called_boundary_response", *common, lambda m,u,p,c,g,o,a,s: row(m,"R07").__setitem__("G6_finite_cell_boundary_global_response", "PASS")),
        rejected("strong_CSN_called_derived", *common, lambda m,u,p,c,g,o,a,s: premise(p,"P11").__setitem__("status", "DERIVED")),
        rejected("anchor_called_selector", *common, lambda m,u,p,c,g,o,a,s: premise(p,"P09").__setitem__("status", "FUNCTIONAL_SELECTOR")),
        rejected("unregistered_pairing_called_unique", *common, lambda m,u,p,c,g,o,a,s: row(m,"R04").__setitem__("G8_noncircular_selection", "PASS")),
        rejected("ontology_cross_splice", *common, lambda m,u,p,c,g,o,a,s: row(m,"R05").__setitem__("G7_reciprocity_frame_ontology_compatibility", "PASS")),
        rejected("source_hash_drift", *common, lambda m,u,p,c,g,o,a,s: s[0].__setitem__("sha256", "0"*64)),
        rejected("density_only_bootstrap", *common, lambda m,u,p,c,g,o,a,s: c.pop(0)),
        rejected("energy_promoted_selected", *common, lambda m,u,p,c,g,o,a,s: channel(c,"C01").__setitem__("owner_status", "DERIVED_FUNCTIONAL")),
        rejected("curvature_promoted_selected", *common, lambda m,u,p,c,g,o,a,s: channel(c,"C03").__setitem__("owner_status", "DERIVED_FUNCTIONAL")),
        rejected("multiobservable_jacobian_lost", *common, lambda m,u,p,c,g,o,a,s: a["structural_rulings"].__setitem__("multiobservable_bootstrap", "DENSITY_ONLY")),
        rejected("density_obstruction_promoted_universal", *common, lambda m,u,p,c,g,o,a,s: a["structural_rulings"].__setitem__("tracefree_angular_channel", "NO_BOOTSTRAP_ANGULAR_RESPONSE_POSSIBLE")),
        rejected("global_to_local_arrow_promoted", *common, lambda m,u,p,c,g,o,a,s: arrow(g,"GL01").__setitem__("current_status", "DERIVED")),
        rejected("scalar_extremization_without_objective", *common, lambda m,u,p,c,g,o,a,s: arrow(g,"GL04").__setitem__("current_status", "DERIVED_OPTIMIZATION")),
        rejected("owner_tuning_semantics_lost", *common, lambda m,u,p,c,g,o,a,s: term(o,"TUNING_OR_CLOSURE").__setitem__("status", "OPEN")),
        rejected("scalar_extremization_conflated", *common, lambda m,u,p,c,g,o,a,s: term(o,"SCALAR_EXTREMIZATION_REALIZATION").__setitem__("status", "WORKING_BOOTSTRAP_HYPOTHESIS")),
        rejected("scalar_extremization_label_regressed", *common, lambda m,u,p,c,g,o,a,s: arrow(g,"GL04").__setitem__("direction", "optimization_realization")),
    ]
    if any(not item["rejected"] for item in proofs):
        errors.append("catch proof accepted corruption")
    survivors = [row["candidate_id"] for row in matrix if row["disposition"] == "DERIVED_COMPLETE_RESPONSE_MAP"]
    result = {
        "schema": "udt-bootstrap-to-local-response-verification-1.0",
        "result": "PASS" if not errors else "FAIL",
        "candidate_count": len(matrix),
        "parameter_channel_count": len(channels),
        "global_local_arrow_count": len(closure),
        "survivors": survivors,
        "maximum_conclusion": "NO_DERIVED_COMPLETE_MAP__CONDITIONAL_RESPONSE_SKELETON_AND_MINIMUM_MISSING_OBJECT_IDENTIFIED",
        "catch_proofs": proofs,
        "errors": errors,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
