"""bv7 blind-verifier core harness.

Reuses ONLY `rhs` + `make_risefall_slice` from cell_solver_universe_T3.py.
Own: DOP853 chunked integrator, own event location (dense-interpolant sign scan +
Brent on the interpolant -- costs NO extra IVP shots), own bracketing root-finder
(secant-with-forced-bisection safeguard), own hysteresis zero counter with
graduated floors (>=2-decade stability required) at 100k + 200k samples.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq as _interp_brent  # used ONLY on dense interpolants
import importlib.util

REPO = "/home/udt-admin/udt_mass_codex"
_spec = importlib.util.spec_from_file_location("t3mod", REPO + "/cell_solver_universe_T3.py")
_t3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_t3)
rhs = _t3.rhs                                # REUSED (allowed)
make_risefall_slice = _t3.make_risefall_slice  # REUSED (allowed)

LN1101 = float(np.log(1101.0))
PHI_C = -LN1101

SHOTS = {"n": 0}


# ------------------------------------------------------------ slices I define myself
def make_A2_slice(a, k=3.0, m=2.0):
    """U = 2 rho^m exp(-a (rho^k - 1)); stuck (U'(1)=0) at a = m/k."""
    def U(rho):
        return 2.0 * rho ** m * np.exp(-a * (rho ** k - 1.0))
    def Up(rho):
        u = 2.0 * rho ** m * np.exp(-a * (rho ** k - 1.0))
        return u * (m / rho - a * k * rho ** (k - 1.0))
    return U, Up


def make_A3_slice(b):
    """U = 2 rho^2 (1+b) / (1 + b rho^4); stuck at b = 1."""
    def U(rho):
        return 2.0 * rho ** 2 * (1.0 + b) / (1.0 + b * rho ** 4)
    def Up(rho):
        return 4.0 * (1.0 + b) * rho * (1.0 - b * rho ** 4) / (1.0 + b * rho ** 4) ** 2
    return U, Up


# ------------------------------------------------------------ own shooter
class Traj:
    """Piecewise dense-output evaluator across integration chunks."""
    def __init__(self):
        self.segs = []
    def add(self, r0, r1, f):
        self.segs.append((r0, r1, f))
    def __call__(self, r):
        r = np.atleast_1d(np.asarray(r, float))
        out = np.full((4, r.size), np.nan)
        for (r0, r1, f) in self.segs:
            m = (r >= r0) & (r <= r1)
            if m.any():
                out[:, m] = f(r[m])
        return out


def shoot(Z, Up, rtol=1e-11, atol=1e-13, r_cap=1.0e6, chunk0=100.0, grow=2.0,
          chunk_max=5.0e4):
    """IC: phi=-ln(1101), phi'=0, rho=1, rho'=0 at r=0. Terminate at first phi=0
    UPcrossing (seal) or rho collapse. Hazard-aware: every chunk's dense output is
    scanned for events BEFORE moving on (including aborted chunks)."""
    SHOTS["n"] += 1
    y = np.array([PHI_C, 0.0, 1.0, 0.0])
    r0, chunk = 0.0, chunk0
    traj = Traj()
    while r0 < r_cap:
        r1 = min(r0 + chunk, r_cap)
        sol = solve_ivp(rhs, (r0, r1), y, args=(Z, Up), method="DOP853",
                        rtol=rtol, atol=atol, dense_output=True)
        r_end = sol.t[-1]
        if r_end > r0:
            traj.add(r0, r_end, sol.sol)
            ns = max(4000, 30 * len(sol.t))
            rr = np.linspace(r0, r_end, ns)
            vals = sol.sol(rr)
            phi, rho = vals[0], vals[2]
            up = np.where((phi[:-1] < 0.0) & (phi[1:] >= 0.0))[0]
            col = np.where(rho[1:] <= 1e-9)[0]
            i_up = int(up[0]) if up.size else None
            i_col = int(col[0]) if col.size else None
            if i_col is not None and (i_up is None or i_col < i_up):
                return {"status": "collapse", "r": float(rr[i_col + 1]), "traj": traj}
            if i_up is not None:
                fphi = lambda r: float(sol.sol(r)[0])
                a_, b_ = float(rr[i_up]), float(rr[i_up + 1])
                if fphi(b_) == 0.0:
                    r_s = b_
                else:
                    r_s = _interp_brent(fphi, a_, b_, xtol=1e-12 * max(1.0, b_),
                                        rtol=8.9e-16)
                ys = sol.sol(r_s)
                return {"status": "seal", "r_s": float(r_s), "phi_s": float(ys[0]),
                        "phip_s": float(ys[1]), "rho_s": float(ys[2]),
                        "rhop_s": float(ys[3]),
                        "q": float(Z * ys[2] ** 2 * ys[1]), "traj": traj}
        if sol.status != 0:
            return {"status": "fail:%s" % sol.status, "r": float(r_end), "traj": traj}
        y = sol.y[:, -1]
        r0 = r_end
        chunk = min(chunk * grow, chunk_max)
    return {"status": "no-seal", "r": float(r_cap), "traj": traj}


# ------------------------------------------------------------ own root-finder
def bracket_root(F, a, b, fa, fb, xtol=1e-10, maxiter=28):
    """Own bracketing root-finder: secant step, forced-bisection safeguard (every 2
    iters the bracket must have halved, else bisect). Reuses endpoint f values.
    F(x) -> (f, out). Returns (x*, f*, out*, n_iters, converged)."""
    assert np.isfinite(fa) and np.isfinite(fb) and fa * fb < 0
    cache = []
    side = 0
    it = 0
    while (b - a) > xtol and it < maxiter:
        it += 1
        x = (a * fb - b * fa) / (fb - fa)
        if not (a < x < b):
            x = 0.5 * (a + b)
        f, out = F(x)
        cache.append((abs(f) if np.isfinite(f) else np.inf, x, f, out))
        if not np.isfinite(f):
            # non-seal point inside a seal-seal bracket: abort honestly
            break
        if f == 0.0:
            a = b = x
            break
        if fa * f < 0:
            b, fb = x, f
            if side == -1:
                fa *= 0.5           # Illinois: unstick the stagnant end
            side = -1
        else:
            a, fa = x, f
            if side == +1:
                fb *= 0.5
            side = +1
    cache.sort(key=lambda t: t[0])
    _, x_best, f_best, out_best = cache[0]
    return x_best, f_best, out_best, it, (b - a) <= xtol


# ------------------------------------------------------------ own zero counter
def hyst_count(f, floor):
    """Hysteresis zero count: sign changes of the subsequence with |f|>floor."""
    s = np.sign(f[np.abs(f) > floor])
    if s.size == 0:
        return 0
    return int(np.sum(s[1:] != s[:-1]))


def plateau_count(f):
    """Graduated floors amax*10^-k, k=2..13; longest equal-count run = plateau.
    Returns (counts list, ks, best=(runlen, count, (k_lo,k_hi)))."""
    amax = float(np.max(np.abs(f)))
    ks = list(range(2, 14))
    counts = [hyst_count(f, amax * 10.0 ** (-k)) for k in ks]
    best = (0, None, (None, None))
    i = 0
    while i < len(counts):
        j = i
        while j + 1 < len(counts) and counts[j + 1] == counts[i]:
            j += 1
        if j - i + 1 > best[0]:
            best = (j - i + 1, counts[i], (ks[i], ks[j]))
        i = j + 1
    return counts, ks, best


def diagnose(out, Z, U):
    """Twin zero counts (100k + 2x recheck), identities, drift, for a sealed root."""
    r_s, traj = out["r_s"], out["traj"]
    res = {"r_s": r_s, "rho_s": out["rho_s"], "rhop_s_resid": out["rhop_s"],
           "q": out["q"], "phi_s": out["phi_s"],
           "Dphi_carried": out["phi_s"] + LN1101,
           "ms_seal": 1.0 - out["rhop_s"] ** 2 * np.exp(-2.0 * out["phi_s"])}
    for tag, nsamp in (("100k", 100000), ("200k", 200000)):
        rr = np.linspace(0.0, r_s, nsamp + 2)[1:-1]
        phi, phip, rho, rhop = traj(rr)
        delta = rho - 1.0
        cd, ksd, bd = plateau_count(delta)
        cp, ksp, bp = plateau_count(rhop)
        res["Nd_" + tag] = bd
        res["Np_" + tag] = bp
        res["Nd_ladder_" + tag] = cd
        res["Np_ladder_" + tag] = cp
        if tag == "100k":
            H = (0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 * np.exp(-2.0 * phi)
                 - 2.0 + U(rho))
            res["H_drift"] = float(np.max(np.abs(H)))
            res["U_seal_identity_res"] = float(
                U(out["rho_s"]) - (2.0 - out["q"] ** 2 / (2.0 * Z * out["rho_s"] ** 2)))
    return res


def fmt_root(label, p, d, res):
    n1 = res["Nd_100k"]; n2 = res["Nd_200k"]
    m1 = res["Np_100k"]; m2 = res["Np_200k"]
    return (f"{label}: p*={p:.12f} d={d:.10e} rho_s={res['rho_s']:.9f} "
            f"q={res['q']:.8f} r_s={res['r_s']:.6f} | "
            f"N_delta={n1[1]}(run{n1[0]},k{n1[2]})/{n2[1]}(run{n2[0]}) "
            f"N_rhop={m1[1]}(run{m1[0]},k{m1[2]})/{m2[1]}(run{m2[0]}) | "
            f"rhop_resid={res['rhop_s_resid']:.2e} Hdrift={res['H_drift']:.2e} "
            f"Useal_id={res['U_seal_identity_res']:.2e} "
            f"Dphi={res['Dphi_carried']:.14f} ms_seal={res['ms_seal']:.12f}")
