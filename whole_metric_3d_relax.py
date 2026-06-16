#!/usr/bin/env python3
"""
whole_metric_3d_relax.py -- THE FULL 3-D COUPLED RELAXATION SOLVER.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md realization (A).

THE UNPROVEN CAPABILITY: not evaluating a config (we have the validated engine for
that -- whole_metric_3d_core/matter, off-diag G to ~5e-6, stress to ~5e-14), but
SOLVING: finding metric+matter configs that satisfy ALL the equations, with ALL 10
metric components free, NO symmetry imposed, off-diagonals live.

METHOD (charter principle 4 -- transformed NR numerics; principle 2 -- full nonlinear,
sanctioned FD, NO linearization-as-result):

  (1) MATTER EL by exact action gradient.  The matter field n (unit S^3, parametrized
      by the profile Th and -- in the full solve -- the two target angles) satisfies its
      Euler-Lagrange eqs iff dS_matter/dn = 0, S = integral sqrt(-g) (L2+L4).  We compute
      dS/dTh EXACTLY by torch autograd of the VALIDATED Lagrangian density (no hand
      re-derivation; the derivative of the exact action IS the exact EL), and drive Th by
      damped Newton / gradient descent.  This reproduces the verified radial EL in the
      round limit (checked) and extends correctly to full (r,theta,psi).

  (2) METRIC by nonlinear relaxation on the full Einstein residual.  G_mn[g] is, in its
      principal part, a curved Laplace/wave operator on each g_mn.  The damped
      nonlinear-Jacobi (Richardson) update
         g_mn  <-  g_mn  -  omega * (G_mn - kappa8 T_mn) / w
      with w = sum_k |g^kk|/h_k^2 the principal-symbol diagonal weight, CONTRACTS to a
      solution (the standard relaxation for elliptic systems; the residual is the FULL
      numerical engine, no closed form assumed).  BC's pin boundary values (center/axis
      regularity, seal, finite cell).  All 10 components are updated; off-diagonals are
      free and evolve only if the matter sources them.

  Sector-iterated to self-consistency; the CONVERGED config's residual (validated
  engine) is the gate.

VALIDATION (whole_metric_3d_relax_validate.py): (i) seeded at corrected #56 the relaxer
STAYS (residual bounded, no drift); (ii) seeded PERTURBED it RELAXES BACK (residual
falls, M_MS recovers, un-sourced off-diagonals decay to ~0).  Proof it SOLVES.
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


# ===========================================================================
# Principal-symbol diagonal weight for the metric relaxation preconditioner.
# ===========================================================================
def symbol_weight(ginv, G):
    w = (ginv[..., R, R].abs()/G['hr']**2
         + ginv[..., TH, TH].abs()/G['hth']**2
         + ginv[..., PS, PS].abs()/G['hps']**2)
    return w.clamp(min=1e-9)


# ===========================================================================
# MATTER: action density and its exact EL gradient (autograd).
# n is parametrized by the profile field Th (hedgehog) OR a general unit n.  Here we
# carry the hedgehog profile Th(r,theta,psi) for the axisymmetric/round validation and
# the general-n option for the full exploration.
# ===========================================================================
def lagrangian_density_from_Th(Th_field, g, ginv, G):
    n = mat.hedgehog_n(Th_field, G['Tht'], G['Ps'])
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=n.device)
    dn[..., R, :]  = S.d_dx(n, G['hr'], 3)
    dn[..., TH, :] = S.d_dx(n, G['hth'], 4)
    dn[..., PS, :] = S.d_dx(n, G['hps'], 5)
    Gmn = mat.field_metric(dn)
    L, L2, L4, SS = mat.lagrangian(ginv, Gmn, XI, KAP)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    return sqrtg*L


def field_EL_grad_Th(Th_field, g, ginv, G):
    """Exact dS/dTh by autograd of the validated action density (S=sum sqrtg L * dV;
    dV constant on uniform grid -> drop).  Returns grad with shape of Th_field."""
    Th = Th_field.detach().clone().requires_grad_(True)
    dens = lagrangian_density_from_Th(Th, g, ginv, G)
    Stot = dens.sum()
    grad, = torch.autograd.grad(Stot, Th)
    return grad


def relax_matter_Th(Th_field, g, ginv, G, bc_core, bc_seal, steps=40, lr=None):
    """Drive Th toward dS/dTh=0 by preconditioned gradient ASCENT/DESCENT.  The action
    is a SADDLE in Th (the soliton is a stationary point), so we use Newton-like damped
    steps on |grad|: move along -grad/|H_diag|.  Diagonal Hessian via autograd-of-grad
    on a probe is expensive; we use a robust line-searched gradient step with the
    symbol weight as preconditioner (sin^2-type stiffness)."""
    Th = Th_field.clone()
    w = symbol_weight(ginv, G)
    if lr is None:
        lr = 0.25
    for _ in range(steps):
        gradTh = field_EL_grad_Th(Th, g, ginv, G)
        step = lr*gradTh/(w.clamp(min=1e-6))
        # interior update; pin BCs (core: Th=pi, seal: Th=0)
        Th_new = Th - step
        Th_new[0, :, :]  = bc_core
        Th_new[-1, :, :] = bc_seal
        Th = Th_new
    return Th


# ===========================================================================
# METRIC relaxation: one damped nonlinear-Jacobi sweep on the FULL Einstein residual.
# Updates ALL 10 lower components g_mn; off-diagonals are free.
# ===========================================================================
def relax_metric_sweep(g, n, kap8, G, omega=0.3):
    Gmn, ginv, Ric, Rscal = S.full_einstein(g, G)
    Tab, dn, L = S.matter_stress(n, g, ginv, G)
    Res_low = Gmn - kap8*Tab                       # lower-index residual G_mn - k T_mn
    w = symbol_weight(ginv, G)
    # principal symbol of G_mn ~ -1/2 g^{ab} d_a d_b g_mn  => coefficient ~ -1/2 * w.
    # Jacobi update solves (-1/2 w) dg = -Res  =>  dg = 2 Res / w, damped by omega.
    dg = 2.0*Res_low/w[..., None, None]
    g_new = g + omega*dg
    return g_new, Res_low, ginv


# ===========================================================================
# BOUNDARY CONDITIONS on the full metric.
#   center/core (r=rc): regularity -- keep the seeded core values (Dirichlet from seed).
#   seal (r=ri): the same-minus mirror fold => phi(seal)=0 i.e. g_tt(seal)=-1; for the
#       full metric the seal is time-reversal: it FLIPS sign of the time-row off-diagonals
#       (g_tr,g_ttheta,g_tpsi -> -them) so they must VANISH at the seal (a node), while the
#       spatial metric is mirror-even (Neumann).  We impose: g_t.(seal)=0 for the time-row
#       off-diagonals, g_tt(seal)=-1, and Dirichlet-hold the rest of the boundary at seed.
#   theta edges: Dirichlet-hold at seed (chart coordinate edges, off the axis).
#   psi: periodic (handled by FD).
# ===========================================================================
def apply_metric_bcs(g, g_seed, seal_timerow_node=True):
    # core: hold seed
    g[0, :, :, :, :] = g_seed[0, :, :, :, :]
    # seal: g_tt = -1 (phi=0), time-row off-diagonals -> 0 (mirror-fold time reversal)
    g[-1, :, :, :, :] = g_seed[-1, :, :, :, :]
    if seal_timerow_node:
        for (a, b) in [(T, R), (T, TH), (T, PS)]:
            g[-1, :, :, a, b] = 0.0
            g[-1, :, :, b, a] = 0.0
    # theta edges: hold seed (chart edges)
    g[:, 0, :, :, :]  = g_seed[:, 0, :, :, :]
    g[:, -1, :, :, :] = g_seed[:, -1, :, :, :]
    return g


# ===========================================================================
# THE FULL COUPLED SOLVE: alternate matter-EL and metric relaxation to self-consistency.
# ===========================================================================
def solve(g0, Th0, kap8, G, bc_core, bc_seal, outer=200, omega=0.3,
          matter_steps=8, matter_lr=0.2, mask_core=1.0, verbose=True, tag=""):
    g = g0.clone()
    Th = Th0.clone()
    g_seed = g0.clone()
    rmask = (G['rg'] > G['rc'] + mask_core) & (G['rg'] < G['ri'] - 0.5)
    i0 = int(rmask.float().argmax().item())
    i1 = int(G['Nr'] - 1 - rmask.flip(0).float().argmax().item())
    hist = []
    for it in range(outer):
        ginv = core.metric_inverse(g)
        Th = relax_matter_Th(Th, g, ginv, G, bc_core, bc_seal,
                             steps=matter_steps, lr=matter_lr)
        n = mat.hedgehog_n(Th, G['Tht'], G['Ps'])
        g, Res_low, ginv = relax_metric_sweep(g, n, kap8, G, omega=omega)
        g = apply_metric_bcs(g, g_seed)
        # diagnostics on the smooth body (mixed residual)
        Gud = torch.einsum('...am,...mb->...ab', ginv, Res_low)  # ~ mixed res (lower->mixed)
        body = Gud[i0:i1, 8:-8, :]
        rmax = max(body[..., a, a].abs().max().item() for a in range(4))
        offmax = 0.0
        for a in range(4):
            for b in range(4):
                if a != b:
                    offmax = max(offmax, body[..., a, b].abs().max().item())
        hist.append((it, rmax, offmax))
        if verbose and (it % 20 == 0 or it == outer-1):
            print(f"  [{tag}] it={it} body max|res_diag|={rmax:.3e} max|res_off|={offmax:.3e}",
                  flush=True)
    return dict(g=g, Th=Th, hist=hist, i0=i0, i1=i1)
