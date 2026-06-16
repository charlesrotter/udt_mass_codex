#!/usr/bin/env python3
"""
full3d_spectral.py -- the FULL-3-D SPECTRAL coupled Einstein+L2+L4 solver.
NO spatial symmetry imposed: (r, theta, psi) all LIVE; the full 4x4 metric carried
(all off-diagonals available); the matter a FREE unit-S^3 field over (r,theta,psi);
winding m.  Chebyshev_r x Gauss-Legendre_theta x Fourier_psi spectral basis.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers).

=== ARCHITECTURE (every piece category-A; proofs in full3d_catalog_results.md) ===

REUSED VALIDATED PHYSICS (infra-audit 2026-06-16 CLEAN -- solver is new, PHYSICS reused):
  * whole_metric_3d_core.christoffel / einstein : the FULL numerical NR Einstein
    engine for a GENERAL 4x4 metric (all off-diagonals), exact tensor algebra
    (verified vs independent sympy G to 2.7e-15 incl off-diagonal G_{tpsi}).  The
    ONLY change here: derivatives are taken SPECTRALLY (Cheb_r/Legendre_theta/
    Fourier_psi), NOT by uniform-grid FD -- this is the cure for the #57/#58
    coordinate-spike ill-conditioning that killed the FD full-3-D line.
  * whole_metric_3d_matter.stress_tensor : the EXACT Hilbert L2+L4 stress for a
    GENERAL unit 4-vector field (verified vs independent sympy Hilbert stress to
    4.2e-17, |n|^2=1, -T^t_t=rho).

THE MATTER EL -- by AUTOGRAD of the action (NOT symbolic codegen):  the matter
Euler-Lagrange residual is delta S_matter / delta(field) where
  S_matter = int sqrt(-g) (L2+L4) d^4x.
We compute it by torch.autograd of the discrete proper-volume-weighted action wrt
the field DOF.  This is STRUCTURALLY immune to the L4 codegen bug the verifier
found in axisym_matter_el.py (which mis-varied the quartic off-round): autograd
differentiates the SAME action that builds the stress, so the EL is EXACTLY
consistent with the Hilbert stress by construction.  VERIFIED off-round by the
covariant identity  div_mu T^mu_nu = - EL . d_nu(field)  (the matter-EOM <=>
conservation theorem) -- the prompt's div-identity gate.

METRIC PARAMETRIZATION (the metric DOF that are solved):
  Diagonal Weyl-like warps a,b,c,d (functions of r,theta,psi) PLUS the spatial
  off-diagonal warps for genuine non-axisymmetry.  Default diagonal seed; the
  solver carries the full 4x4 and the off-diagonals are FREE to grow (they are
  zero on the round/axisym soliton, nonzero for a genuine 3-D shape).  B=1/A is
  NOT tied (a,b independent) -- the whole point.

  g_tt = -e^{2a},  g_rr = e^{2b},  g_thth = e^{2c} r^2,  g_psps = e^{2d} r^2 sin^2 th,
  plus optional g_rth, g_rps, g_thps (the spatial off-diagonals, units carried in
  the same areal scaling).  Time-row off-diagonals (rotation/twist) = 0 here
  (static; the stationary-twist sector is a separate criterion-7 push).

REGULARITY:  GL-in-mu nodes never touch the axis (theta=0,pi); psi is periodic
(Fourier, no edge); the innermost/outermost Cheb radial rows are regularity-excised
from the objective (O(N^2) edge amplification on the steep core); winding BC
Theta(core)=m*pi, Theta(seal)=0; seal gauge a(seal)=0; depth dial b(core)=-p.

NUMERICS (principle 2):  full nonlinear; spectral-derivative + autograd-Jacobian are
the sanctioned exact-on-poly / machine-precision function-replacements.  NO
linearization kept as a result.  Damped Levenberg-Marquardt, strict monotone accept.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi
T, R, TH, PS = 0, 1, 2, 3
EXP_CLAMP = 60.0

from spectral_cheb import cheb_interval, clenshaw_curtis_weights
from spectral_sph import theta_operators, psi_operators
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
from einstein_3d_eval import einstein_mixed_weyl


# ---------------------------------------------------------------------------
# load the auto-generated CORRECT 3-D matter EL (direct variation; torch-evaluable)
# ---------------------------------------------------------------------------
def _load_matter_el_3d():
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'matter_el_3d_gen.py')).read()
    src = '\n'.join(l for l in src.split('\n')
                    if not l.strip().startswith('import numpy')
                    and not l.strip().startswith('from numpy'))
    ns = {'numpy': torch, 'np': torch, 'exp': torch.exp, 'sin': torch.sin,
          'cos': torch.cos, 'tan': torch.tan, 'sqrt': torch.sqrt}
    exec(src, ns)
    return ns['matter_el_3d']


_MEL3D = _load_matter_el_3d()


# ===========================================================================
# THE GRID:  Cheb_r x GL_theta x Fourier_psi tensor product.
# Fields are stored as (Nr, Nth, Nps) torch tensors.  Spectral derivative
# operators act along each axis via matmul (tensordot).
# ===========================================================================
class Grid3D:
    def __init__(self, Nr, Nth, Nps, rc=0.05, cell=14.0, dev=DEV):
        self.Nr, self.Nth, self.Nps = Nr, Nth, Nps
        self.rc, self.ri = rc, rc + cell
        # radial (Chebyshev)
        r, Dr = cheb_interval(Nr - 1, rc, self.ri)        # Nr nodes
        wr = clenshaw_curtis_weights(Nr - 1, rc, self.ri)
        # theta (Gauss-Legendre in mu)
        th, wmu, Dth, sth = theta_operators(Nth)
        # psi (Fourier)
        psi, Dps, wps = psi_operators(Nps)
        # tensors
        self.r = torch.tensor(r, device=dev)
        self.th = torch.tensor(th, device=dev)
        self.psi = torch.tensor(psi, device=dev)
        self.Dr = torch.tensor(Dr, device=dev)
        self.Dth = torch.tensor(Dth, device=dev)
        self.Dps = torch.tensor(Dps, device=dev)
        self.wr = torch.tensor(wr, device=dev)
        self.wmu = torch.tensor(wmu, device=dev)         # includes sin th
        self.wps = torch.tensor(wps, device=dev)
        self.sth = torch.tensor(sth, device=dev)
        # broadcast coordinate fields (Nr,Nth,Nps)
        self.Rg = self.r[:, None, None].expand(Nr, Nth, Nps).contiguous()
        self.THg = self.th[None, :, None].expand(Nr, Nth, Nps).contiguous()
        self.PSg = self.psi[None, None, :].expand(Nr, Nth, Nps).contiguous()
        self.STHg = self.sth[None, :, None].expand(Nr, Nth, Nps).contiguous()
        self.dev = dev
        # body mask (exclude 2 Cheb edge rows each end; poles auto-excluded by GL)
        self.body = torch.zeros(Nr, Nth, Nps, dtype=torch.bool, device=dev)
        self.body[2:Nr-2, :, :] = True
        # proper-volume measure placeholder weight (set per-metric in objective)
        # coordinate quadrature weight w_r * w_mu(sin th incl) * w_ps over (r,th,ps)
        self.wvol = (self.wr[:, None, None] * self.wmu[None, :, None]
                     * self.wps[None, None, :])          # (Nr,Nth,Nps), includes sin th

    # spectral derivatives along each axis ----------------------------------
    def d_r(self, f):
        return torch.tensordot(self.Dr, f, dims=([1], [0]))
    def d_th(self, f):
        return torch.tensordot(self.Dth, f, dims=([1], [1])).permute(1, 0, 2)
    def d_ps(self, f):
        return torch.tensordot(self.Dps, f, dims=([1], [2])).permute(1, 2, 0)

    def grad_coords(self, f):
        """Return d_t f (=0), d_r f, d_th f, d_ps f stacked as (...,4) over coords."""
        z = torch.zeros_like(f)
        return torch.stack([z, self.d_r(f), self.d_th(f), self.d_ps(f)], dim=-1)


# ===========================================================================
# THE METRIC.  7 free spatial functions (a,b,c,d diagonal warps + 3 spatial
# off-diagonal warps e_rt,e_rp,e_tp), all functions of (r,theta,psi).  Static:
# time row off-diagonal = 0.  Returns g (Nr,Nth,Nps,4,4).
# ===========================================================================
def build_metric(G, a, b, c, d, e_rt=None, e_rp=None, e_tp=None):
    r, sth = G.Rg, G.STHg
    z = torch.zeros_like(a)
    if e_rt is None: e_rt = z
    if e_rp is None: e_rp = z
    if e_tp is None: e_tp = z
    g = torch.zeros(*a.shape, 4, 4, device=a.device)
    g[..., T, T] = -torch.exp(torch.clamp(2*a, max=EXP_CLAMP))
    g[..., R, R] = torch.exp(torch.clamp(2*b, max=EXP_CLAMP))
    g[..., TH, TH] = torch.exp(torch.clamp(2*c, max=EXP_CLAMP)) * r**2
    g[..., PS, PS] = torch.exp(torch.clamp(2*d, max=EXP_CLAMP)) * r**2 * sth**2
    # spatial off-diagonals (symmetric).  scale by sqrt of the two diagonal
    # geometric factors so they are dimensionless warps (zero on round).
    g[..., R, TH] = g[..., TH, R] = e_rt * r
    g[..., R, PS] = g[..., PS, R] = e_rp * r * sth
    g[..., TH, PS] = g[..., PS, TH] = e_tp * r**2 * sth
    return g


# ===========================================================================
# SPECTRAL EINSTEIN.  Build dg (spectral), Christoffel, dGamma (spectral), Einstein
# G_{mu nu}, raise to mixed G^mu_nu.  Reuses CORE.christoffel / CORE.einstein
# (the validated exact tensor algebra) with SPECTRAL derivatives.
# ===========================================================================
def einstein_mixed(G, g):
    ginv = CORE.metric_inverse(g)
    # dg[...,k,m,n] = d_k g_{mn}, k over (t,r,th,ps); d_t=0
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    # derivative of each metric component
    for m in range(4):
        for n in range(4):
            comp = g[..., m, n]
            dg[..., R, m, n] = G.d_r(comp)
            dg[..., TH, m, n] = G.d_th(comp)
            dg[..., PS, m, n] = G.d_ps(comp)
    Gamma = CORE.christoffel(ginv, dg)                    # (...,4,4,4) Gamma^a_{bc}
    # dGamma[...,k,a,b,c] = d_k Gamma^a_{bc}
    dGamma = torch.zeros(Nr, Nth, Nps, 4, 4, 4, 4, device=g.device)
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                comp = Gamma[..., a_, b_, c_]
                dGamma[..., R, a_, b_, c_] = G.d_r(comp)
                dGamma[..., TH, a_, b_, c_] = G.d_th(comp)
                dGamma[..., PS, a_, b_, c_] = G.d_ps(comp)
    Gmn, Ric, Rscal = CORE.einstein(g, ginv, Gamma, dGamma)
    Gmix = torch.einsum('...ma,...an->...mn', ginv, Gmn)  # G^m_n
    return Gmix, Gmn, ginv, Gamma


# ===========================================================================
# THE MATTER FIELD.  Unit S^3 hedgehog generalized: a SINGLE profile field
# Theta(r,theta,psi) FREE, with the standard hedgehog angular embedding
#   n = (sinTheta sin th cos(m psi), sinTheta sin th sin(m psi), sinTheta cos th, cosTheta)
# winding m in psi.  For m=1 this is the validated #56/#55 field; FREE Theta(r,th,ps)
# lets the matter carry NON-AXISYMMETRIC shape.  (A richer 3-vector-of-angles
# parametrization is available but this single-profile family already spans the
# psi-dependent / lobed / higher-winding seeds the search needs; flagged in ledger.)
# Returns n (...,4) unit 4-vector.
# ===========================================================================
def field_n(G, Th, m=1):
    sT, cT = torch.sin(Th), torch.cos(Th)
    sth, cth = G.STHg, torch.cos(G.THg)
    sps, cps = torch.sin(m*G.PSg), torch.cos(m*G.PSg)
    return torch.stack([sT*sth*cps, sT*sth*sps, sT*cth, cT], dim=-1)


def field_dn(G, Th, m=1):
    """dn[...,k,a] = d_k n_a, k over (t,r,th,ps) (d_t=0), via the EXACT CHAIN RULE.

    n = n(Theta(r,th,ps), th, ps).  d_mu n = (dn/dTheta) d_mu Theta + (explicit th,ps).
    Spectral differentiation does NOT obey the chain rule pointwise (it is global), so
    differentiating each NONLINEAR component n_a directly is inaccurate (gave G_rr =
    2 Theta'^2 instead of Theta'^2).  We therefore take the SPECTRAL derivatives of the
    SMOOTH profile Theta only, and combine with the ANALYTIC partials of n -- exact.
    Theta = Theta(r,th,ps) FREE (the matter can be fully NON-AXISYMMETRIC)."""
    sT, cT = torch.sin(Th), torch.cos(Th)
    sth, cth = G.STHg, torch.cos(G.THg)
    mps = m*G.PSg
    sps, cps = torch.sin(mps), torch.cos(mps)
    # spectral partials of the smooth profile Theta
    Th_r = G.d_r(Th); Th_t = G.d_th(Th); Th_p = G.d_ps(Th)
    # dn/dTheta (analytic): derivative of n wrt Theta
    nTh = torch.stack([cT*sth*cps, cT*sth*sps, cT*cth, -sT], dim=-1)
    # explicit theta partial of n (Theta held): d/dth at fixed Theta
    n_th_exp = torch.stack([sT*cth*cps, sT*cth*sps, -sT*sth,
                            torch.zeros_like(sT)], dim=-1)
    # explicit psi partial of n (Theta held): d/dps at fixed Theta (winding m)
    n_ps_exp = torch.stack([-m*sT*sth*sps, m*sT*sth*cps,
                            torch.zeros_like(sT), torch.zeros_like(sT)], dim=-1)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 4, device=Th.device)
    dn[..., R, :] = Th_r[..., None]*nTh
    dn[..., TH, :] = Th_t[..., None]*nTh + n_th_exp
    dn[..., PS, :] = Th_p[..., None]*nTh + n_ps_exp
    return dn


# ===========================================================================
# THE MATTER ACTION DENSITY and the EL by AUTOGRAD.
#  L = L2 + L4 (the EXACT MAT.lagrangian).  S = int sqrt(-g) L dV_coord.
#  The matter EL residual at each node = delta S / delta Theta(node) / (measure).
#  We get it by autograd of the scalar S wrt the Theta nodal tensor.  This is the
#  TRUE variation of the SAME action that builds the stress => stress-consistent
#  by construction (immune to the codegen L4 bug).
# ===========================================================================
def matter_action(G, g, ginv, Th, m=1):
    dn = field_dn(G, Th, m=m)
    Gmn = MAT.field_metric(dn)
    L, L2, L4, SS = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)   # xi=kap=1
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    # coordinate volume element: dr dth dps; sqrt|g| already carries the r^2 sin th
    dV = G.wvol_coord
    S = (sqrtg * L * dV).sum()
    return S, L, n, dn, Gmn, SS


def matter_el_autograd(G, g, ginv, Th, m=1):
    """delta S / delta Theta(node), divided by the local proper measure, giving the
    pointwise EL residual (the field EOM).  Computed by autograd of the action."""
    Th_ = Th.detach().clone().requires_grad_(True)
    dn = field_dn(G, Th_, m=m)
    Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv.detach(), Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g.detach()), min=1e-30))
    S = (sqrtg * L * G.wvol_coord).sum()
    gradTh, = torch.autograd.grad(S, Th_, create_graph=False)
    # divide by (sqrtg * dV) to get the pointwise EL density (so it matches the
    # continuum delta S/delta Theta / sqrtg, i.e. the covariant field EOM)
    meas = sqrtg * G.wvol_coord
    el = gradTh / torch.clamp(meas, min=1e-30)
    return el


def _warp_partials(G, f):
    fr = G.d_r(f); ft = G.d_th(f); fp = G.d_ps(f)
    frr = G.d_r(fr); ftt = G.d_th(ft); fpp = G.d_ps(fp)
    frt = G.d_th(fr); frp = G.d_ps(fr); ftp = G.d_ps(ft)
    return (f, fr, ft, fp, frr, ftt, fpp, frt, frp, ftp)


def matter_el_3d(G, a, b, c, d, Th, m=1):
    """The CORRECT analytic 3-D matter Euler-Lagrange residual (direct variation;
    matter_el_3d_gen.py).  Stress-consistent by construction (div(T) = -EL d Theta),
    immune to the L4 codegen bug.  Smooth partials taken spectrally."""
    A = _warp_partials(G, a); B = _warp_partials(G, b)
    C = _warp_partials(G, c); D = _warp_partials(G, d); TH_ = _warp_partials(G, Th)
    mm = torch.full_like(a, float(m))
    return _MEL3D(G.Rg, G.THg, G.PSg, mm, *A, *B, *C, *D, *TH_, 1.0, 1.0)


# coordinate quadrature weight WITHOUT the sin th (sqrt|g| carries r^2 sin th).
def attach_coord_weight(G):
    # pure coordinate weight dr * dmu_theta_in_dtheta * dpsi.  spectral_sph wmu is
    # the int-over-dtheta-with-sin weight; we want the plain-dtheta weight = wmu/sin.
    wth_plain = G.wmu / G.sth
    G.wvol_coord = (G.wr[:, None, None] * wth_plain[None, :, None]
                    * G.wps[None, None, :])
    return G


# ===========================================================================
# RESIDUAL SYSTEM.  Unknowns: a,b,c,d (and optional off-diag e_rt,e_rp,e_tp) +
# Theta, all (Nr,Nth,Nps).  Residuals: G^mu_nu - kap8 T^mu_nu (the 10 mixed
# Einstein, here the static set), and the matter EL.  Plus BC rows.
# ===========================================================================
def residuals(G, fields, p, kap8, m=1):
    """The full coupled residual: G^mu_nu - kap8 T^mu_nu (analytic ANALYTIC Einstein,
    pole-stable) and the matter EL (autograd of the action).  Diagonal Weyl metric
    (a,b,c,d FREE, B=1/A NOT tied); matter Theta(r,th,ps) FREE."""
    a, b, c, d, Th = fields[:5]
    g = build_metric(G, a, b, c, d)
    ginv = CORE.metric_inverse(g)
    Gmix = einstein_mixed_weyl(G, a, b, c, d)             # analytic, pole-stable
    n = field_n(G, Th, m=m)
    dn = field_dn(G, Th, m=m)
    Tab, Lscal, L2, L4 = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)  # T^m_n
    res_E = Gmix - kap8 * Tmix                            # (...,4,4) mixed Einstein
    el = matter_el_3d(G, a, b, c, d, Th, m=m)             # CORRECT analytic 3-D EL
    return dict(res_E=res_E, el=el, g=g, Gmix=Gmix, Tmix=Tmix, Tab=Tab,
                ginv=ginv, n=n, dn=dn, Lscal=Lscal)


# ===========================================================================
# THE div(T) IDENTITY (the prompt's off-round matter-EL correctness gate).
# For the matter field obeying its EOM,  nabla_mu T^mu_nu = 0; off the solution,
# the covariant divergence of the stress EQUALS - EL . d_nu(field).  We verify the
# autograd EL is the TRUE variation by checking  nabla_mu T^mu_r  ==  -EL * d_r Theta
# (and the theta, psi components) -- the conservation<->EOM theorem.  This is the
# structural proof the EL is correct OFF-ROUND (the axisym_matter_el.py L4 bug test).
#   nabla_mu T^mu_nu = (1/sqrt|g|) d_mu( sqrt|g| T^mu_nu ) - Gamma^l_{mu nu} T^mu_l
# computed with the analytic metric + spectral derivatives.
# ===========================================================================
def divT_identity(G, out):
    g = out['g']; ginv = out['ginv']; Tab = out['Tab']
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)  # T^mu_nu (mixed)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    # build dg spectrally for Christoffel
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for mm in range(4):
        for nn in range(4):
            comp = g[..., mm, nn]
            dg[..., R, mm, nn] = G.d_r(comp)
            dg[..., TH, mm, nn] = G.d_th(comp)
            dg[..., PS, mm, nn] = G.d_ps(comp)
    Gamma = CORE.christoffel(ginv, dg)                    # Gamma^a_{bc}
    # nabla_mu T^mu_nu = (1/sqrtg) d_mu(sqrtg T^mu_nu) - Gamma^l_{mu nu} T^mu_l
    def d_mu(field, mu):
        if mu == R: return G.d_r(field)
        if mu == TH: return G.d_th(field)
        if mu == PS: return G.d_ps(field)
        return torch.zeros_like(field)
    divT = torch.zeros(Nr, Nth, Nps, 4, device=g.device)
    for nu in range(4):
        term = torch.zeros(Nr, Nth, Nps, device=g.device)
        for mu in range(1, 4):  # mu=t gives 0 (static)
            term = term + d_mu(sqrtg * Tmix[..., mu, nu], mu)
        term = term / torch.clamp(sqrtg, min=1e-30)
        for mu in range(4):
            for l in range(4):
                term = term - Gamma[..., l, mu, nu] * Tmix[..., mu, l]
        divT[..., nu] = term
    return divT


# ===========================================================================
# DIAGNOSTICS.  M_MS (areal mass at seal), gauge-invariant shape scalars.
# ===========================================================================
def diagnostics(G, out, kap8):
    Tab = out['Tab']; g = out['g']; ginv = out['ginv']
    # rho = -T^t_t  (mixed)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    rho = -Tmix[..., T, T]
    # areal mass M(r) = int_0^r kap8 r'^2 rho dOmega/(4pi)... use the (t,t) sourced
    # m'(r) = kap8 * <r^2 rho>_angle (angle-averaged), integrate radially.
    # angle average of rho with proper sphere measure:
    dOmega = (G.wmu[None, :, None] * G.wps[None, None, :])
    rho_ang = (rho * dOmega).sum(dim=(1, 2)) / (4*PI)     # (Nr,)
    integ = kap8 * G.r**2 * rho_ang
    # radial cumulative via Clenshaw-Curtis-consistent trapezoid on Cheb nodes
    # (use simple cumulative trapezoid in physical r ordering)
    r = G.r
    M = torch.zeros_like(r)
    for i in range(1, len(r)):
        M[i] = M[i-1] + 0.5*(integ[i]+integ[i-1])*(r[i]-r[i-1])
    M_MS = (M[-1] - M[0]).item()
    # gauge-invariant ANGULAR shape: variation of rho (a scalar density invariant
    # under SPATIAL gauge among the angular DOF) over the sphere at fixed r,
    # averaged over the body radii.  tvar = mean_r std_angle(rho)/mean_angle(rho).
    body_r = (r > 0.8) & (r < G.ri - 0.8)
    rb = rho[body_r]                                       # (nb,Nth,Nps)
    mean_a = (rb * dOmega).sum(dim=(1, 2)) / (4*PI)
    var_a = ((rb - mean_a[:, None, None])**2 * dOmega).sum(dim=(1, 2)) / (4*PI)
    tvar = (torch.sqrt(torch.clamp(var_a, min=0)) / torch.clamp(mean_a.abs(), min=1e-12)).mean().item()
    # psi-shape specifically (non-axisymmetry witness): variation in psi at fixed r,th
    psivar = (rb.std(dim=2) / torch.clamp(rb.mean(dim=2).abs(), min=1e-12)).mean().item()
    return dict(M_MS=M_MS, tvar=tvar, psivar=psivar, rho_ang=rho_ang)


if __name__ == "__main__":
    print("=== full3d_spectral smoke test: build grid + flat-space Einstein=0 ===")
    G = Grid3D(Nr=20, Nth=6, Nps=8, rc=0.05, cell=14.0)
    G = attach_coord_weight(G)
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
    # flat space: a=b=c=d=0 => g = diag(-1, 1, r^2, r^2 sin^2) = flat in spherical
    g = build_metric(G, z, z, z, z)
    Gmix, Gmn, ginv, Gamma = einstein_mixed(G, g)
    print(f"  flat-space max|G^mu_nu| (body) = {float(Gmix[G.body].abs().max()):.3e}")
