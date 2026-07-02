"""Stage B two-method spot checks: re-bisect selected roots with (i) Radau rtol=1e-9/atol=1e-11
and, for first/middle/highest, also (ii) LSODA rtol=1e-12/atol=1e-14. Agreement target >=6 digits
in a (abs 1.5e-6). Output: stageB_twomethod.json"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss, rhs, PHI_C
from scipy.integrate import solve_ivp

Z, M = 8.0, 3.0
SCR = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad"
SHOTS = 0

def f_alt(d, method, rtol, atol):
    global SHOTS
    a = 1.5 * (1.0 - d)
    U, Up, _ = make_risefall_slice(a, m=M)
    SHOTS += 1
    if method == "LSODA":
        f, o = miss(Z, U, Up, 1.0, rtol=rtol, atol=atol)
        return f
    seal = lambda r, y, *aa: y[0]; seal.terminal, seal.direction = True, +1
    collapse = lambda r, y, *aa: y[2] - 1e-9; collapse.terminal, collapse.direction = True, -1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="Radau", rtol=rtol, atol=atol, events=[seal, collapse])
    if sol.t_events[1].size or not sol.t_events[0].size: return np.nan
    return sol.y_events[0][0][3]

def rebisect(d_hi, d_lo, method, rtol, atol, tol_d=1.0e-7, maxit=12):
    fhi = f_alt(d_hi, method, rtol, atol)
    if not np.isfinite(fhi): return None, "no-seal-at-hi"
    lo, hi = d_lo, d_hi
    it = 0
    while (hi - lo) > tol_d and it < maxit:
        mid = 0.5 * (lo + hi)
        fm = f_alt(mid, method, rtol, atol)
        it += 1
        if not np.isfinite(fm): return None, f"no-seal-at-mid-{mid:.4e}"
        if fhi * fm < 0: lo = mid
        else: hi, fhi = mid, fm
    return 0.5 * (lo + hi), "ok"

rungs = json.load(open(f"{SCR}/stageB_rungs.json"))["rungs"]
CHECK = [0, 3, 7, 11, 15, 19, 22]          # ~1/3 incl. first, middle, highest-N refined
DOUBLE = {0, 11, 22}                        # also the second alt config
t0 = time.time()
out = []
for bi in CHECK:
    r = rungs[bi]
    d_hi, d_lo = r["d_bracket"]
    base = r["d_star"]; a_base = r["a_star"]
    res = {"bracket_index": bi, "a_base": a_base, "N": r["N_delta"]}
    d1, s1 = rebisect(d_hi, d_lo, "Radau", 1e-9, 1e-11)
    res["radau"] = {"status": s1, "a": 1.5*(1-d1) if d1 else None,
                    "delta_a": abs(1.5*(1-d1) - a_base) if d1 else None}
    if bi in DOUBLE:
        d2, s2 = rebisect(d_hi, d_lo, "LSODA", 1e-12, 1e-14)
        res["lsoda_tight"] = {"status": s2, "a": 1.5*(1-d2) if d2 else None,
                              "delta_a": abs(1.5*(1-d2) - a_base) if d2 else None}
    ok = all(v.get("delta_a") is not None and v["delta_a"] < 1.5e-6
             for k, v in res.items() if isinstance(v, dict))
    res["verdict"] = "CONFIRMED(>=6 digits)" if ok else "UNCONFIRMED"
    out.append(res)
    print(f"[{bi:2d}] N={res['N']:2d} a_base={a_base:.10f} "
          f"radau_da={res['radau'].get('delta_a')} "
          + (f"lsoda12_da={res['lsoda_tight'].get('delta_a')} " if bi in DOUBLE else "")
          + res["verdict"])

json.dump({"checks": out, "shots_this_script": SHOTS},
          open(f"{SCR}/stageB_twomethod.json", "w"), indent=1)
print(f"\nshots this script = {SHOTS}, wall = {time.time()-t0:.1f}s")
