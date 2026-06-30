#!/usr/bin/env python3
"""D1 conditioning -- ISOLATE the smax source (KTE falsified the Chebyshev-endpoint hypothesis: smax 7.1e6
barely moved under node declustering). Candidates the KTE agent named: the X=-2e5 stiff phi-throttle (a CHOSEN
physics placeholder), the wbc=30 BC penalty, the W weight. Test: (1) sweep X -> does smax scale with |X|?
(2) row-norm breakdown by residual row-GROUP -> which rows carry the large norm? Cheap (a few Jacobian builds).
Category-A diagnosis (but X is a FREE PHYSICS constant -- if it drives smax, that's a chose-or-derived premise,
not a numerical fix). OBSERVE. Run UNBUFFERED (python3 -u), no grep pipe."""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
from torch.func import jacrev

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
u = P1.seed_round_native(G, p=1.0, m=1)

print("=== (1) does smax scale with |X|? (determined Jacobian at seed, standard grid) ===", flush=True)
for X in (-1.0, -1e2, -1e4, -2e5):
    f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=X, branch='G', determined=True)
    J = jacrev(f, chunk_size=128)(u).double()
    sv = torch.linalg.svdvals(J).cpu().numpy()
    print(f"  X={X:>9.1f}: smax={sv[0]:.4e} smin={sv[-1]:.3e}  (smax/|X|={sv[0]/abs(X):.3e})", flush=True)

print("\n=== (2) WHICH rows carry the large norm? row-norm breakdown by group (X=-2e5) ===", flush=True)
# reproduce the determined-branch row ORDER to label row groups (see p1_residual determined branch)
Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
ni = Nth * Nps
nintr = (Nr - 2) * ni
f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=-2e5, branch='G', determined=True)
J = jacrev(f, chunk_size=128)(u).double()
rn = J.abs().amax(dim=1).cpu().numpy()         # per-row inf-norm
groups = []
o = 0
for nm in ['E_tt', 'E_rr', 'E_thth', 'E_psps', 'E_rth', 'E_rps', 'E_thps', 'phi_EL',
           'matterEOM_0', 'matterEOM_1', 'matterEOM_2']:
    groups.append((nm, o, o + nintr)); o += nintr           # interior PDE rows (Nr-2 layers)
groups.append(('|n|=1(all nodes)', o, o + Nr * ni)); o += Nr * ni
# endpoint closures: pairs (core,seal) of ni each, in the branch's append order
for nm in ['a', 'b', 'c', 'd', 'phi', 'e_rt', 'e_rp', 'e_tp', 'matter_n0', 'matter_n1', 'matter_n2']:
    groups.append((nm + '_core', o, o + ni)); o += ni
    groups.append((nm + '_seal', o, o + ni)); o += ni
print(f"  total rows={len(rn)} (accounted {o})", flush=True)
gn = sorted([(nm, float(rn[a:b].max())) for (nm, a, b) in groups], key=lambda t: -t[1])
for nm, mx in gn[:12]:
    print(f"    {nm:18s} max row-norm = {mx:.4e}", flush=True)
print("INTERPRET: if smax ~ |X| and the top rows are phi_EL / off-diagonal-Einstein -> the X=-2e5 phi-throttle"
      " (a CHOSEN placeholder) drives the conditioning -> premise question, not a preconditioner.", flush=True)
