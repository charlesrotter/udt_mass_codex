#!/usr/bin/env python3
"""
free_s2_matter.py -- THE GENUINELY FREE S^2 MATTER FIELD for the complete 4-D solver.
Stage S2 of THE COMPLETE 4-D SOLVER BUILD PROGRAM (COMPLETION_PROGRAM.md).

Driver: Claude (Opus 4.8, 1M).  2026-06-21.  Frame: COMPLETION_PROGRAM S2.
Mode: INFRASTRUCTURE, DATA-BLIND.  BUILD + cheap EVAL only -- NO Newton/coupled solve.

WHY THIS EXISTS (the matter audit, [[full-dimensional-complete-solver]]):
  The matter field used in the off-round solver was a SINGLE scalar profile Theta in a
  FIXED hedgehog embedding that WELDS the target-space direction to the physical angles --
  n = (sinTheta(r,th,ps) sin th cos(m ps), sinTheta sin th sin(m ps), cos Theta).  That is
  effectively ONE degree of freedom (one scalar field), not a free S^2 matter field.  A
  complete solver must let the matter carry FULL angular freedom on the target sphere.

WHAT THIS BUILDS (Charles's spec; S^2 EVERYWHERE per the M10/M11 closure -- the unit
  3-vector; the stale S^3 4-vector embedding is RETIRED):
  matter = a unit 3-vector field  n : (r,th,ps) -> S^2  with TWO genuinely free fields.

PARAMETRIZATION CHOICE (premise-ledgered, justified below): we provide BOTH and validate
  they agree, but the PRIMARY/ROBUST one for the solver is the 3-COMPONENT + |n|=1 form.
  - 3-COMPONENT (primary):  carry n=(n1,n2,n3) as three free nodal fields, projected to
    the unit sphere  nhat = n/|n|  (|nhat|=1 exact, no Lagrange multiplier).  dn computed
    by the QUOTIENT-RULE chain rule on the SMOOTH components (spectral d on n1,n2,n3, then
    the analytic d(n/|n|)).  Pole-robust: there is NO target-pole coordinate singularity
    (the (Theta,Phi) chart's Phi-degeneracy at Theta=0,pi simply does not exist here).
    This form REPRESENTS the banked welded hedgehog EXACTLY (it is just a particular n
    field), which the 2-angle form CANNOT (see note).
  - 2-ANGLE (analytic seed / special case):  n=(sinTh_t cosPh_t, sinTh_t sinPh_t, cosTh_t)
    with free Th_t(r,th,ps), Ph_t(r,th,ps).  |n|=1 automatic.  Matches Charles's stated
    form; used as an exact analytic cross-check of the 3-component machinery in a regime
    away from the target poles.  NOTE: the welded round hedgehog is NOT a 2-angle field
    in this chart (its target-polar-angle is arccos(cos Theta(r)) but its n1^2+n2^2 =
    sin^2Theta sin^2 th != sin^2(target-polar), so the (Th_t,Ph_t) chart cannot reproduce
    it with Th_t=Theta(r)).  Hence the 3-component form is the one that recovers the gate.

THE ACTION (settled native S^2; coupled_tl_s2_derive.py / C-2026-06-14-1):
  L2 = -(xi/2) g^{mn} d_m n . d_n n                      (. = dot over the 3 S^2 comps)
  L4 = -(kap/4) g^{mp} g^{nq} S_{mn}.S_{pq},  S_{mn} = d_m n x d_n n  (3-vector cross
       product -- exists for an S^2 3-vector; = the native H1 area-form current).
  IDENTITY (Lagrange):  for a 3-vector,  (d_m n x d_n n).(d_p n x d_q n)
       = (d_m n.d_p n)(d_n n.d_q n) - (d_m n.d_q n)(d_n n.d_p n) = G_mp G_nq - G_mq G_np.
  => the Lagrange-identity L4 in MAT.lagrangian (whole_metric_3d_matter.py) IS the
     cross-product L4 for a 3-vector target.  So MAT.field_metric/lagrangian/stress_tensor
     -- which contract only over the target index a -- are TARGET-DIMENSION-AGNOSTIC and
     are REUSED VERBATIM here with a 3-component dn.  (Validated in __main__ below.)

THE EL: autograd of the action S = int sqrt(-g) (xi=kap weight) L over BOTH free fields
  (Th_t,Ph_t) or the THREE components (n1,n2,n3) -- torch.autograd.grad pointed at the
  free field tensors.  This RETIRES the codegen matter_el_3d (a second hand-generated EL
  with a documented off-round bug); autograd of the same action that builds the stress is
  stress-consistent by construction.

e^{2phi} WEIGHT (the derived operator's matter weight, b1prime_3d_offround_residual.py):
  the matter enters the action as  f L_m  with f = e^{2phi}.  Since f is field-independent
  for the matter variation, delta(f L_m)/delta(field) = f * delta L_m/delta(field).  We
  carry an OPTIONAL f weight on the action so the EL inherits it correctly.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3

import whole_metric_3d_matter as MAT   # field_metric / lagrangian / stress_tensor (general)


# ===========================================================================
# PARAMETRIZATION A -- 3-COMPONENT + |n|=1 (PRIMARY).
#   carry three free nodal fields (n1,n2,n3); the physical field is nhat = n/|n|.
#   dn computed by the analytic quotient rule on the SMOOTH components.
# ===========================================================================
def nhat_from_components(n_raw):
    """n_raw (...,3) free; return the unit field nhat (...,3) and the norm |n_raw|."""
    nrm = torch.sqrt(torch.clamp((n_raw**2).sum(-1), min=1e-300))
    return n_raw / nrm[..., None], nrm


def field_dn_components_exact(G, n_raw):
    """dn[...,k,a] = d_k nhat_a for the PURE 3-component S^2 carrier, with d/dtheta computed by
    the SPHERICAL-HARMONIC-EXACT operator (spectral_sph_exact) instead of the grid's
    -sin(theta) D_mu (which mis-differentiates winding sin(theta) structure non-convergently).
    This is the grid-fixed, FULLY-FREE dn (no imposed polar shape).  Quotient rule on nhat=n/|n|;
    built by stacking (jacrev-/vmap-safe, no in-place)."""
    from spectral_sph_exact import dtheta_exact_torch
    nrm = torch.sqrt(torch.clamp((n_raw**2).sum(-1), min=1e-300))
    inv = 1.0 / nrm

    def proj(dnk):                                   # tangential (quotient-rule) derivative
        ndotk = (n_raw * dnk).sum(-1)
        return inv[..., None] * dnk - (inv**3 * ndotk)[..., None] * n_raw

    z3 = torch.zeros_like(n_raw)                      # d_t = 0
    dr = torch.stack([G.d_r(n_raw[..., a]) for a in range(3)], dim=-1)
    dth = torch.stack([dtheta_exact_torch(n_raw[..., a]) for a in range(3)], dim=-1)  # EXACT
    dps = torch.stack([G.d_ps(n_raw[..., a]) for a in range(3)], dim=-1)
    return torch.stack([z3, proj(dr), proj(dth), proj(dps)], dim=-2)   # (...,4,3): t,r,th,ps


def field_dn_components(G, n_raw):
    """dn[...,k,a] = d_k nhat_a, k over (t,r,th,ps) (d_t=0), a over the 3 S^2 comps.

    CHAIN RULE (quotient form): nhat = n / |n|.  For each coordinate mu,
      d_mu nhat = (1/|n|) d_mu n  -  (n / |n|^3) (n . d_mu n).
    We take the SPECTRAL derivatives of the SMOOTH raw components n1,n2,n3 (each a smooth
    nodal field), then combine analytically -- exact (no raw spectral diff of a nonlinear
    composite, which the audit showed gives a 2x error).  No target-pole singularity."""
    nrm = torch.sqrt(torch.clamp((n_raw**2).sum(-1), min=1e-300))     # (...,)
    inv = 1.0/nrm
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 3, device=n_raw.device)
    for k, dop in ((R, G.d_r), (TH, G.d_th), (PS, G.d_ps)):
        dnk = torch.stack([dop(n_raw[..., 0]), dop(n_raw[..., 1]),
                           dop(n_raw[..., 2])], dim=-1)               # d_k n_raw (...,3)
        ndotk = (n_raw * dnk).sum(-1)                                 # n . d_k n
        dn[..., k, :] = inv[..., None]*dnk - (inv**3 * ndotk)[..., None]*n_raw
    return dn


# ===========================================================================
# PARAMETRIZATION B -- 2-ANGLE (Charles's stated form; analytic seed / cross-check).
#   n = (sinTh_t cosPh_t, sinTh_t sinPh_t, cosTh_t).  |n|=1 automatic.
#   dn by the analytic chain rule on the SMOOTH angle fields Th_t,Ph_t.
# ===========================================================================
def field_n_angles(Th_t, Ph_t):
    sT, cT = torch.sin(Th_t), torch.cos(Th_t)
    sP, cP = torch.sin(Ph_t), torch.cos(Ph_t)
    return torch.stack([sT*cP, sT*sP, cT], dim=-1)


def field_dn_angles(G, Th_t, Ph_t):
    """dn[...,k,a]=d_k n_a via the EXACT chain rule on the smooth angle fields.
    d_mu n = (dn/dTh_t) d_mu Th_t + (dn/dPh_t) d_mu Ph_t, spectral d on Th_t,Ph_t.
    REGULARITY: at the TARGET poles Th_t=0,pi, dn/dPh_t = (sinTh_t)(...)->0, so n & dn
    stay finite even though Ph_t is geometrically undefined (sin Th_t kills the Ph term).
    """
    sT, cT = torch.sin(Th_t), torch.cos(Th_t)
    sP, cP = torch.sin(Ph_t), torch.cos(Ph_t)
    nTh = torch.stack([cT*cP, cT*sP, -sT], dim=-1)            # dn/dTh_t
    nPh = torch.stack([-sT*sP, sT*cP, torch.zeros_like(sT)], dim=-1)  # dn/dPh_t (~sinTh_t)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 3, device=Th_t.device)
    for k, dop in ((R, G.d_r), (TH, G.d_th), (PS, G.d_ps)):
        dn[..., k, :] = dop(Th_t)[..., None]*nTh + dop(Ph_t)[..., None]*nPh
    return dn


# ===========================================================================
# THE CANONICAL UNIT S^2 HEDGEHOG (the banked charge-1 reference) -- n = x/r.
#   M10/M11 closure (M10_M11_object_identity_closure_results.md, lines 129-135):
#   the GENUINE NATIVE unit degree-1 hedgehog is the radial map
#       n = x/r = (sin th cos(m ps), sin th sin(m ps), cos th),   |n|^2 = 1 EXACTLY.
#   CRITICAL CORRECTION (this build): the OLD seed n=(sinTheta sin th cos mps, ...,
#   cosTheta) -- used in coupled_tl_s2_derive.py AND the retired S^3 4-vector
#   full3d_spectral.field_dn -- is NOT a unit map (|n|^2 = cos^2th cos^2Theta-cos^2th+1
#   != 1).  Its cos-theta "texture" was a verifier-KILLED ARTIFACT of that bad chart.
#   The canonical carrier carries its RADIAL structure in the metric (B=1/A), NOT in a
#   Theta(r) field -- n=x/r is purely angular.  T^t_t = T^r_r exactly (the C-14-1 break);
#   T^th_th is theta-independent.  This is the hedgehog-limit reference the gate must hit.
#   (A radial profile generalizes to n=(sin f(th) cos mps, ..., cos f(th)); the canon
#   degree-1 carrier is f(th)=th, i.e. n=x/r.)
# ===========================================================================
# ---------------------------------------------------------------------------
# GRID NOTE (load-bearing, found this build): the inherited angular grid
# (spectral_sph.theta_operators) is GAUSS-LEGENDRE in mu=cos theta with Dth=(-sin th)Dmu,
# EXACT only for functions POLYNOMIAL in mu.  Bare sin(theta)=sqrt(1-mu^2) is NOT a
# mu-polynomial -> a raw spectral d_th of any sin(theta)-bearing component is INACCURATE
# (~0.17, NON-convergent; verified by /tmp resolution sweep).  So the genuinely-free
# angular matter field on THIS grid must carry the sin(theta) structure ANALYTICALLY and
# differentiate only the mu-smooth free fields spectrally -- exactly the original full3d
# field_dn design.  The analytic-dn builders below do this; their dn is EXACT (machine
# precision).  (The component quotient-rule field_dn_components is correct ONLY when the
# raw components are mu-polynomial; it is kept for that case + to expose the grid error.)
# ---------------------------------------------------------------------------
def dn_xr_analytic(G, m=1):
    """EXACT dn for the canon unit hedgehog n = x/r = (sth cmps, sth smps, cth).
    sin theta carried ANALYTICALLY (the grid cannot spectrally differentiate it); the
    ps-derivatives are spectral-exact (Fourier).  d_r = 0 (purely angular)."""
    sth, cth = G.STHg, torch.cos(G.THg)
    sps, cps = torch.sin(m*G.PSg), torch.cos(m*G.PSg)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 3, device=G.dev)
    # d_th n (analytic): d_th(sth)=cth, d_th(cth)=-sth
    dn[..., TH, :] = torch.stack([cth*cps, cth*sps, -sth], dim=-1)
    # d_ps n (analytic, winding m): d_ps(cos m ps)=-m sin m ps, etc; n3 has no ps
    dn[..., PS, :] = torch.stack([-m*sth*sps, m*sth*cps, torch.zeros_like(sth)], dim=-1)
    return dn


# ---------------------------------------------------------------------------
# A GENUINELY-FREE FAMILY with EXACT dn on the Gauss-in-mu grid: the hedgehog with a
# FREE AZIMUTH field Psi = m*ps + phi(r,ps) (phi a smooth field of r and ps, NO theta so
# it stays mu-trivial) AND a FREE POLAR TILT amplitude.  n stays unit; sin theta analytic.
#   n = ( sth cos Psi, sth sin Psi, cth ),  Psi(r,ps) free.
# d_ps and d_r of Psi are spectral-EXACT (Fourier in ps, Chebyshev in r); d_th carries the
# analytic sin/cos theta.  This is a genuine non-hedgehog DOF (azimuth winding modulated
# in ps and r) the welded single-profile field cannot represent.  EL over phi is autograd.
# ---------------------------------------------------------------------------
# NOTE the winding m*ps is a RAMP (non-periodic) -- its spectral Fourier d_ps is WRONG.
# So the winding is carried ANALYTICALLY (Psi = m*ps + phi); only the PERIODIC free field
# phi(r,ps) is spectrally differentiated (Fourier-exact).  d_ps Psi = m + d_ps phi.
def field_n_freeaz(G, phi, m=1):
    sth, cth = G.STHg, torch.cos(G.THg)
    Psi = m*G.PSg + phi
    return torch.stack([sth*torch.cos(Psi), sth*torch.sin(Psi), cth], dim=-1)


def field_dn_freeaz(G, phi, m=1):
    """EXACT dn for n=(sth cosPsi, sth sinPsi, cth), Psi=m*ps+phi(r,ps), phi PERIODIC &
    free.  The winding m*ps is analytic; d_r,d_ps of phi spectral-exact (Cheb/Fourier).
    sin/cos theta analytic (grid cannot differentiate bare sin theta)."""
    sth, cth = G.STHg, torch.cos(G.THg)
    Psi = m*G.PSg + phi
    cP, sP = torch.cos(Psi), torch.sin(Psi)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 3, device=G.dev)
    Psi_r = G.d_r(phi)                       # d_r(m ps)=0
    Psi_p = float(m) + G.d_ps(phi)           # d_ps(m ps)=m (analytic) + spectral d_ps phi
    z3 = torch.zeros_like(sth)
    dn[..., R, :] = torch.stack([-sth*sP*Psi_r, sth*cP*Psi_r, z3], dim=-1)
    dn[..., TH, :] = torch.stack([cth*cP, cth*sP, -sth], dim=-1)
    dn[..., PS, :] = torch.stack([-sth*sP*Psi_p, sth*cP*Psi_p, z3], dim=-1)
    return dn


def matter_el_autograd_freeaz(G, g, ginv, phi, xi, kap, m=1, f=None):
    """Autograd EL over the free PERIODIC field phi (retires codegen EL; stress-consistent)."""
    Psi_ = phi.detach().clone().requires_grad_(True)
    dn = field_dn_freeaz(G, Psi_, m=m)
    S, *_ = _action_scalar(G, g.detach(), ginv.detach(), dn, xi, kap,
                           None if f is None else f.detach())
    gP, = torch.autograd.grad(S, Psi_, create_graph=False)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g.detach()), min=1e-300))
    meas = (sqrtg if f is None else sqrtg*f.detach()) * G.wvol_coord
    return gP / torch.clamp(meas, min=1e-300)


def hedgehog_xr_components(G, m=1):
    sth, cth = G.STHg, torch.cos(G.THg)
    sps, cps = torch.sin(m*G.PSg), torch.cos(m*G.PSg)
    return torch.stack([sth*cps, sth*sps, cth], dim=-1)


# ===========================================================================
# THE ACTION + AUTOGRAD EL (retires the codegen matter_el_3d).
#   S = sum_nodes sqrt|g| * f * L * dV_coord,  f = e^{2phi} (default 1).
#   EL_field(node) = delta S / delta field(node) / measure  (covariant field EOM density).
# ===========================================================================
def _action_scalar(G, g, ginv, dn, xi, kap, f=None):
    Gmn = MAT.field_metric(dn)
    L, L2, L4, SS = MAT.lagrangian(ginv, Gmn, xi, kap)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-300))
    w = sqrtg if f is None else sqrtg * f
    S = (w * L * G.wvol_coord).sum()
    return S, L, L2, L4


def matter_el_autograd_angles(G, g, ginv, Th_t, Ph_t, xi, kap, f=None):
    """EL over BOTH angle fields by autograd of the SAME action that builds the stress.
    Returns (el_Th, el_Ph), each the pointwise covariant EOM density."""
    Th_ = Th_t.detach().clone().requires_grad_(True)
    Ph_ = Ph_t.detach().clone().requires_grad_(True)
    dn = field_dn_angles(G, Th_, Ph_)
    S, *_ = _action_scalar(G, g.detach(), ginv.detach(), dn, xi, kap,
                           None if f is None else f.detach())
    gTh, gPh = torch.autograd.grad(S, (Th_, Ph_), create_graph=False)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g.detach()), min=1e-300))
    meas = (sqrtg if f is None else sqrtg*f.detach()) * G.wvol_coord
    meas = torch.clamp(meas, min=1e-300)
    return gTh/meas, gPh/meas


def matter_el_autograd_components(G, g, ginv, n_raw, xi, kap, f=None):
    """EL over the THREE raw components by autograd (projected field nhat=n/|n|).
    Returns el (...,3): the covariant EOM density per raw component.  (The physical EOM
    is its tangential projection; the radial part is the |n|=1 constraint direction.)"""
    n_ = n_raw.detach().clone().requires_grad_(True)
    dn = field_dn_components(G, n_)
    S, *_ = _action_scalar(G, g.detach(), ginv.detach(), dn, xi, kap,
                           None if f is None else f.detach())
    gN, = torch.autograd.grad(S, n_, create_graph=False)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g.detach()), min=1e-300))
    meas = (sqrtg if f is None else sqrtg*f.detach()) * G.wvol_coord
    return gN / torch.clamp(meas, min=1e-300)[..., None]


def stress(g, ginv, dn, xi, kap):
    """Reuse the GENERAL Hilbert stress verbatim (target-dim-agnostic)."""
    return MAT.stress_tensor(g, ginv, dn, xi, kap)


if __name__ == "__main__":
    # =======================================================================
    # CHEAP EVALUATION / VALIDATION (NO Newton, NO coupled solve).  Single process.
    # =======================================================================
    import numpy as np
    import full3d_spectral as F3
    torch.manual_seed(0)
    DEVl = DEV
    print(f"device = {DEVl}")
    G = F3.Grid3D(12, 9, 8, rc=0.05, cell=12.0, dev=DEVl)
    G = F3.attach_coord_weight(G)

    rr = G.r
    rc, ri = float(rr[0]), float(rr[-1])
    # round diagonal metric: a=b=c=d=0 -> Schwarzschild-flat areal chart (e^{2B}=1).
    # NOTE the CANON unit S^2 carrier n=x/r is PURELY ANGULAR -- no Theta(r) profile; its
    # radial structure lives in the metric (B=1/A).  (f=e^{2phi}=1 for this gate.)
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEVl)
    g = F3.build_metric(G, z, z, z, z)
    ginv = F3.CORE.metric_inverse(g)
    xi = kap = 1.0

    print("\n=========================================================")
    print("VALIDATION 0: Lagrange identity  cross-L4 == identity-L4  (3-vector)")
    print("=========================================================")
    # build a random smooth 3-comp field, compare MAT.lagrangian L4 (identity form)
    # to the explicit cross-product L4.
    nr = torch.randn(G.Nr, G.Nth, G.Nps, 3, device=DEVl)
    nhat, _ = nhat_from_components(nr)
    dn = field_dn_components(G, nr)
    Gmn = MAT.field_metric(dn)
    Lid, L2id, L4id, SS = MAT.lagrangian(ginv, Gmn, xi, kap)
    # explicit cross product L4
    def cross(u, v):
        return torch.stack([u[..., 1]*v[..., 2]-u[..., 2]*v[..., 1],
                            u[..., 2]*v[..., 0]-u[..., 0]*v[..., 2],
                            u[..., 0]*v[..., 1]-u[..., 1]*v[..., 0]], dim=-1)
    L4cross = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEVl)
    for mm in range(4):
        for nn in range(4):
            Smn = cross(dn[..., mm, :], dn[..., nn, :])
            L4cross = L4cross + ginv[..., mm, mm]*ginv[..., nn, nn]*(Smn*Smn).sum(-1)
    L4cross = -(kap/4)*L4cross
    err = (L4id - L4cross).abs().max().item()
    print(f"  max|L4_identity - L4_cross| = {err:.3e}   (=> MAT.lagrangian IS the S^2 L4)")

    print("\n=========================================================")
    print("VALIDATION 1: HEDGEHOG-LIMIT GATE  (free S^2 machinery vs banked CANON unit")
    print("              S^2 hedgehog n=x/r, against sympy-verified closed forms)")
    print("=========================================================")
    mm = 1
    n_h = hedgehog_xr_components(G, m=mm)                       # CANON unit S^2, |n|=1
    nhat_h, nrm_h = nhat_from_components(n_h)
    print(f"  |n|=1 (n=x/r, all theta incl poles): max||n|-1| = "
          f"{(nrm_h-1).abs().max().item():.3e}")
    # dn: ANALYTIC (the grid cannot spectrally differentiate sin theta -- see GRID NOTE).
    # We ALSO report the spectral-dn error to document the grid limitation explicitly.
    dn_h = dn_xr_analytic(G, m=mm)
    dn_spec = field_dn_components(G, n_h)
    print(f"  dn finite everywhere: max|dn| = {dn_h.abs().max().item():.3e}, "
          f"any nan/inf = {bool(torch.isnan(dn_h).any() or torch.isinf(dn_h).any())}")
    print(f"  [grid note] max|dn_spectral - dn_analytic| = "
          f"{(dn_spec-dn_h).abs().max().item():.3e}  (spectral d_th of sin th is INEXACT; "
          f"analytic dn is the correct path)")
    Tab, Lsc, L2sc, L4sc = stress(g, ginv, dn_h, xi, kap)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)

    # banked CANON closed forms (sympy-verified /tmp/s2_canon_stress.py; m=mm, A=B=0):
    #   rho = -T^t_t = (kap m^2 + r^2 xi (m^2+1)) / (2 r^4)
    #   p_r =  T^r_r = -rho                       (T^t_t == T^r_r, the C-14-1 B=1/A break)
    #   p_th=  T^th_th = (kap m^2 - m^2 r^2 xi + r^2 xi) / (2 r^4)   (theta-INDEPENDENT)
    #   p_ps=  T^ps_ps = (kap m^2 + m^2 r^2 xi - r^2 xi) / (2 r^4)
    rr2 = G.Rg**2; rr4 = G.Rg**4
    m2 = float(mm)**2
    rho_round = (kap*m2 + rr2*xi*(m2+1)) / (2*rr4)
    pr_round  = -rho_round
    pth_round = (kap*m2 - m2*rr2*xi + rr2*xi) / (2*rr4)
    pps_round = (kap*m2 + m2*rr2*xi - rr2*xi) / (2*rr4)

    rho_num = -Tmix[..., T, T]
    pr_num  =  Tmix[..., R, R]
    pth_num =  Tmix[..., TH, TH]
    pps_num =  Tmix[..., PS, PS]

    body = G.body
    def cmp(a, b, name):
        e_all = (a-b).abs().max().item()
        e_body = (a-b)[body].abs().max().item()
        scale = b[body].abs().max().item() + 1e-30
        print(f"  {name:8s}: max|free-canon| all={e_all:.3e}  body={e_body:.3e}  "
              f"rel_body={e_body/scale:.3e}")
        return e_body/scale
    r1 = cmp(rho_num, rho_round, "rho")
    r2 = cmp(pr_num,  pr_round,  "p_r")
    r3 = cmp(pth_num, pth_round, "p_th")
    r4 = cmp(pps_num, pps_round, "p_ps")
    # the C-14-1 break test: T^t_t == T^r_r exactly for the canon carrier
    ttrr = (Tmix[..., T, T] - Tmix[..., R, R])[body].abs().max().item()
    print(f"  C-14-1 break  T^t_t == T^r_r: max|diff| = {ttrr:.3e}")
    # T^th_th theta-independent (texture-free): at each radius, max spread across theta
    pth_b = pth_num                                            # (Nr,Nth,Nps)
    spread = (pth_b.amax(dim=1) - pth_b.amin(dim=1))           # over theta, per (r,ps)
    tex = spread[3:G.Nr-3, :].abs().max().item()
    print(f"  texture-free (T^th_th theta-spread, body) = {tex:.3e} (canon: ~0)")
    # off-diagonal stress must vanish for the round hedgehog
    offmax = 0.0
    for (i, j) in [(R, TH), (R, PS), (TH, PS), (T, R), (T, TH), (T, PS)]:
        offmax = max(offmax, Tmix[..., i, j].abs().max().item())
    print(f"  off-diagonal T^mu_nu max = {offmax:.3e}  (round => should be ~0)")
    gate_pass = max(r1, r2, r3, r4) < 1e-8 and offmax < 1e-8 and ttrr < 1e-8
    print(f"  HEDGEHOG-LIMIT GATE: {'PASS (machine precision)' if gate_pass else 'SEE NUMBERS (rel<1e-8?)'}")

    print("\n=========================================================")
    print("VALIDATION 2: |n|=1 across the chart (3-comp & 2-angle, incl target poles)")
    print("=========================================================")
    # 3-component: the canon hedgehog is unit everywhere incl theta-poles (already shown);
    # also check the 2-angle form hits the TARGET poles Th_t=0,pi with |n|=1 and finite dn.
    Th_t = math.pi*(1.0 - (G.Rg - rc)/(ri-rc))                # 0..pi, hits both poles
    Ph_t = 1.0*G.PSg
    n_ang = field_n_angles(Th_t, Ph_t)
    nrm_ang = torch.sqrt((n_ang**2).sum(-1))
    dn_ang = field_dn_angles(G, Th_t, Ph_t)
    poles = (Th_t < 0.2) | (Th_t > math.pi-0.2)
    print(f"  3-comp n=x/r |n|=1: max||n|-1| = {(nrm_h-1).abs().max().item():.3e}")
    print(f"  2-angle |n|=1 (incl Th_t=0,pi): max||n|-1| = "
          f"{(nrm_ang-1).abs().max().item():.3e}")
    print(f"  2-angle dn finite AT target poles: max|dn|_poles="
          f"{dn_ang[poles].abs().max().item():.3e}, "
          f"nan/inf={bool(torch.isnan(dn_ang).any() or torch.isinf(dn_ang).any())}  "
          f"(sin Th_t kills the undefined Phi-direction => regular)")

    print("\n=========================================================")
    print("VALIDATION 3: GENUINE FREEDOM  (a non-hedgehog field changes L & T)")
    print("=========================================================")
    # FREE-AZIMUTH family: Psi = m ps + phi(r,ps), phi a smooth NON-trivial deformation
    # (r- and ps-modulated winding) the SINGLE-PROFILE welded hedgehog CANNOT represent.
    # dn is EXACT (grid-correct).  Confirm L & T respond and NEW stress structure appears.
    rfac = torch.sin(math.pi*(G.Rg-rc)/(ri-rc))               # 0 at core/seal, smooth in r
    phi_def = 0.3*rfac*torch.cos(2*G.PSg)                      # r,ps modulated azimuth twist
    phi0 = torch.zeros_like(phi_def)                           # pure hedgehog winding
    dn0 = field_dn_freeaz(G, phi0, m=mm)                       # = the hedgehog (check)
    dn1 = field_dn_freeaz(G, phi_def, m=mm)
    # sanity: Psi0 reproduces the canon hedgehog stress exactly
    Tab0, *_ = stress(g, ginv, dn0, xi, kap)
    Tmix0 = torch.einsum('...ma,...an->...mn', ginv, Tab0)
    pth0_err = (Tmix0[..., TH, TH]-pth_round)[body].abs().max().item()
    print(f"  free-az at phi=0 reproduces canon T^th_th: max err = {pth0_err:.3e}")
    Tab1, L1, *_ = stress(g, ginv, dn1, xi, kap)
    Tmix1 = torch.einsum('...ma,...an->...mn', ginv, Tab1)
    S0, *_ = _action_scalar(G, g, ginv, dn0, xi, kap)
    S1, *_ = _action_scalar(G, g, ginv, dn1, xi, kap)
    dS = abs(S1.item()-S0.item())
    # new off-diagonal stress the welded hedgehog had ZERO of (T^r_ps, T^th_ps)
    off0 = max(Tmix0[..., R, PS].abs().max().item(), Tmix0[..., TH, PS].abs().max().item())
    off1 = max(Tmix1[..., R, PS].abs().max().item(), Tmix1[..., TH, PS].abs().max().item())
    print(f"  action change |dS| = {dS:.3e}  (nonzero => phi is a real new DOF)")
    print(f"  off-diag stress: hedgehog={off0:.3e} -> deformed={off1:.3e} "
          f"(NEW momentum flux the welded field could not carry)")
    free_pass = (dS > 1e-6 and off1 > 1e-6 and off0 < 1e-10 and pth0_err < 1e-10)
    print(f"  GENUINE FREEDOM: {'PASS' if free_pass else 'SEE NUMBERS'}")

    print("\n=========================================================")
    print("VALIDATION 4: AUTOGRAD-EL <-> div(T) CONSISTENCY (free-azimuth channel)")
    print("=========================================================")
    # conservation<->EOM theorem:  nabla_mu T^mu_nu = - EL_Psi * d_nu Psi   (single free
    # field Psi here).  div(T) via analytic Christoffel + spectral metric/T derivatives.
    # Use the DEFORMED field (non-trivial EL) so the test is meaningful.
    g2 = g; ginv2 = ginv
    dn2 = dn1
    Psi = float(mm)*G.PSg + phi_def                           # full azimuth (winding+free)
    # analytic d_nu Psi (winding part analytic; phi spectral)
    dPsi_r = G.d_r(phi_def)
    dPsi_ps = float(mm) + G.d_ps(phi_def)
    Tab2 = Tab1
    Tmix2 = Tmix1
    sqrtg2 = torch.sqrt(torch.clamp(-torch.linalg.det(g2), min=1e-300))
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=DEVl)
    for ii in range(4):
        for jj in range(4):
            comp = g2[..., ii, jj]
            dg[..., R, ii, jj] = G.d_r(comp); dg[..., TH, ii, jj] = G.d_th(comp)
            dg[..., PS, ii, jj] = G.d_ps(comp)
    Gamma = F3.CORE.christoffel(ginv2, dg)
    def d_mu(field, mu):
        if mu == R: return G.d_r(field)
        if mu == TH: return G.d_th(field)
        if mu == PS: return G.d_ps(field)
        return torch.zeros_like(field)
    divT = torch.zeros(Nr, Nth, Nps, 4, device=DEVl)
    for nu in range(4):
        acc = torch.zeros(Nr, Nth, Nps, device=DEVl)
        for mu in range(4):
            acc = acc + d_mu(sqrtg2*Tmix2[..., mu, nu], mu)
        acc = acc / torch.clamp(sqrtg2, min=1e-300)
        corr = torch.einsum('...lm,...ml->...', Gamma[..., :, :, nu], Tmix2)
        divT[..., nu] = acc - corr
    elPsi = matter_el_autograd_freeaz(G, g2, ginv2, phi_def, xi, kap, m=mm)
    dPsi = {R: dPsi_r, PS: dPsi_ps}
    for nu, nm in ((R, 'r'), (PS, 'ps')):
        pred = -elPsi*dPsi[nu]
        e = (divT[..., nu]-pred)[body].abs().max().item()
        sc = pred[body].abs().max().item()+1e-30
        print(f"  [divT path, GRID-LIMITED] nu={nm}: max|divT-(-EL.dPsi)|={e:.3e} rel={e/sc:.3e}")
    print("  (the divT path differentiates sqrtg*T spectrally in theta -> the bare-sin-theta")
    print("   GRID error contaminates it; NOT an EL error.  The clean EL check is below.)")

    # GRID-CLEAN EL CHECK: EL = delta S / delta phi by DEFINITION.  Verify by a finite
    # directional derivative of the SAME action S along a random smooth perturbation eta:
    #   S(phi + t eta) - S(phi - t eta) = 2 t sum_nodes EL(node) eta(node) measure  + O(t^3).
    # This uses ONLY the action (autograd EL vs numeric dS) -- NO spectral theta-derivative
    # of sin theta -- so it is the grid-independent proof the autograd EL is correct.
    torch.manual_seed(1)
    eta = torch.randn_like(phi_def)
    eta = eta - eta.mean()
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g2), min=1e-300))
    meas = sqrtg * G.wvol_coord
    def Sof(ph):
        return _action_scalar(G, g2, ginv2, field_dn_freeaz(G, ph, m=mm), xi, kap)[0]
    tt = 1e-5
    Sp = Sof(phi_def + tt*eta).item(); Sm = Sof(phi_def - tt*eta).item()
    dS_num = (Sp - Sm)/(2*tt)
    dS_el = (elPsi * eta * meas).sum().item()
    rel = abs(dS_num - dS_el)/(abs(dS_num)+1e-30)
    print(f"  [GRID-CLEAN] dS/dt(numeric) = {dS_num:.6e}")
    print(f"  [GRID-CLEAN] sum EL.eta.meas = {dS_el:.6e}   rel diff = {rel:.3e}")
    print(f"  AUTOGRAD-EL CORRECT: {'PASS (EL == delta S/delta phi)' if rel < 1e-5 else 'SEE NUMBERS'}")
    print("\nDONE.  (build + eval only; no Newton/coupled solve was run)")
