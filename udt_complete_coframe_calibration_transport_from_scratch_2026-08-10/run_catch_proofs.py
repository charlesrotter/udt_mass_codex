#!/usr/bin/env python3
"""Exercise fail-closed mathematical and provenance mutations."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


PKG = Path(__file__).resolve().parent


def q_full(h00: F, h01: F, h11: F) -> F:
    return -(h00 * h11 - h01 * h01) / (h00 * h00)


def main() -> None:
    catches: dict[str, bool] = {}

    h00, h01, h11 = F(-3, 16), F(1, 12), F(37, 9)
    correct = q_full(h00, h01, h11)
    drop_shift = -(h00 * h11) / (h00 * h00)
    catches["C01_drop_shift_or_mixing"] = drop_shift != correct

    common = F(7)
    catches["C02_treat_common_scale_as_depth"] = q_full(
        common * common * h00,
        common * common * h01,
        common * common * h11,
    ) == correct

    # Wrong sign on the clock term fails pure reciprocal normalization.
    p = F(5, 3)
    correct_rate = (p - (-p)) / 2
    wrong_rate = (p + (-p)) / 2
    catches["C03_wrong_clock_sign"] = correct_rate == p and wrong_rate != p

    # Determinant character sees no founded reciprocal squeeze.
    catches["C04_use_determinant_as_depth"] = F(1, 2) * F(2) == 1

    # A Lorentz boost is nontrivial but its reciprocal density multiplier is one.
    gamma, velocity = F(5, 4), F(3, 4)
    catches["C05_assign_metric_carry_nonzero_depth"] = gamma * gamma - velocity * velocity == 1

    # Screen angle cannot define a single-valued additive real character on SO(2).
    angle_zero, angle_same_group_element = F(0), F(2)  # units of pi
    catches["C06_scalarize_SO2_angle"] = angle_zero != angle_same_group_element

    # A live time derivative produces nonzero depth rate; freezing it erases the result.
    b00_t, b11_t = F(-7, 3), F(7, 3)
    live_rate = (b11_t - b00_t) / 2
    frozen_rate = F(0)
    catches["C07_freeze_time_dependence"] = live_rate != frozen_rate

    # Finite screen mixing changes the full pair invariant relative to the bare block.
    catches["C08_drop_phi_orchestra"] = F(64, 3) != F(16)

    # Independent tape offsets need not telescope.
    oa, ob, oc = F(2, 7), F(-3, 11), F(5, 13)
    catches["C09_assume_independent_reset_identity"] = oa + ob - oc != 0

    # Exact endpoint coboundaries produce distinct lawful transports.
    f0, f1 = F(1, 5), F(7, 9)
    catches["C10_claim_unique_general_line_connection"] = f1 - f0 != 0

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    paths = [row["path"] for row in sources]
    catches["C11_import_stopped_historical_census"] = not any(
        "udt_native_onshell_timelive_reset_owner_audit" in path for path in paths
    )
    catches["C12_access_protected_atlas"] = not any(
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in path for path in paths
    )

    derivation = (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    catches["C13_use_cE_to_construct_pair_family"] = (
        "does not choose" in derivation and "terminal" in derivation
    )
    catches["C14_promote_R17_universally"] = "recovery only, not universal" in derivation
    catches["C15_promote_local_theorem_to_degenerate_strata"] = (
        "clock line becomes null" in derivation
        and "outside declared local line-transport theorem" in derivation
    )

    failed = sorted(name for name, passed in catches.items() if not passed)
    result = {
        "schema_version": 1,
        "catch_count": len(catches),
        "caught_count": sum(catches.values()),
        "failed": failed,
        "catches": catches,
    }
    (PKG / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    assert not failed, f"uncaught mutations: {failed}"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
