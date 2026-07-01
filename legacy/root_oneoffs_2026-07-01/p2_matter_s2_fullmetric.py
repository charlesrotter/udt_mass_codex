#!/usr/bin/env python3
"""
p2_matter_s2_fullmetric.py -- PHASE 2 of the everything-on solver build.

GOAL (EVERYTHING_ON_SOLVER_P2_MAP.md): make the native matter Euler-Lagrange
equation (a) live in full 3-D -- a FREE profile F(r,theta,psi), not just F(r) -- and
(b) VARY ON THE FULL OFF-DIAGONAL-AWARE METRIC P1 turned on.  Today (P1) the matter EL
(full3d_spectral.matter_el_3d / matter_el_3d_gen.py) is varied on the DIAGONAL metric
only -- it is BLIND to e_rt,e_rp,e_tp.  P2 closes that gap, on the NATIVE S^2 carrier.

Driver: Claude (Opus 4.8, 1M).  2026-06-19/20.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).

REPO DISCIPLINE: committed scripts are IMMUTABLE.  NEW file; imports clean primitives.

=== THE CARRIER (settled BEFORE P2; s2_s3_identity_results.md + _VERIFIER.md) ===
The native matter object is the **S^2 UNIT 3-vector** (NOT S^3/Skyrme, which is the
import #61).  The genuine UNIT, texture-free S^2 field with a radial profile is the
TARGET-POLAR-ANGLE hedgehog:

    n = ( sin F * cos(m psi),  sin F * sin(m psi),  cos F ),   |n|^2 = 1 EXACTLY for any F.

  * F = F(r,theta,psi) is the SINGLE FREE PROFILE (the 3-D generalization of Theta(r)).
  * |n|=1 for ANY F (verified) -- this is the genuine UNIT embedding.  Contrast the
    superseded `(sinTheta*sinth*cos mps, sinTheta*sinth*sin mps, cosTheta)` form used in
    the committed S^2 derive / the S^3 4-vector field_n: that one is NON-UNIT
    (|n|^2 = 1 - sin^2(Theta) cos^2(theta) != 1 off the equator) -- the "texture
    artifact" the carrier settle (results.md S3) identified.  The genuine unit hedgehog
    with F=theta is exactly n=x/r (texture-free, T^t_t=T^r_r); a radial profile is
    carried by letting F run (F=pi node at the core, F=0 node at the seal for deg-1).
  * NATIVE L4 = cross-product (eps_abc) form.  For a 3-vector this EQUALS the
    Lagrange-identity L4 (Part 1 of the settle; re-verified machine-0 here), so
    MAT.lagrangian / MAT.stress_tensor are the CORRECT native S^2 objects when given
    the 3-component field gradient dn (...,4,3).  NO S^3 4th component.

=== THE EL: AUTOGRAD ON THE FULL METRIC (the P2 closure) ===
The matter EL = delta S_matter / delta F(node), S_matter = int sqrt(-g)(L2+L4) d^4x,
computed by torch.autograd of the discrete proper-volume-weighted action wrt the nodal
F.  CRUCIAL: the action uses ginv from the FULL off-diagonal metric g_full -- so the EL
genuinely VARIES ON THE OFF-DIAGONALS.  This is the literal Euler-Lagrange variation of
the SAME action that builds the Hilbert stress (MAT.stress_tensor on the same g_full),
so the EL and stress are consistent BY CONSTRUCTION -> the divT identity (nabla_mu T^mu_nu
= -EL d_nu F) holds to the spectral floor.  Autograd is exact (machine precision), not a
codegen; it sees every metric component the Lagrangian density contains.

=== CORE BC (NO Skyrme) ===
The ONLY core condition is the native regularity NODE sin F(0)=0 (value free); the deg-1
homotopy sector pins the pi node at the core (F[core]=pi -> F[seal]=0).  pi is a NODE
value (sin pi = 0), NOT the forbidden m*pi LADDER (m is not a free index; we solve only
the charge-1 sector).  Grep this file: the only m*PI is the labelled negative control.

=== SCOPE / FREEZES (declared) ===
a(phi) = -1 (GR baseline) -- a(phi) is P3, NOT touched.  Time row ZEROED -- P4.
B=1/A FREE (a,b independent, never injected).  Off-diagonals e_rt,e_rp,e_tp LIVE.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    einstein_mixed, einstein_mixed_weyl, DEV, PI, T, R, TH, PS)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
from full3d_newton import inv4x4, det4x4


# ===========================================================================
# THE NATIVE S^2 UNIT 3-VECTOR FIELD.  n = (sinF cos mps, sinF sin mps, cosF),
# |n|=1 for any F.  F = F(r,theta,psi) FREE.  THREE target components (no n_4).
# ===========================================================================
def field_n_s2(G, F, m=1):
    sF, cF = torch.sin(F), torch.cos(F)
    mps = m * G.PSg
    return torch.stack([sF*torch.cos(mps), sF*torch.sin(mps), cF], dim=-1)  # (...,3)


def field_dn_s2(G, F, m=1):
    """dn[...,k,a] = d_k n_a, k over (t,r,th,ps) (d_t=0), a over the 3 target comps,
    via the EXACT CHAIN RULE.  n depends on F(r,th,ps) AND explicitly on psi (via m psi).
    Spectral differentiation is global (does not obey the pointwise chain rule on the
    nonlinear sin/cos of F), so we take SPECTRAL derivatives of the SMOOTH profile F only
    and combine with the ANALYTIC partials of n -- exact (same pattern as the committed
    field_dn, adapted to the genuine UNIT S^2 field)."""
    sF, cF = torch.sin(F), torch.cos(F)
    mps = m * G.PSg
    sps, cps = torch.sin(mps), torch.cos(mps)
    # spectral partials of the smooth profile F
    F_r = G.d_r(F); F_t = G.d_th(F); F_p = G.d_ps(F)
    # dn/dF (analytic)
    nF = torch.stack([cF*cps, cF*sps, -sF], dim=-1)
    # explicit psi partial of n at fixed F (winding m); explicit theta partial = 0
    n_ps_exp = torch.stack([-m*sF*sps, m*sF*cps, torch.zeros_like(sF)], dim=-1)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 3, device=F.device)
    dn[..., R, :] = F_r[..., None]*nF
    dn[..., TH, :] = F_t[..., None]*nF                 # no explicit theta dependence
    dn[..., PS, :] = F_p[..., None]*nF + n_ps_exp
    return dn


# ===========================================================================
# NATIVE S^2 STRESS on the FULL metric.  Reuse MAT.stress_tensor with the
# 3-component dn (verified: Lagrange-identity L4 == native cross-product L4 on a
# 3-vector).  ginv MUST be from the FULL off-diagonal metric.  Returns T_{ab}.
# ===========================================================================
def stress_s2_fullmetric(g, ginv, dn, xi=1.0, kap=1.0):
    return MAT.stress_tensor(g, ginv, dn, xi, kap)     # (Tab, L, L2, L4)


# ===========================================================================
# THE MATTER ACTION (scalar) on the FULL metric.  S = sum_nodes sqrt(-g) L dV_coord.
# Uses ginv from the FULL metric -> the action (hence its variation, the EL) SEES the
# off-diagonals.  This is the P2 closure of the P1 gap.
# ===========================================================================
def matter_action_s2(G, g, ginv, F, m=1, xi=1.0, kap=1.0):
    dn = field_dn_s2(G, F, m=m)
    Gmn = MAT.field_metric(dn)
    L, L2, L4, SS = MAT.lagrangian(ginv, Gmn, xi, kap)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    S = (sqrtg * L * G.wvol_coord).sum()
    return S, L, dn, Gmn


# ===========================================================================
# THE NATIVE S^2 MATTER EL ON THE FULL METRIC -- by AUTOGRAD.
#  el(node) = (1/measure) delta S / delta F(node),  measure = sqrt(-g) dV_coord.
#  ginv from the FULL off-diagonal metric => the EL VARIES ON THE OFF-DIAGONALS.
#  Exact variation of the SAME action that builds the stress -> stress-consistent ->
#  the divT identity holds.  Works for ANY metric (diagonal or off-diagonal).
# ===========================================================================
def matter_el_s2_fullmetric(G, g, ginv, F, m=1, xi=1.0, kap=1.0):
    F_ = F.detach().clone().requires_grad_(True)
    dn = field_dn_s2(G, F_, m=m)
    Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv.detach(), Gmn, xi, kap)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g.detach()), min=1e-30))
    S = (sqrtg * L * G.wvol_coord).sum()
    gradF, = torch.autograd.grad(S, F_, create_graph=False)
    meas = sqrtg * G.wvol_coord
    el = gradF / torch.clamp(meas, min=1e-30)
    return el


# ===========================================================================
# COVARIANT divT FIELD on the FULL metric (the gate).  nabla_mu T^mu_nu, all nodes.
#   nabla_mu T^mu_nu = (1/sqrt|g|) d_mu(sqrt|g| T^mu_nu) - Gamma^l_{mu nu} T^mu_l
# Uses CORE.christoffel on the FULL metric + spectral derivatives.  (Same algebra as
# divT_excised.covariant_divT_field, but built directly from g,ginv,Tab for any metric,
# and using det4x4 for vmap/clean-allocator safety.)
# ===========================================================================
def covariant_divT_field(G, g, ginv, Tab):
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)   # T^mu_nu
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for mm in range(4):
        for nn in range(4):
            comp = g[..., mm, nn]
            dg[..., R, mm, nn] = G.d_r(comp)
            dg[..., TH, mm, nn] = G.d_th(comp)
            dg[..., PS, mm, nn] = G.d_ps(comp)
    Gamma = CORE.christoffel(ginv, dg)

    def d_mu(field, mu):
        if mu == R:  return G.d_r(field)
        if mu == TH: return G.d_th(field)
        if mu == PS: return G.d_ps(field)
        return torch.zeros_like(field)

    divT = torch.zeros(Nr, Nth, Nps, 4, device=g.device)
    for nu in range(4):
        term = torch.zeros(Nr, Nth, Nps, device=g.device)
        for mu in range(1, 4):                              # mu=t -> 0 (static)
            term = term + d_mu(sqrtg * Tmix[..., mu, nu], mu)
        term = term / torch.clamp(sqrtg, min=1e-30)
        for mu in range(4):
            for l in range(4):
                term = term - Gamma[..., l, mu, nu] * Tmix[..., mu, l]
        divT[..., nu] = term
    return divT


def interior_mask(G, r_margin=1.0, n_theta_edge=2):
    """Well-conditioned spectral interior (physical radial margin + polar excision).
    Same category-A excision divT_excised uses (edge rows carry differentiation-matrix
    noise, not physics).  psi periodic -> kept in full."""
    r = G.r
    rmask = (r > G.rc + r_margin) & (r < G.ri - r_margin)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    thmask = torch.zeros(Nth, dtype=torch.bool, device=G.dev)
    k = int(n_theta_edge)
    thmask[k:Nth - k] = True
    m = (rmask[:, None, None] & thmask[None, :, None]
         & torch.ones(Nps, dtype=torch.bool, device=G.dev)[None, None, :])
    return m
