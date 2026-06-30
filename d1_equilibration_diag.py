#!/usr/bin/env python3
"""D1 conditioning DIAGNOSTIC (offline, no solve): does Ruiz equilibration drop the determined-posing
cond~1e11 to a workable range? Builds J at the provisional determined field, measures cond, then iteratively
row/col-equilibrates (safe for a root-find S(u)=0 -- row reweighting does not bias the root) and re-measures.
Category-A (conditioning technique). Cheap: one Jacobian build + a few SVDs."""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D
from torch.func import jacrev

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
ncols = 11*8*6*8
# linearize at the PROVISIONAL determined field (closest to where the solve is grinding); fall back to old.
try:
    d = torch.load('solved_fields_nr8_G_kap8_1_DETERMINED.pt', map_location='cpu', weights_only=False)
    print("[lin pt] provisional DETERMINED field")
except Exception:
    d = torch.load('solved_fields_nr8_G_kap8_1.pt', map_location='cpu', weights_only=False)
    print("[lin pt] old underdetermined field")
u = d['u'].to(G.Dr.device)
f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=-2e5, branch='G', determined=True)
J = jacrev(f, chunk_size=128)(u).double()
print(f"J shape = {tuple(J.shape)}", flush=True)

def cond_of(M):
    sv = torch.linalg.svdvals(M).cpu().numpy()
    return sv[0], sv[-1], sv[0]/max(sv[-1], 1e-300)

s0, smin0, c0 = cond_of(J)
print(f"RAW            : smax={s0:.3e} smin={smin0:.3e} cond={c0:.3e}", flush=True)

# Ruiz equilibration: iterate D_r <- D_r / sqrt(rownorm_inf), D_c <- D_c / sqrt(colnorm_inf)
Dr = torch.ones(J.shape[0], device=J.device)
Dc = torch.ones(J.shape[1], device=J.device)
Js = J.clone()
for it in range(20):
    rn = Js.abs().amax(dim=1).clamp_min(1e-300)
    cn = Js.abs().amax(dim=0).clamp_min(1e-300)
    dr = rn.rsqrt(); dc = cn.rsqrt()
    Js = dr[:, None] * Js * dc[None, :]
    Dr *= dr; Dc *= dc
    if it in (0, 4, 9, 19):
        s, smin, c = cond_of(Js)
        # column-conditioning of the equilibrated system = the relevant one for the Newton step
        print(f"  ruiz it={it:2d}: smax={s:.3e} smin={smin:.3e} cond={c:.3e}"
              f"  (rownorm spread {float(rn.max()/rn.min()):.1e}, colnorm spread {float(cn.max()/cn.min()):.1e})",
              flush=True)
print("INTERPRET: equilibrated cond < ~1e8 => float64 LM should floor it (workable); still >~1e10 => need the"
      " parity/Galerkin basis (endpoint amplification is structural, not mere scaling).", flush=True)

# COLUMN-ONLY scaling (the LM-correct preconditioner: preserves the ||F||^2 objective, conditions the GN solve).
print("\n--- COLUMN-ONLY (preserves objective; the correct LM preconditioner) ---", flush=True)
Dc2 = torch.ones(J.shape[1], device=J.device)
Jc = J.clone()
for it in range(6):
    cn = Jc.abs().amax(dim=0).clamp_min(1e-300).rsqrt()
    Jc = Jc * cn[None, :]; Dc2 *= cn
    if it in (0, 2, 5):
        s, smin, c = cond_of(Jc)
        print(f"  col it={it}: smax={s:.3e} smin={smin:.3e} cond={c:.3e}", flush=True)
print("INTERPRET(col-only): cond < ~1e7 => column-scaled LM should floor while preserving ||F||^2 descent.", flush=True)
