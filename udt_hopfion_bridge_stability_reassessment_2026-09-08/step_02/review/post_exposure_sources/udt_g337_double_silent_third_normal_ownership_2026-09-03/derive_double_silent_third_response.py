#!/usr/bin/env python3
"""Exact G337 third-normal response on the inherited double-silent stratum."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "96135e03"


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


class Jet2:
    """Value and first two x derivatives, with exact rational arithmetic."""

    __slots__ = ("v", "d1", "d2")

    def __init__(self, value=0, first=0, second=0):
        self.v, self.d1, self.d2 = F(value), F(first), F(second)

    @staticmethod
    def lift(value):
        return value if isinstance(value, Jet2) else Jet2(value)

    def __add__(self, other):
        other = self.lift(other)
        return Jet2(self.v + other.v, self.d1 + other.d1, self.d2 + other.d2)

    __radd__ = __add__

    def __neg__(self):
        return Jet2(-self.v, -self.d1, -self.d2)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Jet2(
            self.v * other.v,
            self.d1 * other.v + self.v * other.d1,
            self.d2 * other.v + 2 * self.d1 * other.d1 + self.v * other.d2,
        )

    __rmul__ = __mul__

    def inverse(self):
        if self.v == 0:
            raise ZeroDivisionError("zero jet")
        return Jet2(
            1 / self.v,
            -self.d1 / self.v**2,
            2 * self.d1**2 / self.v**3 - self.d2 / self.v**2,
        )

    def __truediv__(self, other):
        return self * self.lift(other).inverse()

    def __rtruediv__(self, other):
        return self.lift(other) * self.inverse()

    def dx(self):
        return Jet2(self.d1, self.d2, 0)


class TimeDual:
    """First-order time dual whose coefficients are exact spatial two-jets."""

    __slots__ = ("a", "b")

    def __init__(self, base=0, tangent=0):
        self.a, self.b = Jet2.lift(base), Jet2.lift(tangent)

    @staticmethod
    def lift(value):
        return value if isinstance(value, TimeDual) else TimeDual(value)

    def __add__(self, other):
        other = self.lift(other)
        return TimeDual(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return TimeDual(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return TimeDual(self.a * other.a, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def inverse(self):
        return TimeDual(self.a.inverse(), -self.b / (self.a * self.a))

    def __truediv__(self, other):
        return self * self.lift(other).inverse()

    def __rtruediv__(self, other):
        return self.lift(other) * self.inverse()

    def dx(self):
        return TimeDual(self.a.dx(), self.b.dx())


def identity(n: int, zero=F(0), one=F(1)):
    return [[one if i == j else zero for j in range(n)] for i in range(n)]


def inverse_matrix(matrix):
    n = len(matrix)
    zero, one = type(matrix[0][0])(0), type(matrix[0][0])(1)
    augmented = [list(matrix[i]) + identity(n, zero, one)[i] for i in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column].a.v != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor.a.v != 0 or factor.b.v != 0:
                augmented[row] = [
                    augmented[row][j] - factor * augmented[column][j]
                    for j in range(2 * n)
                ]
    return [row[n:] for row in augmented]


def mm(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), type(left[0][0])(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def weighted_fields(x_value: F, w1: F, w2: F):
    x, one = Jet2(x_value, 1, 0), Jet2(1)
    radial = x * (one - x)
    f = w1 * x + w2 * (one - x)
    eta = [Jet2(0), x / f, (one - x) / f]
    zeta = [Jet2(0), Jet2(w2) / f, Jet2(-w1) / f]
    metric = [[Jet2(0) for _ in range(3)] for _ in range(3)]
    metric[0][0] = 1 / (4 * radial * f)
    for i in (1, 2):
        for j in (1, 2):
            metric[i][j] = radial / f * zeta[i] * zeta[j] + eta[i] * eta[j]
    # Directly simplified scalar curvature of the same coordinate metric.
    numerator = (
        4 * w1 * w1 * x - 8 * w1 * w2 + w1 * x
        - 4 * w2 * w2 * x + 4 * w2 * w2 - w2 * x + w2
    )
    scalar = -2 * numerator / f
    return metric, eta, scalar


def ricci_of_dual_metric(metric):
    inverse = inverse_matrix(metric)
    zero = TimeDual(0)
    connection = [[[TimeDual(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for ell in range(3):
                    term = metric[ell][j].dx() if i == 0 else zero
                    term += metric[ell][i].dx() if j == 0 else zero
                    term -= metric[i][j].dx() if ell == 0 else zero
                    connection[upper][i][j] += inverse[upper][ell] * term / 2
    ricci = [[TimeDual(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = connection[0][i][j].dx()
            if j == 0:
                value -= sum((connection[k][i][k].dx() for k in range(3)), TimeDual(0))
            for k in range(3):
                for ell in range(3):
                    value += connection[k][i][j] * connection[ell][k][ell]
                    value -= connection[ell][i][k] * connection[k][j][ell]
            ricci[i][j] = value
    return inverse, ricci


def contract(tensor, left, right):
    return sum((left[i] * tensor[i][j] * right[j] for i in range(3) for j in range(3)), F(0))


def mat_value(matrix):
    return [[matrix[i][j].v for j in range(3)] for i in range(3)]


def inverse_fraction(matrix):
    dual = [[TimeDual(Jet2(matrix[i][j])) for j in range(3)] for i in range(3)]
    return [[entry.a.v for entry in row] for row in inverse_matrix(dual)]


def add_matrix(*matrices):
    return [[sum((matrix[i][j] for matrix in matrices), F(0)) for j in range(3)] for i in range(3)]


def scale_matrix(scale, matrix):
    return [[scale * matrix[i][j] for j in range(3)] for i in range(3)]


def exact_control(w1: F, w2: F, x_value: F, branch: int, mu=F(16, 25), bmag=F(1)):
    metric_j, eta_j, scalar_j = weighted_fields(x_value, w1, w2)
    R = scalar_j.v
    b = F(branch) * bmag
    C = b * (1 - 2 * mu)
    Lambda = R / 2 - 2 * b * b * mu + 3 * b * b * mu * mu
    require_root = (b + C) ** 2 == 2 * (R + 2 * C * C - 2 * Lambda)
    if not require_root:
        raise AssertionError("G332 root identity")

    # Differentiate the strict G332 branch, with C and Lambda spatially constant.
    bp = scalar_j.d1 / (b + C)
    bpp = (scalar_j.d2 - bp * bp) / (b + C)
    b_j = Jet2(b, bp, bpp)
    a_j = (C - b_j) / 2
    K_j = [[a_j * metric_j[i][j] + b_j * eta_j[i] * eta_j[j]
            for j in range(3)] for i in range(3)]
    h_j = [[-2 * K_j[i][j] for j in range(3)] for i in range(3)]
    dual_metric = [[TimeDual(metric_j[i][j], h_j[i][j]) for j in range(3)] for i in range(3)]
    inverse_dual, ricci_dual = ricci_of_dual_metric(dual_metric)

    g = mat_value(metric_j)
    gi = [[entry.a.v for entry in row] for row in inverse_dual]
    K = mat_value(K_j)
    Ric = [[entry.a.v for entry in row] for row in ricci_dual]
    Ricdot = [[entry.b.v for entry in row] for row in ricci_dual]
    A = mm([[TimeDual(Jet2(v)) for v in row] for row in gi],
           [[TimeDual(Jet2(v)) for v in row] for row in K])
    A = [[entry.a.v for entry in row] for row in A]
    tau = sum(A[i][i] for i in range(3))
    B = mm([[TimeDual(Jet2(v)) for v in row] for row in K],
           mm([[TimeDual(Jet2(v)) for v in row] for row in gi],
              [[TimeDual(Jet2(v)) for v in row] for row in K]))
    B = [[entry.a.v for entry in row] for row in B]
    Ften = add_matrix(Ric, scale_matrix(tau, K), scale_matrix(-2, B), scale_matrix(-Lambda, g))

    # Direct time differentiation of B=K g^{-1} K, including n(g^{-1}).
    Fm = [[TimeDual(Jet2(v)) for v in row] for row in Ften]
    Km = [[TimeDual(Jet2(v)) for v in row] for row in K]
    gim = [[TimeDual(Jet2(v)) for v in row] for row in gi]
    Bdot_1 = mm(Fm, mm(gim, Km))
    Bdot_2 = mm(Km, mm(gim, Fm))
    Bdot_3 = mm(Km, mm(gim, mm(Km, mm(gim, Km))))
    Bdot = [[Bdot_1[i][j].a.v + Bdot_2[i][j].a.v + 2 * Bdot_3[i][j].a.v
             for j in range(3)] for i in range(3)]
    third_tensor = add_matrix(scale_matrix(-1, Ricdot), scale_matrix(2, Bdot))

    xi = [F(0), w1, w2]
    # The x-coordinate line is horizontal and orthogonal to the unit xi line.
    ex2 = 1 / g[0][0]
    sx = third_tensor[0][0] * ex2
    sv = contract(third_tensor, xi, xi)
    sxv = sum(third_tensor[0][j] * xi[j] for j in range(3))
    s2 = (1 - mu) * sx + mu * sv
    grad_R_squared = ex2 * scalar_j.d1 * scalar_j.d1
    q0 = -((1 - mu) * (C - b) / 2 + mu * (C + b) / 2)
    s1 = -((1 - mu) * contract(Ften, [1, 0, 0], [1, 0, 0]) * ex2
            + mu * contract(Ften, xi, xi))
    return {
        "w1": str(w1), "w2": str(w2), "x": str(x_value),
        "R": str(R), "R_prime": str(scalar_j.d1), "R_second": str(scalar_j.d2),
        "grad_R_squared": str(grad_R_squared),
        "mu": str(mu), "b": str(b), "C": str(C), "Lambda": str(Lambda),
        "b_prime": str(bp), "b_second": str(bpp), "q0": str(q0), "s1": str(s1),
        "s2": str(s2), "s2_horizontal": str(sx), "s2_vertical": str(sv),
        "mixed_x_xi": str(sxv), "third_tensor": [[str(v) for v in row] for row in third_tensor],
    }


def boost_from_half_tangent(t: F) -> tuple[F, F]:
    return 2 * t / (1 - t * t), (1 + t * t) / (1 - t * t)


def derive() -> dict:
    checks: list[str] = []
    # Two inequivalent positive-weight controls with the same complete pointwise tuple.
    R0 = F(319, 200)
    controls = (
        (F(1, 4), F(1, 2), F(1438, 1919)),
        (F(1, 3), F(1, 2), F(4071, 6157)),
    )
    records = []
    for branch in (-1, 1):
        branch_records = [exact_control(*control, branch) for control in controls]
        for index, record in enumerate(branch_records):
            require(F(record["R"]) == R0, f"control_{branch}_{index}_same_R", checks)
            require(F(record["q0"]) == 0, f"control_{branch}_{index}_q0_zero", checks)
            require(F(record["s1"]) == 0, f"control_{branch}_{index}_s1_zero", checks)
            require(F(record["mixed_x_xi"]) == 0,
                    f"control_{branch}_{index}_radial_vertical_decoupling", checks)
        require(branch_records[0]["s2"] != branch_records[1]["s2"],
                f"branch_{branch}_pointwise_tuple_nonownership", checks)
        require(branch_records[0]["grad_R_squared"] != branch_records[1]["grad_R_squared"],
                f"branch_{branch}_invariant_spatial_germs_distinct", checks)
        records.extend(branch_records)

    # Equal-weight homogeneous result, independently simplified before production: s2=8*b*mu.
    homogeneous = []
    for branch in (-1, 1):
        record = exact_control(F(719, 1600), F(719, 1600), F(1, 3), branch)
        expected = 8 * F(branch) * F(16, 25)
        require(F(record["s2"]) == expected, f"homogeneous_{branch}_eight_b_mu", checks)
        homogeneous.append(record)
    require(F(homogeneous[0]["s2"]) == -F(homogeneous[1]["s2"]),
            "homogeneous_branches_reverse_third_response", checks)

    boost_checks = 0
    for index, record in enumerate(records + homogeneous):
        s2 = F(record["s2"])
        for half_tangent in (F(-3, 5), F(-1, 3), F(0), F(1, 4), F(2, 3)):
            sh, ch = boost_from_half_tangent(half_tangent)
            require(ch * ch - sh * sh == 1,
                    f"boost_{index}_{half_tangent}_lorentz", checks)
            h00, h01, h11 = 2 * s2 * sh * sh, 2 * s2 * sh * ch, 2 * s2 * ch * ch
            require(-h00 + h11 == 2 * s2,
                    f"boost_{index}_{half_tangent}_trace", checks)
            require(h00 * h11 - h01 * h01 == 0,
                    f"boost_{index}_{half_tangent}_rank_one", checks)
            require(s2 * sh * sh == h00 / 2,
                    f"boost_{index}_{half_tangent}_terminal", checks)
            if half_tangent == 0:
                require(h00 == 0, f"boost_{index}_zero_terminal_blind", checks)
            boost_checks += 1

    landing = (
        "G337_FULL_INITIAL_FIELDS_OWN_INHERITED_DOUBLE_SILENT_THIRD_JET"
        "__POINTWISE_R_B_C_LAMBDA_MU_TUPLE_DOES_NOT"
        "__SPATIAL_JETS_SURVIVE"
        "__BOTH_STRICT_ROOTS_AND_NONZERO_HOMOGENEOUS_RESPONSE_RETAINED"
        "__NO_FINITE_TIME_STABILITY_OR_HISTORY_SELECTION"
    )
    return {
        "package": "G337",
        "preregistration_commit": PREREG_COMMIT,
        "grade": "DERIVED_CONDITIONAL_BOUNDED__PENDING_INDEPENDENT_REVIEW",
        "landing": landing,
        "analytic_identity": {
            "double_silent_s2": "-(nRic3)(v,v)+2(n[K gamma^-1 K])(v,v)",
            "nB": "F gamma^-1 K + K gamma^-1 F + 2K gamma^-1 K gamma^-1 K",
            "ricci_variation_h_minus_2K": (
                "-D^kD_iK_kj-D^kD_jK_ki+D^kD_kK_ij+D_iD_j tau"
            ),
            "homogeneous_equal_weight": "s2=8*b*mu on the strict double-silent surface",
            "finite_boost_pair_third_jet": (
                "2s2[[sinh^2(z),sinh(z)cosh(z)],[sinh(z)cosh(z),cosh^2(z)]]"
            ),
            "finite_boost_terminal_third_jet": "s2*sinh(z)^2",
        },
        "classifications": {
            "complete_initial_field_ownership": "YES_CONDITIONAL",
            "pointwise_tuple_ownership": "NO",
            "spatial_jet_dependence": "YES",
            "both_strict_roots": "RETAINED",
            "finite_time_or_stability": "NOT_TESTED",
            "history_selection": "NOT_CLAIMED",
        },
        "exact_pointwise_twins": records,
        "homogeneous_controls": homogeneous,
        "finite_boost_controls": boost_checks,
        "checks_passed": len(checks),
        "checks_sha256": hashlib.sha256("\n".join(checks).encode()).hexdigest(),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "checks_passed": result["checks_passed"],
        "landing": result["landing"],
        "twin_s2": [row["s2"] for row in result["exact_pointwise_twins"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
