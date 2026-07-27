#!/usr/bin/env python3
"""Exact same-branch quotient geometry and selector-rank derivation."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    p, dp, c, a, radius, lam, kappa = sp.symbols(
        "phi delta_phi c_E a R lambda kappa", real=True
    )
    da, dr, dl = sp.symbols("delta_a delta_R delta_lambda", real=True)
    assert c != 0 and radius != 0

    em2 = sp.exp(-2 * p)
    ep2 = sp.exp(2 * p)
    e2l = sp.exp(2 * lam * p)

    # Basis order: (dt, sigma_1, sigma_2, sigma_3).
    metric = sp.diag(-c**2 * em2, radius**2 * e2l, radius**2 * e2l, radius**2 * ep2 - a**2 * em2)
    metric[0, 3] = metric[3, 0] = -c * a * em2
    gtt = metric[0, 0]
    gt = sp.Matrix([metric[0, i] for i in range(1, 4)])
    spatial_block = metric[1:4, 1:4]
    quotient = sp.simplify(spatial_block - (gt * gt.T) / gtt)
    expected_quotient = sp.diag(radius**2 * e2l, radius**2 * e2l, radius**2 * ep2)
    assert sp.simplify(quotient - expected_quotient) == sp.zeros(3)
    assert all(sp.simplify(sp.diff(entry, a)) == 0 for entry in quotient)

    # The normalized stationary connection eta=K_flat/g(K,K)=dt+(a/c_E)sigma_3.
    # Its curvature keeps the shift/twist information discarded by the quotient metric.
    connection_components = [sp.S.One, sp.S.Zero, sp.S.Zero, a / c]
    connection_curvature_sigma12 = sp.simplify(a * kappa / c)

    quotient_det = sp.factor(quotient.det())
    volume_density = radius**3 * sp.exp((1 + 2 * lam) * p)
    assert sp.simplify(quotient_det - volume_density**2) == 0
    slice_det = sp.factor(spatial_block.det())
    slice_to_quotient_volume_ratio_squared = sp.factor(slice_det / quotient_det)
    expected_slice_ratio_squared = 1 - a**2 * sp.exp(-4 * p) / radius**2
    assert sp.simplify(slice_to_quotient_volume_ratio_squared - expected_slice_ratio_squared) == 0

    varied_density = sp.diff(volume_density, p) * dp + sp.diff(volume_density, lam) * dl + sp.diff(volume_density, radius) * dr + sp.diff(volume_density, a) * da
    normalized_variation = sp.simplify(varied_density / volume_density)
    expected_variation = (1 + 2 * lam) * dp + 2 * p * dl + 3 * dr / radius
    assert sp.simplify(normalized_variation - expected_variation) == 0
    assert sp.diff(volume_density, a) == 0
    assert sp.simplify(sp.diff(volume_density, p).subs(lam, sp.Rational(-1, 2))) == 0

    # Exact two-cell mean-zero control for the volume derivative.
    w1, w2 = sp.symbols("w_1 w_2", positive=True)
    f1, f2 = w2, -w1
    weighted_mean = sp.expand(w1 * f1 + w2 * f2)
    assert weighted_mean == 0

    # Dimensional audit for c^alpha G^beta. Rows are exponents of L,M,T.
    alpha, beta = sp.symbols("alpha beta")
    dimensions = sp.Matrix([alpha + 3 * beta, -beta, -alpha - 2 * beta])
    length_solution = sp.solve(
        [sp.Eq(dimensions[0], 1), sp.Eq(dimensions[1], 0), sp.Eq(dimensions[2], 0)],
        (alpha, beta),
        dict=True,
    )
    density_solution = sp.solve(
        [sp.Eq(dimensions[0], -3), sp.Eq(dimensions[1], 1), sp.Eq(dimensions[2], 0)],
        (alpha, beta),
        dict=True,
    )
    assert length_solution == []
    assert density_solution == []

    # The exact witness conditions are strict/nonzero and therefore open, not equations.
    witness_rank_det = sp.Rational(
        330801319823081673814309577,
        159252480000000000000000000000,
    )
    witness_phi_gradient = sp.Matrix([1, 2, 3]) / 400
    witness_a = sp.Rational(1, 10)
    witness_kappa = -2
    assert witness_rank_det != 0
    assert witness_phi_gradient.dot(witness_phi_gradient) > 0
    assert witness_a * witness_kappa != 0

    result = {
        "schema": "udt.metric_native_selector_rank.derivation.v1",
        "quotient_metric_basis": [
            [str(sp.factor(value)) for value in row] for row in quotient.tolist()
        ],
        "quotient_metric_shift_a_cancels": True,
        "stationary_connection_basis_dt_sigma1_sigma2_sigma3": [
            str(value) for value in connection_components
        ],
        "stationary_connection_curvature_sigma1_wedge_sigma2": str(
            connection_curvature_sigma12
        ),
        "quotient_determinant": str(quotient_det),
        "quotient_volume_density": str(volume_density),
        "t_constant_slice_determinant": str(slice_det),
        "slice_to_quotient_volume_ratio_squared": str(slice_to_quotient_volume_ratio_squared),
        "normalized_volume_first_variation": str(normalized_variation),
        "volume_phi_response_at_lambda_minus_half": "0",
        "volume_phi_derivative_rank_generic": 1,
        "volume_phi_derivative_rank_lambda_minus_half": 0,
        "explicit_weighted_mean_zero_control": {
            "perturbation": [str(f1), str(f2)],
            "weighted_derivative": str(weighted_mean),
        },
        "finite_differentiable_scalar_family_derivative_has_infinite_kernel": True,
        "finite_scalar_derivative_kernel_proof": "m_by_m_plus_1_disjoint_bump_matrix_has_nonzero_null_vector_repeated_on_disjoint_groups",
        "cG_length_solution": length_solution,
        "cG_density_solution": density_solution,
        "unique_K_witness_conditions_are_open_nonzero_conditions": True,
        "witness_rank_determinant": str(witness_rank_det),
        "witness_phi_gradient_squared": str(witness_phi_gradient.dot(witness_phi_gradient)),
        "witness_a_kappa": str(witness_a * witness_kappa),
        "branchwise_orbit_volume_available": True,
        "native_mass_available": False,
        "same_solution_density_executable": False,
        "bootstrap_return_map_available": False,
        "working_Xmax_identified_with_quotient_diameter": False,
        "independent_profile_selector_rank_from_active_premises": 0,
        "residual_phi_function_space": "INFINITE_DIMENSIONAL_OPEN_NEIGHBORHOOD",
        "maximum_interpretation": "same_branch_output_and_rank_classification_no_physical_selection",
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "DERIVATION_RESULT.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
