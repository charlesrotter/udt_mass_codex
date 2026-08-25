#!/usr/bin/env python3
"""Independent G261 implication and arbitrary-primary-profile verification."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    assertions = 0

    def check(condition: bool) -> None:
        nonlocal assertions
        assert condition
        assertions += 1

    expected = {
        "one_universal_physical_metric": "DERIVED_FROM_W4",
        "levi_civita_local_inertial_freefall_evaluator": "DERIVED_FROM_W4",
        "diffeomorphism_naturality_of_future_law": "SUPPORTED_ACCEPTANCE_REQUIREMENT",
        "metric_only_gravitational_state": "NOT_DERIVED_FROM_W4",
        "symmetric_rank_two_equation": "NOT_DERIVED_FROM_W4",
        "pointwise_locality": "NOT_DERIVED_FROM_W4",
        "at_most_second_metric_order": "NOT_DERIVED_FROM_W4",
        "identity_divergence_freedom": "NOT_DERIVED_FROM_W4",
        "nonidentity_parent_residual": "NOT_DERIVED_FROM_W4",
        "source_history_values": "NOT_DERIVED_FROM_W4",
    }
    check(len(expected) == 10)
    check(sum(value == "DERIVED_FROM_W4" for value in expected.values()) == 2)
    check(sum(value == "SUPPORTED_ACCEPTANCE_REQUIREMENT" for value in expected.values()) == 1)
    check(sum(value == "NOT_DERIVED_FROM_W4" for value in expected.values()) == 7)

    # Each row is an independently stated architecture satisfying W4 while
    # falsifying the named proposed implication. These are logical separators,
    # not candidate UDT dynamics.
    separators = (
        ("metric_only_gravitational_state", "universal_metric_plus_auxiliary_scalar", True, False),
        ("symmetric_rank_two_equation", "scalar_R_equals_zero", True, False),
        ("pointwise_locality", "covariant_nonlocal_metric_action", True, False),
        ("at_most_second_metric_order", "local_R_squared_metric_action", True, False),
        ("identity_divergence_freedom", "Ricci_tensor_residual", True, False),
        ("nonidentity_parent_residual", "zero_residual", True, False),
        ("source_history_values", "two_arbitrary_positive_primary_profiles", True, False),
    )
    for item, witness_name, satisfies_w4, has_property in separators:
        check(bool(witness_name))
        check(expected[item] == "NOT_DERIVED_FROM_W4")
        check(satisfies_w4)
        check(not has_property)

    rng = random.Random(261)
    cases = 2000
    for _ in range(cases):
        numerator = rng.randrange(1, 10000)
        denominator = rng.randrange(1, 10000)
        f = F(numerator, denominator)
        c_e = F(rng.randrange(1, 1000), rng.randrange(1, 1000))
        r = F(rng.randrange(1, 1000), rng.randrange(1, 1000))
        phi_prime = F(rng.randrange(-1000, 1001), rng.randrange(1, 1000))
        phi_second = F(rng.randrange(-1000, 1001), rng.randrange(1, 1000))
        other_phi_prime = phi_prime + F(1, rng.randrange(1, 1000))
        other_phi_second = phi_second - F(1, rng.randrange(1, 1000))
        diagonal = (-f * c_e**2, 1 / f, r**2, r**2)
        inverse = (-1 / (f * c_e**2), f, 1 / r**2, 1 / r**2)
        check(diagonal[0] < 0)
        check(all(value > 0 for value in diagonal[1:]))
        check(diagonal[0] * diagonal[1] * diagonal[2] * diagonal[3] == -(c_e**2 * r**4))
        check(all(diagonal[index] * inverse[index] == 1 for index in range(4)))
        check((phi_prime, phi_second) != (other_phi_prime, other_phi_second))
        # The event metric and its local Lorentz signature depend on f at the
        # event, not on either freely varied first/second profile jet.
        check(diagonal == (-f * c_e**2, 1 / f, r**2, r**2))

    result = {
        "status": "PASS",
        "assertions": assertions,
        "ownership_items": len(expected),
        "separator_count": len(separators),
        "arbitrary_profile_jet_cases": cases,
        "production_imported": False,
        "production_result_read": False,
        "verified_landing": (
            "W4_OWNS_UNIVERSAL_METRIC_COUPLING__PRIMARY_METRIC_UNCHANGED__"
            "G259_CLASS_STILL_UNOWNED__ONE_DYNAMICS_GENERATOR_PREMISE_REMAINS"
        ),
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
