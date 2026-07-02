"""Stage C library: combos, Z-aware graduated-floor characterization, sweep + Illinois bisect.
Reuses cell_solver_universe_T3.rhs/make_risefall_slice; A2/A3 slices defined locally per spec.
Shot ledger kept per combo. Single process, CPU, bounded everywhere.
"""
import sys, time
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, LN1101, make_risefall_slice

SHOTS = 0


# ----------------------------------------------------------------- local slices (CHOSE, per spec)
def make_A2_slice(a, k=3.0):
    """U(rho) = 2 rho^2 exp(-a(rho^k - 1)); U(1)=2 built in; stuck a = 2/k."""
    def U(rho):
        return 2.0 * rho ** 2 * np.exp(-a * (rho ** k - 1.0))
    def Up(rho):
        return 2.0 * rho ** 2 * np.exp(-a * (rho ** k - 1.0)) * (2.0 / rho - a * k * rho ** (k - 1.0))
    return U, Up, f"A2 k={k} a={a:+.10f}"


def make_A3_slice(b):
    """U(rho) = 2 rho^2 (1+b)/(1+b rho^4); U(1)=2 built in; stuck b = 1."""
    def U(rho):
        return 2.0 * rho ** 2 * (1.0 + b) / (1.0 + b * rho ** 4)
    def Up(rho):
        den = 1.0 + b * rho ** 4
        return 2.0 * (1.0 + b) * (2.0 * rho * den - rho ** 2 * 4.0 * b * rho ** 3) / den ** 2
    return U, Up, f"A3 b={b:+.10f}"


# ----------------------------------------------------------------- combos (priority order)
# param(d) = stuck * (1 - d)   [below side]
COMBOS = {
    "c1_A1m2_Z8": dict(Z=8.0, stuck=1.0, d0_est=0.01393,
                       make=lambda p: make_risefall_slice(p, m=2.0)),
    "c2_A1m3_Z1": dict(Z=1.0, stuck=1.5, d0_est=0.00382,
                       make=lambda p: make_risefall_slice(p, m=3.0)),
    "c3_A2k3_Z8": dict(Z=8.0, stuck=2.0 / 3.0, d0_est=0.019119,
                       make=lambda p: make_A2_slice(p, k=3.0)),
    "c4_A3_Z8":   dict(Z=8.0, stuck=1.0, d0_est=0.02375,
                       make=lambda p: make_A3_slice(p)),
    "c5_A1m4_Z8": dict(Z=8.0, stuck=2.0, d0_est=0.011545,
                       make=lambda p: make_risefall_slice(p, m=4.0)),
}


# ----------------------------------------------------------------- shooting (method-switchable)
def shoot_g(Z, Up, method="LSODA", rtol=1e-10, atol=1e-12, r_max=5.0e7):
    global SHOTS
    SHOTS += 1
    seal = lambda r, y, *aa: y[0]
    seal.terminal, seal.direction = True, +1
    collapse = lambda r, y, *aa: y[2] - 1e-9
    collapse.terminal, collapse.direction = True, -1
    sol = solve_ivp(rhs, (0.0, r_max), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method=method, rtol=rtol, atol=atol, events=[seal, collapse],
                    dense_output=True)
    o = {"status": "no-seal", "sol": sol}
    if sol.t_events[1].size:
        o["status"] = "collapse"
        return o
    if not sol.t_events[0].size:
        return o
    r_s = sol.t_events[0][0]
    phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
    o.update(status="seal", r_s=r_s, rho_s=rho_s, rhop_s=rhop_s, q=Z * rho_s ** 2 * phip_s)
    return o


def f_of_d(combo, d, **kw):
    c = COMBOS[combo]
    p = c["stuck"] * (1.0 - d)
    U, Up, _ = c["make"](p)
    o = shoot_g(c["Z"], Up, **kw)
    f = o["rhop_s"] if o["status"] == "seal" else np.nan
    return f, o, U


# ----------------------------------------------------------------- graduated-floor zero counting
def graded_count(f):
    """Interior sign changes of f above graduated relative floors (1e-1..1e-12, 4/decade).
    Stable = plateau spanning >= 2 decades (>= 9 consecutive)."""
    fmax = float(np.max(np.abs(f)))
    fracs = 10.0 ** (-np.arange(4, 49) / 4.0)
    prof = []
    for fr in fracs:
        m = np.abs(f) > fr * fmax
        s = np.sign(f[m])
        prof.append(int(np.sum(s[1:] * s[:-1] < 0)))
    runs, i = [], 0
    while i < len(prof):
        j = i
        while j + 1 < len(prof) and prof[j + 1] == prof[i]:
            j += 1
        runs.append((i, j, prof[i]))
        i = j + 1
    good = [(i, j, c) for (i, j, c) in runs if (j - i) >= 8]
    if not good:
        return None, None, list(zip([float(x) for x in fracs], prof))
    best = max(good, key=lambda t: (t[1] - t[0], t[0]))
    return best[2], (float(fracs[best[0]]), float(fracs[best[1]])), \
        list(zip([float(x) for x in fracs], prof))


def characterize(o, U, Z, npts=100001):
    r_s = o["r_s"]
    rr = np.linspace(0.0, r_s, npts)
    phi, phip, rho, rhop = o["sol"].sol(rr)
    Nd, Nd_rng, Nd_prof = graded_count((rho - 1.0)[1:-1])
    Np, Np_rng, Np_prof = graded_count(rhop[1:-1])
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


# ----------------------------------------------------------------- sweep + root refinement
def sweep(combo, d_hi, d_lo, ratio=0.98):
    """Geometric d-grid, descending; returns rows [(d, f_or_None, status)] and brackets."""
    n = int(np.ceil(np.log(d_hi / d_lo) / np.log(1.0 / ratio))) + 1
    grid = np.geomspace(d_hi, d_lo, n)
    rows = []
    for d in grid:
        f, o, _ = f_of_d(combo, float(d))
        rows.append((float(d), float(f) if np.isfinite(f) else None, o["status"]))
    return rows


def find_brackets(rows):
    rows = sorted(rows, key=lambda r: -r[0])
    br = []
    for (d1, f1, s1), (d2, f2, s2) in zip(rows, rows[1:]):
        if s1 == s2 == "seal" and f1 is not None and f2 is not None and f1 * f2 < 0:
            br.append((d1, d2, f1, f2))
    return br


def refine_root(combo, d_hi, d_lo, f_hi, f_lo, dtol=5e-9, itmax=60):
    """Illinois (modified regula falsi) with nan-fallback-to-bisection. Returns (d*, steps)."""
    a, b, fa, fb = d_hi, d_lo, f_hi, f_lo
    side = 0
    steps = 0
    while abs(a - b) > dtol and steps < itmax:
        m = (a * fb - b * fa) / (fb - fa)
        # keep strictly interior; else bisect
        if not (min(a, b) < m < max(a, b)):
            m = 0.5 * (a + b)
        fm, o, _ = f_of_d(combo, m)
        steps += 1
        if not np.isfinite(fm):
            m2 = 0.5 * (a + b)
            fm, o, _ = f_of_d(combo, m2)
            steps += 1
            if not np.isfinite(fm):
                return None, steps
            m = m2
        if fa * fm < 0:
            b, fb = m, fm
            if side == -1:
                fa *= 0.5
            side = -1
        else:
            a, fa = m, fm
            if side == +1:
                fb *= 0.5
            side = +1
    return 0.5 * (a + b), steps
