#!/usr/bin/env python3
"""Fail-closed semantic and source verifier for the connector audit."""

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
    "G1_metric_native_local_definition", "G2_local_nontriviality_or_response",
    "G3_global_completion_or_descent", "G4_same_complete_branch_colocation",
    "G5_global_to_local_A_arrow", "G6_local_to_global_R_arrow",
    "G7_finite_cell_boundary_differentiability", "G8_reciprocity_and_metric_ontology",
    "G9_noncircular_bootstrap_selection",
]
ALLOWED = {"PASS", "CONDITIONAL", "ABSENT", "INCOMPATIBLE", "OUT_OF_SCOPE", "PROVENANCE_BLOCKED"}
DISPOSITIONS = {
    "DERIVED_COMPLETE_BOOTSTRAP_CONNECTOR", "DERIVED_CONDITIONAL_NONTRIVIALITY_SKELETON",
    "DERIVED_PARTIAL_CONNECTOR", "CONDITIONAL_CONNECTOR", "LOCAL_ONLY", "GLOBAL_ONLY",
    "TYPE_INCOMPLETE", "ABSENT", "PROVENANCE_BLOCKED",
}
EXPECTED = [f"C{i:02d}" for i in range(1, 14)]
EXPECTED_GATE_ROWS = {
    "C01": ("CONDITIONAL", "CONDITIONAL", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "CONDITIONAL", "ABSENT"),
    "C02": ("PASS", "PASS", "CONDITIONAL", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "PASS", "ABSENT"),
    "C03": ("PASS", "PASS", "CONDITIONAL", "ABSENT", "ABSENT", "CONDITIONAL", "ABSENT", "PASS", "ABSENT"),
    "C04": ("CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT", "ABSENT", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT"),
    "C05": ("CONDITIONAL", "PASS", "CONDITIONAL", "ABSENT", "ABSENT", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT"),
    "C06": ("CONDITIONAL", "PASS", "CONDITIONAL", "ABSENT", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT"),
    "C07": ("CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT", "ABSENT", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT"),
    "C08": ("PASS", "PASS", "CONDITIONAL", "ABSENT", "ABSENT", "ABSENT", "CONDITIONAL", "CONDITIONAL", "ABSENT"),
    "C09": ("PASS", "PASS", "CONDITIONAL", "ABSENT", "ABSENT", "CONDITIONAL", "ABSENT", "PASS", "ABSENT"),
    "C10": ("CONDITIONAL", "CONDITIONAL", "ABSENT", "ABSENT", "PROVENANCE_BLOCKED", "CONDITIONAL", "ABSENT", "CONDITIONAL", "ABSENT"),
    "C11": ("CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT", "ABSENT", "CONDITIONAL", "CONDITIONAL", "CONDITIONAL", "ABSENT"),
    "C12": ("ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT"),
    "C13": ("PASS", "PASS", "ABSENT", "ABSENT", "ABSENT", "CONDITIONAL", "ABSENT", "CONDITIONAL", "ABSENT"),
}


def tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(matrix, universe, premises, strata, loops, algebra, sources) -> list[str]:
    errors: list[str] = []
    ids = [row.get("candidate_id", "") for row in matrix]
    if ids != EXPECTED or [row.get("candidate_id", "") for row in universe] != EXPECTED:
        errors.append("candidate universe mismatch")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate")
    u = {row["candidate_id"]: row for row in universe}
    for row in matrix:
        cid = row.get("candidate_id", "")
        if cid not in u or row.get("connector_family") != u[cid]["connector_family"]:
            errors.append(f"generated or relabeled candidate: {cid}")
        if {row.get(gate, "") for gate in GATES} - ALLOWED:
            errors.append(f"invalid gate: {cid}")
        if row.get("disposition") not in DISPOSITIONS:
            errors.append(f"invalid disposition: {cid}")
        all_pass = all(row.get(gate) == "PASS" for gate in GATES)
        if (row.get("disposition") == "DERIVED_COMPLETE_BOOTSTRAP_CONNECTOR") != all_pass:
            errors.append(f"complete connector equivalence: {cid}")

    by_id = {row["candidate_id"]: row for row in matrix}
    if by_id.get("C01", {}).get("disposition") != "DERIVED_CONDITIONAL_NONTRIVIALITY_SKELETON":
        errors.append("coupled skeleton promoted or lost")
    if by_id.get("C01", {}).get("G4_same_complete_branch_colocation") != "ABSENT":
        errors.append("same-branch witness invented")
    if by_id.get("C02", {}).get("G3_global_completion_or_descent") == "PASS":
        errors.append("local clock kernel promoted globally")
    if by_id.get("C03", {}).get("G9_noncircular_bootstrap_selection") != "ABSENT":
        errors.append("curvature candidate promoted selected")
    if by_id.get("C04", {}).get("G5_global_to_local_A_arrow") != "ABSENT":
        errors.append("density response invented")
    if by_id.get("C07", {}).get("G6_local_to_global_R_arrow") == "PASS":
        errors.append("topology promoted to response")
    if by_id.get("C09", {}).get("disposition") != "LOCAL_ONLY" or by_id.get("C09", {}).get("G3_global_completion_or_descent") == "PASS":
        errors.append("local transport promoted to holonomy")
    if by_id.get("C10", {}).get("G5_global_to_local_A_arrow") != "PROVENANCE_BLOCKED":
        errors.append("missing boundary functional bypassed")
    if by_id.get("C10", {}).get("G7_finite_cell_boundary_differentiability") != "ABSENT":
        errors.append("boundary functional invented")
    if by_id.get("C11", {}).get("disposition") != "GLOBAL_ONLY" or by_id.get("C11", {}).get("G2_local_nontriviality_or_response") == "PASS":
        errors.append("diameter promoted to local response")
    if any(by_id.get("C12", {}).get(gate) == "PASS" for gate in GATES):
        errors.append("native energy or mass invented")
    for cid, expected_values in EXPECTED_GATE_ROWS.items():
        if tuple(by_id.get(cid, {}).get(gate, "") for gate in GATES) != expected_values:
            errors.append(f"adversarial gate matrix drift: {cid}")

    premise = {row["premise_id"]: row for row in premises}
    if premise.get("P05", {}).get("status") != "OWNER_STATED_WORKING":
        errors.append("owner tuning promoted or lost")
    if premise.get("P06", {}).get("status") != "OPEN_STRONGER_PREMISE":
        errors.append("scalar extremization conflated")
    if premise.get("P15", {}).get("status") != "OBSERVED_ANCHOR" or premise.get("P16", {}).get("status") != "OBSERVED_ANCHOR":
        errors.append("observed anchor promoted")
    if premise.get("P19", {}).get("status") != "OPEN_REQUIRED_CHECK" or premise.get("P20", {}).get("status") != "OPEN_REQUIRED_CHECK":
        errors.append("kernel sufficiency promoted")

    if {row.get("stratum_id") for row in strata} != {f"K{i:02d}" for i in range(1, 7)}:
        errors.append("critical strata universe mismatch")
    if any(row.get("physical_status") not in {
        "OPEN_NOT_MATTER", "CONDITIONAL_LOCAL_CANDIDATE", "OPEN_NO_PHYSICAL_TIE_RULE",
        "OPEN_NO_REGIME_LABEL", "OPEN_NO_GLOBAL_SELECTION", "CONDITIONAL_TOPOLOGY_ONLY",
    } for row in strata):
        errors.append("critical stratum promoted physical")
    if {row.get("loop_id") for row in loops} != {f"L{i:02d}" for i in range(1, 5)}:
        errors.append("feedback loop universe mismatch")
    if any("COMPLETE" in row.get("current_grade", "") for row in loops):
        errors.append("feedback loop promoted complete")

    rulings = {
        "two_arrow_nontriviality": "KERNEL_OF_A_X_PLUS_A_O_R_X_IS_EXACT_NECESSARY_INFINITESIMAL_CONDITION",
        "feedback": "GLOBAL_LOCAL_FEEDBACK_CAN_CREATE_OR_REMOVE_AN_INFINITESIMAL_KERNEL",
        "kernel_scope": "KERNEL_IS_NOT_MATTER_WITHOUT_GAUGE_BOUNDARY_DESCENT_AND_NONLINEAR_CONTINUATION",
        "root_scope": "REALIZED_ROOT_DOES_NOT_SELECT_REGULAR_OR_SINGULAR_LINEARIZATION",
        "minimum_missing_object": "COMPLETE_SAME_BRANCH_A_AND_R_MAPS_WITH_GAUGE_BOUNDARY_DESCENT_AND_NONLINEAR_DOMAIN",
        "scalar_bootstrap_insufficiency": "DENSITY_AND_SCALAR_CURVATURE_TRACE_DO_NOT_DETERMINE_POINTWISE_TRACEFREE_RICCI_RESPONSE",
    }
    if algebra.get("sympy_version") != "1.14.0" or algebra.get("check_count") != 31 or set(algebra.get("checks", {}).values()) != {"PASS"}:
        errors.append("pinned algebra replay invalid")
    for key, expected in rulings.items():
        if algebra.get("structural_rulings", {}).get(key) != expected:
            errors.append(f"algebra ruling mismatch: {key}")

    if len(sources) != 16 or len({row.get("source_id") for row in sources}) != 16:
        errors.append("source manifest cardinality")
    evidence = tsv("CONNECTOR_SOURCE_EVIDENCE.tsv")
    if [row.get("candidate_id") for row in evidence] != EXPECTED:
        errors.append("candidate source-evidence coverage")
    source_ids = {row.get("source_id") for row in sources}
    for row in evidence:
        referenced = set(filter(None, (row.get("positive_source_ids", "") + ";"
                                       + row.get("blocking_source_ids", "")).split(";")))
        if not referenced or not referenced <= source_ids:
            errors.append(f"candidate source-evidence identity: {row.get('candidate_id')}")
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


def rejected(name, items, mutate) -> dict[str, object]:
    values = [deepcopy(item) for item in items]
    mutate(*values)
    errors = validate(*values)
    return {"name": name, "rejected": bool(errors), "first_error": errors[0] if errors else ""}


def main() -> None:
    matrix = tsv("CONNECTOR_GATE_MATRIX.tsv")
    universe = tsv("CANDIDATE_CONNECTOR_UNIVERSE.tsv") + tsv("CANDIDATE_CONNECTOR_ADDITION.tsv")
    premises = tsv("PREMISE_LEDGER.tsv")
    strata = tsv("CRITICAL_STRATA_ATLAS.tsv")
    loops = tsv("FEEDBACK_LOOP_CANDIDATES.tsv")
    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    sources = tsv("SOURCE_MANIFEST.tsv")
    items = (matrix, universe, premises, strata, loops, algebra, sources)
    errors = validate(*items)
    row = lambda data, cid: next(item for item in data if item["candidate_id"] == cid)
    premise = lambda data, pid: next(item for item in data if item["premise_id"] == pid)
    proofs = [
        rejected("missing_candidate", items, lambda m,u,p,k,l,a,s: m.pop()),
        rejected("duplicate_candidate", items, lambda m,u,p,k,l,a,s: m.append(deepcopy(m[0]))),
        rejected("generated_candidate", items, lambda m,u,p,k,l,a,s: m.__setitem__(0, {**m[0], "candidate_id": "C13"})),
        rejected("nonpass_complete_connector", items, lambda m,u,p,k,l,a,s: row(m,"C01").__setitem__("disposition", "DERIVED_COMPLETE_BOOTSTRAP_CONNECTOR")),
        rejected("same_branch_splice", items, lambda m,u,p,k,l,a,s: row(m,"C01").__setitem__("G4_same_complete_branch_colocation", "PASS")),
        rejected("local_kernel_called_global", items, lambda m,u,p,k,l,a,s: row(m,"C02").__setitem__("G3_global_completion_or_descent", "PASS")),
        rejected("curvature_called_selected", items, lambda m,u,p,k,l,a,s: row(m,"C03").__setitem__("G9_noncircular_bootstrap_selection", "PASS")),
        rejected("density_called_A_arrow", items, lambda m,u,p,k,l,a,s: row(m,"C04").__setitem__("G5_global_to_local_A_arrow", "PASS")),
        rejected("topology_called_response", items, lambda m,u,p,k,l,a,s: row(m,"C07").__setitem__("G6_local_to_global_R_arrow", "PASS")),
        rejected("transport_called_holonomy", items, lambda m,u,p,k,l,a,s: row(m,"C09").__setitem__("G3_global_completion_or_descent", "PASS")),
        rejected("boundary_arrow_unblocked", items, lambda m,u,p,k,l,a,s: row(m,"C10").__setitem__("G5_global_to_local_A_arrow", "CONDITIONAL")),
        rejected("boundary_called_complete", items, lambda m,u,p,k,l,a,s: row(m,"C10").__setitem__("G7_finite_cell_boundary_differentiability", "PASS")),
        rejected("diameter_called_local_response", items, lambda m,u,p,k,l,a,s: row(m,"C11").__setitem__("G2_local_nontriviality_or_response", "PASS")),
        rejected("energy_called_native", items, lambda m,u,p,k,l,a,s: row(m,"C12").__setitem__("G1_metric_native_local_definition", "PASS")),
        rejected("tuning_promoted", items, lambda m,u,p,k,l,a,s: premise(p,"P05").__setitem__("status", "DERIVED")),
        rejected("scalar_extremization_conflated", items, lambda m,u,p,k,l,a,s: premise(p,"P06").__setitem__("status", "OWNER_STATED_WORKING")),
        rejected("gauge_check_removed", items, lambda m,u,p,k,l,a,s: premise(p,"P19").__setitem__("status", "PASS")),
        rejected("nonlinear_sufficiency_promoted", items, lambda m,u,p,k,l,a,s: premise(p,"P20").__setitem__("status", "DERIVED")),
        rejected("anchor_promoted", items, lambda m,u,p,k,l,a,s: premise(p,"P15").__setitem__("status", "CLOSURE_SELECTOR")),
        rejected("root_determines_linearization", items, lambda m,u,p,k,l,a,s: a["structural_rulings"].__setitem__("root_scope", "ROOT_SELECTS_LINEARIZATION")),
        rejected("kernel_called_matter", items, lambda m,u,p,k,l,a,s: a["structural_rulings"].__setitem__("kernel_scope", "KERNEL_IS_MATTER")),
        rejected("critical_stratum_promoted", items, lambda m,u,p,k,l,a,s: k[0].__setitem__("physical_status", "DERIVED_MATTER")),
        rejected("feedback_loop_promoted", items, lambda m,u,p,k,l,a,s: l[0].__setitem__("current_grade", "COMPLETE_DERIVED_LOOP")),
        rejected("source_hash_drift", items, lambda m,u,p,k,l,a,s: s[0].__setitem__("sha256", "0" * 64)),
    ]
    if any(not proof["rejected"] for proof in proofs):
        errors.append("catch proof accepted corruption")
    result = {
        "schema": "udt-metric-native-nontriviality-connector-verification-1.0",
        "result": "PASS" if not errors else "FAIL",
        "candidate_count": len(matrix),
        "critical_stratum_count": len(strata),
        "feedback_loop_count": len(loops),
        "complete_survivors": [row["candidate_id"] for row in matrix if row["disposition"] == "DERIVED_COMPLETE_BOOTSTRAP_CONNECTOR"],
        "maximum_conclusion": "EXACT_COUPLED_NONTRIVIALITY_SKELETON__NO_COMPLETE_METRIC_NATIVE_BOOTSTRAP_CONNECTOR",
        "catch_proofs": proofs,
        "errors": errors,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
