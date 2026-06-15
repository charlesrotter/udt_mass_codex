#!/usr/bin/env python3
"""
whole_metric_3d_core.py -- FULL 3-D numerical Einstein-matter machinery on a
(r, theta, psi) grid for the WHOLE-METRIC solve (realization A: stationary soliton,
ALL 10 metric components live, NO symmetry imposed).

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  Frame: whole_metric_solve_MAP.md.
DATA-BLIND (units L=sqrt(kappa/xi)=1).

THE STANDARD NR ROUTE (charter principle 4: the GR corpus is TRANSFORMED numerics,
not imported new physics):
  metric g_{mu nu}(x)  --FD-->  d g  --> Christoffel Gamma^a_{bc}
                       --FD-->  d Gamma --> Riemann R^a_{bcd}
                       --contract--> Ricci R_{mu nu}, scalar R
                       --> Einstein G_{mu nu} = R_{mu nu} - 1/2 g_{mu nu} R.
  Computed NUMERICALLY for a GENERAL metric (no closed-form G assumed).

Coordinates: x = (t, r, theta, psi), indices 0,1,2,3.  STATIONARY: d_t = 0 (adapted
gauge), so the metric depends on (r, theta, psi) only -> a 3-D spatial grid, but the
FULL 4x4 metric (incl. all time-row g_{t.} and twist g_{.psi} off-diagonals) is carried.

This module provides ONLY the geometry + matter-stress primitives and their
SELF-VALIDATION against an exact case (Schwarzschild).  The solver lives elsewhere.

NUMERICS (principle 2): exact tensor algebra; FD derivatives are the sanctioned
function-replacement (4th-order central in the interior).  NO linearization.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"

# coordinate index labels for clarity
T, R, TH, PS = 0, 1, 2, 3


# ===========================================================================
# FINITE DIFFERENCES on a uniform grid (4th-order central interior, lower-order
# one-sided at edges).  Field shape: (..., Nr, Nth, Nps).  axis in {0,1,2} maps to
# spatial coords (r, theta, psi).  Returns same shape.
# ===========================================================================
def d_dx(f, h, axis, periodic=False):
    """4th-order central first derivative along a SPATIAL axis (0=r,1=th,2=psi).
    f shape (..., Nr, Nth, Nps); spatial axes are the last 3 (map axis 0->-3,...).
    periodic=True: azimuth psi is genuinely periodic (no boundary) -> 4th-order
    central everywhere via torch.roll; this removes ALL edge degradation in psi."""
    ax = axis - 3
    n = f.shape[ax]
    if periodic:
        return (-torch.roll(f, -2, dims=ax) + 8*torch.roll(f, -1, dims=ax)
                - 8*torch.roll(f, 1, dims=ax) + torch.roll(f, 2, dims=ax)) / (12*h)
    g = torch.zeros_like(f)
    sl = [slice(None)] * f.ndim
    def S(i):
        s = list(sl); s[ax] = i; return tuple(s)
    # 4th-order central interior  (-f[+2]+8 f[+1]-8 f[-1]+f[-2])/(12 h)
    g[S(slice(2, n-2))] = (
        -f[S(slice(4, n))] + 8*f[S(slice(3, n-1))]
        - 8*f[S(slice(1, n-3))] + f[S(slice(0, n-4))]) / (12*h)
    # 4th-order one-sided at the two near-edge interior points (keeps order up)
    g[S(1)] = (-3*f[S(0)] - 10*f[S(1)] + 18*f[S(2)] - 6*f[S(3)] + f[S(4)]) / (12*h)
    g[S(n-2)] = (3*f[S(n-1)] + 10*f[S(n-2)] - 18*f[S(n-3)] + 6*f[S(n-4)] - f[S(n-5)]) / (12*h)
    # 4th-order one-sided at edges (5-pt forward/backward)
    g[S(0)] = (-25*f[S(0)] + 48*f[S(1)] - 36*f[S(2)] + 16*f[S(3)] - 3*f[S(4)]) / (12*h)
    g[S(n-1)] = (25*f[S(n-1)] - 48*f[S(n-2)] + 36*f[S(n-3)] - 16*f[S(n-4)] + 3*f[S(n-5)]) / (12*h)
    return g


# ===========================================================================
# METRIC INVERSE.  g shape (..., 4,4) at every grid point.  Returns g^{mu nu}.
# We pack the 4x4 in the LAST two dims; grid dims precede.  Use torch.linalg.inv
# (small 4x4 -> stable; V100-safe, no solve_triangular broadcast).
# ===========================================================================
def metric_inverse(g):
    return torch.linalg.inv(g)


# ===========================================================================
# CHRISTOFFEL SYMBOLS.  Gamma^a_{bc} = 1/2 g^{ad}(d_b g_{dc} + d_c g_{db} - d_d g_{bc}).
# Inputs:
#   g     : (..., 4,4)  metric at grid points
#   ginv  : (..., 4,4)  inverse metric
#   dg    : (..., 4,4,4) where dg[..., k, mu, nu] = d_{x_k} g_{mu nu}, and k runs over
#           the FOUR coords (t,r,theta,psi).  d_t g = 0 (stationary) -> dg[...,0,:,:]=0.
# Returns Gamma (..., 4,4,4):  Gamma[..., a, b, c] = Gamma^a_{bc}.
# ===========================================================================
def christoffel(ginv, dg):
    # term_{d,b,c} = d_b g_{dc} + d_c g_{db} - d_d g_{bc}
    # dg index order is [k, mu, nu] = d_k g_{mu nu}
    db_gdc = dg.permute(*range(dg.ndim-3), -2, -3, -1)   # [b, d, c] -> want [d,b,c]
    # easier: build with explicit einsum-style indexing
    # dg[..., k, m, n] = d_k g_{m n}
    # d_b g_{d c} = dg[..., b, d, c]
    # d_c g_{d b} = dg[..., c, d, b]
    # d_d g_{b c} = dg[..., d, b, c]
    term = (dg.permute(*range(dg.ndim-3), -2, -3, -1)        # [d? ] -> need care
            )
    # Do it cleanly with einsum.
    # We want Tbc_d[..., d, b, c] = dg[...,b,d,c] + dg[...,c,d,b] - dg[...,d,b,c]
    A = torch.einsum('...bdc->...dbc', dg)   # dg[...,b,d,c] rearranged to [d,b,c]
    Bp = torch.einsum('...cdb->...dbc', dg)  # dg[...,c,d,b] -> [d,b,c]
    Cp = dg                                   # dg[...,d,b,c] already [d,b,c]
    Tterm = A + Bp - Cp                        # (..., d,b,c)
    Gamma = 0.5 * torch.einsum('...ad,...dbc->...abc', ginv, Tterm)
    return Gamma


# ===========================================================================
# RIEMANN, RICCI, EINSTEIN.  Computed from Gamma and dGamma.
#   R^a_{bcd} = d_c Gamma^a_{bd} - d_d Gamma^a_{bc}
#               + Gamma^a_{ce} Gamma^e_{bd} - Gamma^a_{de} Gamma^e_{bc}
#   R_{bd} = R^a_{bad}   (contract a=c)
#   R = g^{bd} R_{bd}
#   G_{mn} = R_{mn} - 1/2 g_{mn} R
# Inputs:
#   g, ginv : (...,4,4)
#   Gamma   : (...,4,4,4)   Gamma[...,a,b,c]=Gamma^a_{bc}
#   dGamma  : (...,4,4,4,4) dGamma[...,k,a,b,c] = d_{x_k} Gamma^a_{bc}, k over 4 coords
#             (d_t = 0 stationary).
# Returns G_{mu nu} (...,4,4), and R_{mu nu}, R for diagnostics.
# ===========================================================================
def einstein(g, ginv, Gamma, dGamma):
    # R^a_{bcd} = d_c Gamma^a_{bd} - d_d Gamma^a_{bc} + Gamma^a_{ce}Gamma^e_{bd} - Gamma^a_{de}Gamma^e_{bc}
    # dGamma[...,k,a,b,c] = d_k Gamma^a_{bc}
    dc_Gabd = torch.einsum('...cabd->...abcd', dGamma)  # d_c Gamma^a_{bd}
    dd_Gabc = torch.einsum('...dabc->...abcd', dGamma)  # d_d Gamma^a_{bc}
    GG1 = torch.einsum('...ace,...ebd->...abcd', Gamma, Gamma)
    GG2 = torch.einsum('...ade,...ebc->...abcd', Gamma, Gamma)
    Riem = dc_Gabd - dd_Gabc + GG1 - GG2   # R^a_{bcd}
    # Ricci R_{bd} = R^a_{bad}  (contract a=c)
    Ric = torch.einsum('...abad->...bd', Riem)
    Rscal = torch.einsum('...bd,...bd->...', ginv, Ric)
    Gmn = Ric - 0.5 * g * Rscal[..., None, None]
    return Gmn, Ric, Rscal
