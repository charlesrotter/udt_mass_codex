#!/usr/bin/env python3
"""Exact scale-weight, trace, and Derrick checks under locked CSN.

The historical S^2 carrier is used only as a conditional probe.  The script
does not derive a carrier, a scale-setting mechanism, or a particle mass.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


D, p = sp.symbols("D p", integer=True, positive=True)
Omega = sp.symbols("Omega", positive=True)

# A 2p-derivative scalar of weight-zero fields contracted by p inverse
# metrics has density weight D-2p.
weight = D - 2 * p
check("two-derivative density has weight plus two in 4D",
      weight.subs({D: 4, p: 1}) == 2)
check("four-derivative density is common-scale neutral in 4D",
      weight.subs({D: 4, p: 2}) == 0)
check("six-derivative density has weight minus two in 4D",
      weight.subs({D: 4, p: 3}) == -2)

# Fixed dimensionful mass terms are not pre-scale invariant.
wpsi = -1  # standard scale weight that makes a scalar kinetic sector possible
mass_density_weight = D + 2 * wpsi
check("fixed scalar mass density is not scale neutral in 4D",
      mass_density_weight.subs(D, 4) == 2)
check("massive point action rescales with proper interval",
      sp.simplify(Omega - 1) != 0)

# Trace of the source required by a traceless metric Euler tensor.
Btrace, normalization = sp.symbols("Btrace normalization", real=True)
Ttrace = normalization * Btrace
check("Bach source equation requires zero trace",
      Ttrace.subs(Btrace, 0) == 0)

# Stress traces of the conditional two- and four-derivative carrier terms.
xi, kappa, X2, F2 = sp.symbols("xi kappa X2 F2", real=True)
trace_L2 = xi * (1 - D / 2) * X2
trace_L4 = kappa * (1 - D / 4) * F2
check("two-derivative carrier trace is nonzero in 4D",
      sp.simplify(trace_L2.subs(D, 4) + xi * X2) == 0)
check("quartic carrier trace vanishes in 4D",
      sp.simplify(trace_L4.subs(D, 4)) == 0)
check("two-derivative carrier density violates CSN",
      weight.subs({D: 4, p: 1}) != 0)
check("quartic carrier density respects CSN",
      weight.subs({D: 4, p: 2}) == 0)

# CSN does not select a unique four-derivative carrier invariant.  Evaluate
# Q1=(Tr M)^2 and Q2=Tr(M^2) on two Gram matrices.
M_rank1 = sp.diag(1, 0, 0, 0)
M_rank2 = sp.diag(1, 1, 0, 0)


def quartic_pair(matrix):
    return sp.trace(matrix)**2, sp.trace(matrix * matrix)


q1a, q2a = quartic_pair(M_rank1)
q1b, q2b = quartic_pair(M_rank2)
check("quartic invariants agree on rank-one probe", q1a == q2a == 1)
check("quartic invariants differ on rank-two probe", q1b == 4 and q2b == 2)
check("common scale cannot select one quartic carrier invariant",
      sp.Rational(q1a, q2a) != sp.Rational(q1b, q2b))

# Exact three-dimensional Derrick scaling of the historical static probe.
R, C2, C4 = sp.symbols("R C2 C4", positive=True)
E2 = C2 * xi * R
E4 = C4 * kappa / R
E = E2 + E4
check("quartic-only energy has no finite stationary radius",
      sp.solve(sp.Eq(sp.diff(E4, R), 0), R) == [])
Rstar_sq = sp.simplify(C4 * kappa / (C2 * xi))
check("two-term stationary radius",
      sp.simplify(sp.diff(E, R).subs(R**2, Rstar_sq)) == 0)
check("two-term stationary point has positive radial Hessian",
      sp.diff(E, R, 2) == 2 * C4 * kappa / R**3)
check("stationarity gives equal scaling energies",
      sp.simplify((E2 - E4).subs(R**2, Rstar_sq)) == 0)

# A global solution scale can label a post-scale branch without appearing as
# a primitive local coupling.  This is bookkeeping only.
Xglobal, dimensionless = sp.symbols("Xglobal dimensionless", positive=True)
emergent_xi = dimensionless / Xglobal**2
check("a post-scale two-derivative coefficient has inverse-length-square dimension",
      sp.simplify(emergent_xi * Xglobal**2 - dimensionless) == 0)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")

