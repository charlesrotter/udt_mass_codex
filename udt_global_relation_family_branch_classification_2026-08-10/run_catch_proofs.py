#!/usr/bin/env python3
"""Exercise fail-closed mutations without modifying the banked ledgers."""

from __future__ import annotations

import copy
import csv
from pathlib import Path

import classify_relation_families as prod

HERE = Path(__file__).resolve().parent


def load(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rejected(fn) -> bool:
    try:
        fn()
    except (AssertionError, KeyError):
        return True
    return False


def main() -> None:
    universe = load("BRANCH_UNIVERSE.tsv")
    atlas = load("GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv")
    crosswalk = load("SOURCE_TO_BRANCH_CROSSWALK.tsv")

    tests = []

    def check(name, mutate):
        u, a, x = copy.deepcopy(universe), copy.deepcopy(atlas), copy.deepcopy(crosswalk)
        mutate(u, a, x)
        tests.append((name, rejected(lambda: prod.classify(u, a, x))))

    check("missing_branch", lambda u, a, x: a.pop())
    check("duplicate_branch", lambda u, a, x: a.append(copy.deepcopy(a[-1])))
    check("taxonomy_promoted_without_metric", lambda u, a, x: a[0].update(primary_disposition="COMMON_CALIBRATED_ATLAS_OWNED"))
    check("path_holonomy_forced_to_common_atlas", lambda u, a, x: a[16].update(primary_disposition="COMMON_CALIBRATED_ATLAS_OWNED"))
    check("stationary_clock_overpromoted_to_physical_pair", lambda u, a, x: a[17].update(caveat="PHYSICAL_RELATION_SELECTED"))
    check("historical_fc12_regrade_removed", lambda u, a, x: a[11].update(primary_disposition="PATH_BRANCH_GROUPOID_OWNED"))
    check("degenerate_slice_called_complete_path", lambda u, a, x: a[20].update(primary_disposition="PATH_BRANCH_GROUPOID_OWNED"))
    check("unowned_scalar_promoted", lambda u, a, x: a[16].update(scalar_reciprocal_reduction="PHYSICAL_RELATION_SELECTED"))
    check("bad_crosswalk_target", lambda u, a, x: x[0].update(stable_branch_id="R99"))
    check("unfrozen_evidence_source", lambda u, a, x: a[0].update(evidence="NOT_FROZEN.md"))

    controls = prod.exact_controls()
    tests.append(("common_atlas_identity_control", controls["common_atlas_triangle_identity"]))
    tests.append(("nonidentity_path_loop_retained", controls["path_loop_may_be_nonidentity"]))
    tests.append(("explicit_middle_transition_retained", controls["explicit_middle_transition_changes_composite"]))
    tests.append(("rank_degenerate_boundary_retained", controls["rank_degenerate_boundary_detected"]))
    tests.append(("protected_source_absent", not any("kernel_plane_global_curvature" in r["evidence"] for r in atlas)))

    assert all(ok for _, ok in tests)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("catch_id", "mutation_or_control", "result"))
        for index, (name, ok) in enumerate(tests, 1):
            writer.writerow((f"C{index:02d}", name, "PASS_REJECTED_OR_CONTROL_HELD" if ok else "FAIL"))
    print(f"PASS: {len(tests)}/{len(tests)} catch proofs")


if __name__ == "__main__":
    main()
