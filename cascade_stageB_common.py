"""Common Stage B characterization: graduated-floor zero counting + per-rung table columns.
Extracted verbatim from stageB_bisect.py."""
import numpy as np
Z = 8.0
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

