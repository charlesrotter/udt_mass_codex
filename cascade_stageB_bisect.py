"""Stage B: bisect brackets (far-tail cut: d > 2e-3 => 23 brackets), characterize each rung.
Graduated-floor zero counting (N_delta PRIMARY, N_rho' SEPARATE; >=2-decade stability;
100k dense sampling + 200k re-check). Per-rung table per the frozen addendum.
Output: stageB_rungs.json
"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss, diagnose, LN1101

Z, M = 8.0, 3.0
SCR = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad"
SHOTS = 0

def f_of_d(d, method="LSODA", rtol=1e-10, atol=1e-12):
    global SHOTS
    a = 1.5 * (1.0 - d)
    U, Up, _ = make_risefall_slice(a, m=M)
    SHOTS += 1
    if method == "LSODA":
        f, o = miss(Z, U, Up, 1.0, rtol=rtol, atol=atol)
        return f, o, U
    # Radau path: re-implement shoot with method switch (same events)
    from scipy.integrate import solve_ivp
    from cell_solver_universe_T3 import rhs, PHI_C
    seal = lambda r, y, *aa: y[0]; seal.terminal, seal.direction = True, +1
    collapse = lambda r, y, *aa: y[2] - 1e-9; collapse.terminal, collapse.direction = True, -1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="Radau", rtol=rtol, atol=atol, events=[seal, collapse],
                    dense_output=True)
    o = {"status": "no-seal", "sol": sol}
    if sol.t_events[1].size: o["status"] = "collapse"; return np.nan, o, U
    if not sol.t_events[0].size: return np.nan, o, U
    r_s = sol.t_events[0][0]
    phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
    o.update(status="seal", r_s=r_s, rho_s=rho_s, rhop_s=rhop_s, q=Z*rho_s**2*phip_s)
    return rhop_s, o, U

# ---------------------------------------------------------------- graduated-floor zero counting
def graded_count(rr, f):
    """Count interior sign changes of f above graduated relative floors.
    Returns (stable_count_or_None, plateau_frac_range, full_profile)."""
    fmax = float(np.max(np.abs(f)))
    fracs = 10.0 ** (-np.arange(4, 49) / 4.0)          # 1e-1 .. 1e-12, 4 per decade
    prof = []
    for fr in fracs:
        m = np.abs(f) > fr * fmax
        s = np.sign(f[m])
        prof.append(int(np.sum(s[1:] * s[:-1] < 0)))
    # plateaus: runs of identical count; need span >= 2 decades (>= 9 consecutive at 0.25/dec)
    runs = []
    i = 0
    while i < len(prof):
        j = i
        while j + 1 < len(prof) and prof[j + 1] == prof[i]: j += 1
        runs.append((i, j, prof[i]))
        i = j + 1
    good = [(i, j, c) for (i, j, c) in runs if (j - i) >= 8]
    if not good:
        return None, None, list(zip([float(x) for x in fracs], prof))
    # choose the longest; tie -> lowest floor (latest)
    best = max(good, key=lambda t: (t[1] - t[0], t[0]))
    return best[2], (float(fracs[best[0]]), float(fracs[best[1]])), \
        list(zip([float(x) for x in fracs], prof))

def characterize(o, U, npts=100001):
    r_s = o["r_s"]
    rr = np.linspace(0.0, r_s, npts)
    phi, phip, rho, rhop = o["sol"].sol(rr)
    delta = rho - 1.0
    # interior: drop exact endpoints
    Nd, Nd_rng, Nd_prof = graded_count(rr[1:-1], delta[1:-1])
    Np, Np_rng, Np_prof = graded_count(rr[1:-1], rhop[1:-1])
    e2p = np.exp(2.0 * phi)
    L = float(np.trapezoid(np.exp(phi), rr))
    m_ms = 0.5 * rho * (1.0 - rhop ** 2 / e2p)
    H = 0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 / e2p - 2.0 + U(rho)
    return {
        "N_delta": Nd, "N_delta_floor_range": Nd_rng,
        "N_rhop": Np, "N_rhop_floor_range": Np_rng,
        "N_delta_profile": Nd_prof, "N_rhop_profile": Np_prof,
        "rho_s": float(o["rho_s"]), "r_s": float(r_s), "q": float(o["q"]),
        "L_proper": L, "chi": L / float(o["rho_s"]),
        "dphi_carried": float(phi[-1] - phi[0]),
        "ms_seal_2m_over_rho": float(2.0 * m_ms[-1] / rho[-1]),
        "H_drift": float(np.max(np.abs(H))),
        "rhop_seal_residual": float(o["rhop_s"]),
    }

# ---------------------------------------------------------------- load brackets, bisect
sw = json.load(open(f"{SCR}/stageB_sweep.json"))
rows = {r[0]: (r[1], r[2]) for r in sw["rows"]}
brackets = [b for b in sw["brackets"] if 0.5 * (b[0] + b[1]) > 2.0e-3]
cut = [b for b in sw["brackets"] if 0.5 * (b[0] + b[1]) <= 2.0e-3]
print(f"bisecting {len(brackets)} brackets (far-tail cut leaves {len(cut)} unbisected, d<=~2e-3)")

t0 = time.time()
rungs = []
for bi, (d_hi, d_lo) in enumerate(brackets):
    f_hi = rows[d_hi][0]
    lo, hi, fhi = d_lo, d_hi, f_hi
    steps = 0
    best = None
    while (hi - lo) > 1.0e-8 and steps < 18:
        mid = 0.5 * (lo + hi)
        fm, om, Um = f_of_d(mid)
        steps += 1
        if not np.isfinite(fm):
            print(f"  bracket {bi}: non-finite miss at d={mid:.3e} status={om['status']}"); break
        best = (mid, fm, om, Um)
        if fhi * fm < 0: lo = mid
        else: hi, fhi = mid, fm
    d_star = 0.5 * (lo + hi)
    # final characterization shot at the converged midpoint
    fm, om, Um = f_of_d(d_star); steps += 1
    if om["status"] == "seal":
        ch = characterize(om, Um)
        ch2 = characterize(om, Um, npts=200001)   # 2x re-check (no extra shot)
        ch["N_delta_recheck200k"] = ch2["N_delta"]
        ch["N_rhop_recheck200k"] = ch2["N_rhop"]
    else:
        ch = {"status": om["status"]}
    a_star = 1.5 * (1.0 - d_star)
    rung = {"bracket_index": bi, "d_bracket": [d_hi, d_lo], "d_star": d_star,
            "a_star": a_star, "bisect_steps": steps, "final_width_d": hi - lo, **ch}
    rungs.append(rung)
    print(f"[{bi:2d}] a*={a_star:.10f} d={d_star:.6e} steps={steps} "
          f"N_delta={ch.get('N_delta')} N_rhop={ch.get('N_rhop')} "
          f"(200k: {ch.get('N_delta_recheck200k')},{ch.get('N_rhop_recheck200k')}) "
          f"q={ch.get('q', float('nan')):.5f} rho_s={ch.get('rho_s', float('nan')):.5f} "
          f"L={ch.get('L_proper', float('nan')):.4f} chi={ch.get('chi', float('nan')):.4f} "
          f"Hd={ch.get('H_drift', float('nan')):.1e}")

json.dump({"rungs": [{k: v for k, v in r.items() if 'profile' not in k} for r in rungs],
           "profiles": [{ "bracket_index": r["bracket_index"],
                          "N_delta_profile": r.get("N_delta_profile"),
                          "N_rhop_profile": r.get("N_rhop_profile")} for r in rungs],
           "cut_brackets": cut, "shots_this_script": SHOTS},
          open(f"{SCR}/stageB_rungs.json", "w"), indent=1)
print(f"\nshots this script = {SHOTS}, wall = {time.time()-t0:.1f}s")
