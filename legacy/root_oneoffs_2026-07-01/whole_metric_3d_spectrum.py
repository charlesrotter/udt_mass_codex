#!/usr/bin/env python3
"""
whole_metric_3d_spectrum.py -- THE LINEARIZED WHOLE-METRIC OPERATOR and its spectrum
around the corrected #56 round soliton, with ALL metric perturbations live (incl. the
off-diagonal time-row / twist sector and angular-shape matter modes).

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md realization (A) -- the honest binary at the EXISTENCE
level.

WHY THIS IS THE RIGHT TOOL (zoom-out, charter "no tunnel vision"):
A global nonlinear residual-Newton on the full metric is ill-conditioned (the deep-core
/ near-axis coordinate spike dominates |F|; diagnosed & committed).  But the HONEST
BINARY question -- "does the unreduced metric produce NEW structure / distinct types /
discreteness that the round continuum did not?" -- is exactly a BIFURCATION question, and
bifurcation is decided by the LINEARIZED operator's SPECTRUM around the known round
solution:
  * a ZERO mode of the linearized Einstein-matter operator = a marginal direction =
    a bifurcation to a NEW branch (shaped/non-axisymmetric/off-diagonal type).
  * NO zero mode across the dial = the round soliton is locally UNIQUE; no shaped types
    branch off; the continuum stays one round family.
  * a sign change of the lowest eigenvalue as the depth dial varies = a fold / new branch.
This is rigorous, tractable (ONE linear operator), uses ONLY the validated engine
(autograd of the exact action + Einstein residual), and CANNOT be fooled by the
coordinate spike (we build the operator in the regular body and weight by geometry).

THE OPERATOR.  Stationary action S[g,n] (Einstein-Hilbert + L2+L4 matter).  Its second
variation Hessian H at the round soliton is the linearized Einstein-matter operator.  We
do NOT form H densely (millions of DOF); we compute its action H@v by autograd
(double-backward of the gradient), restrict to the FREE perturbation space (off-diagonals
+ shape modes in the regular body, core/axis/seal frozen by BC), and extract the LOWEST
eigenvalues by Lanczos (matrix-free, on the V100).  A near-zero lowest eigenvalue would
signal a bifurcation -> new structure.

We use the ENERGY functional E = integral sqrt(-g) ( -R/(2 kappa8) + (L2+L4) ) as the
action whose stationary point is the soliton (varying g gives Einstein, varying n gives
the matter EL).  Its Hessian is the object whose null space = marginal deformations.
For the matter-only sub-block this reproduces the verified radial min|eig|~0.11 (a
cross-check).  The NEW content is the off-diagonal metric block.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3
XI = 1.0
KAP = 1.0

import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW


# ===========================================================================
# THE ACTION whose stationary point is the soliton (per unit grid-cell; dV constant).
#   S = sum_x sqrt(-g) [ -R/(2 kappa8) + L_matter ]
# Varying g -> Einstein G_mn = kappa8 T_mn ; varying n -> matter EL.  (We carry the
# matter as the hedgehog profile Th; the metric as the full symmetric tensor.)
# ===========================================================================
def action(g, Th, kap8, G):
    ginv = core.metric_inverse(g)
    # geometry: Ricci scalar from the validated engine
    dg = torch.zeros(*g.shape[:-2], 4, 4, 4, device=DEV)
    dg[..., R, :, :]  = S.d_dx(g, G['hr'], 3)
    dg[..., TH, :, :] = S.d_dx(g, G['hth'], 4)
    dg[..., PS, :, :] = S.d_dx(g, G['hps'], 5)
    Gamma = core.christoffel(ginv, dg)
    dGamma = torch.zeros(*Gamma.shape[:-3], 4, 4, 4, 4, device=DEV)
    dGamma[..., R, :, :, :]  = S.d_dx(Gamma, G['hr'], 3)
    dGamma[..., TH, :, :, :] = S.d_dx(Gamma, G['hth'], 4)
    dGamma[..., PS, :, :, :] = S.d_dx(Gamma, G['hps'], 5)
    _, Ric, Rscal = core.einstein(g, ginv, Gamma, dGamma)
    # matter
    n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=DEV)
    dn[..., R, :]  = S.d_dx(n, G['hr'], 3)
    dn[..., TH, :] = S.d_dx(n, G['hth'], 4)
    dn[..., PS, :] = S.d_dx(n, G['hps'], 5)
    Gmn = mat.field_metric(dn)
    Lm, _, _, _ = mat.lagrangian(ginv, Gmn, XI, KAP)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    dens = sqrtg*(-Rscal/(2*kap8) + Lm)
    # restrict the SUM to the regular body (mask out coordinate-singular core/axis/edges)
    return dens


# ===========================================================================
# The DOF vector u = (free metric components, free Th) in the regular body.
# ===========================================================================
def pack(g, Th, mask_g, mask_th):
    xg = NW.x_from_g(g, mask_g)
    xt = Th[mask_th]
    return torch.cat([xg, xt]), xg.numel()


def unpack(u, ng, g_base, Th_base, mask_g, mask_th):
    g = NW.g_from_x(u[:ng], g_base, mask_g)
    Th = Th_base.clone()
    Th[mask_th] = u[ng:]
    return g, Th


# ===========================================================================
# Body-mask weighting for the action SUM (so the Hessian is the regular-body operator).
# ===========================================================================
def body_mask(G, rcore=1.0):
    m = torch.zeros(G['Nr'], G['Nth'], G['Nps'], dtype=torch.bool, device=DEV)
    rok = (G['rg'] > G['rc']+rcore) & (G['rg'] < G['ri']-0.5)
    m[rok, 4:-4, :] = True
    return m


# ===========================================================================
# Hessian-vector product H@v by double-backward of the action restricted to the body.
# ===========================================================================
def make_HVP(g_base, Th_base, kap8, G, mask_g, mask_th, bmask):
    ng = NW.x_from_g(g_base, mask_g).numel()
    u0, _ = pack(g_base, Th_base, mask_g, mask_th)

    def scalar_action(u):
        g, Th = unpack(u, ng, g_base, Th_base, mask_g, mask_th)
        dens = action(g, Th, kap8, G)
        return (dens*bmask).sum()

    def Hv(v):
        u = u0.detach().clone().requires_grad_(True)
        s = scalar_action(u)
        g1, = torch.autograd.grad(s, u, create_graph=True)
        hv, = torch.autograd.grad(g1, u, grad_outputs=v, retain_graph=False)
        return hv.detach()

    return Hv, ng, u0


# ===========================================================================
# Lanczos for the lowest / most-negative eigenvalues of the symmetric H.
# ===========================================================================
def lanczos_extremes(Hv, n, k=80, seed=0):
    torch.manual_seed(seed)
    q = torch.randn(n, device=DEV); q /= q.norm()
    Q = [q]; alpha = []; beta = []
    qprev = torch.zeros_like(q); b = 0.0
    for j in range(k):
        w = Hv(Q[-1])
        a = (w@Q[-1]).item(); alpha.append(a)
        w = w - a*Q[-1] - b*qprev
        # full reorth (small k)
        for qq in Q:
            w = w - (w@qq)*qq
        b = w.norm().item(); beta.append(b)
        if b < 1e-12:
            break
        qprev = Q[-1]; Q.append(w/b)
    Tm = torch.diag(torch.tensor(alpha, device=DEV))
    for i in range(len(beta)-1):
        Tm[i, i+1] = beta[i]; Tm[i+1, i] = beta[i]
    ev = torch.linalg.eigvalsh(Tm)
    return ev
