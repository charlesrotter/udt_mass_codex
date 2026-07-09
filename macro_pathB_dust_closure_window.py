#!/usr/bin/env python3
"""
Improved closure window: outer turn after real expansion; bracket in mass M.
Contract: macro_pathB_dust_closure_window_CONTRACT.md
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0
R_EXP = 3.0  # D_max/D0
R_SEP = 2.0  # r_turn / r_c
EPS_S = 0.02
D_FLOOR = 1e-4


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-(r / rc) ** 2)


def rho_tophat(r, rho0, rc, soft=0.05):
    return rho0 / (1.0 + np.exp((r - rc) / (soft * rc + 1e-12)))


def make_rhs(rho0, rc, profile):
    def rho_of(r):
        return rho_gauss(r, rho0, rc) if profile == "gauss" else rho_tophat(r, rho0, rc)

    def f(r, y):
        D, S, phi, Q = y
        De = max(float(D), 1e-14)
        rh = float(rho_of(r))
        e2 = np.exp(np.clip(2.0 * phi, -40, 40))
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        A11 = 4.0 * De * em2
        A12 = -Z * De * De
        A21 = -4.0
        A22 = 4.0 * De
        b1 = 2.0 * Z * De * S * Q
        b2 = -Z * De * e2 * Q * Q + 2.0 * De * rh * e2 + 8.0 * De * Q * Q - 8.0 * S * Q
        det = A11 * A22 - A12 * A21
        if abs(det) < 1e-30:
            return [S, 0.0, Q, 0.0]
        Sp = (b1 * A22 - A12 * b2) / det
        Qp = (A11 * b2 - b1 * A21) / det
        Sp = float(np.clip(Sp if np.isfinite(Sp) else 0.0, -1e6, 1e6))
        Qp = float(np.clip(Qp if np.isfinite(Qp) else 0.0, -1e6, 1e6))
        return [S, Sp, Q, Qp]

    return f, rho_of


def integrate(rho0, rc, y0, r0, r_max, profile="gauss"):
    f, rho_of = make_rhs(rho0, rc, profile)

    def event_Dfloor(r, y):
        return y[0] - D_FLOOR

    event_Dfloor.terminal = True
    event_Dfloor.direction = -1

    sol = solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.04,
        events=[event_Dfloor],
    )
    return sol, rho_of


def mass_M(sol, rho_of):
    r, D = sol.t, sol.y[0]
    if len(r) < 2:
        return 0.0
    dens = 4.0 * np.pi * D**2 * np.array([rho_of(ri) for ri in r])
    return float(np.trapezoid(dens, r))


def classify(sol, rho_of, rc, label):
    if sol is None or len(sol.t) < 4:
        return None
    r, D, S, phi = sol.t, sol.y[0], sol.y[1], sol.y[2]
    D0 = float(D[0])
    Dmax = float(np.max(D))
    Dmin = float(np.min(D))
    imax = int(np.argmax(D))
    ratio = Dmax / max(D0, 1e-15)
    M = mass_M(sol, rho_of)
    phi_max = float(np.nanmax(phi))

    # outer turn: after imax (or after D has grown), S crosses + -> -
    # require some growth before turn
    i_turn = None
    for i in range(1, len(S)):
        if D[i] < D0 * 1.05:
            continue  # still near core size
        if ratio < R_EXP and D[i] < R_EXP * D0:
            # allow turn detection only if eventually ratio ok - check at end
            pass
        if S[i - 1] > EPS_S and S[i] <= 0.0:
            # check expansion ratio at this turn using max so far
            Dmax_so_far = float(np.max(D[: i + 1]))
            if Dmax_so_far / D0 >= R_EXP and r[i] >= R_SEP * rc:
                i_turn = i
                break

    collapsed = Dmin <= 1.5 * D_FLOOR or (
        not sol.success and Dmin < 0.1 * D0 and float(S[-1]) < -1.0
    )

    if i_turn is not None and not collapsed:
        status = "CLOSE"
    elif collapsed:
        status = "COLLAPSE"
    else:
        status = "OPEN"

    # secondary: any turn even if core-stuck
    i_any_turn = None
    for i in range(1, len(S)):
        if S[i - 1] > EPS_S and S[i] <= 0.0 and D[i] > D0:
            i_any_turn = i
            break

    return {
        "label": label,
        "status": status,
        "M": M,
        "M_over_rc": M / rc,
        "rho0": None,
        "rc": rc,
        "phi_max": phi_max,
        "dphi": float(phi[-1] - phi[0]),
        "D0": D0,
        "Dmax": Dmax,
        "Dend": float(D[-1]),
        "ratio": ratio,
        "r_turn": float(r[i_turn]) if i_turn is not None else None,
        "phi_turn": float(phi[i_turn]) if i_turn is not None else None,
        "r_any_turn": float(r[i_any_turn]) if i_any_turn is not None else None,
        "ceil": phi_max > 2.15,
        "ok": bool(sol.success),
        "r_end": float(r[-1]),
    }


def run_family(profile, rc, Q0, rho0_list, r0=0.2, r_max=15.0):
    y0 = [1.0, 0.0, 0.0, Q0]
    out = []
    for rho0 in rho0_list:
        sol, rho_of = integrate(float(rho0), rc, y0, r0, r_max, profile=profile)
        o = classify(sol, rho_of, rc, f"{profile} rc={rc:g} ρ0={rho0:.4g} Q0={Q0:g}")
        if o:
            o["rho0"] = float(rho0)
            o["Q0"] = Q0
            o["prof"] = profile
            out.append(o)
    return out


def summarize_band(rows, name):
    print(f"\n=== {name} ===")
    if not rows:
        print("  (empty)")
        return
    rows = sorted(rows, key=lambda x: x["M"])
    for st in ("OPEN", "CLOSE", "COLLAPSE"):
        sub = [x for x in rows if x["status"] == st]
        if not sub:
            print(f"  {st}: 0")
            continue
        Ms = [x["M"] for x in sub]
        print(
            f"  {st}: n={len(sub)}  M∈[{min(Ms):.3g}, {max(Ms):.3g}]  "
            f"median M={np.median(Ms):.3g}"
        )
    close = [x for x in rows if x["status"] == "CLOSE"]
    if close:
        Ms = sorted([x["M"] for x in close])
        width = Ms[-1] - Ms[0]
        # contiguous clusters in log M
        logM = np.log10(np.maximum(Ms, 1e-30))
        clusters = []
        cur = [Ms[0]]
        for m in Ms[1:]:
            if abs(np.log10(m) - np.log10(cur[-1])) < 0.15:  # within ~0.15 dex
                cur.append(m)
            else:
                clusters.append(cur)
                cur = [m]
        clusters.append(cur)
        print(f"  CLOSE M span: [{Ms[0]:.3g}, {Ms[-1]:.3g}]  linear_width={width:.3g}")
        print(f"  CLOSE clusters (0.15 dex link): {len(clusters)}")
        for i, cl in enumerate(clusters):
            print(
                f"    cluster {i+1}: M∈[{cl[0]:.3g},{cl[-1]:.3g}] n={len(cl)} "
                f"Δlog10M={np.log10(cl[-1]/cl[0]):.3f}"
            )
        print("  CLOSE samples:")
        for x in close[:12]:
            print(
                f"    M={x['M']:.4g} M/rc={x['M_over_rc']:.3g} ρ0={x['rho0']:.4g} "
                f"ratio={x['ratio']:.2f} r_t={x['r_turn']:.3g} φmax={x['phi_max']:.3f}"
            )
    # transition M: last OPEN before first CLOSE, first COLLAPSE after
    statuses = [(x["M"], x["status"]) for x in rows]
    first_close = next((m for m, s in statuses if s == "CLOSE"), None)
    last_open_before = None
    for m, s in statuses:
        if first_close is not None and m < first_close and s == "OPEN":
            last_open_before = m
        if first_close is not None and m >= first_close:
            break
    first_coll_after_close = None
    seen_close = False
    for m, s in statuses:
        if s == "CLOSE":
            seen_close = True
        if seen_close and s == "COLLAPSE":
            first_coll_after_close = m
            break
    print(
        f"  transitions: last OPEN before CLOSE M~{last_open_before} ; "
        f"first CLOSE M~{first_close} ; first COLLAPSE after CLOSE M~{first_coll_after_close}"
    )


def main():
    print("=" * 70)
    print(f"CLOSURE WINDOW  R_exp={R_EXP}  R_sep={R_SEP}  (Path B + FREE dust)")
    print("=" * 70)

    # Dense rho0 grids -> will sort by M
    rho_coarse = np.logspace(-2, 2, 48)
    rho_mid = np.logspace(-0.5, 1.5, 40)  # denser where WP2 saw action

    all_rows = []

    # Primary family
    print("\n[A] gauss rc=1 Q0=0.5 — dense amount scan")
    rows_a = run_family("gauss", 1.0, 0.5, np.unique(np.concatenate([rho_coarse, rho_mid])))
    for o in rows_a:
        mark = o["status"][0]
        print(
            f"  [{mark}] ρ0={o['rho0']:.4g} M={o['M']:.4g} ratio={o['ratio']:.2f} "
            f"φmax={o['phi_max']:.3f} r_t={o['r_turn']} status={o['status']}"
        )
    all_rows.extend(rows_a)
    summarize_band(rows_a, "gauss rc=1 Q0=0.5")

    print("\n[B] gauss rc=1 Q0=0 — matter-only seed")
    rows_b = run_family("gauss", 1.0, 0.0, np.unique(np.concatenate([rho_coarse, rho_mid])))
    for o in rows_b:
        if o["status"] != "OPEN" or o["phi_max"] > 2.1:
            print(
                f"  [{o['status'][0]}] ρ0={o['rho0']:.4g} M={o['M']:.4g} "
                f"ratio={o['ratio']:.2f} φmax={o['phi_max']:.3f} r_t={o['r_turn']}"
            )
    all_rows.extend(rows_b)
    summarize_band(rows_b, "gauss rc=1 Q0=0")

    print("\n[C] top-hat rc=1.5 Q0=0.5 — shape cross-check")
    rows_c = run_family("tophat", 1.5, 0.5, np.logspace(-2, 1.8, 40))
    for o in rows_c:
        if o["status"] != "OPEN" or o["ceil"]:
            print(
                f"  [{o['status'][0]}] ρ0={o['rho0']:.4g} M={o['M']:.4g} "
                f"ratio={o['ratio']:.2f} φmax={o['phi_max']:.3f} r_t={o['r_turn']}"
            )
    all_rows.extend(rows_c)
    summarize_band(rows_c, "tophat rc=1.5 Q0=0.5")

    print("\n[D] gauss rc=2 Q0=0.5 — larger core")
    rows_d = run_family("gauss", 2.0, 0.5, np.logspace(-2, 1.5, 36))
    summarize_band(rows_d, "gauss rc=2 Q0=0.5")
    all_rows.extend(rows_d)

    # Cross-family CLOSE M overlap
    print("\n" + "=" * 70)
    print("CROSS-FAMILY CLOSE M COMPARISON")
    print("=" * 70)
    for name, rows in [
        ("gauss rc=1 Q0=0.5", rows_a),
        ("gauss rc=1 Q0=0", rows_b),
        ("tophat rc=1.5 Q0=0.5", rows_c),
        ("gauss rc=2 Q0=0.5", rows_d),
    ]:
        cl = [x["M"] for x in rows if x["status"] == "CLOSE"]
        if cl:
            print(
                f"  {name}: CLOSE M∈[{min(cl):.3g},{max(cl):.3g}]  "
                f"M/rc∈[{min(x['M_over_rc'] for x in rows if x['status']=='CLOSE'):.3g},"
                f"{max(x['M_over_rc'] for x in rows if x['status']=='CLOSE'):.3g}]  n={len(cl)}"
            )
        else:
            print(f"  {name}: no CLOSE under improved criteria")

    # Sensitivity: loosen/tighten R_exp briefly
    print("\n[E] Sensitivity of CLOSE count vs R_exp (gauss rc=1 Q0=0.5, fixed runs)")
    # reclassify stored is hard without re-run; quick re-run subset
    test_rhos = np.logspace(-1, 1.5, 24)
    for Rexp in (2.0, 3.0, 5.0):
        n_close = 0
        Ms = []
        for rho0 in test_rhos:
            sol, rho_of = integrate(float(rho0), 1.0, [1.0, 0.0, 0.0, 0.5], 0.2, 15.0)
            if len(sol.t) < 4:
                continue
            r, D, S = sol.t, sol.y[0], sol.y[1]
            D0 = D[0]
            Dmax = np.max(D)
            if Dmax / D0 < Rexp:
                continue
            ok_turn = False
            for i in range(1, len(S)):
                if D[i] < 1.05 * D0:
                    continue
                if S[i - 1] > EPS_S and S[i] <= 0 and np.max(D[: i + 1]) / D0 >= Rexp and r[i] >= R_SEP * 1.0:
                    if np.min(D[i:]) > 1.5 * D_FLOOR:
                        ok_turn = True
                        Ms.append(mass_M(sol, rho_of))
                        break
            if ok_turn:
                n_close += 1
        print(
            f"  R_exp={Rexp}: n_CLOSE={n_close}/{len(test_rhos)}  "
            f"M∈[{min(Ms):.3g},{max(Ms):.3g}]" if Ms else f"  R_exp={Rexp}: n_CLOSE=0"
        )

    print("\nDONE")


if __name__ == "__main__":
    main()
