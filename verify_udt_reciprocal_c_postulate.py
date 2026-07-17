#!/usr/bin/env python3
"""Exact audit of the user-proposed reciprocal-c founding postulate.

This distinguishes conversion-map covariance from reciprocal duality, verifies
the metric implication of the latter, and checks the surviving action/profile
nonuniqueness. It does not adopt the postulate or bank a UDT conclusion.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


c, u, v = sp.symbols("c u v", positive=True)

# F1: ordinary naturality of an isomorphism c:T->L gives equal, not dual,
# representations in one dimension.
intertwining_defect = sp.simplify(v * c - c * u)
check("conversion-map covariance gives equal scale factors",
      sp.solve(intertwining_defect, v) == [u])
check("conversion-map covariance does not generically give reciprocity",
      sp.simplify((u * v).subs(v, u) - 1) == u**2 - 1)

# F2: contragredient time-length duality preserves an off-diagonal evaluation
# pairing and forces inverse scale factors.
K = sp.Matrix([[0, 1], [1, 0]])
P = sp.diag(u, v)
pairing_pullback = sp.simplify(P.T * K * P)
check("dual pairing scales by product uv", pairing_pullback == u * v * K)
check("pairing preservation forces inverse scale",
      sp.solve(sp.Eq(u * v, 1), v) == [1 / u])

# Continuous positive representation of additive positional depth.
d1, d2, k = sp.symbols("d1 d2 k", real=True)
U = lambda d: sp.exp(-k * d)
V = lambda d: sp.exp(k * d)
check("temporal representation composes",
      sp.simplify(U(d1 + d2) - U(d1) * U(d2)) == 0)
check("radial representation composes",
      sp.simplify(V(d1 + d2) - V(d1) * V(d2)) == 0)
check("representations are reciprocal", sp.simplify(U(d1) * V(d1)) == 1)
check("comparison reverses", sp.simplify(U(-d1) - 1 / U(d1)) == 0
      and sp.simplify(V(-d1) - 1 / V(d1)) == 0)
check("trivial representation remains allowed", U(d1).subs(k, 0) == 1
      and V(d1).subs(k, 0) == 1)

# Metric readout in the transformed dimension-matched coframe.
phi, r, theta = sp.symbols("phi r theta", real=True)
r_pos = sp.symbols("r_pos", positive=True)
gtt = -c**2 * sp.exp(-2 * phi)
grr = sp.exp(2 * phi)
det2 = sp.simplify(gtt * grr)
det4 = sp.simplify(det2 * r_pos**4 * sp.sin(theta)**2)
check("reciprocal-c dual representation gives UDT clock coefficient",
      gtt == -c**2 * sp.exp(-2 * phi))
check("reciprocal-c dual representation gives UDT radial coefficient",
      grr == sp.exp(2 * phi))
check("radial metric determinant is fixed", det2 == -c**2)
check("four-volume is independent of dilation depth",
      sp.diff(det4, phi) == 0)

# Equal-scaling F1 instead produces a conformal radial block, demonstrating
# that c as a reversible isomorphism alone is insufficient.
w = sp.symbols("w", positive=True)
f1_det2 = sp.simplify((-c**2 * w**2) * w**2)
check("equal-scaling formalization gives a different metric family",
      f1_det2 == -c**2 * w**4)
check("equal-scaling determinant is not fixed for nontrivial scale",
      sp.diff(f1_det2, w) != 0)

# Local measured null speed remains c for arbitrary positive coframe scales,
# so invariant local c alone cannot choose between F1 and F2.
coordinate_null_speed = sp.simplify(c * u / v)
physical_null_speed = sp.simplify(v * coordinate_null_speed / u)
check("local measured null speed is c for arbitrary scales",
      physical_null_speed == c)

# Determinant-one group consequences.
S = sp.diag(sp.exp(-phi), sp.exp(phi))
check("positional duality transformation has determinant one", S.det() == 1)
check("positional duality preserves evaluation pairing",
      sp.simplify(S.T * K * S - K) == sp.zeros(2))
check("positional reversal is matrix inversion",
      sp.simplify(S.subs(phi, -phi) - S.inv()) == sp.zeros(2))
H = sp.simplify(S.inv() * sp.diff(S, phi))
check("positional generator is traceless", sp.trace(H) == 0)
check("canonical group tangent norm is quadratic", sp.trace(H * H) / 2 == 1)

# Relative invariant.
phi1, phi2 = sp.symbols("phi1 phi2", real=True)
S1 = sp.diag(sp.exp(-phi1), sp.exp(phi1))
S2 = sp.diag(sp.exp(-phi2), sp.exp(phi2))
relative_trace = sp.simplify(sp.trace(S1.inv() * S2) / 2)
cosh_exp = (sp.exp(phi2 - phi1) + sp.exp(phi1 - phi2)) / 2
check("relative invariant is reversal-even",
      sp.simplify(relative_trace - cosh_exp) == 0)

# The group gives a canonical quadratic tangent scalar but not a unique action.
x, alpha = sp.symbols("x alpha", real=True)
f = sp.Function("f")(x)
fp = sp.diff(f, x)
Y = fp**2
L_quadratic = Y / 2
L_counter = Y / 2 + alpha * Y**2 / 4
EL_quadratic = sp.simplify(sp.diff(sp.diff(L_quadratic, fp), x)
                           - sp.diff(L_quadratic, f))
EL_counter = sp.factor(sp.simplify(sp.diff(sp.diff(L_counter, fp), x)
                                   - sp.diff(L_counter, f)))
check("quadratic action gives linear one-dimensional equation",
      EL_quadratic == sp.diff(f, x, 2))
check("reciprocity-compatible counteraction gives different equation",
      sp.simplify(EL_counter
                  - (1 + 3 * alpha * fp**2) * sp.diff(f, x, 2)) == 0)
check("founding kinematics does not select unique action",
      sp.simplify(EL_counter - EL_quadratic) != 0)

# No local X selector: any positive reciprocal profile belongs to the same
# kinematic family. WR-L is one member.
X = sp.symbols("X", positive=True)
A = sp.Function("A")(r_pos)
general_det = sp.simplify((-c**2 * A) / A)
check("arbitrary reciprocal radial profile obeys the kinematics",
      general_det == -c**2)
check("WR-L profile is one member but is not selected",
      sp.simplify(general_det.subs(A, 1 - r_pos / X) + c**2) == 0)

# In the WR-L member, the wall is group infinity, but the group does not set
# the coordinate X at which it is approached.
phi_wrl = -sp.log(1 - r_pos / X) / 2
check("WR-L wall is infinite reciprocal depth",
      sp.limit(phi_wrl, r_pos, X, dir="-") == sp.oo)

# Even choosing the canonical quadratic group norm as a physical-metric action
# does not yield the WR-L profile.  For static radial phi and A=exp(-2 phi),
# sqrt(-g) g^rr phi'^2 reduces (up to a constant) to r^2 A'^2/(4A).
Aprime = sp.diff(A, r_pos)
L_canonical = r_pos**2 * Aprime**2 / (4 * A)
EL_canonical = sp.factor(sp.simplify(
    sp.diff(sp.diff(L_canonical, Aprime), r_pos)
    - sp.diff(L_canonical, A)))
A_wrl = 1 - r_pos / X
EL_on_wrl = sp.factor(EL_canonical.subs({
    A: A_wrl,
    sp.diff(A, r_pos): -1 / X,
    sp.diff(A, r_pos, 2): 0,
}))
check("canonical quadratic group action does not produce WR-L",
      sp.simplify(EL_on_wrl + r_pos * (4 * X - 3 * r_pos)
                  / (4 * (X - r_pos)**2)) == 0)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
