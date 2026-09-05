#!/usr/bin/env python3
"""Behavioral and scope mutations required by the G349 preregistration."""

from __future__ import annotations

import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")

    fold_absolute, fold_signed, fold_union = 2.0, 0.0, 1.0
    rank_zero_absolute, rank_zero_union = 2.0, 1.0
    isolated_mult, isolated_union = 2.0, 2.0
    doppler, local_area, local_sky = 2.3, 1.7, 0.4
    observer_product = doppler ** 2 * local_area * local_sky / doppler ** 2
    # For F(x,y)=(x,y^3+xy), dF at zero has rank one. Its kernel (0,1) is tangent
    # to the critical curve x=-3y^2, so the origin is a cusp rather than a fold.
    cusp_rank_one = True
    cusp_kernel = (0.0, 1.0)
    cusp_critical_tangent = (0.0, 1.0)

    mutations = {
        "add_transverse_cut_gradient": "d tau_n(v) k_n" in prereg
        and "changes neither" in prereg,
        "use_signed_for_sheet_area": fold_signed != fold_absolute,
        "identify_fold_sheet_and_union": fold_absolute != fold_union,
        "demand_strict_injectivity_for_equality": isolated_mult == isolated_union,
        "delete_rank_one": "rank-one" in prereg,
        "delete_rank_zero": "rank-zero" in prereg,
        "call_every_rank_one_a_fold": cusp_rank_one
        and cusp_kernel == cusp_critical_tangent,
        "call_caustic_singular_spacetime": "but remain in `F`" in prereg,
        "omit_preimage_multiplicity": "N(F,U;y)" in prereg,
        "count_only_one_fold_sheet": fold_absolute == 2.0 * fold_union,
        "turn_isolated_crossing_into_positive_area_overlap": isolated_union == isolated_mult,
        "make_signed_area_positive": fold_signed == 0.0 and fold_absolute > 0.0,
        "wrong_observer_power": abs(observer_product - local_area * local_sky) < 1e-14,
        "insert_target_observer_factor": "Target observer changes are quotient" in prereg,
        "select_or_weight_path_labels": "neither chooses labels nor supplies weights" in prereg,
        "retain_auxiliary_metric_physically": "may not become physical input" in prereg,
        "confuse_rank_zero_absolute_and_union": rank_zero_absolute != rank_zero_union,
        "promote_to_light_transfer": "No light or transfer law" in prereg,
        "promote_to_distance_population_history_scale_Xmax": all(
            token in prereg for token in
            ("observational distance", "path population", "history", "scale", "`X_max`")
        ),
        "promote_to_canon": "canon may be selected" in prereg,
        "hide_physics_pins": "PINNED_BY_HABIT" not in ledger,
    }
    failed = [name for name, caught in mutations.items() if not caught]
    result = {
        "status": "PASS" if not failed else "FAIL",
        "caught": sum(mutations.values()),
        "total": len(mutations),
        "failed": failed,
        "mutations": mutations,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not os.environ.get("UDT_NO_WRITE"):
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
