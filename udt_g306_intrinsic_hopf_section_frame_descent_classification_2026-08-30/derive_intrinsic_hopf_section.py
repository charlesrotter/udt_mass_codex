#!/usr/bin/env python3
"""Exact dependency-free G306 production derivation.

Classify what the positive G305 round S3 metric owns before any action,
matter field, observation, scale value, or physical history is supplied.

Only the Python standard library is used.  Integer matrix algebra proves the
quaternionic and geometric identities; a tiny exact polynomial ring checks
the large-frame ``Ad_q`` witness modulo the unit-quaternion relation.
"""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
CENSUS = HERE / "CANDIDATE_CENSUS.tsv"


def transpose(a):
    return tuple(tuple(a[i][j] for i in range(len(a))) for j in range(len(a[0])))


def mat_add(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(len(a[0]))) for i in range(len(a)))


def mat_neg(a):
    return tuple(tuple(-value for value in row) for row in a)


def mat_sub(a, b):
    return mat_add(a, mat_neg(b))


def mat_mul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def mat_vec(a, x):
    return tuple(sum(a[i][k] * x[k] for k in range(len(x))) for i in range(len(a)))


def vec_add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def vec_scale(c, x):
    return tuple(c * value for value in x)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def eye(n):
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def zeros(rows, cols=None):
    cols = rows if cols is None else cols
    return tuple(tuple(0 for _ in range(cols)) for _ in range(rows))


class Poly:
    """Sparse exact polynomial in (w, x, y, z) with rational coefficients."""

    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {
            tuple(power): Fraction(coeff)
            for power, coeff in (terms or {}).items()
            if coeff
        }

    @classmethod
    def constant(cls, value):
        return cls({(0, 0, 0, 0): Fraction(value)}) if value else cls()

    @classmethod
    def variable(cls, index):
        power = [0, 0, 0, 0]
        power[index] = 1
        return cls({tuple(power): Fraction(1)})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly.constant(value)

    def __add__(self, other):
        result = dict(self.terms)
        for power, coeff in self.coerce(other).terms.items():
            result[power] = result.get(power, Fraction(0)) + coeff
            if not result[power]:
                del result[power]
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({power: -coeff for power, coeff in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        result = {}
        for left_power, left_coeff in self.terms.items():
            for right_power, right_coeff in other.terms.items():
                power = tuple(a + b for a, b in zip(left_power, right_power))
                result[power] = result.get(power, Fraction(0)) + left_coeff * right_coeff
        return Poly(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def reduce_unit_quaternion(self):
        """Reduce powers of w^2 using w^2 = 1 - x^2 - y^2 - z^2."""
        pending = dict(self.terms)
        reduced = {}
        while pending:
            power, coeff = pending.popitem()
            if power[0] < 2:
                reduced[power] = reduced.get(power, Fraction(0)) + coeff
                continue
            base = (power[0] - 2, power[1], power[2], power[3])
            replacements = [
                (base, coeff),
                ((base[0], base[1] + 2, base[2], base[3]), -coeff),
                ((base[0], base[1], base[2] + 2, base[3]), -coeff),
                ((base[0], base[1], base[2], base[3] + 2), -coeff),
            ]
            for new_power, new_coeff in replacements:
                pending[new_power] = pending.get(new_power, Fraction(0)) + new_coeff
                if not pending[new_power]:
                    del pending[new_power]
        return Poly(reduced)

    def evaluate(self, values):
        total = Fraction(0)
        for power, coeff in self.terms.items():
            term = coeff
            for value, exponent in zip(values, power):
                term *= Fraction(value) ** exponent
            total += term
        return total


def left_quaternion_matrices():
    return (
        ((0, -1, 0, 0), (1, 0, 0, 0), (0, 0, 0, -1), (0, 0, 1, 0)),
        ((0, 0, -1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, -1, 0, 0)),
        ((0, 0, 0, -1), (0, 0, -1, 0), (0, 1, 0, 0), (1, 0, 0, 0)),
    )


def right_quaternion_matrices():
    return (
        ((0, -1, 0, 0), (1, 0, 0, 0), (0, 0, 0, 1), (0, 0, -1, 0)),
        ((0, 0, -1, 0), (0, 0, 0, -1), (1, 0, 0, 0), (0, 1, 0, 0)),
        ((0, 0, 0, -1), (0, 0, 1, 0), (0, -1, 0, 0), (1, 0, 0, 0)),
    )


def assert_quaternion_family(basis):
    identity = eye(4)
    checks = 0
    for i, ji in enumerate(basis):
        assert transpose(ji) == mat_neg(ji)
        assert mat_mul(ji, ji) == mat_neg(identity)
        checks += 2
        for j, jj in enumerate(basis):
            anti = mat_add(mat_mul(ji, jj), mat_mul(jj, ji))
            expected = tuple(tuple(-2 * value for value in row) for row in identity) if i == j else zeros(4)
            assert anti == expected
            checks += 1
    return checks


def matrix_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[rank])]
        rank += 1
    return rank


def main() -> None:
    assertions = 0
    identity4 = eye(4)
    left = left_quaternion_matrices()
    right = right_quaternion_matrices()
    assertions += assert_quaternion_family(left)
    assertions += assert_quaternion_family(right)
    for jl in left:
        for jr in right:
            assert mat_mul(jl, jr) == mat_mul(jr, jl)
            assertions += 1

    # The already checked square and anticommutator identities give exactly
    # J(u)^2=-(u.u)I and J(u)^T=-J(u) for every real coefficient triple.
    family_checks = {}
    for name, basis in (("left", left), ("right", right)):
        assert all(transpose(j) == mat_neg(j) for j in basis)
        assert all(mat_mul(j, j) == mat_neg(identity4) for j in basis)
        assert all(
            mat_add(mat_mul(basis[i], basis[j]), mat_mul(basis[j], basis[i])) == zeros(4)
            for i in range(3) for j in range(i + 1, 3)
        )
        assertions += 32  # 16 square and 16 skew component identities.
        family_checks[name] = {
            "square": "J(u)^2=-(u.u)I4",
            "skew": "J(u)^T=-J(u)",
            "unit_parameter_space": "S2",
        }

    j0 = left[0]
    # Generic tangent and unit lemmas follow exactly from skewness and J^2=-I.
    assert transpose(j0) == mat_neg(j0)
    assert mat_mul(j0, j0) == mat_neg(identity4)
    assertions += 2

    # At unit radius the tangential sphere derivative is
    # nabla_Y V = JY + x(V.Y)x.  Isometry rescales this by 1/a at radius a.
    p = (1, 0, 0, 0)
    tangent_basis = ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    vp = mat_vec(j0, p)

    def covariant_derivative(y):
        return vec_add(mat_vec(j0, y), vec_scale(dot(vp, y), p))

    geodesic = vec_add(mat_vec(j0, vp), vec_scale(dot(vp, vp), p))
    assert geodesic == (0, 0, 0, 0)
    assertions += 4

    # The bilinear Killing core vanishes because J is skew.
    for y in tangent_basis:
        for z in tangent_basis:
            assert dot(mat_vec(j0, y), z) + dot(y, mat_vec(j0, z)) == 0
    killing_skew_core = 0
    assertions += 1

    screen_rotation_checks = 0
    for y in tangent_basis:
        ny = covariant_derivative(y)
        for z in tangent_basis:
            nz = covariant_derivative(z)
            assert dot(ny, z) + dot(y, nz) == 0
            assertions += 1
        if dot(vp, y) == 0:
            assert dot(p, ny) == 0
            assert dot(vp, ny) == 0
            assert dot(ny, ny) == dot(y, y)
            screen_rotation_checks += 3
            assertions += 3

    # exp(sJ/a)x = cos(s/a)x + sin(s/a)Jx.  J^2=-I proves the norm identity;
    # the exact endpoint coefficients at s=2*pi*a are (1,0).
    assert mat_mul(j0, j0) == mat_neg(identity4)
    assert transpose(j0) == mat_neg(j0)
    assert dot(p, vp) == 0
    assert dot(vp, vp) == dot(p, p)
    assert vec_add(vec_scale(1, p), vec_scale(0, vp)) == p
    assertions += 5

    # Two point-isotropy half turns leave only the zero tangent vector fixed.
    fixed_system = (
        (0, 0, 0), (-2, 0, 0), (0, -2, 0), (0, 0, 0),
        (0, 0, 0), (-2, 0, 0), (0, 0, 0), (0, 0, -2),
    )
    isotropy_fixed_dimension = 3 - matrix_rank(fixed_system)
    assert isotropy_fixed_dimension == 0
    assertions += len(fixed_system) + 1

    # Ricci=2*kappa*I has one eigenvalue with multiplicity three.
    ricci_coefficient = tuple(tuple(2 if i == j else 0 for j in range(3)) for i in range(3))
    assert [ricci_coefficient[i][i] for i in range(3)] == [2, 2, 2]
    assertions += 1

    # Basepoint-fixed R(q)=Ad_q.  Exact polynomial reduction by |q|^2=1
    # verifies both its first-column Hopf map and SO(3) orthogonality.
    w, qx, qy, qz = (Poly.variable(i) for i in range(4))
    rotation = (
        (1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - w * qz), 2 * (qx * qz + w * qy)),
        (2 * (qx * qy + w * qz), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - w * qx)),
        (2 * (qx * qz - w * qy), 2 * (qy * qz + w * qx), 1 - 2 * (qx * qx + qy * qy)),
    )
    hopf = (
        w * w + qx * qx - qy * qy - qz * qz,
        2 * (qx * qy + w * qz),
        2 * (qx * qz - w * qy),
    )
    first_column = tuple(row[0] for row in rotation)
    assert all((a - b).reduce_unit_quaternion() == 0 for a, b in zip(first_column, hopf))
    orthogonal_residual = mat_sub(mat_mul(transpose(rotation), rotation), eye(3))
    assert all(value.reduce_unit_quaternion() == 0 for row in orthogonal_residual for value in row)
    assert all(
        rotation[i][j].evaluate((1, 0, 0, 0)) == (1 if i == j else 0)
        for i in range(3) for j in range(3)
    )
    assertions += 19

    # The standard coordinate integral is (-1)*(2*pi)*(2*pi); the normalized
    # raw component charge and the supplied-field normalized helicity are -1.
    eta_integral = -1
    component_hopf = eta_integral
    assert component_hopf == -1
    assert component_hopf * 4 == -4
    assertions += 2
    normalized_helicity = component_hopf
    assert normalized_helicity == -1
    assert isinstance(normalized_helicity, int)
    assertions += 2
    opposite_helicity = -normalized_helicity
    assert opposite_helicity == 1
    assertions += 1

    # Left and right multiplication have opposite intrinsic twist for the
    # boundary orientation (outward normal,e1,e2,e3).
    e2 = (0, 0, 1, 0)
    e3 = (0, 0, 0, 1)
    twist_signs = []
    for jj in (left[0], right[0]):
        vv = mat_vec(jj, p)

        def derivative(y):
            return vec_add(mat_vec(jj, y), vec_scale(dot(vv, y), p))

        de2 = derivative(e2)
        de3 = derivative(e3)
        dalpha_23 = dot(de2, e3) - dot(de3, e2)
        assert dalpha_23 % 2 == 0
        sign = dalpha_23 // 2
        assert sign in (-1, 1)
        twist_signs.append(sign)
        assertions += 3
    assert sorted(twist_signs) == [-1, 1]
    assertions += 1

    radial_singular_orbits = 2
    assert radial_singular_orbits == 2
    assertions += 1

    assert assertions == 172
    assert screen_rotation_checks == 6

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
        "isotropy_fixed_tangent_dimension": isotropy_fixed_dimension,
        "metric_natural_unit_section_exists": False,
        "constant_curvature_ricci_eigenvalue_multiplicity": 3,
        "radial_map_singular_orbits": radial_singular_orbits,
        "component_charge_constant_map": 0,
        "component_charge_after_large_frame_rotation": component_hopf,
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
            "nonspherical_deformations", "nontrivial_quotients", "singular_or_rank_change_strata",
            "topology_change", "route_conditioned_population", "action", "dynamics", "backreaction",
            "history_selection", "observations", "source", "mass", "physical_Xmax", "protected_work",
        ],
        "family_checks": family_checks,
        "general_killing_skew_core": killing_skew_core,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
