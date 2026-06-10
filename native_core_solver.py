"""Self-consistent softened-core profile from localized angular source.

This is the first nontrivial "ensemble" profile solve:

    f = e^{-2 phi}
    phi'' + 2 phi'/r - 2(phi')^2 = s W(r) / r^2

In f this is

    f'' + 2 f'/r + 2 s W(r) f/r^2 = 0.

With x=ln r:

    f_xx + f_x + 2 s W(x) f = 0.

For W=1 near the core, f ~ r^-p with p(1-p)/2=s. The finite-action
branch is p<1/2. For W=0 outside the core, f=A+B/r, so after normalization
the exterior is asymptotically flat, f -> 1 + a/r.

This is not yet a derivation of W or s. It tests whether the candidate
postulate "localized angular source" can actually produce the desired
finite-action negative-phi core matched to a UDT exterior.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class Sector:
    label: str
    angular_lambda: float
    degeneracy: int


def ordinary_sector(ell: int) -> Sector:
    return Sector(f"ell={ell}", float(ell * (ell + 1)), 2 * ell + 1)


def monopole_sector(n: int, k: int = 0) -> Sector:
    spin = abs(n) / 2.0
    j = spin + k
    lam = j * (j + 1.0) - spin * spin
    return Sector(f"monopole n={n} k={k} j={j:g}", lam, int(round(2.0 * j + 1.0)))


def p_roots(source: float):
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    root = math.sqrt(max(disc, 0.0))
    return 0.5 * (1.0 - root), 0.5 * (1.0 + root)


def window(x: float, x_core: float, width: float) -> float:
    """Smooth source window: 1 inside core, 0 outside."""

    z = (x - x_core) / width
    if z > 50.0:
        return 0.0
    if z < -50.0:
        return 1.0
    return 1.0 / (1.0 + math.exp(z))


def solve_profile(source: float, x_core: float, width: float, xmin: float, xmax: float):
    roots = p_roots(source)
    if roots is None:
        raise ValueError("source exceeds real-root limit 1/8")
    p_soft, _ = roots

    def rhs(x, y):
        f, fx = y
        w = window(float(x), x_core, width)
        return [fx, -fx - 2.0 * source * w * f]

    # Linear equation: use unit amplitude at the inner endpoint. The outer
    # asymptotic normalization is applied after integration.
    y0 = [1.0, -p_soft]
    sol = solve_ivp(
        rhs,
        (xmin, xmax),
        y0,
        rtol=1.0e-10,
        atol=1.0e-12,
        max_step=0.05,
        dense_output=False,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    x = sol.t
    f = sol.y[0]
    fx = sol.y[1]

    # Outside W~0, f=A+B/r = A+B exp(-x), fx=-B exp(-x).
    # Estimate A and B at the outer endpoint, then normalize A -> 1.
    A = f[-1] + fx[-1]
    B = -fx[-1] * math.exp(x[-1])
    if A <= 0:
        raise RuntimeError(f"nonpositive asymptotic A={A}")

    f_norm = f / A
    fx_norm = fx / A
    exterior_a = B / A

    # C1 radial action scale, up to the common angular/time factor:
    # int f^2 phi_x^2 r dx, phi_x=-fx/(2f).
    r = np.exp(x)
    integrand = 0.25 * fx_norm * fx_norm * r
    action_scale = float(np.trapezoid(integrand, x))

    phi = -0.5 * np.log(f_norm)
    return {
        "p_soft": p_soft,
        "x": x,
        "f": f_norm,
        "fx": fx_norm,
        "phi": phi,
        "A": 1.0,
        "a_tail": exterior_a,
        "action_scale": action_scale,
        "phi_inner": float(phi[0]),
        "phi_outer": float(phi[-1]),
        "f_min": float(np.min(f_norm)),
        "f_max": float(np.max(f_norm)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=0.0)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--xmax", type=float, default=8.0)
    args = parser.parse_args()

    sectors = [
        monopole_sector(1),
        monopole_sector(2),
        ordinary_sector(1),
        ordinary_sector(2),
    ]

    print("Localized angular-source softened-core solve")
    print("equation in x=ln r: f_xx + f_x + 2 s W(x) f = 0")
    print(
        f"eta={args.eta:g} x_core={args.x_core:g} width={args.width:g} "
        f"xmin={args.xmin:g} xmax={args.xmax:g}"
    )
    print()

    for sector in sectors:
        source = args.eta * sector.angular_lambda
        roots = p_roots(source)
        if roots is None:
            print(
                f"{sector.label}: lambda={sector.angular_lambda:g} "
                f"source={source:g} -> no real softened endpoint"
            )
            continue
        result = solve_profile(
            source, args.x_core, args.width, args.xmin, args.xmax
        )
        print(
            f"{sector.label}: lambda={sector.angular_lambda:g} "
            f"deg={sector.degeneracy} source={source:g}"
        )
        print(
            f"  p_soft={result['p_soft']:.8f} "
            f"a_tail={result['a_tail']:.8g} "
            f"action_scale={result['action_scale']:.8g}"
        )
        print(
            f"  phi_inner={result['phi_inner']:.8g} "
            f"phi_outer={result['phi_outer']:.8g} "
            f"f_range=[{result['f_min']:.8g}, {result['f_max']:.8g}]"
        )
        print()


if __name__ == "__main__":
    main()
