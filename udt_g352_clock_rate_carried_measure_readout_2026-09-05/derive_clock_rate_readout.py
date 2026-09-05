#!/usr/bin/env python3
"""Exact regression witnesses for the bounded G352 clock-rate readout."""

from fractions import Fraction
import itertools
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "DERIVATION_RESULT.json"
LANDING = (
    "OWNER_PROVISIONAL_CLOCK_RATE_READOUT"
    "__CHOSE_CONTINUOUS_TOTAL_PHASE_INTENSITY_AND_PHASE_INDEPENDENT_LABEL_PRODUCT"
    "__P_EQUALS_ONE_AND_Q_EQUALS_MINUS_ONE_ONLY_FOR_THIS_READOUT"
    "__T_CLOCK_EQUALS_R_A_INVERSE"
    "__PHASE_NORMALIZATION_OBSERVER_COVARIANCE_SEWING_AND_REVERSAL_CLOSE"
    "__INTEGRABLE_RATE_MEASURE_SURVIVES_CAUSTIC_RANK_LOSS_WHILE_DENSITY_NEED_NOT"
    "__LITERAL_ATOMIC_CROSSING_COUNT_P_ZERO_DENSITY_AND_OTHER_READOUT_WEIGHTS_REMAIN_DISTINCT"
    "__NO_LIGHT_ENERGY_DETECTOR_DISTANCE_HISTORY_SCALE_XMAX_MATTER_MASS_OR_CANON"
)


def transfer(omega_i, omega_j, jac_i, jac_j):
    """G352 clock-rate transfer from cut i to cut j."""
    frequency_ratio = omega_j / omega_i
    area_ratio = jac_j / jac_i
    return frequency_ratio / area_ratio


def gamma(omega, jac, label_density, phase_spacing):
    """Continuous total-phase intensity per proper time per metric sheet area."""
    return omega * label_density / (phase_spacing * jac)


def main():
    checks = 0

    def exact(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(label)

    case_count = 2400
    for case in range(case_count):
        base = case + 1
        # Every base state is distinct. These exact states are regression
        # witnesses, not independent mathematical proofs.
        omegas = [Fraction(11 * base + 2 * i + 1, 5 + i) for i in range(3)]
        jacobians = [Fraction(13 * base + 3 * i + 2, 7 + i) for i in range(3)]
        label_density = Fraction(17 * base + 3, 11)
        phase_spacing = Fraction(19 * base + 5, 13)
        gammas = [
            gamma(omegas[i], jacobians[i], label_density, phase_spacing)
            for i in range(3)
        ]

        # For k_a=grad_a(Theta) in the registered future-null convention,
        # dTheta/dtau=-omega; the continuous total-phase intensity uses its
        # magnitude. A literal discrete crossing count instead has an atomic
        # proper-time measure and is not asserted to have this smooth rate.
        for omega in omegas:
            phase_derivative = -omega
            exact(abs(phase_derivative) / phase_spacing == omega / phase_spacing,
                  "repaired positive continuous phase intensity")
            exact(phase_derivative / phase_spacing < 0,
                  "signed phase form is not a nonnegative counting measure")

        for i in range(3):
            exact(transfer(omegas[i], omegas[i], jacobians[i], jacobians[i]) == 1,
                  "identity transfer")
            exact(
                gamma(
                    5 * omegas[i],
                    jacobians[i],
                    label_density,
                    5 * phase_spacing,
                )
                == gammas[i],
                "common phase reparameterization",
            )

        for i, j in itertools.permutations(range(3), 2):
            t_ji = transfer(omegas[i], omegas[j], jacobians[i], jacobians[j])
            exact(gammas[j] == t_ji * gammas[i], "clock-rate transfer")
            t_ij = transfer(omegas[j], omegas[i], jacobians[j], jacobians[i])
            exact(t_ij * t_ji == 1, "algebraic reversal")

            d_i = Fraction(23 * base + 2 * i + 1, 17 + i)
            d_j = Fraction(29 * base + 3 * j + 2, 19 + j)
            transformed = transfer(
                d_i * omegas[i],
                d_j * omegas[j],
                jacobians[i],
                jacobians[j],
            )
            exact(transformed == (d_j / d_i) * t_ji, "observer weight one")
            exact(
                gamma(d_j * omegas[j], jacobians[j], label_density, phase_spacing)
                == d_j * gammas[j],
                "endpoint rate covariance",
            )

        for i, j, k in itertools.permutations(range(3), 3):
            t_ki = transfer(omegas[i], omegas[k], jacobians[i], jacobians[k])
            t_kj = transfer(omegas[j], omegas[k], jacobians[j], jacobians[k])
            t_ji = transfer(omegas[i], omegas[j], jacobians[i], jacobians[j])
            exact(t_ki == t_kj * t_ji, "three-cut sewing")

        exact(gamma(omegas[0], jacobians[0], Fraction(0), phase_spacing) == 0,
              "zero measure remains zero")

    # A literal fixed-level count is a step function. Between two neighboring
    # phase levels it can have zero atomic crossings while total phase
    # variation is nonzero, so the two objects must remain distinct.
    atomic_crossings_between_levels = 0
    continuous_phase_variation = Fraction(1, 2)
    exact(atomic_crossings_between_levels == 0, "atomic interval witness")
    exact(continuous_phase_variation > 0, "continuous interval witness")
    exact(atomic_crossings_between_levels != continuous_phase_variation,
          "atomic count differs from continuous phase intensity")

    # The repaired product measure uses |dTheta| and is nonnegative. Its
    # phase-independent tensor factorization with the same mu on every slice
    # is supplied/CHOSEN for this bounded realization, not derived from G351.
    phase_variation = Fraction(7, 5)
    supplied_label_mass = Fraction(11, 13)
    product_mass = phase_variation * supplied_label_mass
    exact(product_mass >= 0, "nonnegative total-variation product measure")

    # In logarithmic character coordinates the readout residual is
    # (a-1) log R + (q+1) log A.  Independent coordinate directions fix
    # a=1 and q=-1 inside G350's declared full positive abstract domain.
    coefficient_grid = [Fraction(n, 2) for n in range(-5, 6)]
    selected_pairs = []
    for a in coefficient_grid:
        for q in coefficient_grid:
            frequency_residual = a - 1
            area_residual = q + 1
            matches = frequency_residual == 0 and area_residual == 0
            exact(matches == (a == 1 and q == -1), "character coefficient witness")
            if matches:
                selected_pairs.append((a, q))
    exact(selected_pairs == [(Fraction(1), Fraction(-1))], "unique bounded weights")

    # Rank-loss sequence: the integrated clock-rate measure stays finite while
    # the ordinary area density grows without bound as J tends to zero.
    omega = Fraction(7, 3)
    phase_spacing = Fraction(5, 2)
    label_mass = Fraction(11, 7)
    previous_density = None
    caustic_steps = 160
    for n in range(1, caustic_steps + 1):
        jac = Fraction(1, n * n)
        density = gamma(omega, jac, label_mass, phase_spacing)
        integrated_rate = density * jac
        exact(integrated_rate == omega * label_mass / phase_spacing,
              "finite integrated rate measure")
        if previous_density is not None:
            exact(density > previous_density, "unbounded density sequence")
        previous_density = density

    # Mathematical preimage accounting on a many-to-one endpoint map.
    weights = [Fraction(2, 5), Fraction(3, 7), Fraction(5, 11)]
    frequencies = [Fraction(7, 4), Fraction(9, 5), Fraction(11, 6)]
    spacing = Fraction(13, 8)
    contributions = [frequencies[i] * weights[i] / spacing for i in range(3)]
    endpoint_by_label = {"lambda_0": "y", "lambda_1": "y", "lambda_2": "z"}
    contribution_by_label = {
        f"lambda_{i}": contributions[i] for i in range(len(contributions))
    }
    pushforward = {}
    for label, endpoint in endpoint_by_label.items():
        pushforward[endpoint] = pushforward.get(endpoint, Fraction(0)) + contribution_by_label[label]
    exact(pushforward["y"] == contributions[0] + contributions[1],
          "pushforward sums distinct preimages at y")
    exact(pushforward["z"] == contributions[2],
          "pushforward retains singleton preimage at z")
    exact(all(value > 0 for value in contributions), "finite positive rate weights")

    result = {
        "case_count": case_count,
        "distinct_base_states": case_count,
        "caustic_steps": caustic_steps,
        "checks_passed": checks,
        "checks_total": checks,
        "exact_arithmetic": True,
        "frequency_weight_for_clock_rate": 1,
        "area_weight_for_regular_density": -1,
        "phase_rescaling_cancels": True,
        "continuous_phase_intensity": True,
        "literal_discrete_instantaneous_rate_claimed": False,
        "product_measure_nonnegative": True,
        "phase_label_factorization_explicit_and_supplied": True,
        "phase_label_factorization_derived_from_g351": False,
        "observer_covariance_weight": 1,
        "universal_p_selected": False,
        "observer_neutral_p0_retained": True,
        "source_or_population_generated": False,
        "light_or_energy_identified": False,
        "landing": LANDING,
    }

    if os.environ.get("UDT_NO_WRITE") != "1":
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
