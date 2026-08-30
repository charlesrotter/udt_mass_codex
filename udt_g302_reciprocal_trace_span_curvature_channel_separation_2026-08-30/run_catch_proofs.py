#!/usr/bin/env python3
"""Hostile mutation checks for the registered G302 load-bearing statements."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def validate(data):
    gate_a = data["gate_A"]
    gate_b = data["gate_B"]
    assert gate_a["all_reciprocal_tangents_metric_trace"] == "0"
    assert gate_a["generator_only_rank"] == 8
    assert gate_a["reciprocal_shape_rank"] == 9
    assert gate_a["complete_metric_rank"] == 10
    assert gate_a["determinant_normalized_pair_change"] == "zero"
    assert "does not select" in gate_a["selection_consequence"]
    assert gate_b["scalar_curvature"] == "R0"
    assert gate_b["weyl_squared"] == "12*b**2/r**6"
    assert gate_b["angular_parallel"] == "3*b/(2*r)"
    assert gate_b["angular_perpendicular"] == "-3*b/(2*r)"
    assert gate_b["R0_absent_from_registered_angular_channels"] is True
    assert gate_b["smooth_areal_center_condition"] == "b=0"
    assert gate_b["domain_strata_count"] == 8
    assert data["physics_changes"]["field_equation_adopted"] is False
    assert data["physics_changes"]["mass_interpretation_adopted"] is False


def main():
    source = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    validate(source)
    mutations = {
        "trace_pollution": lambda d: d["gate_A"].__setitem__("all_reciprocal_tangents_metric_trace", "2"),
        "missing_compound_boost": lambda d: d["gate_A"].__setitem__("reciprocal_shape_rank", 8),
        "dropped_common_scale": lambda d: d["gate_A"].__setitem__("complete_metric_rank", 9),
        "false_tracefree_selection": lambda d: d["gate_A"].__setitem__("selection_consequence", "selects tracefree"),
        "R0_sign_error": lambda d: d["gate_B"].__setitem__("scalar_curvature", "-R0"),
        "false_R0_angular_coupling": lambda d: d["gate_B"].__setitem__("angular_parallel", "3*b/(2*r)+R0*r**2"),
        "angular_factor_error": lambda d: d["gate_B"].__setitem__("angular_perpendicular", "-3*b/r"),
        "false_smooth_b_center": lambda d: d["gate_B"].__setitem__("smooth_areal_center_condition", "any b"),
        "missing_repeated_root_stratum": lambda d: d["gate_B"].__setitem__("domain_strata_count", 7),
        "mass_promotion": lambda d: d["physics_changes"].__setitem__("mass_interpretation_adopted", True),
        "field_equation_promotion": lambda d: d["physics_changes"].__setitem__("field_equation_adopted", True),
    }
    caught = {}
    for name, mutate in mutations.items():
        trial = deepcopy(source)
        mutate(trial)
        try:
            validate(trial)
        except AssertionError:
            caught[name] = True
        else:
            caught[name] = False
    assert all(caught.values())
    output = {"status": "PASS", "caught": caught, "count": len(caught)}
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"G302 catch proofs PASS ({len(caught)}/{len(caught)})")


if __name__ == "__main__":
    main()
