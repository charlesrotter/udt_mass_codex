#!/usr/bin/env python3
"""
p3_aphi_matter.py -- PHASE 3 of the everything-on solver build: the a(phi) CAPABILITY.

GOAL (EVERYTHING_ON_SOLVER_BUILD_MAP.md P3 + premise ledger L-a):
Wire the CAPABILITY for the matter coupling exponent `a` to be a FUNCTION a(phi).
Insert the e^{(a+1)phi} source weight into the matter action/stress consistently with
the field-equation arc, with the Bianchi-forced modified conservation
div T = -(a+1) phi' T.  TWO CASES, NEVER CONFLATED:
  * BASELINE a=-1 (k=0): weight identically 1, standard conservation -> reproduces P2
    EXACTLY.  The validated zero point and the PRIMARY reported case.
  * EXPLORATION a(phi)!=-1 (k!=0): a SEPARATE, DECLARED hypothesis with stated (k,p,eps0);
    UNFORCED at the principle level (a=-1=GR remains admissible); never "the UDT answer".

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE mode.  DATA-BLIND.
Branch: p3-aphi-coupling.  NEW file; committed scripts IMMUTABLE; builds on P2.

================================================================================
WHERE THE WEIGHT IS PLACED, AND WHY (the placement is a smuggle-risk; cite the arc)
================================================================================
The field-equation arc (udt_field_equations_derivation_results.md sec.3, sec.2b;
udt_a_exponent_derivation_results.md sec.0) banks, twice blind-verified:

    G^mu_nu = (8 pi G / c^4) * e^{(a+1)phi} * T^mu_nu      [the WEIGHT on the SOURCE]
    curvature side UNCHANGED ; vacuum = GR (weight multiplies zero in vacuum)
    a=-1 => weight=1 => UDT=GR ; a!=-1 => genuine, NON-absorbable modification
    Bianchi forces:  div T = -(a+1) phi' T   (a=-1 -> standard div T = 0)

ABSORBABILITY SUBTLETY honored: a CONSTANT weight (constant a) RELABELS to GR
(absorbable).  ONLY a position-dependent a(phi) is genuinely new.  Derived shape
(a_function_both_extremes.py): a(phi) = -1 + k*eps0^p*e^{-p phi} (k,p,eps0 declared,
NOT fitted; k departure strength UNFORCED, p exponent, eps0 scale).

PLACEMENT (the one load-bearing choice):  the weight goes on the matter ACTION
DENSITY, NOT hand-multiplied onto the assembled stress:

    S_matter = int sqrt(-g) * W(phi) * L_matter d^4x ,   W(phi) = e^{(a+1)phi}

WHY the action and not the stress:
  (1) It is the action that the arc's field equation derives from (sec.3:
      S = int sqrt(-g)[c^4/16piG R + L_matter], the modification a reweighting of
      L_matter's contribution).  Placing it in the action is the derived placement.
  (2) phi here is the GEOMETRIC POTENTIAL read off the metric (phi = b, since
      g_rr = e^{2phi} = e^{2b} in this codebase's convention -- DERIVED identification,
      not a new field).  W(phi) is therefore a POSITION-FIELD MULTIPLIER on the
      Lagrangian density; it is NOT a function of the matter field F, and (in the
      arc's treatment) phi is the external potential, NOT a metric DOF varied here.
  (3) Consequently the Hilbert stress of the weighted density is
          Tw_munu = -2/sqrt(-g) * delta(sqrt(-g) W L)/delta g^munu = W * T_munu(L)
      (W passes through as a scalar multiplier), reproducing the arc's source weight
      EXACTLY -- and the EL = delta S_w/delta F carries the SAME W, so stress and EL
      stay MUTUALLY CONSISTENT BY CONSTRUCTION.  The modified conservation then
      EMERGES from Bianchi (nabla_mu(W T^mu_nu)=0 => nabla_mu T^mu_nu =
      -(1/W) d_mu W T^mu_nu = -(a+1) phi_mu T^mu_nu); it is NOT imposed.  This is the
      whole point of placing W in the action rather than patching the stress.

  SMUGGLE FLAG: a tempting WRONG placement is to weight only one sector (e.g. only
  the kinetic X piece) -- that is the a_eff sector-split of udta sec.3 and would
  smuggle a "which invariant is the mass" choice.  We do NOT do that: the arc's
  banked weight is UNIFORM on the whole source.  We weight the whole L (=L2+L4)
  uniformly, exactly as banked.  (The sector-split is a DIFFERENT, unbanked question.)
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    DEV, PI, T, R, TH, PS)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2


# ===========================================================================
# phi READ OFF THE METRIC (DERIVED identification, not a new field).
#   g_rr = e^{2 b} = e^{2 phi}  (CANON C-2026-06-18-1)  =>  phi = b.
# We read phi from g_rr so the weight depends on the ACTUAL solved metric, not on
# a separately-tracked field (no double bookkeeping).  phi = 0.5 ln(g_rr).
# ===========================================================================
def phi_from_metric(g):
    return 0.5 * torch.log(torch.clamp(g[..., R, R], min=1e-30))


# ===========================================================================
# THE DECLARED a(phi) FUNCTION (the L-a choice, made VISIBLE).
#   a(phi) = -1 + k * eps0^p * e^{-p phi}           [a_function_both_extremes.py]
#   weight W(phi) = e^{(a(phi)+1) phi} = e^{ k eps0^p e^{-p phi} * phi }
#   k = 0  =>  a == -1  =>  W == 1  =>  GR baseline (validated zero point).
#   k != 0 =>  a(phi) is a genuine FUNCTION of position => NON-absorbable (shown below).
# (k,p,eps0) are DECLARED parameters, NOT fitted.  DATA-BLIND: no wall numbers.
# ===========================================================================
def a_of_phi(phi, k=0.0, p=1.0, eps0=1.0):
    return -1.0 + k * (eps0 ** p) * torch.exp(-p * phi)


def weight_W(phi, k=0.0, p=1.0, eps0=1.0):
    """W(phi) = e^{(a(phi)+1) phi}.  k=0 -> W identically 1 (machine-exact)."""
    aP1 = (a_of_phi(phi, k=k, p=p, eps0=eps0) + 1.0)   # = k eps0^p e^{-p phi}
    return torch.exp(aP1 * phi)


# ===========================================================================
# WEIGHTED native-S^2 STRESS:  Tw_munu = W(phi) * T_munu(L).   (placement: the
# weight multiplies the Hilbert stress of the SAME action density it weights, so
# Tw = W*T exactly -- see the header derivation Tw = -2/sqrt(-g) d(sqrt(-g) W L)/dg.)
# k=0 -> W=1 -> identical to P2's stress_s2_fullmetric.
# ===========================================================================
def stress_s2_weighted(g, ginv, dn, k=0.0, p=1.0, eps0=1.0, xi=1.0, kap=1.0):
    Tab, L, L2, L4 = MAT.stress_tensor(g, ginv, dn, xi, kap)
    phi = phi_from_metric(g)
    W = weight_W(phi, k=k, p=p, eps0=eps0)
    return Tab * W[..., None, None], L, L2, L4, W


# ===========================================================================
# WEIGHTED matter ACTION:  S_w = sum sqrt(-g) W(phi) L dV.   (the derived placement)
# ===========================================================================
def matter_action_weighted(G, g, ginv, F, m=1, k=0.0, p=1.0, eps0=1.0, xi=1.0, kap=1.0):
    dn = P2.field_dn_s2(G, F, m=m)
    Gmn = MAT.field_metric(dn)
    L, L2, L4, SS = MAT.lagrangian(ginv, Gmn, xi, kap)
    phi = phi_from_metric(g)
    W = weight_W(phi, k=k, p=p, eps0=eps0)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    S = (sqrtg * W * L * G.wvol_coord).sum()
    return S, L, dn, Gmn, W


# ===========================================================================
# WEIGHTED matter EL by AUTOGRAD: el(node) = (1/measure) delta S_w / delta F(node).
# The SAME weighted action that builds the weighted stress -> EL & stress mutually
# consistent -> the MODIFIED conservation div T = -(a+1) phi' T holds in continuum.
# k=0 -> W=1 -> identical to P2's matter_el_s2_fullmetric.
# ===========================================================================
def matter_el_s2_weighted(G, g, ginv, F, m=1, k=0.0, p=1.0, eps0=1.0, xi=1.0, kap=1.0):
    F_ = F.detach().clone().requires_grad_(True)
    dn = P2.field_dn_s2(G, F_, m=m)
    Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv.detach(), Gmn, xi, kap)
    phi = phi_from_metric(g.detach())
    W = weight_W(phi, k=k, p=p, eps0=eps0)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g.detach()), min=1e-30))
    S = (sqrtg * W * L * G.wvol_coord).sum()
    gradF, = torch.autograd.grad(S, F_, create_graph=False)
    meas = sqrtg * G.wvol_coord
    el = gradF / torch.clamp(meas, min=1e-30)
    return el


# ===========================================================================
# THE MODIFIED CONSERVATION RESIDUAL (the generalized divT gate).
#   target identity (Bianchi-forced):  nabla_mu T^mu_nu  =  -(a+1) phi_mu T^mu_nu
# i.e.  nabla_mu (W T^mu_nu) = 0  with W=e^{(a+1)phi}.  We compute BOTH:
#   lhs = covariant_divT(T)          (P2's covariant operator, on the UNWEIGHTED T)
#   rhs = -(a+1) phi_,mu T^mu_nu     (the forced source-exchange term)
# and the WELDED form  nabla_mu(W T^mu_nu)  whose vanishing is the clean statement.
# (The covariant operator is gate-Nth-limited off-round on this driver -- P2 sec.3;
#  reported as such, not forced.)
# ===========================================================================
def modified_conservation_residual(G, g, ginv, dn, k=0.0, p=1.0, eps0=1.0,
                                    xi=1.0, kap=1.0):
    # unweighted stress and its covariant divergence
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, xi, kap)
    divT = P2.covariant_divT_field(G, g, ginv, Tab)            # nabla_mu T^mu_nu
    # the forced exchange term -(a+1) phi_,mu T^mu_nu
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)       # T^mu_nu
    phi = phi_from_metric(g)
    aP1 = (a_of_phi(phi, k=k, p=p, eps0=eps0) + 1.0)           # (a+1)
    # phi_,mu  (spectral; d_t=0 static)
    dphi = torch.zeros(*phi.shape, 4, device=g.device)
    dphi[..., R] = G.d_r(phi); dphi[..., TH] = G.d_th(phi); dphi[..., PS] = G.d_ps(phi)
    exch = torch.zeros_like(divT)                              # -(a+1) phi_mu T^mu_nu
    for nu in range(4):
        s = torch.zeros_like(phi)
        for mu in range(4):
            s = s + dphi[..., mu] * Tmix[..., mu, nu]
        exch[..., nu] = -aP1 * s
    # welded: nabla_mu (W T^mu_nu) = W [ nabla_mu T^mu_nu + (a+1) phi_,mu T^mu_nu ]
    #   = W [ divT - exch ]   (since exch = -(a+1) phi.T)  -> should vanish in continuum
    welded = divT - exch
    return dict(divT=divT, exch=exch, welded=welded)
