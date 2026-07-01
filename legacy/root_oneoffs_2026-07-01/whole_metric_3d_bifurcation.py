#!/usr/bin/env python3
"""
whole_metric_3d_bifurcation.py -- THE BIFURCATION TEST: smallest singular values of the
FIELD-EQUATION Jacobian J = d(G^mu_nu - kappa8 T^mu_nu)/d(metric, matter) around the
corrected #56 round soliton, with the OFF-DIAGONAL metric sector LIVE.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md realization (A), honest binary at the existence level.

WHY THIS IS THE RIGHT OBJECT (correcting the action-Hessian misstep):
The second variation of the Einstein-Hilbert ACTION is INDEFINITE (the conformal-factor
mode is unbounded below) -- its huge negative eigenvalues are NOT physical bifurcations.
The correct bifurcation criterion linearizes the FIELD EQUATIONS themselves:
      F(u) = G^mu_nu[g] - kappa8 T^mu_nu[n,g] = 0 ,   u = (metric, matter) DOF.
A NEW solution branch (shaped / non-axisymmetric / off-diagonal type) bifurcates off the
round soliton exactly where the Jacobian  J = dF/du  becomes SINGULAR (a zero singular
value sigma_min -> 0, with a localized null mode).  This is the implicit-function-theorem
criterion; it is the same operator the verified radial test used (the Theta-EL
linearization there had min|eig|~0.11, bounded from 0 = no bifurcation), now EXTENDED to
the full metric incl. the 6 off-diagonals and angular-shape matter modes.

J is never formed densely; sigma_min^2 = smallest eigenvalue of J^T J, obtained matrix-
free by Lanczos on  v -> J^T(J v)  via autograd JVP/VJP of the VALIDATED residual
(whole_metric_3d_newton.F_of_x), restricted to the regular body (core/axis/seal frozen),
geometry-weighted.  CANNOT be fooled by the coordinate spike (frozen) or the conformal
mode (we linearize equations, not an action).

OUTPUT: sigma_min of J across the depth dial and across which DOF are freed (off-diagonal
only; full metric; +matter shape).  sigma_min bounded away from 0 = round soliton locally
unique, NO new branch.  sigma_min -> 0 with a localized null mode = bifurcation to NEW
structure (a shaped/off-diagonal type).  Gauge modes give exact zeros distinguished by
being pure-coordinate (we test by their residual under a gauge projection).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3

import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW


# ===========================================================================
# Residual as a function of the FULL DOF vector u = (free metric x, free Th).
# Built on the VALIDATED NW.F_of_x (metric) + the matter residual = mixed Einstein at
# the matter's own equation is already inside F; the matter EL is enforced jointly because
# T depends on Th.  We add Th to the DOF and let the SAME residual F (which depends on Th
# through T) carry the coupling; plus the explicit matter-EL residual so the matter
# direction is constrained.
# ===========================================================================
def matter_action_density(g, Th, G):
    ginv = core.metric_inverse(g)
    n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=DEV)
    dn[..., R, :]  = S.d_dx(n, G['hr'], 3)
    dn[..., TH, :] = S.d_dx(n, G['hth'], 4)
    dn[..., PS, :] = S.d_dx(n, G['hps'], 5)
    Gmn = mat.field_metric(dn)
    Lf, _, _, _ = mat.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    return sqrtg*Lf


def matter_EL_field(g, Th, G):
    """dS_matter/dTh as a FIELD (same shape as Th), via inner autograd.  create_graph so
    the OUTER JVP/VJP can differentiate through it."""
    Thl = Th.requires_grad_(True)
    dens = matter_action_density(g, Thl, G)
    grad, = torch.autograd.grad(dens.sum(), Thl, create_graph=True)
    return grad


def build_residual_fn(g_base, Th_base, kap8, G, mask_g, mask_th, eqmask, wgeom):
    ng = NW.x_from_g(g_base, mask_g).numel()
    has_th = bool(mask_th.any())

    def F(u):
        g = NW.g_from_x(u[:ng], g_base, mask_g)
        if has_th:
            Th = Th_base.clone()
            Th = Th.index_put((mask_th.nonzero(as_tuple=True)), u[ng:])
        else:
            Th = Th_base
        parts = []
        # Einstein residual (geometry-weighted) at the free metric eqs
        if eqmask.any():
            Res = NW.residual_of_g(g, mat.hedgehog_n(Th, G['Tht'], G['Ps']), kap8, G)
            Rflat = torch.zeros(Res.shape[:-2]+(10,), device=DEV)
            for k, (a, b) in enumerate(NW.SYM_IDX):
                Rflat[..., k] = 0.5*(Res[..., a, b]+Res[..., b, a])
            Rflat = Rflat*wgeom[..., None]
            parts.append(Rflat[eqmask])
        # matter EL residual at the free Th points
        if has_th:
            el = matter_EL_field(g, Th, G)
            parts.append((el*wgeom)[mask_th])
        return torch.cat(parts) if parts else g.new_zeros(0)

    return F, ng


def n_of(g, Th, G):
    return mat.hedgehog_n(Th, G['Tht'], G['Ps'])


# ===========================================================================
# sigma_min(J) via Lanczos on J^T J, matrix-free.
# ===========================================================================
def sigma_min_max(F, u0, k=60, seed=0):
    u0 = u0.detach()

    def Jv(v):
        _, jv = torch.autograd.functional.jvp(F, (u0,), (v,), strict=False)
        return jv

    def JTw(w):
        u = u0.clone().requires_grad_(True)
        Fz = F(u)
        g, = torch.autograd.grad(Fz, u, grad_outputs=w, retain_graph=False)
        return g

    def JTJ(v):
        return JTw(Jv(v))

    # Lanczos on the SPD operator J^T J -> eigenvalues = sigma^2
    torch.manual_seed(seed)
    n = u0.numel()
    q = torch.randn(n, device=DEV); q /= q.norm()
    Q = [q]; alpha = []; beta = []; qprev = torch.zeros_like(q); b = 0.0
    for j in range(k):
        w = JTJ(Q[-1])
        a = (w@Q[-1]).item(); alpha.append(a)
        w = w - a*Q[-1] - b*qprev
        for qq in Q:
            w = w - (w@qq)*qq
        b = w.norm().item(); beta.append(b)
        if b < 1e-14:
            break
        qprev = Q[-1]; Q.append(w/b)
    Tm = torch.diag(torch.tensor(alpha, device=DEV))
    for i in range(len(beta)-1):
        Tm[i, i+1] = beta[i]; Tm[i+1, i] = beta[i]
    ev = torch.linalg.eigvalsh(Tm).clamp(min=0)
    sig = ev.sqrt()
    return sig, JTJ
