#!/usr/bin/env python3
"""
OBSERVE-C3: seed scan for C matter-ball -> exterior.

Fixed ball: Z=1, rho0=5, R_m=2 (C2 reference).
Vary center seed (r0 fixed 0.05):
  D0, v0=D'(r0), u0=phi'(r0), phi0=0.

Classify exterior D behavior: GROW / PLATEAU / FALL / PINCH / TURN (D' crosses 0).

Mode: OBSERVE.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp

from macro_C_observe2 import rho_compact, rhs_C

PREMISES = {
    "packaging": "C",
    "ball": "Z=1, rho0=5, R_m=2 fixed FREE reference",
    "vary": "D0, v0, u0 at r0=0.05",
    "mode": "OBSERVE",
}


@dataclass
class SeedRun:
    tag: str
    D0: float
    v0: float
    u0: float
    status: str
    r_end: float
    G_Rm: float
    G_drift: float
    D_Rm: float
    v_Rm: float
    D_end: float
    v_end: float
    D_min_ext: float
    D_max_ext: float
    ext_class: str
    notes: str


def classify_exterior(rs, D, v, R_m) -> str:
    """rs increasing, only use r >= R_m."""
    m = rs >= R_m - 1e-12
    if not np.any(m):
        return "NO_EXT"
    re, De, ve = rs[m], D[m], v[m]
    if len(re) < 3:
        return "SHORT_EXT"
    # pinch already handled by status
    dD = De[-1] - De[0]
    # turn: v changes sign in exterior
    if np.any(ve[:-1] * ve[1:] < 0):
        return "TURN"
    v_mean = float(np.mean(ve))
    if abs(v_mean) < 0.02 and abs(De[-1] - De[0]) < 0.05 * max(De[0], 1e-6):
        return "PLATEAU"
    if De[-1] > De[0] + 0.05:
        return "GROW"
    if De[-1] < De[0] - 0.05:
        return "FALL"
    return "MILD"


def run_seed(
    D0: float,
    v0: float,
    u0: float = 0.0,
    Z: float = 1.0,
    rho0: float = 5.0,
    R_m: float = 2.0,
    r0: float = 0.05,
    r_max: float = 60.0,
) -> SeedRun:
    y0 = np.array([0.0, u0, D0, v0], dtype=float)

    def fun(r, y):
        return rhs_C(r, y, Z, rho0, R_m)

    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1

    sol = solve_ivp(
        fun,
        (r0, r_max),
        y0,
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        events=hit_D,
        max_step=0.05,
        dense_output=True,
    )
    pinched = bool(sol.t_events and len(sol.t_events[0]) > 0)
    status = "ok" if sol.success else ("pinch" if pinched else "stopped")
    r_end = float(sol.t[-1])

    if sol.sol is None or r_end < R_m:
        return SeedRun(
            tag=f"D{D0:g}_v{v0:g}_u{u0:g}",
            D0=D0,
            v0=v0,
            u0=u0,
            status=status,
            r_end=r_end,
            G_Rm=float("nan"),
            G_drift=float("nan"),
            D_Rm=float("nan"),
            v_Rm=float("nan"),
            D_end=float(sol.y[2, -1]),
            v_end=float(sol.y[3, -1]),
            D_min_ext=float("nan"),
            D_max_ext=float("nan"),
            ext_class="PINCH" if pinched else "NO_EXT",
            notes="failed_before_Rm" if r_end < R_m else status,
        )

    rs = np.linspace(r0, r_end, 400)
    Y = sol.sol(rs)
    phi, u, D, v = Y
    # at Rm
    yRm = sol.sol(min(R_m, r_end))
    G_Rm = float(yRm[2] ** 2 * yRm[1])
    D_Rm, v_Rm = float(yRm[2]), float(yRm[3])
    if r_end > R_m:
        re = rs[rs >= R_m]
        Ye = sol.sol(re)
        Ge = Ye[2] ** 2 * Ye[1]
        G_drift = float(np.max(np.abs(Ge - G_Rm)))
        D_min_ext = float(np.min(Ye[2]))
        D_max_ext = float(np.max(Ye[2]))
        ext_class = "PINCH" if pinched else classify_exterior(rs, D, v, R_m)
    else:
        G_drift = float("nan")
        D_min_ext = D_max_ext = float("nan")
        ext_class = "NO_EXT"

    notes = []
    if G_drift == G_drift and G_drift < 1e-6:
        notes.append("G_ok")
    elif G_drift == G_drift:
        notes.append(f"G_drift={G_drift:.1e}")

    return SeedRun(
        tag=f"D{D0:g}_v{v0:g}_u{u0:g}",
        D0=D0,
        v0=v0,
        u0=u0,
        status=status,
        r_end=r_end,
        G_Rm=G_Rm,
        G_drift=G_drift,
        D_Rm=D_Rm,
        v_Rm=v_Rm,
        D_end=float(sol.y[2, -1]),
        v_end=float(sol.y[3, -1]),
        D_min_ext=D_min_ext,
        D_max_ext=D_max_ext,
        ext_class=ext_class,
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-C3 seed scan (fixed ball Z=1 rho0=5 Rm=2)")
    print("=" * 70)

    runs: list[SeedRun] = []
    r0 = 0.05

    # (A) C2 baseline neighborhood: D0 ~ r0, vary v0
    print("\n--- (A) D0=r0=0.05, vary v0, u0=0 ---")
    for v0 in [0.0, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, -0.2, -0.5]:
        rr = run_seed(D0=r0, v0=v0, u0=0.0)
        runs.append(rr)
        print(
            f"  v0={v0:+g}: {rr.status:6s} class={rr.ext_class:8s} "
            f"r_end={rr.r_end:6.1f} G_Rm={rr.G_Rm:7.3f} "
            f"D_Rm={rr.D_Rm:.3f} v_Rm={rr.v_Rm:.3f} D_end={rr.D_end:.3f} | {rr.notes}"
        )

    # (B) vary D0 at fixed v0=1
    print("\n--- (B) v0=1, vary D0, u0=0 ---")
    for D0 in [0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
        rr = run_seed(D0=D0, v0=1.0, u0=0.0)
        runs.append(rr)
        print(
            f"  D0={D0:g}: {rr.status:6s} class={rr.ext_class:8s} "
            f"G_Rm={rr.G_Rm:7.3f} D_Rm={rr.D_Rm:.3f} v_Rm={rr.v_Rm:.3f} "
            f"D_end={rr.D_end:.3f}"
        )

    # (C) D0=r0, v0=1, vary u0
    print("\n--- (C) D0=0.05 v0=1, vary u0 ---")
    for u0 in [-0.5, -0.2, -0.1, 0.0, 0.1, 0.2, 0.5]:
        rr = run_seed(D0=r0, v0=1.0, u0=u0)
        runs.append(rr)
        print(
            f"  u0={u0:+g}: {rr.status:6s} class={rr.ext_class:8s} "
            f"G_Rm={rr.G_Rm:7.3f} D_end={rr.D_end:.3f} phi via G"
        )

    # (D) aim for exterior plateau: small v0, larger D0 (fat core slow open)
    print("\n--- (D) fat core / slow open ---")
    for D0, v0 in [
        (0.5, 0.0),
        (0.5, 0.1),
        (1.0, 0.0),
        (1.0, 0.1),
        (1.0, 0.5),
        (2.0, 0.0),
        (2.0, 0.2),
        (0.2, 0.0),
        (0.2, 0.05),
    ]:
        rr = run_seed(D0=D0, v0=v0, u0=0.0, r_max=80.0)
        runs.append(rr)
        print(
            f"  D0={D0:g} v0={v0:g}: {rr.status:6s} class={rr.ext_class:8s} "
            f"r_end={rr.r_end:6.1f} G_Rm={rr.G_Rm:7.3f} "
            f"D_Rm={rr.D_Rm:.3f} v_Rm={rr.v_Rm:.3f} D_end={rr.D_end:.3f}"
        )

    # (E) try to get TURN or FALL in exterior: start with large u0 at small D
    print("\n--- (E) large central phi slope ---")
    for u0 in [0.5, 1.0, 2.0, -1.0]:
        for v0 in [0.5, 1.0]:
            rr = run_seed(D0=0.05, v0=v0, u0=u0, r_max=60.0)
            runs.append(rr)
            print(
                f"  u0={u0:+g} v0={v0:g}: {rr.status:6s} class={rr.ext_class:8s} "
                f"G_Rm={rr.G_Rm:7.3f} D_end={rr.D_end:.3f}"
            )

    # Summary counts
    from collections import Counter

    c = Counter(r.ext_class for r in runs)
    print("\n--- ext_class counts ---")
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

    # Vacuum exterior analytic: D'' = -(Z/4) G^2 / D^3 < 0 always if G!=0
    # so v is always decreasing in vacuum when G!=0!
    # => if v_Rm > 0, may stay positive (GROW) or hit zero (TURN then FALL)
    # if v_Rm < 0, FALL
    print("\n--- Theory note: vacuum D'' = -(Z/4) G^2/D^3 <= 0 ---")
    print("  => D' strictly decreases in exterior when G!=0.")
    print("  => PLATEAU only if G=0 or v~0 already; TURN if v_Rm>0 but D'' kills v.")

    # Bisect v0 for TURN at D0=0.05
    print("\n--- Bisect v0 for TURN (D0=0.05, u0=0) ---")
    # find if any TURN in v0 scan; refine
    lo, hi = 0.0, 3.0
    # check classes
    samples = []
    for v0 in np.linspace(0.0, 2.5, 26):
        rr = run_seed(D0=0.05, v0=float(v0), u0=0.0, r_max=100.0)
        samples.append((v0, rr.ext_class, rr.v_Rm, rr.D_end, rr.status))
    for v0, cl, vRm, Dend, st in samples:
        print(f"  v0={v0:.2f}: class={cl:8s} v_Rm={vRm:7.3f} D_end={Dend:8.3f} {st}")

    # D0=1 v0 scan for TURN
    print("\n--- v0 scan D0=1 u0=0 r_max=100 ---")
    for v0 in np.linspace(0.0, 2.0, 11):
        rr = run_seed(D0=1.0, v0=float(v0), u0=0.0, r_max=100.0)
        print(
            f"  v0={v0:.2f}: class={rr.ext_class:8s} v_Rm={rr.v_Rm:7.3f} "
            f"G_Rm={rr.G_Rm:7.3f} D_end={rr.D_end:8.3f}"
        )
        runs.append(rr)

    out = {"premises": PREMISES, "runs": [asdict(r) for r in runs]}
    path = "macro_C_observe3_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-C3")


if __name__ == "__main__":
    main()
