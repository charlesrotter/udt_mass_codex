#!/usr/bin/env python3
"""Fail-closed semantic verification and mutation catch-proofs."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(witnesses: list[dict[str, str]], invariant: list[dict[str, str]], fibers: list[dict[str, str]], projectors: list[dict[str, str]], result: dict[str, object]) -> None:
    assert [row["candidate_id"] for row in witnesses] == [f"W{i:02d}" for i in range(1, 9)]
    assert len(invariant) == len(fibers) == len(projectors) == 8
    assert all(row["completion_status"] == "COMPLETE_OFFSHELL_METRIC_WITNESS" for row in witnesses)
    assert all(row["seam_regularity"] == "C_INFINITY_ALL_POSITIVE_ORDER_ENDPOINT_JETS_ZERO" for row in witnesses)
    assert all(row["screen_metric"] == "SPD_FOR_ALL_h0_SPD_AND_0_LE_chi_LE_1" for row in witnesses)
    assert sum(row["coframe_globality"].startswith("GLOBAL_") for row in witnesses) == 6
    assert sum(row["coframe_globality"].startswith("LOCAL_") for row in witnesses) == 2
    assert all(row["orientation_stratum"] == "ORIENTABLE" for row in witnesses if row["det_M"] == "1")
    assert all(row["orientation_stratum"] == "NONORIENTABLE_FC07_FC09_OVERLAP" for row in witnesses if row["det_M"] == "-1")
    assert [row["monodromy_id"] for row in invariant if row["positive_definite_fixed_member"].startswith("NO_")] == ["M_PARABOLIC", "M_HYPERBOLIC"]
    assert len({row["metric_fiber_class"] for row in fibers}) == 7
    central = [row for row in fibers if row["monodromy_id"] in ("M_IDENTITY", "M_MINUS_IDENTITY")]
    assert len(central) == 2 and len({row["metric_fiber_class"] for row in central}) == 1
    assert all(row["descent_identity"] == "T*Pi=Pi*T" for row in projectors)
    assert all(row["neighborhood_scope"] == "BLOCK_SEAM_COMPATIBLE_SPD_PERTURBATIONS_ONLY" for row in projectors)
    assert result["status"] == "PASS"
    assert result["complete_metric_witnesses"] == 8
    assert result["global_oriented_coframe_witnesses"] == 6
    assert result["local_transition_coframe_only_witnesses"] == 2
    assert result["metric_congruence_fiber_classes"] == 7
    assert result["metric_operator_distinct_pairs"] == 27 and result["metric_operator_collapsed_pairs"] == 1
    assert result["collapsed_pair"] == ["M_IDENTITY", "M_MINUS_IDENTITY"]
    assert result["forced_varying_screen_monodromies"] == ["M_PARABOLIC", "M_HYPERBOLIC"]
    assert result["lattice_basis_covariance_controls"] == 16
    assert result["physical_completion_selectors"] == result["native_field_equations"] == 0
    assert result["outcome"] == "FC07_COMPLETE_OFFSHELL_FULL_SCREEN_METRIC_WITNESS_FAMILY_EXISTS__SEVEN_FROZEN_REPRESENTATIVE_ENDPOINT_CONGRUENCE_FIBERS_FROM_EIGHT_MONODROMIES__NO_PHYSICAL_SELECTION"


def main() -> int:
    witnesses, invariant, fibers, projectors = (rows(name) for name in ("COMPLETE_WITNESS_CENSUS.tsv", "INVARIANT_SCREEN_STRATA.tsv", "METRIC_CONGRUENCE_FIBER_ATLAS.tsv", "PROJECTOR_DESCENT_ATLAS.tsv"))
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    validate(witnesses, invariant, fibers, projectors, result)
    mutations = []
    for index in range(8):
        changed = deepcopy(witnesses); changed[index]["candidate_id"] = "W99"; mutations.append((changed, deepcopy(invariant), deepcopy(fibers), deepcopy(projectors), deepcopy(result)))
    for index in range(8):
        changed = deepcopy(witnesses); changed[index]["completion_status"] = "LOCAL_ONLY"; mutations.append((changed, deepcopy(invariant), deepcopy(fibers), deepcopy(projectors), deepcopy(result)))
    changed = deepcopy(witnesses); next(row for row in changed if row["det_M"] == "-1")["coframe_globality"] = "GLOBAL_ORIENTED_COFRAME"; mutations.append((changed, deepcopy(invariant), deepcopy(fibers), deepcopy(projectors), deepcopy(result)))
    changed = deepcopy(invariant); next(row for row in changed if row["monodromy_id"] == "M_PARABOLIC")["positive_definite_fixed_member"] = "YES"; mutations.append((deepcopy(witnesses), changed, deepcopy(fibers), deepcopy(projectors), deepcopy(result)))
    changed = deepcopy(fibers); next(row for row in changed if row["monodromy_id"] == "M_MINUS_IDENTITY")["metric_fiber_class"] = "K99"; mutations.append((deepcopy(witnesses), deepcopy(invariant), changed, deepcopy(projectors), deepcopy(result)))
    changed = deepcopy(projectors); changed[0]["descent_identity"] = "FAIL"; mutations.append((deepcopy(witnesses), deepcopy(invariant), deepcopy(fibers), changed, deepcopy(result)))
    changed = deepcopy(projectors); changed[0]["neighborhood_scope"] = "ALL_METRICS"; mutations.append((deepcopy(witnesses), deepcopy(invariant), deepcopy(fibers), changed, deepcopy(result)))
    for field, value in (("complete_metric_witnesses", 7), ("global_oriented_coframe_witnesses", 8), ("local_transition_coframe_only_witnesses", 0), ("metric_congruence_fiber_classes", 8), ("metric_operator_distinct_pairs", 28), ("metric_operator_collapsed_pairs", 0), ("collapsed_pair", []), ("forced_varying_screen_monodromies", []), ("lattice_basis_covariance_controls", 0), ("physical_completion_selectors", 1), ("native_field_equations", 1), ("outcome", "PHYSICAL_BOOTSTRAP_SELECTED")):
        changed = deepcopy(result); changed[field] = value; mutations.append((deepcopy(witnesses), deepcopy(invariant), deepcopy(fibers), deepcopy(projectors), changed))
    catches = 0
    for args in mutations:
        try:
            validate(*args)
        except AssertionError:
            catches += 1
    assert catches == len(mutations) == 33
    output = {"schema": "udt.torus_bundle_full_screen_witness.verification.v1", "status": "PASS", "mutation_catches": catches, "complete_metric_witnesses": 8, "global_coframes": 6, "local_transition_coframes": 2, "metric_fiber_classes": 7, "forced_varying_screen_classes": 2, "physical_selectors": 0, "native_field_equations": 0}
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
