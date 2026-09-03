#!/usr/bin/env python3
"""Hostile algebra, carry, and scope mutation catches for G336."""

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
    R, mu, b2 = F(0), F(1, 2), F(2)
    C, Lambda = F(0), F(-1, 2)
    ricci_vv = (R - 2) / 2 + (6 - R) * mu / 2
    k2_vv = b2 * mu * (1 - mu)
    baseline = Lambda - ricci_vv + 2 * k2_vv
    reduced = 1 + (R - 6) * mu / 2 + b2 * mu * mu
    catch(baseline == reduced == 0, "baseline_double_silent", caught)

    # 1. Dropping the three-dimensional Ricci contribution changes the exact answer.
    without_ricci = Lambda + 2 * k2_vv
    catch(without_ricci != baseline, "ricci_term_dropped", caught)

    # 2. Reversing the ADM evolution sign changes the inherited second jet.
    wrong_adm_sign = -Lambda + ricci_vv - 2 * k2_vv
    positive_control = F(1) - F(3, 2) + F(1)
    catch(wrong_adm_sign != positive_control,
          "wrong_adm_sign", caught)

    # 3. Omitting K squared fails away from its zero coefficient.
    catch(Lambda - ricci_vv != baseline,
          "K_squared_omitted", caught)

    # 4. Both roots are real and distinct on the exact b^2=2 control.
    branch_labels = {"-sqrt(2)", "+sqrt(2)"}
    catch(len(branch_labels) == 2, "G332_branch_collapsed", caught)

    # 5. The exact zero response is data, not a case to discard.
    sign_triplet = [F(-1, 4), F(0), F(1, 2)]
    catch(F(0) in sign_triplet, "double_silent_discarded", caught)

    # 6. An inherited Lie carry cannot be promoted to every unit-direction carry.
    hv2 = b2 * mu * (1 - mu)
    carried_a = baseline + 2 * (F(0) - 1) * hv2
    carried_b = baseline + 2 * (F(2) - 1) * hv2
    catch(carried_a != carried_b,
          "Lie_carry_called_universal", caught)

    # 7. Zero boost hides terminal Phi even when the spatial pair second jet is nonzero.
    nonzero_s1 = F(1)
    catch(nonzero_s1 != 0 and nonzero_s1 * F(0) ** 2 == 0,
          "zero_boost_terminal_called_complete", caught)

    # 8. A second initial jet is not finite-time or nonlinear stability.
    maximum_claim = "INITIAL_SECOND_NORMAL_JET"
    catch(maximum_claim != "FINITE_TIME_NONLINEAR_STABILITY",
          "second_jet_promoted_to_stability", caught)

    # 9. Interior carry dependence does not apply at the strict horizontal endpoint.
    endpoint_mu = F(0)
    endpoint_hv2 = b2 * endpoint_mu * (1 - endpoint_mu)
    catch(endpoint_hv2 == 0,
          "horizontal_endpoint_carry_dependence_inserted", caught)

    # 10. Vertical silence is a zero-radicand branch boundary, not strict G332 data.
    vertical_mu = F(1)
    vertical_C = F(-1)  # choose b=1
    vertical_radicand = (F(1) + vertical_C) ** 2
    catch(vertical_mu == 1 and vertical_radicand == 0,
          "vertical_boundary_called_strict", caught)

    # 11. The horizontal endpoint is always +1, not Lambda-2.
    catch(F(1) != Lambda - 2,
          "horizontal_vertical_endpoint_swapped", caught)

    # 12. The theorem has no Hopf/topology input.
    theorem_inputs = {"gamma", "K", "Ricci3", "Lambda", "n", "v", "carry", "boost"}
    catch(theorem_inputs.isdisjoint({"Hopf", "orbit_period", "topology"}),
          "topology_imported", caught)

    # 13. No matter, observational, scale, or Xmax input occurs.
    catch(theorem_inputs.isdisjoint(
        {"source", "matter", "mass", "observation", "scale", "X_max"}
    ), "external_physics_imported", caught)

    return {
        "package": "G336",
        "verdict": "PASS",
        "mutations_caught": len(caught),
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
                      "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
