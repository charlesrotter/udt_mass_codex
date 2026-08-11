#!/usr/bin/env python3
"""Fail-closed numeric and semantic guard catches for the causal selector result.

These guards enforce the preregistered forbidden-inference surface. They are not an independent
mathematical proof of the universal cone identities or causal-isomorphism classification.
"""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    catches: dict[str, bool] = {}
    derivation = " ".join((HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    T, L, beta = F(3), F(5), F(2, 7)
    rp, rm = -beta + L / T, -beta - L / T
    wp, wm = 1 / rp, 1 / rm
    catches["F01_beta_not_zeroed"] = beta != 0
    catches["F02_one_way_not_invariant"] = wp != T / L and wm != -T / L
    catches["F03_full_graph_mixing_live"] = F(1, 3) ** 2 * F(1, 4) * F(1, 5) != 0
    catches["F04_pullback_not_selector"] = "automatic" in derivation
    catches["F05_nonlinear_maps_retained"] = "f(u)" in derivation
    catches["F06_composition_not_selection"] = "does not select" in derivation
    catches["F07_copresence_not_access"] = "does not mean causal access" in derivation
    catches["F08_no_material_signal_claim"] = "material signal" in derivation
    catches["F09_xmax_not_wall"] = "not a wall" in derivation
    catches["F10_regimes_not_physical_labels"] = "not physical assignments" in derivation
    catches["F11_time_live_not_on_shell"] = "not an on-shell" in derivation
    catches["F12_no_GR_equations"] = "No GR field equation" in derivation
    catches["F13_R17_not_selected"] = "R17 remains a control" in derivation
    catches["F14_branch_path_retained"] = "cut locus" in derivation
    catches["F15_local_not_global"] = "does not imply global" in derivation
    catches["R01_no_physical_family_nonselection_overclaim"] = (
        "DO_NOT_SELECT_THE_PHYSICAL_PAIR_FAMILY" not in derivation
    )
    catches["R02_local_transition_scope_present"] = (
        "local transition/calibration family" in derivation
    )
    catches["R03_no_ambient_multiplicity_theorem"] = (
        "not an ambient-immersion multiplicity theorem" in derivation
    )
    catches["R04_bidirectional_class_explicit"] = (
        "preserves the cone in both directions" in derivation
    )
    catches["R05_branch_speed_notation_repaired"] = (
        "w_+ := (dy^1/dy^0)_+ = 1/r_+" in derivation
        and "w_- := (dy^1/dy^0)_- = 1/r_-" in derivation
    )
    smoke_test = (HERE / "verify_causal_pair_selector_independent.py").read_text(encoding="utf-8")
    catches["R06_sampled_verifier_not_overgraded"] = (
        "sampled_independent_standard_library_fraction_smoke_test" in smoke_test
    )

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        paths = [row["path"] for row in csv.DictReader(stream, delimiter="\t")]
    catches["source_scope"] = not any(
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in path
        or "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" in path
        for path in paths
    )
    failed = sorted(name for name, passed in catches.items() if not passed)
    result = {
        "schema_version": 1,
        "implementation": "mixed_numeric_and_semantic_guards_not_independent_theorem_proof",
        "catch_count": len(catches),
        "caught_count": sum(catches.values()),
        "failed": failed,
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    assert not failed, failed
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
