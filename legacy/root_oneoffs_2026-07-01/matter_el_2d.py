#!/usr/bin/env python3
"""
matter_el_2d.py -- the NATIVE 2-D (r,theta) matter Euler-Lagrange operator for the
winding profile Theta(r,theta) of the unit S^3 hedgehog on a diagonal axisymmetric
metric.  THE ENABLER for the genuine matter-FREE catalog search.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND
(units L = sqrt(kappa/xi) = 1; no wall numbers, no comparison to nature).

WHY THIS MODULE (the #58 gap): the prior axisym solver (gapcloser_axisym.py) built
the matter EL by AUTOGRAD of sum(sqrt|g| * L) where L was assembled from the FULL
4-vector hedgehog n(Theta(r,th),th,ps) FINITE-DIFFERENCED in (r,th,ps).  That
FD-differences the ANGULAR structure (sin th, sin^2 Theta entering via d_th n) on the
coarse Nth grid, leaving a ~0.2 inner-body truncation residual on the round #56 Theta
that does NOT vanish with resolution -> matter had to be FROZEN (w_matter=0), so
matter-shaped catalog members were never searched.

THE FIX (numerical conditioning of the SAME equations, NOT a patch): for the hedgehog
the field "first fundamental form" G_{mn} = d_m n . d_n n is known ANALYTICALLY
(sympy, derive2d.py):
    G_rr = Theta_r^2,   G_thth = sin^2 Theta + Theta_th^2,
    G_psps = sin^2 th sin^2 Theta,   G_rth = Theta_r Theta_th,   G_rps = G_thps = 0.
So the angular structure is EXACT; only Theta_r, Theta_th are discretized.  On the
diagonal axisym metric ds^2 = -e^{2a}dt^2 + e^{2b}dr^2 + e^{2c}r^2 dth^2 +
e^{2d}r^2 sin^2 th dps^2 the proper-volume action density is (sympy, gen_el_code.py)
    dens = sqrt|g| (L2+L4),  sqrt|g| = e^{a+b+c+d} r^2 sin th,
and the field EL is the standard
    EL[Theta] = d_r P_r + d_th P_th - Q = 0,
with (A=e^{2a}, B=e^{2b}, C=e^{2c}, D=e^{2d}; common factor sin th = proper measure):
    P_r  = - e^{a-b-c-d} Theta_r ( C D r^2 xi + kap (C+D) sin^2 T ) sin th
    P_th = - e^{a+b-c-d} Theta_th ( D r^2 xi + kap sin^2 T ) sin th / r^2
    Q    = - e^{a-b-c-d} ( B r^2 xi (C+D)
                           + kap ( B (Theta_th^2 + 2 sin^2 T) + (C+D) Theta_r^2 r^2 ) )
             sin T cos T sin th / r^2

VALIDATION (check_round_limit.py, sympy, EXACT): in the round limit
(Theta_th = 0, c = d = 0) this EL reduces IDENTICALLY to the 1-D theta_ddot_freed of
radial_Bfree_soliton.py (#56, blind-verified clean O(h^2)).  So this is the SAME
native physics as the validated 1-D EL -- a better 2-D DISCRETIZATION, not a different
equation.

NATIVE-vs-PATCH: the analytic angular reduction is an EXACT identity (no approximation,
no linearization); proper-volume weighting and the FD of (Theta_r, Theta_th) are the
sanctioned function-replacements.  B=1/A is NOT tied (a,b,c,d independent).  No seal,
no source injection, no imported mechanism, no target tuning.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi
EXP_CLAMP = 60.0


# ---------------------------------------------------------------------------
# 4th-order central FD on a uniform 1-D axis of a 2-D (Nr,Nth) field.
# axis=0 -> r, axis=1 -> theta.  One-sided 4th-order at edges (matches core.d_dx).
# ---------------------------------------------------------------------------
def d_dx(f, h, axis):
    n = f.shape[axis]
    g = torch.zeros_like(f)
    def sl(i):
        s = [slice(None)] * f.ndim
        s[axis] = i
        return tuple(s)
    if n >= 5:
        g[sl(slice(2, n - 2))] = (
            -f[sl(slice(4, n))] + 8 * f[sl(slice(3, n - 1))]
            - 8 * f[sl(slice(1, n - 3))] + f[sl(slice(0, n - 4))]) / (12 * h)
        # 4th-order one-sided at the two edges on each side
        for k in (0, 1):
            g[sl(k)] = (-25 * f[sl(k)] + 48 * f[sl(k + 1)] - 36 * f[sl(k + 2)]
                        + 16 * f[sl(k + 3)] - 3 * f[sl(k + 4)]) / (12 * h)
        for k in (n - 1, n - 2):
            g[sl(k)] = (25 * f[sl(k)] - 48 * f[sl(k - 1)] + 36 * f[sl(k - 2)]
                        - 16 * f[sl(k - 3)] + 3 * f[sl(k - 4)]) / (12 * h)
    else:  # tiny axis: 2nd-order central
        g[sl(slice(1, n - 1))] = (f[sl(slice(2, n))] - f[sl(slice(0, n - 2))]) / (2 * h)
        g[sl(0)] = (f[sl(1)] - f[sl(0)]) / h
        g[sl(n - 1)] = (f[sl(n - 1)] - f[sl(n - 2)]) / h
    return g


# ---------------------------------------------------------------------------
# THE FLUXES and SOURCE of the native EL (exact analytic angular reduction).
# a,b,c,d,Theta are (Nr,Nth) fields; rg (Nr,), thg (Nth,).  xi,kap couplings.
# Returns P_r, P_th, Q on the full (Nr,Nth) grid.
# ---------------------------------------------------------------------------
def el_fluxes(a, b, c, d, Th, Tr, Tth, rg, thg, xi, kap):
    r = rg[:, None]
    sth = torch.sin(thg)[None, :]
    sT = torch.sin(Th)
    A = torch.exp(torch.clamp(2 * a, max=EXP_CLAMP))
    B = torch.exp(torch.clamp(2 * b, max=EXP_CLAMP))
    C = torch.exp(torch.clamp(2 * c, max=EXP_CLAMP))
    D = torch.exp(torch.clamp(2 * d, max=EXP_CLAMP))
    rA = torch.exp(torch.clamp(a - b - c - d, max=EXP_CLAMP))     # e^{a-b-c-d}=sqrtA/sqrt(BCD)
    rAth = torch.exp(torch.clamp(a + b - c - d, max=EXP_CLAMP))   # e^{a+b-c-d}
    s2 = sT * sT
    Pr = -rA * Tr * (C * D * r**2 * xi + kap * (C + D) * s2) * sth
    Pth = -rAth * Tth * (D * r**2 * xi + kap * s2) * sth / r**2
    Q = -rA * (B * r**2 * xi * (C + D)
               + kap * (B * (Tth**2 + 2 * s2) + (C + D) * Tr**2 * r**2)) \
        * sT * torch.cos(Th) * sth / r**2
    return Pr, Pth, Q


# ---------------------------------------------------------------------------
# THE NATIVE 2-D EL RESIDUAL  R[Theta] = d_r P_r + d_th P_th - Q  (=0 at solution).
# This is the proper-volume-weighted EL density (carries the sin th measure); to get
# a per-point residual comparable to the 1-D one we divide out the local measure
# factor so the units match the 1-D Theta''-form residual (see gate).
# ---------------------------------------------------------------------------
def el_residual(a, b, c, d, Th, rg, thg, hr, hth, xi, kap):
    Tr = d_dx(Th, hr, 0)
    Tth = d_dx(Th, hth, 1)
    Pr, Pth, Q = el_fluxes(a, b, c, d, Th, Tr, Tth, rg, thg, xi, kap)
    dPr = d_dx(Pr, hr, 0)
    dPth = d_dx(Pth, hth, 1)
    R = dPr + dPth - Q
    return R, dict(Tr=Tr, Tth=Tth, Pr=Pr, Pth=Pth, Q=Q)


# ---------------------------------------------------------------------------
# A per-point NORMALIZED residual matching the 1-D theta_ddot_freed convention,
# so the 2-D gate can be compared head-to-head with the clean 1-D residual.
# The 1-D EL in Theta''-form is  Theta'' - rhs = 0.  Our density EL is
#   d_r P_r + d_th P_th - Q = 0  with P_r = -M_r(r) Theta_r * sin th  (M_r>0),
# so dividing by (-M_r sin th) recovers the leading Theta'' coefficient = 1.
# We use the round-limit leading coefficient  M_r = e^{a-b-c-d}(C D r^2 xi + kap(C+D)s^2).
# ---------------------------------------------------------------------------
def el_residual_normalized(a, b, c, d, Th, rg, thg, hr, hth, xi, kap):
    R, aux = el_residual(a, b, c, d, Th, rg, thg, hr, hth, xi, kap)
    r = rg[:, None]
    sth = torch.sin(thg)[None, :]
    sT = torch.sin(Th)
    C = torch.exp(torch.clamp(2 * c, max=EXP_CLAMP))
    D = torch.exp(torch.clamp(2 * d, max=EXP_CLAMP))
    rA = torch.exp(torch.clamp(a - b - c - d, max=EXP_CLAMP))
    M_r = rA * (C * D * r**2 * xi + kap * (C + D) * sT * sT) * sth
    Rn = R / (M_r + 1e-300)
    return Rn, aux


def make_grid_rt(Nr, Nth, rc, ri, th0, th1):
    rg = torch.linspace(rc, ri, Nr, device=DEV)
    thg = torch.linspace(th0, th1, Nth, device=DEV)
    hr = (rg[1] - rg[0]).item()
    hth = (thg[1] - thg[0]).item()
    return rg, thg, hr, hth
