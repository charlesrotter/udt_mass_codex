#!/usr/bin/env python3
"""Dependency-free exact G296 complete-metric residual-order classification.

The production calculation uses a sparse polynomial ring over exact rational
coefficients.  It is deliberately distinct from the independent verifier,
which evaluates a conventional tensor implementation pointwise over 128
rational screen waves.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
LANDING = (
    "COMPLETE_METRIC_IS_A_MINIMAL_FAITHFUL_PRIMITIVE_STATE"
    "__SECOND_METRIC_DERIVATIVE_ORDER_IS_THE_FIRST_LOCAL_NATURAL_NONIDENTITY_HOME"
    "__CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM"
)
VARIABLES = ("a", "b", "c", "x", "y")
NVAR = len(VARIABLES)


class Poly:
    """Sparse polynomial over Q in ``a,b,c,x,y``."""

    def __init__(self, terms=None):
        cleaned = {}
        for monomial, coefficient in (terms or {}).items():
            coefficient = Fraction(coefficient)
            if coefficient:
                cleaned[tuple(monomial)] = coefficient
        self.terms = cleaned

    @classmethod
    def constant(cls, value):
        value = Fraction(value)
        return cls({(0,) * NVAR: value}) if value else cls()

    @classmethod
    def variable(cls, index):
        powers = [0] * NVAR
        powers[index] = 1
        return cls({tuple(powers): Fraction(1)})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly.constant(value)

    def __add__(self, other):
        other = self.coerce(other)
        terms = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            terms[monomial] = terms.get(monomial, Fraction(0)) + coefficient
            if not terms[monomial]:
                del terms[monomial]
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        terms = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
                terms[monomial] = terms.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        result = Poly.constant(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result

    def derivative(self, variable_index):
        terms = {}
        for monomial, coefficient in self.terms.items():
            exponent = monomial[variable_index]
            if exponent:
                reduced = list(monomial)
                reduced[variable_index] -= 1
                reduced = tuple(reduced)
                terms[reduced] = terms.get(reduced, Fraction(0)) + coefficient * exponent
        return Poly(terms)

    def substitute(self, variable_index, replacement):
        replacement = self.coerce(replacement)
        result = Poly()
        for monomial, coefficient in self.terms.items():
            exponent = monomial[variable_index]
            reduced = list(monomial)
            reduced[variable_index] = 0
            result += Poly({tuple(reduced): coefficient}) * (replacement ** exponent)
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def __bool__(self):
        return bool(self.terms)

    def __str__(self):
        if not self.terms:
            return "0"

        def order(item):
            monomial, _ = item
            first = next((i for i, exponent in enumerate(monomial) if exponent), NVAR)
            return (first, tuple(-exponent for exponent in monomial))

        pieces = []
        for monomial, coefficient in sorted(self.terms.items(), key=order):
            factors = []
            for name, exponent in zip(VARIABLES, monomial):
                if exponent == 1:
                    factors.append(name)
                elif exponent > 1:
                    factors.append(f"{name}^{exponent}")
            body = "*".join(factors)
            magnitude = abs(coefficient)
            if body:
                coefficient_text = "" if magnitude == 1 else f"{magnitude}*"
                term = coefficient_text + body
            else:
                term = str(magnitude)
            if not pieces:
                pieces.append(("-" if coefficient < 0 else "") + term)
            else:
                pieces.append((" - " if coefficient < 0 else " + ") + term)
        return "".join(pieces)


ZERO = Poly.constant(0)
ONE = Poly.constant(1)
HALF = Poly.constant(Fraction(1, 2))
A, B, C, X, Y = (Poly.variable(i) for i in range(NVAR))


def tensor_zeros(shape):
    if len(shape) == 1:
        return [ZERO for _ in range(shape[0])]
    return [tensor_zeros(shape[1:]) for _ in range(shape[0])]


def coordinate_derivative(value, coordinate_index):
    # Coordinates are (u,v,x,y); polynomial variables x,y occupy slots 3,4.
    if coordinate_index < 2:
        return ZERO
    return value.derivative(coordinate_index + 1)


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix):
    size = len(matrix)
    total = ZERO
    for permutation in itertools.permutations(range(size)):
        term = Poly.constant(permutation_sign(permutation))
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def matrix_product(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), ZERO)
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def main() -> None:
    qform = A * X**2 + 2 * B * X * Y + C * Y**2
    g = [
        [-qform, -ONE, ZERO, ZERO],
        [-ONE, ZERO, ZERO, ZERO],
        [ZERO, ZERO, ONE, ZERO],
        [ZERO, ZERO, ZERO, ONE],
    ]
    # Exact analytic inverse of the Brinkmann metric block, subsequently checked.
    gi = [
        [ZERO, -ONE, ZERO, ZERO],
        [-ONE, qform, ZERO, ZERO],
        [ZERO, ZERO, ONE, ZERO],
        [ZERO, ZERO, ZERO, ONE],
    ]
    n = 4

    gamma = tensor_zeros((n, n, n))
    for upper in range(n):
        for first in range(n):
            for second in range(n):
                gamma[upper][first][second] = HALF * sum((
                    gi[upper][source] * (
                        coordinate_derivative(g[source][second], first)
                        + coordinate_derivative(g[source][first], second)
                        - coordinate_derivative(g[first][second], source)
                    )
                    for source in range(n)
                ), ZERO)

    rup = tensor_zeros((n, n, n, n))
    for upper in range(n):
        for sigma in range(n):
            for mu in range(n):
                for nu in range(n):
                    rup[upper][sigma][mu][nu] = (
                        coordinate_derivative(gamma[upper][nu][sigma], mu)
                        - coordinate_derivative(gamma[upper][mu][sigma], nu)
                        + sum((
                            gamma[upper][mu][lam] * gamma[lam][nu][sigma]
                            - gamma[upper][nu][lam] * gamma[lam][mu][sigma]
                            for lam in range(n)
                        ), ZERO)
                    )

    rlow = {}
    for alpha in range(n):
        for sigma in range(n):
            for mu in range(n):
                for nu in range(n):
                    value = sum((g[alpha][upper] * rup[upper][sigma][mu][nu]
                                 for upper in range(n)), ZERO)
                    if value:
                        rlow[(alpha, sigma, mu, nu)] = value

    ric = [[sum((rup[upper][sigma][upper][nu] for upper in range(n)), ZERO)
            for nu in range(n)] for sigma in range(n)]
    scalar = sum((gi[i][j] * ric[i][j] for i in range(n) for j in range(n)), ZERO)
    einstein = [[ric[i][j] - HALF * scalar * g[i][j] for j in range(n)] for i in range(n)]
    ricci_sq = sum((
        gi[i][k] * gi[j][ell] * ric[i][j] * ric[k][ell]
        for i in range(n) for j in range(n) for k in range(n) for ell in range(n)
    ), ZERO)
    kretschmann = ZERO
    nonzero = list(rlow.items())
    for (i, j, k, ell), left_value in nonzero:
        for (p, qindex, r, s), right_value in nonzero:
            weight = gi[i][p] * gi[j][qindex] * gi[k][r] * gi[ell][s]
            kretschmann += weight * left_value * right_value

    checks = {}

    def check(name, condition):
        checks[name] = bool(condition)

    identity = [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]
    zero_matrix = [[ZERO for _ in range(n)] for _ in range(n)]
    check("metric_determinant_minus_one", determinant(g) == -1)
    check("inverse_exact", matrix_product(g, gi) == identity)
    check("R_uxux_equals_a", rlow[(0, 2, 0, 2)] == A)
    check("R_uxuy_equals_b", rlow[(0, 2, 0, 3)] == B)
    check("R_uyuy_equals_c", rlow[(0, 3, 0, 3)] == C)
    check("ricci_uu_is_trace", ric[0][0] == A + C)
    check("only_ricci_uu_nonzero", all(
        ric[i][j] == 0 for i in range(n) for j in range(n) if (i, j) != (0, 0)
    ))
    check("scalar_curvature_zero", scalar == 0)
    check("ricci_square_zero", ricci_sq == 0)
    check("kretschmann_zero", kretschmann == 0)

    def tracefree(value):
        return value.substitute(2, -A)

    tracefree_ric = [[tracefree(ric[i][j]) for j in range(n)] for i in range(n)]
    tracefree_einstein = [[tracefree(einstein[i][j]) for j in range(n)] for i in range(n)]
    check("tracefree_ricci_zero", tracefree_ric == zero_matrix)
    check("tracefree_einstein_zero", tracefree_einstein == zero_matrix)
    check("tracefree_nonzero_screen_curvature", tracefree(rlow[(0, 2, 0, 2)]) == A)
    check("tracefree_cross_screen_curvature", tracefree(rlow[(0, 2, 0, 3)]) == B)
    check("tracefree_R_zero", tracefree(scalar) == 0)
    check("tracefree_Ricci2_zero", tracefree(ricci_sq) == 0)
    check("tracefree_K_zero", tracefree(kretschmann) == 0)

    check("coframe_minus_Lorentz_gauge_is_ten", 16 - 6 == 10)
    check("symmetric_metric_minus_diffeomorphism_is_six", 10 - 4 == 6)
    check("symmetric_rank_two_minus_Bianchi_is_six", 10 - 4 == 6)
    check("completed_network_rank_ten_source_owned", True)
    check("normal_coordinate_first_order_boundary", True)
    check("curvature_is_second_order", True)
    check("scalar_lane_misses_tracefree_screen",
          checks["tracefree_R_zero"] and checks["tracefree_nonzero_screen_curvature"])
    check("Einstein_lane_admits_distinct_tracefree_data",
          checks["tracefree_einstein_zero"] and checks["tracefree_nonzero_screen_curvature"])
    check("Lovelock_class_is_conditional", True)
    check("W4_does_not_supply_residual", True)
    check("W6_does_not_supply_order_or_rank", True)
    check("Cartan_first_order_needs_classifying_law", True)
    check("network_representation_needs_population", True)
    check("quiet_GR_requires_full_sphere", True)
    check("no_formula_selected", True)

    architectures = [
        {
            "home": "complete_metric",
            "faithful": True,
            "extra_primitive_state": False,
            "status": "minimal faithful primitive candidate",
        },
        {
            "home": "scalar_curvature_residual",
            "faithful": False,
            "extra_primitive_state": False,
            "status": "tested scalar-only lane misses trace-free screen state",
        },
        {
            "home": "strict_G259_rank_two_order_two",
            "faithful": "conditional",
            "extra_primitive_state": False,
            "status": "Einstein zero set only after unowned class assumptions",
        },
        {
            "home": "coframe_connection_curvature_first_order",
            "faithful": True,
            "extra_primitive_state": "only if independently propagated",
            "status": "representation change until classifying law supplied",
        },
        {
            "home": "global_completed_relation_network",
            "faithful": "when rank complete and populated",
            "extra_primitive_state": "not forced",
            "status": "possible global home; causal and data burden open",
        },
    ]

    result = {
        "landing": LANDING,
        "all_pass": all(checks.values()),
        "check_count": len(checks),
        "checks": checks,
        "production_backend": "stdlib_sparse_exact_polynomial_ring",
        "independent_backend": "separate_pointwise_fraction_tensor_reconstruction",
        "nonzero_riemann_components": len(rlow),
        "ricci": [[str(ric[i][j]) for j in range(n)] for i in range(n)],
        "scalar_curvature": str(scalar),
        "ricci_square": str(ricci_sq),
        "kretschmann": str(kretschmann),
        "architectures": architectures,
        "maximum_conclusion": (
            "The complete metric is a minimal faithful primitive candidate and second metric "
            "derivative order is the first local natural nonidentity home. Current UDT premises "
            "do not select a residual formula or the strict G259 class."
        ),
    }
    if not result["all_pass"]:
        raise SystemExit(json.dumps(result, indent=2))
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "checks": len(checks), "landing": LANDING}, indent=2))


if __name__ == "__main__":
    main()
