#!/usr/bin/env python3
"""
Dilated dust interior -> Path B vacuum exterior soft-close (S2 target).
Contract: macro_pathB_dilated_softclose_CONTRACT.md
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0
D_FLOOR = 1e-4
EPS_Q = 0.05
EPS_S = 0.15
DPHI_MAX = 0.5


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-(r / rc) ** 2)


def make_rhs(rho0, rc, vacuum=False):
    """Dilated dust when not vacuum: L_m weight e^{-2 phi}."""

    def f(r, y):
        D, S, phi, Q = y
        De = max(float(D), 1e-14)
        rh = 0.0 if vacuum else float(rho_gauss(r, rho0, rc))
        e2 = np.exp(np.clip(2.0 * phi, -40, 40))
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        A11 = 4.0 * De * em2
        A12 = -Z * De * De
        A21 = -4.0
        A22 = 4.0 * De
        if vacuum or rh == 0.0:
            b1 = 2.0 * Z * De * S * Q
            b2 = -Z * De * e2 * Q * Q + 8.0 * De * Q * Q - 8.0 * S * Q
        else:
            b1 = 2.0 * Z * De * S * Q - 2.0 * De * De * rh * em2
            b2 = -Z * De * e2 * Q * Q + 8.0 * De * Q * Q - 8.0 * S * Q + 2.0 * De * rh
        det = A11 * A22 - A12 * A21
        if abs(det) < 1e-30:
            return [S, 0.0, Q, 0.0]
        Sp = (b1 * A22 - A12 * b2) / det
        Qp = (A11 * b2 - b1 * A21) / det
        Sp = float(np.clip(Sp if np.isfinite(Sp) else 0.0, -1e6, 1e6))
        Qp = float(np.clip(Qp if np.isfinite(Qp) else 0.0, -1e6, 1e6))
        return [S, Sp, Q, Qp]

    return f


def integrate(f, y0, r0, r_max):
    def ev(r, y):
        return y[0] - D_FLOOR

    ev.terminal = True
    ev.direction = -1
    return solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.04,
        events=[ev],
        dense_output=True,
    )


def mass_M(sol, rho0, rc, r_int):
    """Mass only in interior r<=r_int."""
    r, D = sol.t, sol.y[0]
    m = r <= r_int + 1e-12
    if np.sum(m) < 2:
        return 0.0
    rr, DD = r[m], D[m]
    dens = 4.0 * np.pi * DD**2 * np.array([rho_gauss(ri, rho0, rc) for ri in rr])
    return float(np.trapezoid(dens, rr))


def s2_score(sol_ext):
    """Return (mean|Q|, mean|dS/dr|, dphi) on outer third."""
    r = sol_ext.t
    D, S, phi, Q = sol_ext.y
    n = len(r)
    if n < 6:
        return 99.0, 99.0, 99.0
    i0 = (2 * n) // 3
    ro, So, Qo, phio = r[i0:], S[i0:], Q[i0:], phi[i0:]
    mean_Q = float(np.mean(np.abs(Qo)))
    # dS/dr ~ D''
    if len(ro) > 2:
        dS = np.gradient(So, ro)
        mean_dS = float(np.mean(np.abs(dS)))
    else:
        mean_dS = 99.0
    dphi = float(phio[-1] - phio[0])
    return mean_Q, mean_dS, dphi


def process(rho0, rc, Q0, kappa=3.0, r0=0.2, L_ext=8.0):
    r_int = kappa * rc
    if r_int <= r0:
        r_int = r0 + 1.0
    f_int = make_rhs(rho0, rc, vacuum=False)
    y0 = [1.0, 0.0, 0.0, Q0]
    sol_i = integrate(f_int, y0, r0, r_int)
    if len(sol_i.t) < 4 or np.min(sol_i.y[0]) <= 1.5 * D_FLOOR:
        return {
            "class": "NO_INT",
            "M": 0.0,
            "rho0": rho0,
            "rc": rc,
            "Q0": Q0,
            "kappa": kappa,
        }
    # state at r_int (dense)
    if sol_i.sol is not None:
        y_int = [float(v) for v in sol_i.sol(r_int)]
    else:
        y_int = [float(sol_i.y[k, -1]) for k in range(4)]
    M = mass_M(sol_i, rho0, rc, r_int)
    phi_int = y_int[2]
    # vacuum exterior
    f_ext = make_rhs(0.0, rc, vacuum=True)
    r_ext = r_int + L_ext
    sol_e = integrate(f_ext, y_int, r_int, r_ext)
    if len(sol_e.t) < 4 or np.min(sol_e.y[0]) <= 1.5 * D_FLOOR:
        return {
            "class": "EXT_FAIL",
            "M": M,
            "rho0": rho0,
            "rc": rc,
            "Q0": Q0,
            "kappa": kappa,
            "r_int": r_int,
            "phi_int": phi_int,
            "phi_max_int": float(np.nanmax(sol_i.y[2])),
        }
    mean_Q, mean_dS, dphi = s2_score(sol_e)
    dphi_tot = float(sol_e.y[2, -1] - phi_int)
    finite = bool(np.all(np.isfinite(sol_e.y)))
    if not finite or abs(dphi_tot) > 10:
        cls = "EXT_FAIL"
    elif mean_Q < EPS_Q and mean_dS < EPS_S and abs(dphi_tot) < DPHI_MAX:
        cls = "MATCH_S2"
    else:
        cls = "EXT_OPEN"

    return {
        "class": cls,
        "M": M,
        "rho0": rho0,
        "rc": rc,
        "Q0": Q0,
        "kappa": kappa,
        "r_int": r_int,
        "phi_int": phi_int,
        "phi_max_int": float(np.nanmax(sol_i.y[2])),
        "phi_end": float(sol_e.y[2, -1]),
        "mean_Q": mean_Q,
        "mean_dS": mean_dS,
        "dphi_ext": dphi_tot,
        "Dend": float(sol_e.y[0, -1]),
        "Send": float(sol_e.y[1, -1]),
        "Dint": y_int[0],
        "Sint": y_int[1],
        "Qint": y_int[3],
    }


def summarize(rows, title):
    print(f"\n=== {title} ===")
    for cl in ("NO_INT", "EXT_FAIL", "EXT_OPEN", "MATCH_S2"):
        sub = [x for x in rows if x["class"] == cl]
        if not sub:
            print(f"  {cl}: 0")
            continue
        Ms = [x["M"] for x in sub]
        print(f"  {cl}: n={len(sub)} M∈[{min(Ms):.3g},{max(Ms):.3g}] med={np.median(Ms):.3g}")
    ok = sorted([x for x in rows if x["class"] == "MATCH_S2"], key=lambda z: z["M"])
    if ok:
        print(
            f"  MATCH_S2 window M∈[{ok[0]['M']:.3g},{ok[-1]['M']:.3g}] "
            f"Δlog10={np.log10(max(ok[-1]['M']/ok[0]['M'],1e-30)):.3f} n={len(ok)}"
        )
        for x in ok[:12]:
            print(
                f"    M={x['M']:.4g} ρ0={x['rho0']:.4g} κ={x['kappa']} "
                f"φ_int={x['phi_int']:.3f} mean|Q|={x['mean_Q']:.3e} "
                f"mean|S'|={x['mean_dS']:.3e} dφ_ext={x['dphi_ext']:+.3f}"
            )
    # best EXT_OPEN by S2 score
    op = [x for x in rows if x["class"] == "EXT_OPEN"]
    if op:
        op2 = sorted(op, key=lambda z: z["mean_Q"] + z["mean_dS"])
        print("  Best EXT_OPEN (lowest mean|Q|+mean|S'|):")
        for x in op2[:5]:
            print(
                f"    M={x['M']:.4g} ρ0={x['rho0']:.4g} mean|Q|={x['mean_Q']:.3e} "
                f"mean|S'|={x['mean_dS']:.3e} dφ={x['dphi_ext']:+.3f} φ_end={x['phi_end']:.3f}"
            )


def main():
    print("=" * 70)
    print("DILATED SOFT-CLOSE: interior → vacuum S2 score")
    print(f"  EPS_Q={EPS_Q} EPS_S={EPS_S} DPHI_MAX={DPHI_MAX}")
    print("=" * 70)

    rho_list = np.unique(
        np.concatenate([np.logspace(-2, 2, 32), np.logspace(-0.5, 1.5, 24)])
    )

    all_match = []

    for kappa in (2.5, 3.0, 4.0):
        print(f"\n[A] rc=1 Q0=0.5 kappa={kappa}")
        rows = []
        for rho0 in rho_list:
            o = process(float(rho0), 1.0, 0.5, kappa=kappa)
            rows.append(o)
            if o["class"] in ("MATCH_S2", "EXT_FAIL") or (
                o["class"] == "EXT_OPEN" and o.get("mean_Q", 9) < 0.2
            ):
                print(
                    f"  [{o['class'][:4]}] ρ0={rho0:.4g} M={o['M']:.4g} "
                    f"Q~{o.get('mean_Q', float('nan')):.3e} S'~{o.get('mean_dS', float('nan')):.3e}"
                )
        summarize(rows, f"rc=1 Q0=0.5 κ={kappa}")
        all_match.extend([x for x in rows if x["class"] == "MATCH_S2"])

    print("\n[B] rc=1 Q0=0 kappa=3")
    rows_b = [process(float(rho0), 1.0, 0.0, kappa=3.0) for rho0 in rho_list]
    summarize(rows_b, "rc=1 Q0=0 κ=3")

    print("\n[C] rc=2 Q0=0.5 kappa=3")
    rows_c = [
        process(float(rho0), 2.0, 0.5, kappa=3.0)
        for rho0 in np.logspace(-2, 1.5, 28)
    ]
    summarize(rows_c, "rc=2 Q0=0.5 κ=3")

    # Vacuum-only softclose (rho0=0): baseline S2 quality from Q0 seed
    print("\n[D] vacuum baseline Q0 scan (no dust)")
    for Q0 in (0.0, 0.1, 0.5, 1.0):
        o = process(0.0, 1.0, Q0, kappa=3.0)
        print(
            f"  vac Q0={Q0}: class={o['class']} mean|Q|={o.get('mean_Q')} "
            f"mean|S'|={o.get('mean_dS')} dφ={o.get('dphi_ext')}"
        )

    print("\n" + "=" * 70)
    print("SUMMARY MATCH_S2")
    print("=" * 70)
    if all_match:
        Ms = [x["M"] for x in all_match]
        print(f"  total MATCH_S2 (κ variants on A): n={len(all_match)} M∈[{min(Ms):.3g},{max(Ms):.3g}]")
    else:
        print("  total MATCH_S2 on primary κ variants: 0")
        print("  => dilated soft-close to S2 not achieved under these FREE thresholds")

    print("\nDONE")


if __name__ == "__main__":
    main()
