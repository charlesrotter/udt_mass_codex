#!/usr/bin/env python3
"""Phase 3b+ — grid-converged masses via DEEP-FLOORED warm-start continuation + Richardson.
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND. Category-A. Foreground/synchronous.

The matrix-free large-grid route stalled; the DENSE newton_solve works at 16/18/20x8x8 (jacrev
build ~5-38s/iter). The earlier continuation 'drift' was UNDER-CONVERGENCE (maxit=20). Here we
DEEP-FLOOR each grid (tol 1e-11) and warm-start the next via interp_state -> tracks ONE basin to
a true minimum at each grid -> Richardson-extrapolate to the continuum.
m=1: round (winding_seed). m=2: OBLATE global-min basin (winding_seed + oblate_P2 shape).
Writes phase3b_richardson_out.json after each solve.
"""
import os, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC
from cross_grid_branch import interp_state

P, KAP8 = 0.4, 0.05
GRIDS = [(16, 8, 8), (18, 8, 8), (20, 8, 8)]
RESULT = {}
OUT = "/home/udt-admin/udt_mass_codex/phase3b_richardson_out.json"


def richardson_1overN(pairs):
    """continuum estimate assuming M(N) = Minf + c/N^2 from the two finest deep grids."""
    if len(pairs) < 2:
        return float('nan')
    (n1, M1), (n2, M2) = pairs[-2], pairs[-1]
    h1, h2 = 1.0 / n1**2, 1.0 / n2**2
    return float((M2 * h1 - M1 * h2) / (h1 - h2))


def track(m, oblate, key):
    out = []
    G = make_grid_shexact(*GRIDS[0], mmax=GRIDS[0][2] // 2)
    u0, _ = WC.winding_seed(G, m)
    if oblate:
        a, b, c, d, Th = unpack(u0, G)
        sh = WC.mode_shapes(G)['oblate_P2']
        u0 = pack(a, b, c, d, Th + 0.5 * sh)
    Gprev = None
    for g in GRIDS:
        Gt = make_grid_shexact(*g, mmax=g[2] // 2)
        ui = u0 if Gprev is None else interp_state(u, Gprev, Gt)
        t0 = time.time()
        u, hist = NEW.newton_solve(ui, Gt, P, KAP8, m=m, maxit=70, tol=1e-11, verbose=False)
        dg, _ = WC.full_diag(u, Gt, P, KAP8, m)
        a, b, c, d, Th = unpack(u, Gt)
        r = dict(grid=list(g), M_MS=float(dg['M_MS']), psivar=float(dg['psivar']),
                 Phi=float(hist[-1]), maxB1A=float((a + b)[Gt.body].abs().max()),
                 wall=time.time() - t0)
        out.append(r)
        print(f"[{key} {g}] M={r['M_MS']:.6f} psivar={r['psivar']:.3e} Phi={r['Phi']:.2e} "
              f"B1A={r['maxB1A']:.2e} ({r['wall']:.0f}s)", flush=True)
        RESULT[key] = out; json.dump(RESULT, open(OUT, "w"), indent=1)
        Gprev = Gt
    deep = [(r['grid'][0], r['M_MS']) for r in out if r['Phi'] < 1e-9]
    Minf = richardson_1overN(deep)
    Ms = [M for _, M in deep]
    spread = (max(Ms) - min(Ms)) / np.mean(Ms) if len(Ms) >= 2 else float('nan')
    print(f"[{key}] deep-floored {[n for n,_ in deep]} masses={np.round(Ms,6)} "
          f"spread={spread*100:.2f}% Richardson(1/N^2)={Minf:.6f}", flush=True)
    RESULT[key + '_summary'] = dict(deep=deep, spread=float(spread), Minf=float(Minf))
    json.dump(RESULT, open(OUT, "w"), indent=1)
    return out


if __name__ == "__main__":
    t0 = time.time()
    print("=== m=1 round (deep-floored continuation) ===", flush=True)
    track(1, oblate=False, key='m1')
    print("\n=== m=2 oblate global-min (deep-floored continuation) ===", flush=True)
    track(2, oblate=True, key='m2')
    print(f"\nDONE_RICHARDSON ({time.time()-t0:.0f}s)", flush=True)
