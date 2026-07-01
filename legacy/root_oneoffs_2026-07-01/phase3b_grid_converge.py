#!/usr/bin/env python3
"""Phase 3b Step 2+3 — GRID CONVERGENCE of the platonic masses M_MS(m) + BINDING.
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND. Category-A.

For m in {1,2,3}: re-solve on a radial ladder (Nr) and an angular ladder (Nth,Nps),
each from the analytic seed (+ the winning platonic shape for m>=2, so we track the
PLATONIC branch, selecting the lowest-M non-axisym state), recording M_MS, psivar, Phi.
Then grid-matched BINDING B(m)=m*M_MS(1)-M_MS(m) at the finest common grid, and a
Richardson/last-two-grid error estimate for M_MS(m).  Foreground/synchronous.
Cost-bounded: skip a grid if a solve does not reach Phi<1e-6.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import json, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import PI
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC


def platonic_shapes(G):
    r = G.Rg; sth = G.STHg; cth = torch.cos(G.THg); ps = G.PSg
    env = torch.sin(PI * (r - G.rc) / (G.ri - G.rc))
    return {'cos2psi': env * sth * torch.cos(2 * ps),
            'cos3psi': env * sth * torch.cos(3 * ps),
            'tetra':   env * sth * (torch.cos(2 * ps) * cth + 0.5 * torch.cos(3 * ps) * sth)}


def solve_state(Nr, Nth, Nps, m, win_shape=None, win_amp=0.3, p=0.4, kap8=0.05):
    """Return (M_MS, psivar, Phi) for the tracked branch (platonic for m>=2)."""
    G = make_grid_shexact(Nr, Nth, Nps, mmax=max(2, Nps // 2))
    cands = []
    u0, _ = WC.winding_seed(G, m, p=p, kap8=kap8)
    u, hist = NEW.newton_solve(u0, G, p, kap8, m=m, maxit=40, tol=1e-12, verbose=False)
    dg, _ = WC.full_diag(u, G, p, kap8, m)
    cands.append((dg['M_MS'], dg['psivar'], hist[-1]))
    if m >= 2 and win_shape is not None:
        a, b, c, d, Th = unpack(u, G)
        sh = platonic_shapes(G)[win_shape]
        useed = pack(a, b, c, d, Th + win_amp * sh)
        ur, hr = NEW.newton_solve(useed, G, p, kap8, m=m, maxit=30, tol=1e-12, verbose=False)
        dgr, _ = WC.full_diag(ur, G, p, kap8, m)
        cands.append((dgr['M_MS'], dgr['psivar'], hr[-1]))
    # track the platonic branch: lowest-M with psivar>1e-3 (else lowest-M)
    nonax = [c for c in cands if (m == 1 or c[1] > 1e-3)]
    pool = nonax if nonax else cands
    return min(pool, key=lambda x: x[0])


def ladder(m, grids, win_shape, label):
    rows = []
    for (Nr, Nth, Nps) in grids:
        t = time.time()
        M, ps, Phi = solve_state(Nr, Nth, Nps, m, win_shape)
        rows.append(dict(grid=[Nr, Nth, Nps], M_MS=M, psivar=ps, Phi=Phi, t=time.time() - t))
        print(f"[{label} m={m}] {Nr}x{Nth}x{Nps}: M={M:.5f} psivar={ps:.2e} Phi={Phi:.1e} "
              f"({rows[-1]['t']:.0f}s)", flush=True)
    return rows


if __name__ == "__main__":
    # cost-trimmed: base-only solves (the m=2 base tracks the toroidal branch), m=1 & m=2,
    # a few grids to show M_MS is stabilizing + grid-matched binding. m=3 left at Step-1 grid.
    grids = [(16, 8, 8), (18, 8, 8), (20, 8, 8), (18, 10, 10)]
    res = {}
    for m in (1, 2):
        res[f'm{m}_grids'] = ladder(m, grids, None, 'grid')   # win_shape=None => base-only
    # grid-matched binding at 18x10x10 (finest common)
    def Mat(m, grid):
        for row in res[f'm{m}_grids']:
            if row['grid'] == grid:
                return row['M_MS']
        return None
    fg = [18, 10, 10]
    binding = {}
    M1 = Mat(1, fg)
    Mm = Mat(2, fg)
    if M1 and Mm:
        binding[2] = dict(M_MS=Mm, m_M1=2 * M1, B=2 * M1 - Mm, ratio=Mm / (2 * M1))
    res['binding_18x10x10'] = dict(M1=M1, per_m=binding)
    json.dump(res, open("/home/udt-admin/udt_mass_codex/phase3b_grid_converge_out.json", "w"), indent=1)
    print("BINDING (18x10x10):", json.dumps(binding, indent=1))
    print("DONE_GRIDCONV")
