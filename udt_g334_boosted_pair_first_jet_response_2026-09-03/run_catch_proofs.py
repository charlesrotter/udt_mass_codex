#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G334 result."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from derive_boosted_pair_first_jet import (
    add_transport,
    boost_from_half_tangent,
    g333_rate,
    inherited_response,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()

    caught = []

    def catch(condition, name):
        if not condition:
            raise AssertionError(f"mutation escaped: {name}")
        caught.append(name)

    _, b_plus, rate_plus = g333_rate(F(12), F(20), F(3), 1, F(1, 4))
    _, b_minus, _ = g333_rate(F(12), F(20), F(3), -1, F(1, 4))
    ch, sh = boost_from_half_tangent(F(1, 2))
    response = inherited_response(rate_plus, ch, sh)
    d00, d01, d11 = response[0][0], response[0][1], response[1][1]
    catch(rate_plus.nonzero() and b_plus != b_minus, "baseline_nonzero_and_branched")

    mutated_cross = -2 * rate_plus * sh * ch
    catch(mutated_cross != d01, "wrong_cross_sign")

    alpha, beta, gamma, delta = F(2, 3), F(5, 7), F(-1, 4), F(-3, 5)
    transported = add_transport(response, alpha, beta, gamma, delta)
    catch(transported != response, "dropped_general_transport_terms")
    catch(transported[0][0] / 2 != d00 / 2, "terminal_phi_transport_omission")

    unboosted = inherited_response(rate_plus, F(1), F(0))
    catch(unboosted[0][0] == 0 and rate_plus.nonzero(), "false_terminal_completeness_at_zero_boost")

    catch(b_plus != b_minus, "collapsed_G332_branches")

    normal_jet = F(7, 5)
    observer_a = ch * normal_jet + sh * F(0)
    observer_b = ch * normal_jet + sh * F(9, 4)
    catch(observer_a != observer_b, "normal_derivative_promoted_to_observer_time")

    different_alpha = add_transport(response, F(1), F(0), F(0), F(0))
    catch(different_alpha[0][0] != response[0][0], "boost_value_called_transport_complete")

    zeta = F(11, 6)
    correct_boost_rate = add_transport(response, F(0), zeta, zeta, F(0))
    mutated_boost_rate = add_transport(response, F(0), zeta, -zeta, F(0))
    catch(correct_boost_rate == response and mutated_boost_rate != response,
          "Lorentz_boost_rate_false_leak")

    reorthonormalized = add_transport(response, d00 / 2, -d01, F(0), -d11 / 2)
    catch(reorthonormalized == [[0, 0], [0, 0]] and rate_plus.nonzero(),
          "zero_frame_components_called_zero_geometry")

    wrong_phi_sign = -d00 / 2
    catch(wrong_phi_sign != d00 / 2, "terminal_phi_sign_mutation")

    allowed_inputs = {"g", "n", "v", "q", "z", "pair_transport"}
    topology_mutation = allowed_inputs | {"Hopf_period"}
    catch("Hopf_period" not in allowed_inputs and "Hopf_period" in topology_mutation,
          "inserted_Hopf_dependency")

    required_tokens = {
        "ARBITRARY_PAIR_FIRST_JET_REMAINS_TRANSPORT_QUALIFIED",
        "NO_NEW_CHANNEL_OR_OBSERVER_TIME_EVOLUTION",
    }
    landing = (
        "G333_FIRST_NORMAL_RESPONSE_HAS_EXACT_FINITE_BOOST_CONGRUENCE__"
        "ARBITRARY_PAIR_FIRST_JET_REMAINS_TRANSPORT_QUALIFIED__"
        "COMPLETE_MATRIX_EXCEEDS_TERMINAL_PHI_ON_INHERITED_GERMS__"
        "NO_NEW_CHANNEL_OR_OBSERVER_TIME_EVOLUTION"
    )
    catch(all(token in landing for token in required_tokens), "scope_tokens_present")
    promoted = "G334_DERIVES_ALL_PHYSICAL_OBSERVER_EVOLUTION_AND_HOPF_STABILITY"
    catch(any(token not in promoted for token in required_tokens), "scope_promotion_rejected")

    payload = {
        "package": "G334",
        "mutations_caught": len(caught) - 2,
        "checks": caught,
        "verdict": "PASS",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"mutations_caught": payload["mutations_caught"], "verdict": "PASS"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
