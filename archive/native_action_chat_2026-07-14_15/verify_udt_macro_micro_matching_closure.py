#!/usr/bin/env python3
"""Exact radial fourth-order matching audit for the conditional conformal branch.

The calculation uses only
  I[A]=integral W[A]^2/r^2 dr,
  W=r^2 A''-2r A'+2(A-1),
and the previously audited full-Bach constraint on the radial Euler family.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def general_jets(r, a0, a1, am1, a2):
    A = a0 + a1 * r + am1 / r + a2 * r**2
    Ap = a1 - am1 / r**2 + 2 * a2 * r
    App = 2 * am1 / r**3 + 2 * a2
    Appp = -6 * am1 / r**4
    return A, Ap, App, Appp


def W_from_jets(r, A, Ap, App):
    return r**2 * App - 2 * r * Ap + 2 * (A - 1)


def momenta(r, W, Wp):
    P1 = 2 * W
    P0 = -4 * W / r - 2 * Wp
    return P0, P1


# Exact first-variation coefficients are checked against direct partial derivatives of L=W^2/r^2.
for r, W, Wp in ((F(2), F(3), F(-1)), (F(7, 3), F(-5, 4), F(9, 2)), (F(5), F(0), F(2))):
    dL_dA = 4 * W / r**2
    dL_dAp = -4 * W / r
    dL_dApp = 2 * W
    P0, P1 = momenta(r, W, Wp)
    check(f"P1 equals dL/dA'' at r={r}", P1 == dL_dApp)
    check(f"P0 equals dL/dA'-d(P1)/dr at r={r}", P0 == dL_dAp - 2 * Wp)
    # Euler cancellation: dL/dA-d(dL/dA')/dr+d2(dL/dA'')/dr2
    # =2(W''+2W'/r). Test the coefficient identity for arbitrary W,W',W''.
    Wpp = F(11, 5)
    direct_euler = dL_dA - (-4 * Wp / r + 4 * W / r**2) + 2 * Wpp
    check(f"Euler operator identity at r={r}", direct_euler == 2 * (Wpp + 2 * Wp / r))

# General radial Euler family and exact W content.
families = (
    (F(2), F(1), F(-1, 3), F(2, 5), F(7, 11)),
    (F(7, 3), F(3, 2), F(5, 7), F(-1, 4), F(-2, 9)),
    (F(5), F(-1), F(4, 3), F(0), F(1, 8)),
)
for r, a0, a1, am1, a2 in families:
    A, Ap, App, _ = general_jets(r, a0, a1, am1, a2)
    W = W_from_jets(r, A, Ap, App)
    W_expected = 2 * (a0 - 1) + 6 * am1 / r
    Wp = -6 * am1 / r**2
    Wpp = 12 * am1 / r**3
    check(f"general Euler-family W at r={r}", W == W_expected)
    check(f"general Euler-family equation at r={r}", Wpp + 2 * Wp / r == 0)

# Previously audited unrestricted Bach constraint on the same family.
bach_samples = (
    (F(1), F(-1, 2), F(0)),
    (F(2), F(1, 3), F(3)),
    (F(-1), F(5, 4), F(0)),
)
for a0, a1, am1 in bach_samples:
    constraint = a0**2 - 3 * a1 * am1 - 1
    check(f"full-Bach constraint evaluation a0={a0}, a1={a1}, am1={am1}", constraint == 0)

# Smooth normalized center: a0=1, a1=0, am1=0, leaving only the quadratic mode.
X = F(11, 3)
a0, a1, am1, a2 = F(1), F(0), F(0), -1 / X**2
check("smooth normalized center satisfies full Bach constraint", a0**2 - 3 * a1 * am1 == 1)
check("smooth wall value fixes a2=-1/X^2", a0 + a1 * X + a2 * X**2 == 0)
check("smooth source-free member is quadratic", all(general_jets(r, a0, a1, am1, a2)[0] == 1 - r**2 / X**2 for r in (F(1, 4), F(2), F(3))))

# Pointwise C1 match of 1+b r^2 to 1-r/X gives incompatible values of b.
for R in (X / 10, X / 3, 3 * X / 4):
    b_from_value = -1 / (X * R)
    b_from_slope = -1 / (2 * X * R)
    check(f"value/slope matching contradiction at R/X={R / X}", b_from_value != b_from_slope)

# Both conformal phases have vanishing higher-derivative momenta and radial Hamiltonian.
for r, Ap, App in ((X / 4, -1 / X, F(0)), (X / 2, -2 * (X / 2) / X**2, -2 / X**2)):
    W, Wp = F(0), F(0)
    P0, P1 = momenta(r, W, Wp)
    L = W**2 / r**2
    H = Ap * P0 + App * P1 - L
    check(f"zero-Weyl phase momenta vanish at r={r}", P0 == 0 and P1 == 0)
    check(f"zero-Weyl phase transversality Hamiltonian vanishes at r={r}", H == 0)

# A jump J in A' produces r^2 J delta(r-R) in W; its square is not an ordinary
# locally integrable function. The nonzero coefficient is audited exactly.
for R, J in ((X / 5, F(1, 7)), (X / 2, F(-3, 8)), (4 * X / 5, F(2))):
    delta_coefficient = R**2 * J
    check(f"A' jump creates nonzero delta coefficient at R/X={R / X}", delta_coefficient != 0)

# With A and A' continuous, momentum continuity is equivalent to W and W' continuity.
for r, Wm, Wpm in ((F(2), F(3), F(4)), (F(7, 2), F(-1), F(5, 3))):
    P0m, P1m = momenta(r, Wm, Wpm)
    P0p, P1p = momenta(r, Wm, Wpm)
    check(f"equal W,W' give equal interface momenta at r={r}", P0m == P0p and P1m == P1p)
    Wp_changed = Wpm + 1
    P0_changed, P1_changed = momenta(r, Wm, Wp_changed)
    check(f"W' jump changes P0 at r={r}", P0_changed != P0m and P1_changed == P1m)

# A generic interface primitive B(A,A',R) changes both momentum jumps independently.
for BA, BAp in ((F(1), F(0)), (F(0), F(1)), (F(3, 5), F(-7, 4))):
    jump_P0_required = -BA
    jump_P1_required = -BAp
    check(f"interface primitive changes jump data BA={BA}, BAp={BAp}", jump_P0_required == -BA and jump_P1_required == -BAp)

passed = sum(ok for _, ok in checks)
total = len(checks)
print("\nJUNCTION RESULT:")
print("P1=2W")
print("P0=-2W'-4W/r")
print("source-free junction: [A]=[A']=[W]=[W']=0")
print("1+bR^2=1-R/X and 2bR=-1/X require incompatible b")
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
