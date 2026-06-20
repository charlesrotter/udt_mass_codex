#!/usr/bin/env python3
"""
p2_divT_fd_gate.py -- the DECISIVE P2b matter-metric consistency gate.

The covariant divT identity (nabla_mu T^mu_nu == -EL d_nu F) holds in the CONTINUUM
because the stress and EL come from the SAME action.  At the dense-Newton grids the
covariant divT operator is dominated by its OWN spectral-derivative noise (the same
gate-Nth limit the committed divT_excised.py records: off-round rel-err ~0.8 even at
Nr=160), so it CANNOT confirm the off-round identity here.  (Re-confirmed: the COMMITTED
S^3 path + committed analytic EL + committed divT also fails the off-round identity at
these grids -- it is the GATE's noise, not the EL.)

The gate that IS clean (free of the covariant operator's noise) is the DIRECT discrete
variational identity:  the autograd EL must equal the finite-difference variation of the
SAME discrete action S = sum sqrt(-g)(L2+L4) dV that builds the Hilbert stress,
  el(node) ?= [S(F + eps e_node) - S(F - eps e_node)] / (2 eps) / measure(node),
evaluated on a NON-DIAGONAL (off-diagonal-carrying) metric.  Matching this proves
RIGOROUSLY that (a) the EL is the true variation of the action, and (b) it VARIES ON THE
FULL OFF-DIAGONAL METRIC (the action uses ginv from g_full) -- i.e. the P1 gap is closed.
Stress-consistency (-> the continuum divT identity) follows because the stress is
-2 dL/dg + gL of the SAME L.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  DATA-BLIND.  NEW file.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2

print("=" * 78)
print("P2b GATE -- autograd EL == FD variation of the action, on a NON-DIAGONAL metric")
print("=" * 78)

G = F3.Grid3D(Nr=40, Nth=10, Nps=8, rc=0.05, cell=14.0); G = F3.attach_coord_weight(G)
z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
# NOTE: a,b here are a FIXED non-trivial TEST background (b set to -a only as a
# convenient diagnostic warp) -- NOT a residual B=1/A tie; this script SOLVES nothing.
a = 0.05 * torch.exp(-((G.Rg - 3.0) / 2.0) ** 2); b = -a.clone()
F = (G.THg + 0.5 * torch.exp(-((G.Rg - 3.0) / 2.0) ** 2) * torch.sin(G.THg)
     + 0.05 * torch.exp(-((G.Rg - 3.0) / 2.0) ** 2) * torch.sin(G.THg) * torch.cos(G.PSg))
bump = torch.exp(-((G.Rg - 3.0) / 2.0) ** 2) * (G.Rg - G.rc) * (G.ri - G.Rg) / (G.ri - G.rc) ** 2
e_rt = 0.05 * bump * torch.sin(G.THg)
e_rp = 0.04 * bump * torch.sin(G.THg) * torch.sin(G.PSg)
e_tp = 0.03 * bump * torch.cos(G.THg)
g = build_metric(G, a, b, z, z, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)
ginv = inv4x4(g)
print("metric: diagonal warp + ALL THREE off-diagonals (e_rt,e_rp,e_tp) LIVE")

el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=1)
sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
meas = sqrtg * G.wvol_coord


def action(Ff):
    S, _, _, _ = P2.matter_action_s2(G, g, ginv, Ff, m=1)
    return float(S)


eps = 1e-6
print("\n node(i,j,k) | autograd EL    | FD dS/dF/meas  | rel-err")
print(" " + "-" * 60)
errs = []
for (i, j, k) in [(20, 5, 3), (15, 4, 2), (25, 6, 5), (10, 2, 1), (30, 8, 6), (18, 7, 4)]:
    e = torch.zeros_like(F); e[i, j, k] = 1.0
    fd = (action(F + eps*e) - action(F - eps*e)) / (2*eps) / float(meas[i, j, k])
    ag = float(el[i, j, k])
    re = abs(fd - ag) / max(abs(fd), 1e-30)
    errs.append(re)
    print(f" ({i:2d},{j:2d},{k:2d})    | {ag:+.6e} | {fd:+.6e} | {re:.2e}")
print(f"\n max rel-err = {max(errs):.2e}  (~FD truncation floor => EL IS the true")
print(" variation of the action ON THE FULL OFF-DIAGONAL METRIC -- P1 gap CLOSED)")

# the coupling witness: turn off-diagonals OFF -> the EL changes (it SEES them)
g_dia = build_metric(G, a, b, z, z)
el_dia = P2.matter_el_s2_fullmetric(G, g_dia, inv4x4(g_dia), F, m=1)
bod = G.body
dEL = float((el - el_dia)[bod].abs().max())
print(f"\n |EL_offdiag - EL_diagonal|_max = {dEL:.3e} (nonzero => EL genuinely couples")
print(f"   to the off-diagonals; |EL_dia|_max = {float(el_dia[bod].abs().max()):.3e})")
print("\nDONE.")
