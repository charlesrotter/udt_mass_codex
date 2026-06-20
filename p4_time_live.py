#!/usr/bin/env python3
"""
p4_time_live.py -- PHASE 4 of the everything-on solver build: TURN ON THE LIVE TIME ROW.

GOAL (EVERYTHING_ON_SOLVER_BUILD_MAP.md S III, P4):  the kernel
whole_metric_3d_core has a dg[...,T,...] (time) slot that EXISTS but is ZEROED by
every caller (full3d_spectral.einstein_mixed builds dg with only R/TH/PS filled;
einstein_3d_eval.einstein_mixed_weyl is purely static/diagonal).  P4 supplies
d_T g != 0 to the kernel and brings the MATTER profile's time-dependence live, so
that T_tr != 0 can source G_tr (escapes Birkhoff -> unfreezes time), per phase0 +
native_matter_timelive_probe.

METHOD = OPEN-TIME HARMONIC BALANCE (phase0 (C), DERIVED-from-kernel):
  every field carries a single live harmonic about its static profile,
     u(t,r,..) = u0(r,..) + u1(r,..) * cos(omega t)          (open time; omega FREE)
  so  d_t u  = -omega u1 sin(omega t)    (algebraic in omega)
      d_t^2 u = -omega^2 u1 cos(omega t) (algebraic in omega)  ->  d_t^2 -> -omega^2 on u1.
  The kernel's time slot dg[...,T,...]=d_t g and the SECOND time content dGamma[...,T,..]
  =d_t Gamma are supplied ANALYTICALLY from these (d_dx is spatial-only -- phase0 (C)4),
  evaluated at a representative phase.  omega -> 0  =>  d_t g -> 0  =>  STATIC kernel
  recovered EXACTLY (CONTAINMENT, the binding P4b check).

  OPEN TIME ONLY.  NO closed-time import (a dropped object -- prompt discipline).

WHAT STAYS / WHAT TURNS ON (audited, declared):
  * a(phi) = -1 (GR) baseline (P3 ruler weight at k=0 -> W==1).  a(phi)!=-1 is NOT P4.
  * native S^2 unit-3-vector carrier (P2).  NO Skyrme BC, NO B=1/A injection (a,b free).
  * the time row (this phase): metric time-amplitudes a1,b1 + matter time-amplitude F1,
    + omega + its closure (the harmonic-balanced t-row residual rows).
  * off-diagonals: available via the P1 hybrid; the TRACTABLE channel P4 OBSERVES is the
    round/near-round time-live one (#65 says it is tractable).  The FULL off-round +
    time-live coupled Newton is the P5 throughput wall -- reported as such, not a verdict.

REPO DISCIPLINE: committed scripts IMMUTABLE.  NEW file; imports clean primitives
(whole_metric_3d_core kernel, whole_metric_3d_matter, full3d_spectral, p2/p3 stack).
Branch p4-time-live.  DATA-BLIND (units L=1; no wall numbers).  OBSERVE, not target.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV, T, R, TH, PS
from einstein_3d_eval import einstein_mixed_weyl  # noqa: F401 (used via F3.einstein_mixed_weyl)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2
import p3fix_aphi_ruler as P3F   # ruler weight (k=0 -> W==1 = GR baseline)


# ===========================================================================
# THE LIVE-TIME METRIC (single open-time harmonic).  At a representative phase
# we set cos(omega t)=CPH, sin(omega t)=SPH.  The static limit is CPH->1, SPH->0
# with omega=0 (so d_t g = 0).  The metric VALUE at the phase:
#     a(t) = a0 + a1*CPH ,  b(t) = b0 + b1*CPH , ...
# Its time derivatives (ANALYTIC, algebraic in omega -- the kernel cannot make them):
#     d_t a   = -omega a1 SPH
#     d_t^2 a = -omega^2 a1 CPH
# We carry the diagonal warps a,b (round time-live channel; c=d=0 round) + matter.
# ===========================================================================
def build_metric_live(G, a0, b0, a1, b1, omega, cph, sph,
                      c0=None, d0=None):
    """Metric VALUE g and its time partials dt_g (d_t g), dtt_g (d_t^2 g) at the phase.
    Diagonal Weyl class (round channel): g_tt=-e^{2a}, g_rr=e^{2b}, g_thth=e^{2c}r^2,
    g_psps=e^{2d}r^2 sin^2.  c=d=0 (round) unless supplied.  All algebraic in omega."""
    if c0 is None: c0 = torch.zeros_like(a0)
    if d0 is None: d0 = torch.zeros_like(a0)
    a = a0 + a1 * cph
    b = b0 + b1 * cph
    c = c0
    d = d0
    g = build_metric(G, a, b, c, d)                       # VALUE at the phase

    # time partials of the warps (analytic, algebraic in omega)
    at = -omega * a1 * sph;  att = -omega**2 * a1 * cph
    bt = -omega * b1 * sph;  btt = -omega**2 * b1 * cph
    # time partials of the metric components via chain rule on e^{2*}:
    #   g_tt = -e^{2a}  => d_t g_tt = -2 a_t e^{2a};  d_t^2 = -(2 a_tt + 4 a_t^2) e^{2a}
    #   g_rr =  e^{2b}  => d_t g_rr =  2 b_t e^{2b};  d_t^2 =  (2 b_tt + 4 b_t^2) e^{2b}
    r, sth = G.Rg, G.STHg
    e2a = torch.exp(2*a); e2b = torch.exp(2*b)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dt_g  = torch.zeros(Nr, Nth, Nps, 4, 4, device=a.device)
    dtt_g = torch.zeros(Nr, Nth, Nps, 4, 4, device=a.device)
    dt_g[..., T, T]  = -2*at*e2a
    dtt_g[..., T, T] = -(2*att + 4*at*at)*e2a
    dt_g[..., R, R]  =  2*bt*e2b
    dtt_g[..., R, R] =  (2*btt + 4*bt*bt)*e2b
    # c=d=0 round => g_thth, g_psps time-static (no time amplitude on them this channel)
    return g, dt_g, dtt_g, a, b


# ===========================================================================
# THE LIVE-TIME EINSTEIN (the WIRED time row) -- POLE-STABLE HYBRID.
#
# *** CONDITIONING REALITY (found this session; same as P1's header, load-bearing) ***
# The RAW CORE-kernel general Einstein (double spectral pass on the Christoffels) is
# BADLY conditioned on the steep soliton warps near the Cheb core edge: on the
# converged round-S^2 soliton it gives G^t_t~16, G^r_r~33 vs the analytic pole-stable
# Weyl ~0.28 -- a NUMERICAL artifact, not physics.  Routing the diagonal/spatial rows
# through the raw kernel would corrupt them and break omega=0 containment (a FALSE
# "P4 failed" that is really conditioning).  So, EXACTLY as P1 does for the off-
# diagonal rows, the diagonal/spatial backbone comes from the analytic pole-stable
# einstein_mixed_weyl, and the kernel supplies ONLY the TIME-ROW DELTA:
#
#   G_live = G_weyl(a,b,c=0,d=0)  +  [ einstein_live_kernel(time ON) - einstein_live_kernel(time OFF) ]
#
# Both kernel evals share the SAME steep diagonal background, so the dominant core-
# conditioning error SUBTRACTS OUT in the bracket (the time delta is O(omega), well-
# conditioned), while the genuine live-time content survives.  At omega=0 the bracket
# is IDENTICALLY ZERO -> G_live == G_weyl EXACTLY -> the static round soliton is
# provably unchanged (CONTAINMENT by construction).  The field equations are UNCHANGED
# (same general 4x4 Einstein); only the EVALUATION is pole-stable (category-A).
#
# einstein_live_kernel below is the literal CORE kernel with the live t-row wired:
#   dg[...,t,..] <- dt_g ; dGamma[...,t,..] <- analytic d_t Gamma (phase0 (C): d_dx is
#   spatial-only, so the time content MUST be supplied analytically from harmonic balance).
# omega->0 => dt_g=0,dtt_g=0 => dGamma[t]=0,dg[t]=0 => the kernel's STATIC value (which
# cancels in the bracket regardless of conditioning).
# ===========================================================================
def einstein_live_kernel(G, g, dt_g, dtt_g):
    """The literal CORE-kernel general 4x4 Einstein with the live t-row wired.  Used
    INSIDE the pole-stable hybrid as a DELTA (time ON minus time OFF); not called
    directly for the diagonal rows (it is core-edge ill-conditioned on steep warps)."""
    ginv = CORE.metric_inverse(g)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    # ---- dg: spatial spectral slots + LIVE time slot ----
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for m in range(4):
        for n in range(4):
            comp = g[..., m, n]
            dg[..., R, m, n]  = G.d_r(comp)
            dg[..., TH, m, n] = G.d_th(comp)
            dg[..., PS, m, n] = G.d_ps(comp)
            dg[..., T, m, n]  = dt_g[..., m, n]          # <-- THE LIVE TIME ROW
    Gamma = CORE.christoffel(ginv, dg)                    # Gamma^a_{bc}

    # ---- dGamma: spatial spectral slots + LIVE time slot (analytic) ----
    dGamma = torch.zeros(Nr, Nth, Nps, 4, 4, 4, 4, device=g.device)
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                comp = Gamma[..., a_, b_, c_]
                dGamma[..., R, a_, b_, c_]  = G.d_r(comp)
                dGamma[..., TH, a_, b_, c_] = G.d_th(comp)
                dGamma[..., PS, a_, b_, c_] = G.d_ps(comp)

    # d_t Gamma analytically.  Need d_t(dg): the [k,m,n] tensor d_t(d_k g).
    #   k=t slot: d_t(d_t g) = dtt_g
    #   k=spatial: d_t(d_x g) = d_x(d_t g)  (mixed partials commute) -> spectral d_x of dt_g
    dt_dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for m in range(4):
        for n in range(4):
            comp_t = dt_g[..., m, n]
            dt_dg[..., R, m, n]  = G.d_r(comp_t)
            dt_dg[..., TH, m, n] = G.d_th(comp_t)
            dt_dg[..., PS, m, n] = G.d_ps(comp_t)
            dt_dg[..., T, m, n]  = dtt_g[..., m, n]
    # d_t ginv = -ginv (d_t g) ginv
    dt_ginv = -torch.einsum('...ab,...bc,...cd->...ad', ginv, dt_g, ginv)
    # Tterm[...,d,b,c] = dg[...,b,d,c] + dg[...,c,d,b] - dg[...,d,b,c]  (kernel's form)
    def Tterm_of(DG):
        A  = torch.einsum('...bdc->...dbc', DG)
        Bp = torch.einsum('...cdb->...dbc', DG)
        Cp = DG
        return A + Bp - Cp
    Tterm    = Tterm_of(dg)
    dt_Tterm = Tterm_of(dt_dg)
    # Gamma = 1/2 ginv Tterm ;  d_t Gamma = 1/2[ dt_ginv Tterm + ginv dt_Tterm ]
    dGamma[..., T, :, :, :] = 0.5*(torch.einsum('...ad,...dbc->...abc', dt_ginv, Tterm)
                                   + torch.einsum('...ad,...dbc->...abc', ginv, dt_Tterm))

    Gmn, Ric, Rscal = CORE.einstein(g, ginv, Gamma, dGamma)
    Gmix = torch.einsum('...ma,...an->...mn', ginv, Gmn)
    return Gmix, Gmn, ginv, Gamma


def einstein_live(G, a, b, dt_g, dtt_g, c=None, d=None, g=None):
    """POLE-STABLE HYBRID mixed Einstein with the LIVE time row.
       G_live = G_weyl(a,b,c,d)  +  [ kernel(time ON) - kernel(time OFF) ]
    The bracket is the TIME-ROW DELTA (well-conditioned, O(omega)); the diagonal/
    spatial backbone is the analytic pole-stable Weyl.  omega=0 => dt_g=dtt_g=0 =>
    bracket==0 => G_live == G_weyl EXACTLY (containment by construction).
    g (the metric VALUE at the phase) is required for the kernel evals + matter."""
    if c is None: c = torch.zeros_like(a)
    if d is None: d = torch.zeros_like(a)
    if g is None: g = build_metric(G, a, b, c, d)
    zer = torch.zeros_like(dt_g)
    Gon,  _, ginv, _ = einstein_live_kernel(G, g, dt_g, dtt_g)   # time ON
    Goff, _, _,    _ = einstein_live_kernel(G, g, zer, zer)      # time OFF (same g)
    delta = Gon - Goff                                            # the live-time content
    Gweyl = F3.einstein_mixed_weyl(G, a, b, c, d)                # pole-stable backbone
    return Gweyl + delta, ginv


# ===========================================================================
# THE LIVE-TIME NATIVE S^2 MATTER.  F(t,r,..) = F0 + F1*cos(omega t).  The native
# unit 3-vector n = (sinF cos mps, sinF sin mps, cosF) is built at the phase; its
# time partial d_t n carries the live d_t F (so dn[...,T,:] != 0 -> T_tr != 0).
# This is the native_matter_timelive_probe object in the production stack.
# ===========================================================================
def field_dn_s2_live(G, F0, F1, omega, cph, sph, m=1):
    """dn[...,k,a] with the LIVE time slot k=T populated by d_t F = -omega F1 sin(wt).
    Spatial slots = P2.field_dn_s2 chain rule on the phase value F = F0 + F1 cph."""
    F = F0 + F1 * cph
    dn = P2.field_dn_s2(G, F, m=m)                        # spatial slots (T slot = 0 here)
    # analytic d_t n = (dn/dF) * d_t F ; d_t F = -omega F1 sph
    sF, cF = torch.sin(F), torch.cos(F)
    mps = m * G.PSg
    sps, cps = torch.sin(mps), torch.cos(mps)
    nF = torch.stack([cF*cps, cF*sps, -sF], dim=-1)       # dn/dF (3-vector)
    Ft = -omega * F1 * sph                                # d_t F (algebraic in omega)
    dn[..., T, :] = Ft[..., None] * nF                    # <-- THE LIVE MATTER TIME ROW
    return dn, F


def stress_live(G, g, ginv, dn, k=0.0, p=1.0, eps0=1.0):
    """Native S^2 L2+L4 Hilbert stress on the live dn (carries d_t n), ruler-weighted
    (k=0 -> W==1 = GR baseline).  Returns T_{ab} INCLUDING the off-diagonal T_tr the
    live time row sources."""
    Tab, L, L2, L4 = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    phi = P3F.P3.phi_from_metric(g)
    W = P3F.weight_W_ruler(phi, k=k, p=p, eps0=eps0)
    return Tab * W[..., None, None], L, W


# ===========================================================================
# <T_tr> ANCHOR (P4b physical justification, in THIS stack).  The l=0 angular
# average of T_tr; nonzero => sources the G_tr momentum constraint => escapes
# Birkhoff => unfreezes time (native_matter_timelive_probe, in production).
# ===========================================================================
def T_tr_anchor(G, g, ginv, dn):
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    T_tr = Tab[..., T, R]                                 # lowered T_{tr}
    dOm = (G.wmu[None, :, None] * G.wps[None, None, :])
    l0 = (T_tr * dOm).sum(dim=(1, 2)) / (4*PI)            # <T_tr>_{l=0}(r)
    return T_tr, l0


# ===========================================================================
# THE M_MS READOUT (same operator as the static anchor, on the live config's rho).
# ===========================================================================
def M_MS_of(G, g, ginv, Tab, kap8):
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    rho = -Tmix[..., T, T]
    dOm = (G.wmu[None, :, None] * G.wps[None, None, :])
    rho_ang = (rho * dOm).sum(dim=(1, 2)) / (4*PI)
    integ = kap8 * G.r**2 * rho_ang
    r = G.r; M = torch.zeros_like(r)
    for i in range(1, len(r)):
        M[i] = M[i-1] + 0.5*(integ[i]+integ[i-1])*(r[i]-r[i-1])
    return float(M[-1] - M[0])
