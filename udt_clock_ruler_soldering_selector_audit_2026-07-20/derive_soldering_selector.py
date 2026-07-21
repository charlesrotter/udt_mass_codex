#!/usr/bin/env python3
"""Exact algebra for the UDT metric-native soldering selector audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    require(name, good, checks)


def scalar_curvature(metric: sp.Matrix, coordinates: list[sp.Symbol]) -> sp.Expr:
    size = len(coordinates)
    inverse = sp.simplify(metric.inv())
    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        / 2
                        for d in range(size)
                    )
                )
                for c in range(size)
            ]
            for b in range(size)
        ]
        for a in range(size)
    ]
    ricci = sp.zeros(size)
    for a in range(size):
        for b in range(size):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(christoffel[c][a][b], coordinates[c])
                    - sp.diff(christoffel[c][a][c], coordinates[b])
                    + sum(
                        christoffel[c][c][d] * christoffel[d][a][b]
                        - christoffel[c][b][d] * christoffel[d][a][c]
                        for d in range(size)
                    )
                    for c in range(size)
                )
            )
    return sp.factor(
        sum(inverse[a, b] * ricci[a, b] for a in range(size) for b in range(size))
    )


def main() -> None:
    checks: dict[str, str] = {}
    alpha, b = sp.symbols("alpha b", positive=True)
    k = sp.symbols("k", real=True, positive=True)
    phi, chi = sp.symbols("phi chi", real=True)
    u, v = sp.symbols("u v", real=True)

    # Parameterize the spatial-reflection sign branch of the mixed family by
    # B=-k*alpha*b, k>1. The inequalities are recorded separately in the result.
    H = sp.Matrix([[alpha, -k * alpha * b], [-k * alpha * b, alpha * b**2]])
    L = sp.diag(-1, 1)
    F = sp.Matrix([[0, b], [1 / b, 0]])
    eta = sp.diag(-1, 1)
    v_plus = sp.Matrix([b, 1])
    v_minus = sp.Matrix([-b, 1])

    require_zero("seal_involution", F**2 - sp.eye(2), checks)
    require_zero("seal_inverts_reciprocal_generator", F * L * F + L, checks)
    require_zero("mixed_metric_seal_isometry", F.T * H * F - H, checks)
    require_zero("seal_plus_eigenvector", F * v_plus - v_plus, checks)
    require_zero("seal_minus_eigenvector", F * v_minus + v_minus, checks)

    norm_plus = sp.factor((v_plus.T * H * v_plus)[0])
    norm_minus = sp.factor((v_minus.T * H * v_minus)[0])
    cross_norm = sp.factor((v_plus.T * H * v_minus)[0])
    require_zero("seal_plus_norm", norm_plus - 2 * alpha * b**2 * (1 - k), checks)
    require_zero("seal_minus_norm", norm_minus - 2 * alpha * b**2 * (1 + k), checks)
    require_zero("seal_eigenlines_metric_orthogonal", cross_norm, checks)
    require("spatial_reflection_branch_plus_is_timelike_witness", norm_plus.subs(k, 2) < 0, checks)
    require("spatial_reflection_branch_minus_is_spacelike_witness", norm_minus.subs(k, 2) > 0, checks)

    n_time = b * sp.sqrt(2 * alpha * (k - 1))
    n_radial = b * sp.sqrt(2 * alpha * (k + 1))
    S0 = sp.Matrix.hstack(v_plus / n_time, v_minus / n_radial)
    require_zero("seal_selected_base_orthonormalizer", S0.T * H * S0 - eta, checks)
    F0 = sp.simplify(S0.inv() * F * S0)
    T0 = sp.simplify(S0.inv() * (-F) * S0)
    require_zero("seal_is_standard_spatial_reflection", F0 - sp.diag(1, -1), checks)
    require_zero("minus_seal_is_standard_temporal_reflection", T0 - sp.diag(-1, 1), checks)

    reciprocal_in_seal_frame = sp.simplify(S0.inv() * L * S0)
    ratio = sp.sqrt((k - 1) / (k + 1))
    expected_reciprocal = sp.Matrix([[0, ratio], [1 / ratio, 0]])
    require_zero(
        "reciprocal_generator_in_seal_frame",
        reciprocal_in_seal_frame - expected_reciprocal,
        checks,
    )
    require_zero("reciprocal_generator_remains_involution", reciprocal_in_seal_frame**2 - sp.eye(2), checks)

    boost = sp.Matrix([[sp.cosh(chi), sp.sinh(chi)], [sp.sinh(chi), sp.cosh(chi)]])
    require_zero("orthonormalizer_lorentz_family", boost.T * eta * boost - eta, checks)
    require_zero("boosted_base_frame_still_orthonormal", (S0 * boost).T * H * (S0 * boost) - eta, checks)
    seal_standard = sp.diag(1, -1)
    seal_boost_commutator = sp.simplify(seal_standard * boost - boost * seal_standard)
    require_zero(
        "seal_removes_continuous_base_boost_at_fixed_surface",
        seal_boost_commutator
        - sp.Matrix([[0, 2 * sp.sinh(chi)], [-2 * sp.sinh(chi), 0]]),
        checks,
    )
    require(
        "only_zero_real_boost_preserves_standard_seal",
        sp.solveset(sp.sinh(chi), chi, domain=sp.S.Reals) == sp.FiniteSet(0),
        checks,
    )

    pair_invariant = sp.factor(sp.trace(H.inv() * L.T * H * L))
    mu = k**2
    require_zero(
        "base_pair_invariant_retains_mu",
        pair_invariant - 2 * (1 + mu) / (1 - mu),
        checks,
    )

    # Full 2+2 coframe: use an angular axis reflection and the complete nonzero
    # parity-compatible base-angular cross block.
    H_base = sp.Matrix([[1, -k], [-k, 1]])
    F1 = sp.Matrix([[0, 1], [1, 0]])
    angular_metric = sp.eye(2)
    angular_reflection = sp.diag(1, -1)
    cross = sp.Matrix([[u, v], [u, -v]])
    require_zero(
        "complete_cross_block_parity_equation",
        F1.T * cross * angular_reflection - cross,
        checks,
    )
    full_metric = H_base.row_join(cross).col_join(cross.T.row_join(angular_metric))
    full_seal = sp.diag(1, 1, 1, 1)
    full_seal[:2, :2] = F1
    full_seal[2:, 2:] = angular_reflection
    full_generator = sp.diag(-1, 1, 0, 0)
    require_zero("full_seal_involution", full_seal**2 - sp.eye(4), checks)
    require_zero("full_seal_metric_isometry", full_seal.T * full_metric * full_seal - full_metric, checks)
    require_zero("full_seal_inverts_generator", full_seal * full_generator * full_seal + full_generator, checks)
    require("full_seal_orientation_preserving_witness", full_seal.det() == 1, checks)
    require("full_seal_fixed_dimension_two", len((full_seal - sp.eye(4)).nullspace()) == 2, checks)
    require("full_seal_antifixed_dimension_two", len((full_seal + sp.eye(4)).nullspace()) == 2, checks)

    # In the conditional transverse-identity reciprocal extension, im(L4)
    # selects the reciprocal plane. The metric then constructs its unique
    # orthogonal complement even when the coordinate base/angular blocks mix.
    reciprocal_plane_basis = sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    orthogonal_projector = sp.simplify(
        reciprocal_plane_basis
        * H_base.inv()
        * reciprocal_plane_basis.T
        * full_metric
    )
    require_zero(
        "metric_orthogonal_reciprocal_projector_is_idempotent",
        orthogonal_projector**2 - orthogonal_projector,
        checks,
    )
    require_zero(
        "metric_orthogonal_reciprocal_projector_is_self_adjoint",
        orthogonal_projector.T * full_metric - full_metric * orthogonal_projector,
        checks,
    )
    require_zero(
        "seal_preserves_metric_orthogonal_split",
        full_seal * orthogonal_projector * full_seal - orthogonal_projector,
        checks,
    )
    transverse_complement_metric = sp.simplify(
        angular_metric - cross.T * H_base.inv() * cross
    )
    require_zero(
        "transverse_complement_metric_formula",
        transverse_complement_metric
        - sp.diag(
            (k + 2 * u**2 - 1) / (k - 1),
            (k - 2 * v**2 + 1) / (k + 1),
        ),
        checks,
    )

    P4 = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
    full_g = sp.simplify(P4.T * full_metric * P4)
    require_zero(
        "full_depth_reversal_metric_isometry",
        full_seal.T * full_g.subs(phi, -phi) * full_seal - full_g,
        checks,
    )
    full_determinant = sp.factor(full_metric.det())
    require_zero(
        "full_metric_determinant_formula",
        full_determinant - (-k + 2 * v**2 - 1) * (k + 2 * u**2 - 1),
        checks,
    )
    full_invariant = sp.factor(
        sp.trace(full_metric.inv() * full_generator.T * full_metric * full_generator)
    )
    expected_full_invariant = sp.factor(
        2
        * (k**2 + k * u**2 - k * v**2 - u**2 - v**2 + 1)
        / ((-k + 2 * v**2 - 1) * (k + 2 * u**2 - 1))
    )
    require_zero("full_pair_invariant_formula", full_invariant - expected_full_invariant, checks)

    # Exact nonzero-coupling witnesses with identical angular block, angular seal,
    # cross coupling, c convention, orientation class, and Lorentz signature.
    epsilon = sp.Rational(1, 10)
    witnesses: dict[str, dict[str, object]] = {}
    for label, kval, determinant, invariant in (
        ("MU4", 2, sp.Rational(-7599, 2500), sp.Rational(-8300, 2533)),
        ("MU9", 3, sp.Rational(-20099, 2500), sp.Rational(-49900, 20099)),
    ):
        substitutions = {k: kval, u: epsilon, v: epsilon}
        witness_metric = full_metric.subs(substitutions)
        witness_det = sp.factor(witness_metric.det())
        witness_I = sp.factor(full_invariant.subs(substitutions))
        require_zero(f"{label}_nonzero_cross_determinant", witness_det - determinant, checks)
        require_zero(f"{label}_full_pair_invariant", witness_I - invariant, checks)
        first_block_det = sp.Rational(1 - kval) - 2 * epsilon**2
        second_block_det = sp.Rational(1 + kval) - 2 * epsilon**2
        require(f"{label}_one_Lorentz_negative_direction", first_block_det < 0 < second_block_det, checks)
        require(f"{label}_cross_block_nonzero", witness_metric[:2, 2:] != sp.zeros(2), checks)
        witness_transverse = transverse_complement_metric.subs(substitutions)
        require(
            f"{label}_metric_selected_transverse_complement_positive",
            witness_transverse[0, 0] > 0 and witness_transverse[1, 1] > 0,
            checks,
        )
        witnesses[label] = {
            "mu": kval**2,
            "determinant": str(determinant),
            "full_pair_invariant": str(invariant),
            "cross_u": "1/10",
            "cross_v": "1/10",
            "signature": "(-,+,+,+)",
        }
    require(
        "nonzero_coupling_does_not_collapse_mu_witnesses",
        witnesses["MU4"]["full_pair_invariant"] != witnesses["MU9"]["full_pair_invariant"],
        checks,
    )

    # Determinant/volume normalization can be satisfied for every k>1 by an
    # angular scale. It removes one common scale, not the dimensionless pair invariant.
    angular_scale = 1 / sp.sqrt(k**2 - 1)
    volume_metric = sp.diag(1, 1, angular_scale, angular_scale)
    volume_metric[:2, :2] = H_base
    require_zero("unit_determinant_angular_compensation", volume_metric.det() + 1, checks)
    volume_invariant = sp.factor(
        sp.trace(volume_metric.inv() * full_generator.T * volume_metric * full_generator)
    )
    require_zero("unit_determinant_retains_mu", volume_invariant - 2 * (1 + k**2) / (1 - k**2), checks)
    common_scale = sp.symbols("common_scale", positive=True)
    scaled_full = common_scale**2 * full_metric
    scaled_invariant = sp.factor(
        sp.trace(scaled_full.inv() * full_generator.T * scaled_full * full_generator)
    )
    require_zero("positive_CSN_does_not_change_full_pair_invariant", scaled_invariant - full_invariant, checks)
    require_zero("four_metric_determinant_CSN_weight", scaled_full.det() - common_scale**8 * full_metric.det(), checks)

    # Cartan geometry can see k once a nontrivial metric is supplied, but an
    # identity computing curvature is not an equation selecting its value.
    t_coord, r_coord = sp.symbols("t_coord r_coord", real=True)
    varying_metric = sp.Matrix(
        [[sp.exp(-2 * r_coord), -k], [-k, sp.exp(2 * r_coord)]]
    )
    curvature = scalar_curvature(varying_metric, [t_coord, r_coord])
    require_zero(
        "varying_reciprocal_metric_scalar_curvature",
        curvature - 4 * sp.exp(-2 * r_coord) / (k**2 - 1),
        checks,
    )
    require(
        "Cartan_curvature_distinguishes_but_does_not_select_witnesses",
        sp.simplify(curvature.subs(k, 2) - curvature.subs(k, 3)) != 0,
        checks,
    )

    outcomes = [
        "ANGULAR_SEAL_STRUCTURE_LEAVES_MU_OPEN",
        "NONZERO_ANGULAR_COUPLING_LEAVES_MU_OPEN",
        "CSN_OR_VOLUME_NORMALIZATION_LEAVES_MU_OPEN",
        "CARTAN_HOLONOMY_IS_CONDITIONAL_ON_COFRAME_CHOICE",
        "BOOTSTRAP_HAS_NO_CURRENT_SOLDERING_EQUATION",
        "METRIC_NATIVE_SOLDERING_RULE_ABSENT_FROM_CURRENT_LEDGER",
        "FULL_ANGULAR_DYNAMIC_COMPLETION_COULD_STILL_SELECT_OPEN",
    ]
    result = {
        "schema": "udt-clock-ruler-soldering-selector-derivation-1.0",
        "maximum_conclusion": "UDT_CURRENT_METRIC_NATIVE_SOLDERING_SELECTOR_STATUS_CHARACTERIZED",
        "outcomes": outcomes,
        "seal_local_base_soldering": {
            "status": "DERIVED_CONDITIONAL_WITHIN_PRE_SPLIT_MIXED_BASE_AT_SEAL",
            "spatial_branch": "B=-k*A*b with A>0,b>0,k>1",
            "time_line": "F_b +1 eigenspace span((b,1))",
            "radial_line": "F_b -1 eigenspace span((-b,1))",
            "normalization": "metric norms give eta; residual continuous O(1,1) boost is removed by fixing the seal to diag(+1,-1)",
            "temporal_relation": "-F_b becomes diag(-1,+1) in the same base frame",
            "limit": "requires the pre-split base and holds at the fixed seal; full angular parity subspaces are higher-dimensional",
        },
        "conditional_complete_soldering": {
            "status": "DERIVED_WITHIN_CHOSEN_TRANSVERSE_IDENTITY_AND_AXIS_REFLECTION_LIFT",
            "reciprocal_plane": "im(L4)",
            "transverse_plane": "metric-orthogonal complement of im(L4)",
            "seal_axes": "joint metric normalization and seal parity reduce the local frame to discrete signs",
            "cross_terms": "allowed and absorbed by the metric-orthogonal projector; they do not fix mu",
            "limit": "the transverse-identity reciprocal extension and angular axis-reflection lift are conditional witnesses, not selected current UDT structure",
        },
        "mu_status": {
            "status": "INVARIANT_OPEN",
            "base_invariant": "2*(1+mu)/(1-mu)",
            "selected_sign_only": "spatial rather than temporal seal selects the B<-|A*b| branch in the stated convention",
            "magnitude": "not selected",
        },
        "full_coframe_countermodels": witnesses,
        "selector_rank": {
            "CSN": "one scalar gauge direction; no dimensionless-mu equation",
            "spatial_seal": "involution and parity decomposition; no magnitude equation",
            "angular_lift": "multiple lifts and same-parity base-angular couplings remain",
            "Cartan": "connection/curvature derived per supplied representative and coframe; curvature may see mu but identities do not choose it",
            "bootstrap": "current after-solution admissibility predicate; no coframe map or invariant equation",
        },
        "outcome_scope": {
            "METRIC_NATIVE_SOLDERING_RULE_ABSENT_FROM_CURRENT_LEDGER": "complete selected lift and global continuation absent; a conditional seal-local construction is present",
            "FULL_ANGULAR_DYNAMIC_COMPLETION_COULD_STILL_SELECT_OPEN": "could select the complete lift, global transport, and mu; none is currently supplied",
        },
        "check_count": len(checks),
        "checks": checks,
        "exclusions": [
            "action or field-equation selection",
            "imported observer/tetrad mechanics",
            "global angular topology or section",
            "physical representative or scale",
            "carrier, source, matter, mass, and boundary charge",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
