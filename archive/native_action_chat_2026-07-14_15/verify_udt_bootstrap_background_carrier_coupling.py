#!/usr/bin/env python3
"""Exact bootstrap-depth / reciprocal-axis coupling audit.

The full four-dimensional tensor constructor is evaluated for q=q(z) and an axis whose base
direction is parallel or transverse to grad(q). Fractions only; no fitted densities, finite
differences, or linearization of q are used.
"""

import contextlib
import io
import runpy
from fractions import Fraction as F


with contextlib.redirect_stdout(io.StringIO()):
    curvature = runpy.run_path("verify_udt_reciprocal_axis_metric_curvature.py")["curvature"]
with contextlib.redirect_stdout(io.StringIO()):
    transverse_expected = runpy.run_path("verify_udt_reciprocal_axis_functional_structure.py")["expected"]


def parallel_expected(q, u, v, p, s):
    q, u, v, p, s = map(F, (q, u, v, p, s))
    d = q - 1
    R = v / q**2 - 2 * u**2 / q**3 - 2 * d * p**2 / q
    Ricci2 = (
        v**2 / (2 * q**4)
        - 2 * v * u**2 / q**5
        - d * v * p**2 / q**3
        + 2 * u**4 / q**6
        + 2 * d * u**2 * p**2 / q**4
        + 2 * d**2 * p**4 / q**2
    )
    Riemann2 = (q * v - 2 * u**2) ** 2 / q**6 + 4 * d**2 * p**4 / q**2
    Weyl2 = (q * v - 2 * u**2 + q**2 * d * p**2) ** 2 / (3 * q**6) + d**2 * p**4 / q**2
    return {"R": R, "Ricci2": Ricci2, "Riemann2": Riemann2, "Weyl2": Weyl2}


def parallel_carrier_coefficients(q, u, v):
    q, u, v = map(F, (q, u, v))
    d = q - 1
    K = 2 * d * (q * v - 2 * u**2) / (3 * q**4)
    c = 4 * d**2 / (3 * q**2)
    return K, c


def transverse_carrier_coefficients(q, u, v):
    q, u, v = map(F, (q, u, v))
    d = q - 1
    a = d**2 / q
    cross = 4 * d * u / q
    Kraw = -2 * d * v / q**2 + 4 * u**2 / q - 4 * d**2 * u**2 / (3 * q**3)
    cross_half_derivative = 2 * (d * v / q + u**2 / q**2)
    Keff = Kraw - cross_half_derivative
    Keff_closed = -2 * d * (q + 1) * v / q**2 + 2 * (4 * q**2 + q - 2) * u**2 / (3 * q**3)
    c = 4 * d**2 * (q**2 + q + 1) / (3 * q**2)
    return a, cross, Kraw, Keff, Keff_closed, c


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


jets = (
    (F(3, 2), 0, 1, 0, 1),
    (F(2), 1, 1, 0, -3),
    (F(2), 0, 1, 1, 5),
    (F(9, 4), 1, 0, 1, -2),
    (F(3), 0, 0, 1, 7),
    (F(7, 5), 2, -3, 4, -5),
    (F(11, 4), -2, 3, -1, 4),
    (F(1), 3, 2, 5, 7),
    (F(6), 1, 2, 3, 4),
)

parallel_outputs = [curvature(q, p, s, u, v, True) for q, u, v, p, s in jets]
check("all parallel full-tensor audits pass", all(all(out["audits"].values()) for out in parallel_outputs))
for key in ("R", "Ricci2", "Riemann2", "Weyl2"):
    check(
        f"parallel exact closed form for {key}",
        all(out[key] == parallel_expected(q, u, v, p, s)[key] for out, (q, u, v, p, s) in zip(parallel_outputs, jets)),
    )

check("parallel invariants are independent of theta second jet", all(
    curvature(q, p, F(13, 7), u, v, True)["Weyl2"] == curvature(q, p, F(-9, 5), u, v, True)["Weyl2"]
    for q, u, v, p, _s in jets
))

for q, u, v, p, s in jets:
    background = curvature(q, 0, 0, u, v, True)["Weyl2"]
    delta = curvature(q, p, s, u, v, True)["Weyl2"] - background
    K, c = parallel_carrier_coefficients(q, u, v)
    check(f"parallel carrier expansion q={q}, p={p}", delta == K * p**2 + c * p**4)

# Transverse expansion and integration-by-parts coefficient.
for q, u, v, p, s in jets:
    out = curvature(q, p, s, u, v, False)
    background = curvature(q, 0, 0, u, v, False)["Weyl2"]
    a, cross, Kraw, Keff, Keff_closed, c = transverse_carrier_coefficients(q, u, v)
    delta = out["Weyl2"] - background
    check(f"transverse raw carrier expansion q={q}, p={p}", delta == a * s**2 + cross * p * s + Kraw * p**2 + c * p**4)
    check(f"transverse integrated coefficient identity q={q}", Keff == Keff_closed)
    check(f"transverse full invariant agrees with prior exact formula q={q}", out["Weyl2"] == transverse_expected(q, u, v, p, s)["Weyl2"])

# Dimensionless WR-L profile: q=1/(1-x), u=q^2, v=2q^3.
for x in (F(1, 10), F(1, 4), F(1, 2), F(3, 4)):
    q = 1 / (1 - x)
    u = q**2
    v = 2 * q**3
    Kp, cp = parallel_carrier_coefficients(q, u, v)
    check(f"WR-L parallel quadratic coefficient vanishes x={x}", Kp == 0)
    check(f"WR-L parallel quartic coefficient x={x}", cp == 4 * x**2 / 3)

q_inner = 1 / (1 - F(1, 4))
q_outer = 1 / (1 - F(1, 2))
u_inner, v_inner = q_inner**2, 2 * q_inner**3
u_outer, v_outer = q_outer**2, 2 * q_outer**3
Kt_inner = transverse_carrier_coefficients(q_inner, u_inner, v_inner)[3]
Kt_outer = transverse_carrier_coefficients(q_outer, u_outer, v_outer)[3]
check("WR-L transverse effective coefficient positive at x=1/4", Kt_inner > 0)
check("WR-L transverse effective coefficient negative at x=1/2", Kt_outer < 0)

# Dimensionless smooth profile: q=1/(1-x^2), u=2x q^2,
# v=2q^2+8x^2 q^3.
for x in (F(1, 10), F(1, 4), F(1, 2), F(3, 4)):
    q = 1 / (1 - x**2)
    u = 2 * x * q**2
    v = 2 * q**2 + 8 * x**2 * q**3
    Kp, cp = parallel_carrier_coefficients(q, u, v)
    a, _cross, _Kraw, Kt, _Ktclosed, ct = transverse_carrier_coefficients(q, u, v)
    check(f"smooth parallel quadratic coefficient x={x}", Kp == 4 * x**2 / 3)
    check(f"smooth parallel quartic coefficient x={x}", cp == 4 * x**4 / 3)
    check(f"smooth parallel coefficients are positive x={x}", Kp > 0 and cp > 0)
    check(f"smooth transverse highest terms are positive x={x}", a > 0 and ct > 0)
    check(f"smooth transverse effective coefficient is negative x={x}", Kt < 0)

# A positive two-derivative coefficient and a positive four-derivative coefficient have the
# scale balance E(R)=A2*R/X^2+A4/R, stationary at R/X=sqrt(A4/A2).
for A2, A4 in ((F(1), F(1)), (F(3, 2), F(2, 3)), (F(7), F(5, 4))):
    sigma2 = A4 / A2
    check(f"positive formal scale-balance ratio A2={A2}, A4={A4}", sigma2 > 0)

passed = sum(ok for _, ok in checks)
total = len(checks)
print("\nPARALLEL CARRIER EXPANSION:")
print("Delta C2 = K_parallel*(theta')^2 + c_parallel*(theta')^4")
print("K_parallel=2(q-1)(q q''-2 q'^2)/(3 q^4)")
print("c_parallel=4(q-1)^2/(3 q^2)")
print("WR-L: K_parallel=0")
print("smooth q=1/(1-x^2): K_parallel=4x^2/(3X^2), c_parallel=4x^4/3")
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
