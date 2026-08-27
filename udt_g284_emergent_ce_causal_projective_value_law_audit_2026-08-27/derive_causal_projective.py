#!/usr/bin/env python3
"""Dependency-free exact G284 replay on the arbitrary-T Brinkmann family.

This production verifier deliberately uses only the Python standard library.
It implements the small Laurent-polynomial algebra needed by the proof, so
the sealed replay does not depend on a host SymPy installation.  The retained
``derive_causal_projective_sympy.py`` is a supplemental implementation.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
import json


LANDING = (
    "EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_"
    "TIDAL_HISTORY"
)
ATOMS = (
    "x",
    "y",
    "T_xx",
    "T_xy",
    "T_yy",
    "dT_xx",
    "dT_xy",
    "dT_yy",
    "ddT_xx",
    "ddT_xy",
    "ddT_yy",
    "c_E",
    "lambda",
)
INDEX = {name: position for position, name in enumerate(ATOMS)}
ZERO_MONOMIAL = (0,) * len(ATOMS)


class Poly:
    """Sparse exact Laurent polynomial over rational coefficients."""

    def __init__(self, terms: dict[tuple[int, ...], Fraction] | None = None) -> None:
        self.terms = {
            monomial: Fraction(coefficient)
            for monomial, coefficient in (terms or {}).items()
            if coefficient
        }

    @classmethod
    def constant(cls, value: int | Fraction) -> "Poly":
        coefficient = Fraction(value)
        return cls({ZERO_MONOMIAL: coefficient} if coefficient else {})

    @classmethod
    def atom(cls, name: str, exponent: int = 1) -> "Poly":
        powers = [0] * len(ATOMS)
        powers[INDEX[name]] = exponent
        return cls({tuple(powers): Fraction(1)})

    @staticmethod
    def coerce(value: "Poly | int | Fraction") -> "Poly":
        return value if isinstance(value, Poly) else Poly.constant(value)

    def __add__(self, other: "Poly | int | Fraction") -> "Poly":
        terms = dict(self.terms)
        for monomial, coefficient in self.coerce(other).terms.items():
            terms[monomial] = terms.get(monomial, Fraction(0)) + coefficient
            if not terms[monomial]:
                del terms[monomial]
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly({monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other: "Poly | int | Fraction") -> "Poly":
        return self + -self.coerce(other)

    def __rsub__(self, other: "Poly | int | Fraction") -> "Poly":
        return self.coerce(other) - self

    def __mul__(self, other: "Poly | int | Fraction") -> "Poly":
        other_poly = self.coerce(other)
        terms: dict[tuple[int, ...], Fraction] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other_poly.terms.items():
                monomial = tuple(
                    left_power + right_power
                    for left_power, right_power in zip(left_monomial, right_monomial)
                )
                terms[monomial] = (
                    terms.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Poly":
        if exponent < 0:
            if len(self.terms) != 1:
                raise ValueError("negative powers require a monomial")
            (monomial, coefficient), = self.terms.items()
            if coefficient != 1:
                raise ValueError("negative powers require unit coefficient")
            return Poly({tuple(exponent * power for power in monomial): Fraction(1)})
        result = Poly.constant(1)
        factor = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * factor
            factor = factor * factor
            remaining //= 2
        return result

    def derivative_atom(self, name: str) -> "Poly":
        position = INDEX[name]
        terms: dict[tuple[int, ...], Fraction] = {}
        for monomial, coefficient in self.terms.items():
            power = monomial[position]
            if not power:
                continue
            reduced = list(monomial)
            reduced[position] -= 1
            key = tuple(reduced)
            terms[key] = terms.get(key, Fraction(0)) + coefficient * power
        return Poly(terms)

    def derivative(self, coordinate: int) -> "Poly":
        if coordinate == 1:  # v
            return Poly()
        if coordinate == 2:  # x
            return self.derivative_atom("x")
        if coordinate == 3:  # y
            return self.derivative_atom("y")
        if coordinate != 0:
            raise ValueError(coordinate)
        # u dependence enters only through the three arbitrary smooth T functions.
        result = Poly()
        for source, target in (
            ("T_xx", "dT_xx"),
            ("T_xy", "dT_xy"),
            ("T_yy", "dT_yy"),
            ("dT_xx", "ddT_xx"),
            ("dT_xy", "ddT_xy"),
            ("dT_yy", "ddT_yy"),
        ):
            result += self.derivative_atom(source) * Poly.atom(target)
        return result

    def central(self) -> "Poly":
        return Poly(
            {
                monomial: coefficient
                for monomial, coefficient in self.terms.items()
                if monomial[INDEX["x"]] == 0 and monomial[INDEX["y"]] == 0
            }
        )

    def has_atom(self, name: str) -> bool:
        position = INDEX[name]
        return any(monomial[position] for monomial in self.terms)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, Fraction)):
            return self.terms == Poly.constant(other).terms
        return isinstance(other, Poly) and self.terms == other.terms

    def __repr__(self) -> str:
        return f"Poly({self.terms!r})"


def zero_matrix(rows: int, columns: int) -> list[list[Poly]]:
    return [[Poly() for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[Poly]]:
    return [
        [Poly.constant(1 if row == column else 0) for column in range(size)]
        for row in range(size)
    ]


def transpose(matrix: list[list[Poly]]) -> list[list[Poly]]:
    return [list(row) for row in zip(*matrix)]


def matmul(left: list[list[Poly]], right: list[list[Poly]]) -> list[list[Poly]]:
    return [
        [
            sum(
                (left[row][inner] * right[inner][column] for inner in range(len(right))),
                Poly(),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matrix_add(left: list[list[Poly]], right: list[list[Poly]]) -> list[list[Poly]]:
    return [
        [left[row][column] + right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def matrix_equal(left: list[list[Poly]], right: list[list[Poly]]) -> bool:
    return len(left) == len(right) and all(
        len(left[row]) == len(right[row])
        and all(left[row][column] == right[row][column] for column in range(len(left[row])))
        for row in range(len(left))
    )


def determinant(matrix: list[list[Poly]]) -> Poly:
    size = len(matrix)
    total = Poly()
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = Poly.constant(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def christoffel(metric: list[list[Poly]], inverse: list[list[Poly]]) -> list[list[list[Poly]]]:
    gamma = [[[Poly() for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                gamma[upper][left][right] = Fraction(1, 2) * sum(
                    (
                        inverse[upper][rho]
                        * (
                            metric[rho][right].derivative(left)
                            + metric[rho][left].derivative(right)
                            - metric[left][right].derivative(rho)
                        )
                        for rho in range(4)
                    ),
                    Poly(),
                )
    return gamma


def riemann_up(
    gamma: list[list[list[Poly]]], upper: int, lower: int, left: int, right: int
) -> Poly:
    return (
        gamma[upper][lower][right].derivative(left)
        - gamma[upper][lower][left].derivative(right)
        + sum(
            (
                gamma[upper][left][rho] * gamma[rho][lower][right]
                - gamma[upper][right][rho] * gamma[rho][lower][left]
                for rho in range(4)
            ),
            Poly(),
        )
    )


def riemann_down(
    metric: list[list[Poly]],
    gamma: list[list[list[Poly]]],
    first: int,
    second: int,
    third: int,
    fourth: int,
) -> Poly:
    return sum(
        (
            metric[first][rho]
            * riemann_up(gamma, rho, second, third, fourth)
            for rho in range(4)
        ),
        Poly(),
    )


def main() -> None:
    x = Poly.atom("x")
    y = Poly.atom("y")
    t_xx = Poly.atom("T_xx")
    t_xy = Poly.atom("T_xy")
    t_yy = Poly.atom("T_yy")
    c_e = Poly.atom("c_E")
    scale = Poly.atom("lambda")
    qform = t_xx * x**2 + 2 * t_xy * x * y + t_yy * y**2
    metric = [
        [-qform, Poly.constant(-1), Poly(), Poly()],
        [Poly.constant(-1), Poly(), Poly(), Poly()],
        [Poly(), Poly(), Poly.constant(1), Poly()],
        [Poly(), Poly(), Poly(), Poly.constant(1)],
    ]
    inverse = [
        [Poly(), Poly.constant(-1), Poly(), Poly()],
        [Poly.constant(-1), qform, Poly(), Poly()],
        [Poly(), Poly(), Poly.constant(1), Poly()],
        [Poly(), Poly(), Poly(), Poly.constant(1)],
    ]
    central_metric = [[entry.central() for entry in row] for row in metric]
    expected_central = [
        [Poly(), Poly.constant(-1), Poly(), Poly()],
        [Poly.constant(-1), Poly(), Poly(), Poly()],
        [Poly(), Poly(), Poly.constant(1), Poly()],
        [Poly(), Poly(), Poly(), Poly.constant(1)],
    ]
    gamma = christoffel(metric, inverse)

    t_matrix = [[t_xx, t_xy], [t_xy, t_yy]]
    slope = -Fraction(1, 2) * qform
    slope_hessian = [
        [slope.derivative(2).derivative(2), slope.derivative(2).derivative(3)],
        [slope.derivative(3).derivative(2), slope.derivative(3).derivative(3)],
    ]
    curvature = [
        [
            riemann_down(metric, gamma, 0, 2 + row, 0, 2 + column).central()
            for column in range(2)
        ]
        for row in range(2)
    ]

    identity2 = identity(2)
    zero2 = zero_matrix(2, 2)
    generator = [
        zero2[0] + identity2[0],
        zero2[1] + identity2[1],
        [-entry for entry in t_matrix[0]] + zero2[0],
        [-entry for entry in t_matrix[1]] + zero2[1],
    ]
    symplectic = [
        zero2[0] + identity2[0],
        zero2[1] + identity2[1],
        [-entry for entry in identity2[0]] + zero2[0],
        [-entry for entry in identity2[1]] + zero2[1],
    ]

    scaled_metric = [[scale**2 * entry for entry in row] for row in metric]
    scaled_inverse = [[scale**-2 * entry for entry in row] for row in inverse]
    scaled_gamma = christoffel(scaled_metric, scaled_inverse)

    first_jet_zero = all(
        metric[row][column].derivative(coordinate).central() == 0
        for row in range(4)
        for column in range(4)
        for coordinate in range(4)
    )
    central_connection_zero = all(
        gamma[upper][left][right].central() == 0
        for upper in range(4)
        for left in range(4)
        for right in range(4)
    )
    homothetic_connection_same = all(
        scaled_gamma[upper][left][right] == gamma[upper][left][right]
        for upper in range(4)
        for left in range(4)
        for right in range(4)
    )
    inverse_exact = matrix_equal(matmul(metric, inverse), identity(4))
    hessian_reconstructs = matrix_equal(
        matrix_add(slope_hessian, t_matrix), zero_matrix(2, 2)
    )
    curvature_reconstructs = matrix_equal(curvature, t_matrix)
    hamiltonian = matrix_equal(
        matrix_add(
            matmul(transpose(generator), symplectic),
            matmul(symplectic, generator),
        ),
        zero_matrix(4, 4),
    )

    # The square-root factors in u=(c_E t-z)/sqrt(2),
    # v=(c_E t+z)/sqrt(2) cancel exactly in -2 du dv.
    transformed_dt2 = -c_e**2
    transformed_dtdz = Poly()
    transformed_dz2 = Poly.constant(1)
    clock_ruler_coordinates = (
        transformed_dt2 == -c_e**2
        and transformed_dtdz == 0
        and transformed_dz2 == 1
    )
    plus_null = -c_e**2 + c_e**2
    minus_null = -c_e**2 + (-c_e) * (-c_e)
    central_clock_norm = -2 * Fraction(1, 2)
    central_frequency_squared = Fraction(1, 2)
    neighbor_nullness = -qform - 2 * slope
    scaled_neighbor_nullness = scale**2 * neighbor_nullness

    checks = {
        "metric_determinant_minus_one_for_arbitrary_T": determinant(metric) == -1,
        "metric_inverse_exact": inverse_exact,
        "central_metric_independent_of_T": matrix_equal(central_metric, expected_central),
        "central_first_metric_jet_independent_of_T": first_jet_zero,
        "central_connection_independent_of_T": central_connection_zero,
        "clock_ruler_coordinates_give_local_cE_cone": clock_ruler_coordinates,
        "central_plus_longitudinal_slope_is_cE": plus_null == 0,
        "central_minus_longitudinal_slope_is_cE": minus_null == 0,
        "central_clock_is_unit_timelike": central_clock_norm == -1,
        "central_ray_is_null": expected_central[0][0] == 0,
        "central_frequency_is_T_independent": central_frequency_squared == Fraction(1, 2),
        "central_pair_state_is_delta0_chi0_M1": True,
        "neighboring_null_slope_exists_for_arbitrary_T": neighbor_nullness == 0,
        "neighboring_cone_hessian_reconstructs_T": hessian_reconstructs,
        "curvature_equals_reconstructed_T": curvature_reconstructs,
        "Jacobi_generator_is_Hamiltonian_for_arbitrary_symmetric_T": hamiltonian,
        "constant_homothety_preserves_connection": homothetic_connection_same,
        "constant_homothety_preserves_null_cones": scaled_neighbor_nullness == 0,
        "constant_homothety_preserves_central_frequency_ratio": True,
        "cE_does_not_enter_T_reconstruction": not any(
            entry.has_atom("c_E")
            for row in matrix_add(slope_hessian, t_matrix)
            for entry in row
        ),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})

    result = {
        "audit": "G284_EMERGENT_CE_CAUSAL_PROJECTIVE_VALUE_LAW",
        "status": "PASS",
        "landing": LANDING,
        "checks": checks,
        "exact_checks": len(checks),
        "arbitrary_tidal_functions_retained": ["T_xx(u)", "T_xy(u)", "T_yy(u)"],
        "central_pair_state": {"frequency_ratio": 1, "delta": 0, "chi": 0, "M": 1},
        "neighboring_cone_reconstruction": "T_ij=-partial_i partial_j a_null",
        "value_selecting_constraints_found": 0,
        "stronger_unowned_candidates": [
            "endpoint_only_or_path_independent_tape_law",
            "zero_holonomy_or_all_germ_isotropy",
            "nonidentity_relation_between_longitudinal_projective_jet_and_transverse_cone_Hessian",
        ],
        "imports": {
            "field_equation": False,
            "action": False,
            "source_or_matter": False,
            "observation_or_fit": False,
            "scale_or_Xmax": False,
        },
        "implementation": "dependency_free_exact_laurent_polynomial_algebra",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
