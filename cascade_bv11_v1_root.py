"""bv11 V1 part 2: Illinois root-polish of the N=0 bracket + full identity suite.
Budget: <=10 Illinois shots + 1 final dense re-shoot."""
import json
import numpy as np
import bv11_lib as L

# bracket from bv11_scan.json (endpoint values reused -- no re-evaluation)
lo, flo = 0.006627732752467227, 0.429691661942872
hi, fhi = 0.0066940100799919, -0.5522772903946928

a_side, b_side, fa, fb = lo, hi, flo, fhi
for it in range(10):
    m = a_side - fa * (b_side - a_side) / (fb - fa)   # regula falsi point
    if not (min(a_side, b_side) < m < max(a_side, b_side)):
        m = 0.5 * (a_side + b_side)
    fm, _ = L.miss_dp(m)
    print(f"it={it} d'={m:.15f} miss={fm:+.6e} width={abs(b_side-a_side):.3e}", flush=True)
    if not np.isfinite(fm):
        raise SystemExit("non-seal inside bracket -- refutation signal")
    if fa * fm < 0:
        b_side, fb = m, fm
        fa *= 0.5                      # Illinois modification
    else:
        a_side, fa = m, fm
        fb *= 0.5
    if abs(b_side - a_side) < 1e-12 or fm == 0.0:
        break
    # restore true endpoint values for the secant when a NEW point replaced the same side twice
dstar = m
astar = 1.5 * (1.0 + dstar)
print(f"\nroot: d'* = {dstar:.12f}   a* = {astar:.12f}   bracket width {abs(b_side-a_side):.2e}")

# final dense re-shoot at the root: identity suite at 100k and 200k samples
f, o = L.miss_dp(dstar, keep=True)
print(f"final miss(rho'_s) = {f:+.3e}")
d100 = L.characterize(o, npts=100001)
d200 = L.characterize(o, npts=200001)
print("\nIDENTITY SUITE @100k:")
for k, v in d100.items():
    print(f"  {k:20s} = {v}")
print("IDENTITY SUITE @200k (twin counts + monotonicity):")
for k in ("N_delta", "N_rhop", "rho_monotone_dec", "n_rho_increase", "H_drift"):
    print(f"  {k:20s} = {d200[k]}")

# save trajectory samples for the V3 cap/approach checks (no extra shot)
rr = np.linspace(0.0, o["r_s"], 200001)
tr = L.eval_traj(o["sols"], rr)
np.savez("bv11_fundamental_traj.npz", rr=rr, phi=tr[0], phip=tr[1], rho=tr[2],
         rhop=tr[3], dstar=dstar, astar=astar)
json.dump({"dstar": dstar, "astar": astar, "suite100k": d100,
           "suite200k": {k: d200[k] for k in d200 if k not in ()},
           "shots": L.SHOTS["n"]}, open("bv11_root.json", "w"), indent=1, default=str)
print("shots this script:", L.SHOTS["n"])
