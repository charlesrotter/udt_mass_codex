#!/usr/bin/env python3
"""D1 fix — bounded RE-SOLVE on the DETERMINED posing + inline RE-GRADE of the soft quantities.
Tests whether the determined posing (full rank, but cond~1e11) is SOLVABLE with LM damping, or whether
the conditioning needs the parity/Galerkin basis upgrade. Self-contained: writes per-step progress, saves
the field, and prints the re-graded quantities (so a summarized/fresh session can read the log + re-grade).
FREE physics constants this rides: branch=G (FREE), kap8=1 (THEORY), X=-2e5 (FREE), xi=kap=1 (THEORY).
Conditioning params (Nr, n_steps, maxit) = category-A. Run MYSELF, bounded, single process, NO nohup."""
import os, time
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M
import whole_metric_3d_matter as MAT
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
from full3d_newton import inv4x4

t0 = time.time()
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
u0 = P1.seed_round_native(G, p=1.0, m=1)
print("=== D1 RE-SOLVE: determined=True, cold continuation, Nr=8 Branch G kap8=1 X->-2e5 ===", flush=True)
u, hist, Xfin = P1.continuation_solve_p1(u0, G, 1.0, 1.0, X_target=-2.0e5, m=1, branch="G",
                                         n_steps=14, maxit=12, determined=True, verbose=True)
F = P1.residual_vector_p1(u, G, 1.0, 1.0, X=Xfin, branch="G", determined=True)
Phi = float((F * F).sum())
torch.save({'u': u.cpu(), 'Xfin': Xfin, 'Nr': 8, 'branch': 'G', 'kap8': 1.0, 'determined': True},
           'solved_fields_nr8_G_kap8_1_DETERMINED.pt')
print(f"\n=== SOLVED (Phi={Phi:.3e}, Xfin={Xfin:.2e}, t={time.time()-t0:.0f}s) ===", flush=True)

# ---- RE-GRADE the soft quantities on the determined field (vs the old underdetermined values) ----
a, b, c, d, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
n_raw = torch.stack([n1, n2, n3], -1)
dn = S2M.field_dn_components_exact(G, n_raw)
g = build_metric(G, a, b, c, d, e_rt=ert, e_rp=erp, e_tp=etp); ginv = inv4x4(g)
rho = -torch.einsum('...ma,...an->...mn', ginv, MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)[0])[..., T, T]
warp = max(float(x.abs().max()) for x in (a, b, c, d))
eoff = max(float(x.abs().max()) for x in (ert, erp, etp))
nrm = torch.sqrt(torch.clamp((n_raw**2).sum(-1), min=1e-300))
wth = G.wmu / G.sth; dpl = wth[None, :, None] * G.wps[None, None, :]
crs = torch.cross(dn[..., TH, :], dn[..., PS, :], dim=-1)
Q_r = ((n_raw/nrm[..., None] * crs).sum(-1) * dpl).sum(dim=(1, 2)) / (4*np.pi)
Qint = Q_r[2:-2]
print("RE-GRADE (DETERMINED posing) vs OLD (underdetermined min-norm) values:")
print(f"  winding degree Q interior mean = {float(Qint.mean()):.3f}  (OLD 0.977; QUALITATIVE/topological -- expect SURVIVE)")
print(f"  |n| range = [{float(nrm.min()):.4f},{float(nrm.max()):.4f}]")
print(f"  phi range = [{float(phi.min()):.4f},{float(phi.max()):.4f}]  (OLD ~[-0.041,0.003], gentle)")
print(f"  diagonal warp max|a,b,c,d| = {warp:.4f}  (OLD off-ON 1.022 -- QUANTITATIVE, may move)")
print(f"  off-diag eoff_max = {eoff:.3e}  (OLD e_rt~0.112)")
print(f"  rho_max(body) = {float(rho[G.body].abs().max()):.3e}  (OLD 0.182 -- QUANTITATIVE, may move)")
print(f"  lapse exp(a) min(body) = {float(torch.exp(a)[G.body].min()):.4f}  (OLD 0.37 -- not-a-horizon check)")
print("\nINTERPRET: qualitative (degree~1, lapse O(1), gentle phi) expected to SURVIVE; quantitative numbers"
      " (warp, rho_max, eoff) may MOVE -- that move is the point of re-grading on a determined solve.")
print(f"SOLVE HEALTH: Phi={Phi:.3e} -- floored(<1e-6) => determined posing SOLVES with LM (cond~1e11 workable);"
      " stalled high => needs parity/Galerkin basis (the flagged conditioning work).", flush=True)
