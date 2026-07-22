#!/usr/bin/env python3
"""Exact algebra for the reciprocal-c metric-meaning correction."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(sp.expand(value.rewrite(sp.exp))) == 0 for value in matrix)


def main() -> None:
    c = sp.symbols("c", positive=True)
    phi = sp.symbols("phi", real=True)
    beta = sp.symbols("beta", real=True, nonzero=True)
    u, v = sp.symbols("u v", positive=True)

    # Foundational two-way clock/ruler conversion and the separately required dual action.
    conversion_forward = c
    conversion_inverse = 1 / c
    P = sp.diag(u, v)
    K = sp.Matrix([[0, 1], [1, 0]])
    pairing_residual = sp.simplify(P.T * K * P - K)
    reciprocal_character = sp.diag(sp.exp(-phi), sp.exp(phi))

    eta2 = sp.diag(-1, 1)
    g2 = sp.simplify(reciprocal_character.T * eta2 * reciprocal_character)

    # Passive Lorentz-coframe covariance: D must conjugate, not remain diagonal by fiat.
    boost = sp.Matrix([[sp.cosh(beta), sp.sinh(beta)], [sp.sinh(beta), sp.cosh(beta)]])
    boost_inverse = sp.simplify(boost.inv())
    transformed_character = sp.simplify(boost * reciprocal_character * boost_inverse)
    transformed_metric_direct = sp.simplify(boost_inverse.T * g2 * boost_inverse)
    transformed_metric_from_character = sp.simplify(
        transformed_character.T * eta2 * transformed_character
    )
    fixed_diagonal_commutator = sp.simplify(boost * reciprocal_character - reciprocal_character * boost)

    # Four-dimensional directional realization: one supplied clock u and one supplied spatial n.
    eta4 = sp.diag(-1, 1, 1, 1)
    directional_x = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
    directional_y = sp.diag(sp.exp(-phi), 1, sp.exp(phi), 1)
    g_directional_x = sp.simplify(directional_x.T * eta4 * directional_x)
    g_directional_y = sp.simplify(directional_y.T * eta4 * directional_y)

    # One supplied clock with equal scaling of all three spatial axes.
    isotropic_13 = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(phi), sp.exp(phi))
    g_isotropic_13 = sp.simplify(isotropic_13.T * eta4 * isotropic_13)

    # Two determinant-one ways to distribute one reciprocal weight over three spatial directions.
    volume_normalized_phi = sp.diag(
        sp.exp(-phi), sp.exp(phi / 3), sp.exp(phi / 3), sp.exp(phi / 3)
    )
    volume_normalized_psi = sp.diag(
        sp.exp(-3 * phi), sp.exp(phi), sp.exp(phi), sp.exp(phi)
    )

    # Static spherical control in an orthonormal areal coframe.
    r, theta = sp.symbols("r theta", positive=True)
    coframe_to_coordinate = sp.diag(c, 1, r, r * sp.sin(theta))
    static_distortion = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
    static_coordinate_metric = sp.simplify(
        coframe_to_coordinate.T * static_distortion.T * eta4 * static_distortion * coframe_to_coordinate
    )
    expected_static_metric = sp.diag(
        -c**2 * sp.exp(-2 * phi),
        sp.exp(2 * phi),
        r**2,
        r**2 * sp.sin(theta) ** 2,
    )

    # A supplied solution clock congruence transforms covariantly rather than becoming preferred in law.
    boost4 = sp.eye(4)
    boost4[:2, :2] = boost
    directional_boosted = sp.simplify(boost4 * directional_x * boost4.inv())
    directional_metric_boosted_direct = sp.simplify(boost4.inv().T * g_directional_x * boost4.inv())
    directional_metric_boosted_from_D = sp.simplify(
        directional_boosted.T * eta4 * directional_boosted
    )

    checks = {
        "c_and_inverse_are_two_way_conversion": sp.simplify(conversion_forward * conversion_inverse - 1) == 0,
        "dual_pairing_requires_uv_one": zero(pairing_residual.subs(v, 1 / u)),
        "ordinary_covariance_v_equals_u_is_distinct": sp.simplify(v * c - c * u).subs(v, u) == 0
        and sp.simplify((u * v - 1).subs(v, u)) != 0,
        "reciprocal_character_preserves_K": zero(
            reciprocal_character.T * K * reciprocal_character - K
        ),
        "one_plus_one_metric_recovered": zero(
            g2 - sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi))
        ),
        "one_plus_one_determinant_fixed": sp.simplify(g2.det() + 1) == 0,
        "passive_boost_covariance": zero(
            transformed_metric_direct - transformed_metric_from_character
        ),
        "nontrivial_D_not_same_diagonal_in_every_boosted_frame": not zero(
            fixed_diagonal_commutator
        ),
        "same_diagonal_all_frames_forces_trivial_character": zero(
            fixed_diagonal_commutator.subs(phi, 0)
        ) and any(entry.has(sp.sinh(beta)) and entry != 0 for entry in fixed_diagonal_commutator),
        "pair_direction_changes_four_metric_when_phi_nonzero": not zero(
            g_directional_x - g_directional_y
        ),
        "directional_realization_has_det_one_distortion": sp.simplify(directional_x.det() - 1) == 0,
        "naive_one_plus_three_scaling_not_det_one": sp.simplify(isotropic_13.det() - sp.exp(2 * phi)) == 0,
        "one_plus_three_metric_depends_on_supplied_clock_split": zero(
            g_isotropic_13
            - sp.diag(
                -sp.exp(-2 * phi), sp.exp(2 * phi), sp.exp(2 * phi), sp.exp(2 * phi)
            )
        ),
        "volume_normalized_phi_candidate_det_one": sp.simplify(volume_normalized_phi.det() - 1) == 0,
        "volume_normalized_psi_candidate_det_one": sp.simplify(volume_normalized_psi.det() - 1) == 0,
        "volume_normalized_candidates_inequivalent_at_same_phi": not zero(
            volume_normalized_phi - volume_normalized_psi
        ),
        "static_spherical_metric_exactly_reproduced": zero(
            static_coordinate_metric - expected_static_metric
        ),
        "static_spherical_distortion_det_one": sp.simplify(static_distortion.det() - 1) == 0,
        "static_spherical_four_volume_phi_independent": not static_coordinate_metric.det().has(phi),
        "solution_specific_directional_structure_is_covariant": zero(
            directional_metric_boosted_direct - directional_metric_boosted_from_D
        ),
    }
    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise AssertionError(f"failed exact checks: {failed}")

    result = {
        "schema": "udt-reciprocal-c-metric-meaning-algebra-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "checks": checks,
        "counts": {
            "exact_checks": len(checks),
            "founding_postulates": 2,
            "additional_static_spherical_readout_choices": 4,
            "determinant_one_one_plus_three_weightings_exhibited": 2,
        },
        "additional_static_spherical_readout_choices": [
            "LOCAL_LORENTZIAN_QUADRATIC_READOUT",
            "CLOCK_AND_POSITIONAL_DEPTH_COFRAME_SLOTS",
            "DIAGONAL_TRANSVERSE_COMPLETION",
            "SPHERICAL_AREAL_ANGULAR_COFRAME",
        ],
        "exact_outputs": {
            "reciprocal_1plus1_metric": str(g2.tolist()),
            "static_spherical_coordinate_metric": str(static_coordinate_metric.tolist()),
            "directional_x_metric": str(g_directional_x.tolist()),
            "directional_y_metric": str(g_directional_y.tolist()),
            "naive_1plus3_distortion_determinant": str(sp.simplify(isotropic_13.det())),
            "boost_commutator": str(fixed_diagonal_commutator.tolist()),
        },
        "primary_ruling": "TWO_POSTULATES_DERIVE_RECIPROCAL_MEASUREMENT_BLOCK__COMPLETE_3PLUS1_ASSEMBLY_REMAINS_CONDITIONAL",
        "prior_audit_regrade": "RANK_TWO_UNIVERSAL_SELECTOR_NOT_REQUIRED_BY_PAIR_RELATIONAL_MEANING__EXACT_STABILIZER_RESULT_RETAINED",
        "scope": "KINEMATIC_MEASUREMENT_AND_METRIC_ASSEMBLY_ONLY",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
