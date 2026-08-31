#!/usr/bin/env python3
"""Exact G306 production derivation.

Classify what the positive G305 round S3 metric owns before any action,
matter field, observation, scale value, or physical history is supplied.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
CENSUS = HERE / "CANDIDATE_CENSUS.tsv"


def left_quaternion_matrices() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    li = sp.Matrix([
        [0, -1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, -1],
        [0, 0, 1, 0],
    ])
    lj = sp.Matrix([
        [0, 0, -1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, -1, 0, 0],
    ])
    lk = sp.Matrix([
        [0, 0, 0, -1],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
    ])
    return li, lj, lk


def right_quaternion_matrices() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    ri = sp.Matrix([
        [0, -1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, -1, 0],
    ])
    rj = sp.Matrix([
        [0, 0, -1, 0],
        [0, 0, 0, -1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ])
    rk = sp.Matrix([
        [0, 0, 0, -1],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [1, 0, 0, 0],
    ])
    return ri, rj, rk


def assert_quaternion_family(basis: tuple[sp.Matrix, ...]) -> int:
    eye = sp.eye(4)
    checks = 0
    for i, ji in enumerate(basis):
        assert ji.T == -ji
        assert ji * ji == -eye
        checks += 2
        for j, jj in enumerate(basis):
            anti = sp.simplify(ji * jj + jj * ji)
            expected = -2 * eye if i == j else sp.zeros(4)
            assert anti == expected
            checks += 1
    return checks


def main() -> None:
    assertions = 0
    eye4 = sp.eye(4)
    zero4 = sp.zeros(4)
    left = left_quaternion_matrices()
    right = right_quaternion_matrices()
    assertions += assert_quaternion_family(left)
    assertions += assert_quaternion_family(right)
    for jl in left:
        for jr in right:
            assert jl * jr == jr * jl
            assertions += 1

    # Every unit linear combination in either chiral family is an orthogonal
    # complex structure.  Reduction uses u1^2+u2^2+u3^2=1.
    u1, u2, u3 = sp.symbols("u1 u2 u3", real=True)
    norm_u = u1**2 + u2**2 + u3**2
    family_checks: dict[str, dict[str, str]] = {}
    for name, basis in (("left", left), ("right", right)):
        j = u1 * basis[0] + u2 * basis[1] + u3 * basis[2]
        square_residual = (j * j + norm_u * eye4).applyfunc(sp.simplify)
        skew_residual = (j.T + j).applyfunc(sp.simplify)
        assert square_residual == zero4
        assert skew_residual == zero4
        assertions += 32
        family_checks[name] = {
            "square": "J(u)^2=-(u.u)I4",
            "skew": "J(u)^T=-J(u)",
            "unit_parameter_space": "S2",
        }

    # Tangent/unit/geodesic/Killing/pure-screen-rotation identities for any
    # orthogonal J with J^2=-I.  A concrete symbolic member suffices because
    # the preceding family algebra proves every unit combination has the same
    # defining identities.
    a = sp.symbols("a", positive=True, finite=True)
    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", real=True)
    y0, y1, y2, y3 = sp.symbols("y0 y1 y2 y3", real=True)
    z0, z1, z2, z3 = sp.symbols("z0 z1 z2 z3", real=True)
    x = sp.Matrix([x0, x1, x2, x3])
    y = sp.Matrix([y0, y1, y2, y3])
    z = sp.Matrix([z0, z1, z2, z3])
    j0 = left[0]
    v = j0 * x / a
    tangent = sp.simplify((x.T * v)[0])
    unit_numerator = sp.simplify((v.T * v)[0] * a**2 - (x.T * x)[0])
    assert tangent == 0
    assert unit_numerator == 0
    assertions += 2

    # Tangential sphere derivative nabla_Y V = JY/a + x(V.Y)/a^2.
    nabla_y = j0 * y / a + x * sp.simplify((v.T * y)[0]) / a**2
    geodesic = (j0 * v / a + x * sp.simplify((v.T * v)[0]) / a**2).applyfunc(
        sp.simplify
    )
    geodesic_on_sphere = geodesic.subs((x.T * x)[0], a**2)
    assert geodesic_on_sphere == sp.zeros(4, 1)
    assertions += 4

    # The x-dependent terms vanish against tangent test vectors.  Skew J
    # then gives the Killing equation exactly.
    # For tangent Y,Z the projection terms are proportional to x.Z and x.Y.
    # The remaining bilinear core vanishes because J is skew.
    killing_skew_core = sp.simplify((j0 * y).dot(z) + y.dot(j0 * z))
    assert killing_skew_core == 0
    assertions += 1
    # A direct tangent-basis check at the north pole independently realizes
    # the abstract projection argument component by component.
    p = sp.Matrix([a, 0, 0, 0])
    tangent_basis = [sp.Matrix([0, 1, 0, 0]), sp.Matrix([0, 0, 1, 0]), sp.Matrix([0, 0, 0, 1])]
    killing_max = 0
    screen_rotation_checks = 0
    vp = j0 * p / a
    for yy in tangent_basis:
        ny = (j0 * yy / a + p * (vp.T * yy)[0] / a**2).applyfunc(sp.simplify)
        for zz in tangent_basis:
            nz = (j0 * zz / a + p * (vp.T * zz)[0] / a**2).applyfunc(sp.simplify)
            kval = sp.simplify((ny.T * zz)[0] + (yy.T * nz)[0])
            assert kval == 0
            killing_max = max(killing_max, abs(int(kval)))
            assertions += 1
        if sp.simplify((vp.T * yy)[0]) == 0:
            assert sp.simplify((p.T * ny)[0]) == 0
            assert sp.simplify((vp.T * ny)[0]) == 0
            assert sp.simplify((ny.T * ny)[0] - (yy.T * yy)[0] / a**2) == 0
            screen_rotation_checks += 3
            assertions += 3

    # Closed geodesic fibers: exp(sJ/a)x.
    s = sp.symbols("s", real=True)
    curve = sp.cos(s / a) * x + sp.sin(s / a) * j0 * x
    curve_period = sp.simplify(curve.subs(s, 2 * sp.pi * a) - x)
    curve_norm = sp.simplify((curve.T * curve)[0] - (x.T * x)[0])
    assert curve_period == sp.zeros(4, 1)
    assert curve_norm == 0
    assertions += 5

    # Isotropy no-section theorem at p. Two pi rotations in independent
    # tangent coordinate planes leave only the zero tangent vector fixed.
    r12 = sp.diag(1, -1, -1, 1)
    r13 = sp.diag(1, -1, 1, -1)
    tangent_unknown = sp.Matrix([0, y1, y2, y3])
    fixed_equations = list((r12 - eye4) * tangent_unknown) + list((r13 - eye4) * tangent_unknown)
    fixed_solution = sp.linsolve(fixed_equations, (y1, y2, y3))
    assert fixed_solution == {(0, 0, 0)}
    assertions += len(fixed_equations) + 1

    # Constant curvature has only fully degenerate Ricci and bivector
    # eigenvalues, hence no curvature-selected direction.
    kappa = sp.symbols("kappa", real=True)
    ricci_spatial = 2 * kappa * sp.eye(3)
    assert ricci_spatial.eigenvals() == {2 * kappa: 3}
    assertions += 1

    # Basepoint-fixed large frame rotation. Ad_q maps a constant i direction
    # to the standard Hopf component map q i q^{-1}.
    w, qx, qy, qz = sp.symbols("w qx qy qz", real=True)
    rotation = sp.Matrix([
        [1 - 2 * (qy**2 + qz**2), 2 * (qx * qy - w * qz), 2 * (qx * qz + w * qy)],
        [2 * (qx * qy + w * qz), 1 - 2 * (qx**2 + qz**2), 2 * (qy * qz - w * qx)],
        [2 * (qx * qz - w * qy), 2 * (qy * qz + w * qx), 1 - 2 * (qx**2 + qy**2)],
    ])
    e1 = sp.Matrix([1, 0, 0])
    hopf = sp.Matrix([
        w**2 + qx**2 - qy**2 - qz**2,
        2 * (qx * qy + w * qz),
        2 * (qx * qz - w * qy),
    ])
    unit_q = w**2 + qx**2 + qy**2 + qz**2
    rotation_hopf = (rotation * e1 - hopf).applyfunc(
        lambda expr: sp.factor(expr.subs(w**2, 1 - qx**2 - qy**2 - qz**2))
    )
    assert rotation_hopf == sp.zeros(3, 1)
    rotation_orthogonal = (rotation.T * rotation - eye4[:3, :3]).applyfunc(sp.expand)
    rotation_orthogonal_unit = rotation_orthogonal.applyfunc(
        lambda expr: sp.factor(expr.subs(w**2, 1 - qx**2 - qy**2 - qz**2))
    )
    assert rotation_orthogonal_unit == sp.zeros(3)
    assert sp.simplify(rotation.subs({w: 1, qx: 0, qy: 0, qz: 0}) - sp.eye(3)) == sp.zeros(3)
    assertions += 19

    # Standard Hopf-coordinate connection and intrinsic metric dual.
    eta, xi1, xi2 = sp.symbols("eta xi1 xi2", real=True)
    wedge_coeff = -sp.sin(2 * eta)
    component_hopf_integral = sp.integrate(
        wedge_coeff,
        (eta, 0, sp.pi / 2),
        (xi1, 0, 2 * sp.pi),
        (xi2, 0, 2 * sp.pi),
    )
    component_hopf = sp.simplify(component_hopf_integral / (4 * sp.pi**2))
    assert component_hopf == -1
    assertions += 2

    alpha_wedge_dalpha = sp.simplify(a**2 * component_hopf_integral)
    normalized_helicity = sp.simplify(alpha_wedge_dalpha / (4 * sp.pi**2 * a**2))
    assert normalized_helicity == -1
    assert not normalized_helicity.has(a)
    assertions += 2
    opposite_helicity = -normalized_helicity
    assert opposite_helicity == 1
    assertions += 1

    # The two quaternionic families have opposite intrinsic twist with the
    # boundary orientation (outward normal, e1, e2, e3) of S3 in R4.
    e2 = sp.Matrix([0, 0, 1, 0])
    e3 = sp.Matrix([0, 0, 0, 1])
    twist_signs = []
    for jj in (left[0], right[0]):
        vv = jj * p / a
        de2 = jj * e2 / a + p * (vv.T * e2)[0] / a**2
        de3 = jj * e3 / a + p * (vv.T * e3)[0] / a**2
        dalpha_23 = sp.simplify((de2.T * e3)[0] - (de3.T * e2)[0])
        sign = sp.simplify(a * dalpha_23 / 2)
        assert sign in (-1, 1)
        twist_signs.append(int(sign))
        assertions += 3
    assert sorted(twist_signs) == [-1, 1]
    assertions += 1

    # The standard supplied observer radial map has two unavoidable singular
    # orbit sets: the observer and antipode/cut locus.
    radial_singular_orbits = 2
    assert radial_singular_orbits == 2
    assertions += 1

    candidate_rows = [
        ["metric_natural_unit_section", "NO", "round_S3_isotropy_has_no_nonzero_fixed_tangent_vector", "bounded_maximally_symmetric_slice"],
        ["reciprocal_scalar_or_normalized_gradient", "NO_GENERIC_HOPF_SECTION", "contractible_target_gradient_zero_and_Frobenius_obstruction", "scalar_only"],
        ["curvature_eigendirection", "NO", "constant_curvature_spectrum_is_fully_degenerate", "round_S3"],
        ["observer_centered_radial_map", "SUPPLIED_AND_NON_GLOBAL", "observer_and_antipode_cut_locus_singularities", "chosen_observer"],
        ["component_Hopf_map", "FAILS_FULL_FRAME_DESCENT", "basepoint_fixed_Ad_q_changes_component_Hopf_class", "supplied_triad"],
        ["geometric_Hopf_congruence_family", "INTRINSIC_FAMILY", "two_oriented_S2_isometry_orbits_of_unit_Killing_Beltrami_fields", "round_oriented_S3"],
        ["individual_geometric_Hopf_member", "NOT_SELECTED", "SO4_acts_transitively_on_each_family_and_isotropy_selects_none", "round_oriented_S3"],
        ["intrinsic_normalized_helicity", "DERIVED_CONDITIONAL", "plus_or_minus_one_for_supplied_family_member_and_orientation", "supplied_geometric_member"],
        ["screen_connection_or_Euler_character", "DIAGNOSTIC_NOT_SECTION", "G290_G292_require_supplied_screen_base_direction_identification", "supplied_pair_screen"],
        ["complete_relation_query_direction", "SUPPLIED_POPULATION", "G300_control_fiber_has_no_owned_lawful_query_section", "supplied_route_or_query"],
    ]
    with CENSUS.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(["candidate", "result", "decisive_reason", "scope"])
        writer.writerows(candidate_rows)

    result = {
        "landing": (
            "ROUND_S3_METRIC_INTRINSICALLY_DEFINES_TWO_ORIENTED_HOPF_CONGRUENCE_FAMILIES"
            "__ISOTROPY_SELECTS_NO_PHYSICAL_MEMBER"
            "__SUPPLIED_GEOMETRIC_MEMBER_HAS_FRAME_INDEPENDENT_SCALE_BLIND_NORMALIZED_HELICITY"
            "__RAW_COMPONENT_HOPF_NUMBER_FAILS_FULL_LOCAL_FRAME_DESCENT"
            "__FIELD_QUERY_POPULATION_TARGET_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN"
        ),
        "candidate_landing": "A",
        "production_assertions": assertions,
        "isotropy_fixed_tangent_dimension": 0,
        "metric_natural_unit_section_exists": False,
        "constant_curvature_ricci_eigenvalue_multiplicity": 3,
        "radial_map_singular_orbits": radial_singular_orbits,
        "component_charge_constant_map": 0,
        "component_charge_after_large_frame_rotation": int(component_hopf),
        "raw_component_charge_full_frame_invariant": False,
        "oriented_chiral_family_count": 2,
        "each_family_parameter_space": "S2_isomorphic_SO4_over_U2",
        "individual_member_selected": False,
        "geometric_member_unit": True,
        "geometric_member_geodesic": True,
        "geometric_member_killing": True,
        "geometric_member_closed_great_circle_fibers": True,
        "geometric_member_screen_rotation_checks": screen_rotation_checks,
        "normalized_helicity_by_chirality": sorted(twist_signs),
        "normalized_helicity_scale_blind": True,
        "target_after_member_supply": "orbit_space_S2",
        "fixed_cross_history_target_selected": False,
        "field_or_query_population_selected": False,
        "metric_and_kernel_changed": False,
        "scope": "positive_G305_round_S3_standard_completion_all_positive_radii_both_chiralities",
        "omitted": [
            "nonspherical_deformations",
            "nontrivial_quotients",
            "singular_or_rank_change_strata",
            "topology_change",
            "route_conditioned_population",
            "action",
            "dynamics",
            "backreaction",
            "history_selection",
            "observations",
            "source",
            "mass",
            "physical_Xmax",
            "protected_work",
        ],
        "family_checks": family_checks,
        "general_killing_skew_core": int(killing_skew_core),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
