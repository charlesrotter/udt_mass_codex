#!/usr/bin/env python3
"""
test_shexact_cheap.py -- the FAST (no-Newton) gates for the SH-exact-theta grid:
  G0  operator m=0 equality + psi engagement
  G1s node-grid byte-identity + ROUND-SEED residual equality (Legendre vs SH-exact)
  G2a full-residual ENGAGEMENT on a psi-dependent state
These are all single residual evaluations -- cheap on CPU.  The two Newton-solve gates
(G1 converged, G2b runs) live in test_shexact_solve.py (run briefly on GPU).
Driver: Claude (Opus 4.8, 1M).  2026-06-16.  NEW file.  DATA-BLIND.
"""
import os, sys
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, diagnostics, residuals, PI, T, R, TH, PS
import full3d_solver as FS
from full3d_solver import pack, unpack, residual_vector
import full3d_newton as FN
from full3d_grid_shexact import make_grid_shexact, legendre_d_th

P, KAP8 = 0.4, 0.05
NR, NTH, NPS = 20, 6, 8
def pr(*a): print(*a); sys.stdout.flush()

def main():
    Gleg = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); Gleg = attach_coord_weight(Gleg)
    Gsh = make_grid_shexact(NR, NTH, NPS, rc=0.05, cell=14.0, mmax=NPS // 2)

    pr("\n=== G0: operator m=0 equality + psi engagement ===")
    mu = torch.cos(Gsh.THg)
    f0 = (0.5*(5*mu**3 - 3*mu)) * torch.exp(-Gsh.Rg)
    eq = float((Gsh.d_th(f0) - legendre_d_th(Gsh, f0)).abs().max())
    f1 = f0 + torch.sin(Gsh.THg)*torch.cos(2*Gsh.PSg)*torch.exp(-Gsh.Rg)
    eng = float((Gsh.d_th(f1) - legendre_d_th(Gsh, f1)).abs().max())
    pr(f"  m=0 equality   = {eq:.3e}  (PASS<1e-11)")
    pr(f"  psi engagement = {eng:.3e}  (PASS>1e-3)")
    g0 = (eq < 1e-11) and (eng > 1e-3)

    pr("\n=== G1s: node identity + round-seed residual equality ===")
    node_ok = True
    for nm in ('th','sth','wmu','wr','wps'):
        dd = float((getattr(Gleg,nm)-getattr(Gsh,nm)).abs().max()); node_ok &= (dd==0.0)
        pr(f"  node {nm:>4}: max|diff|={dd:.3e}")
    dwv = float((Gleg.wvol_coord-Gsh.wvol_coord).abs().max()); node_ok &= (dwv==0.0)
    pr(f"  node wvol_coord: max|diff|={dwv:.3e}")
    u0L, solL = FS.round_seed(Gleg, p=P, kap8=KAP8)
    u0S, solS = FS.round_seed(Gsh, p=P, kap8=KAP8)
    FL = residual_vector(u0L, Gleg, P, KAP8); FSr = residual_vector(u0S, Gsh, P, KAP8)
    PhiL = float((FL*FL).sum()); PhiS = float((FSr*FSr).sum())
    seed_diff = float((FL-FSr).abs().max())
    pr(f"  round-seed Phi: Legendre={PhiL:.6e}  SHexact={PhiS:.6e}")
    pr(f"  round-seed ||F_Leg - F_SH||_inf = {seed_diff:.3e}  (PASS<1e-12)")
    # M_MS on the round seed (cheap diagnostics, no solve)
    outL = residuals(Gleg, unpack(u0L,Gleg), P, KAP8, m=1)
    outS = residuals(Gsh, unpack(u0S,Gsh), P, KAP8, m=1)
    mL = diagnostics(Gleg, outL, KAP8)['M_MS']; mS = diagnostics(Gsh, outS, KAP8)['M_MS']
    pr(f"  round-seed M_MS: Legendre={mL:.6f}  SHexact={mS:.6f}  |diff|={abs(mL-mS):.3e}  "
       f"(#56 radial M_MS={solL['M_MS']:.5f})")
    g1s = node_ok and (seed_diff < 1e-12) and (abs(mL-mS) < 1e-12)

    pr("\n=== G2a: full-residual ENGAGEMENT on psi-dependent state (m=3, cos(3 psi)) ===")
    a,b,c,d,Th = unpack(u0L, Gleg)
    taper = torch.exp(-((Gleg.Rg-3.0)/2.0)**2)
    Th_d = Th + 0.15*torch.sin(Gleg.THg)*torch.cos(3*Gleg.PSg)*taper
    u_d = pack(a,b,c,d,Th_d)
    F_leg = residual_vector(u_d, Gleg, P, KAP8)
    F_sh  = residual_vector(u_d, Gsh,  P, KAP8)
    diff = float((F_leg-F_sh).abs().max())
    pr(f"  ||F_Legendre - F_SHexact||_inf = {diff:.3e} (rel "
       f"{diff/float(F_leg.abs().max()):.3e})  (PASS>1e-6 => engaged)")
    g2a = diff > 1e-6

    pr("\n--- CHEAP GATES ---")
    pr(f"  G0  operator     : {'PASS' if g0 else 'FAIL'}")
    pr(f"  G1s seed/nodes   : {'PASS' if g1s else 'FAIL'}")
    pr(f"  G2a engagement   : {'PASS' if g2a else 'FAIL'}")

if __name__ == "__main__":
    main()
