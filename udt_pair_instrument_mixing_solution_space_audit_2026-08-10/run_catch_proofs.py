#!/usr/bin/env python3
"""Fail-closed algebraic and semantic catches for the G59 landing."""

from __future__ import annotations

import csv
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
READ_ONLY = "--read-only" in sys.argv[1:]


def dot(u: tuple[F, ...], v: tuple[F, ...]) -> F:
    return -u[0] * v[0] + sum(u[i] * v[i] for i in range(1, 4))


def bivector(u: tuple[F, ...], v: tuple[F, ...]) -> dict[tuple[int, int], F]:
    return {(a, b): u[a] * v[b] - u[b] * v[a] for a in range(4) for b in range(a + 1, 4)}


def channels(u: tuple[F, ...], v: tuple[F, ...]) -> tuple[tuple[F, F, F], tuple[F, F, F]]:
    return (
        (-u[0] ** 2 + u[1] ** 2, -u[0] * v[0] + u[1] * v[1], -v[0] ** 2 + v[1] ** 2),
        (u[2] ** 2 + u[3] ** 2, u[2] * v[2] + u[3] * v[3], v[2] ** 2 + v[3] ** 2),
    )


def main() -> None:
    exact = " ".join((HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    report = " ".join((HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    u = (F(2), F(1), F(3), F(-1))
    v = (F(-1), F(4), F(2), F(5))
    h00, h01, h11 = dot(u, u), dot(u, v), dot(v, v)
    det_h = h00 * h11 - h01**2
    b = bivector(u, v)
    r = b[0, 1] ** 2
    a = b[2, 3] ** 2
    ms = -b[0, 2] ** 2 - b[0, 3] ** 2 + b[1, 2] ** 2 + b[1, 3] ** 2
    hr, ha = channels(u, v)

    pure_u = (F(1), F(0), F(0), F(0))
    pure_v = (F(0), F(1), F(0), F(0))
    tilt_u = (F(5, 4), F(0), F(3, 4), F(0))

    q1 = math.sqrt(0.0**2 + 1.0 * (1.0 + 0.25) ** 2)
    q4 = math.sqrt(0.0**2 + 4.0 * (1.0 + 0.25) ** 2)

    catches: dict[str, bool] = {
        "F01_gram_wrong_sign_rejected": det_h == -r + a + ms and det_h != r + a + ms,
        "F02_pluecker_wrong_sign_rejected": (
            b[0, 1] * b[2, 3] - b[0, 2] * b[1, 3] + b[0, 3] * b[1, 2] == 0
        ),
        "F03_missing_angular_matrix_rejected": (
            (hr[0] + ha[0], hr[1] + ha[1], hr[2] + ha[2]) == (h00, h01, h11)
            and hr != (h00, h01, h11)
        ),
        "F04_cross_term_required": det_h - (hr[0] * hr[2] - hr[1] ** 2) - (ha[0] * ha[2] - ha[1] ** 2) == ms,
        "F05_same_h_not_same_orchestra": (
            (dot(pure_u, pure_u), dot(pure_u, pure_v), dot(pure_v, pure_v))
            == (dot(tilt_u, tilt_u), dot(tilt_u, pure_v), dot(pure_v, pure_v))
            and channels(pure_u, pure_v) != channels(tilt_u, pure_v)
        ),
        "F06_full_ambient_invariance_overclaim_rejected": channels(pure_u, pure_v) != channels(tilt_u, pure_v),
        "F07_unique_positive_weight_rejected": q1 != q4,
        "F08_positive_boost_quadratic_rejected": all(-F(av) ** 2 <= 0 for av in range(-5, 6)),
        "F09_physical_regime_not_assigned": "No physical regime label is attached" in exact,
        "F10_cE_not_weight_selector": "does not select `H_R`, `H_A`" in exact,
        "F11_split_ownership_conditional": "conditional on the split" in exact.lower(),
        "F12_R17_not_universal": "R17 remains conditional" in (
            HERE / "STATUS_LEDGER.tsv"
        ).read_text(encoding="utf-8"),
        "F13_time_live_path_open": "physical curve through this solution space remains `OPEN`" in exact,
        "F14_strong_CSN_inactive": "strong local CSN is inactive" in exact,
        "F15_pair_state_not_erased": "are not erased by this plane atlas" in exact,
        "F16_null_boundary_present": "NULL_CROSSOVER" in (HERE / "STRATA_ATLAS.tsv").read_text(encoding="utf-8"),
        "F17_rank_loss_present": "PAIR_RANK_LOSS" in (HERE / "STRATA_ATLAS.tsv").read_text(encoding="utf-8"),
        "F18_landing_exact": result["status"] == "SPLIT_RELATIVE_SIGNED_ORCHESTRA_ATLAS",
        "F19_scope_bounded": "bounded to local algebra" in report,
        "F20_no_action_claim": "No action, source, matter" in (HERE / "NEXT_STEP.md").read_text(encoding="utf-8"),
        "F21_all_components_live": "No component is set to zero" in exact,
        "F22_generic_not_global_uniqueness": "generic continuous split-frame orbit" in exact,
    }

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        paths = [row["path"] for row in csv.DictReader(handle, delimiter="\t")]
    catches["F23_protected_atlas_absent"] = not any(
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in path for path in paths
    )
    catches["F24_stopped_draft_absent"] = not any(
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" in path for path in paths
    )

    failed = sorted(name for name, passed in catches.items() if not passed)
    payload = {
        "schema_version": 1,
        "catch_count": len(catches),
        "caught_count": sum(catches.values()),
        "failed": failed,
        "catches": catches,
    }
    if not READ_ONLY:
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    assert not failed, failed
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
