"""stageA_lib.py -- Stage A persistence survey library (observe-mode).
Reuses cell_solver_universe_T3.rhs + fold ICs; adds method-parameterized shoot
(bv4 two-method-check pattern), slice families A1/A2/A3, coarse scan, brentq
root refinement, two-method verification, and per-root Stage-B diagnostics
(PRIMARY N_delta = interior zeros of rho-1; SEPARATE N_rhop = interior zeros
of rho'; never merged). No interpretation anywhere -- data collection only.
"""
import sys, json, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, LN1101   # banked EOMs + anchor

SHOTS = {"n": 0}          # global IVP-shot counter (budget ledger)


# --------------------------------------------------------------- slice families (all CHOSE)
def make_A1(m, a):
    """U = 2 rho^m exp(-a(rho^2-1)); U(1)=2; U'(1)=2(m-2a) -> stuck a=m/2."""
    def U(rho):  return 2.0 * rho ** m * np.exp(-a * (rho * rho - 1.0))
    def Up(rho): return (2.0 * rho ** m * np.exp(-a * (rho * rho - 1.0))) * (m / rho - 2.0 * a * rho)
    return U, Up, f"A1 m={m} a={a:.10f}"

def make_A2(k, a):
    """U = 2 rho^2 exp(-a(rho^k-1)); U(1)=2; U'(1)=2(2-ak) -> stuck a=2/k."""
    def U(rho):  return 2.0 * rho ** 2 * np.exp(-a * (rho ** k - 1.0))
    def Up(rho): return (2.0 * rho ** 2 * np.exp(-a * (rho ** k - 1.0))) * (2.0 / rho - a * k * rho ** (k - 1.0))
    return U, Up, f"A2 k={k} a={a:.10f}"

def make_A3(b):
    """U = 2 rho^2 (1+b)/(1+b rho^4); U(1)=2; U'(1)=4(1-b)/(1+b) -> stuck b=1."""
    def U(rho):  return 2.0 * rho ** 2 * (1.0 + b) / (1.0 + b * rho ** 4)
    def Up(rho): return 2.0 * (1.0 + b) * (2.0 * rho - 2.0 * b * rho ** 5) / (1.0 + b * rho ** 4) ** 2
    return U, Up, f"A3 b={b:.10f}"


# --------------------------------------------------------------- shoot (method-parameterized)
def shoot2(Z, U, Up, rho_c=1.0, r_max=1.0e6, rtol=1e-10, atol=1e-12, method="LSODA",
           dense=False):
    SHOTS["n"] += 1
    seal = lambda r, y, *a: y[0]
    seal.terminal, seal.direction = True, +1
    coll = lambda r, y, *a: y[2] - 1e-9 * rho_c
    coll.terminal, coll.direction = True, -1
    sol = solve_ivp(rhs, (0.0, r_max), [PHI_C, 0.0, rho_c, 0.0], args=(Z, Up),
                    method=method, rtol=rtol, atol=atol, events=[seal, coll],
                    dense_output=dense)
    out = {"status": "no-seal(rmax)", "sol": sol, "r_end": sol.t[-1]}
    if sol.t_events[1].size:
        out["status"] = "collapse"
        out["r_coll"] = float(sol.t_events[1][0])
        return out
    if not sol.t_events[0].size:
        return out
    r_s = float(sol.t_events[0][0])
    phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
    out.update(status="seal", r_s=r_s, rho_s=float(rho_s), rhop_s=float(rhop_s),
               phip_s=float(phip_s), q=float(Z * rho_s ** 2 * phip_s))
    return out


def miss_at(family, Z, p, rtol=1e-10, method="LSODA", r_max=1.0e6, dense=False):
    """family = ('A1', m) / ('A2', k) / ('A3',); p = slice parameter (a or b)."""
    if family[0] == "A1":   U, Up, lab = make_A1(family[1], p)
    elif family[0] == "A2": U, Up, lab = make_A2(family[1], p)
    else:                   U, Up, lab = make_A3(p)
    o = shoot2(Z, U, Up, rtol=rtol, atol=rtol * 1e-2, method=method, r_max=r_max,
               dense=dense)
    o["U"], o["Up"], o["label"] = U, Up, lab
    f = o["rhop_s"] if o["status"] == "seal" else np.nan
    return f, o


# --------------------------------------------------------------- diagnostics (Stage-B collect)
def diagnose_root(o, Z, n_samp=60001, noise_rel=1e-8):
    """Per-root record. N_delta = interior sign changes of rho-1 (PRIMARY, pre-named);
    N_rhop = interior sign changes of rho' (SEPARATE). Endpoints excluded by sampling
    (0, r_s) open. Small-|value| samples below noise_rel*max|value| dropped before
    sign counting (noise floor reported)."""
    sol, r_s = o["sol"], o["r_s"]
    rr = np.linspace(r_s * 1e-6, r_s * (1.0 - 1e-6), n_samp)
    phi, phip, rho, rhop = sol.sol(rr)
    e2p = np.exp(2.0 * phi)
    U = o["U"]
    H = 0.5 * Z * rho ** 2 * phip ** 2 - 2.0 * rhop ** 2 / e2p - 2.0 + U(rho)

    def count_zeros(v):
        amp = np.max(np.abs(v))
        tau = noise_rel * amp if amp > 0 else 0.0
        s = np.sign(v[np.abs(v) > tau])
        return int(np.sum(s[1:] != s[:-1])), float(tau)

    N_delta, tau_d = count_zeros(rho - 1.0)
    N_rhop, tau_p = count_zeros(rhop)
    L = float(np.trapezoid(np.exp(phi), rr))
    return {
        "r_s": r_s, "rho_s": o["rho_s"], "q": o["q"], "miss_at_root": o["rhop_s"],
        "L_proper": L, "chi": L / o["rho_s"],
        "N_delta": N_delta, "N_rhop": N_rhop,
        "noise_floor_delta": tau_d, "noise_floor_rhop": tau_p,
        "H_drift_max": float(np.max(np.abs(H))), "n_samp": n_samp,
        "sample_dr": float(rr[1] - rr[0]),
    }


# --------------------------------------------------------------- coarse scan + roots
def coarse_grid(stuck, below_n=15, below_hi=0.4, below_lo=0.0008,
                above=(0.0015, 0.004, 0.012, 0.035, 0.1)):
    """Relative offsets from the stuck point, geometric on the approach (below) side."""
    d_below = np.geomspace(below_hi, below_lo, below_n)
    pts = [stuck * (1.0 - d) for d in d_below] + [stuck * (1.0 + d) for d in above]
    return sorted(pts)


def scan(family, Z, grid, r_max=1.0e6):
    rows = []
    for p in grid:
        f, o = miss_at(family, Z, p, r_max=r_max)
        rows.append({"p": float(p), "miss": (float(f) if np.isfinite(f) else None),
                     "status": o["status"],
                     "rho_s": o.get("rho_s"), "r_s": o.get("r_s"),
                     "q": o.get("q")})
    return rows


def find_brackets(rows):
    """Adjacent seal-seal sign changes; also record status transitions (not bisectable)."""
    br, trans = [], []
    for r1, r2 in zip(rows, rows[1:]):
        if r1["status"] == r2["status"] == "seal" and r1["miss"] is not None \
                and r2["miss"] is not None and r1["miss"] * r2["miss"] < 0:
            br.append((r1["p"], r2["p"]))
        elif r1["status"] != r2["status"]:
            trans.append((r1["p"], r1["status"], r2["p"], r2["status"]))
    return br, trans


def refine_root(family, Z, lo, hi, rtol=1e-10, method="LSODA", xtol=1e-12,
                r_max=1.0e6):
    f = lambda p: miss_at(family, Z, p, rtol=rtol, method=method, r_max=r_max)[0]
    try:
        root, res = brentq(f, lo, hi, xtol=xtol, rtol=1e-15, maxiter=80,
                           full_output=True)
        return float(root), int(res.function_calls)
    except Exception as e:
        return None, str(e)


def verify_root(family, Z, p_star, stuck, r_max=1.0e6):
    """Two-method check (bv4 pattern): re-find the root (i) rtol=1e-11 LSODA,
    (ii) rtol=1e-10 Radau, each in a tight bracket around p_star. >=6-digit
    agreement in the parameter required to CONFIRM."""
    out = {}
    for tag, kw in (("rtol1e-11_LSODA", dict(rtol=1e-11, method="LSODA")),
                    ("rtol1e-10_Radau", dict(rtol=1e-10, method="Radau"))):
        w = max(1e-8 * max(abs(p_star), 1.0), 1e-4 * abs(p_star - stuck))
        got = None
        for widen in (1.0, 30.0):
            lo, hi = p_star - w * widen, p_star + w * widen
            f = lambda p: miss_at(family, Z, p, r_max=r_max, **kw)[0]
            flo, fhi = f(lo), f(hi)
            if np.isfinite(flo) and np.isfinite(fhi) and flo * fhi < 0:
                try:
                    got = float(brentq(f, lo, hi, xtol=1e-12, rtol=1e-15, maxiter=60))
                except Exception:
                    got = None
                break
        out[tag] = got
    ok = all(v is not None and abs(v - p_star) <= 5e-7 * abs(p_star)
             for v in out.values())
    out["confirmed"] = bool(ok)
    out["rel_diffs"] = {k: (abs(v - p_star) / abs(p_star) if v is not None else None)
                        for k, v in out.items() if k.endswith(("LSODA", "Radau"))}
    return out


# --------------------------------------------------------------- family pre-checks (no shots)
def precheck(family, stuck):
    if family[0] == "A1":   mk = lambda p: make_A1(family[1], p)
    elif family[0] == "A2": mk = lambda p: make_A2(family[1], p)
    else:                   mk = lambda p: make_A3(p)
    h = 1e-6
    rec = {}
    for tag, p in (("below", stuck * (1 - 0.01)), ("at", stuck), ("above", stuck * (1 + 0.01))):
        U, Up, _ = mk(p)
        fd = (U(1 + h) - U(1 - h)) / (2 * h)
        rec[tag] = {"p": p, "U(1)": float(U(1.0)), "Up(1)_analytic": float(Up(1.0)),
                    "Up(1)_fd": float(fd)}
    return rec
