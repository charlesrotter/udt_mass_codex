#!/usr/bin/env python3
"""
whole_metric_3d_solver.py -- THE FULL 3-D COUPLED SOLVER for the WHOLE-METRIC solve
(realization A: full stationary soliton, ALL 10 metric components live, NO symmetry
imposed, B=1/A FREE, off-diagonals live).  This is the never-built capability: we have
the validated EVALUATOR (whole_metric_3d_core: G_mn for a general metric, off-diagonal
correct to ~5e-6; whole_metric_3d_matter: full T_mn to ~5e-14).  Here we SOLVE: find
metric + matter configurations on the (r,theta,psi) grid that satisfy ALL the equations.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND (L=sqrt(kap/xi)=1).
Frame + premise ledger: whole_metric_solve_MAP.md.

==============================================================================
THE METHOD (charter principle 4: the GR/NR corpus is TRANSFORMED numerics, not
imported new physics; principle 2: full nonlinear, sanctioned FD function-replacement,
NO linearization-as-result).

We solve the full coupled system by DAMPED NEWTON-RELAXATION on the FULL Einstein
residual  Res_mn = G_mn[g] - kappa8 T_mn[n,g]  computed by the VALIDATED 3-D engine,
plus the matter EL for the field n, sector-iterated to self-consistency.  This is
exactly the structure the corrected radial solver (radial_Bfree_soliton.py, #56,
blind-verified) uses and that PASSES the radial gate at O(h^2) -- here generalized to
the full 3-D grid with ALL components free.

  metric update : the 10 components g_mn(r,theta,psi) are driven so that the full
                  numerical Einstein residual -> 0.  We use the standard 3+1/elliptic
                  structure WHERE IT REDUCES (the (t,t)=Hamiltonian gives the radial
                  warp via Misner-Sharp; the (r,r) gives the lapse gradient; the
                  angular eqs give the angular warps), and a residual-Newton correction
                  for the full coupling incl. the off-diagonals.  No equation is dropped;
                  the engine residual of the converged config is the GATE.
  matter update : the EL for the unit field n (S^3 hedgehog generalized) -- damped
                  Newton on the profile + angular DOF.

VALIDATION GATE (mandatory, MAP sec 10.2): seeded axisymmetric/round, the 3-D solver
MUST reproduce the CORRECTED radial #56 soliton (M_MS~0.281, the profile, exterior
B=1/A) with all Einstein residuals -> 0 converging.  See whole_metric_3d_gate56.py.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3
EXP_CLAMP = 60.0

import whole_metric_3d_core as core
import whole_metric_3d_matter as mat


# ===========================================================================
# GRID.  (r,theta,psi); psi periodic.  theta kept off the axis (chart coordinate
# singularity, exactly as the validated core test).
# ===========================================================================
def mkgrid(Nr, Nth, Nps, rc, ri, th0, th1):
    rg = torch.linspace(rc, ri, Nr, device=DEV)
    thg = torch.linspace(th0, th1, Nth, device=DEV)
    psg = torch.linspace(0.0, 2*math.pi, Nps+1, device=DEV)[:-1]
    hr = (rg[1]-rg[0]).item()
    hth = (thg[1]-thg[0]).item()
    hps = 2*math.pi/Nps
    Rr, Tht, Ps = torch.meshgrid(rg, thg, psg, indexing='ij')
    return dict(rg=rg, thg=thg, psg=psg, hr=hr, hth=hth, hps=hps,
                Rr=Rr, Tht=Tht, Ps=Ps, Nr=Nr, Nth=Nth, Nps=Nps,
                rc=rc, ri=ri, th0=th0, th1=th1)


def d_dx(f, h, axis):
    # axis: 3=r, 4=theta, 5=psi.  psi periodic.
    return core.d_dx(f, h, axis, periodic=(axis == 5))


# ===========================================================================
# FULL 3-D EINSTEIN (validated engine).  Returns G_mn (lower), ginv, and Ric,R.
# ===========================================================================
def full_einstein(g, G):
    ginv = core.metric_inverse(g)
    dg = torch.zeros(*g.shape[:-2], 4, 4, 4, device=g.device)
    dg[..., R, :, :]  = d_dx(g, G['hr'], 3)
    dg[..., TH, :, :] = d_dx(g, G['hth'], 4)
    dg[..., PS, :, :] = d_dx(g, G['hps'], 5)
    Gamma = core.christoffel(ginv, dg)
    dGamma = torch.zeros(*Gamma.shape[:-3], 4, 4, 4, 4, device=g.device)
    dGamma[..., R, :, :, :]  = d_dx(Gamma, G['hr'], 3)
    dGamma[..., TH, :, :, :] = d_dx(Gamma, G['hth'], 4)
    dGamma[..., PS, :, :, :] = d_dx(Gamma, G['hps'], 5)
    Gmn, Ric, Rscal = core.einstein(g, ginv, Gamma, dGamma)
    return Gmn, ginv, Ric, Rscal


# ===========================================================================
# MATTER.  General unit field n on S^3 carried as a 4-vector (|n|=1).  We
# parametrize by a profile field Th(r,theta,psi) and TWO target angles (alpha,beta)
# that place n on S^3 -- the hedgehog is the special case where the angles are the
# coordinate angles.  For the round/axisymmetric solve the hedgehog profile suffices;
# for the full exploration we carry n directly and project to |n|=1.
# ===========================================================================
def hedgehog_field(Th_field, G):
    return mat.hedgehog_n(Th_field, G['Tht'], G['Ps'])


def matter_stress(n, g, ginv, G):
    dn = torch.zeros(*n.shape[:-1], 4, 4, device=n.device)
    dn[..., R, :]  = d_dx(n, G['hr'], 3)
    dn[..., TH, :] = d_dx(n, G['hth'], 4)
    dn[..., PS, :] = d_dx(n, G['hps'], 5)
    Tab, L, L2, L4 = mat.stress_tensor(g, ginv, dn, MAT_XI, MAT_KAP)
    return Tab, dn, L


MAT_XI = 1.0
MAT_KAP = 1.0


# ===========================================================================
# RESIDUAL of the full coupled system (the GATE quantity).
# Mixed Einstein residual  Res^mu_nu = G^mu_nu - kappa8 T^mu_nu  (the physical eqs).
# ===========================================================================
def einstein_residual_mixed(g, n, kap8, G):
    Gmn, ginv, Ric, Rscal = full_einstein(g, G)
    Tab, dn, L = matter_stress(n, g, ginv, G)
    Gud = torch.einsum('...am,...mb->...ab', ginv, Gmn)
    Tud = torch.einsum('...am,...mb->...ab', ginv, Tab)
    Res = Gud - kap8*Tud
    return Res, Gud, Tud, ginv, dn


def interior(A, mr=6, mth=6):
    """Strip r,theta FD edges (psi periodic -> keep all)."""
    return A[mr:-mr, mth:-mth, :]
