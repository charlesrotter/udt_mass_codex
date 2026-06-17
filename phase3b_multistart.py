#!/usr/bin/env python3
"""Phase 3b+ — MULTI-START landscape survey of the m=2 winding sector at a fixed,
well-converging grid (18x8x8, Phi reaches ~1e-8).  OBSERVE, DATA-BLIND. Category-A.

Goal: using ONLY the validated newton_solve (no new tool), map the distinct local minima
of the m=2 sector by converging from many diverse seeds, and reliably identify the LOWEST
(the ground-state candidate AT THIS GRID) + how crowded the landscape is.  This characterizes
the 'many nearby minima' physics that made fresh-solve masses scatter, without needing the
cross-grid minimizer (which is the separate next build).  Foreground/synchronous; flush on.
"""
import os, sys
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import json, time
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import PI
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC

P, KAP8, M = 0.4, 0.05, 2


def shapes(G):
    r = G.Rg; sth = G.STHg; cth = torch.cos(G.THg); ps = G.PSg
    env = torch.sin(PI * (r - G.rc) / (G.ri - G.rc))
    return {
        'cos2psi': env * sth * torch.cos(2 * ps),
        'cos3psi': env * sth * torch.cos(3 * ps),
        'tetra':   env * sth * (torch.cos(2 * ps) * cth + 0.5 * torch.cos(3 * ps) * sth),
        'oblate':  env * (cth**2 - 1.0 / 3.0),
        'sin2psi': env * sth * torch.sin(2 * ps),
    }


def main():
    t0 = time.time()
    G = make_grid_shexact(18, 8, 8, mmax=4)
    u0, _ = WC.winding_seed(G, M)
    seeds = [('base', None, 0.0)]
    for nm in ('cos2psi', 'cos3psi', 'tetra', 'oblate', 'sin2psi'):
        for amp in (0.3, 0.6):
            seeds.append((nm, nm, amp))
    # converge base first to get its (a,b,c,d) for perturbation seeds
    ub, hb = NEW.newton_solve(u0, G, P, KAP8, m=M, maxit=40, tol=1e-12, verbose=False)
    a, b, c, d, Th = unpack(ub, G)
    sh = shapes(G)
    results = []
    for (label, key, amp) in seeds:
        if key is None:
            u = ub; hist = hb
        else:
            us = pack(a.clone(), b.clone(), c.clone(), d.clone(), Th + amp * sh[key])
            u, hist = NEW.newton_solve(us, G, P, KAP8, m=M, maxit=35, tol=1e-12, verbose=False)
        dg, comp = WC.full_diag(u, G, P, KAP8, M)
        a2, b2, c2, d2, _ = unpack(u, G)
        b1a = float((a2 + b2).abs()[G.body].max())
        conv = hist[-1] < 1e-6
        results.append(dict(seed=label, M_MS=dg['M_MS'], psivar=dg['psivar'], tvar=dg['tvar'],
                            Phi=hist[-1], maxB1A=b1a, converged=conv))
        print(f"[{label:12s}] M={dg['M_MS']:8.4f} psivar={dg['psivar']:.3e} tvar={dg['tvar']:.3e} "
              f"Phi={hist[-1]:.1e} B1A={b1a:.2f} {'OK' if conv else 'UNCONV'} ({time.time()-t0:.0f}s)",
              flush=True)
    conv = [r for r in results if r['converged']]
    # cluster by (M rounded to 0.5, psivar rounded to 0.05)
    clusters = {}
    for r in conv:
        kk = (round(r['M_MS'] * 2) / 2, round(r['psivar'] * 20) / 20)
        clusters.setdefault(kk, []).append(r['seed'])
    lowest = min(conv, key=lambda r: r['M_MS']) if conv else None
    print(f"\n=== {len(conv)}/{len(results)} converged; {len(clusters)} distinct minima clusters ===", flush=True)
    for kk, seeds_in in sorted(clusters.items()):
        print(f"  M~{kk[0]:.1f} psivar~{kk[1]:.2f}: {seeds_in}", flush=True)
    if lowest:
        print(f"LOWEST m=2 @18x8x8: M={lowest['M_MS']:.4f} psivar={lowest['psivar']:.3e} via '{lowest['seed']}'",
              flush=True)
    json.dump(dict(results=results, n_clusters=len(clusters),
                   clusters={f"{k[0]}_{k[1]}": v for k, v in clusters.items()},
                   lowest=lowest), open("/home/udt-admin/udt_mass_codex/phase3b_multistart_out.json", "w"), indent=1)
    print(f"DONE_MULTISTART ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
