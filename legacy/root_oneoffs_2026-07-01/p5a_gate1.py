#!/usr/bin/env python3
"""P5a GATE 1: anchor reproduction + PC-independence.  NEW FILE, branch p5a-jfnk-precond.
On the small (16,6,8) round-seed case the dense anchor can also solve:
  - JFNK (physics PC) must converge to the SAME fixed point as the anchor (field-by-field).
  - The converged solution must be PRECONDITIONER-INDEPENDENT (>=2 PC variants -> same).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import time, numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import round_seed, residual_vector, unpack
import full3d_newton as NW
import p5a_jfnk_precond as P5

G = Grid3D(16, 6, 8, rc=0.05, cell=14.0); G = attach_coord_weight(G)
u0, sol = round_seed(G, p=0.4, kap8=0.05)
Phi0 = float((residual_vector(u0, G, 0.4, 0.05) ** 2).sum())
print(f"seed Phi={Phi0:.3e}  nU={u0.numel()}")

# ANCHOR (dense Newton)
RUN_ANCHOR = os.environ.get("RUN_ANCHOR", "1") == "1"
if RUN_ANCHOR:
    t = time.time()
    uA, hA = NW.newton_solve(u0, G, 0.4, 0.05, maxit=25, tol=1e-12)
    tA = time.time() - t
    print(f"ANCHOR: Phi={hA[-1]:.3e} iters={len(hA)-1} time={tA:.0f}s", flush=True)
    torch.save(uA, "/tmp/p5a_anchor_16x6x8.pt")
else:
    uA = torch.load("/tmp/p5a_anchor_16x6x8.pt")
    print("ANCHOR: loaded cached uA", flush=True)

results = {}
for variant in ['radial', 'radial+col']:
    t = time.time()
    u, h, cg, dt = P5.jfnk_solve(u0, G, 0.4, 0.05, maxit=30, lam0=1e-3, tol=1e-10,
                                 variant=variant, cg_maxit=300, cg_tol=1e-7, verbose=True)
    print(f"JFNK[{variant}]: Phi={h[-1]:.3e} iters={len(h)-1} cg_avg={np.mean(cg) if cg else 0:.0f} time={dt:.0f}s")
    results[variant] = u

# field-by-field anchor match
names = ['a', 'b', 'c', 'd', 'Theta']
for variant, u in results.items():
    fA = unpack(uA, G); fJ = unpack(u, G)
    diffs = [float((fJ[i] - fA[i]).abs().max()) for i in range(5)]
    print(f"  [{variant}] vs ANCHOR field-by-field max|diff|: " +
          " ".join(f"{n}={d:.2e}" for n, d in zip(names, diffs)))

# PC-independence: radial vs radial+col
fr = unpack(results['radial'], G); fc = unpack(results['radial+col'], G)
pcdiff = [float((fr[i] - fc[i]).abs().max()) for i in range(5)]
print("  PC-INDEPENDENCE radial vs radial+col max|diff|: " +
      " ".join(f"{n}={d:.2e}" for n, d in zip(names, pcdiff)))
