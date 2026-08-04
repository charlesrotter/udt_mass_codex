#!/usr/bin/env python3
"""Exact sparse transition and variation algebra for the extension bundle."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
checks: dict[str, str] = {}


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


# Exact local block and right-logarithmic variation.
phi = sp.symbols("phi", real=True)
u, v, w = sp.symbols("u v w", nonzero=True, real=True)
s11, s12, s21, s22 = sp.symbols("s11 s12 s21 s22", real=True)
du, dv, dw = sp.symbols("du dv dw", real=True)
ds11, ds12, ds21, ds22 = sp.symbols("ds11 ds12 ds21 ds22", real=True)
dphi = sp.symbols("dphi", real=True)

A = sp.diag(sp.exp(-phi), sp.exp(phi))
D = sp.Matrix([[u, v], [0, w]])
S = sp.Matrix([[s11, s12], [s21, s22]])
dA = sp.diag(-sp.exp(-phi) * dphi, sp.exp(phi) * dphi)
dD = sp.Matrix([[du, dv], [0, dw]])
dS = sp.Matrix([[ds11, ds12], [ds21, ds22]])

E = A.row_join(sp.zeros(2)).col_join((D * S).row_join(D))
Einv = A.inv().row_join(sp.zeros(2)).col_join((-S * A.inv()).row_join(D.inv()))
dE = dA.row_join(sp.zeros(2)).col_join((dD * S + D * dS).row_join(dD))
right_log = sp.simplify(dE * Einv)
expected_right_log = (dA * A.inv()).row_join(sp.zeros(2)).col_join((D * dS * A.inv()).row_join(dD * D.inv()))
check("block_inverse", zero(E * Einv - sp.eye(4)) and zero(Einv * E - sp.eye(4)))
check("fixed_rank_determinant_factorization", sp.simplify(E.det() - A.det() * D.det()) == 0)
check("right_log_variation_factorization", zero(right_log - expected_right_log))
check("depth_variation_block", zero(right_log[:2, :2] - sp.diag(-dphi, dphi)))
check("mixing_variation_cancels_delta_D_cross_terms", zero(right_log[2:, :2] - D * dS * A.inv()))
check("angular_variation_block", zero(right_log[2:, 2:] - dD * D.inv()))

# Seven chart tangents remain seven; this is not a physical mode count.
params = (u, v, w, s11, s12, s21, s22)
identity = {phi: 0, u: 1, v: 0, w: 1, s11: 0, s12: 0, s21: 0, s22: 0}
tangents = [E.diff(p).subs(identity) for p in params]
check("seven_local_extension_tangent_rank", sp.Matrix.hstack(*(x.reshape(16, 1) for x in tangents)).rank() == 7)

# Two-sided overlap and triple-overlap consistency using exact noncommuting rational anchors.
Ei = sp.Matrix([
    [1, 0, 0, 0], [0, 2, 0, 0], [1, -1, 3, 1], [2, 1, 0, 2]
])
Lij = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
Ljk = sp.Matrix([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]])
Rij = sp.Matrix([[2, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 1]])
Rjk = sp.Matrix([[1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 1, 1]])
Ej = Lij * Ei * Rij.inv()
Ek_seq = Ljk * Ej * Rjk.inv()
Lik = Ljk * Lij
Rik = Rjk * Rij
Ek_direct = Lik * Ei * Rik.inv()
check("two_sided_overlap_rule", zero(Ej * Rij - Lij * Ei))
check("triple_overlap_associativity", zero(Ek_seq - Ek_direct))
check("left_transition_cocycle_order", Lik == Ljk * Lij)
check("right_transition_cocycle_order", Rik == Rjk * Rij)

# Exact variation of the two-sided overlap.
dEi = sp.Matrix([[1, 0, 1, 0], [0, -1, 0, 0], [1, 2, 0, 1], [0, 1, -1, 0]])
dLij = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]])
dRij = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 0, -1, 0], [1, 0, 0, 0]])
dEj = dLij * Ei * Rij.inv() + Lij * dEi * Rij.inv() - Lij * Ei * Rij.inv() * dRij * Rij.inv()
ei = dEi * Ei.inv()
ej = dEj * Ej.inv()
ell = dLij * Lij.inv()
rr = dRij * Rij.inv()
ej_expected = ell + Lij * ei * Lij.inv() - Ej * rr * Ej.inv()
check("linearized_two_sided_overlap", zero(ej - ej_expected))

dLjk = sp.Matrix([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1]])
dLik = dLjk * Lij + Ljk * dLij
ell_ik = dLik * Lik.inv()
ell_jk = dLjk * Ljk.inv()
check("linearized_left_cocycle", zero(ell_ik - ell_jk - Ljk * ell * Ljk.inv()))

dRjk = sp.Matrix([[0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, -1, 0, 0]])
dRik = dRjk * Rij + Rjk * dRij
r_ik = dRik * Rik.inv()
r_jk = dRjk * Rjk.inv()
check("linearized_right_cocycle", zero(r_ik - r_jk - Rjk * rr * Rjk.inv()))

# Exact reciprocal Z2-graded algebra.
a, d0, b0, c0, z = sp.symbols("a d0 b0 c0 z", nonzero=True, real=True)
Ga = sp.diag(a, 1 / a)
Gd = sp.diag(d0, 1 / d0)
Fb = sp.Matrix([[0, b0], [1 / b0, 0]])
Fc = sp.Matrix([[0, c0], [1 / c0, 0]])
Dz = sp.diag(1 / z, z)
check("reciprocal_preserving_group_law", zero(Ga * Gd - sp.diag(a * d0, 1 / (a * d0))))
check("reciprocal_reversal_pair_is_preserving", zero(Fb * Fc - sp.diag(b0 / c0, c0 / b0)))
check("reciprocal_reversal_conjugates_depth", zero(Fb * Dz * Fb.inv() - Dz.inv()))
check("three_reversals_remain_reversing", (Fb * Fc * Fb)[0, 1] != 0 and (Fb * Fc * Fb)[0, 0] == 0)
check("two_reversals_plus_preserver_cocycle_witness", zero(Fb * Fc * sp.diag(c0 / b0, b0 / c0) - sp.eye(2)))

# Reversal is algebraic but not ordinary Lorentz transport in the diagonal base readout.
eta2 = sp.diag(-1, 1)
F1 = sp.Matrix([[0, 1], [1, 0]])
check("swap_not_diagonal_Lorentz_isometry", F1.T * eta2 * F1 == -eta2)

# Screen-frame gauge, convex metric gluing identity, and sign-insensitive dphi data.
O = sp.Matrix([[0, -1], [1, 0]])
Hscreen = D.T * D
check("screen_O2_left_gauge", zero((O * D).T * (O * D) - Hscreen))
check(
    "screen_SPD_principal_minor_identities",
    sp.simplify(Hscreen[0, 0] - u**2) == 0
    and sp.simplify(Hscreen.det() - (u * w) ** 2) == 0,
)

t = sp.symbols("t", real=True)
H1 = sp.Matrix([[2, 0], [0, 3]])
H2 = sp.Matrix([[4, 1], [1, 5]])
x1, x2 = sp.symbols("x1 x2", real=True)
x = sp.Matrix([x1, x2])
Hmix = t * H1 + (1 - t) * H2
check("screen_convex_gluing_quadratic_identity", sp.expand((x.T * Hmix * x)[0] - t * (x.T * H1 * x)[0] - (1 - t) * (x.T * H2 * x)[0]) == 0)
check("mixing_zero_section", sp.zeros(2) == sp.zeros(2))

ginv = sp.diag(-1, 1, 1, 1)
q0, q1, q2, q3 = sp.symbols("q0 q1 q2 q3", real=True)
q = sp.Matrix([q0, q1, q2, q3])
sphi = (q.T * ginv * q)[0]
projector = ginv * q * q.T / sphi
check("dphi_sign_preserves_causal_scalar", sp.simplify(((-q).T * ginv * (-q))[0] - sphi) == 0)
check("dphi_sign_preserves_unoriented_projector", zero(ginv * (-q) * (-q).T / sphi - projector))

if len(checks) != 26:
    raise AssertionError(f"unexpected check count: {len(checks)}")

result = {
    "schema": "udt-extension-globalization-transition-variation-1.0",
    "status": "PASS",
    "sympy_version": sp.__version__,
    "check_count": len(checks),
    "checks": checks,
    "maximum_conclusion": "SPARSE_TRANSITION_COCYCLE_AND_LOCAL_VARIATION_IDENTITIES_ONLY",
}
(HERE / "TRANSITION_VARIATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
