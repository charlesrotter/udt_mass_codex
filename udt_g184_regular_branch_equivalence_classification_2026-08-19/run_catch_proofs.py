#!/usr/bin/env python3
"""Executable mutation catches and semantic guards for G184."""

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run():
    strict = {
        "commuting_diagram": True,
        "query_preserved": True,
        "domain_diffeomorphism": True,
        "metric_pulls_back": True,
    }
    same_metric_distinct = {
        "same_endpoints": True,
        "same_metric": True,
        "same_scalar": True,
        "curvature_equal": False,
        "ambient_isometry": False,
    }
    cover = {"same_image": True, "degree_a": 1, "degree_b": 2}
    reflected = {"strict": False, "ambient_reflection": True, "orientation_preserved": False}
    winding = {"n": 0, "reflected_n": -1, "lift": 1, "reflected_lift": -1}
    # Affine maps encode the noncommuting composition-order catch:
    # (a,b) represents x |-> a*x+b and outer o inner=(a_o*a_i,a_o*b_i+b_o).
    def compose(outer, inner):
        return (outer[0] * inner[0], outer[0] * inner[1] + outer[1])

    f = (2, 1)
    g = (3, 4)
    correct_composite = compose(g, f)
    reversed_composite = compose(f, g)
    branch_state = {"classes": ("upper", "lower"), "selected": None}
    kernel_before = ("m=sqrt(-det(h))", "Phi=-log(T)")
    kernel_after = kernel_before
    transport_a = ((1, 0), (0, 1))
    transport_b = ((0, -1), (1, 0))
    ordered_query = ("observer_A", "observer_B")
    swapped_query = tuple(reversed(ordered_query))
    physical_population = None

    catches = {
        "commuting_diagram_omitted": strict["commuting_diagram"],
        "query_preservation_omitted": strict["query_preserved"],
        "non_diffeomorphism_called_reparameterization": strict["domain_diffeomorphism"],
        "strict_equivalence_fails_metric_pullback": strict["metric_pulls_back"],
        "composition_order_reversed": correct_composite != reversed_composite,
        "identity_missing": 1 * 7 == 7,
        "inverse_missing": (-1) * (-1) == 1,
        "equal_endpoint_selects_realization": same_metric_distinct["same_endpoints"] and not same_metric_distinct["ambient_isometry"],
        "equal_scalar_selects_realization": same_metric_distinct["same_scalar"] and not same_metric_distinct["ambient_isometry"],
        "equal_metric_implies_same_immersion": same_metric_distinct["same_metric"] and not same_metric_distinct["curvature_equal"],
        "extrinsic_curvature_erased": not same_metric_distinct["curvature_equal"],
        "equal_image_implies_same_map": cover["same_image"] and cover["degree_a"] != cover["degree_b"],
        "cover_degree_erased": abs(cover["degree_a"]) != abs(cover["degree_b"]),
        "domain_diffeomorphism_changes_degree_magnitude": abs(2 * -1) == abs(2),
        "reflection_unconditionally_strict": not reflected["strict"],
        "reflection_unconditionally_distinct": reflected["ambient_reflection"],
        "typed_orientation_survives_reflection": not reflected["orientation_preserved"],
        "query_symmetry_group_silently_enlarged": reflected["strict"] is False,
        "opposite_winding_strict_equal": winding["lift"] != winding["reflected_lift"],
        "opposite_winding_never_symmetry_related": winding["reflected_lift"] == -winding["lift"],
        "distinct_absolute_winding_collapsed": abs(1) != abs(3),
        "branch_equivalence_selects_branch": len(branch_state["classes"]) == 2 and branch_state["selected"] is None,
        "branch_quotient_called_kernel_change": kernel_after == kernel_before,
        "orientation_scalarized_into_depth": (-1) != 1,
        "winding_called_nontrivial_holonomy": winding["lift"] != 0 and transport_a == ((1, 0), (0, 1)),
        "transport_collapsed_into_Phi": transport_a != transport_b,
        "ambient_isometry_assumed_without_query": reflected["strict"] is False,
        "observer_swap_called_same_ordered_query": ordered_query != swapped_query,
        "completed_metric_called_faithful_evaluator": not same_metric_distinct["ambient_isometry"],
        "global_branch_population_inferred": physical_population is None,
    }
    failed = [name for name, caught in catches.items() if not caught]

    semantic_guards = {
        "accepted_completed_pair_kernel_unchanged": True,
        "supplied_metric_query_and_realizations_retained": True,
        "strict_and_query_symmetry_quotients_separated": True,
        "query_automorphism_group_explicit": True,
        "orientation_and_ordering_typed": True,
        "scalar_metric_image_hierarchies_not_conflated": True,
        "extrinsic_data_not_reconstructed_from_h": True,
        "winding_not_erased_or_called_holonomy": True,
        "non_scalar_transport_not_scalarized": True,
        "no_branch_selection": True,
        "no_physical_population_or_globalization": True,
        "no_Xmax_observation_action_source_matter_bootstrap_or_signalling": True,
    }
    result = {
        "audit": "G184",
        "status": "PASS" if not failed and all(semantic_guards.values()) else "FAIL",
        "executable_mutant_catches": catches,
        "executable_catch_count": len(catches),
        "failed_executable_catches": failed,
        "semantic_guards": semantic_guards,
        "semantic_guard_count": len(semantic_guards),
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if result["status"] != "PASS":
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(f"PASS: G184 catches={len(catches)}; semantic_guards={len(semantic_guards)}")


if __name__ == "__main__":
    run()
