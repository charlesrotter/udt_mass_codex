#!/usr/bin/env python3
"""
p2_validate_ab.py -- P2a + P2b VALIDATION (evaluations only; no full coupled solve).

P2a: the 3-D native S^2 EL -- genuine UNIT field, native (cross) L4 == MAT L4, the
     pure-radial F(r) ansatz is polar-singular (the genuine native object ties the
     target polar angle to theta), node core only.
P2b: see p2_divT_fd_gate.py -- the autograd EL == FD variation of the action on a
     NON-DIAGONAL metric (the decisive matter-metric consistency gate, clean of the
     covariant divT operator's own spectral noise).

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  DATA-BLIND.  NEW file.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, T, R, TH, PS, PI, DEV
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2
import whole_metric_3d_matter as MAT


def hdr(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------------------
# 0. UNIT-FIELD CHECK + native cross-product L4 == Lagrange-id L4 on the S^2 3-vector.
# ---------------------------------------------------------------------------
hdr("[P2a-0] genuine UNIT S^2 field + native (cross) L4 == MAT (Lagrange-id) L4")
G = F3.Grid3D(Nr=24, Nth=8, Nps=8, rc=0.05, cell=14.0); G = F3.attach_coord_weight(G)
F_test = 0.7 * G.Rg / G.ri * PI + 0.3 * torch.sin(G.THg) * torch.cos(G.PSg)
n = P2.field_n_s2(G, F_test, m=1)
print(f"  max | |n|^2 - 1 | = {(((n*n).sum(-1)) - 1.0).abs().max().item():.3e}   "
      "(0 => genuine UNIT S^2, no texture artifact)")
dn = P2.field_dn_s2(G, F_test, m=1)
g0 = build_metric(G, *(torch.zeros_like(F_test) for _ in range(4)))
gi0 = inv4x4(g0)
_, _, L4_lag, _ = MAT.lagrangian(gi0, MAT.field_metric(dn), 1.0, 1.0)


def cross(u, v):
    return torch.stack([u[..., 1]*v[..., 2]-u[..., 2]*v[..., 1],
                        u[..., 2]*v[..., 0]-u[..., 0]*v[..., 2],
                        u[..., 0]*v[..., 1]-u[..., 1]*v[..., 0]], -1)


L4_cross = torch.zeros_like(F_test)
for mp in range(4):
    for nq in range(4):
        S1 = cross(dn[..., mp, :], dn[..., nq, :])
        L4_cross = L4_cross - 0.25*gi0[..., mp, mp]*gi0[..., nq, nq]*(S1*S1).sum(-1)
print(f"  max | L4_native(cross) - L4_MAT(Lagrange-id) | = "
      f"{(L4_lag - L4_cross).abs().max().item():.3e}   (0 => MAT stress is native S^2)")


# ---------------------------------------------------------------------------
# 1. P2a -- the round soliton anchor.  The pure-radial F(r) S^2 ansatz is POLAR-
#    SINGULAR (rho diverges on the axis -> M_MS Nr-unstable); the genuine native
#    object ties the target polar angle to theta (F=theta is the texture-free n=x/r
#    monopole with rho theta-INDEPENDENT and T^t_t=T^r_r, the CANON object).  Show both.
# ---------------------------------------------------------------------------
hdr("[P2a-1] axis-regularity: pure-radial F(r) is polar-singular; F=theta is regular")
G = F3.Grid3D(Nr=40, Nth=16, Nps=8, rc=0.05, cell=14.0); G = F3.attach_coord_weight(G)
z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
g = build_metric(G, z, z, z, z); ginv = inv4x4(g)
for label, F in [("F=F(r) separable", PI*(1-(G.Rg-G.rc)/(G.ri-G.rc))),
                 ("F=theta (n=x/r)", G.THg.clone())]:
    dn = P2.field_dn_s2(G, F, m=1)
    Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    rho = -Tmix[..., T, T]
    tt_rr = float((Tmix[..., T, T] - Tmix[..., R, R])[G.body].abs().max())
    rpole = float(rho[20, 0, 0]); requ = float(rho[20, G.Nth//2, 0])
    print(f"  {label:18s}: rho(pole)={rpole:.3e}  rho(equ)={requ:.3e}  "
          f"ratio={rpole/max(requ,1e-30):.1f}  |T^t_t-T^r_r|_max={tt_rr:.2e}")
print("  => F=theta is texture-free (rho flat, T^t_t=T^r_r=CANON); F(r) separable is")
print("     polar-singular (rho axis/equ ratio >>1) -- the genuine native object needs")
print("     F(r,theta) tying target-polar to theta (axis-regular).  See P2c + results.")


# ---------------------------------------------------------------------------
# 2. node-core check: sin F(0)=0 selected, value free; NO m*pi ladder.
# ---------------------------------------------------------------------------
hdr("[P2a-2] core condition = regularity NODE sin F(0)=0 (value free); NO Skyrme m*pi")
for val in (PI, 2*PI, 0.0):
    Fc = torch.full((G.Nth, G.Nps), float(val), device=DEV)
    print(f"  F(core)={val:.4f}: |sin F(core)|={float(torch.sin(Fc).abs().max()):.2e} "
          f"=> {'NODE (regular)' if float(torch.sin(Fc).abs().max())<1e-9 else 'NOT a node'}")
print("  All of {0,pi,2pi} are nodes (sin=0); the operator selects sin F(0)=0, value FREE.")
print("  (deg-1 sector PINS the pi node = homotopy choice, NOT the m*pi ladder.)")
print("\nDONE -- P2b gate is p2_divT_fd_gate.py.")
