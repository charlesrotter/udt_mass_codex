#!/usr/bin/env python3
"""
p5b_diag.py -- P5b DIAGNOSTIC (no gate, no record): characterize the re-posed
operator's spectrum + block structure to design the LIGHTEST effective right-PC.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.  Branch p5b-pc-floor.

We want to know, on the FULL-RANK reposed J (body DOF), where the conditioning lives:
 - the singular-value spread (kappa) and where the small SVs sit (which field/row class),
 - whether a cheap diagonal of J^T J (block-Jacobi) already flattens the spectrum,
 - whether the bad conditioning is RADIAL-band (Cheb d/dr on the steep core) -> a
   radial-band approx-inverse PC is the natural cheap fix.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")  # dense jacrev path
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight
from full3d_solver import round_seed, unpack
import p5a_prime_repose as RP

NR, NTH, NPS = 12, 6, 8
P, KAP8 = 0.4, 0.05
G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
u0, sol = round_seed(G, p=P, kap8=KAP8)
rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(u0)
ub0 = rp.extract(u0)
print("nB =", rp.nB, "body rows =", rp.body_r.tolist())

# build the dense reposed J at the seed
J, F = RP.reposed_jacobian_jacrev(ub0, rp, KAP8)
print("J shape", tuple(J.shape), "Phi0 =", float((F*F).sum()))
S = torch.linalg.svdvals(J)
print(f"raw J: kappa={float(S[0]/S[-1]):.3e}  smax={float(S[0]):.3e} smin={float(S[-1]):.3e}")
print("  smallest 8 SVs:", [f"{float(x):.3e}" for x in S[-8:]])

# ---- block-Jacobi (diagonal of J^T J) right-PC: D^{-1/2} ----
JTJ_diag = (J*J).sum(0)                      # exact diag(J^T J)
dscale = 1.0/torch.sqrt(torch.clamp(JTJ_diag, min=1e-30))
Jd = J*dscale[None, :]                        # J D^{-1/2}  (right-PC)
Sd = torch.linalg.svdvals(Jd)
print(f"diag-PC J D^-1/2: kappa={float(Sd[0]/Sd[-1]):.3e}  smin={float(Sd[-1]):.3e}")

# ---- where does the diag scale vary? per-field, per-radial-row ----
# body DOF order: field f in [a,b,c,d,Th], radial body row j, (th,ps)
nbr, Nth, Nps = rp.nbr, rp.Nth, rp.Nps
ds = dscale.reshape(5, nbr, Nth, Nps)
fields = ['a', 'b', 'c', 'd', 'Th']
print("per-field diag-PC scale (geomean over each field block):")
for f in range(5):
    blk = ds[f]
    print(f"  {fields[f]}: min={float(blk.min()):.2e} max={float(blk.max()):.2e} "
          f"geomean={float(torch.exp(torch.log(blk).mean())):.2e}")
print("per-radial-body-row diag-PC scale (geomean over fields,th,ps):")
gm_row = torch.exp(torch.log(ds).mean(dim=(0, 2, 3)))
for j, rr in enumerate(rp.body_r.tolist()):
    print(f"  body-row r-idx={rr} (r={float(G.r[rr]):.3f}): geomean-scale={float(gm_row[j]):.2e}")

# ---- RADIAL-BAND structure probe: is J dominated by the Cheb d/dr coupling? ----
# Reshape columns by (field, radial). For each output row, the column with the
# largest |J| entry: is it same-radial or cross-radial (derivative coupling)?
print("\n[done diag]")
