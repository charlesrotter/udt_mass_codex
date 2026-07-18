#!/usr/bin/env python3
"""D1 determinacy check (audit archive/pre_2026-07-01/SOLVER_AUDIT_2026-06-29.md, HIGH finding): is the converged static
solve DETERMINED, or underdetermined (residual-smallness regularized by seed+Levenberg, not pinned
by the metric)? Compute the residual Jacobian J = d(residual)/d(u) at the converged Nr=8 off-ON point
and report: #rows (equations) vs #cols (unknowns), the singular-value spectrum, the numerical rank,
and the null-space dimension (cols - rank). NO solve -- one jacrev eval (minutes).

  rows >= cols AND full column rank (smallest SV >> 0) => DETERMINED (D1 dismissed).
  rows <  cols, or a cluster of ~0 singular values    => UNDERDETERMINED (D1 confirmed): that many
     directions in u are unconstrained by the equations and are fixed only by the seed/min-norm step.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
d = torch.load('solved_fields_nr8_G_kap8_1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.dev); Xfin = float(d['Xfin'])
ncols = u.numel()

F = P1.residual_vector_p1(u, G, 1.0, 1.0, X=Xfin, branch='G')
nrows = F.numel()
print(f"converged point: Phi=(F.F)={float((F*F).sum()):.3e}  |F|_max={float(F.abs().max()):.2e}")
print(f"residual: rows(equations) = {nrows}   unknowns(cols) = {ncols}   (11 fields x {ncols//11} pts)")
print(f"structural: rows {'>=' if nrows>=ncols else '<'} cols  ->  "
      f"{'square/overdetermined' if nrows>=ncols else f'UNDERDETERMINED by >= {ncols-nrows} (rows < cols)'}")

print("computing Jacobian (one jacrev eval)...", flush=True)
J, _ = P1.jacobian_p1(u, G, 1.0, 1.0, X=Xfin, branch='G', chunk_size=128)
print(f"J shape = {tuple(J.shape)}", flush=True)

sv = torch.linalg.svdvals(J.double()).cpu().numpy()      # singular values, descending
smax = sv[0]
print(f"\nsingular values: max={smax:.3e}  min={sv[-1]:.3e}  (ratio max/min = {smax/max(sv[-1],1e-300):.2e})")
for tol_rel in (1e-8, 1e-10, 1e-12):
    tol = tol_rel * smax
    rank = int((sv > tol).sum())
    print(f"  numerical rank @ tol={tol_rel:.0e}*smax: {rank:5d}   null-space dim (cols-rank) = {ncols-rank}")
# distribution: how many SV are tiny (the unconstrained directions)
print(f"\nSV percentiles: {np.percentile(sv,[100,99,90,50,10,1,0]).round(6)}")
print(f"  # SV < 1e-6*smax = {int((sv<1e-6*smax).sum())}   # SV < 1e-10*smax = {int((sv<1e-10*smax).sum())}")
nrank = int((sv > 1e-10*smax).sum())
print(f"\nVERDICT: rank~{nrank} of {ncols} unknowns => {ncols-nrank} unconstrained directions.")
print("  If unconstrained dims >> 0, the solution is NOT pinned by the equations in those directions")
print("  (fixed by seed/min-norm). If rank==cols and min SV well above 0, the solve is DETERMINED.")
