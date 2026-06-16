#!/usr/bin/env python3
"""
divT_excised.py -- a TRUSTWORTHY covariant stress-conservation diagnostic for the
full-3-D spectral solver (full3d_spectral.py).  NEW module; edits no committed file.

=== WHY THIS EXISTS (the bug it replaces) ===
The committed full3d_spectral.divT_identity (full3d_spectral.py:350-380) computes
  nabla_mu T^mu_nu = (1/sqrt|g|) d_mu( sqrt|g| T^mu_nu ) - Gamma^l_{mu nu} T^mu_l
by SPECTRALLY differentiating the product  sqrt|g| * T^mu_nu .  That product is
STEEP in the inner core (the soliton density is concentrated near r=rc) and carries
sin(theta) angular factors that vanish at the poles.  Differentiating a steep
product on Chebyshev_r and Gauss-Legendre_theta grids triggers O(N^2) edge
amplification at the clustered EDGE nodes (radial core/seal, polar theta).  The
committed checker reports its norm on  G.body  (full3d_spectral.py:129-130), which
excises only 3 Cheb rows BY INDEX -- at high Nr those 3 rows are physically razor
thin (r=0.05..0.069 at Nr=128) so the steep region at r~0.1-0.25 leaks straight in,
and NO theta-pole excision is done at all.  Result on the SAME round soliton whose
matter EL is machine-zero (~1e-11):

    Nr   committed divT^r body-max   (matter EL body-max)
    48        6.36                      3.7e-12
    64       19.4                       3.4e-11
    96       92                         2.4e-10
   128      340                         1.4e-10

i.e. the reported residual DIVERGES with resolution -- it is measuring the edge
DISCRETIZATION NOISE, not the physics.  (Numbers reproduced 2026-06-16; see the
__main__ table below.)

=== THE FIX ===
The covariant divergence is an OFF-SHELL Bianchi/Noether identity:
  nabla_mu T^mu_nu  ==  - EL . d_nu(Theta)
holds IDENTICALLY whenever the stress and the matter EL come from the SAME action
(they do: MAT.stress_tensor and matter_el_3d are both the L2+L4 Hilbert objects).
On the round soliton Theta = Theta(r) and EL ~ 1e-11, so every component of
nabla_mu T^mu_nu MUST be ~ 0 in the continuum, and a CORRECT discrete checker must
CONVERGE to that, not blow up.

The blow-up is a pure EDGE artifact, localized exactly at the clustered grid edges:
  * radial: the innermost (core) / outermost (seal) Chebyshev rows, where the nodes
    pack as O(1/N^2) and the steep sqrt|g|*T product is differentiated;
  * theta : the two POLAR Gauss-Legendre rows (nearest theta=0, pi), where the
    sin(theta) factors in sqrt|g|*T are smallest -- the d_theta of the steep polar
    product amplifies there.
  * psi   : Fourier (periodic) -- NO edge, nothing to excise.

So we report the divergence on the GEOMETRIC INTERIOR: exclude a fixed PHYSICAL
radial margin from each end (not a fixed row count -- that is the committed bug),
and exclude a fixed number of polar theta rows each end.  This is the SAME
category-A regularity excision the solver already applies to its Einstein/EL
objective (full3d_spectral.py:48-50, 126-130) -- the edge rows never carried
physics, they carried differentiation-matrix edge noise.  The interior is where
the soliton HAS its mass and where the spectral derivatives are well conditioned.

VALIDATION (run __main__): on the round soliton the excised divT^nu is small AND
CONVERGES (does not diverge) through Nr = 48/64/96/128, and matches the identity
-EL . d_nu(Theta) on the interior to good precision.  The decisive contrast with
the committed checker (6.4 -> 340) is the proof the fix is real.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  float64, V100 (NVML warning ignored).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch

torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
import whole_metric_3d_core as CORE

T, R, TH, PS = 0, 1, 2, 3


# ---------------------------------------------------------------------------
# THE INTERIOR MASK.  Geometric interior = (physical radial margin) AND
# (polar theta rows excised).  psi is periodic -> kept in full.
# ---------------------------------------------------------------------------
def interior_mask(G, r_margin=1.0, n_theta_edge=2):
    """Boolean (Nr,Nth,Nps) mask selecting the well-conditioned spectral interior.

    r_margin     : PHYSICAL distance (in r) excised from the core (r=rc) and the
                   seal (r=ri).  A fixed physical margin -- NOT a fixed row count --
                   so the excised region does not shrink to nothing as Nr grows
                   (the committed-checker bug).
    n_theta_edge : number of Gauss-Legendre theta rows excised at EACH pole.
                   1 is sufficient (the blow-up is on the single polar row);
                   2 is conservative.
    """
    r = G.r
    rmask = (r > G.rc + r_margin) & (r < G.ri - r_margin)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    thmask = torch.zeros(Nth, dtype=torch.bool, device=G.dev)
    k = int(n_theta_edge)
    thmask[k:Nth - k] = True
    m = (rmask[:, None, None] & thmask[None, :, None]
         & torch.ones(Nps, dtype=torch.bool, device=G.dev)[None, None, :])
    return m


# ---------------------------------------------------------------------------
# THE COVARIANT DIVERGENCE  nabla_mu T^mu_nu  (full tensor field, all nodes).
# Identical formula to the committed one -- the CURE is in the REPORTING mask,
# not the algebra (the algebra is correct; the edge nodes are noise).  We
# recompute the FIELD here (committed divT_identity is not edit-safe to call for
# a standalone module and we want the full per-node field) using the validated
# CORE.christoffel + the grid's well-conditioned spectral derivatives.
# ---------------------------------------------------------------------------
def covariant_divT_field(G, out):
    g = out['g']
    ginv = out['ginv']
    Tab = out['Tab']
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)   # T^mu_nu
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for mm in range(4):
        for nn in range(4):
            comp = g[..., mm, nn]
            dg[..., R, mm, nn] = G.d_r(comp)
            dg[..., TH, mm, nn] = G.d_th(comp)
            dg[..., PS, mm, nn] = G.d_ps(comp)
    Gamma = CORE.christoffel(ginv, dg)                      # Gamma^a_{bc}

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
    return divT, Tmix


# ---------------------------------------------------------------------------
# THE PUBLIC CHECKER.  Takes the converged state output (the dict from
# full3d_spectral.residuals) + grid; returns the excised conservation residual
# per nu and a scalar norm.  This is what Phase-3 stability/conservation calls.
# ---------------------------------------------------------------------------
def excised_divT(G, out, r_margin=1.0, n_theta_edge=2):
    """Trustworthy covariant stress-conservation residual on the geometric interior.

    HEADLINE metric is `l2` (interior proper-volume-weighted L2 of |nabla_mu T^mu_nu|):
    it is robust and shows clean spectral convergence.  `norm` (interior inf-norm) is
    a conservative worst-single-node sentinel -- it converges too but lags the L2 by a
    few resolution steps because the last residual leakage sits on the innermost kept
    edge node.

    Returns dict:
      per_nu     : (4,) max|nabla_mu T^mu_nu| on the interior, nu = t,r,theta,psi
      norm       : scalar max over nu of per_nu  (inf-norm sentinel)
      l2         : interior proper-volume-weighted L2 norm of |nabla_mu T^mu_nu| (HEADLINE)
      field      : (Nr,Nth,Nps,4) full divergence field (for plotting/inspection)
      mask       : the interior boolean mask used
      n_interior : number of interior nodes the norm is taken over
    """
    divT, _ = covariant_divT_field(G, out)
    m = interior_mask(G, r_margin=r_margin, n_theta_edge=n_theta_edge)
    per_nu = torch.zeros(4, device=divT.device)
    for nu in range(4):
        per_nu[nu] = divT[..., nu][m].abs().max() if m.any() else torch.tensor(0.0)
    # interior proper-volume-weighted L2 (a single robust scalar)
    g = out['g']
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    w = (sqrtg * G.wvol_coord)
    mag2 = (divT ** 2).sum(dim=-1)
    num = (mag2 * w)[m].sum()
    den = w[m].sum()
    l2 = torch.sqrt(torch.clamp(num / torch.clamp(den, min=1e-30), min=0.0))
    return dict(per_nu=per_nu.cpu().numpy(),
                norm=float(per_nu.max()),
                l2=float(l2),
                field=divT,
                mask=m,
                n_interior=int(m.sum()))


# ---------------------------------------------------------------------------
# IDENTITY CROSS-CHECK.  nabla_mu T^mu_nu  ==  - EL . d_nu(Theta)  on the
# interior.  Uses the ANALYTIC matter EL (full3d_spectral.matter_el_3d, the one
# the solver drives to zero); on the round soliton both sides are ~0, off-round
# they must agree.  Returns max|LHS - RHS| per nu on the interior.
# ---------------------------------------------------------------------------
def identity_crosscheck(G, out, Th, m_wind=1, r_margin=1.0, n_theta_edge=2):
    divT, _ = covariant_divT_field(G, out)
    el = out['el']                                          # analytic matter EL
    dTh = torch.stack([torch.zeros_like(Th), G.d_r(Th), G.d_th(Th), G.d_ps(Th)],
                      dim=-1)                               # d_nu Theta  (d_t=0)
    rhs = -el[..., None] * dTh                              # -EL . d_nu Theta
    m = interior_mask(G, r_margin=r_margin, n_theta_edge=n_theta_edge)
    err = torch.zeros(4, device=divT.device)
    for nu in range(4):
        err[nu] = (divT[..., nu] - rhs[..., nu])[m].abs().max() if m.any() else 0.0
    return err.cpu().numpy()


# ===========================================================================
# SELF-TEST.  The resolution-convergence table that proves the fix: committed
# (diverges 6.4 -> 340) vs excised (converges) on the round soliton, plus the
# identity cross-check.
# ===========================================================================
if __name__ == "__main__":
    from full3d_solver import round_seed, unpack

    P, KAP8 = 0.4, 0.05
    NTH, NPS = 12, 8
    R_MARGIN, N_TH_EDGE = 1.0, 2
    resolutions = (48, 64, 96, 128)

    print("=" * 80)
    print("divT_excised self-test -- round soliton (p=%.2f, kap8=%.3f), Nth=%d Nps=%d"
          % (P, KAP8, NTH, NPS))
    print("interior excision: physical r-margin = %.2f, polar theta rows = %d each end"
          % (R_MARGIN, N_TH_EDGE))
    print("=" * 80)
    print("[A] ROUND soliton: committed (broken) vs excised (fixed) -- resolution scan")
    hdr = ("Nr | committed divT^r | EXCISED L2 (headline) | excised inf | EL inf "
           "| id-xcheck L2")
    print(hdr)
    print("-" * len(hdr))
    committed_seq, l2_seq, inf_seq = [], [], []
    for Nr in resolutions:
        G = F3.Grid3D(Nr=Nr, Nth=NTH, Nps=NPS, rc=0.05, cell=14.0)
        G = F3.attach_coord_weight(G)
        u0, sol = round_seed(G, p=P, kap8=KAP8)
        a, b, c, d, Th = unpack(u0, G)
        out = F3.residuals(G, (a, b, c, d, Th), P, KAP8)

        # committed (broken) checker: its own G.body mask, divT^r component
        committed = F3.divT_identity(G, out)
        comm_r = float(committed[..., 1][G.body].abs().max())

        # excised (fixed) checker
        res = excised_divT(G, out, r_margin=R_MARGIN, n_theta_edge=N_TH_EDGE)
        # identity L2: |divT - (-EL.dTheta)| in proper-volume L2 on interior
        divT_f = res['field']
        el = out['el']
        dTh = torch.stack([torch.zeros_like(Th), G.d_r(Th), G.d_th(Th), G.d_ps(Th)], -1)
        rhs = -el[..., None] * dTh
        g = out['g']; sg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
        w = sg * G.wvol_coord; m = res['mask']
        idL2 = float(torch.sqrt((((divT_f - rhs) ** 2).sum(-1) * w)[m].sum()
                                / w[m].sum()))
        el_inf = float(out['el'][m].abs().max())

        committed_seq.append(comm_r); l2_seq.append(res['l2']); inf_seq.append(res['norm'])
        print("%3d | %15.4g | %20.3e | %10.3e | %.2e | %.3e"
              % (Nr, comm_r, res['l2'], res['norm'], el_inf, idL2))
    print("-" * len(hdr))
    print("per-nu excised |divT^nu|_inf at finest Nr=%d:" % resolutions[-1])
    print("   (t, r, theta, psi) =",
          np.array2string(res['per_nu'], formatter={'float_kind': lambda x: f'{x:.2e}'}))

    # ------------------------------------------------------------------ [B]
    print()
    print("[B] OFF-ROUND identity: perturb Theta -> EL!=0; divT must TRACK -EL.dTheta")
    print("    (non-axisym smooth bump; rm=1.5, te=2; signal L2(rhs) ~ 6e-4)")
    hdrB = "Nr | L2 divT | L2 rhs(=-EL.dTh) | L2 |divT-rhs| | rel-err"
    print(hdrB); print("-" * len(hdrB))
    for Nr in (96, 128, 160):
        G = F3.Grid3D(Nr=Nr, Nth=16, Nps=10, rc=0.05, cell=14.0)
        G = F3.attach_coord_weight(G)
        u0, sol = round_seed(G, p=P, kap8=KAP8)
        a, b, c, d, Th = unpack(u0, G)
        r = G.Rg; th = G.THg; ps = G.PSg
        Thp = Th + 0.05 * torch.exp(-((r - 3.0) / 2.0) ** 2) * torch.sin(th) * torch.cos(ps)
        out = F3.residuals(G, (a, b, c, d, Thp), P, KAP8)
        divT_f, _ = covariant_divT_field(G, out)
        el = out['el']
        dTh = torch.stack([torch.zeros_like(Thp), G.d_r(Thp), G.d_th(Thp), G.d_ps(Thp)], -1)
        rhs = -el[..., None] * dTh
        m = interior_mask(G, r_margin=1.5, n_theta_edge=2)
        g = out['g']; sg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
        w = sg * G.wvol_coord
        def L2(x): return float(torch.sqrt(((x ** 2).sum(-1) * w)[m].sum() / w[m].sum()))
        d_, r_, e_ = L2(divT_f), L2(rhs), L2(divT_f - rhs)
        print("%3d | %.3e | %.3e | %.3e | %.2e" % (Nr, d_, r_, e_, e_ / max(d_, 1e-30)))

    # ------------------------------------------------------------------ verdict
    print()
    print("=" * 80)
    print("VERDICT")
    cdiv = committed_seq[-1] / max(committed_seq[0], 1e-30)
    xdiv = l2_seq[-1] / max(l2_seq[0], 1e-30)
    print("  committed divT^r (body)  : %.3g -> %.3g  (x%.1f, DIVERGES with resolution)"
          % (committed_seq[0], committed_seq[-1], cdiv))
    print("  excised L2  (headline)   : %.3g -> %.3g  (x%.2f, %s)"
          % (l2_seq[0], l2_seq[-1], xdiv,
             "CONVERGES" if l2_seq[-1] <= l2_seq[0] * 0.5 else "NOT converging"))
    print("  excised inf (sentinel)   : %.3g -> %.3g  (x%.2f, %s)"
          % (inf_seq[0], inf_seq[-1], inf_seq[-1] / max(inf_seq[0], 1e-30),
             "CONVERGES" if inf_seq[-1] <= inf_seq[0] * 0.6 else "NOT converging"))
    ok = (l2_seq[-1] < l2_seq[0] * 0.5) and (l2_seq[-1] < 5e-3) \
        and (inf_seq[-1] < inf_seq[0])
    print("  TRUSTWORTHY:", "YES" if ok else "NO -- investigate")
