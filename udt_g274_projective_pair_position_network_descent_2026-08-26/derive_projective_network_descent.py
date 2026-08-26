#!/usr/bin/env python3
"""Exact G274 projective pair-position network descent derivation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "FULL_PATH_LABELLED_FRAME_MORPHISMS_DESCEND_EXACTLY__"
    "PROJECTIVE_OPEN_BALL_VECTOR_IS_A_VALID_PAIR_COORDINATE_BUT_NOT_A_"
    "STANDALONE_NONRADIAL_COMPOSITION_LAW__SCREEN_FRAME_CARRY_IS_REQUIRED__"
    "RADIAL_MOBIUS_STRATUM_CLOSES__SCALE_HISTORY_BRANCH_POPULATION_AND_XMAX_REMAIN_OPEN"
)


def boost_from_cayley(q: sp.Matrix) -> sp.Matrix:
    """Rational future Lorentz boost from a rational open-ball Cayley parameter."""

    q2 = (q.T * q)[0]
    gamma = sp.cancel((1 + q2) / (1 - q2))
    spatial = q.applyfunc(lambda x: sp.cancel(2 * x / (1 - q2)))
    block = sp.eye(q.rows) + spatial * spatial.T / (gamma + 1)
    return sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[gamma]]), spatial.T),
        sp.Matrix.hstack(spatial, block),
    ).applyfunc(sp.cancel)


def projective_clock(matrix: sp.Matrix) -> sp.Matrix:
    clock = matrix[:, 0]
    return clock[1:, :] / clock[0]


def exact_zero(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(value) == 0 for value in matrix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    eta = sp.diag(-1, 1, 1, 1)
    e0 = sp.Matrix([1, 0, 0, 0])
    bx = boost_from_cayley(sp.Matrix([sp.Rational(1, 3), 0, 0]))
    bs = boost_from_cayley(sp.Matrix([0, sp.Rational(1, 4), sp.Rational(1, 5)]))
    rotation = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    rotation_2 = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, sp.Rational(3, 5), -sp.Rational(4, 5), 0],
            [0, sp.Rational(4, 5), sp.Rational(3, 5), 0],
            [0, 0, 0, 1],
        ]
    )

    composite = bs * bx
    carried_bs = bs * rotation
    carried_composite = carried_bs * bx
    v_bx = projective_clock(bx)
    v_bs = projective_clock(bs)
    v_carried_bs = projective_clock(carried_bs)
    v_composite = projective_clock(composite).applyfunc(sp.cancel)
    v_carried_composite = projective_clock(carried_composite).applyfunc(sp.cancel)

    z1, z2, z3 = sp.symbols("z1 z2 z3", real=True)

    def mobius(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.cancel((left + right) / (1 + left * right))

    gamma1, gamma2 = sp.symbols("gamma1 gamma2", nonzero=True)
    radial_1 = sp.Matrix([[gamma1, gamma1 * z1], [gamma1 * z1, gamma1]])
    radial_2 = sp.Matrix([[gamma2, gamma2 * z2], [gamma2 * z2, gamma2]])
    radial_composite = radial_2 * radial_1
    radial_projective = sp.cancel(radial_composite[1, 0] / radial_composite[0, 0])

    ca = rotation
    cb = rotation_2
    cc = rotation * rotation_2
    lab = bx
    lbc = bs
    lac = lbc * lab
    lab_prime = cb * lab * ca.inv()
    lbc_prime = cc * lbc * cb.inv()
    lac_prime = cc * lac * ca.inv()

    scale, rescale = sp.symbols("X k", positive=True)
    x_pair = scale * v_composite
    x_pair_rescaled = rescale * scale * v_composite

    holonomy = bx
    direct_with_holonomy = holonomy * composite

    checks = {
        "bx_preserves_lorentz_metric": exact_zero(bx.T * eta * bx - eta),
        "bs_preserves_lorentz_metric": exact_zero(bs.T * eta * bs - eta),
        "rotation_preserves_lorentz_metric": exact_zero(rotation.T * eta * rotation - eta),
        "rotation2_preserves_lorentz_metric": exact_zero(rotation_2.T * eta * rotation_2 - eta),
        "bx_inverse_is_opposite_boost": exact_zero(bx.inv() - boost_from_cayley(sp.Matrix([-sp.Rational(1, 3), 0, 0]))),
        "bs_inverse_is_opposite_boost": exact_zero(bs.inv() - boost_from_cayley(sp.Matrix([0, -sp.Rational(1, 4), -sp.Rational(1, 5)]))),
        "full_composite_preserves_metric": exact_zero(composite.T * eta * composite - eta),
        "full_reversal_inverts_composite": exact_zero(composite.inv() * composite - sp.eye(4)),
        "middle_composition_exact": exact_zero(lac - lbc * lab),
        "open_ball_vector_is_clock_projectivization": exact_zero(composite * e0 - composite[:, 0]),
        "bx_projective_norm_below_one": sp.cancel(1 - (v_bx.T * v_bx)[0]) > 0,
        "bs_projective_norm_below_one": sp.cancel(1 - (v_bs.T * v_bs)[0]) > 0,
        "composite_projective_norm_below_one": sp.cancel(1 - (v_composite.T * v_composite)[0]) > 0,
        "both_screen_components_active": v_bs[1] != 0 and v_bs[2] != 0,
        "same_projective_vector_under_right_spatial_carry": exact_zero(v_carried_bs - v_bs),
        "same_pair_vectors_different_carried_composite": not exact_zero(v_carried_composite - v_composite),
        "vector_projection_not_composition_congruence": not exact_zero(
            projective_clock((bs * rotation) * bx) - projective_clock(bs * bx)
        ),
        "noncollinear_boost_product_not_pure_symmetric_boost": not exact_zero(composite - composite.T),
        "radial_projective_is_mobius": sp.cancel(radial_projective - mobius(z2, z1)) == 0,
        "radial_mobius_associative": sp.cancel(mobius(z3, mobius(z2, z1)) - mobius(mobius(z3, z2), z1)) == 0,
        "radial_reversal": sp.cancel(mobius(z1, -z1)) == 0,
        "overlap_full_arrow_covariance": exact_zero(lbc_prime * lab_prime - lac_prime),
        "overlap_changes_coordinates_not_morphism_content": exact_zero(
            ca.inv() * lac_prime.inv() * cc - lac.inv()
        ),
        "common_scale_normalization_cancels": exact_zero(x_pair / scale - v_composite),
        "common_rescaling_does_not_select_scale": exact_zero(x_pair_rescaled / (rescale * scale) - v_composite),
        "path_holonomy_not_forced_to_identity": not exact_zero(direct_with_holonomy - composite),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    assert len(checks) == 26
    assert all(checks.values()), [key for key, value in checks.items() if not value]

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": (
            "B__FULL_FRAME_MORPHISM_DESCENDS__PROJECTIVE_VECTOR_REQUIRES_CARRY__"
            "RADIAL_MOBIUS_EXACT"
        ),
        "exact_checks": len(checks),
        "checks": checks,
        "separator": {
            "v_AB": [str(sp.cancel(x)) for x in v_bx],
            "v_BC": [str(sp.cancel(x)) for x in v_bs],
            "v_BC_same_after_right_spatial_carry": [str(sp.cancel(x)) for x in v_carried_bs],
            "v_composite_without_carry": [str(sp.cancel(x)) for x in v_composite],
            "v_composite_with_hidden_carry": [str(sp.cancel(x)) for x in v_carried_composite],
        },
        "scope": {
            "physical_position_attachment": "CANDIDATE_NOT_ADOPTED",
            "path_labels": "RETAINED",
            "dimensionful_scale": "OPEN_NOT_SELECTED",
            "history": "OPEN_NOT_SELECTED",
            "branch_population": "OPEN_NOT_SELECTED",
            "X_max": "OPEN_NOT_USED",
            "observations": "NOT_USED",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
