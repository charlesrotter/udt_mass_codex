#!/usr/bin/env python3
"""Phase 3b Step 1 (LEAN) — checkpoint the winding ground states m=1,2,3.
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND. Category-A only.

Cost reality: each SH-exact dense solve at 18x8x8 is ~15 min, so minimize solves.
The m>=2 base solve on the SH-exact grid ALREADY falls to the platonic state (verified:
m=2 base -> M=13.4, psivar 0.30); we add ONE cross-check platonic seed per charge and
keep the lower-M genuinely-non-axisym state.  m=1 (round) is checkpointed as the control.
Saves u_plat_m{m}_18x8x8.pt + .json.  Verifies via independent component_residuals +
B=1/A-free witness.  Foreground/synchronous; no background jobs.
"""
import os
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

XSEED = {2: 'cos2psi', 3: 'cos3psi'}   # one natural platonic cross-check seed per charge


def platonic_shapes(G):
    r = G.Rg; sth = G.STHg; cth = torch.cos(G.THg); ps = G.PSg
    env = torch.sin(PI * (r - G.rc) / (G.ri - G.rc))
    return {'cos2psi': env * sth * torch.cos(2 * ps),
            'cos3psi': env * sth * torch.cos(3 * ps)}


def maxB1A(u, G):
    a, b, c, d, Th = unpack(u, G)
    return float((a + b).abs()[G.body].max())


def run_sector(m, Nr=18, Nth=8, Nps=8, p=0.4, kap8=0.05):
    G = make_grid_shexact(Nr, Nth, Nps, mmax=Nps // 2)
    cands = []
    u0, _ = WC.winding_seed(G, m, p=p, kap8=kap8)
    u, hist = NEW.newton_solve(u0, G, p, kap8, m=m, maxit=40, tol=1e-12, verbose=False)
    dg, comp = WC.full_diag(u, G, p, kap8, m)
    cands.append((dg['M_MS'], 'base', u, dg, comp, hist[-1]))
    print(f"[m={m}] base: M={dg['M_MS']:.5f} psivar={dg['psivar']:.3e} tvar={dg['tvar']:.3e} "
          f"Phi={hist[-1]:.2e} ({time.time()-T0:.0f}s)", flush=True)
    if m in XSEED:
        a, b, c, d, Th = unpack(u, G)
        sh = platonic_shapes(G)[XSEED[m]]
        useed = pack(a.clone(), b.clone(), c.clone(), d.clone(), Th + 0.3 * sh)
        ur, hr = NEW.newton_solve(useed, G, p, kap8, m=m, maxit=30, tol=1e-12, verbose=False)
        dgr, compr = WC.full_diag(ur, G, p, kap8, m)
        cands.append((dgr['M_MS'], XSEED[m], ur, dgr, compr, hr[-1]))
        print(f"[m={m}] {XSEED[m]}@0.3: M={dgr['M_MS']:.5f} psivar={dgr['psivar']:.3e} "
              f"Phi={hr[-1]:.2e} ({time.time()-T0:.0f}s)", flush=True)
    nonax = [c for c in cands if (m == 1 or c[3]['psivar'] > 1e-3)]
    pool = nonax if nonax else cands
    M, label, u, dg, comp, Phi = min(pool, key=lambda x: x[0])
    b1a = maxB1A(u, G)
    indep = {k: float(v) for k, v in NEW.component_residuals(u, G, p, kap8, m).items()}
    tile = dict(m=m, grid=[Nr, Nth, Nps], M_MS=M, psivar=dg['psivar'], tvar=dg['tvar'],
                Phi=Phi, comp_fulldiag={k: float(v) for k, v in comp.items()},
                comp_independent=indep, maxB1A=b1a, winning=label)
    ckpt = f"/home/udt-admin/udt_mass_codex/u_plat_m{m}_{Nr}x{Nth}x{Nps}.pt"
    torch.save(u.detach().cpu(), ckpt)
    json.dump(tile, open(ckpt.replace('.pt', '.json'), 'w'), indent=1)
    print(f"[m={m}] WINNER={label} M={M:.5f} psivar={dg['psivar']:.3e} maxB1A={b1a:.3e}", flush=True)
    print(f"[m={m}] indep comp: {indep}", flush=True)
    return tile


if __name__ == "__main__":
    T0 = time.time()
    out = [run_sector(m) for m in (1, 2, 3)]
    json.dump(out, open("/home/udt-admin/udt_mass_codex/phase3b_step1_out.json", "w"), indent=1)
    print(f"DONE_STEP1 ({time.time()-T0:.0f}s)", flush=True)
