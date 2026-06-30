#!/usr/bin/env python3
"""WHERE does the Phi=2e-3 floor live? (the new central puzzle: the determined solve does not floor even at the
well-conditioned X=-1). Cheap: load the saved X=-1 partial field, evaluate the determined residual, break |F|^2
down by row-GROUP (which equations / which sector / which BC carry the un-floored residual). NO solve, NO Jacobian.
Points at the cause (gauge sector? off-diagonal? matter EOM = the e^{2phi}-weight territory? a specific BC?) before
any expensive re-solve. OBSERVE. Run UNBUFFERED (python3 -u), no grep pipe."""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('xexplore_field_X1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device); X = d['X']
F = P1.residual_vector_p1(u, G, 1.0, 1.0, X=X, branch='G', determined=True)
Phi = float((F*F).sum())
F2 = (F*F).cpu().numpy()
print(f"=== residual localization at saved X={X} field, Phi={Phi:.4e} (total rows={len(F2)}) ===", flush=True)

Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
ni = Nth * Nps
nintr = (Nr - 2) * ni
groups, o = [], 0
for nm in ['E_tt', 'E_rr', 'E_thth', 'E_psps', 'E_rth', 'E_rps', 'E_thps', 'phi_EL',
           'matterEOM_0', 'matterEOM_1', 'matterEOM_2']:
    groups.append((nm, o, o + nintr)); o += nintr
groups.append(('|n|=1', o, o + Nr * ni)); o += Nr * ni
for nm in ['a', 'b', 'c', 'd', 'phi', 'e_rt', 'e_rp', 'e_tp', 'matter_n0', 'matter_n1', 'matter_n2']:
    groups.append((nm + '_core', o, o + ni)); o += ni
    groups.append((nm + '_seal', o, o + ni)); o += ni
assert o == len(F2), (o, len(F2))

# sum of squares per group (= contribution to Phi) + max single-row |F|
gs = sorted([(nm, float(F2[a:b].sum()), float(np.sqrt(F2[a:b].max()))) for (nm, a, b) in groups],
            key=lambda t: -t[1])
print(f"  {'group':18s} {'sum|F|^2 (Phi share)':>22s} {'% of Phi':>9s} {'max|F| row':>12s}", flush=True)
for nm, ss, mx in gs[:14]:
    print(f"  {nm:18s} {ss:22.4e} {100*ss/Phi:8.1f}% {mx:12.3e}", flush=True)
print(f"\nINTERPRET: the group(s) carrying most of Phi localize the floor. If it is the matter EOM / off-diagonal /"
      f" a specific BC, that sector is the obstruction (vs a uniform un-converged crawl).", flush=True)
