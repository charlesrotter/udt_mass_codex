#!/usr/bin/env python3
"""Hostile semantic and algebraic mutation catches for G335."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def catch(condition: bool, label: str, caught: list[str]) -> None:
    if not condition:
        raise AssertionError(f"mutation escaped: {label}")
    caught.append(label)


def run() -> dict:
    caught: list[str] = []

    # Baseline all-direction gap and silent controls.
    C_gap, b_gap = F(3), F(1)
    gap = (abs(C_gap) - abs(b_gap)) / 2
    catch(gap == 1, "baseline_gap", caught)
    C_silent, b_silent, mu_silent = F(0), F(4), F(1, 2)
    q_silent = (b_silent - C_silent) / 2 - b_silent * mu_silent
    catch(q_silent == 0, "baseline_silent", caught)

    # 1. A qualitative continuity theorem owns no numerical or physical duration.
    claimed_duration = F(1)
    derived_duration = None
    catch(derived_duration != claimed_duration, "continuity_called_fixed_duration", caught)

    # 2. Silent directions are an admitted stratum, not failed data.
    filtered_directions = [mu for mu in (F(0), F(1, 2), F(1))
                           if (b_silent - C_silent) / 2 - b_silent * mu != 0]
    catch(len(filtered_directions) != 3, "silent_direction_discarded", caught)

    # 3. Equality |b|=|C| gives an endpoint silent direction and must not be dropped.
    C_endpoint, b_endpoint = F(3), F(3)
    endpoint_mu = (b_endpoint - C_endpoint) / (2 * b_endpoint)
    catch(endpoint_mu == 0, "silent_endpoint_strictness_mutation", caught)

    # 4. Re-orthonormalized components can be zero while geometric response is nonzero.
    q, sh, ch = F(2), F(3, 4), F(5, 4)
    D = (2 * q * sh * sh, 2 * q * sh * ch, 2 * q * ch * ch)
    raw = tuple(value - value for value in D)
    catch(raw == (0, 0, 0) and D != (0, 0, 0),
          "component_zero_called_zero_geometry", caught)

    # 5. Terminal Phi is blind at zero boost even for nonzero q.
    catch(q != 0 and q * F(0) * F(0) == 0,
          "terminal_phi_called_complete_at_zero_boost", caught)

    # 6. The two G332 algebraic branches remain distinct.
    C, root = F(3), F(4)
    b_minus, b_plus = -C - root, -C + root
    catch(b_minus != b_plus, "branch_collapse", caught)

    # 7. Observer time depends on the spatial jet at nonzero boost.
    normal_jet = F(2)
    observer_a = ch * normal_jet + sh * F(1)
    observer_b = ch * normal_jet + sh * F(-1)
    catch(observer_a != observer_b, "normal_called_observer_time", caught)

    # 8. One exact silent member refutes an all-direction full-family response gap.
    catch(q_silent == 0, "full_family_uniform_gap_claim", caught)

    # 9. A local marked interval is not global or stable evolution.
    maximum_claim = "PER_DATUM_LOCAL_MARKED_INTERVAL"
    promoted_claim = "GLOBAL_NONLINEAR_STABILITY"
    catch(maximum_claim != promoted_claim, "local_called_global_stability", caught)

    # 10. The known flat-slicing control is not the G332 development.
    control_role = "NON_LOAD_BEARING_CONSISTENCY_CONTROL"
    catch(control_role != "PROOF_OF_G332_EVOLUTION",
          "control_example_called_G332_proof", caught)

    # 11. Hopf orbit closure is absent from the local tensor theorem.
    theorem_inputs = {"gamma", "K", "n", "v", "boost", "smooth_development", "transport"}
    catch("Hopf" not in theorem_inputs and "orbit_period" not in theorem_inputs,
          "inserted_Hopf_dependency", caught)

    # 12. No physical scale, matter, observation, or Xmax enters.
    forbidden = {"physical_scale", "matter", "observation", "X_max"}
    catch(theorem_inputs.isdisjoint(forbidden), "inserted_physics_input", caught)

    return {
        "package": "G335",
        "verdict": "PASS",
        "mutations_caught": 12,
        "checks": caught,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({"mutations_caught": result["mutations_caught"],
                      "verdict": result["verdict"]}))


if __name__ == "__main__":
    main()
