#!/usr/bin/env python3
"""Gate driver for the large-grid deep-floor solver (matrix-free nk2g route).
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND. Category-A. Foreground/synchronous.

Diagnosis (large_grid_solver_out.json): the Jacobian BUILD (jacrev) dominates -- 37.9s/iter @
20x8x8, 132.7s/iter @ 24x10x10 -- not the lstsq.  So use the MATRIX-FREE Newton-Krylov route
(newton_krylov_2grid): never forms the fine dense Jacobian; a small coarse-grid (12x6x6) jacrev
preconditions the CG.  First grid uses the cheap dense newton_solve; larger grids warm-start
(interp_state) + nk2g.
GATE A/B: m=1 ladder 16->18->20->24 deep floor + grid-converged M_MS.
GATE C: m=2 OBLATE ground state (u_plat_m2_18x8x8.pt) up the ladder.
Writes large_grid_gates_out.json after each solve; time_budget per grid.
"""
import os, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_solver import unpack
import full3d_newton as NEW
import winding_catalog_map as WC
from cross_grid_branch import interp_state
import large_grid_solver as LGS

P, KAP8 = 0.4, 0.05
COARSE = (12, 6, 6)
TB = 1200
RESULT = {}
OUT = "/home/udt-admin/udt_mass_codex/large_grid_gates_out.json"


def rec_of(u, G, m, hist, info):
    dg, _ = WC.full_diag(u, G, P, KAP8, m)
    a, b, c, d, Th = unpack(u, G)
    return dict(grid=[G.Nr, G.Nth, G.Nps], Phi0=float(hist[0]), Phi=float(hist[-1]),
                niter=info.get('niter', len(hist) - 1), M_MS=float(dg['M_MS']),
                psivar=float(dg['psivar']), maxB1A=float((a + b)[G.body].abs().max()),
                wall=float(info.get('wall', 0.0)))


def ladder(m, grids, u0=None, key=''):
    out = []
    G = make_grid_shexact(*grids[0], mmax=grids[0][2] // 2)
    if u0 is None:
        u0, _ = WC.winding_seed(G, m)
    t0 = time.time()
    u, hist = NEW.newton_solve(u0, G, P, KAP8, m=m, maxit=60, tol=1e-13, verbose=False)
    r = rec_of(u, G, m, hist, dict(niter=len(hist) - 1, wall=time.time() - t0))
    out.append(r); print(f"[{key} {grids[0]}] M={r['M_MS']:.6f} Phi={r['Phi']:.2e} "
                         f"B1A={r['maxB1A']:.2e} ({r['wall']:.0f}s)", flush=True)
    RESULT[key] = out; json.dump(RESULT, open(OUT, "w"), indent=1)
    Gprev = G
    for g in grids[1:]:
        Gt = make_grid_shexact(*g, mmax=g[2] // 2)
        ui = interp_state(u, Gprev, Gt)
        Gc = Gprev   # GEOMETRIC 2-grid: coarse = the previous (deep-floored) ladder grid
        u, hist, info = LGS.newton_krylov_2grid(ui, Gt, Gc, P, KAP8, m=m, maxit=30,
                                                tol=1e-13, cg_iters=80, cg_tol=1e-8,
                                                verbose=True, time_budget=TB)
        r = rec_of(u, Gt, m, hist, info)
        out.append(r); print(f"[{key} {g}] M={r['M_MS']:.6f} Phi={r['Phi']:.2e} "
                             f"B1A={r['maxB1A']:.2e} nit={r['niter']} ({r['wall']:.0f}s)", flush=True)
        RESULT[key] = out; json.dump(RESULT, open(OUT, "w"), indent=1)
        Gprev = Gt
    return out


if __name__ == "__main__":
    t0 = time.time()
    print(f"=== large-grid gates (nk2g)  cuda={torch.cuda.is_available()} ===", flush=True)
    print("=== GATE A/B: m=1 ladder ===", flush=True)
    m1 = ladder(1, [(16, 8, 8), (18, 8, 8), (20, 8, 8), (24, 10, 10)], key='m1')
    deep = [(r['grid'][0], r['M_MS']) for r in m1 if r['Phi'] < 1e-9]
    Ms = [M for _, M in deep]
    if len(Ms) >= 2:
        spread = (max(Ms) - min(Ms)) / np.mean(Ms)
        print(f"[GATE B] m=1 deep-floored {[g for g,_ in deep]} masses={np.round(Ms,6)} "
              f"spread={spread*100:.2f}% Richardson={LGS.richardson(deep):.6f}", flush=True)
    else:
        print(f"[GATE B] m=1 deep-floored grids: {[g for g,_ in deep]} (need >=2 for spread)", flush=True)
    print("\n=== GATE C: m=2 OBLATE up the ladder ===", flush=True)
    G18 = make_grid_shexact(18, 8, 8, mmax=4)
    u2 = torch.load("/home/udt-admin/udt_mass_codex/u_plat_m2_18x8x8.pt", weights_only=False).to(G18.dev)
    m2 = ladder(2, [(18, 8, 8), (20, 8, 8), (24, 10, 10)], u0=u2, key='m2')
    print(f"[GATE C] m=2 masses: {[(r['grid'], round(r['M_MS'],4), '%.1e'%r['Phi']) for r in m2]}", flush=True)
    json.dump(RESULT, open(OUT, "w"), indent=1)
    print(f"\nDONE_LGGATES ({time.time()-t0:.0f}s)", flush=True)
