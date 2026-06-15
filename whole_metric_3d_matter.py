#!/usr/bin/env python3
"""
whole_metric_3d_matter.py -- the MATTER sector (unit 3-vector field n:S^2, L2+L4)
on a GENERAL 4-D metric, for the WHOLE-METRIC solve.  Stress tensor T_{mu nu} with
ALL components (incl. the off-diagonal momentum/shear pieces the reduced T never had),
and the field gradient n_{,mu}, computed for an ARBITRARY metric -- NO symmetry, NO
diagonal-only assumption.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  Frame: whole_metric_solve_MAP.md.
DATA-BLIND.

THE ACTION (settled, native; native_stabilizer_results.md / C-2026-06-14-1):
  L2 = -(xi/2) g^{mn} d_m n . d_n n                 (the angular winding field)
  L4 = -(kappa/4) g^{mp} g^{nq} S_{mn}.S_{pq},  S_{mn}.S_{pq} in LAGRANGE-IDENTITY form
       (d_m n.d_p n)(d_n n.d_q n) - (d_m n.d_q n)(d_n n.d_p n)   (native Skyrme).

THE FIELD (DERIVED, matter_ansatz_derive.py, 2026-06-15):  the UNIT field that
reproduces the committed reduced pointwise stress (rho,p_r) EXACTLY (sympy, all theta)
is the S^3 / SU(2) Skyrme hedgehog -- a UNIT 4-vector:
   n = ( sinTheta sin th cos ps,  sinTheta sin th sin ps,  sinTheta cos th,  cosTheta ).
We carry n as a GENERAL unit 4-vector (4 components, |n|=1) so the field can be ANY
configuration in the 3-D solve; the hedgehog above is the special-case seed.  The
Lagrange-identity L4 is the correct native form for a unit 4-vector (the literal
3-vector cross product only exists for a 3-vector S^2 target).

STRESS TENSOR (Hilbert; for a Lagrangian with no metric-DERIVATIVE coupling, which
L2+L4 are):
  T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L          (L = L2 + L4, the scalar density)
We derive dL/dg^{mu nu} EXACTLY (symbolic, below) and evaluate it numerically.

This is the UNREDUCED matter stress: it depends on the full n_{,mu} (all of r,th,psi)
and the full inverse metric g^{mn} (all 10 components).  The reduced hedgehog
(n with the fixed angular dependence, T=Theta(r), C=psi) is the SPECIAL CASE.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3


# ---------------------------------------------------------------------------
# THE FIELD GRADIENT.  n is a UNIT 4-vector field on the grid; dn[...,mu,a] = d_mu n_a
# (mu over the 4 coords, a over the 4 target components; d_t n = 0 stationary).
# We provide a HEDGEHOG builder (the seed/special-case) and accept a general dn.
#
# Hedgehog (the validation-gate seed):  n parametrized by ONE radial profile Theta(r)
#   n = ( sinTheta sin th cos ps,  sinTheta sin th sin ps,  sinTheta cos th,  cosTheta )
# Its coordinate derivatives (analytic) are returned for an EXACT special-case check;
# in the solver dn is taken by finite differences of a general n field.
# ---------------------------------------------------------------------------
def hedgehog_n(Th, thg, psg):
    """Unit S^3 hedgehog n (...,4) from profile field Th and the angular coords."""
    sT, cT = torch.sin(Th), torch.cos(Th)
    sth, cth = torch.sin(thg), torch.cos(thg)
    sps, cps = torch.sin(psg), torch.cos(psg)
    n = torch.stack([sT*sth*cps, sT*sth*sps, sT*cth, cT], dim=-1)
    return n


# ---------------------------------------------------------------------------
# THE FIELD "first fundamental form"  G_{mn} := d_m n . d_n n  (sum over the 4
# target components).  dn (...,4,4): dn[...,m,a]=d_m n_a.  Returns (...,4,4).
# ---------------------------------------------------------------------------
def field_metric(dn):
    return torch.einsum('...ma,...na->...mn', dn, dn)


# ---------------------------------------------------------------------------
# The matter Lagrangian SCALAR DENSITY L = L2 + L4 (LAGRANGE-IDENTITY L4 for a
# unit 4-vector -- the correct native form, matter_ansatz_derive.py):
#   L2 = -(xi/2) g^{mn} G_{mn}
#   S_{mn}.S_{pq} = G_{mp} G_{nq} - G_{mq} G_{np}
#   L4 = -(kappa/4) g^{mp} g^{nq} (G_{mp}G_{nq} - G_{mq}G_{np})
# ginv (...,4,4); G_{mn} (...,4,4).  Returns L, L2, L4.
# ---------------------------------------------------------------------------
def lagrangian(ginv, Gmn, xi, kap):
    L2 = -(xi/2) * torch.einsum('...mn,...mn->...', ginv, Gmn)
    # SS_{mnpq} = G_{mp}G_{nq} - G_{mq}G_{np}
    GG1 = torch.einsum('...mp,...nq->...mnpq', Gmn, Gmn)
    GG2 = torch.einsum('...mq,...np->...mnpq', Gmn, Gmn)
    SS = GG1 - GG2
    L4 = -(kap/4) * torch.einsum('...mp,...nq,...mnpq->...', ginv, ginv, SS)
    return L2 + L4, L2, L4, SS


# ---------------------------------------------------------------------------
# THE STRESS TENSOR  T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L  (Hilbert; no
# metric-derivative coupling).  With L4 in Lagrange-identity form:
#   dL2/dg^{ab} = -(xi/2) G_{ab}
#   dL4/dg^{ab} = -(kappa/2) g^{nq} SS_{a n b q}|_sym(ab)   (same algebra as before:
#     SS symmetric under (mn)<->(pq), the two metric factors give equal contributions)
#   => T_{ab} = xi G_{ab} + kappa [g^{nq} SS_{a n b q}]_sym(ab) + g_{ab} L.
# Returns T_{mu nu} (...,4,4) and the pieces.
# ---------------------------------------------------------------------------
def stress_tensor(g, ginv, dn, xi, kap):
    Gmn = field_metric(dn)
    L, L2, L4, SS = lagrangian(ginv, Gmn, xi, kap)
    C_ab = torch.einsum('...nq,...anbq->...ab', ginv, SS)
    C_ab = 0.5*(C_ab + C_ab.transpose(-1, -2))   # symmetrize (a,b)
    Tab = xi*Gmn + kap*C_ab + g*L[..., None, None]
    return Tab, L, L2, L4
