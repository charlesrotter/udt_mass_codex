#!/usr/bin/env python3
"""
einstein_3d_general_filtered.py -- GENERAL-metric mixed Einstein G^mu_nu + R via the
numerical NR route (CORE.christoffel + spectral dGamma) but with an EXPONENTIAL
SPECTRAL FILTER inserted between the two differentiation passes to kill the O(N^2)
high-mode amplification that the S1 diagnosis localized (the nested spectral-d of a
spectrally-built Gamma made CORE.einstein DIVERGE with N).

This is the LIGHT cure (works for ANY metric incl shear and time-row off-diagonals).
The analytic-codegen cure (einstein_3d_general_gen) is the HEAVY clean cure; this is
the fallback / cross-check.

FILTER: exponential (Hou-Li / Vandeven style) applied to the Chebyshev radial modes
and the Legendre theta modes of each Christoffel component before d_r/d_th are taken a
second time.  sigma(eta) = exp(-alpha eta^(2p)), eta = mode/Nmax.  Damps only the top
modes; spectral-accurate (no contamination of resolved modes for alpha,p chosen large).
Driver: Claude (Opus 4.8, 1M). 2026-06-21. eval-only, anti-hang trivial.
"""
import os, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
import whole_metric_3d_core as CORE

T, R, TH, PS = 0, 1, 2, 3


def _cheb_filter_matrix(Nr, alpha=36.0, p=8):
    """Filter operator on Cheb-Lobatto values: V_inv -> sigma -> V (value->coef->value).
    Built from the Chebyshev-T Vandermonde at the CGL nodes (ascending r matches grid)."""
    # CGL nodes x in [-1,1] ascending (matches cheb_interval flip): x_j = -cos? Build T_k(x).
    j = np.arange(Nr)
    x = np.cos(np.pi*np.arange(Nr-1, -1, -1)/(Nr-1)) if Nr > 1 else np.array([1.0])  # ascending
    # Chebyshev-T Vandermonde V[i,k] = T_k(x_i)
    V = np.cos(np.outer(np.arccos(np.clip(x, -1, 1)), np.arange(Nr)))
    Vinv = np.linalg.inv(V)
    eta = np.arange(Nr)/max(Nr-1, 1)
    sig = np.exp(-alpha*eta**(2*p))
    Fm = V @ np.diag(sig) @ Vinv
    return torch.tensor(Fm)


def _leg_filter_matrix(Nth, alpha=36.0, p=8):
    """Filter on GL-theta values via the Legendre Vandermonde (mu=cos theta nodes)."""
    from numpy.polynomial.legendre import legvander
    from scipy.special import roots_legendre
    mu, _ = roots_legendre(Nth)
    th = np.arccos(mu); idx = np.argsort(th); mu = mu[idx]
    V = legvander(mu, Nth-1)
    Vinv = np.linalg.inv(V)
    eta = np.arange(Nth)/max(Nth-1, 1)
    sig = np.exp(-alpha*eta**(2*p))
    Fm = V @ np.diag(sig) @ Vinv
    return torch.tensor(Fm)


class FilterPack:
    def __init__(self, G, alpha=36.0, p=8):
        self.Fr = _cheb_filter_matrix(G.Nr, alpha, p).to(G.r.device)
        self.Fth = _leg_filter_matrix(G.Nth, alpha, p).to(G.r.device)
    def apply(self, f):
        # filter radial then theta on a field whose first 3 axes are (Nr,Nth,Nps)
        # and any trailing axes are component indices (kept intact).
        nd = f.ndim
        f = torch.tensordot(self.Fr, f, dims=([1], [0]))          # contracts axis0 -> front
        # theta is axis 1; tensordot puts the new theta axis at front, restore order
        f = torch.tensordot(self.Fth, f, dims=([1], [1]))
        perm = [1, 0] + list(range(2, nd))
        f = f.permute(*perm)
        return f


def einstein_mixed_filtered(G, g, fp=None, alpha=36.0, p=8):
    """G^mu_nu and Rscal for a GENERAL metric g via CORE with a filter between passes."""
    if fp is None:
        fp = FilterPack(G, alpha, p)
    ginv = CORE.metric_inverse(g)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for m in range(4):
        for n in range(4):
            comp = g[..., m, n]
            dg[..., R, m, n] = G.d_r(comp)
            dg[..., TH, m, n] = G.d_th(comp)
            dg[..., PS, m, n] = G.d_ps(comp)
    Gamma = CORE.christoffel(ginv, dg)
    # FILTER each Christoffel component before the second differentiation
    Gam_f = fp.apply(Gamma.reshape(Nr, Nth, Nps, 64)).reshape(Nr, Nth, Nps, 4, 4, 4)
    dGamma = torch.zeros(Nr, Nth, Nps, 4, 4, 4, 4, device=g.device)
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                comp = Gam_f[..., a_, b_, c_]
                dGamma[..., R, a_, b_, c_] = G.d_r(comp)
                dGamma[..., TH, a_, b_, c_] = G.d_th(comp)
                dGamma[..., PS, a_, b_, c_] = G.d_ps(comp)
    Gmn, Ric, Rscal = CORE.einstein(g, ginv, Gamma, dGamma)
    Gmix = torch.einsum('...ma,...an->...mn', ginv, Gmn)
    return Gmix, Rscal
