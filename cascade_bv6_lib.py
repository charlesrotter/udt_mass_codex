"""bv6 blind-verifier library.

Reuses ONLY rhs + make_risefall_slice from cell_solver_universe_T3.py.
Own integrator: chunked DOP853 (solver uses LSODA + scipy events -- independent).
Own event location: sign-scan of dense output + 80-step bisection on the interpolant.
Own root finder: Illinois (bracketing regula-falsi variant) with bisection fallback.
Own zero counter: graduated-floor sign-change counter, >=2-decade stability, 2x re-check.

Shot definition (ledger): 1 shot = 1 full trajectory evaluation g(a) (all chunks of one IVP).
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

SHOTS = {"n": 0}  # global ledger


def shoot(a, Z=8.0, m=3.0, rtol=1e-11, atol=1e-13, r_cap=3.0e5,
          chunk0=2.0, chunk_max=500.0, keep_sols=False):
    """Integrate from the inner fold to the first phi=0 upcrossing (my own event location).
    Returns dict: status in {seal, no-seal, collapse, fail}; on seal: r_s, y_s (phi,phip,rho,rhop),
    and (if keep_sols) the list of chunk dense solutions."""
    SHOTS["n"] += 1
    U, Up, _ = make_risefall_slice(a, m=m)
    y = np.array([PHI_C, 0.0, 1.0, 0.0])
    r0, chunk = 0.0, chunk0
    sols = []
    while r0 < r_cap:
        r1 = min(r0 + chunk, r_cap)
        sol = solve_ivp(rhs, (r0, r1), y, args=(Z, Up), method="DOP853",
                        rtol=rtol, atol=atol, dense_output=True)
        failed = (not sol.success) or (not np.all(np.isfinite(sol.y[:, -1])))
        r_end = float(sol.t[-1])
        if keep_sols:
            sols.append(sol)
        # scan whatever portion WAS integrated (a failed chunk may still contain the seal)
        if r_end > r0:
            nsub = max(400, 4 * len(sol.t))
            rr = np.linspace(r0, r_end, nsub)
            vals = sol.sol(rr)
            ph, rho = vals[0], vals[2]
            cross = np.where((ph[:-1] < 0.0) & (ph[1:] >= 0.0))[0]
            coll = np.where(rho <= 1e-9)[0]
            i_cross = cross[0] if cross.size else None
            i_coll = coll[0] if coll.size else None
            if i_cross is not None and (i_coll is None or i_cross < i_coll):
                lo, hi = rr[i_cross], rr[i_cross + 1]
                for _ in range(80):                   # own bisection on the interpolant
                    mid = 0.5 * (lo + hi)
                    if sol.sol(mid)[0] < 0.0:
                        lo = mid
                    else:
                        hi = mid
                r_s = 0.5 * (lo + hi)
                y_s = sol.sol(r_s)
                return {"status": "seal", "r_s": float(r_s), "y_s": np.asarray(y_s),
                        "sols": sols if keep_sols else None,
                        "U": U, "Up": Up, "a": a, "Z": Z}
            if i_coll is not None:
                return {"status": "collapse", "sols": sols if keep_sols else None}
        if failed:
            return {"status": "fail", "r_fail": r_end, "sols": sols if keep_sols else None}
        y = sol.y[:, -1]
        r0 = r1
        chunk = min(chunk * 1.6, chunk_max)
    return {"status": "no-seal", "sols": sols if keep_sols else None}


def g_of_a(a, **kw):
    """Root function: rho'(r_s); nan if no seal."""
    o = shoot(a, **kw)
    if o["status"] == "seal":
        return float(o["y_s"][3]), o
    return float("nan"), o


def eval_piecewise(sols, rr):
    """Evaluate stacked chunk dense outputs at points rr (sorted)."""
    out = np.empty((4, rr.size))
    bounds = np.array([s.t[-1] for s in sols])
    idx = np.searchsorted(bounds, rr, side="left")
    idx = np.clip(idx, 0, len(sols) - 1)
    for k in range(len(sols)):
        mask = idx == k
        if np.any(mask):
            out[:, mask] = sols[k].sol(rr[mask])
    return out


def sign_changes(s, floor):
    """Count sign changes of s restricted to |s| > floor."""
    m = np.abs(s) > floor
    sg = np.sign(s[m])
    if sg.size < 2:
        return 0
    return int(np.sum(sg[1:] != sg[:-1]))


def graduated_count(s, floors=None):
    """Return (counts per floor, stable count or None). Stability = same count over >=3
    consecutive floors (>=2 decades)."""
    if floors is None:
        floors = [10.0 ** e for e in range(-4, -12, -1)]  # 1e-4 .. 1e-11
    counts = [sign_changes(s, f) for f in floors]
    best = None
    run_start, run_len = 0, 1
    for i in range(1, len(counts)):
        if counts[i] == counts[i - 1]:
            run_len += 1
        else:
            run_start, run_len = i, 1
        if run_len >= 3 and best is None:
            best = counts[i]
        elif run_len >= 3:
            best = counts[i] if best is None else best
    # choose the FIRST (largest-floor) stable plateau of length >=3
    plateau = None
    i = 0
    while i < len(counts):
        j = i
        while j + 1 < len(counts) and counts[j + 1] == counts[i]:
            j += 1
        if j - i + 1 >= 3:
            plateau = counts[i]
            break
        i = j + 1
    return counts, plateau, [float(f) for f in floors]


def diagnose(o, nsamp=20001):
    """Full diagnostics on a sealed, root-refined shot (needs keep_sols=True).
    N_delta / N_rho' with graduated floors + 2x re-check; identities; L_proper; chi."""
    sols, r_s = o["sols"], o["r_s"]
    Z, U = o["Z"], o["U"]
    res = {"a": o["a"], "r_s": r_s}
    ys = o["y_s"]
    phi_s, phip_s, rho_s, rhop_s = [float(v) for v in ys]
    res.update(phi_s=phi_s, phip_s=phip_s, rho_s=rho_s, rhop_s=rhop_s,
               q=Z * rho_s ** 2 * phip_s)
    counts = {}
    for tag, n in (("1x", nsamp), ("2x", 2 * nsamp)):
        rr = np.linspace(0.0, r_s, n)[1:-1]
        v = eval_piecewise(sols, rr)
        delta = v[2] - 1.0
        rp = v[3]
        cd, pd_, fl = graduated_count(delta)
        cp, pp_, _ = graduated_count(rp)
        counts[tag] = {"N_delta_counts": cd, "N_delta": pd_,
                       "N_rhop_counts": cp, "N_rhop": pp_, "floors": fl}
    res["counts"] = counts
    # identities + proper length on a fine grid
    rr = np.linspace(0.0, r_s, nsamp)
    v = eval_piecewise(sols, rr)
    phi, phip, rho, rhop = v
    L = float(np.trapezoid(np.exp(phi), rr))          # L_proper = int e^phi dr (defn stated)
    res["L_proper"] = L
    res["chi"] = L / rho_s
    res["dphi_carried"] = phi_s - float(phi[0])
    res["dphi_dev"] = res["dphi_carried"] - LN1101
    m_s = 0.5 * rho_s * (1.0 - np.exp(-2.0 * phi_s) * rhop_s ** 2)
    res["two_m_over_rho_seal"] = 2.0 * m_s / rho_s
    res["two_m_over_rho_dev"] = res["two_m_over_rho_seal"] - 1.0
    H = 0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 / np.exp(2 * phi) - 2.0 + U(rho)
    res["H_drift"] = float(np.max(np.abs(H)))
    res["min_rho"] = float(rho.min())
    res["max_rho"] = float(rho.max())
    return res


def illinois(a, b, fa, fb, xtol=1e-11, maxit=22, shoot_kw=None):
    """Own bracketing root finder (Illinois). Returns (a*, g*, width, best_out, nev)."""
    shoot_kw = shoot_kw or {}
    best = None  # (abs_g, a, out)
    nev = 0
    Fa, Fb = fa, fb
    side = 0
    lo, hi = a, b
    for _ in range(maxit):
        c = (lo * Fb - hi * Fa) / (Fb - Fa)
        w = hi - lo
        if not (lo + 1e-16 * abs(lo) < c < hi - 1e-16 * abs(hi)):
            c = 0.5 * (lo + hi)
        fc, oc = g_of_a(c, keep_sols=True, **shoot_kw)
        nev += 1
        if not np.isfinite(fc):
            # fallback: plain bisection step using midpoint status unknown -> shrink toward lo
            c = 0.5 * (lo + hi)
            fc, oc = g_of_a(c, keep_sols=True, **shoot_kw)
            nev += 1
            if not np.isfinite(fc):
                break
        if best is None or abs(fc) < best[0]:
            best = (abs(fc), c, oc)
        if fa * fc < 0:
            hi, Fb = c, fc
            if side == -1:
                Fa *= 0.5
            side = -1
        else:
            lo, Fa = c, fc
            fa = fc
            if side == +1:
                Fb *= 0.5
            side = +1
        if hi - lo < xtol:
            break
    return best[1], best[0], hi - lo, best[2], nev
