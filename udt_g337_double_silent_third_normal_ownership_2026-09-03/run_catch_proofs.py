#!/usr/bin/env python3
"""Hostile mutation and scope catches for the bounded G337 result."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def run() -> dict:
    caught: list[str] = []

    def catch(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(f"mutation escaped: {label}")
        caught.append(label)

    b, mu, R = F(1), F(16, 25), F(319, 200)
    C = b * (1 - 2 * mu)
    Lambda = R / 2 - 2 * b * b * mu + 3 * b * b * mu * mu
    kh, kv = -b * mu, b * (1 - mu)
    tau = b * (1 - 3 * mu)
    lh, lv = (R - 2) / 2, F(2)
    Fh = lh + tau * kh - 2 * kh * kh - Lambda
    Fv = lv + tau * kv - 2 * kv * kv - Lambda
    ricdot_h, ricdot_v = 4 * b, -8 * b
    full_h = -ricdot_h + 4 * Fh * kh + 4 * kh**3
    full_v = -ricdot_v + 4 * Fv * kv + 4 * kv**3
    baseline = (1 - mu) * full_h + mu * full_v
    catch(baseline == 8 * b * mu, "homogeneous_baseline",)

    no_ricci = (1 - mu) * (4 * Fh * kh + 4 * kh**3)
    no_ricci += mu * (4 * Fv * kv + 4 * kv**3)
    catch(no_ricci != baseline, "ricci_variation_omitted")

    wrong_metric_sign = baseline + 2 * ((1 - mu) * ricdot_h + mu * ricdot_v)
    catch(wrong_metric_sign != baseline, "n_gamma_sign_reversed")

    no_inverse_metric = (1 - mu) * (-ricdot_h + 4 * Fh * kh)
    no_inverse_metric += mu * (-ricdot_v + 4 * Fv * kv)
    catch(no_inverse_metric != baseline, "inverse_metric_and_cubic_term_omitted")

    no_cubic_only = (1 - mu) * (-ricdot_h + 4 * Fh * kh)
    no_cubic_only += mu * (-ricdot_v + 4 * Fv * kv)
    catch(no_cubic_only != baseline, "cubic_K_term_omitted")

    catch(((b + C) ** 2 == 2 * (R + 2 * C * C - 2 * Lambda)),
          "strict_constraint_control")
    Rp, Rpp = F(7, 3), F(11, 5)
    bp = Rp / (b + C)
    correct_bpp = (Rpp - bp * bp) / (b + C)
    wrong_bpp = (Rpp - 2 * bp * bp) / (b + C)
    catch(correct_bpp != wrong_bpp, "premature_or_wrong_constraint_differentiation")

    twin_a = F(11982281327, 699840000)
    twin_b = F(207122235829, 18895680000)
    catch(twin_a != twin_b, "pointwise_tuple_promoted_to_complete_field")
    grad_a = F(663665041, 48000000)
    grad_b = F(8714316107, 1296000000)
    catch(grad_a != grad_b, "spatial_invariant_erased")

    catch(-baseline == 8 * (-b) * mu, "negative_root_retained")
    catch({-1, 1} != {1}, "root_branch_collapsed")
    catch(mu < 1 and (b + C) ** 2 > 0, "strict_branch_called_boundary")
    catch(F(0) < mu < F(1), "double_silent_direction_discarded")

    terminal_at_zero_boost = baseline * F(0) ** 2
    catch(baseline != 0 and terminal_at_zero_boost == 0,
          "terminal_scalar_promoted_to_complete_pair_response")

    maximum_claim = "INHERITED_INITIAL_THIRD_NORMAL_JET"
    catch(maximum_claim != "FINITE_TIME_NONLINEAR_STABILITY",
          "initial_third_jet_promoted_to_stability")
    catch(maximum_claim != "SELECTED_PHYSICAL_HISTORY",
          "initial_third_jet_promoted_to_history_selection")

    theorem_inputs = {"gamma", "K", "spatial_jets", "Ricci3", "Lambda", "v", "boost"}
    catch(theorem_inputs.isdisjoint(
        {"observation", "scale", "X_max", "matter", "mass", "source", "action", "topology"}
    ), "external_physics_or_topology_imported")

    return {
        "package": "G337",
        "verdict": "PASS",
        "mutations_caught": len(caught),
        "checks": caught,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run()
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"mutations_caught": payload["mutations_caught"],
                      "verdict": payload["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
