#!/usr/bin/env python3
"""Fail-closed semantic/provenance verifier for FC07 harmonic ownership."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
IDS = [f"O{i:02d}" for i in range(1, 5)]
MAXIMUM = (
    "FOUR_UNIQUE_H1_FC07_COMPLETIONS_HAVE_EXACT_RECIPROCAL_HARMONIC_LINE_OWNERSHIP_FOR_ARBITRARY_"
    "SMOOTH_FINITE_DESCENDING_PHI_AND_EVERY_DESCENDING_MEMBER_OF_A_BOUNDED_LOWER_TRIANGULAR_"
    "PAIR_SCREEN_MIXING_CLASS_CONTAINING_THE_REGISTERED_E02_MEMBERS__ANGULAR_AREA_"
    "MODULATES_THE_LOCAL_HARMONIC_AMPLITUDE_THROUGH_A_COMPLETE_CELL_NORMALIZATION__THE_UNRESCALED_"
    "RULER_IS_HARMONIC_IFF_ANGULAR_AREA_IS_CONSTANT__NO_NONTRIVIAL_BACKGROUND_CURVATURE_WINDOW_"
    "NATIVE_RETURN_EQUATION_DENSITY_BRIDGE_XMAX_OR_MATTER"
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(ownership, descent, windows, derivation, independent) -> None:
    assert [r["candidate_id"] for r in ownership] == IDS
    assert [r["candidate_id"] for r in descent] == IDS
    assert len(windows) == 5
    assert all(r["line_ownership"] == "ALL_SMOOTH_NONDEGENERATE_BOUNDED_MEMBERS" for r in ownership)
    assert all(r["rescaled_form"] == "alpha=theta1/(I*sqrt(det(h)))" for r in ownership)
    assert all(r["theta1_harmonic"] == "IFF_d_ds_sqrt_det_h_EQUALS_0" for r in ownership)
    assert all(r["mixing_dependence"] == "NONE_FOR_u_OR_b" for r in ownership)
    assert all(r["mixing_descent_scope"] == "CHOSE_BOUNDED_FIELD_GENERALIZATION_CONTAINING_E02__CONDITIONAL_ON_GLOBAL_DESCENT" for r in ownership)
    assert all(r["physical_selection"] == "NONE" for r in ownership)
    assert all(r["b1"] == "1" and r["invariant_fiber_covector"] == "NONE" for r in descent)
    assert all(r["base_harmonic_line"] == "UNIQUE" and r["descent_status"] == "PASS" for r in descent)
    own_window = next(r for r in windows if r["object"] == "harmonic_line_ownership")
    theta_window = next(r for r in windows if r["object"] == "theta1_itself_harmonic")
    norm_window = next(r for r in windows if r["object"] == "unit_period_normalization")
    density_window = next(r for r in windows if r["object"] == "rho_tot_or_energy_density")
    assert own_window["window_class"] == "NO_NONTRIVIAL_CURVATURE_WINDOW"
    assert own_window["bootstrap_status"] == "KINEMATIC_COMPATIBILITY_NOT_RETURN_EQUATION"
    assert theta_window["window_class"] == "CODIMENSION_CONDITION_NOT_FINITE_RANGE"
    assert theta_window["condition"] == "d_ds_sqrt(det(h))=0"
    assert norm_window["bootstrap_status"] == "NONIDENTITY_GLOBAL_TO_LOCAL_READOUT_NOT_CLOSURE"
    assert density_window["window_class"] == "OPEN_NOT_COMPUTABLE_HERE"
    assert density_window["bootstrap_status"] == "NO_DENSITY_CLAIM"
    assert derivation["all_checks_pass"] and derivation["checks"] == 45
    assert independent["all_checks_pass"] and independent["checks"] == 68
    assert independent["implementation"] == "stdlib_fraction_no_sympy_no_production_import"
    assert derivation["maximum_conclusion"] == MAXIMUM
    assert derivation["harmonic_form"] == "alpha=theta1/(I*sqrt(det(h)));I=int_cell L*exp(phi)/sqrt(det(h)) ds"
    assert derivation["ruler_harmonic_condition"] == "d_ds_sqrt(det(h))=0"
    assert derivation["window_result"] == "NO_NONTRIVIAL_CURVATURE_WINDOW_AT_KINEMATIC_OWNERSHIP_LEVEL"
    assert derivation["bootstrap_result"] == "GLOBAL_TO_LOCAL_READOUT_PRESENT__NO_SAME_SOLUTION_RETURN_EQUATION"
    assert derivation["density_result"] == "OPEN_NO_NATIVE_DENSITY_CURVATURE_BRIDGE"
    assert derivation["mixing_field_promotion_status"] == "CHOSE_BOUNDED_GENERALIZATION_NOT_DERIVED"
    for field in (
        "nontrivial_background_window_derived",
        "native_return_equation_derived",
        "density_curvature_bridge_derived",
        "physical_completion_selected",
        "matter_or_source_derived",
        "mixing_descent_law_derived",
    ):
        assert derivation[field] is False


def verify_sources() -> int:
    source_rows = rows("SOURCE_MANIFEST.tsv")
    assert len(source_rows) == len({r["path"] for r in source_rows}) == 16
    for row in source_rows:
        entry = subprocess.run(
            ["git", "ls-tree", row["base_commit"], "--", row["path"]],
            cwd=ROOT, text=True, capture_output=True, check=True,
        ).stdout.split()
        payload = subprocess.run(
            ["git", "show", f"{row['base_commit']}:{row['path']}"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        assert entry[2] == row["git_blob"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
        assert len(payload) == int(row["bytes"])
    return len(source_rows)


def verify_anchors() -> int:
    sources = {r["path"]: r for r in rows("SOURCE_MANIFEST.tsv")}
    anchors = rows("SOURCE_ANCHOR_LEDGER.tsv")
    assert len(anchors) == 13
    for row in anchors:
        source = sources[row["path"]]
        text = subprocess.run(
            ["git", "show", f"{source['base_commit']}:{row['path']}"],
            cwd=ROOT, text=True, capture_output=True, check=True,
        ).stdout
        assert row["exact_anchor"] in text, (row["path"], row["exact_anchor"])
    return len(anchors)


def import_guard() -> None:
    production = ast.parse((HERE / "derive_harmonic_ownership.py").read_text(encoding="utf-8"))
    independent = ast.parse((HERE / "verify_harmonic_independent.py").read_text(encoding="utf-8"))
    prod_imports = {n.names[0].name for n in ast.walk(production) if isinstance(n, ast.Import)}
    ind_imports = {n.names[0].name for n in ast.walk(independent) if isinstance(n, ast.Import)}
    ind_from = {n.module or "" for n in ast.walk(independent) if isinstance(n, ast.ImportFrom)}
    assert "sympy" in prod_imports
    assert "sympy" not in ind_imports and not any("derive_harmonic" in x for x in ind_from)


def main() -> int:
    ownership = rows("OWNERSHIP_ATLAS.tsv")
    descent = rows("MONODROMY_DESCENT_ATLAS.tsv")
    windows = rows("BACKGROUND_WINDOW_ATLAS.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    scope_correction = (HERE / "SCOPE_CORRECTION.md").read_text(encoding="utf-8")
    assert "CHOSE_BOUNDED_FIELD_GENERALIZATION_CONTAINING_REGISTERED_E02" in scope_correction
    assert "J07/J11 construction/selection remains OPEN" in scope_correction
    validate(ownership, descent, windows, derivation, independent)
    source_count = verify_sources()
    anchor_count = verify_anchors()
    import_guard()

    mutations = []
    for index in range(4):
        changed = deepcopy(ownership); changed[index]["candidate_id"] = "O99"
        mutations.append((changed, deepcopy(descent), deepcopy(windows), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(ownership); changed[0]["theta1_harmonic"] = "ALL_MEMBERS"
    mutations.append((changed, deepcopy(descent), deepcopy(windows), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(ownership); changed[1]["mixing_dependence"] = "REQUIRES_b_ZERO"
    mutations.append((changed, deepcopy(descent), deepcopy(windows), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(ownership); changed[2]["physical_selection"] = "PREFERRED"
    mutations.append((changed, deepcopy(descent), deepcopy(windows), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(descent); changed[3]["invariant_fiber_covector"] = "SELECTED_NONZERO"
    mutations.append((deepcopy(ownership), changed, deepcopy(windows), deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(windows); next(r for r in changed if r["object"] == "harmonic_line_ownership")["window_class"] = "FINITE_DENSITY_WINDOW"
    mutations.append((deepcopy(ownership), deepcopy(descent), changed, deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(windows); next(r for r in changed if r["object"] == "theta1_itself_harmonic")["window_class"] = "FINITE_RANGE"
    mutations.append((deepcopy(ownership), deepcopy(descent), changed, deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(windows); next(r for r in changed if r["object"] == "unit_period_normalization")["bootstrap_status"] = "NATIVE_RETURN_EQUATION"
    mutations.append((deepcopy(ownership), deepcopy(descent), changed, deepcopy(derivation), deepcopy(independent)))
    changed = deepcopy(windows); next(r for r in changed if r["object"] == "rho_tot_or_energy_density")["bootstrap_status"] = "DENSITY_CURVATURE_DERIVED"
    mutations.append((deepcopy(ownership), deepcopy(descent), changed, deepcopy(derivation), deepcopy(independent)))
    for field in (
        "nontrivial_background_window_derived",
        "native_return_equation_derived",
        "density_curvature_bridge_derived",
        "physical_completion_selected",
        "matter_or_source_derived",
        "mixing_descent_law_derived",
    ):
        changed = deepcopy(derivation); changed[field] = True
        mutations.append((deepcopy(ownership), deepcopy(descent), deepcopy(windows), changed, deepcopy(independent)))
    changed = deepcopy(derivation); changed["maximum_conclusion"] = "MATTER_SOURCE_DERIVED"
    mutations.append((deepcopy(ownership), deepcopy(descent), deepcopy(windows), changed, deepcopy(independent)))
    changed = deepcopy(independent); changed["checks"] = 0
    mutations.append((deepcopy(ownership), deepcopy(descent), deepcopy(windows), deepcopy(derivation), changed))

    caught = 0
    for mutation in mutations:
        try:
            validate(*mutation)
        except AssertionError:
            caught += 1
    assert caught == len(mutations)
    result = {
        "schema": "udt.fc07.reciprocal_harmonic_ownership.verification.v1",
        "status": "PASS",
        "source_identities": source_count,
        "source_anchors": anchor_count,
        "semantic_mutations": len(mutations),
        "semantic_mutations_caught": caught,
        "production_checks": derivation["checks"],
        "independent_checks": independent["checks"],
        "maximum_conclusion": MAXIMUM,
        "promotions_rejected": [
            "line_ownership_equals_harmonicity", "kinematic_normalization_equals_equation",
            "nondegeneracy_equals_window", "density_curvature_bridge", "preferred_completion",
            "matter_or_source",
        ],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
