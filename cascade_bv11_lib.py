"""bv11 blind-verifier library (fresh harness).

Reuses ONLY rhs + make_risefall_slice from cell_solver_universe_T3.py.
Own integrator: chunked DOP853 (banked solver uses LSODA + scipy events).
Own event location: dense-output sign scan + 90-step bisection on the interpolant
(including scan of a failed chunk's partial dense output -- banked hazard).
Own zero counter: graduated RELATIVE floors 1e-1..1e-12 (4/decade), plateau >= 2 decades.

Shot ledger: 1 shot = 1 full trajectory (all chunks of one IVP).
"""
import importlib.util
import numpy as np
from scipy.integrate import solve_ivp

_spec = importlib.util.spec_from_file_location(
    "t3", "/home/udt-admin/udt_mass_codex/cell_solver_universe_T3.py")
_t3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_t3)
rhs = _t3.rhs
make_risefall_slice = _t3.make_risefall_slice

LN1101 = float(np.log(1101.0))
PHI_C = -LN1101
Z = 8.0
M = 3.0

SHOTS = {"n": 0}


def shoot(a, rtol=1e-11, atol=1e-13, r_cap=5.0e5, chunk0=2.0, chunk_max=400.0,
          keep=False):
    """Integrate from the inner fold to the FIRST phi=0 upcrossing.
    Returns dict: status in {seal,no-seal,collapse,fail}; on seal r_s,y_s (+sols if keep)."""
    SHOTS["n"] += 1
    U, Up, _ = make_risefall_slice(a, m=M)
    y = np.array([PHI_C, 0.0, 1.0, 0.0])
    r0, chunk = 0.0, chunk0
    sols = []
    while r0 < r_cap:
        r1 = min(r0 + chunk, r_cap)
        sol = solve_ivp(rhs, (r0, r1), y, args=(Z, Up), method="DOP853",
                        rtol=rtol, atol=atol, dense_output=True)
        failed = (not sol.success) or (not np.all(np.isfinite(sol.y[:, -1])))
        r_end = float(sol.t[-1])
        if keep:
            sols.append(sol)
        if r_end > r0:  # ALWAYS scan integrated portion (failed chunk may hold the seal)
            nsub = max(600, 5 * len(sol.t))
            rr = np.linspace(r0, r_end, nsub)
            vals = sol.sol(rr)
            ph, rho = vals[0], vals[2]
            up = np.where((ph[:-1] < 0.0) & (ph[1:] >= 0.0))[0]
            co = np.where(rho <= 1e-9)[0]
            i_up = up[0] if up.size else None
            i_co = co[0] if co.size else None
            if i_up is not None and (i_co is None or i_up < i_co):
                lo, hi = rr[i_up], rr[i_up + 1]
                for _ in range(90):
                    mid = 0.5 * (lo + hi)
                    if sol.sol(mid)[0] < 0.0:
                        lo = mid
                    else:
                        hi = mid
                r_s = 0.5 * (lo + hi)
                return {"status": "seal", "r_s": float(r_s),
                        "y_s": np.asarray(sol.sol(r_s)),
                        "sols": sols if keep else None, "a": a, "U": U, "Up": Up}
            if i_co is not None:
                return {"status": "collapse", "sols": sols if keep else None, "a": a}
        if failed:
            return {"status": "fail", "r_fail": r_end, "a": a,
                    "sols": sols if keep else None}
        y = sol.y[:, -1]
        r0 = r1
        chunk = min(chunk * 1.6, chunk_max)
    return {"status": "no-seal", "sols": sols if keep else None, "a": a}


def miss_dp(dprime, **kw):
    """Root function in d' (above side): a = 1.5*(1+d'); returns (rho'(r_s), shot dict)."""
    o = shoot(1.5 * (1.0 + dprime), **kw)
    return (float(o["y_s"][3]) if o["status"] == "seal" else np.nan), o


def eval_traj(sols, rr):
    """Evaluate stacked chunk dense outputs at sorted points rr."""
    out = np.empty((4, rr.size))
    bounds = np.array([s.t[-1] for s in sols])
    idx = np.clip(np.searchsorted(bounds, rr, side="left"), 0, len(sols) - 1)
    for k in range(len(sols)):
        m = idx == k
        if np.any(m):
            out[:, m] = sols[k].sol(rr[m])
    return out


def graded_count(f):
    """Interior sign changes of f above graduated RELATIVE floors.
    Floors 1e-1..1e-12 at 4/decade; stable = same count over >= 2 decades (>=9 pts)."""
    fmax = float(np.max(np.abs(f)))
    fracs = 10.0 ** (-np.arange(4, 49) / 4.0)
    prof = []
    for fr in fracs:
        m = np.abs(f) > fr * fmax
        s = np.sign(f[m])
        prof.append(int(np.sum(s[1:] * s[:-1] < 0)) if s.size > 1 else 0)
    runs, i = [], 0
    while i < len(prof):
        j = i
        while j + 1 < len(prof) and prof[j + 1] == prof[i]:
            j += 1
        runs.append((i, j, prof[i]))
        i = j + 1
    good = [(i, j, c) for (i, j, c) in runs if (j - i) >= 8]
    if not good:
        return None, prof
    best = max(good, key=lambda t: (t[1] - t[0], t[0]))
    return best[2], prof


def characterize(o, npts=100001):
    """Full identity suite on a sealed shot with kept dense output."""
    r_s, U = o["r_s"], o["U"]
    rr = np.linspace(0.0, r_s, npts)
    phi, phip, rho, rhop = eval_traj(o["sols"], rr)
    e2p = np.exp(2.0 * phi)
    Nd, _ = graded_count((rho - 1.0)[1:-1])
    Np, _ = graded_count(rhop[1:-1])
    H = 0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 / e2p - 2.0 + U(rho)
    m_ms = 0.5 * rho * (1.0 - rhop ** 2 / e2p)
    phi_s, phip_s, rho_s, rhop_s = o["y_s"]
    q = Z * rho_s ** 2 * phip_s
    d = dict(r_s=r_s, rho_s=float(rho_s), q=float(q),
             rhop_seal=float(rhop_s),
             dphi_res=float((phi[-1] - phi[0]) - LN1101),
             ms_seal=float(2 * m_ms[-1] / rho[-1]),
             H_drift=float(np.max(np.abs(H))),
             L_proper=float(np.trapezoid(np.exp(phi), rr)),
             U_seal_id_res=float(U(rho_s) - (2.0 - q ** 2 / (2.0 * Z * rho_s ** 2))),
             N_delta=Nd, N_rhop=Np,
             rho_monotone_dec=bool(np.all(np.diff(rho) < 0)),
             n_rho_increase=int(np.sum(np.diff(rho) > 0)))
    return d
