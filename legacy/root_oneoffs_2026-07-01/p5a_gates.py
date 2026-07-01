#!/usr/bin/env python3
"""P5a GATES 1+2 consolidated.  NEW FILE, branch p5a-jfnk-precond.  DATA-BLIND.
Runs on the small (16,6,8) round + axi_l2 cases the dense anchor can also solve, so
JFNK is compared apples-to-apples against the anchor (uses /tmp/p5a_anchor_16x6x8.pt
if present, else solves it).
"""
import os, sys
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import time, math, numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import round_seed, residual_vector, unpack
import full3d_newton as NW
import p5a_jfnk_precond as P5

G = Grid3D(16, 6, 8, rc=0.05, cell=14.0); G = attach_coord_weight(G)
u0, sol = round_seed(G, p=0.4, kap8=0.05)


def Phi(u):
    return float((residual_vector(u, G, 0.4, 0.05) ** 2).sum())


def shape(u):
    a, b, c, d, Th = unpack(u, G)
    out = residuals(G, (a, b, c, d, Th), 0.4, 0.05)
    dg = diagnostics(G, out, 0.05)
    return dg['tvar'], dg['psivar'], dg['M_MS']


# ----- ANCHOR on round (cached) -----
if os.path.exists("/tmp/p5a_anchor_16x6x8.pt"):
    uA = torch.load("/tmp/p5a_anchor_16x6x8.pt")
    print(f"ANCHOR round (cached): Phi={Phi(uA):.3e}", flush=True)
else:
    uA, hA = NW.newton_solve(u0, G, 0.4, 0.05, maxit=25, tol=1e-12)
    torch.save(uA, "/tmp/p5a_anchor_16x6x8.pt")
    print(f"ANCHOR round: Phi={hA[-1]:.3e} iters={len(hA)-1}", flush=True)

print("\n===== GATE 1: round-seed anchor match + PC-independence =====", flush=True)
res = {}
for pc in ['none', 'fieldblock']:
    u, h, it, dt = P5.jfnk_lsmr_solve(u0, G, 0.4, 0.05, maxit=18, lam0=1e-3, tol=1e-11,
                                      pc=pc, lsmr_maxit=600, lsmr_tol=1e-11, verbose=False)
    res[pc] = u
    print(f"  JFNK-LSMR[{pc}]: Phi={h[-1]:.3e} iters={len(h)-1} time={dt:.0f}s", flush=True)
names = ['a', 'b', 'c', 'd', 'Th']
for pc, u in res.items():
    fA = unpack(uA, G); fJ = unpack(u, G)
    d = [float((fJ[i] - fA[i]).abs().max()) for i in range(5)]
    print(f"  [{pc}] vs ANCHOR max|diff|: " + " ".join(f"{n}={x:.2e}" for n, x in zip(names, d)), flush=True)
fa = unpack(res['none'], G); fb = unpack(res['fieldblock'], G)
d = [float((fa[i] - fb[i]).abs().max()) for i in range(5)]
print("  PC-INDEPENDENCE none vs fieldblock max|diff|: " + " ".join(f"{n}={x:.2e}" for n, x in zip(names, d)), flush=True)

print("\n===== GATE 2: the #60 axisym-l2 stall case =====", flush=True)
useed = P5.axi_l2_seed(G, u0, amp=0.25)
tv, pv, M = shape(useed); print(f"  axi_l2 SEED: Phi={Phi(useed):.3e} tvar={tv:.3e} psivar={pv:.3e}", flush=True)

# anchor on the stall case (the relax-to-round target)
t = time.time(); uAx, hAx = NW.newton_solve(useed, G, 0.4, 0.05, maxit=25, tol=1e-12)
tv, pv, M = shape(uAx)
print(f"  ANCHOR axi_l2: Phi={hAx[-1]:.3e} tvar={tv:.3e} psivar={pv:.3e} iters={len(hAx)-1} time={time.time()-t:.0f}s", flush=True)

# #60 control: Jacobi-PCG (the documented stall solver), via the CG jfnk
t = time.time(); uj, hj, cgj, dtj = P5.jfnk_solve(useed, G, 0.4, 0.05, maxit=30, lam0=1e-2,
                                                  tol=1e-10, variant='jacobi', cg_maxit=120, cg_tol=1e-6)
tv, pv, M = shape(uj)
print(f"  #60 JACOBI-PCG: Phi={hj[-1]:.3e} tvar={tv:.3e} psivar={pv:.3e} iters={len(hj)-1} time={dtj:.0f}s", flush=True)
print("    Phi hist:", " ".join(f"{x:.1e}" for x in hj), flush=True)

# JFNK-LSMR (physics-PC line)
t = time.time(); ur, hr, itr, dtr = P5.jfnk_lsmr_solve(useed, G, 0.4, 0.05, maxit=24, lam0=1e-2,
                                                       tol=1e-10, pc='none', lsmr_maxit=600, lsmr_tol=1e-11)
tv, pv, M = shape(ur)
print(f"  JFNK-LSMR: Phi={hr[-1]:.3e} tvar={tv:.3e} psivar={pv:.3e} iters={len(hr)-1} time={dtr:.0f}s", flush=True)
print("    Phi hist:", " ".join(f"{x:.1e}" for x in hr), flush=True)
