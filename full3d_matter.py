#!/usr/bin/env python3
"""
full3d_matter.py -- the FULL-3-D matter sector (unit field on S^3, L2+L4) for the
unreduced coupled solver.  The matter field is FREE over (r,theta,psi); winding m.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

================================================================================
THE FIELD (FREE, non-axisymmetric).  Unit 4-vector n:R^3 -> S^3, parametrized by THREE
free scalar profiles over (r,theta,psi):
   F(r,th,ps) chiral profile;  G,H internal angles of the pion direction n_hat in S^2.
   n = ( cos F,  sin F sin G cos H,  sin F sin G sin H,  sin F cos G )   (|n|=1 exact)
ROUND HEDGEHOG = special case  F=Theta(r), G=theta, H=psi  (the validated #56 field).
Freeing (F,G,H) over all three coords lets the matter take ANY non-axisymmetric /
higher-winding shape -- the dimension prior solves removed.

THE ACTION (settled native, C-2026-06-14-1; identical Lagrangian to
whole_metric_3d_matter.py, infra-audit CLEAN):
   L2 = -(xi/2)  g^{mn} G_{mn},   G_{mn} = d_m n . d_n n
   L4 = -(kap/4) g^{mp} g^{nq} (G_{mp}G_{nq} - G_{mq}G_{np})
   S  = INT sqrt(-g) (L2+L4) dt dr dtheta dpsi

THE MATTER EL (correct OFF-ROUND BY CONSTRUCTION -- the cure for the 2-D L4 bug).
The Euler-Lagrange equation for each field phi in {F,G,H} is the variation
   delta S / delta phi = 0.
We evaluate S as a SPECTRAL QUADRATURE over the grid (Clenshaw-Curtis in r x spherical
quadrature in (theta,psi), with sqrt(-g) the proper measure) and take its gradient
w.r.t. the field NODAL VALUES by AUTOGRAD.  This gradient IS the discrete EL: it is the
exact variation of the SAME native action, so it is correct off-round automatically
(no separate symbolic EL to get wrong in the L4 sector).  CATEGORY-A: autograd is a
sanctioned machine-precision function-replacement (the same tool as the autograd
Jacobian in the validated 2-D solver); spectral quadrature is exact for smooth fields.

VERIFICATION (delivered in full3d_catalog_results.md):
  (a) on the ROUND hedgehog the matter EL (= dS/dfield) is machine-zero (the #56 gate);
  (b) the div-identity  div_mu T^mu_nu = -(EL.dphi)  holds off-round (the bug-exposing
      test) -- T^mu_nu from the verified whole_metric_3d_matter.stress_tensor, EL from
      this autograd variation, both on a psi-dependent field.

This module also provides the field gradient dn (spectral) for the stress tensor
(reusing whole_metric_3d_matter.stress_tensor, infra-audit CLEAN).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi


# ---------------------------------------------------------------------------
# The unit field n (...,4) from (F,G,H).
# ---------------------------------------------------------------------------
def field_n(F, G, H):
    sF, cF = torch.sin(F), torch.cos(F)
    sG, cG = torch.sin(G), torch.cos(G)
    sH, cH = torch.sin(H), torch.cos(H)
    return torch.stack([cF, sF*sG*cH, sF*sG*sH, sF*cG], dim=-1)


# ---------------------------------------------------------------------------
# Spectral derivative helpers on a field of shape (Nr, Nth, Nps).
# Dr (Nr,Nr) Chebyshev; Dth (Nth,Nth) Legendre; Dps (Nps,Nps) Fourier.
# ---------------------------------------------------------------------------
def d_r(f, Dr):
    return torch.einsum('ij,jkl->ikl', Dr, f)

def d_th(f, Dth_sh):
    """SH-EXACT d/dtheta.  Dth_sh is the flattened (Nth*Nps, Nth*Nps) SH matrix;
    f is (Nr,Nth,Nps)."""
    Nr, Nth, Nps = f.shape
    flat = f.reshape(Nr, Nth * Nps)
    out = torch.einsum('ab,ib->ia', Dth_sh, flat)
    return out.reshape(Nr, Nth, Nps)

def d_ps(f, Dps):
    return torch.einsum('lm,ijm->ijl', Dps, f)


# ---------------------------------------------------------------------------
# THE DISCRETE ACTION  S = sum_grid  w_r w_Omega  sqrt(-g) (L2+L4).
# g: (Nr,Nth,Nps,4,4) diagonal Weyl metric;  field (F,G,H): (Nr,Nth,Nps).
# Returns scalar S (torch, autograd-connected to F,G,H).
# ---------------------------------------------------------------------------
def field_metric_Gmn(dn):
    # dn (...,4_coord, 4_target);  G_{mn} = sum_a dn[...,m,a] dn[...,n,a]
    return torch.einsum('...ma,...na->...mn', dn, dn)


def lagrangian_density(ginv, Gmn, xi, kap):
    L2 = -(xi/2) * torch.einsum('...mn,...mn->...', ginv, Gmn)
    GG1 = torch.einsum('...mp,...nq->...mnpq', Gmn, Gmn)
    GG2 = torch.einsum('...mq,...np->...mnpq', Gmn, Gmn)
    SS = GG1 - GG2
    L4 = -(kap/4) * torch.einsum('...mp,...nq,...mnpq->...', ginv, ginv, SS)
    return L2 + L4


def build_dn(F, G, H, Dr, Dth, Dps):
    """Spectral coordinate derivatives of n: dn (Nr,Nth,Nps,4_coord,4_target).
    d_t n = 0 (static).  coord order (t,r,theta,psi)."""
    n = field_n(F, G, H)                       # (Nr,Nth,Nps,4)
    Nr, Nth, Nps, _ = n.shape
    dn = torch.zeros(Nr, Nth, Nps, 4, 4, dtype=n.dtype, device=n.device)
    # for each target component, take spectral derivatives
    for a in range(4):
        na = n[..., a]
        dn[..., 1, a] = d_r(na, Dr)            # d_r
        dn[..., 2, a] = d_th(na, Dth)          # d_theta
        dn[..., 3, a] = d_ps(na, Dps)          # d_psi
    return dn, n


def action(F, G, H, ginv_diag, sqrtg, wr, wOm, Dr, Dth, Dps, xi, kap):
    """Discrete action S (scalar).  ginv_diag (Nr,Nth,Nps,4) the diagonal inverse
    metric; sqrtg (Nr,Nth,Nps)=sqrt(-g); wr (Nr,) radial CC weights; wOm (Nth,Nps)
    spherical area weights."""
    dn, n = build_dn(F, G, H, Dr, Dth, Dps)
    Gmn = field_metric_Gmn(dn)
    ginv = torch.diag_embed(ginv_diag)          # (...,4,4)
    Ldens = lagrangian_density(ginv, Gmn, xi, kap)
    # measure: sqrt(-g) * w_r * w_Omega
    w = sqrtg * wr[:, None, None] * wOm[None, :, :]
    return (Ldens * w).sum()


def matter_EL(F, G, H, ginv_diag, sqrtg, wr, wOm, Dr, Dth, Dps, xi, kap):
    """The matter Euler-Lagrange residual fields EL_F,EL_G,EL_H = dS/d(field nodal),
    by autograd.  Correct OFF-ROUND by construction (exact variation of the action).
    Returns (EL_F, EL_G, EL_H), each (Nr,Nth,Nps).  Note: dS/dphi_node already carries
    the measure weight w; to compare to a pointwise EL density we divide it out."""
    Fv = F.detach().clone().requires_grad_(True)
    Gv = G.detach().clone().requires_grad_(True)
    Hv = H.detach().clone().requires_grad_(True)
    S = action(Fv, Gv, Hv, ginv_diag, sqrtg, wr, wOm, Dr, Dth, Dps, xi, kap)
    gF, gG, gH = torch.autograd.grad(S, [Fv, Gv, Hv], create_graph=False)
    # divide out the measure weight to get a pointwise EL density (interior only;
    # the weight is strictly positive in the interior)
    w = sqrtg * wr[:, None, None] * wOm[None, :, :]
    return gF, gG, gH, w
