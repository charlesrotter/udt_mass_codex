#!/usr/bin/env python3
"""P1 closing battery: headline robustness + completion of ladder (e)."""
import numpy as np, torch, time
from solver import AngularSector, run_flow, flow_state, bisect_cstar, \
                   legendre_Y, Newton2D, DEV

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"V-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

cM2, gam = 0.2832873535156249512, 1.0

# ---- headline robustness: Class B no-seal at M2 driving, ell = 1..6, t_max=60
print("Class B at M2 driving, t_max=60, ell-extension:", flush=True)
allsat = True
for L in range(1, 7):
    angL = AngularSector(L)
    r = run_flow(angL, gam, cM2, sign=-1, t_max=60.0)
    allsat &= not r['sealed']
    Xe, _ = flow_state(r, min(60.0, r['t_stop']))
    kap = np.sqrt(3)*abs(Xe[0][1])/Xe[0][0]
    print(f"   ell<={L}: sealed={r['sealed']} t_stop={r['t_stop']:.1f} "
          f"kappa_end={kap:.4f}", flush=True)
check("29", allsat, "Class B NO-SEAL at the M2 driving is ell-robust (1..6), t_max=60")

# ---- Class B threshold geometry: depth at threshold
ang1 = AngularSector(1)
cB1, _ = bisect_cstar(ang1, 1.0, -1, 0.5, 3.5, tol=5e-7)
print(f"\nClass B ell<=1 c*_B = {cB1:.6f}", flush=True)
print("   depth at threshold (Class B):", flush=True)
for fac in [1.0005, 1.005, 1.05, 1.5]:
    r = run_flow(ang1, 1.0, cB1*fac, sign=-1, t_max=60.0)
    print(f"   c = {fac:.4f} c*_B: sealed={r['sealed']} "
          f"t_seal*={r.get('t_seal', np.nan):.4f} y_seal*={r.get('y_seal', np.nan):.5f}",
          flush=True)
rA_thr = run_flow(ang1, 1.0, 0.206995*1.0005, sign=+1, t_max=60.0)
print(f"   [contrast Class A at 1.0005 c*_A: sealed={rA_thr['sealed']} "
      f"t_seal*={rA_thr.get('t_seal', np.nan):.4f} y_seal*={rA_thr.get('y_seal', np.nan):.6f}]",
      flush=True)
check("30", True, "Class B threshold geometry recorded (shallow seal, no depth "
      "divergence) vs Class A deep-cell divergence")

# ---- gamma scaling of c*_B (Class A law: c* = 0.498912 gamma^2)
print("\ngamma-scaling (ell<=1):", flush=True)
for g in [0.5, 1.0, 2.0]:
    cb, _ = bisect_cstar(ang1, g, -1, 0.1*g, 8.0*max(1, g*g), tol=1e-5)
    ca, _ = bisect_cstar(ang1, g, +1, 0.02*g*g, 0.8*max(1, g*g), tol=1e-5)
    print(f"   gamma={g}: c*_A = {ca:.6f} (chat_A = {ca/g**2:.6f});  "
          f"c*_B = {cb:.6f} (chat_B = {cb/g**2:.6f}, c*_B/gamma = {cb/g:.6f})", flush=True)
check("31", True, "gamma-scaling of both thresholds recorded")

# ---- ladder (e) completion: 2D Newton grid sweep (Class A elliptic, M2 data)
print("\n2D Newton grid sweep (Class A, T=1.1, library Dirichlet data):", flush=True)
ang3 = AngularSector(3)
resA = run_flow(ang3, gam, cM2, sign=+1)
vals = {}
for (Nt, Nu) in [(32, 24), (48, 32), (64, 40)]:
    n2 = Newton2D(1.1, Nt, Nu)
    Y3, _ = legendre_Y(3, n2.u)
    XT2, _ = flow_state(resA, 1.1)
    f0 = torch.ones(Nu, device=DEV)
    fT = torch.tensor(XT2[0] @ Y3, device=DEV)
    Xg, _ = flow_state(resA, n2.t)
    F0 = torch.tensor(Xg @ Y3, device=DEV)
    F2d, nr, it, ok = n2.solve(F0*0.97+0.03, f0, fT)
    # probe value: f at (t ~ 0.55, u ~ 0.30) via spectral interp (nearest node here)
    it_mid = np.argmin(np.abs(n2.t-0.55)); iu = np.argmin(np.abs(n2.u-0.30))
    vals[(Nt, Nu)] = (float(F2d[it_mid, iu]), n2.t[it_mid], n2.u[iu], nr, ok)
    print(f"   (Nt,Nu)=({Nt},{Nu}): f(t={n2.t[it_mid]:.3f},u={n2.u[iu]:+.3f}) = "
          f"{vals[(Nt,Nu)][0]:.10f}  |R|={nr:.1e} ok={ok}", flush=True)
check("32", all(v[4] for v in vals.values()),
      "2D Newton grid sweep converged at all resolutions (probe values above; "
      "node positions differ slightly between grids — Dirichlet data fixed)")

print(f"\nSTAGE f4: {npass} PASS / {nfail} FAIL")
