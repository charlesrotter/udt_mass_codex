#!/usr/bin/env python3
"""Exact checks for the reverse-engineered positional-relativity principle.

The script verifies group composition, measure preservation, trace-free
variations, and counteraction algebra. It does not adopt the candidate
principle or derive a unique action.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


d1, d2, a, b = sp.symbols("d1 d2 a b", real=True)
c, r, theta = sp.symbols("c r theta", positive=True)
phi, dphi = sp.symbols("phi dphi", real=True)

# Continuous positive representations of additive positional depth.
T = lambda d: sp.exp(a * d)
R = lambda d: sp.exp(b * d)
check("clock comparison composes", sp.simplify(T(d1 + d2) - T(d1) * T(d2)) == 0)
check("ruler comparison composes", sp.simplify(R(d1 + d2) - R(d1) * R(d2)) == 0)
check("clock comparison reverses", sp.simplify(T(-d1) - 1 / T(d1)) == 0)
check("ruler comparison reverses", sp.simplify(R(-d1) - 1 / R(d1)) == 0)
check("positional relativity alone leaves two exponents", sp.simplify(T(d1) * R(d1) - sp.exp((a + b) * d1)) == 0)

# Invariant radial causal measure fixes reciprocal exponents.
TR_balanced = sp.simplify((T(d1) * R(d1)).subs(b, -a))
check("measure preservation fixes reciprocal exponent", TR_balanced == 1)
T_normalized = T(d1).subs(a, -1)
R_normalized = R(d1).subs({a: -1, b: 1})
check("normalized clock factor", T_normalized == sp.exp(-d1))
check("normalized ruler factor", R_normalized == sp.exp(d1))
check("trivial no-dilation branch remains allowed", T(d1).subs(a, 0) == 1 and R(d1).subs(b, 0) == 1)

# Metric determinant and volume form.
gtt = -c**2 * sp.exp(-2 * phi)
grr = sp.exp(2 * phi)
det2 = sp.simplify(gtt * grr)
det4 = sp.simplify(det2 * r**4 * sp.sin(theta) ** 2)
check("radial metric determinant is fixed", det2 == -c**2)
check("four-metric determinant is depth independent", det4 == -c**2 * r**4 * sp.sin(theta) ** 2)
check("four-volume density is depth independent",
      sp.sqrt(-det4) == c * r**2 * sp.Abs(sp.sin(theta)))

# Determinant-one deformation matrix and its invariant trace data.
S = sp.diag(sp.exp(-phi), sp.exp(phi))
check("positional deformation has determinant one", S.det() == 1)
phi1, phi2 = sp.symbols("phi1 phi2", real=True)
S1 = sp.diag(sp.exp(-phi1), sp.exp(phi1))
S2 = sp.diag(sp.exp(-phi2), sp.exp(phi2))
check("deformation matrices compose additively",
      sp.simplify(S1 * S2 - sp.diag(sp.exp(-(phi1 + phi2)), sp.exp(phi1 + phi2))) == sp.zeros(2))
relative = sp.simplify(S1.inv() * S2)
check("relative normalized trace is reciprocal cosh",
      sp.simplify(sp.trace(relative) / 2
                  - (sp.exp(phi2 - phi1) + sp.exp(phi1 - phi2)) / 2) == 0)

# Maurer-Cartan trace norm.
q = sp.symbols("q", real=True)
Sq = sp.diag(sp.exp(-q), sp.exp(q))
J = sp.simplify(Sq.inv() * sp.diff(Sq, q))
check("group current is traceless", sp.trace(J) == 0)
check("group trace norm is quadratic", sp.trace(J * J) / 2 == 1)

# Reciprocal tangent variations are trace free and preserve volume.
dgtt = sp.diff(gtt, phi) * dphi
dgrr = sp.diff(grr, phi) * dphi
trace_variation = sp.simplify((1 / gtt) * dgtt + (1 / grr) * dgrr)
check("reciprocal metric tangent is trace free", trace_variation == 0)
check("metric volume has zero reciprocal variation", sp.diff(sp.sqrt(-det4), phi) == 0)

# Generic diagonal matter contraction under reciprocal tangent variation.
rho, pr = sp.symbols("rho p_r", real=True)
# T^{tt} g_tt = T^t_t = -rho; T^{rr} g_rr = T^r_r = p_r.
source_contraction = sp.simplify((-rho) * (dgtt / gtt) + pr * (dgrr / grr))
check("reciprocal tangent selects rho plus radial pressure",
      sp.simplify(source_contraction - 2 * (rho + pr) * dphi) == 0)

# Local measured light speed is c for any positive diagonal clock/ruler factors;
# therefore invariant local c alone does not force TR=1.
C, D = sp.symbols("C D", positive=True)
coordinate_null_speed = c * sp.sqrt(C / D)
local_speed = sp.simplify(sp.sqrt(D) * coordinate_null_speed / sp.sqrt(C))
check("local measured null speed is automatically c", local_speed == c)

# In areal radius, a constant static time rescaling cannot remove radial
# dependence of the product C(r)D(r).
kappa = sp.symbols("kappa", positive=True)
Cfun = sp.Function("C")(r)
Dfun = sp.Function("D")(r)
old_log_derivative = sp.diff(sp.log(Cfun * Dfun), r)
new_log_derivative = sp.diff(sp.log(Cfun * Dfun / kappa**2), r)
check("constant clock rescaling cannot remove product profile",
      sp.simplify(new_log_derivative - old_log_derivative) == 0)

# The group norm supplies an invariant scalar, but arbitrary functions of it
# remain measure-preserving and reciprocal.
x, alpha = sp.symbols("x alpha", real=True)
f = sp.Function("f")(x)
vf = sp.diff(f, x)
Y = vf**2
L1 = Y / 2
L2 = Y / 2 + alpha * Y**2 / 4
EL1 = sp.simplify(sp.diff(sp.diff(L1, vf), x) - sp.diff(L1, f))
EL2 = sp.factor(sp.simplify(sp.diff(sp.diff(L2, vf), x) - sp.diff(L2, f)))
check("quadratic invariant-strain Euler equation", EL1 == sp.diff(f, x, 2))
check("nonlinear invariant-strain counteraction",
      sp.simplify(EL2 - (1 + 3 * alpha * vf**2) * sp.diff(f, x, 2)) == 0)
check("candidate causal-measure principle does not select action",
      sp.simplify(EL2 - EL1) != 0)

# The local principle contains no X and allows arbitrary depth profiles.
X = sp.symbols("X", positive=True)
Afun = sp.Function("Afun")(r)
general_reciprocal_det = sp.simplify((-c**2 * Afun) * (1 / Afun))
check("arbitrary reciprocal profile preserves measure", general_reciprocal_det == -c**2)
A_wrl = 1 - r / X
check("WR-L is one member, not selected by local measure",
      sp.simplify(general_reciprocal_det.subs(Afun, A_wrl) + c**2) == 0)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
