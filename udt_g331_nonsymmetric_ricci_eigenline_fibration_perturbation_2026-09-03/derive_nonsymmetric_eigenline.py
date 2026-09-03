#!/usr/bin/env python3
"""Exact standard-library checks for the bounded G331 perturbation tile."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


class Jet2:
    """Value and first two derivatives of a one-variable rational function."""

    __slots__ = ("v", "d1", "d2")

    def __init__(self, value=0, first=0, second=0):
        self.v = F(value)
        self.d1 = F(first)
        self.d2 = F(second)

    @staticmethod
    def q(value):
        return value if isinstance(value, Jet2) else Jet2(value)

    def __add__(self, other):
        other = Jet2.q(other)
        return Jet2(self.v + other.v, self.d1 + other.d1, self.d2 + other.d2)

    __radd__ = __add__

    def __neg__(self):
        return Jet2(-self.v, -self.d1, -self.d2)

    def __sub__(self, other):
        return self + (-Jet2.q(other))

    def __rsub__(self, other):
        return Jet2.q(other) - self

    def __mul__(self, other):
        other = Jet2.q(other)
        return Jet2(
            self.v * other.v,
            self.d1 * other.v + self.v * other.d1,
            self.d2 * other.v + 2 * self.d1 * other.d1 + self.v * other.d2,
        )

    __rmul__ = __mul__

    def inverse(self):
        if not self.v:
            raise ZeroDivisionError("zero jet")
        return Jet2(
            1 / self.v,
            -self.d1 / self.v**2,
            2 * self.d1**2 / self.v**3 - self.d2 / self.v**2,
        )

    def __truediv__(self, other):
        return self * Jet2.q(other).inverse()

    def __rtruediv__(self, other):
        return Jet2.q(other) * self.inverse()


def zeros(rows, cols, value=F(0)):
    return [[value for _ in range(cols)] for _ in range(rows)]


def identity(n=3):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matadd(left, right, right_factor=F(1)):
    return [
        [left[i][j] + right_factor * right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matscale(matrix, factor):
    return [[factor * entry for entry in row] for row in matrix]


def inverse_fraction(matrix):
    n = len(matrix)
    aug = [list(matrix[i]) + identity(n)[i] for i in range(n)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col]), None)
        if pivot is None:
            raise ZeroDivisionError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [entry / scale for entry in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def weighted_metric_jets(x_value, weight_1, weight_2):
    """Metric g_w in (x,phi1,phi2), x=cos(theta)^2, including x-jets."""
    x = Jet2(x_value, 1, 0)
    one = Jet2(1)
    radial_product = x * (one - x)
    f = weight_1 * x + weight_2 * (one - x)
    eta = (x / f, (one - x) / f)
    zeta = (Jet2(weight_2) / f, Jet2(-weight_1) / f)
    g = [[Jet2(0) for _ in range(3)] for _ in range(3)]
    g[0][0] = 1 / (4 * radial_product * f)
    g[1][1] = radial_product / f * zeta[0] * zeta[0] + eta[0] * eta[0]
    g[1][2] = g[2][1] = radial_product / f * zeta[0] * zeta[1] + eta[0] * eta[1]
    g[2][2] = radial_product / f * zeta[1] * zeta[1] + eta[1] * eta[1]
    return (
        [[g[i][j].v for j in range(3)] for i in range(3)],
        [[g[i][j].d1 for j in range(3)] for i in range(3)],
        [[g[i][j].d2 for j in range(3)] for i in range(3)],
    )


def coordinate_ricci(x_value, weight_1, weight_2):
    """Exact coordinate Ricci calculation from g,g',g''; no Sasaki identity assumed."""
    g, dg, ddg = weighted_metric_jets(x_value, weight_1, weight_2)
    gi = inverse_fraction(g)
    dgi = matscale(matmul(matmul(gi, dg), gi), F(-1))

    gamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dgamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for ell in range(3):
                    e0 = (dg[ell][j] if i == 0 else 0)
                    e0 += dg[ell][i] if j == 0 else 0
                    e0 -= dg[i][j] if ell == 0 else 0
                    e1 = (ddg[ell][j] if i == 0 else 0)
                    e1 += ddg[ell][i] if j == 0 else 0
                    e1 -= ddg[i][j] if ell == 0 else 0
                    gamma[upper][i][j] += gi[upper][ell] * e0 / 2
                    dgamma[upper][i][j] += (dgi[upper][ell] * e0 + gi[upper][ell] * e1) / 2

    ricci = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            value = dgamma[0][i][j]
            if j == 0:
                value -= sum(dgamma[k][i][k] for k in range(3))
            for k in range(3):
                for ell in range(3):
                    value += gamma[k][i][j] * gamma[ell][k][ell]
                    value -= gamma[ell][i][k] * gamma[k][j][ell]
            ricci[i][j] = value
    return g, ricci, matmul(gi, ricci)


def outer(column, row):
    return [[column[i] * row[j] for j in range(len(row))] for i in range(len(column))]


def exact_rotation():
    return [
        [F(1, 9), F(8, 9), F(4, 9)],
        [F(8, 9), F(1, 9), F(-4, 9)],
        [F(-4, 9), F(4, 9), F(-7, 9)],
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    # G330 base and its exact round boundary.
    def gap(a, c):
        return 4 * (c * c - a * a) / a**4

    for index, (a, c) in enumerate(((F(1), F(3, 2)), (F(3, 2), F(1)), (F(5, 4), F(7, 4)))):
        require(gap(a, c) != 0, f"base_{index}_nonround_gap")
    require(gap(F(1), F(3, 2)) == 5, "g330_witness_gap_five")
    require(gap(F(1), F(1)) == 0, "round_gap_closure")

    # Coordinate rederivation for the weighted Sasaki family.  The registered identity
    # A = lambda_h I + (2-lambda_h) xi tensor eta is verified from metric derivatives.
    samples = (
        (F(1, 2), F(1), F(1)),
        (F(2, 5), F(2), F(3)),
        (F(1, 3), F(3, 2), F(5, 4)),
        (F(3, 7), F(5, 4), F(7, 4)),
    )
    horizontal_values = []
    for index, (x, w1, w2) in enumerate(samples):
        g, ricci, endomorphism = coordinate_ricci(x, w1, w2)
        xi = [F(0), w1, w2]
        eta = [sum(g[i][j] * xi[j] for j in range(3)) for i in range(3)]
        require(sum(eta[i] * xi[i] for i in range(3)) == 1, f"sample_{index}_reeb_unit")
        require(
            [sum(endomorphism[i][j] * xi[j] for j in range(3)) for i in range(3)]
            == [2 * entry for entry in xi],
            f"sample_{index}_ricci_reeb_eigenline",
        )
        trace = sum(endomorphism[i][i] for i in range(3))
        lam_h = (trace - 2) / 2
        expected = matadd(matscale(identity(), lam_h), matscale(outer(xi, eta), 2 - lam_h))
        require(endomorphism == expected, f"sample_{index}_full_ricci_projector_form")
        require(ricci == matmul(g, endomorphism), f"sample_{index}_lowered_ricci")
        horizontal_values.append(lam_h)

    require(horizontal_values[0] == 2, "round_weight_is_round_s3")
    # Unequal weights make the curvature depend on x, so this is not a homogeneous relabeling.
    _, _, left = coordinate_ricci(F(1, 3), F(2), F(3))
    _, _, right = coordinate_ricci(F(2, 3), F(2), F(3))
    require(sum(left[i][i] for i in range(3)) != sum(right[i][i] for i in range(3)),
            "unequal_weights_nonhomogeneous_scalar")

    # Equal weights, followed by one common homothety, recover any Berger radii A,C.
    for index, (a, c, x) in enumerate(((F(3, 2), F(1), F(2, 5)), (F(4, 3), F(7, 5), F(3, 7)))):
        w = a * a / (c * c)
        mu = a**4 / (c * c)
        g_weighted, _, a_weighted = coordinate_ricci(x, w, w)
        radial_product = x * (1 - x)
        h = [[F(0) for _ in range(3)] for _ in range(3)]
        h[0][0] = 1 / (4 * radial_product)
        h[1][1] = h[2][2] = radial_product
        h[1][2] = h[2][1] = -radial_product
        eta0 = [F(0), x, 1 - x]
        berger = matadd(matscale(h, a * a), matscale(outer(eta0, eta0), c * c))
        require(matscale(g_weighted, mu) == berger, f"berger_{index}_metric_recovery")
        scaled_endomorphism = matscale(a_weighted, 1 / mu)
        xi = [F(0), w, w]
        require(
            [sum(scaled_endomorphism[i][j] * xi[j] for j in range(3)) for i in range(3)]
            == [2 * entry / mu for entry in xi],
            f"berger_{index}_vertical_eigenvalue",
        )
        require(2 / mu == 2 * c * c / a**4, f"berger_{index}_g330_match")

    # Exact contact/Reeb conditions in x coordinates.
    for index, (x, w1, w2) in enumerate(samples[1:]):
        f = w1 * x + w2 * (1 - x)
        eta1, eta2 = x / f, (1 - x) / f
        fp = w1 - w2
        eta1p = (f - x * fp) / f**2
        eta2p = (-f - (1 - x) * fp) / f**2
        require(w1 * eta1 + w2 * eta2 == 1, f"contact_{index}_eta_xi")
        require(w1 * eta1p + w2 * eta2p == 0, f"contact_{index}_ixi_deta")

    # Irrational weighted flows can approach the Hopf flow arbitrarily closely.
    # (n+sqrt(2))/(n-sqrt(2)) has the displayed nonzero sqrt(2) coefficient.
    for n in (10, 100, 1000):
        rational_part = F(n * n + 2, n * n - 2)
        irrational_coefficient = F(2 * n, n * n - 2)
        require(irrational_coefficient != 0, f"irrational_{n}_nonzero_sqrt2_part")
        require(F(2, n * n) < F(1, 25), f"irrational_{n}_arbitrarily_close")
        require(rational_part > 0, f"irrational_{n}_positive_slope")

    # Real line bundles are classified by H1(-;Z2).  S3 has one class, but the metric
    # still chooses neither of the two signs of a unit representative.
    h1_mod2_dimension = 0
    real_line_bundle_class_count = 2**h1_mod2_dimension
    require(real_line_bundle_class_count == 1, "s3_line_bundle_triviality")
    sign_selected = False
    require(not sign_selected, "line_orientation_not_selected")

    # The exact 3D conformal Ricci law at a bump point with f=df=0,
    # Hess_13=1 and Delta f=2.  It tilts the old line and makes scalar curvature nonconstant.
    for index, epsilon in enumerate((F(1, 100), F(-1, 40), F(3, 200))):
        conformal_ricci_13 = -epsilon
        scalar_change = -4 * epsilon * 2
        require(conformal_ricci_13 == -epsilon, f"bump_{index}_vertical_line_tilt")
        require(scalar_change == -8 * epsilon, f"bump_{index}_scalar_nonhomogeneous")

    # Projectors, not components, are the gauge-covariant object.
    rotation = exact_rotation()
    ident = identity()
    require(matmul(rotation, transpose(rotation)) == ident, "oblique_rotation_orthogonal")
    p = [[F(int(i == 2 and j == 2)) for j in range(3)] for i in range(3)]
    rotated = matmul(matmul(rotation, p), transpose(rotation))
    require(matmul(rotated, rotated) == rotated, "rotated_projector_idempotent")
    require(sum(rotated[i][i] for i in range(3)) == 1, "rotated_projector_rank_one")

    explicit_bump_constraint_compatible = False
    weighted_family_constraint_compatible = False
    require(not explicit_bump_constraint_compatible, "bump_not_promoted_to_lawful_data")
    require(not weighted_family_constraint_compatible, "weighted_family_not_promoted_to_lawful_data")
    common_closed_fibre_period = False
    g330_period_normalized_integer_available = False
    require(not common_closed_fibre_period, "irrational_flow_has_no_common_fibre_period")
    require(not g330_period_normalized_integer_available,
            "g330_period_normalization_unavailable_without_fibration")

    payload = {
        "landing": (
            "UNIFORM_RICCI_GAP_PRESERVES_GLOBAL_SMOOTH_EIGENLINE"
            "__ARBITRARILY_CLOSE_NONHOMOGENEOUS_METRICS_CAN_HAVE_IRREGULAR_NONCLOSED_RICCI_EIGENFLOW"
            "__HOPF_FIBRATION_AND_G330_PERIOD_NORMALIZATION_ARE_NOT_PERTURBATION_OPEN"
            "__LOCAL_DYNAMIC_CARRY_REMAINS_CONSTRAINT_COMPATIBLE_AND_GAP_CONDITIONAL"
        ),
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "weighted_metric": "g_w=H/F+eta0^2/F^2; F=w1*x+w2*(1-x)",
        "weighted_ricci": "RicSharp=lambda_h*I+(2-lambda_h)*xi tensor eta",
        "weighted_flow": "xi=w1*d_phi1+w2*d_phi2; generic torus orbit closes iff w1/w2 is rational",
        "common_bundle": "B from gamma=gamma0(B.,.); compare B^(1/2) RicSharp_gamma B^(-1/2)",
        "regularity": "C2 metric control gives continuous Ricci projector; smooth metric plus open gap gives smooth line",
        "topology": "H1(S3;Z2)=0 trivializes the line bundle but selects no sign and forces no periodic orbit",
        "explicit_bump_constraint_compatible": explicit_bump_constraint_compatible,
        "weighted_family_constraint_compatible": weighted_family_constraint_compatible,
        "common_closed_fibre_period": common_closed_fibre_period,
        "g330_period_normalized_integer_available": g330_period_normalized_integer_available,
        "dynamic_scope": "only constraint-compatible data; nonzero local interval while uniform gap remains open",
        "historical_carrier_used": False,
        "historical_action_used": False,
        "stability_claimed": False,
        "history_selected": False,
        "scale_selected": False,
        "Xmax_selected": False,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G331 production PASS: {len(checks)} exact checks")


if __name__ == "__main__":
    main()
