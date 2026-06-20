#!/usr/bin/env python3
"""
p5b_gridscan.py -- P5b GATE 3: grid-converged M_MS across >=3 grids via the PC'd
re-posed JFNK, + scalability numbers (JFNK Newton-step cost vs dense jacrev BUILD).

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.  Branch p5b-pc-floor.

For each grid: floor the round seed with the PC'd JFNK (gauge G1 = round-seed edges),
report committed-Phi + M_MS + tvar, and a timing comparison:
  - one JFNK Newton step wall-time (Krylov-iters x JVP, matrix-free)  [via p5b_pc]
  - one dense reposed jacrev Jacobian BUILD wall-time                  [the dense cost]
The scalability claim: JFNK step stays ~flat while the dense build grows with grid.
"""
import os, sys, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")  # for the dense jacrev timing
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack
import p5a_prime_repose as RP
import p5b_pc as PC

P, KAP8 = 0.4, 0.05


def one_grid(NR, NTH, NPS, pc='rband'):
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(u0)
    ub0 = rp.extract(u0)
    ub, hist, its, wt = PC.jfnk_solve(ub0, rp, u0, KAP8, pc=pc, maxit=100,
                                      tol=1e-13, lsmr_maxit=4000, lsmr_tol=1e-13,
                                      verbose=False)
    u = rp.embed_vsafe(ub)
    F = residual_vector(u, G, P, KAP8); Phi = float((F*F).sum())
    out = residuals(G, unpack(u, G), P, KAP8); d = diagnostics(G, out, KAP8)
    newton_its = len(hist)-1
    jfnk_step = wt/max(newton_its, 1)
    # dense reposed jacrev BUILD cost (one build) -- the cost JFNK avoids
    t = time.time(); _ = RP.reposed_jacobian_jacrev(ub0, rp, KAP8); db = time.time()-t
    return dict(NR=NR, nB=rp.nB, Phi=Phi, M_MS=d['M_MS'], tvar=d['tvar'],
                newton_its=newton_its, lsmr_tot=int(np.sum(its)), wall=wt,
                jfnk_step=jfnk_step, dense_build=db)


if __name__ == "__main__":
    pc = sys.argv[1] if len(sys.argv) > 1 else 'rband'
    # >=3 grids: refine Nr (the convergent direction); Nth/Nps fixed adequate
    grids = [(16, 8, 8), (24, 8, 8), (32, 8, 8)]
    print(f"=== P5b GRID SCAN (pc={pc}) ===", flush=True)
    res = []
    for (NR, NTH, NPS) in grids:
        r = one_grid(NR, NTH, NPS, pc=pc)
        print(f"  Nr={r['NR']:<3} nB={r['nB']:<6} Phi={r['Phi']:.2e} M_MS={r['M_MS']:.6f} "
              f"tvar={r['tvar']:.4e} | newton={r['newton_its']} lsmr-tot={r['lsmr_tot']} "
              f"wall={r['wall']:.0f}s jfnk-step={r['jfnk_step']:.1f}s dense-build={r['dense_build']:.1f}s",
              flush=True)
        res.append(r)
    print("\n=== M_MS GRID CONVERGENCE ===", flush=True)
    for i in range(1, len(res)):
        print(f"  Nr {res[i-1]['NR']}->{res[i]['NR']}: dM_MS={abs(res[i]['M_MS']-res[i-1]['M_MS']):.3e}",
              flush=True)
    print("\n=== SCALABILITY (jfnk-step vs dense-build) ===", flush=True)
    for r in res:
        print(f"  Nr={r['NR']}: jfnk-step={r['jfnk_step']:.1f}s  dense-build={r['dense_build']:.1f}s  "
              f"ratio(build/step)={r['dense_build']/max(r['jfnk_step'],1e-9):.2f}", flush=True)
    print("\n=== GRID SCAN DONE ===", flush=True)
