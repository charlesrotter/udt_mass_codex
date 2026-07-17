#!/usr/bin/env python3
"""Exact one-coordinate jet audit for the conditional reciprocal-axis metric.

This verifier reuses the already-audited full four-dimensional tensor constructor, but tests a
strictly larger manufactured jet:

  q=q(z), n=(cos(theta(z)), sin(theta(z)), 0).

At the evaluation point theta=0, write u=q', v=q'', p=theta', s=theta''. All calculations use
fractions. No finite differences or linearization are used.
"""

import contextlib
import io
import runpy
from fractions import Fraction as F


with contextlib.redirect_stdout(io.StringIO()):
    curvature = runpy.run_path("verify_udt_reciprocal_axis_metric_curvature.py")["curvature"]


def expected(q, u, v, p, s):
    q, u, v, p, s = map(F, (q, u, v, p, s))
    d = q - 1

    scalar = -u**2 / (2 * q**2) - d**2 * p**2 / (2 * q)

    ricci2 = (
        v**2 / (2 * q**2)
        + d**2 * s**2 / (2 * q)
        - v * u**2 / q**3
        - d * (q + 1) * v * p**2 / (2 * q**2)
        + d * (q + 1) * s * u * p / q**2
        + 3 * u**4 / (4 * q**4)
        + (3 * q**2 + 1) * u**2 * p**2 / (2 * q**3)
        + d**2 * (3 * q**2 + 2 * q + 3) * p**4 / (4 * q**2)
    )

    riemann2 = (
        2 * v**2 / q**2
        + 2 * d**2 * s**2 / q
        - 4 * v * u**2 / q**3
        - d * (q + 3) * v * p**2 / q**2
        + 2 * d * (3 * q + 1) * s * u * p / q**2
        + 11 * u**4 / (4 * q**4)
        + (11 * q**2 + 6 * q - 1) * u**2 * p**2 / (2 * q**3)
        + d**2 * (11 * q**2 + 10 * q + 11) * p**4 / (4 * q**2)
    )

    # Manifestly nonnegative sum of squares in this static one-coordinate sector.
    weyl2 = (
        (v / q - u**2 / q**2 - d * p**2 / q) ** 2
        + (d * s + 2 * u * p) ** 2 / q
        + (u**2 - d * q * (2 * q + 1) * p**2) ** 2 / (3 * q**4)
    )

    return {"R": scalar, "Ricci2": ricci2, "Riemann2": riemann2, "Weyl2": weyl2}


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


jets = (
    (F(3, 2), 0, 1, 0, 0),
    (F(3, 2), 0, 0, 0, 1),
    (F(2), 1, 1, 0, 0),
    (F(2), 0, 1, 1, 0),
    (F(2), 1, 0, 1, 1),
    (F(9, 4), 1, 0, 0, 0),
    (F(9, 4), 1, 0, 1, 0),
    (F(3), 0, 0, 1, 0),
    (F(7, 5), 2, -3, 4, -5),
    (F(11, 4), -2, 3, -1, 4),
    (F(1), 3, 2, 5, 7),
    (F(6), 1, 2, 3, 4),
)

actual = []
for q, u, v, p, s in jets:
    out = curvature(q, p, s, u, v)
    actual.append(out)

check("all full-tensor audits pass at all manufactured jets", all(all(o["audits"].values()) for o in actual))
for key in ("R", "Ricci2", "Riemann2", "Weyl2"):
    check(
        f"exact closed form for {key} at all manufactured jets",
        all(o[key] == expected(q, u, v, p, s)[key] for o, (q, u, v, p, s) in zip(actual, jets)),
    )

check(
    "Weyl contraction identity at all manufactured jets",
    all(o["Weyl2"] == o["Riemann2"] - 2 * o["Ricci2"] + o["R"] ** 2 / 3 for o in actual),
)
check("one-coordinate Weyl density is nonnegative at all probes", all(o["Weyl2"] >= 0 for o in actual))

# Principal second-jet tests: first jets vanish while one second jet remains.
q0 = F(9, 4)
depth_second = curvature(q0, 0, 0, 0, 1)
axis_second = curvature(q0, 0, 1, 0, 0)
check("pure depth second jet has nonzero Weyl density", depth_second["Weyl2"] == 1 / q0**2)
check("pure axis second jet has nonzero Weyl density", axis_second["Weyl2"] == (q0 - 1) ** 2 / q0)

# Constant-q orientation functional L=a theta''^2+b theta'^4.
a = (q0 - 1) ** 2 / q0
b = 4 * (q0 - 1) ** 2 * (q0**2 + q0 + 1) / (3 * q0**2)
for p, s in ((F(0), F(0)), (F(2, 3), F(5, 7)), (F(-4, 5), F(3, 2))):
    out = curvature(q0, p, s)
    check(f"constant-q reduced density at p={p}, s={s}", out["Weyl2"] == a * s**2 + b * p**4)

check(
    "constant-q reduced Euler coefficient",
    6 * b / a == 8 * (q0**2 + q0 + 1) / q0,
)

# Constant-axis pure-depth sector. With y=ln(q), y'=u/q and
# y''=v/q-u^2/q^2, C^2=y''^2+y'^4/3.
for q, u, v in ((F(3, 2), F(2), F(-1)), (F(2), F(-3), F(4)), (F(5), F(1, 3), F(7, 2))):
    out = curvature(q, 0, 0, u, v)
    y1 = u / q
    y2 = v / q - u**2 / q**2
    check(f"pure-depth log formula at q={q}", out["Weyl2"] == y2**2 + y1**4 / 3)

# Every derivative jet scales with its derivative order, so C^2 is homogeneous of order four.
q, u, v, p, s = F(7, 3), F(2), F(-1), F(3), F(4)
scale = F(5, 2)
unscaled = curvature(q, p, s, u, v)["Weyl2"]
scaled = curvature(q, p / scale, s / scale**2, u / scale, v / scale**2)["Weyl2"]
check("Weyl density scales as inverse length to the fourth", scaled == unscaled / scale**4)
check("three-dimensional static integral scales as inverse size", scaled * scale**3 == unscaled / scale)

# The metric-axis topology is not protected when the anisotropy can reach q=1.
for q in (F(1, 4), F(3, 2), F(7)):
    for t in (F(0), F(1, 5), F(1, 2), F(1)):
        qt = 1 + t * (q - 1)
        check(f"positive homotopy q={q}, t={t}", qt > 0)

check("isotropic endpoint erases constant-q axis curvature", curvature(F(1), F(3), F(5))["Weyl2"] == 0)

passed = sum(ok for _, ok in checks)
total = len(checks)
print("\nEXACT ONE-COORDINATE WEYL DENSITY:")
print("C2=(v/q-u^2/q^2-(q-1)p^2/q)^2")
print("   +((q-1)s+2up)^2/q")
print("   +(u^2-(q-1)q(2q+1)p^2)^2/(3q^4)")
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
