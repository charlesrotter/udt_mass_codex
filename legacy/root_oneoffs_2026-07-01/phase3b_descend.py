#!/usr/bin/env python3
"""Phase 3b Step 5b — DECISIVE coupled stability test (constraint-respecting).
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND.

The fixed-metric matter Hessian gave n_neg=19 (m=2), 44 (m=3), 0 (m=1).  But perturbing
Theta at FIXED metric moves OFF the Einstein constraint surface, so those negatives may be
unphysical off-constraint directions.  Decisive test: perturb Theta along the most-negative
fixed-metric eigenvectors, then FULL COUPLED re-solve (re-imposes Einstein + matter EL).
 - lands at LOWER M  => genuine instability (the checkpoint is a saddle; we descend).
 - returns to base M => the mode was off-constraint; the state is coupled-stable along it.
Foreground/synchronous.  Usage: python3 phase3b_descend.py <m>   (default m=2)
"""
import os, sys
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import json
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import build_metric
from full3d_solver import pack, unpack
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import full3d_newton as NEW
import winding_catalog_map as WC
from phase3b_hessian import S_of_Th


def neg_eigvecs(G, u, m, k=3):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d).detach(); ginv = CORE.metric_inverse(g).detach()
    Th0 = Th.detach().clone().requires_grad_(True)
    H_S = torch.autograd.functional.hessian(lambda x: S_of_Th(G, g, ginv, x, m), Th0)
    n = G.Nr * G.Nth * G.Nps
    H_E = -0.5 * (H_S.reshape(n, n) + H_S.reshape(n, n).t())
    body = torch.zeros(G.Nr, G.Nth, G.Nps, dtype=torch.bool, device=H_E.device)
    body[1:-1, :, :] = True
    bidx = body.reshape(-1).nonzero().squeeze(1)
    evals, evecs = torch.linalg.eigh(H_E[bidx][:, bidx])
    out = []
    for j in range(k):
        if evals[j] >= 0:
            break
        v = torch.zeros(n, device=H_E.device)
        v[bidx] = evecs[:, j]
        out.append((float(evals[j]), v.reshape(G.Nr, G.Nth, G.Nps)))
    return out


def main(m):
    p, kap8 = 0.4, 0.05
    path = f"/home/udt-admin/udt_mass_codex/u_plat_m{m}_18x8x8.pt"
    tile = json.load(open(path.replace('.pt', '.json')))
    G = make_grid_shexact(18, 8, 8, mmax=4)
    u = torch.load(path).to(G.dev)
    a, b, c, d, Th = unpack(u, G)
    dg0, _ = WC.full_diag(u, G, p, kap8, m)
    Mbase = dg0['M_MS']
    print(f"[m={m}] BASE M={Mbase:.5f} psivar={dg0['psivar']:.3e}", flush=True)
    vecs = neg_eigvecs(G, u, m, k=2)
    print(f"[m={m}] top negative fixed-metric eigenvalues: {[round(e,2) for e,_ in vecs]}", flush=True)
    results = []
    best = (Mbase, None)
    for j, (ev, vfield) in enumerate(vecs):
        sc = float(vfield.abs().max()) + 1e-30
        for amp in (0.25, -0.25):
            Th2 = Th + (amp / sc) * vfield     # normalize so perturbation peak = amp
            useed = pack(a.clone(), b.clone(), c.clone(), d.clone(), Th2)
            ur, hr = NEW.newton_solve(useed, G, p, kap8, m=m, maxit=30, tol=1e-12, verbose=False)
            dgr, _ = WC.full_diag(ur, G, p, kap8, m)
            dM = dgr['M_MS'] - Mbase
            tag = "LOWER" if dM < -1e-3 else ("~same" if abs(dM) < 1e-3 else "higher")
            print(f"[m={m}] evec{j}(ev={ev:.1f}) amp={amp:+.2f}: M={dgr['M_MS']:.5f} "
                  f"dM={dM:+.4e} psivar={dgr['psivar']:.3e} Phi={hr[-1]:.1e} {tag}", flush=True)
            results.append(dict(evec=j, ev=ev, amp=amp, M=dgr['M_MS'], dM=dM,
                                psivar=dgr['psivar'], Phi=hr[-1]))
            if dgr['M_MS'] < best[0] - 1e-3:
                best = (dgr['M_MS'], ur.detach().cpu())
    verdict = ("SADDLE (coupled descent found lower state)" if best[1] is not None
               else "STABLE along tested modes (negatives were off-constraint)")
    print(f"[m={m}] VERDICT: {verdict}  best M={best[0]:.5f} (base {Mbase:.5f})", flush=True)
    if best[1] is not None:
        torch.save(best[1], f"/home/udt-admin/udt_mass_codex/u_descended_m{m}_18x8x8.pt")
    json.dump(dict(m=m, Mbase=Mbase, results=results, best_M=best[0], verdict=verdict),
              open(f"/home/udt-admin/udt_mass_codex/phase3b_descend_m{m}_out.json", "w"), indent=1)
    print(f"DONE_DESCEND_m{m}", flush=True)


if __name__ == "__main__":
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    main(m)
