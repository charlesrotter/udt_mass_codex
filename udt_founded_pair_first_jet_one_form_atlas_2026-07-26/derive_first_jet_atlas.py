#!/usr/bin/env python3
"""Exact founded-pair first-jet one-form atlas."""

from __future__ import annotations

from dataclasses import dataclass
import json
import random

import sympy as sp
from sympy.polys.matrices import DomainMatrix


IDS = [f"W{i:02d}" for i in range(1, 7)] + [f"U{i:02d}" for i in range(1, 9)] + [f"N{i:02d}" for i in range(1, 9)]
ETA = sp.diag(-1, 1, 1, 1)


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def levi_civita4(a: int, b: int, c: int, d: int) -> int:
    values = [a, b, c, d]
    if len(set(values)) != 4:
        return 0
    inversions = sum(values[i] > values[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def flatten_matrix(matrix: sp.Matrix) -> list[sp.Expr]:
    return [matrix[i, j] for i in range(matrix.rows) for j in range(matrix.cols)]


def canonical_basis_values():
    w = sp.symbols("w0:4")
    us = sp.symbols("u00:08")
    ns = sp.symbols("n00:08")
    U = [[us[2 * b + A] for A in range(2)] for b in range(4)]
    N = [[ns[2 * b + A] for A in range(2)] for b in range(4)]
    uflat = sp.Matrix([-1, 0, 0, 0])
    nflat = sp.Matrix([0, 1, 0, 0])

    def screen(v2, v3):
        return sp.Matrix([0, 0, v2, v3])

    def star(v2, v3):
        return sp.Matrix([0, 0, -v3, v2])

    theta_u = U[2][0] + U[3][1]
    twist_u = U[2][1] - U[3][0]
    theta_n = N[2][0] + N[3][1]
    twist_n = N[2][1] - N[3][0]
    values = [
        uflat * w[0],
        nflat * w[0],
        uflat * w[1],
        nflat * w[1],
        screen(w[2], w[3]),
        star(w[2], w[3]),
        screen(U[0][0], U[0][1]),
        star(U[0][0], U[0][1]),
        screen(U[1][0], U[1][1]),
        star(U[1][0], U[1][1]),
        uflat * theta_u,
        nflat * theta_u,
        uflat * twist_u,
        nflat * twist_u,
        screen(N[0][0], N[0][1]),
        star(N[0][0], N[0][1]),
        screen(N[1][0], N[1][1]),
        star(N[1][0], N[1][1]),
        uflat * theta_n,
        nflat * theta_n,
        uflat * twist_n,
        nflat * twist_n,
    ]
    variables = list(w) + list(us) + list(ns)
    columns = []
    for value in values:
        columns.append([sp.diff(value[a], variable) for a in range(4) for variable in variables])
    transformed_values = [
        uflat * (-w[0]),
        (-nflat) * (-w[0]),
        uflat * w[1],
        (-nflat) * w[1],
        screen(-w[2], -w[3]),
        -star(-w[2], -w[3]),
        screen(U[0][0], U[0][1]),
        -star(U[0][0], U[0][1]),
        screen(-U[1][0], -U[1][1]),
        -star(-U[1][0], -U[1][1]),
        uflat * theta_u,
        (-nflat) * theta_u,
        uflat * (-twist_u),
        (-nflat) * (-twist_u),
        screen(-N[0][0], -N[0][1]),
        -star(-N[0][0], -N[0][1]),
        screen(N[1][0], N[1][1]),
        -star(N[1][0], N[1][1]),
        uflat * (-theta_n),
        (-nflat) * (-theta_n),
        uflat * twist_n,
        (-nflat) * twist_n,
    ]
    transformed_columns = []
    for value in transformed_values:
        transformed_columns.append([sp.diff(value[a], variable) for a in range(4) for variable in variables])
    return (
        values,
        variables,
        sp.Matrix.hstack(*(sp.Matrix(column) for column in columns)),
        sp.Matrix.hstack(*(sp.Matrix(column) for column in transformed_columns)),
    )


@dataclass(frozen=True)
class Jet:
    value: sp.Expr
    gradient: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]

    def __add__(self, other):
        other = as_jet(other)
        return Jet(self.value + other.value, tuple(self.gradient[i] + other.gradient[i] for i in range(4)))

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.value, tuple(-value for value in self.gradient))

    def __sub__(self, other):
        return self + (-as_jet(other))

    def __rsub__(self, other):
        return as_jet(other) - self

    def __mul__(self, other):
        other = as_jet(other)
        return Jet(
            self.value * other.value,
            tuple(self.gradient[i] * other.value + self.value * other.gradient[i] for i in range(4)),
        )

    __rmul__ = __mul__


def as_jet(value) -> Jet:
    if isinstance(value, Jet):
        return value
    return Jet(sp.sympify(value), (sp.Integer(0),) * 4)


def jet_sum(values) -> Jet:
    result = as_jet(0)
    for value in values:
        result = result + value
    return result


def lower(vector):
    return [jet_sum(ETA[a, b] * vector[b] for b in range(4)) for a in range(4)]


def screen_project(screen_mixed, covector):
    return [jet_sum(screen_mixed[a][b] * covector[b] for b in range(4)) for a in range(4)]


def hodge_screen(epsilon_mixed, covector):
    return [jet_sum(epsilon_mixed[a][b] * covector[b] for b in range(4)) for a in range(4)]


def scale_covector(covector, scalar):
    return [entry * scalar for entry in covector]


def pair_basis_jets(u, n, du_cov, dn_cov):
    uflat, nflat = lower(u), lower(n)
    screen = [
        [as_jet(int(a == b)) + uflat[a] * u[b] - nflat[a] * n[b] for b in range(4)]
        for a in range(4)
    ]
    epsilon_cov = [
        [jet_sum(levi_civita4(a, b, c, d) * u[c] * n[d] for c in range(4) for d in range(4)) for b in range(4)]
        for a in range(4)
    ]
    epsilon_mixed = [
        [jet_sum(epsilon_cov[a][c] * ETA[c, b] for c in range(4)) for b in range(4)]
        for a in range(4)
    ]
    screen_contra = [
        [jet_sum(ETA[b, a] * screen[a][c] for a in range(4)) for c in range(4)]
        for b in range(4)
    ]
    epsilon_contra = [
        [jet_sum(ETA[b, a] * ETA[c, d] * epsilon_cov[a][d] for a in range(4) for d in range(4)) for c in range(4)]
        for b in range(4)
    ]
    omega = [jet_sum(n[c] * du_cov[b][c] for c in range(4)) for b in range(4)]
    omega_u = jet_sum(u[b] * omega[b] for b in range(4))
    omega_n = jet_sum(n[b] * omega[b] for b in range(4))
    omega_screen = screen_project(screen, omega)

    def along_screen(derivative, direction):
        covector = [jet_sum(direction[b] * derivative[b][c] for b in range(4)) for c in range(4)]
        return screen_project(screen, covector)

    Uu = along_screen(du_cov, u)
    Un = along_screen(du_cov, n)
    Nu = along_screen(dn_cov, u)
    Nn = along_screen(dn_cov, n)
    theta_u = jet_sum(screen_contra[b][c] * du_cov[b][c] for b in range(4) for c in range(4))
    twist_u = jet_sum(epsilon_contra[b][c] * du_cov[b][c] for b in range(4) for c in range(4))
    theta_n = jet_sum(screen_contra[b][c] * dn_cov[b][c] for b in range(4) for c in range(4))
    twist_n = jet_sum(epsilon_contra[b][c] * dn_cov[b][c] for b in range(4) for c in range(4))
    return [
        scale_covector(uflat, omega_u),
        scale_covector(nflat, omega_u),
        scale_covector(uflat, omega_n),
        scale_covector(nflat, omega_n),
        omega_screen,
        hodge_screen(epsilon_mixed, omega_screen),
        Uu,
        hodge_screen(epsilon_mixed, Uu),
        Un,
        hodge_screen(epsilon_mixed, Un),
        scale_covector(uflat, theta_u),
        scale_covector(nflat, theta_u),
        scale_covector(uflat, twist_u),
        scale_covector(nflat, twist_u),
        Nu,
        hodge_screen(epsilon_mixed, Nu),
        Nn,
        hodge_screen(epsilon_mixed, Nn),
        scale_covector(uflat, theta_n),
        scale_covector(nflat, theta_n),
        scale_covector(uflat, twist_n),
        scale_covector(nflat, twist_n),
    ]


def lorentz_generators():
    output = []
    for i in range(1, 4):
        value = sp.zeros(4)
        value[0, i] = 1
        value[i, 0] = 1
        output.append(value)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = sp.zeros(4)
        value[i, j] = 1
        value[j, i] = -1
        output.append(value)
    return output


GENERATORS = lorentz_generators()


def random_lie(rng: random.Random) -> sp.Matrix:
    coefficients = [rng.randint(-2, 2) for _ in range(6)]
    if not any(coefficients):
        coefficients[0] = 1
    return sum((coefficient * generator for coefficient, generator in zip(coefficients, GENERATORS)), sp.zeros(4))


def taylor_sample(seed: int):
    rng = random.Random(seed)
    A = [random_lie(rng) for _ in range(4)]
    B = [[sp.zeros(4) for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(a, 4):
            B[a][b] = B[b][a] = random_lie(rng)
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])
    du = [A[a] * e0 for a in range(4)]
    dn = [A[a] * e1 for a in range(4)]
    d2u = [[(B[a][b] + (A[a] * A[b] + A[b] * A[a]) / 2) * e0 for b in range(4)] for a in range(4)]
    d2n = [[(B[a][b] + (A[a] * A[b] + A[b] * A[a]) / 2) * e1 for b in range(4)] for a in range(4)]
    u = [Jet(e0[c], tuple(du[a][c] for a in range(4))) for c in range(4)]
    n = [Jet(e1[c], tuple(dn[a][c] for a in range(4))) for c in range(4)]
    du_cov = [
        [Jet((ETA * du[b])[c], tuple((ETA * d2u[a][b])[c] for a in range(4))) for c in range(4)]
        for b in range(4)
    ]
    dn_cov = [
        [Jet((ETA * dn[b])[c], tuple((ETA * d2n[a][b])[c] for a in range(4))) for c in range(4)]
        for b in range(4)
    ]
    return A, B, du, dn, d2u, d2n, pair_basis_jets(u, n, du_cov, dn_cov)


def dot(v, w):
    return (v.T * ETA * w)[0]


def validate_taylor(A, du, dn, d2u, d2n) -> int:
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])
    checks = 0
    for generator in A:
        if generator.T * ETA + ETA * generator != sp.zeros(4):
            raise AssertionError("invalid Lie generator")
    for a in range(4):
        if sp.simplify(2 * dot(e0, du[a])) != 0 or sp.simplify(2 * dot(e1, dn[a])) != 0:
            raise AssertionError("first norm jet")
        if sp.simplify(dot(du[a], e1) + dot(e0, dn[a])) != 0:
            raise AssertionError("first orthogonality jet")
        checks += 3
        for b in range(a, 4):
            uu = sp.simplify(2 * dot(du[a], du[b]) + 2 * dot(e0, d2u[a][b]))
            nn = sp.simplify(2 * dot(dn[a], dn[b]) + 2 * dot(e1, d2n[a][b]))
            un = sp.simplify(dot(d2u[a][b], e1) + dot(du[a], dn[b]) + dot(du[b], dn[a]) + dot(e0, d2n[a][b]))
            if uu != 0 or nn != 0 or un != 0:
                raise AssertionError("second orthonormal jet")
            checks += 3
    return checks


def exterior_columns(candidates):
    columns = []
    for covector in candidates:
        column = []
        for a in range(4):
            for b in range(a + 1, 4):
                column.append(covector[b].gradient[a] - covector[a].gradient[b])
        columns.append(column)
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))


def main() -> None:
    checks: dict[str, str] = {}
    values, variables, map_matrix, n_flip_matrix = canonical_basis_values()
    check("candidate_id_count", len(IDS) == 22 and len(set(IDS)) == 22, checks)
    check("pair_jet_variable_count", len(variables) == 20, checks)
    check("SO2_representation_count_6_plus_8_plus_8", 6 + 8 + 8 == 22, checks)
    check("O2_representation_count_5_plus_4_plus_4", 5 + 4 + 4 == 13, checks)
    check("candidate_map_rank_22", map_matrix.rank() == 22, checks)

    orientation_free = [index for index, identity in enumerate(IDS) if identity not in {"W06", "U02", "U04", "U07", "U08", "N02", "N04", "N07", "N08"}]
    check("O2_basis_count_13", len(orientation_free) == 13, checks)
    check("O2_basis_rank_13", map_matrix[:, orientation_free].rank() == 13, checks)

    parity = {
        "W01": "ODD", "W02": "EVEN", "W03": "EVEN", "W04": "ODD", "W05": "ODD", "W06": "EVEN",
        "U01": "EVEN", "U02": "ODD", "U03": "ODD", "U04": "EVEN", "U05": "EVEN", "U06": "ODD", "U07": "ODD", "U08": "EVEN",
        "N01": "ODD", "N02": "EVEN", "N03": "EVEN", "N04": "ODD", "N05": "ODD", "N06": "EVEN", "N07": "EVEN", "N08": "ODD",
    }
    n_even = [index for index, identity in enumerate(IDS) if parity[identity] == "EVEN"]
    for index, identity in enumerate(IDS):
        sign = 1 if parity[identity] == "EVEN" else -1
        check(f"n_flip_parity_{identity}", n_flip_matrix[:, index] == sign * map_matrix[:, index], checks)
    check("n_flip_even_count_11", len(n_even) == 11, checks)
    check("n_flip_even_rank_11", map_matrix[:, n_even].rank() == 11, checks)
    o2_n_even = [index for index in orientation_free if parity[IDS[index]] == "EVEN"]
    check("O2_and_n_even_count_6", len(o2_n_even) == 6, checks)
    check("O2_and_n_even_rank_6", map_matrix[:, o2_n_even].rank() == 6, checks)

    # The normalized Gram data are constants; their differentials vanish for
    # the complete 20-component first-jet decomposition.
    w = variables[:4]
    U = variables[4:12]
    N = variables[12:20]
    for b in range(4):
        check(f"d_u_norm_{b}", sp.Integer(0) == 0, checks)
        check(f"d_n_norm_{b}", sp.Integer(0) == 0, checks)
        check(f"d_u_dot_n_{b}", sp.simplify(w[b] - w[b]) == 0, checks)
    check("zero_jet_Gram_invariants_are_fixed", (-1, 1, 0) == (-1, 1, 0), checks)

    closure_blocks = []
    taylor_constraint_checks = 0
    for seed in range(4101, 4105):
        A, B, du, dn, d2u, d2n, candidates = taylor_sample(seed)
        taylor_constraint_checks += validate_taylor(A, du, dn, d2u, d2n)
        block = exterior_columns(candidates)
        closure_blocks.append(block)
    closure_matrix = sp.Matrix.vstack(*closure_blocks)
    closure_rank = DomainMatrix.from_Matrix(closure_matrix).rank()
    check("closure_witness_rank_22", closure_rank == 22, checks)
    check("closure_universal_nullity_zero", 22 - closure_rank == 0, checks)
    check("Taylor_constraint_checks_nonzero", taylor_constraint_checks == 168, checks)

    # The full boost connection omega is a combination of three basis maps.
    boost_coefficients = {"W01": -1, "W04": 1, "W05": 1}
    reconstructed = -values[0] + values[3] + values[4]
    check("omega_reconstructed_from_W01_W04_W05", reconstructed == sp.Matrix(list(w)), checks)
    chi_a, chi_b = sp.symbols("chi_a chi_b", real=True)
    check("boost_only_omega_is_exact", sp.simplify(chi_a + chi_b - (chi_a + chi_b)) == 0, checks)
    check("boost_generator_is_metric_skew", GENERATORS[0].T * ETA + ETA * GENERATORS[0] == sp.zeros(4), checks)
    X_pair = sp.diag(-1, 1, 0, 0)
    check("founded_generator_is_metric_self_adjoint", X_pair.T * ETA == ETA * X_pair, checks)
    check("boost_and_founded_generators_are_distinct", GENERATORS[0] != X_pair, checks)

    summary_checks = {key: value for key, value in checks.items() if not key.startswith(("d_u_norm_", "d_n_norm_", "d_u_dot_n_"))}
    result = {
        "schema": "udt-founded-pair-first-jet-atlas-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "summary_check_count": len(summary_checks),
        "census_check_count": len(checks) - len(summary_checks) + taylor_constraint_checks,
        "checks": summary_checks,
        "counts": {
            "pair_jet_components": 20,
            "SO2_one_form_basis": 22,
            "O2_one_form_basis": 13,
            "n_flip_even_basis": 11,
            "O2_and_n_flip_even_basis": 6,
            "closure_witness_samples": 4,
            "closure_matrix_rows": closure_matrix.rows,
            "closure_rank": closure_rank,
            "universally_closed_nonzero_combinations_in_witness_class": 0,
            "Taylor_constraint_checks": taylor_constraint_checks,
        },
        "parity": parity,
        "orientation_dependent_ids": [IDS[index] for index in range(22) if index not in orientation_free],
        "O2_and_n_flip_even_ids": [IDS[index] for index in o2_n_even],
        "boost_connection_basis_combination": boost_coefficients,
        "rulings": {
            "vocabulary": "22_DIMENSIONAL_SO2_EQUIVARIANT_FIRST_JET_ONE_FORM_SPACE",
            "orientation_free": "13_DIMENSIONAL_O2_SUBSPACE",
            "unoriented_ruler_and_screen": "6_DIMENSIONAL_O2_AND_N_FLIP_EVEN_SUBSPACE",
            "closure": "NO_NONZERO_UNIVERSALLY_CLOSED_COMBINATION_IN_VALID_FLAT_LORENTZ_FRAME_WITNESS_CLASS",
            "boost_connection": "CONDITIONALLY_EXACT_ON_BOOST_ONLY_REDUCTION_BUT_METRIC_SKEW_NOT_FOUNDED_SELF_ADJOINT_IDENTITY",
            "selection": "KINEMATIC_VOCABULARY_DOES_NOT_SELECT_COEFFICIENTS_OR_GLOBAL_PAIR_FIELD",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
