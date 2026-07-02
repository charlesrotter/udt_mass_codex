"""Stage B sanity: anchor root A1 m=3 Z=8 a*=1.4813439689 (banked N=0). Timing + U(1)=2 check."""
import sys, time, json
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, shoot, miss, diagnose, LN1101

A_STAR = 1.4813439689
Z = 8.0

U, Up, lab = make_risefall_slice(A_STAR, m=3.0)
print(f"slice: {lab}")
print(f"U(1) = {U(1.0)!r}   (expect 2.0)")
print(f"Up(1) at a=1.5 stuck check: ", end="")
U15, Up15, _ = make_risefall_slice(1.5, m=3.0)
print(f"Up(1)|a=1.5 = {Up15(1.0)!r} (expect 0.0 = stuck point)")

t0 = time.time()
f, o = miss(Z, U, Up, 1.0)
t1 = time.time()
print(f"shot: status={o['status']}  rho'(r_s)={f:+.6e}  wall={t1-t0:.2f}s")
if o["status"] == "seal":
    d = diagnose(o, Z, U)
    for k in ("r_s", "rho_s", "q", "H_drift", "ms_core", "ms_seal"):
        print(f"  {k:12s} = {d[k]}")
    # dense-output eval timing at 100k
    t0 = time.time()
    rr = np.linspace(0.0, o["r_s"], 100001)
    yy = o["sol"].sol(rr)
    t1 = time.time()
    print(f"dense eval 100k: {t1-t0:.2f}s ; rho range [{yy[2].min():.4f},{yy[2].max():.4f}]")
