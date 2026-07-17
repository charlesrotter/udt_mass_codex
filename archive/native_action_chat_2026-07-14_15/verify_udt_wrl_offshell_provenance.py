#!/usr/bin/env python3
"""Exact checks for the WR-L off-shell action-provenance audit.

The script verifies action transformations and explicit inverse-variational
countermodels.  It does not declare any member of the family to be UDT physics.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


r, s, R, X = sp.symbols("r s R X", positive=True)
a, b, eps = sp.symbols("a b eps", real=True)
k, A0 = sp.symbols("k A0", nonzero=True, real=True)
lam = sp.symbols("lambda", positive=True)


def Fbig(expr, var):
    """r^2 A'' + r A' - A + 1 in the supplied radial variable."""
    return sp.expand(var**2 * sp.diff(expr, var, 2) + var * sp.diff(expr, var) - expr + 1)


# Off-shell residual re-centering.
y = R + s
g = sp.Function("g")
gy = g(y)
ARg = gy / g(R)
Fs_ARg = sp.simplify(Fbig(ARg, s))
F_at_y = y**2 * sp.diff(gy, s, 2) + y * sp.diff(gy, s) - gy + 1
relation = sp.simplify(
    g(R) * Fs_ARg
    - (
        F_at_y
        - R * (2 * s + R) * sp.diff(gy, s, 2)
        - R * sp.diff(gy, s)
        + g(R) - 1
    )
)
check("exact off-shell re-centering relation", relation == 0)

# The full stationary Euler-Cauchy family and its re-centered residual.
q = sp.symbols("q", positive=True)
A_general_q = 1 + a * q + b / q
check("general stationary family", sp.simplify(Fbig(A_general_q, q)) == 0)
A_general_recentered = sp.simplify(A_general_q.subs(q, R + s) / A_general_q.subs(q, R))
residual_general_recentered = sp.factor(Fbig(A_general_recentered, s))
expected_recentered_residual = (
    b * s**2 * (3 * R + s)
    / ((R + s) ** 3 * (R**2 * a + R + b))
)
check("re-centered singular stationary branch residual",
      sp.simplify(residual_general_recentered - expected_recentered_residual) == 0)
check("regular linear stationary branch is re-centering closed",
      sp.simplify(residual_general_recentered.subs(b, 0)) == 0)

# Explicit off-shell action non-invariance on a fixed-endpoint perturbation.
z = sp.symbols("z", positive=True)
A_pert = 1 - r + eps * r * (1 - r)
L0_pert = sp.Rational(1, 2) * (
    r * sp.diff(A_pert, r) ** 2 + (A_pert - 1) ** 2 / r
)
I0_pert = sp.simplify(sp.integrate(L0_pert, (r, 0, 1)))
A_pert_R = sp.simplify(A_pert.subs(r, R + z) / A_pert.subs(r, R))
L0_pert_R = sp.Rational(1, 2) * (
    z * sp.diff(A_pert_R, z) ** 2 + (A_pert_R - 1) ** 2 / z
)
I0_pert_R = sp.factor(sp.integrate(L0_pert_R, (z, 0, 1 - R)))
I0_pert_R_expected = (
    5 * R**2 * eps**2 - 2 * R * eps**2 + 8 * R * eps + eps**2 + 4
) / (8 * (R * eps + 1) ** 2)
check("perturbed base action", sp.simplify(I0_pert - (eps**2 + 4) / 8) == 0)
check("re-centered perturbed base action",
      sp.simplify(I0_pert_R - I0_pert_R_expected) == 0)
action_difference = sp.factor(I0_pert_R - I0_pert)
expected_action_difference = (
    -R * eps**2 * (eps + 1) * (R * eps - R + 2)
    / (8 * (R * eps + 1) ** 2)
)
check("base action is not off-shell re-centering invariant",
      sp.simplify(action_difference - expected_action_difference) == 0)
check("base action is invariant on exact WR-L",
      sp.simplify(action_difference.subs(eps, 0)) == 0)

# Classification in the narrow quadratic first-derivative class.
B = sp.Function("B")(r)
p = sp.Function("p")(r)
sigma = sp.Function("sigma")(r)
qfun = sp.Function("q")(r)
vB = sp.diff(B, r)
LQ = sp.Rational(1, 2) * p * vB**2 + sigma * B * vB + sp.Rational(1, 2) * qfun * B**2
ELQ = sp.simplify(sp.diff(sp.diff(LQ, vB), r) - sp.diff(LQ, B))
ELQ_expected = p * sp.diff(B, r, 2) + sp.diff(p, r) * vB + (sp.diff(sigma, r) - qfun) * B
check("general quadratic Euler expression", sp.simplify(ELQ - ELQ_expected) == 0)
cross_identity = sigma * B * vB - (
    sp.diff(sigma * B**2 / 2, r) - sp.diff(sigma, r) * B**2 / 2
)
check("quadratic cross term is boundary plus potential", sp.simplify(cross_identity) == 0)
C = sp.symbols("C", nonzero=True)
ELQ_selected = sp.simplify(ELQ.subs({p: C * r, qfun: sp.diff(sigma, r) + C / r}).doit())
F_B = r**2 * sp.diff(B, r, 2) + r * vB - B
check("quadratic class yields WR-L ODE", sp.simplify(r * ELQ_selected - C * F_B) == 0)
check("quadratic kinetic coefficient condition", sp.diff(C * r, r) / (C * r) == 1 / r)

# Explicit strictly nondegenerate local scale-free counterfamily.
yfun = sp.Function("y")(r)
vy = sp.diff(yfun, r)
Fsmall = sp.diff(yfun, r, 2) + vy / r - yfun / r**2
Lbase = sp.Rational(1, 2) * (r * vy**2 + yfun**2 / r)
L6 = (
    r**5 * vy**6 / 480
    - r**3 * yfun**2 * vy**4 / 96
    + r * yfun**4 * vy**2 / 32
    + yfun**6 / (96 * r)
)
ELbase = sp.simplify(sp.diff(sp.diff(Lbase, vy), r) - sp.diff(Lbase, yfun))
EL6 = sp.factor(sp.simplify(sp.diff(sp.diff(L6, vy), r) - sp.diff(L6, yfun)))
Cphase = yfun**2 - r**2 * vy**2
check("base Euler equation", sp.simplify(ELbase - r * Fsmall) == 0)
check("sixth-order counteraction Euler multiplier",
      sp.simplify(EL6 - r * Cphase**2 * Fsmall / 16) == 0)
check("sixth-order counteraction Hessian",
      sp.simplify(sp.diff(L6, vy, 2) - r * Cphase**2 / 16) == 0)
Lfamily = Lbase + lam * L6
ELfamily = sp.factor(sp.simplify(sp.diff(sp.diff(Lfamily, vy), r) - sp.diff(Lfamily, yfun)))
family_multiplier = r * (1 + lam * Cphase**2 / 16)
check("counterfamily has exactly the same ODE",
      sp.simplify(ELfamily - family_multiplier * Fsmall) == 0)
check("counterfamily is strictly nondegenerate",
      sp.simplify(sp.diff(Lfamily, vy, 2) - family_multiplier) == 0)

# Inequivalence: a first-order total derivative has zero velocity Hessian,
# while the family Hessian ratio is field-dependent.
check("counterfamily Hessian ratio is field-dependent",
      sp.diff(1 + lam * Cphase**2 / 16, yfun) != 0)

B_wrl = -r / X
v_wrl = sp.diff(B_wrl, r)
Ibase_wrl = sp.integrate(Lbase.subs(yfun, B_wrl).doit(), (r, 0, X))
I6_wrl = sp.integrate(L6.subs(yfun, B_wrl).doit(), (r, 0, X))
check("base WR-L action value", sp.simplify(Ibase_wrl - sp.Rational(1, 2)) == 0)
check("counteraction WR-L action value", sp.simplify(I6_wrl - sp.Rational(1, 180)) == 0)
pbase = sp.diff(Lbase, vy)
p6 = sp.diff(L6, vy)
pbase_wall = sp.simplify(pbase.subs(yfun, B_wrl).doit().subs(r, X))
p6_wall = sp.simplify(p6.subs(yfun, B_wrl).doit().subs(r, X))
check("base WR-L wall momentum", pbase_wall == -1)
check("counteraction changes WR-L wall momentum", p6_wall == -sp.Rational(1, 30))

# Gauge-fixed depth scaling and a relational reference completion.
Aexpr = sp.Function("H")(r)
check("gauge-fixed ODE is not globally depth-scale invariant",
      sp.simplify(Fbig(k * Aexpr, r) - (k * Fbig(Aexpr, r) + 1 - k)) == 0)

Href = sp.Function("Href")(r)
vH = sp.diff(Href, r)
Lrel = (r * vH**2 + (Href - A0)**2 / r) / (2 * A0**2)
ELrel = sp.simplify(sp.diff(sp.diff(Lrel, vH), r) - sp.diff(Lrel, Href))
Frel = r**2 * sp.diff(Href, r, 2) + r * vH - Href + A0
check("relational reference action Euler equation",
      sp.simplify(A0**2 * r * ELrel - Frel) == 0)

Hscaled, A0scaled = k * Href, k * A0
Lrel_scaled = sp.simplify(
    (r * sp.diff(Hscaled, r)**2 + (Hscaled - A0scaled)**2 / r)
    / (2 * A0scaled**2)
)
check("relational reference action restores simultaneous depth scaling",
      sp.simplify(Lrel_scaled - Lrel) == 0)

H_wrl_ref = A0 * (1 - r / X)
Irel_wrl = sp.integrate(Lrel.subs(Href, H_wrl_ref).doit(), (r, 0, X))
check("relational WR-L action remains scale-degenerate",
      sp.simplify(Irel_wrl - sp.Rational(1, 2)) == 0)
check("reference variation vanishes on relational WR-L",
      sp.simplify(sp.diff(Irel_wrl, A0)) == 0)

# Recheck the most tempting geometric parent under reciprocal reduction.
n = sp.Function("n")(r)
L_reciprocal_reduced = (
    sp.Rational(1, 2) * r**2 * n * sp.diff(n, r)**2
    - n / 4 + n**3 / 4 + sp.Rational(1, 2) * r * n**2 * sp.diff(n, r)
)
EL_reciprocal_reduced = (
    sp.diff(sp.diff(L_reciprocal_reduced, sp.diff(n, r)), r)
    - sp.diff(L_reciprocal_reduced, n)
)
N_wrl = sp.sqrt(1 - r / X)
EL_parent_on_wrl = sp.factor(sp.simplify(EL_reciprocal_reduced.subs(n, N_wrl).doit()))
check("fixed-spatial-metric parent fails reciprocal one-field variation",
      sp.simplify(EL_parent_on_wrl - r * (5 * r - 6 * X) / (8 * X * (X - r))) == 0)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
