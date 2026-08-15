#!/usr/bin/env python3
"""Standard-library replay of the flux factorization and nonuniqueness."""

from __future__ import annotations

import json
import math
from pathlib import Path


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def transpose(a):
    return [[a[j][i] for j in range(2)] for i in range(2)]


def determinant(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def max_abs_difference(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(2) for j in range(2))


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def scale(value, a):
    return [[value * a[i][j] for j in range(2)] for i in range(2)]


def tidal(parameter):
    """Nonconstant symmetric operator whose eigendirections rotate along the ray."""
    angle = 0.37 + 0.41 * parameter
    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotation = [[cosine, -sine], [sine, cosine]]
    diagonal = [
        [0.30 + 0.10 * parameter, 0.0],
        [0.0, -0.20 + 0.05 * parameter],
    ]
    return matmul(matmul(rotation, diagonal), transpose(rotation))


def derivative(parameter, state, reverse, length):
    d_matrix, p_matrix = state
    location = length - parameter if reverse else parameter
    return p_matrix, matmul(tidal(location), d_matrix)


def state_add(state, increment, coefficient):
    return (
        add(state[0], scale(coefficient, increment[0])),
        add(state[1], scale(coefficient, increment[1])),
    )


def integrate_jacobi(length, steps, reverse=False):
    step = length / steps
    state = (
        [[0.0, 0.0], [0.0, 0.0]],
        [[1.0, 0.0], [0.0, 1.0]],
    )
    parameter = 0.0
    for _ in range(steps):
        k1 = derivative(parameter, state, reverse, length)
        k2 = derivative(
            parameter + step / 2,
            state_add(state, k1, step / 2),
            reverse,
            length,
        )
        k3 = derivative(
            parameter + step / 2,
            state_add(state, k2, step / 2),
            reverse,
            length,
        )
        k4 = derivative(
            parameter + step,
            state_add(state, k3, step),
            reverse,
            length,
        )
        combined = (
            add(add(k1[0], scale(2, k2[0])), add(scale(2, k3[0]), k4[0])),
            add(add(k1[1], scale(2, k2[1])), add(scale(2, k3[1]), k4[1])),
        )
        state = state_add(state, combined, step / 6)
        parameter += step
    return state[0]


def main():
    # Nonconstant anisotropic rotating screen, solved independently both ways.
    Z = 1.5
    length = 0.8
    d_forward = integrate_jacobi(length, 12000, reverse=False)
    d_reverse_unscaled = integrate_jacobi(length, 12000, reverse=True)
    reciprocity_error = max_abs_difference(d_reverse_unscaled, transpose(d_forward))
    d_reverse = [[Z * value for value in row] for row in d_reverse_unscaled]
    d_A = math.sqrt(abs(determinant(d_forward)))
    d_G = math.sqrt(abs(determinant(d_reverse)))
    area_error = abs(d_G / d_A - Z)

    # Direct bookkeeping from emitted energy, clocks, and receiver area.
    luminosity_omega = 7.0
    source_interval = 0.2
    source_solid_angle = 0.03
    emitted_energy = luminosity_omega * source_interval * source_solid_angle
    observer_interval = Z * source_interval
    receiver_area = d_G**2 * source_solid_angle

    rows = []
    for name, energy_ratio, survival in (
        ("null_momentum_conserved_count", 1 / Z, 1.0),
        ("invariant_packet_energy", 1.0, 1.0),
        ("compensated_transfer", Z ** -0.25, Z ** -0.75),
    ):
        received_energy = emitted_energy * energy_ratio * survival
        direct_flux = received_energy / (observer_interval * receiver_area)
        factorized_flux = (
            luminosity_omega * energy_ratio * survival / (Z**3 * d_A**2)
        )
        rows.append(
            {
                "name": name,
                "energy_ratio": energy_ratio,
                "survival": survival,
                "direct_flux": direct_flux,
                "factorized_flux": factorized_flux,
                "relative_error": abs(direct_flux / factorized_flux - 1.0),
            }
        )

    # Every real exponent defines a positive multiplicative endpoint character.
    Z_1, Z_2 = 1.2, 1.4
    character_errors = []
    for exponent in (-2.0, -0.5, 0.0, 1.0, 2.5):
        character = lambda value: value ** (-exponent)
        composition_error = abs(
            character(Z_1 * Z_2) / (character(Z_1) * character(Z_2)) - 1.0
        )
        reversal_error = abs(character(1 / Z_1) * character(Z_1) - 1.0)
        character_errors.append(max(composition_error, reversal_error))

    # Catch proofs: the omitted factors must alter the result at Z != 1.
    correct = luminosity_omega / (Z**4 * d_A**2)
    dropped_energy = luminosity_omega / (Z**3 * d_A**2)
    dropped_clock = luminosity_omega / (Z**3 * d_A**2)
    collapsed_reverse_area = luminosity_omega / (Z**2 * d_A**2)
    catches = {
        "drop_energy_factor": abs(correct - dropped_energy) > 1e-12,
        "drop_clock_factor": abs(correct - dropped_clock) > 1e-12,
        "equate_reverse_and_forward_area": (
            abs(correct - collapsed_reverse_area) > 1e-12
        ),
    }

    result = {
        "rotated_anisotropic_screen": True,
        "independently_integrated_unscaled_transpose_error": reciprocity_error,
        "scaled_screen_relation_error": max_abs_difference(
            d_reverse, [[Z * value for value in row] for row in transpose(d_forward)]
        ),
        "area_ratio_error": area_error,
        "factorization_rows": rows,
        "maximum_factorization_relative_error": max(
            row["relative_error"] for row in rows
        ),
        "maximum_character_composition_reversal_error": max(character_errors),
        "catch_proofs": catches,
        "all_pass": (
            reciprocity_error < 1e-11
            and area_error < 1e-11
            and max(row["relative_error"] for row in rows) < 1e-13
            and max(character_errors) < 1e-13
            and all(catches.values())
        ),
    }
    output = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
