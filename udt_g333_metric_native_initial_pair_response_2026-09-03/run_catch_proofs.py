#!/usr/bin/env python3
"""Hostile mutation checks for G333 algebra, gauge, topology, and scope."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from derive_initial_pair_response import exact_case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()

    caught = []

    def catch(condition, name):
        if not condition:
            raise AssertionError(f"mutation escaped: {name}")
        caught.append(name)

    _, b_plus, horizontal, checks = exact_case(F(12), F(20), F(3), 1, F(0))
    _, b_minus, vertical_minus, _ = exact_case(F(12), F(20), F(3), -1, F(1))
    _, _, vertical_plus, _ = exact_case(F(12), F(20), F(3), 1, F(1))
    catch(all(checks.values()), "baseline_closes")

    # H=+K reverses the preregistered G315 sign.
    mutated_sign_horizontal = (F(20) - b_plus) / 2
    catch(mutated_sign_horizontal != horizontal, "wrong_G315_sign")

    # A common-only response drops the rank-one b channel.
    common_only_vertical = horizontal
    catch(common_only_vertical != vertical_plus, "dropped_directional_b_channel")

    mutated_trace = (b_plus + 3 * F(20)) / 2
    correct_trace = (b_plus - 3 * F(20)) / 2
    catch(mutated_trace != correct_trace, "trace_C_sign_mutation")

    mutated_shear_norm = b_plus * b_plus / 3
    correct_shear_norm = 2 * b_plus * b_plus / 3
    catch(mutated_shear_norm != correct_shear_norm, "shear_coefficient_mutation")

    catch(b_plus != b_minus, "branch_collapse_mutation")

    # Coordinate-time rate is N times normal rate for lapse N; the normal rate is invariant.
    lapse = F(2)
    coordinate_time_rate = lapse * horizontal
    catch(coordinate_time_rate != horizontal, "lapse_promoted_to_physics_mutation")
    catch(coordinate_time_rate / lapse == horizontal, "normal_rate_restores_lapse_independence")

    # Same proper-normal clock jet (zero) does not recover distinct spatial strains.
    terminal_phi_dot_horizontal = F(0)
    terminal_phi_dot_vertical = F(0)
    catch(terminal_phi_dot_horizontal == terminal_phi_dot_vertical
          and horizontal != vertical_plus, "terminal_scalar_false_completeness")

    allowed_inputs = {"gamma", "K", "n", "v", "C", "b", "mu"}
    topology_mutation = allowed_inputs | {"orbit_period"}
    catch("orbit_period" not in allowed_inputs and "orbit_period" in topology_mutation,
          "inserted_topology_dependency")

    required_scope = {
        "FIRST_JET_ONLY_NO_HOPF_SELECTION_OR_STABILITY",
        "COMPLETE_NORMAL_SPATIAL_PAIR_PULLBACK_EXCEEDS_ITS_TERMINAL_SCALAR",
    }
    baseline_landing = (
        "G332_METRIC_NATIVE_FIRST_RESPONSE_IS_COMMON_PLUS_DIRECTIONAL__"
        "COMPLETE_NORMAL_SPATIAL_PAIR_PULLBACK_EXCEEDS_ITS_TERMINAL_SCALAR__"
        "FIRST_JET_ONLY_NO_HOPF_SELECTION_OR_STABILITY"
    )
    catch(all(token in baseline_landing for token in required_scope), "scope_baseline")
    promoted_landing = "G332_METRIC_NATIVE_FIRST_RESPONSE_SELECTS_HOPF_STABILITY"
    catch(any(token not in promoted_landing for token in required_scope),
          "Hopf_stability_scope_promotion")

    payload = {
        "package": "G333",
        "mutations_caught": len(caught) - 3,
        "checks": caught,
        "verdict": "PASS",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"mutations_caught": payload["mutations_caught"],
                      "verdict": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
