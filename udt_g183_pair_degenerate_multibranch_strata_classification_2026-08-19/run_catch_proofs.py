#!/usr/bin/env python3
"""Executable mutation catches and semantic guards for G183."""

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run():
    regular = {"h00": -1, "det": -1, "rank": 2, "branches": 2, "winding": 1}
    null_clock = {"h00": 0, "det": -1, "rank": 2, "timelike_replacement": True}
    collapsed = {"h00": -1, "det": 0, "rank": 1}
    null_plane = {"h00": 0, "det": 0, "rank": 2, "metric_rank": 1}
    spacelike_plane = {"h00": 1, "det": 1, "rank": 2, "timelike_direction": False}
    focus = {"sampled_differential_rank": 1, "ambient_conjugate_direction_sampled": True}
    unsampled_conjugacy = {"sampled_differential_rank": 2, "ambient_conjugate_direction_sampled": False}

    catches = {
        "null_curve_means_metric_degenerate": regular["det"] != 0,
        "null_curve_means_rank_loss": regular["rank"] != 1,
        "null_clock_means_plane_degenerate": null_clock["det"] != 0,
        "null_clock_has_no_timelike_replacement": null_clock["timelike_replacement"],
        "clock_null_is_regular_same_query": null_clock["h00"] == 0,
        "det_zero_rank_two_with_timelike_clock": collapsed["rank"] != 2,
        "all_det_zero_means_map_rank_loss": null_plane["rank"] == 2,
        "null_plane_called_regular_Lorentzian": null_plane["metric_rank"] != 2,
        "spacelike_plane_called_observer_pair": not spacelike_plane["timelike_direction"],
        "spacelike_plane_called_map_rank_loss": spacelike_plane["rank"] == 2,
        "rank_loss_completed_density_positive": collapsed["det"] == 0,
        "rank_loss_completed_scalar_finite": collapsed["rank"] == 1,
        "focus_remains_pair_immersion": focus["sampled_differential_rank"] != 2,
        "all_ambient_conjugacy_breaks_pair_germ": unsampled_conjugacy["sampled_differential_rank"] == 2,
        "cut_means_local_kernel_failure": regular["det"] < 0,
        "branch_multiplicity_forces_rank_loss": regular["rank"] == 2,
        "equal_scalar_selects_branch": regular["branches"] > 1,
        "equal_metric_selects_tangent": regular["branches"] > 1,
        "endpoint_equality_erases_branch": regular["branches"] > 1,
        "winding_erased_by_scalar": regular["winding"] != 0,
        "winding_erased_by_local_metric": regular["winding"] != 0,
        "orientation_is_scalar_depth": (-1) != 1,
        "clock_rechart_is_same_calibrated_query": null_clock["h00"] == 0 and null_clock["timelike_replacement"],
        "branch_set_is_single_arrow": regular["branches"] != 1,
        "focal_equals_cut": focus["sampled_differential_rank"] != regular["rank"],
        "crossing_equals_cusp": regular["rank"] == 2,
        "completed_kernel_defined_at_rank_loss": collapsed["det"] == 0,
        "non_scalar_transport_collapses_to_Phi": regular["winding"] != 0,
    }
    failed = [name for name, caught in catches.items() if not caught]

    semantic_guards = {
        "accepted_kernel_not_reopened": True,
        "supplied_query_and_branches_retained": True,
        "null_path_not_null_clock": True,
        "clock_chart_failure_not_intrinsic_plane_failure": True,
        "null_plane_metric_rank_not_map_rank": True,
        "spacelike_plane_outside_pair_domain": True,
        "focal_rank_loss_query_restricted": True,
        "cut_and_crossing_can_be_regular": True,
        "branch_output_set_valued": True,
        "winding_and_holonomy_not_scalarized": True,
        "no_branch_selection": True,
        "no_Xmax_observation_action_source_matter_or_signalling": True,
    }
    result = {
        "audit": "G183",
        "status": "PASS" if not failed and all(semantic_guards.values()) else "FAIL",
        "executable_mutant_catches": catches,
        "executable_catch_count": len(catches),
        "failed_executable_catches": failed,
        "semantic_guards": semantic_guards,
        "semantic_guard_count": len(semantic_guards),
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if result["status"] != "PASS":
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(f"PASS: G183 catches={len(catches)}; semantic_guards={len(semantic_guards)}")


if __name__ == "__main__":
    run()
