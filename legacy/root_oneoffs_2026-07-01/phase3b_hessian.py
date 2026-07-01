#!/usr/bin/env python3
"""Phase 3b Step 5a — FULL-NODAL matter-sector Hessian at the platonic ground states.
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND.

The committed verify_winding_hessian probe restricted to the psi-breaking subspace; the
m=3 axisym JSON showed full_min(-186) << break_min5(-151), i.e. a strong negative mode
with NON-psi-breaking content the projection HID.  So here we Hessian the matter action
over the FULL body-Theta space at the PLATONIC checkpoint (u_plat) and count genuinely
negative modes.  A genuine minimum => n_neg = 0 up to near-zero modes (rotational/winding
zero modes of the platonic shape).  m=1 hedgehog = sign calibration (must be n_neg=0).
Energy Hessian H_E = -H_S (S = matter action).  Runs foreground.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import json, glob
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import build_metric, field_dn
from full3d_solver import unpack
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import full3d_newton as NEW
import winding_catalog_map as WC


def S_of_Th(G, g, ginv, Th, m):
    dn = field_dn(G, Th, m=m)
    Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    return (sqrtg * L * G.wvol_coord).sum()


def full_body_hessian(G, u, m):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d).detach()
    ginv = CORE.metric_inverse(g).detach()
    Th0 = Th.detach().clone().requires_grad_(True)
    f = lambda x: S_of_Th(G, g, ginv, x, m)
    H_S = torch.autograd.functional.hessian(f, Th0).reshape(G.Nr * G.Nth * G.Nps, -1)
    H_E = -0.5 * (H_S + H_S.t())                       # energy Hessian, symmetrized
    body = torch.zeros(G.Nr, G.Nth, G.Nps, dtype=torch.bool, device=H_E.device)
    body[1:-1, :, :] = True
    bidx = body.reshape(-1).nonzero().squeeze(1)
    HB = H_E[bidx][:, bidx]
    ev = torch.linalg.eigvalsh(HB).cpu().numpy()
    return np.sort(ev)


def run(label, G, u, m, tol_frac=1e-6):
    ev = full_body_hessian(G, u, m)
    scale = max(abs(ev).max(), 1e-30)
    tol = tol_frac * scale
    n_neg = int((ev < -tol).sum())
    n_zero = int((np.abs(ev) <= tol).sum())
    print(f"[{label} m={m}] lowest8={np.round(ev[:8],3)}  n_neg(<-{tol:.2e})={n_neg}  "
          f"n_zero={n_zero}  scale={scale:.2e}")
    return dict(label=label, m=m, lowest8=[float(x) for x in ev[:8]],
                n_neg=n_neg, n_zero=n_zero, scale=float(scale), tol=float(tol))


if __name__ == "__main__":
    out = []
    print("=== full-body Hessian (m=1 = sign calibration, must be n_neg=0) ===")
    for path in sorted(glob.glob("/home/udt-admin/udt_mass_codex/u_plat_m*_*.pt")):
        tile = json.load(open(path.replace('.pt', '.json')))
        m = tile['m']; Nr, Nth, Nps = tile['grid']
        G = make_grid_shexact(Nr, Nth, Nps, mmax=Nps // 2)
        u = torch.load(path).to(G.dev)
        try:
            out.append(run(f"plat_m{m}", G, u, m))
        except Exception as e:
            print(f"  {path}: ERROR {e}")
    json.dump(out, open("/home/udt-admin/udt_mass_codex/phase3b_hessian_out.json", "w"), indent=1)
    print("DONE_HESSIAN3B")
