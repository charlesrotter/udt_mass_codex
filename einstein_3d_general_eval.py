#!/usr/bin/env python3
"""
einstein_3d_general_eval.py -- evaluate the AUTO-GENERATED analytic GENERAL-metric
mixed Einstein tensor G^mu_nu (+ Ricci scalar R = -trace G^mu_nu) on the spectral
grid.  This is the GENERAL (sheared + time-row) analog of einstein_3d_eval's
einstein_mixed_weyl: smooth WARP derivatives taken spectrally; the cot/1/sin pole
structure and the metric-inverse carried symbolically by the generator (evaluated
only at the off-axis GL nodes -> pole-safe).

Driver: Claude (Opus 4.8, 1M).  2026-06-21.  S1 (GATING).  DATA-BLIND.

WHY (S1 diagnosis):  the numerical CORE.einstein engine double-spectrally-
differentiates a spectrally-built Christoffel; on a Cheb grid this NESTED
differentiation amplifies high modes by O(N^2) and the Einstein error GROWS with N
even on a SMOOTH analytic metric (measured 14->160 over Nr 16->64).  An exponential
spectral filter does NOT cure it (still grows).  The ONLY clean cure is to never
construct/re-differentiate Gamma numerically: get G^mu_nu in CLOSED FORM and feed it
ONLY the smooth warp partials -- exactly the validated diagonal recipe, extended to
the general sheared metric.

WARPS (match full3d_spectral.build_metric + time row):
  g_tt=-e^{2a}, g_rr=e^{2b}, g_thth=e^{2c}r^2, g_psps=e^{2d}r^2 sin^2,
  g_rth=e_rt r, g_rps=e_rp r sin, g_thps=e_tp r^2 sin,
  g_tr=h_tr, g_tth=h_tt r, g_tps=h_tp r sin.   All warps = warp(r,th,ps).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import torch
torch.set_default_dtype(torch.float64)
from einstein_3d_general_gen import Gmix_components_gen

T, R, TH, PS = 0, 1, 2, 3
_ORDER = ['a', 'b', 'c', 'd', 'e_rt', 'e_rp', 'e_tp', 'h_tr', 'h_tt', 'h_tp']


def _warp_derivs(G, f):
    """(f, f_r,f_t,f_p, f_rr,f_tt,f_pp, f_rt,f_rp,f_tp) -- spectral partials."""
    fr = G.d_r(f); ft = G.d_th(f); fp = G.d_ps(f)
    frr = G.d_r(fr); ftt = G.d_th(ft); fpp = G.d_ps(fp)
    frt = G.d_th(fr); frp = G.d_ps(fr); ftp = G.d_ps(ft)
    return (f, fr, ft, fp, frr, ftt, fpp, frt, frp, ftp)


def einstein_mixed_general(G, warps):
    """Analytic mixed Einstein G^mu_nu (Nr,Nth,Nps,4,4) for the general sheared metric.
    warps: dict name->field (Nr,Nth,Nps); missing names default to 0 (e.g. diagonal)."""
    z = None
    args = []
    for nm in _ORDER:
        f = warps.get(nm)
        if f is None:
            if z is None:
                # need a zero tensor of the grid shape; infer from any provided warp
                ref = next(iter(warps.values()))
                z = torch.zeros_like(ref)
            f = z
        args.extend(_warp_derivs(G, f))
    rows = Gmix_components_gen(G.Rg, G.THg, *args)
    out = torch.zeros(G.Nr, G.Nth, G.Nps, 4, 4, device=G.Rg.device)
    for m in range(4):
        for n in range(4):
            v = rows[m][n]
            if not torch.is_tensor(v):
                v = torch.full_like(G.Rg, float(v))
            out[..., m, n] = v
    return out


def ricci_scalar_general(G, warps):
    """R = -trace(G^mu_nu) for the general metric."""
    Gmix = einstein_mixed_general(G, warps)
    return -torch.einsum('...mm->...', Gmix)
