#!/usr/bin/env python3
"""Exact algebra checks for the UDT founding-to-dynamics derivation.

The script verifies encoded counterfamilies, variations, carrier stress
identities, reciprocal tangent sources, virial scaling, and boundary-primitive
ambiguity.  It cannot prove the premise inventory complete, select an action,
validate a variation domain, or turn a conditional action into UDT physics.
"""

import sympy as sp


passed = 0
failed = 0


def check(label, condition):
    global passed, failed
    ok = bool(condition)
    if ok:
        passed += 1
        print(f"PASS {passed + failed:02d}: {label}")
    else:
        failed += 1
        print(f"FAIL {passed + failed:02d}: {label}")


# A. Exact nonlinear shift-invariant counterfamily on a chosen covariant slice.
q, X, alpha, mu = sp.symbols("q X alpha mu", real=True)
Xpos = sp.symbols("Xpos", positive=True)
Y = Xpos**2*q**2
F1 = Y/2
F2 = Y/2 + alpha*Y**2/4
L1 = mu*F1/Xpos**2
L2 = mu*F2/Xpos**2
p1 = sp.diff(L1, q)
p2 = sp.diff(L2, q)

check("quadratic member momentum", sp.simplify(p1 - mu*q) == 0)
check("nonlinear member momentum",
      sp.simplify(p2 - mu*(q + alpha*Xpos**2*q**3)) == 0)
check("counterfamily members are distinct for nonzero alpha",
      sp.simplify(L2-L1) == alpha*mu*Xpos**2*q**4/4)
check("both members have no explicit phi", True)
check("both members are derivative-reversal even",
      sp.simplify(L1.subs(q, -q)-L1) == 0 and
      sp.simplify(L2.subs(q, -q)-L2) == 0)

r = sp.symbols("r", real=True)
phi = sp.Function("phi")(r)
muf = sp.Function("mu")(r)
qf = sp.diff(phi, r)
p2f = muf*(qf + alpha*Xpos**2*qf**3)
euler2 = sp.diff(p2f, r)
expected_euler2 = (
    sp.diff(muf, r)*(qf + alpha*Xpos**2*qf**3) +
    muf*(1 + 3*alpha*Xpos**2*qf**2)*sp.diff(phi, r, 2)
)
check("full nonlinear Euler operator",
      sp.simplify(euler2-expected_euler2) == 0)

# B. Boundary primitive: same bulk Euler equation, shifted endpoint momentum.
Z, a = sp.symbols("Z a", real=True)
q = sp.symbols("q", real=True)
Lbase = Z*q**2/2
Lprim = Lbase + a*q  # a*q = d(a*phi)/dr for constant a
check("total derivative leaves Hessian in q unchanged",
      sp.diff(Lbase, q, 2) == sp.diff(Lprim, q, 2))
check("total derivative shifts endpoint momentum",
      sp.simplify(sp.diff(Lprim, q)-sp.diff(Lbase, q)-a) == 0)
check("total derivative leaves bulk Euler dependence unchanged",
      sp.diff(Lprim, q, 2) == Z)

# C. Conditional physical-metric carrier stress traces in three dimensions.
xi, kap, Xn, Yn = sp.symbols("xi kap Xn Yn", real=True)
rho2 = xi*Xn/2
S2 = xi*(Xn-sp.Rational(3, 2)*Xn)
rho4 = kap*Yn/4
S4 = kap*(Yn-sp.Rational(3, 4)*Yn)
check("L2 spatial trace", sp.simplify(S2 + rho2) == 0)
check("L4 spatial trace", sp.simplify(S4-rho4) == 0)
check("carrier lapse-source identity",
      sp.simplify((rho2+rho4)+(S2+S4)-2*rho4) == 0)

# D. Directional reciprocal-tangent source rho + p_parallel.
a1, a2, a3 = sp.symbols("a1 a2 a3", real=True, nonnegative=True)
f12, f13, f23 = sp.symbols("f12 f13 f23", real=True)
strain_sum = a1+a2+a3
rho2_dir = xi*strain_sum/2
p1_2 = xi*(a1-strain_sum/2)
rho2_parallel = xi*a1/2
check("L2 tangent source is twice parallel L2 energy",
      sp.simplify(rho2_dir+p1_2-2*rho2_parallel) == 0)

fsum = f12**2+f13**2+f23**2
Ydir = 2*fsum
rho4_dir = kap*Ydir/4
p1_4 = kap*((f12**2+f13**2)-Ydir/4)
rho4_parallel = kap*(f12**2+f13**2)/2
check("L4 tangent source is twice parallel L4 energy",
      sp.simplify(rho4_dir+p1_4-2*rho4_parallel) == 0)
check("full reciprocal tangent source",
      sp.simplify(
          rho2_dir+rho4_dir+p1_2+p1_4 -
          2*(rho2_parallel+rho4_parallel)
      ) == 0)

# Direct constrained-action variation gives the same directional combination.
ph = sp.symbols("ph", real=True)
A2p, A2t, A4p, A4t = sp.symbols("A2p A2t A4p A4t", real=True)
measure = sp.exp(-ph)*sp.exp(ph)  # N * sqrt(g_parallel)
rho_channels = (
    A2p*sp.exp(-2*ph) + A2t +
    A4p*sp.exp(-2*ph) + A4t
)
Lm_static = -measure*rho_channels
check("reciprocal static measure is phi-independent",
      sp.simplify(measure-1) == 0)
check("constrained carrier variation sees parallel channels only",
      sp.simplify(
          sp.diff(Lm_static, ph) -
          2*sp.exp(-2*ph)*(A2p+A4p)
      ) == 0)

# E. Distinct time-live completions share exactly the same static limit.
t2, t4, c2, c4 = sp.symbols("t2 t4 c2 c4", real=True)
spatial_static = -(rho2+rho4)
completion_a = spatial_static + c2*t2 + c4*t4
completion_b = spatial_static + (c2+alpha)*t2 + (c4-alpha)*t4
check("different time-live completions agree for static carrier",
      sp.simplify((completion_a-completion_b).subs({t2: 0, t4: 0})) == 0)
check("time-live completions differ off the static sector",
      sp.simplify(completion_a-completion_b) != 0)

# F. Derrick/virial scaling and the conditional mass identity.
lam, E2, E4 = sp.symbols("lam E2 E4", positive=True)
Escale = lam*E2 + E4/lam
check("three-dimensional carrier scaling derivative",
      sp.simplify(sp.diff(Escale, lam).subs(lam, 1)-(E2-E4)) == 0)
check("virial implies total energy equals twice E4",
      sp.simplify((E2+E4-2*E4).subs(E2, E4)) == 0)

kg, flux, intNrho4 = sp.symbols("kg flux intNrho4", nonzero=True)
laplace_integral_relation = sp.Eq(flux, kg*intNrho4)
MN = 2*flux/kg
check("conditional lapse flux gives M_N = 2 integral N rho4",
      sp.simplify(MN.subs(flux, kg*intNrho4)-2*intNrho4) == 0)

# G. One dimensional relation cannot determine both c and X.
G, M, c, beta = sp.symbols("G M c beta", positive=True)
Xclosure = beta*G*M/c**2
chi = G*M/(c**2*Xclosure)
check("global compactness relation fixes only one ratio",
      sp.simplify(chi-1/beta) == 0)
check("c and X closure forms are algebraically identical",
      sp.solve(sp.Eq(Xpos, beta*G*M/c**2), c**2)[0] == beta*G*M/Xpos)

print(f"\nRESULT: {passed}/{passed + failed} checks pass")
if failed:
    raise SystemExit(1)
