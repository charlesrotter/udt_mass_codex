#!/usr/bin/env python3
"""
b1prime_3d_offround_residual.py -- the GENUINE 3-D OFF-ROUND residual of the DERIVED
two-player operator, with phi added as an independent 6th field, built on the existing
full3d_spectral / whole_metric_3d_core machinery.

Task: B1'-step1 (BUILD the off-round residual + VALIDATE it in the ROUND LIMIT by
EVALUATION).  Mode OBSERVE / INFRASTRUCTURE, DATA-BLIND.  NO 3-D Newton solve here
(that is the deferred gated push); validation is by EVALUATION + LINEAR perturbation.

OPERATOR (verbatim, derived upstream native_dilation_weight_derivation):
  S = INT sqrt(-g)[ e^{2phi} R + X e^{2phi} g^{ab} d_a phi d_b phi + e^{2phi} L_m ] dV,  f=e^{2phi}
  E^mu_nu = f G^mu_nu + (delta^mu_nu box f - nabla^mu nabla_nu f)
            - X f (nabla^mu phi nabla_nu phi - 1/2 delta^mu_nu (dphi)^2) - f T^mu_nu = 0
  phi-EOM = delta S / delta phi.
  kap8 = 1 (DERIVED matter coefficient).  L_m = native S^2 L2+L4 charge-1 hedgehog.
  Production X=-2e5, xi=kap=2e-2.

ROUTE A (covariant assembly) for the gravity sector.  Reasons: (1) the radial build
banked that autograd-THROUGH-Rscal carries spectral a'' edge noise; route A uses the
validated analytic einstein_mixed_weyl for G^mu_nu and builds the f-derivative terms
covariantly from the validated CORE.christoffel.  (2) the matter T^mu_nu reuses the
validated MAT.stress_tensor; the matter EL reuses the validated analytic matter_el_3d.
The phi EOM is assembled covariantly (the action's own delta S/delta phi).

phi ADDED as the 6th field: fields = (a,b,c,d,phi,Theta), all (Nr,Nth,Nps).  The
metric build is unchanged (phi does NOT enter g -- it is an independent player, exactly
as in the radial b1prime two-player reconstruction).  phi enters ONLY the operator
(the weight f=e^{2phi}, its covariant Hessian, the X-kinetic, and the e^{2phi} weight on
T and L_m).

ANTI-HANG: single process, sequential, NO Newton solve, evaluation + one linearization
only; grid capped Nr<=16, Nth<=8, Nps<=8.
"""
import os, sys, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
from full3d_spectral import (Grid3D, attach_coord_weight, build_metric, field_n,
                             field_dn, einstein_mixed, DEV)
from einstein_3d_eval import einstein_mixed_weyl

T, R, TH, PS = 0, 1, 2, 3
PI = math.pi


# ===========================================================================
# pack / unpack for the 6-field state (a,b,c,d,phi,Theta), each (Nr,Nth,Nps).
# ===========================================================================
def pack(a, b, c, d, phi, Th):
    return torch.stack([a, b, c, d, phi, Th], dim=0)   # (6,Nr,Nth,Nps)


def unpack(u):
    return u[0], u[1], u[2], u[3], u[4], u[5]


# ===========================================================================
# COVARIANT BUILDING BLOCKS (route A).
# We need, for f = e^{2phi}:
#   d_mu f                          (coord gradient, d_t=0)
#   box f = g^{mu nu} nabla_mu nabla_nu f = (1/sqrt-g) d_mu( sqrt-g g^{mu nu} d_nu f )
#   nabla_mu nabla_nu f = d_mu d_nu f - Gamma^a_{mu nu} d_a f   (covariant Hessian)
# all from the existing CORE.christoffel (reused) + spectral derivatives.
# ===========================================================================
def coord_grad(G, f):
    """d_mu f over the 4 coords (d_t=0).  Returns (...,4)."""
    z = torch.zeros_like(f)
    return torch.stack([z, G.d_r(f), G.d_th(f), G.d_ps(f)], dim=-1)


def coord_hess(G, f):
    """d_mu d_nu f (coordinate second derivatives, symmetric), (...,4,4).  d_t=0."""
    fr = G.d_r(f); ft = G.d_th(f); fp = G.d_ps(f)
    frr = G.d_r(fr); ftt = G.d_th(ft); fpp = G.d_ps(fp)
    frt = G.d_th(fr); frp = G.d_ps(fr); ftp = G.d_ps(ft)
    z = torch.zeros_like(f)
    H = torch.zeros(*f.shape, 4, 4, device=f.device)
    # row/col ordering (t,r,th,ps)
    H[..., R, R] = frr
    H[..., TH, TH] = ftt
    H[..., PS, PS] = fpp
    H[..., R, TH] = H[..., TH, R] = frt
    H[..., R, PS] = H[..., PS, R] = frp
    H[..., TH, PS] = H[..., PS, TH] = ftp
    return H


def christoffel_from_metric(G, g):
    """Gamma^a_{bc} for a general metric via spectral dg + CORE.christoffel (reused)."""
    ginv = CORE.metric_inverse(g)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for m in range(4):
        for n in range(4):
            comp = g[..., m, n]
            dg[..., R, m, n] = G.d_r(comp)
            dg[..., TH, m, n] = G.d_th(comp)
            dg[..., PS, m, n] = G.d_ps(comp)
    return CORE.christoffel(ginv, dg), ginv, dg


def cov_hessian_f(G, f, Gamma):
    """nabla_mu nabla_nu f = d_mu d_nu f - Gamma^a_{mu nu} d_a f.  (...,4,4)."""
    H = coord_hess(G, f)                       # d_mu d_nu f
    df = coord_grad(G, f)                       # d_a f
    # Gamma[...,a,b,c] = Gamma^a_{bc};  Gamma^a_{mu nu} d_a f
    corr = torch.einsum('...amn,...a->...mn', Gamma, df)
    return H - corr


def box_f_scalar(G, f, ginv, Gamma):
    """box f = g^{mu nu} nabla_mu nabla_nu f  (covariant scalar)."""
    covH = cov_hessian_f(G, f, Gamma)
    return torch.einsum('...mn,...mn->...', ginv, covH)


# ===========================================================================
# THE DERIVED OPERATOR -- mixed E^mu_nu (route A, covariant assembly).
# E^mu_nu = f G^mu_nu + (delta^mu_nu box f - (nabla nabla f)^mu_nu)
#           - X f ((dphi)^mu (dphi)_nu - 1/2 delta^mu_nu (dphi)^2) - f T^mu_nu
# with X-kinetic and matter weighted by f=e^{2phi}, kap8=1.
# ===========================================================================
def E_mixed(G, a, b, c, d, phi, dn, X, xi, kap, m=1, kap8=1.0,
            e_rt=None, e_rp=None, e_tp=None, return_parts=False):
    # MATTER decoupled (2026-06-25 native-S^2 wiring): the matter enters ONLY via its derivative
    # tensor dn (...,4,3) -- the operator no longer knows the matter PARAMETRIZATION (the imported
    # S^3 field_n/field_dn left the operator; dn is built natively in the residual via the grid-exact
    # 3-component carrier).  Vacuum = dn=0.  (m kept unused for caller compat; winding lives in dn.)
    # OFF-DIAGONAL completion (2026-06-25, gate #7): when e_rt/e_rp/e_tp are live the metric is the
    # FULL off-round metric and the dilaton/kinetic/matter sectors see it.  Gravity = the pole-stable
    # diagonal Weyl backbone + the general-Einstein OFF-DIAGONAL BRACKET (einstein_mixed(g_full) -
    # einstein_mixed(g_diag)) -- the validated einstein_general_hybrid pattern.  e_*=None/0 =>
    # g_full == g_diag => bracket == 0 AND ginv diagonal => E reduces EXACTLY to the diagonal derived
    # operator (regression lock).
    z = torch.zeros_like(a)
    e_rt = z if e_rt is None else e_rt
    e_rp = z if e_rp is None else e_rp
    e_tp = z if e_tp is None else e_tp
    g = build_metric(G, a, b, c, d, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)   # g_full
    # gravity G^mu_nu : pole-stable diagonal Weyl backbone + off-diagonal bracket (0 when e=0)
    Gmix = einstein_mixed_weyl(G, a, b, c, d)               # (...,4,4) diagonal analytic backbone
    g_diag = build_metric(G, a, b, c, d)
    Ggen_full, _, _, _ = einstein_mixed(G, g)
    Ggen_diag, _, _, _ = einstein_mixed(G, g_diag)
    Gmix = Gmix + (Ggen_full - Ggen_diag)                  # off-diagonal contribution
    Gamma, ginv, dg = christoffel_from_metric(G, g)        # f-terms/kinetic/matter see g_full
    f = torch.exp(torch.clamp(2*phi, max=60.0))
    # f-derivative terms ------------------------------------------------------
    boxf = box_f_scalar(G, f, ginv, Gamma)                  # scalar box f
    covHf = cov_hessian_f(G, f, Gamma)                      # nabla_mu nabla_nu f (low)
    covHf_mix = torch.einsum('...ma,...an->...mn', ginv, covHf)  # (nabla nabla f)^mu_nu
    delta = torch.eye(4, device=g.device).expand(*f.shape, 4, 4)
    fterm = delta * boxf[..., None, None] - covHf_mix       # delta box f - (nabla nabla f)
    # X-kinetic phi term ------------------------------------------------------
    dphi = coord_grad(G, phi)                               # d_mu phi (low)
    dphi_up = torch.einsum('...ma,...a->...m', ginv, dphi)  # nabla^mu phi
    dphi2 = torch.einsum('...m,...m->...', dphi_up, dphi)   # (dphi)^2
    # (nabla^mu phi nabla_nu phi)  mixed = dphi_up[mu] * dphi[nu]
    kin_mix = torch.einsum('...m,...n->...mn', dphi_up, dphi)
    kinterm = -X * f[..., None, None] * (kin_mix - 0.5*delta*dphi2[..., None, None])
    # matter T^mu_nu (validated Hilbert stress, xi=kap production regime; dn passed in) -------
    Tab, Lscal, L2, L4 = MAT.stress_tensor(g, ginv, dn, xi, kap)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)    # T^mu_nu
    # ASSEMBLE  E^mu_nu = f G + fterm + kinterm - kap8 f T --------------------
    E = (f[..., None, None] * Gmix + fterm + kinterm
         - kap8 * f[..., None, None] * Tmix)
    if return_parts:
        return dict(E=E, g=g, ginv=ginv, Gmix=Gmix, Tmix=Tmix, f=f, boxf=boxf,
                    covHf_mix=covHf_mix, fterm=fterm, kinterm=kinterm,
                    dphi2=dphi2, Lscal=Lscal, Gamma=Gamma)
    return E


# ===========================================================================
# phi EOM (the action's own delta S/delta phi), assembled covariantly.
#   delta/delta phi [ sqrt-g (f R + X f (dphi)^2 + f L_m) ] / sqrt-g
#   = f'(phi)[ R + X (dphi)^2 + L_m ]  - 2 X (1/sqrt-g) d_mu( sqrt-g f g^{mu nu} d_nu phi )
#   with f'(phi) = 2 e^{2phi}.
# (kinetic term:  X f g^{mn} d_m phi d_n phi  ->  f' X (dphi)^2 - 2 X div(f grad phi).)
# kap8 carried on the matter weight (matter enters as f L_m at coeff kap8=1).
# ===========================================================================
def EL_phi_3d(G, a, b, c, d, phi, dn, X, xi, kap, m=1, kap8=1.0,
              e_rt=None, e_rp=None, e_tp=None):
    # matter (L_m) enters via dn (...,4,3); operator parametrization-agnostic (native-S^2 wiring).
    # OFF-DIAGONAL completion (2026-06-25): the phi-EOM sees the FULL metric so the dilaton
    # sector is consistent with the off-diagonal Einstein rows.  e_*=0 => g_full==g_diag =>
    # identical to the diagonal phi-EL (regression lock).
    z = torch.zeros_like(a)
    e_rt = z if e_rt is None else e_rt
    e_rp = z if e_rp is None else e_rp
    e_tp = z if e_tp is None else e_tp
    g = build_metric(G, a, b, c, d, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)   # g_full
    Gamma, ginv, dg = christoffel_from_metric(G, g)
    f = torch.exp(torch.clamp(2*phi, max=60.0))
    fp = 2.0 * f                                            # f'(phi) = 2 e^{2phi}
    # Ricci scalar R from the ANALYTIC pole-stable Weyl mixed Einstein:  R = -G^mu_mu.
    # (Route-A gravity source.  CHOSE this over CORE.einstein's double-spectral-of-Gamma
    #  Rscal, which carries the documented O(N^2) edge noise and does NOT converge --
    #  verified: trace route matches analytic round R to 2.7e-15, CORE route to ~80.
    #  This is the radial build's "prefer analytic for the gravity part" lesson, off-round.)
    Gmix_w = einstein_mixed_weyl(G, a, b, c, d)
    Rscal = -torch.einsum('...mm->...', Gmix_w)
    # off-diagonal correction to R (hybrid bracket; identically 0 when e_*=0)
    g_diag = build_metric(G, a, b, c, d)
    Rgen_full, _, _, _ = einstein_mixed(G, g)
    Rgen_diag, _, _, _ = einstein_mixed(G, g_diag)
    Rscal = Rscal - torch.einsum('...mm->...', Rgen_full - Rgen_diag)
    # (dphi)^2
    dphi = coord_grad(G, phi)
    dphi_up = torch.einsum('...ma,...a->...m', ginv, dphi)
    dphi2 = torch.einsum('...m,...m->...', dphi_up, dphi)
    # matter L_m (xi=kap production)
    Gmn = MAT.field_metric(dn)
    Lm, _, _, _ = MAT.lagrangian(ginv, Gmn, xi, kap)
    # algebraic piece:  f'(R + X (dphi)^2 + kap8 L_m)
    alg = fp * (Rscal + X * dphi2 + kap8 * Lm)
    # divergence piece:  -2 X (1/sqrt-g) d_mu( sqrt-g f g^{mu nu} d_nu phi )
    # PRODUCT-RULE EXPANDED (CHOSE, load-bearing): the flux-then-spectral-differentiate
    # form  d_mu(sqrt-g f g^{mu nu} phi_nu)  nests TWO spectral d's on the PRODUCT of a
    # steep metric factor with phi_nu, which amplifies O(N^2) core noise ~7x (verified:
    # flux form gives -2X*div~83 vs the product-rule/analytic ~11.5 on the round soliton;
    # the radial banked solver uses the expanded form).  Expand by the product rule so the
    # only nested-d is the CLEAN scalar Hessian d_mu d_nu phi:
    #   div = f g^{mu nu} (d_mu d_nu phi) + g^{mu nu} (d_mu f)(d_nu phi)
    #         + f (1/sqrt-g) d_mu(sqrt-g g^{mu nu}) phi_nu
    # The last (metric-connection) factor is differentiated WITHOUT phi_nu inside, so no
    # steep-times-derivative product is spectrally re-differentiated.
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    Hphi = coord_hess(G, phi)                               # d_mu d_nu phi (...,4,4)
    df = coord_grad(G, f)                                   # d_mu f
    term_hess = f * torch.einsum('...mn,...mn->...', ginv, Hphi)   # f g^{mn} phi_mn
    term_fdphi = torch.einsum('...mn,...m,...n->...', ginv, df, dphi)  # g^{mn} f_m phi_n
    # connection term: (1/sqrt-g) d_mu(sqrt-g g^{mu nu}) contracted with phi_nu
    conn = torch.zeros_like(f)
    SGgup = sqrtg[..., None, None] * ginv                   # sqrt-g g^{mu nu}
    for mu in range(1, 4):
        for nu in range(1, 4):
            comp = SGgup[..., mu, nu]
            if mu == R:
                dcomp = G.d_r(comp)
            elif mu == TH:
                dcomp = G.d_th(comp)
            else:
                dcomp = G.d_ps(comp)
            conn = conn + dcomp * dphi[..., nu]
    conn = f * conn / torch.clamp(sqrtg, min=1e-30)
    div = term_hess + term_fdphi + conn
    return alg - 2.0 * X * div


# ===========================================================================
# matter Theta EL : reuse the validated analytic 3-D matter EL, but include the
# e^{2phi} weight.  The action's Theta-variation is delta/delta Theta [ f L_m ] =
# f * (delta L_m / delta Theta) since f is Theta-independent.  The analytic
# matter_el_3d is delta(L2+L4)/delta Theta at unit (xi,kap)=(1,1) coefficients
# scaled below; here we recompute via autograd of (f * sqrt-g * L_m) for exactness
# with the production xi,kap and the f weight.
# ===========================================================================
def EL_Th_3d(G, a, b, c, d, phi, Th, X, xi, kap, m=1, kap8=1.0,
             e_rt=None, e_rp=None, e_tp=None):
    z = torch.zeros_like(a)
    e_rt = z if e_rt is None else e_rt
    e_rp = z if e_rp is None else e_rp
    e_tp = z if e_tp is None else e_tp
    g = build_metric(G, a, b, c, d, e_rt=e_rt, e_rp=e_rp, e_tp=e_tp)   # g_full
    ginv = CORE.metric_inverse(g)
    f = torch.exp(torch.clamp(2*phi, max=60.0))
    Th_ = Th.detach().clone().requires_grad_(True)
    dn = field_dn(G, Th_, m=m)
    Gmn = MAT.field_metric(dn)
    Lm, _, _, _ = MAT.lagrangian(ginv.detach(), Gmn, xi, kap)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g.detach()), min=1e-30))
    S = (f.detach() * sqrtg * Lm * G.wvol_coord).sum()
    gradTh, = torch.autograd.grad(S, Th_, create_graph=False)
    meas = f.detach() * sqrtg * G.wvol_coord
    return kap8 * gradTh / torch.clamp(meas, min=1e-30)


# ===========================================================================
# FULL 6-field residual stack (for evaluation / linearization).  Well-posed
# selection mirrors the radial b1prime: E^t_t -> b, E^r_r -> a, and the two
# off-round/angular metric eqs E^th_th, E^ps_ps -> c, d; phi-EL -> phi;
# Theta-EL -> Theta.  (BC rows are added by the CALLER for any solve; here the
# bare interior residual is what we evaluate / linearize.)
# ===========================================================================
def residual_full(G, u, X, xi, kap, m=1, kap8=1.0):
    # LEGACY 6-field eval helper (S^3 Th-profile): computes its own dn so it still works against the
    # dn-decoupled operator.  The LIVE path (p1) uses the native-S^2 3-component dn instead.
    a, b, c, d, phi, Th = unpack(u)
    dn = field_dn(G, Th, m=m)
    E = E_mixed(G, a, b, c, d, phi, dn, X, xi, kap, m=m, kap8=kap8)
    elphi = EL_phi_3d(G, a, b, c, d, phi, dn, X, xi, kap, m=m, kap8=kap8)
    elTh = EL_Th_3d(G, a, b, c, d, phi, Th, X, xi, kap, m=m, kap8=kap8)
    return dict(E=E, elphi=elphi, elTh=elTh)
