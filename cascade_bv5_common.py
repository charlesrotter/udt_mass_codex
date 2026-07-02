"""bv5 blind-verifier common machinery.
REUSED from cell_solver_universe_T3.py (allowed): the rhs function (retyped) + slice definitions.
EVERYTHING ELSE (integration driver, event location, bisection, zero counting) is my own.
Integrator: DOP853 (NOT LSODA), chunked, my own upcrossing detection + brentq refinement.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

LN1101 = float(np.log(1101.0))
PHI_C = -LN1101

SHOTS = {"n": 0}   # global IVP-shot counter


# ---------------- slices (from the task spec / solver header; allowed reuse) ----------------
def make_A1(m, a):
    """U = 2 rho^m exp(-a(rho^2-1)); stuck a=m/2."""
    def U(rho):  return 2.0 * rho**m * np.exp(-a*(rho*rho - 1.0))
    def Up(rho): return 2.0 * rho**m * np.exp(-a*(rho*rho - 1.0)) * (m/rho - 2.0*a*rho)
    return U, Up


def make_A3(b):
    """U = 2 rho^2 (1+b)/(1+b rho^4); stuck b=1."""
    def U(rho):  return 2.0 * rho*rho * (1.0+b) / (1.0 + b*rho**4)
    def Up(rho): return 4.0 * (1.0+b) * rho * (1.0 - b*rho**4) / (1.0 + b*rho**4)**2
    return U, Up


def make_A2(k, a):
    """U = 2 rho^2 exp(-a(rho^k-1)); stuck a=2/k."""
    def U(rho):  return 2.0 * rho*rho * np.exp(-a*(rho**k - 1.0))
    def Up(rho): return 2.0 * rho * np.exp(-a*(rho**k - 1.0)) * (2.0 - a*k*rho**k)
    return U, Up


# ---------------- rhs (RETYPED from cell_solver_universe_T3.py -- allowed reuse) ----------------
def rhs_clean(r, y, Z, Up):
    phi, phip, rho, rhop = y
    e2p = np.exp(2.0*phi)
    sigma = 0.25 * e2p * Up(rho)
    phipp = 4.0*rhop*rhop/(e2p*Z*rho*rho) - 2.0*phip*rhop/rho
    rhopp = 2.0*phip*rhop - 0.25*Z*rho*e2p*phip*phip + sigma
    return [phip, phipp, rhop, rhopp]


# ---------------- my own shooter: DOP853, chunked, own event location ----------------
def shoot_bv5(Z, Up, r_max=2.0e5, rtol=1e-10, atol=1e-12, samples_per_chunk=4000,
              keep_segments=False):
    """Integrate from the inner fold; locate the FIRST phi=0 upcrossing myself.
    Returns dict: status in {seal, collapse, no-seal, fail}; at seal: r_s, y_s, segments."""
    SHOTS["n"] += 1
    y0 = [PHI_C, 0.0, 1.0, 0.0]
    edges = [0.0]
    e = 100.0
    while e < r_max:
        edges.append(e); e *= 4.0
    edges.append(r_max)
    segments = []
    out = {"status": "no-seal", "r_end": r_max}
    for r0, r1 in zip(edges, edges[1:]):
        sol = solve_ivp(rhs_clean, (r0, r1), y0, args=(Z, Up), method="DOP853",
                        rtol=rtol, atol=atol, dense_output=True)
        aborted = sol.status < 0
        r1_eff = sol.t[-1]          # on abort, inspect the PARTIAL range before failing
        if aborted and r1_eff <= r0:
            out["status"] = "fail"; out["msg"] = sol.message; out["r_end"] = r1_eff
            if keep_segments: out["segments"] = segments
            return out
        segments.append(sol)
        rr = np.linspace(r0, r1_eff, samples_per_chunk)
        yy = sol.sol(rr)
        phi, rho = yy[0], yy[2]
        # collapse check -- but only BEFORE any phi=0 upcrossing (order in r decides)
        i_col = np.argmax(rho < 1e-9) if (rho < 1e-9).any() else None
        hit_all = np.where((phi[:-1] < 0.0) & (phi[1:] >= 0.0))[0]
        if i_col is not None and (hit_all.size == 0 or i_col <= hit_all[0]):
            out["status"] = "collapse"; out["r_end"] = rr[i_col]
            if keep_segments: out["segments"] = segments
            return out
        # upcrossing detection (my own): first sample interval with phi[i]<0<=phi[i+1]
        hit = hit_all
        # close-approach refinement guard: phi peaks near 0 without sampled crossing
        if hit.size == 0 and phi.max() > -1e-6:
            rr2 = np.linspace(r0, r1_eff, samples_per_chunk*20)
            phi2 = sol.sol(rr2)[0]
            hit2 = np.where((phi2[:-1] < 0.0) & (phi2[1:] >= 0.0))[0]
            if hit2.size:
                rlo, rhi = rr2[hit2[0]], rr2[hit2[0]+1]
            else:
                if aborted:
                    out["status"] = "fail"; out["msg"] = sol.message; out["r_end"] = r1_eff
                    if keep_segments: out["segments"] = segments
                    return out
                y0 = sol.sol(r1); continue
        elif hit.size:
            rlo, rhi = rr[hit[0]], rr[hit[0]+1]
        else:
            if aborted:
                out["status"] = "fail"; out["msg"] = sol.message; out["r_end"] = r1_eff
                if keep_segments: out["segments"] = segments
                return out
            y0 = sol.sol(r1); continue
        fphi = lambda r: float(sol.sol(r)[0])
        r_s = brentq(fphi, rlo, rhi, xtol=1e-13*max(1.0, rhi), rtol=8.9e-16)
        y_s = sol.sol(r_s)
        out.update(status="seal", r_s=float(r_s), y_s=y_s,
                   q=float(Z*y_s[2]**2*y_s[1]), rho_s=float(y_s[2]), rhop_s=float(y_s[3]))
        if keep_segments: out["segments"] = segments
        return out
    if keep_segments: out["segments"] = segments
    return out


def eval_dense(segments, r_arr):
    """Evaluate stored dense segments at r_arr (must lie within covered range)."""
    y = np.empty((4, r_arr.size))
    for seg in segments:
        m = (r_arr >= seg.t[0]) & (r_arr <= seg.t[-1])
        if m.any():
            y[:, m] = seg.sol(r_arr[m])
    return y


def miss_bv5(Z, Up, **kw):
    o = shoot_bv5(Z, Up, **kw)
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o


# ---------------- my own bisection ----------------
def bisect_root(make_slice, Z, p_lo, p_hi, f_lo, f_hi, tol=1e-10, itmax=40, **kw):
    """Bisect miss(param)=rho'(r_s) to |p_hi-p_lo|<tol. Returns (p*, last shot dict, status)."""
    a, b, fa, fb = p_lo, p_hi, f_lo, f_hi
    assert fa*fb < 0
    o_mid = None
    for _ in range(itmax):
        if (b - a) < tol: break
        mid = 0.5*(a+b)
        U, Up = make_slice(mid)
        fm, o_mid = miss_bv5(Z, Up, **kw)
        if not np.isfinite(fm):
            return mid, o_mid, "lost-seal"
        if fa*fm <= 0.0: b, fb = mid, fm
        else:            a, fa = mid, fm
    return 0.5*(a+b), o_mid, "ok"


# ---------------- my own zero counting: run-of-signs with noise floor ----------------
def count_zeros(r, v, floor):
    """Count sign changes of v(r) with |v|>=floor gating (runs-of-signs).
    Returns (count, positions, min_lobe_amp): positions = crossing midpoints;
    min_lobe_amp = smallest max-|v| over the signed lobes adjacent to any crossing."""
    sign = np.where(v > floor, 1, np.where(v < -floor, -1, 0))
    idx = np.nonzero(sign)[0]
    if idx.size < 2:
        return 0, np.array([]), np.nan
    s = sign[idx]
    tr = np.where(s[1:] * s[:-1] < 0)[0]
    positions = 0.5*(r[idx[tr]] + r[idx[tr+1]])
    # lobe amplitudes: split idx into maximal runs of constant sign, take max|v| per run
    breaks = np.where(np.diff(s) != 0)[0]
    lobe_bounds = np.concatenate(([0], breaks+1, [s.size]))
    amps = [np.max(np.abs(v[idx[lobe_bounds[i]:lobe_bounds[i+1]]]))
            for i in range(lobe_bounds.size-1)]
    min_lobe = min(amps) if len(amps) > 1 else np.nan
    return int(tr.size), positions, float(min_lobe)
