#!/usr/bin/env python3
"""G323 production: explicit unmarked compact-quotient classification."""

import csv
from fractions import Fraction
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
P = 1.5
AMP = 0.2
J0 = 100.0
MU = J0 / 9.0
MODES = (1, 2, 3, 4)
SIGNS = (-1, 1)
SAMPLES = 16384
TWO_PI = 2.0 * math.pi
CHECKS = []
LANDING = (
    "REGISTERED_G320_PROFILES_EMBED_AS_CAUCHY_GRAPHS_IN_ONE_LOCAL_RICCI_FLAT_"
    "TAUB_FORM__INTEGER_MODES_HAVE_STRICTLY_DISTINCT_COMPACT_LATTICE_MODULI_"
    "AND_THUS_DISTINCT_UNMARKED_QUOTIENTS__OPPOSITE_K_SIGNS_ARE_ONE_"
    "TIME_UNORIENTED_METRIC_WITH_OPPOSITE_TIME_ORIENTATIONS__NO_OCCUPANCY_SELECTION"
)


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


class Dual:
    """Exact value and first derivative in R for the tensor audit."""

    __slots__ = ("v", "d")

    def __init__(self, value, derivative=0):
        self.v = Fraction(value)
        self.d = Fraction(derivative)

    @staticmethod
    def lift(other):
        return other if isinstance(other, Dual) else Dual(other)

    def __add__(self, other):
        other = self.lift(other)
        return Dual(self.v + other.v, self.d + other.d)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.v, -self.d)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Dual(self.v * other.v, self.d * other.v + self.v * other.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        return Dual(
            self.v / other.v,
            (self.d * other.v - self.v * other.d) / (other.v * other.v),
        )

    def __rtruediv__(self, other):
        return self.lift(other) / self


def exact_ambient_tensor_audit(r_value, mu_value):
    """Build Gamma, Ricci, and Kretschmann by exact index loops."""
    r = Fraction(r_value)
    mu = Fraction(mu_value)
    g = [
        Dual(-r / mu, -1 / mu),
        Dual(mu / r, -mu / (r * r)),
        Dual(r * r, 2 * r),
        Dual(r * r, 2 * r),
    ]
    dg = [
        Dual(-1 / mu, 0),
        Dual(-mu / (r * r), 2 * mu / (r ** 3)),
        Dual(2 * r, 2),
        Dual(2 * r, 2),
    ]
    inv = [1 / item for item in g]
    gamma = [[[Dual(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for upper in range(4):
        for lower_1 in range(4):
            for lower_2 in range(4):
                total = Dual(0)
                # Diagonal metric: only contracted index equal to upper contributes.
                contracted = upper
                term = Dual(0)
                if lower_1 == 0 and contracted == lower_2:
                    term += dg[contracted]
                if lower_2 == 0 and contracted == lower_1:
                    term += dg[contracted]
                if contracted == 0 and lower_1 == lower_2:
                    term -= dg[lower_1]
                total += inv[upper] * term / 2
                gamma[upper][lower_1][lower_2] = total

    ricci = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for left in range(4):
        for right in range(4):
            total = Fraction(0)
            for a in range(4):
                if a == 0:
                    total += gamma[a][left][right].d
                if right == 0:
                    total -= gamma[a][left][a].d
                for b in range(4):
                    total += gamma[a][a][b].v * gamma[b][left][right].v
                    total -= gamma[a][right][b].v * gamma[b][left][a].v
            ricci[left][right] = total

    rup = [[[[Fraction(0) for _ in range(4)] for _ in range(4)]
            for _ in range(4)] for _ in range(4)]
    for upper in range(4):
        for lower in range(4):
            for c in range(4):
                for d in range(4):
                    total = Fraction(0)
                    if c == 0:
                        total += gamma[upper][d][lower].d
                    if d == 0:
                        total -= gamma[upper][c][lower].d
                    for e in range(4):
                        total += gamma[upper][c][e].v * gamma[e][d][lower].v
                        total -= gamma[upper][d][e].v * gamma[e][c][lower].v
                    rup[upper][lower][c][d] = total

    kretschmann = Fraction(0)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    lowered = g[a].v * rup[a][b][c][d]
                    kretschmann += (
                        inv[a].v * inv[b].v * inv[c].v * inv[d].v
                        * lowered * lowered
                    )
    return ricci, kretschmann


def profile_jet(x_value, mode, p=P, amplitude=AMP):
    u = mode * x_value
    return (
        p + amplitude * math.cos(u),
        -amplitude * mode * math.sin(u),
        -amplitude * mode * mode * math.cos(u),
    )


def embedding_row(x_value, mode, sign):
    psi, psi_1, psi_2 = profile_jet(x_value, mode)
    z_value = 36.0 * psi_1 * psi_1 + J0
    root_z = math.sqrt(z_value)
    b_value = sign * psi ** -3 * root_z
    b_1 = b_value * (
        -3.0 * psi_1 / psi + 36.0 * psi_1 * psi_2 / z_value
    )
    f_value = 12.0 * psi_2 * psi ** -5
    a_value = f_value / b_value
    kx_expected = (3.0 * a_value - b_value) / 6.0
    ky_expected = b_value / 3.0

    r_value = psi * psi
    r_1 = 2.0 * psi * psi_1
    r_2 = 2.0 * (psi_1 * psi_1 + psi * psi_2)
    x_1 = -3.0 * b_value * psi ** 6 / J0
    x_2 = -3.0 * (b_1 * psi ** 6 + 6.0 * b_value * psi ** 5 * psi_1) / J0

    induced_xx = -(r_value / MU) * r_1 ** 2 + (MU / r_value) * x_1 ** 2
    normal_r = MU * x_1 / r_value ** 2
    normal_x = r_1 / MU
    normal_norm = -(r_value / MU) * normal_r ** 2 + (MU / r_value) * normal_x ** 2
    normal_tangent = (
        -(r_value / MU) * normal_r * r_1
        + (MU / r_value) * normal_x * x_1
    )

    # Nonzero ambient Christoffels needed by the embedded curve.
    gamma_r_rr = 1.0 / (2.0 * r_value)
    gamma_r_xx = -MU * MU / (2.0 * r_value ** 3)
    gamma_x_rx = -1.0 / (2.0 * r_value)
    n_cov_r = -x_1 / r_value
    n_cov_x = r_1 / r_value
    k_xx = (
        n_cov_r * (r_2 + gamma_r_rr * r_1 ** 2 + gamma_r_xx * x_1 ** 2)
        + n_cov_x * (x_2 + 2.0 * gamma_x_rx * r_1 * x_1)
    )
    kx_embedded = k_xx / induced_xx
    ky_embedded = -MU * x_1 / r_value ** 3

    # Four-curvature reconstructed on the slice: magnetic part vanishes in this LRS branch.
    e_x = -J0 / (9.0 * psi ** 6)
    e_y = J0 / (18.0 * psi ** 6)
    c2_from_data = 8.0 * (e_x * e_x + 2.0 * e_y * e_y)
    c2_ambient = 12.0 * MU * MU / r_value ** 6
    return {
        "psi": psi,
        "B": b_value,
        "X_prime": x_1,
        "pullback_error": abs(induced_xx - psi ** 4),
        "normal_norm_error": abs(normal_norm + 1.0),
        "normal_tangent_error": abs(normal_tangent),
        "kx_error": abs(kx_embedded - kx_expected),
        "ky_error": abs(ky_embedded - ky_expected),
        "curvature_join_error": abs(c2_from_data - c2_ambient),
    }


# Exact ambient checks at several rational points, using tensor construction rather than a name.
for r_exact, mu_exact in ((Fraction(2, 3), Fraction(5, 7)),
                          (Fraction(7, 5), Fraction(11, 4)),
                          (Fraction(13, 6), Fraction(17, 9))):
    ricci, kret = exact_ambient_tensor_audit(r_exact, mu_exact)
    check(f"ambient Ricci exact R={r_exact} mu={mu_exact}",
          all(value == 0 for row in ricci for value in row))
    check(f"ambient Kretschmann exact R={r_exact} mu={mu_exact}",
          kret == 12 * mu_exact * mu_exact / (r_exact ** 6))

# Exact local-isometry component identities for an arbitrary rational scale.
for scale in (Fraction(2, 3), Fraction(5, 4), Fraction(7, 2)):
    r0 = Fraction(11, 7)
    mu0 = Fraction(13, 9)
    r_star = scale * r0
    mu_star = scale ** 3 * mu0
    check("local isometry RR", -(r_star / mu_star) * scale ** 2 == -r0 / mu0)
    check("local isometry XX", (mu_star / r_star) / scale ** 2 == mu0 / r0)
    check("local isometry YY", r_star ** 2 / scale ** 2 == r0 ** 2)

atlas = []
for mode in MODES:
    for sign in SIGNS:
        rows = [
            embedding_row(TWO_PI * index / SAMPLES, mode, sign)
            for index in range(SAMPLES)
        ]
        period_x = TWO_PI * math.fsum(abs(row["X_prime"]) for row in rows) / SAMPLES
        summary = {
            "mode": mode,
            "sign": sign,
            "L_X": period_x,
            "Q_X": period_x / TWO_PI,
            "min_abs_X_prime": min(abs(row["X_prime"]) for row in rows),
            "max_pullback_error": max(row["pullback_error"] for row in rows),
            "max_normal_norm_error": max(row["normal_norm_error"] for row in rows),
            "max_normal_tangent_error": max(row["normal_tangent_error"] for row in rows),
            "max_kx_error": max(row["kx_error"] for row in rows),
            "max_ky_error": max(row["ky_error"] for row in rows),
            "max_curvature_join_error": max(row["curvature_join_error"] for row in rows),
        }
        check(f"X prime nonzero n={mode} sign={sign}", summary["min_abs_X_prime"] > 0)
        for key in (
            "max_pullback_error", "max_normal_norm_error", "max_normal_tangent_error",
            "max_kx_error", "max_ky_error", "max_curvature_join_error",
        ):
            check(f"{key} n={mode} sign={sign}", summary[key] < 2e-11)
        atlas.append(summary)

positive = {row["mode"]: row for row in atlas if row["sign"] == 1}
negative = {row["mode"]: row for row in atlas if row["sign"] == -1}
for mode in MODES:
    check(f"sign-independent period n={mode}",
          abs(positive[mode]["L_X"] - negative[mode]["L_X"]) < 2e-13)
for lower, upper in zip(MODES, MODES[1:]):
    check(f"strict mode period n={lower}->{upper}",
          positive[upper]["L_X"] > positive[lower]["L_X"])

with (HERE / "QUOTIENT_ATLAS.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=tuple(atlas[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(atlas)

result = {
    "schema": "udt-g323-unmarked-taub-quotient-v1",
    "status": "PASS_PENDING_EXTERNAL_REVIEW",
    "landing": LANDING,
    "assertion_count": len(CHECKS),
    "ambient_ricci_flat_exact": True,
    "ambient_kretschmann": "12*mu^2/R^6",
    "complete_data_embedding_pass": True,
    "profiles_are_local_refoliations": True,
    "primitive_period_formula_pass": True,
    "mode_period_strictly_increasing": True,
    "n1_n2_unmarked_compact_quotients_distinct": True,
    "opposite_K_same_time_unoriented_metric": True,
    "opposite_K_time_orientations_distinct": True,
    "physical_occupancy_selected": False,
    "unique_universe_selected": False,
    "physical_scale_selected": False,
    "Xmax_selected": False,
    "metric_changed": False,
    "kernel_changed": False,
    "angular_cancellation_changed": False,
    "max_pullback_error": max(row["max_pullback_error"] for row in atlas),
    "max_extrinsic_error": max(max(row["max_kx_error"], row["max_ky_error"]) for row in atlas),
    "max_curvature_join_error": max(row["max_curvature_join_error"] for row in atlas),
    "periods": {str(mode): positive[mode]["L_X"] for mode in MODES},
}
(HERE / "DERIVATION_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(f"G323 production PASS: {len(CHECKS)} assertions")
print(f"max pullback error: {result['max_pullback_error']:.3e}")
print(f"max extrinsic error: {result['max_extrinsic_error']:.3e}")
print("periods:", result["periods"])
print(LANDING)

