#!/usr/bin/env python3
"""Exact algebra and deterministic solution-region witnesses for the G59 atlas."""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
READ_ONLY = "--read-only" in sys.argv[1:]


def dot_eta(u: sp.Matrix, v: sp.Matrix) -> sp.Expr:
    eta = sp.diag(-1, 1, 1, 1)
    return (u.T * eta * v)[0]


def bivector(u: sp.Matrix, v: sp.Matrix) -> dict[tuple[int, int], sp.Expr]:
    return {
        (a, b): sp.expand(u[a] * v[b] - u[b] * v[a])
        for a in range(4)
        for b in range(a + 1, 4)
    }


x = sp.Matrix(sp.symbols("x0:4", real=True))
y = sp.Matrix(sp.symbols("y0:4", real=True))
B = bivector(x, y)

h00 = dot_eta(x, x)
h01 = dot_eta(x, y)
h11 = dot_eta(y, y)
det_h = sp.expand(h00 * h11 - h01**2)
h = sp.Matrix([[h00, h01], [h01, h11]])

# Complete split-relative matrix channels.
X = sp.Matrix([[x[0], y[0]], [x[1], y[1]]])
Y = sp.Matrix([[x[2], y[2]], [x[3], y[3]]])
eta2 = sp.diag(-1, 1)
H_R = sp.simplify(X.T * eta2 * X)
H_A = sp.simplify(Y.T * Y)
matrix_sum_residual = sp.simplify(h - H_R - H_A)

plucker = sp.expand(
    B[(0, 1)] * B[(2, 3)]
    - B[(0, 2)] * B[(1, 3)]
    + B[(0, 3)] * B[(1, 2)]
)

R = B[(0, 1)] ** 2
A = B[(2, 3)] ** 2
M_signed = (
    -B[(0, 2)] ** 2
    - B[(0, 3)] ** 2
    + B[(1, 2)] ** 2
    + B[(1, 3)] ** 2
)
gram_residual = sp.expand(det_h - (-R + A + M_signed))
det_reciprocal_residual = sp.expand(H_R.det() + R)
det_angular_residual = sp.expand(H_A.det() - A)
det_cross_residual = sp.expand(det_h - H_R.det() - H_A.det() - M_signed)

# Split-preserving SO+(1,1) x SO(2) transformation.
u, theta = sp.symbols("u theta", real=True)
boost = sp.Matrix(
    [
        [sp.cosh(u), sp.sinh(u), 0, 0],
        [sp.sinh(u), sp.cosh(u), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
rotation = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, sp.cos(theta), -sp.sin(theta)],
        [0, 0, sp.sin(theta), sp.cos(theta)],
    ]
)
G = boost * rotation
BG = bivector(G * x, G * y)
RG = BG[(0, 1)] ** 2
AG = BG[(2, 3)] ** 2
MSG = (
    -BG[(0, 2)] ** 2
    - BG[(0, 3)] ** 2
    + BG[(1, 2)] ** 2
    + BG[(1, 3)] ** 2
)
invariance_residuals = {
    "B01": sp.simplify(sp.trigsimp(BG[(0, 1)] - B[(0, 1)])),
    "B23": sp.simplify(sp.trigsimp(BG[(2, 3)] - B[(2, 3)])),
    "R": sp.simplify(sp.trigsimp(RG - R)),
    "A": sp.simplify(sp.trigsimp(AG - A)),
    "M_signed": sp.simplify(sp.trigsimp(MSG - M_signed)),
}

XG = (G * sp.Matrix.hstack(x, y))[:2, :]
YG = (G * sp.Matrix.hstack(x, y))[2:, :]
HRG = sp.simplify(XG.T * eta2 * XG)
HAG = sp.simplify(YG.T * YG)
matrix_invariance_residuals = {
    "H_R": sp.simplify(sp.trigsimp(HRG - H_R)),
    "H_A": sp.simplify(sp.trigsimp(HAG - H_A)),
}

# Exact same-h witness: pure reciprocal plane versus a plane tilted into e2.
a = sp.symbols("a", real=True)
e0 = sp.Matrix([1, 0, 0, 0])
e1 = sp.Matrix([0, 1, 0, 0])
tilted0 = sp.Matrix([sp.cosh(a), 0, sp.sinh(a), 0])
pure_h = sp.Matrix([[dot_eta(e0, e0), dot_eta(e0, e1)], [dot_eta(e1, e0), dot_eta(e1, e1)]])
tilted_h = sp.Matrix(
    [
        [dot_eta(tilted0, tilted0), dot_eta(tilted0, e1)],
        [dot_eta(e1, tilted0), dot_eta(e1, e1)],
    ]
)
pure_B = bivector(e0, e1)
tilted_B = bivector(tilted0, e1)
same_h_residual = sp.simplify(sp.trigsimp(tilted_h - pure_h))
tilted_R = sp.simplify(tilted_B[(0, 1)] ** 2)
tilted_A = sp.simplify(tilted_B[(2, 3)] ** 2)
tilted_MS = sp.simplify(
    -tilted_B[(0, 2)] ** 2
    - tilted_B[(0, 3)] ** 2
    + tilted_B[(1, 2)] ** 2
    + tilted_B[(1, 3)] ** 2
)
pure_X = sp.Matrix([[1, 0], [0, 1]])
pure_Y = sp.zeros(2)
tilted_X = sp.Matrix([[sp.cosh(a), 0], [0, 1]])
tilted_Y = sp.Matrix([[sp.sinh(a), 0], [0, 0]])
pure_HR = sp.simplify(pure_X.T * eta2 * pure_X)
pure_HA = sp.simplify(pure_Y.T * pure_Y)
tilted_HR = sp.simplify(tilted_X.T * eta2 * tilted_X)
tilted_HA = sp.simplify(tilted_Y.T * tilted_Y)

# Exact first variation of the pair-state coordinates under an angular-matrix change.
r00, r01, r11, a00, a01, a11 = sp.symbols(
    "r00 r01 r11 a00 a01 a11", real=True
)
HRs = sp.Matrix([[r00, r01], [r01, r11]])
HAs = sp.Matrix([[a00, a01], [a01, a11]])
hs = HRs + HAs
dhs = sp.Matrix([[sp.symbols("da00") , sp.symbols("da01")], [sp.symbols("da01"), sp.symbols("da11")]])
da00, da01, da11 = dhs[0, 0], dhs[0, 1], dhs[1, 1]
eps = sp.symbols("eps", real=True)
hs_eps = hs + eps * dhs
kappa_eps = sp.Rational(1, 4) * sp.log(-hs_eps.det())
phi_eps = sp.Rational(1, 4) * sp.log((-hs_eps.det()) / hs_eps[0, 0] ** 2)
beta_eps = hs_eps[0, 1] / hs_eps[0, 0]
dkappa_direct = sp.diff(kappa_eps, eps).subs(eps, 0)
dphi_direct = sp.diff(phi_eps, eps).subs(eps, 0)
dbeta_direct = sp.diff(beta_eps, eps).subs(eps, 0)
dkappa_formula = sp.Rational(1, 4) * sp.trace(hs.inv() * dhs)
dphi_formula = dkappa_formula - sp.Rational(1, 2) * da00 / hs[0, 0]
dbeta_formula = (hs[0, 0] * da01 - hs[0, 1] * da00) / hs[0, 0] ** 2
variation_residuals = {
    "dkappa": sp.simplify(dkappa_direct - dkappa_formula),
    "dphi": sp.simplify(dphi_direct - dphi_formula),
    "dbeta": sp.simplify(dbeta_direct - dbeta_formula),
}

# No positive-definite quadratic form on the boost doublet.
qa, qb, qd = sp.symbols("qa qb qd", real=True)
Q = sp.Matrix([[qa, qb], [qb, qd]])
K = sp.Matrix([[0, 1], [1, 0]])
quadratic_invariance_equations = [
    sp.expand(value) for value in (K.T * Q + Q * K)
]
quadratic_solution = sp.solve(quadratic_invariance_equations, [qb, qd], dict=True)

# Constructive witnesses across the signed invariant region R>0,A>0.
sample_rows: list[dict[str, str]] = []
for Rv in (0.25, 1.0, 4.0):
    for Av in (0.0625, 0.5, 2.0):
        # Three values safely inside R > A + M_signed.
        for offset in (0.125, 1.0, 4.0):
            Mv = Rv - Av - offset
            z = (-Mv + math.sqrt(Mv * Mv + 4.0 * Rv * Av)) / 2.0
            p = math.sqrt(z)
            t = math.sqrt(Rv * Av) / p
            det_m = p * t
            reconstructed_m = -p * p + t * t
            det_pair = -Rv + Av + reconstructed_m
            sample_rows.append(
                {
                    "R": f"{Rv:.17g}",
                    "A": f"{Av:.17g}",
                    "M_signed": f"{Mv:.17g}",
                    "B01": f"{math.sqrt(Rv):.17g}",
                    "B23": f"{math.sqrt(Av):.17g}",
                    "B02": f"{p:.17g}",
                    "B13": f"{t:.17g}",
                    "det_M": f"{det_m:.17g}",
                    "det_h": f"{det_pair:.17g}",
                    "lorentzian": str(det_pair < 0).lower(),
                    "max_abs_residual": f"{max(abs(det_m-math.sqrt(Rv*Av)), abs(reconstructed_m-Mv)):.3e}",
                }
            )

if not READ_ONLY:
    with (HERE / "SAMPLED_REGION_ATLAS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(sample_rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(sample_rows)

assert plucker == 0
assert gram_residual == 0
assert matrix_sum_residual == sp.zeros(2)
assert det_reciprocal_residual == 0
assert det_angular_residual == 0
assert det_cross_residual == 0
assert all(value == 0 for value in invariance_residuals.values())
assert all(value == sp.zeros(2) for value in matrix_invariance_residuals.values())
assert same_h_residual == sp.zeros(2)
assert quadratic_solution == [{qb: 0, qd: -qa}]
assert all(value == 0 for value in variation_residuals.values())
assert all(row["lorentzian"] == "true" for row in sample_rows)
assert max(float(row["max_abs_residual"]) for row in sample_rows) < 1e-12

result = {
    "status": "SPLIT_RELATIVE_SIGNED_ORCHESTRA_ATLAS",
    "base_commit": "8215a31578e571e29750daa53ccf26e436f7e582",
    "preregistration_commit": "b6fb1883",
    "refinement_commit": "162779cf",
    "exact_checks": {
        "plucker_simplicity": str(plucker),
        "gram_sector_identity": str(gram_residual),
        "matrix_sum": str(matrix_sum_residual),
        "det_reciprocal": str(det_reciprocal_residual),
        "det_angular": str(det_angular_residual),
        "det_cross": str(det_cross_residual),
        "split_group_invariance": {key: str(value) for key, value in invariance_residuals.items()},
        "matrix_split_group_invariance": {
            key: str(value) for key, value in matrix_invariance_residuals.items()
        },
        "angular_variation": {key: str(value) for key, value in variation_residuals.items()},
        "same_h_witness": str(same_h_residual),
        "positive_quadratic_form_solution": [{str(k): str(v) for k, v in sol.items()} for sol in quadratic_solution],
    },
    "identities": {
        "plucker": "B01*B23-B02*B13+B03*B12=0",
        "mixed_determinant": "det(M)=B01*B23",
        "gram": "det(h)=-R+A+M_signed",
        "matrix_orchestra": "h=H_R+H_A; H_R=X^T eta_(1,1) X; H_A=Y^T Y",
        "angular_phi_modulation": "dphi=(1/4)tr(h^-1 dH_A)-(1/2)dH_A00/h00",
        "angular_kappa_modulation": "dkappa=(1/4)tr(h^-1 dH_A)",
        "angular_beta_modulation": "dbeta=(h00 dH_A01-h01 dH_A00)/h00^2",
        "lorentzian_regular": "R>A+M_signed",
        "common_scale": "V_i->sigma V_i gives (R,A,M_signed,det_h)->sigma^4 times each",
    },
    "same_h_witness": {
        "h": "diag(-1,1)",
        "pure": {"R": "1", "A": "0", "M_signed": "0"},
        "tilted": {"R": str(tilted_R), "A": str(tilted_A), "M_signed": str(tilted_MS)},
        "pure_H_R": str(pure_HR),
        "pure_H_A": str(pure_HA),
        "tilted_H_R": str(tilted_HR),
        "tilted_H_A": str(tilted_HA),
    },
    "sampled_witness_count": len(sample_rows),
    "maximum_conclusion": "conditional pointwise signed sector-volume atlas; no positive physical mixing law or regime selection",
}

if not READ_ONLY:
    with (HERE / "DERIVATION_RESULT.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")

print(
    "PASS exact=18 sampled={} landing={}".format(
        len(sample_rows), result["status"]
    )
)
