#!/usr/bin/env python3
"""Follow-up #2 to the kap8 characterization (verifier finding C): re-solve the COMPLETE solver at
Nr=8 SAVING the fields, and measure whether the native S^2 winding SURVIVED or UNWOUND to vacuum.

The 40.9h characterization reported only (Phi, metric warp) -- it never checked the matter.  With the
FREE core the degree-1 winding seed (n=x/r) could relax to a CONSTANT (degree-0 vacuum), in which case
the converged "warp" is a boundary-condition artifact with NO matter.  This measures the topological
DEGREE per radial shell  Q(r) = (1/4pi) int nhat.(d_th nhat x d_ps nhat) dth dps  on the SOLVED field,
using the GRID-EXACT dn (so the winding readout itself is not corrupted by the bare-sin(theta) grid bug).
Q(r) ~ 1 across shells => winding SURVIVED (non-trivial S^2 matter solution).
Q(r) ~ 0              => UNWOUND to vacuum (the warp is a BC artifact, no matter).

Branch G, kap8=1, X->-2e5, Nr=8 (~2h -- cheapest representative of the matter character).  BUILD/SOLVE;
run MYSELF in background, NO nohup, output straight to file (no `| grep`).
"""
import os, time
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
import numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M
import whole_metric_3d_matter as MAT
from full3d_spectral import Grid3D, attach_coord_weight, build_metric, T, R, TH, PS
from full3d_newton import inv4x4


def diag(u, G, tag):
    a, b, c, d, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    n_raw = torch.stack([n1, n2, n3], dim=-1)
    nrm = torch.sqrt(torch.clamp((n_raw ** 2).sum(-1), min=1e-300))
    nhat = n_raw / nrm[..., None]
    dn = S2M.field_dn_components_exact(G, n_raw)                  # grid-EXACT dn
    wth_plain = G.wmu / G.sth                                     # plain d-theta weight (Nth,)
    dpl = wth_plain[None, :, None] * G.wps[None, None, :]         # dth dps element
    cr = torch.cross(dn[..., TH, :], dn[..., PS, :], dim=-1)      # d_th n x d_ps n
    Q_r = ((nhat * cr).sum(-1) * dpl).sum(dim=(1, 2)) / (4 * np.pi)   # (Nr,) degree per shell
    g = build_metric(G, a, b, c, d, e_rt=ert, e_rp=erp, e_tp=etp); ginv = inv4x4(g)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    rho = -torch.einsum('...ma,...an->...mn', ginv, Tab)[..., T, T]
    bod = G.body
    Qb = Q_r[2:-2]                                                # interior shells
    print(f"[{tag}] |n| in [{float(nrm.min()):.4f},{float(nrm.max()):.4f}]  "
          f"degree Q(interior shells): min={float(Qb.min()):.3f} max={float(Qb.max()):.3f} "
          f"mean={float(Qb.mean()):.3f}  rho_max(body)={float(rho[bod].abs().max()):.3e}  "
          f"warp(a..d)={max(float(x.abs().max()) for x in (a,b,c,d)):.3f} "
          f"phi_max={float(phi.abs().max()):.3f}", flush=True)
    print(f"        Q per shell: {np.round(Q_r.cpu().numpy(), 3)}", flush=True)
    return Q_r


t0 = time.time()
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
u0 = P1.seed_round_native(G, p=1.0, m=1)
print("=== SEED (canon n=x/r, degree-1 expected) ===", flush=True)
diag(u0, G, "seed")
print("\n=== SOLVING Nr=8 branch=G kap8=1 X->-2e5 (saving fields) ===", flush=True)
u, hist, Xfin = P1.continuation_solve_p1(u0, G, 1.0, 1.0, X_target=-2.0e5, m=1, branch="G", verbose=True)
torch.save({'u': u.cpu(), 'Xfin': Xfin, 'Nr': 8, 'branch': 'G', 'kap8': 1.0},
           'solved_fields_nr8_G_kap8_1.pt')
F = P1.residual_vector_p1(u, G, 1.0, 1.0, X=Xfin, branch="G")
print(f"\n=== SOLVED (Phi={float((F*F).sum()):.3e}  Xfin={Xfin:.2e}  t={time.time()-t0:.0f}s) ===", flush=True)
diag(u, G, "solved")
print("\nVERDICT: Q(r)~1 across shells => winding SURVIVED (non-trivial S^2 matter);"
      " Q(r)~0 => UNWOUND to vacuum (warp is a BC artifact).", flush=True)
