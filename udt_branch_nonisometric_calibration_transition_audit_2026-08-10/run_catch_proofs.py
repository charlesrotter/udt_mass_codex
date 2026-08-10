#!/usr/bin/env python3
"""Exercise fail-closed mutations against the branch-transition ledger."""

from __future__ import annotations

import copy
import csv
from pathlib import Path

import derive_transition_ownership as prod

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rejected(rows, parent) -> bool:
    try:
        prod.validate(rows, parent)
    except (AssertionError, KeyError):
        return True
    return False


def main() -> None:
    rows = load(HERE / "TRANSITION_OWNERSHIP_ATLAS.tsv")
    parent = load(ROOT / "udt_global_relation_family_branch_classification_2026-08-10/GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv")
    tests = []

    def mutate(name, fn):
        candidate = copy.deepcopy(rows)
        fn(candidate)
        tests.append((name, rejected(candidate, parent)))

    mutate("missing_identity", lambda r: r.pop())
    mutate("duplicate_identity", lambda r: r.append(copy.deepcopy(r[-1])))
    mutate("positive_moved_to_general_screen", lambda r: r[22].update(primary_disposition="COMPLETE_NONISOMETRIC_TRANSITION_OWNED"))
    mutate("w01_promoted_to_branch_owned", lambda r: r[16].update(primary_disposition="COMPLETE_NONISOMETRIC_TRANSITION_OWNED"))
    mutate("w01_not_owned_disclosure_removed", lambda r: r[16].update(nonisometric_transition="A_GAMMA=U_GAMMA_EXP[DELTA_K(P,Q)X_P]"))
    mutate("w01_formula_removed", lambda r: r[16].update(nonisometric_transition="LEVI_CIVITA_ONLY"))
    mutate("w01_clock_owner_removed", lambda r: r[16].update(intrinsic_clock_scale="UNSUPPLIED"))
    mutate("w01_ruler_owner_removed", lambda r: r[16].update(intrinsic_ruler_or_grading="UNSUPPLIED"))
    mutate("w01_carry_replaced_by_reset", lambda r: r[16].update(middle_state_rule="RESET_TO_LOCAL_INTRINSIC_STATE"))
    mutate("w01_open_middle_bridge_erased", lambda r: r[16].update(degeneracy_or_branch_handling="ALL_RESETS_IDENTIFIED"))
    mutate("w01_physical_path_selected", lambda r: r[16].update(scope_caveat="physical path selected"))
    mutate("w02_promoted_to_complete", lambda r: r[17].update(primary_disposition="COMPLETE_NONISOMETRIC_TRANSITION_OWNED"))
    mutate("w02_missing_ruler_hidden", lambda r: r[17].update(intrinsic_ruler_or_grading="RULER_DERIVED"))
    mutate("toric_projector_promoted", lambda r: r[23].update(primary_disposition="COMPLETE_NONISOMETRIC_TRANSITION_OWNED"))
    mutate("historical_fc12_promoted", lambda r: r[11].update(primary_disposition="COMPLETE_NONISOMETRIC_TRANSITION_OWNED"))
    mutate("protected_source_inserted", lambda r: r[0].update(evidence="udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"))
    mutate("physical_scalar_silently_selected", lambda r: r[16].update(terminal_reciprocal_status="PHYSICAL_RELATION_SELECTED"))

    for name, ok in prod.controls().items():
        tests.append((f"exact_control_{name}", ok))
    assert all(ok for _, ok in tests)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("catch_id", "mutation_or_control", "result"))
        for index, (name, ok) in enumerate(tests, 1):
            writer.writerow((f"C{index:02d}", name, "PASS_REJECTED_OR_CONTROL_HELD" if ok else "FAIL"))
    print(f"PASS: {len(tests)}/{len(tests)} catch proofs")


if __name__ == "__main__":
    main()
