#!/usr/bin/env python3
"""Independent direct-matrix verification and hostile mutations.

This implementation does not import the production census.
"""

import json
import math

import numpy as np
from scipy.linalg import expm


def norm(matrix):
    return float(np.linalg.norm(matrix, ord=np.inf))


def generator(a, b):
    return np.array(
        [
            [-1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, a, -b],
            [0.0, 0.0, b, a],
        ]
    )


def screen_lift(screen):
    result = np.eye(4)
    result[2:, 2:] = screen
    return result


def main():
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    k = np.array([[0.0, 1.0], [1.0, 0.0]])
    pairing = np.eye(4)
    pairing[:2, :2] = k
    eps = np.array([[0.0, -1.0], [1.0, 0.0]])
    reflection = np.diag([1.0, -1.0])
    rotation = expm(0.371 * eps)

    h = generator(0.23, -0.41)
    group_residuals = []
    for x, y in [(0.17, -0.09), (-0.31, 0.22), (0.41, 0.18)]:
        group_residuals.append(norm(expm(y * h) @ expm(x * h) - expm((x + y) * h)))
        group_residuals.append(norm(np.linalg.inv(expm(x * h)) - expm(-x * h)))

    # O2 covariance: b is killed by reflection. SO2 covariance retains it.
    so2_covariance_residual = norm(screen_lift(rotation) @ h - h @ screen_lift(rotation))
    o2_covariance_residual = norm(
        screen_lift(reflection) @ h - h @ screen_lift(reflection)
    )

    h_scale = generator(0.23, 0.0)
    full_pairing_residual_scale = norm(h_scale.T @ pairing + pairing @ h_scale)
    h_rotation = generator(0.0, -0.41)
    full_pairing_residual_rotation = norm(
        h_rotation.T @ pairing + pairing @ h_rotation
    )

    x_fixed = np.eye(4)
    x_fixed[:2, :2] = k
    x_reflected = x_fixed.copy()
    x_reflected[2:, 2:] = reflection
    fixed_exchange_residual = norm(x_fixed @ h @ x_fixed + h)
    reflected_exchange_residual = norm(x_reflected @ h @ x_reflected + h)
    reflected_rotation_exchange_residual = norm(
        x_reflected @ h_rotation @ x_reflected + h_rotation
    )

    # Active and passive witnesses.
    j = np.array([[5.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]])
    g0 = np.diag([0.5, 2.0, 1.0, 1.0])
    ga = np.diag([0.5, 2.0, 2.0, 2.0])
    h0 = j.T @ g0.T @ eta @ g0 @ j
    ha = j.T @ ga.T @ eta @ ga @ j
    active_difference = norm(ha - h0)

    screen_quarter = np.eye(4)
    screen_quarter[2:, 2:] = eps
    h_rotation_only = j.T @ (screen_quarter @ g0).T @ eta @ (screen_quarter @ g0) @ j

    p = np.array(
        [[1.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 2.0, 1.0], [0.0, 0.0, 0.0, 1.0]]
    )
    v = j.copy()
    v_passive = np.linalg.inv(p) @ (p @ j)
    v_broken = np.linalg.inv(p) @ j

    # Hostile mutations.
    h_offblock = h.copy()
    h_offblock[2, 0] = 0.7
    offblock_covariance_break = norm(
        screen_lift(rotation) @ h_offblock - h_offblock @ screen_lift(rotation)
    )
    h_anisotropic = h.copy()
    h_anisotropic[2:, 2:] = np.diag([0.5, -0.5])
    anisotropic_covariance_break = norm(
        screen_lift(rotation) @ h_anisotropic - h_anisotropic @ screen_lift(rotation)
    )

    # Regression for the exact reviewer-found defect.  For C in the lower-left
    # block, finite covariance differentiates to eps@C=0, not
    # (eps-I)@C=0.  Check the finite-difference derivative against the correct
    # infinitesimal equation and prove the old mutant is a different map.
    c_probe = np.array([[0.7, -0.2], [0.1, 0.4]])
    a_probe = np.array([[0.3, -0.6], [0.2, 0.5]])
    tiny = 1.0e-7
    r_tiny = expm(tiny * eps)
    c_finite_derivative = (r_tiny @ c_probe - c_probe) / tiny
    a_finite_derivative = (a_probe @ expm(-tiny * eps) - a_probe) / tiny
    c_correct_derivative_residual = norm(c_finite_derivative - eps @ c_probe)
    a_correct_derivative_residual = norm(a_finite_derivative + a_probe @ eps)
    c_wrong_mutant_difference = norm((eps @ c_probe - c_probe) - eps @ c_probe)
    a_wrong_mutant_difference = norm((a_probe @ eps - a_probe) - a_probe @ eps)

    # General passive carry, with neither E nor J specialized to an identity.
    e_general = np.array(
        [[2.0, 1.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0],
         [1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 2.0]]
    )
    general_passive_residual = norm(e_general @ np.linalg.inv(p) @ (p @ j) - e_general @ j)

    tolerance = 2.0e-12
    result = {
        "max_group_residual": max(group_residuals),
        "so2_covariance_residual": so2_covariance_residual,
        "o2_reflection_rejects_b_residual": o2_covariance_residual,
        "screen_scale_breaks_full_pairing_residual": full_pairing_residual_scale,
        "screen_rotation_preserves_full_pairing_residual": full_pairing_residual_rotation,
        "fixed_screen_exchange_rejects_a_and_b_residual": fixed_exchange_residual,
        "reflected_screen_exchange_rejects_a_residual": reflected_exchange_residual,
        "reflected_screen_exchange_accepts_b_residual": reflected_rotation_exchange_residual,
        "active_screen_scale_changes_h_norm": active_difference,
        "screen_rotation_changes_h_norm": norm(h_rotation_only - h0),
        "correct_passive_carry_residual": norm(v_passive - v),
        "omitted_J_carry_mutation_residual": norm(v_broken - v),
        "offblock_covariance_mutation_residual": offblock_covariance_break,
        "anisotropic_screen_mutation_residual": anisotropic_covariance_break,
        "correct_C_infinitesimal_from_finite_residual": c_correct_derivative_residual,
        "correct_A_infinitesimal_from_finite_residual": a_correct_derivative_residual,
        "wrong_C_eigenvalue_one_mutant_difference": c_wrong_mutant_difference,
        "wrong_A_eigenvalue_one_mutant_difference": a_wrong_mutant_difference,
        "general_E_passive_carry_residual": general_passive_residual,
    }
    result["all_checks_pass"] = bool(
        result["max_group_residual"] < tolerance
        and result["so2_covariance_residual"] < tolerance
        and result["o2_reflection_rejects_b_residual"] > 1.0e-3
        and result["screen_scale_breaks_full_pairing_residual"] > 1.0e-3
        and result["screen_rotation_preserves_full_pairing_residual"] < tolerance
        and result["fixed_screen_exchange_rejects_a_and_b_residual"] > 1.0e-3
        and result["reflected_screen_exchange_rejects_a_residual"] > 1.0e-3
        and result["reflected_screen_exchange_accepts_b_residual"] < tolerance
        and result["active_screen_scale_changes_h_norm"] > 1.0e-3
        and result["screen_rotation_changes_h_norm"] < tolerance
        and result["correct_passive_carry_residual"] < tolerance
        and result["omitted_J_carry_mutation_residual"] > 1.0e-3
        and result["offblock_covariance_mutation_residual"] > 1.0e-3
        and result["anisotropic_screen_mutation_residual"] > 1.0e-3
        and result["correct_C_infinitesimal_from_finite_residual"] < 2.0e-7
        and result["correct_A_infinitesimal_from_finite_residual"] < 2.0e-7
        and result["wrong_C_eigenvalue_one_mutant_difference"] > 1.0e-3
        and result["wrong_A_eigenvalue_one_mutant_difference"] > 1.0e-3
        and result["general_E_passive_carry_residual"] < tolerance
        and math.isfinite(result["active_screen_scale_changes_h_norm"])
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
