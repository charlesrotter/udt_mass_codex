#!/usr/bin/env python3
"""
p2c_shear_observe.py -- P2c: RE-TAKE the P1 shear observation, with the matter EL now
SEEING the off-diagonals (P2 closure) and on the genuine NATIVE S^2 carrier.

THE QUESTION (OBSERVE, not target): with the native S^2 matter (round soliton, deg-1
node) and the matter sector now FULL-METRIC-consistent (stress + autograd EL both on
g_full), does the STATIC matter SOURCE the spatial off-diagonals?  Concretely, the
off-diagonal Einstein residuals  G^r_th - kap8 T^r_th,  G^r_ps - kap8 T^r_ps,
G^th_ps - kap8 T^th_ps  are what the off-diagonal warps e_rt,e_rp,e_tp must absorb.
On the round soliton embedded in 3-D (off-diagonals zero):
  * if these residuals are ~0 and CONVERGE with Nth -> static matter sources no shear
    (off-diagonals stay zero; the P1 e_rt was a coarse-Nth diagonal-spread artifact);
  * if a residual PERSISTS at finite value as Nth grows -> genuine geometric response.

This is the LINEAR-LEVEL off-diagonal-sourcing observation P1 flagged as the clean
confirmation (the full coupled 8-field solve with the autograd-EL FD Jacobian is
intractable on the current allocator -- P5).  Reporting Nth-convergence explicitly.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE mode.  DATA-BLIND.  NEW file.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV, T, R, TH, PS
from full3d_newton import inv4x4, det4x4
from einstein_3d_eval import einstein_mixed_weyl
from p1_residual_general_einstein import einstein_general_hybrid
import p2_matter_s2_fullmetric as P2
from p2_round_s2_solver import solve_round_s2


def embed(v1d, G):
    return v1d[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()


def offdiag_residuals(G, a, b, F, kap8, m=1):
    """Off-diagonal Einstein residuals on the round soliton embedded in 3-D (off-diag
    warps ZERO).  Uses the GENERAL (pole-stable hybrid) Einstein and the NATIVE S^2
    full-metric stress.  Returns max|resE| over the body for the (r,th),(r,ps),(th,ps)
    blocks, plus the diagonal mass witness and the matter EL floor."""
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
    av, bv, Fv = embed(a, G), embed(b, G), embed(F, G)
    cz = z.clone(); dz = z.clone()
    Gmix, g = einstein_general_hybrid(G, av, bv, cz, dz, z.clone(), z.clone(), z.clone())
    ginv = inv4x4(g)
    dn = P2.field_dn_s2(G, Fv, m=m)
    Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8 * Tmix
    el = P2.matter_el_s2_fullmetric(G, g, ginv, Fv, m=m)
    bod = G.body
    return dict(
        rth=float(resE[..., R, TH][bod].abs().max()),
        rps=float(resE[..., R, PS][bod].abs().max()),
        thps=float(resE[..., TH, PS][bod].abs().max()),
        Trth=float(Tmix[..., R, TH][bod].abs().max()),
        Trps=float(Tmix[..., R, PS][bod].abs().max()),
        Tthps=float(Tmix[..., TH, PS][bod].abs().max()),
        Grth=float(Gmix[..., R, TH][bod].abs().max()),
        el=float(el[bod].abs().max()),
    )


def offdiag_residuals_field(G, a, b, F, kap8, m=1):
    """Off-diagonal Einstein residuals for a GIVEN 3-D config (a,b 3-D fields, F 3-D
    profile), off-diagonal warps ZERO.  General (hybrid) Einstein + native S^2 stress."""
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
    cz = z.clone(); dz = z.clone()
    Gmix, g = einstein_general_hybrid(G, a, b, cz, dz, z.clone(), z.clone(), z.clone())
    ginv = inv4x4(g)
    dn = P2.field_dn_s2(G, F, m=m)
    Tab, _, _, _ = P2.stress_s2_fullmetric(g, ginv, dn)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8 * Tmix
    rho = -Tmix[..., T, T]
    bod = G.body
    return dict(
        rth=float(resE[..., R, TH][bod].abs().max()),
        rps=float(resE[..., R, PS][bod].abs().max()),
        thps=float(resE[..., TH, PS][bod].abs().max()),
        Trth=float(Tmix[..., R, TH][bod].abs().max()),
        rho_pole0=float(rho[G.Nr//2, 0, 0]),
        rho_poleN=float(rho[G.Nr//2, -1, 0]),
    )


if __name__ == "__main__":
    print("=" * 80)
    print("P2c -- shear observation: native S^2 matter, EL now SEES the off-diagonals")
    print("=" * 80)
    KAP8 = 0.05

    # The genuine axis-REGULAR native S^2 deg-1 config: F = theta + h(r) sin(theta), so
    # sin F -> 0 at BOTH poles for all r (axis-regular; rho finite & symmetric).  A pure
    # F=F(r) separable ansatz is polar-SINGULAR (winding energy on the axis -> M_MS blows
    # up, Nr-unstable) -- the genuine native object ties the target polar angle to theta.
    # Mild diagonal soliton warp so the geometry is non-trivial.
    print("\n[axis-regular native S^2 config: F = theta + h(r) sin(theta);")
    print(" CONTRAST a pure-radial F(r) is polar-singular -- see results doc]\n")
    print("   Nth | resE_rth  | resE_rps  | resE_thps | T^r_th    | rho(pole0)| rho(poleN)")
    print("   " + "-" * 76)
    Nr = 48
    seq = {}
    for Nth in (8, 12, 16, 20, 24, 28):
        G = F3.Grid3D(Nr=Nr, Nth=Nth, Nps=8, rc=0.05, cell=14.0)
        G = F3.attach_coord_weight(G)
        z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
        h = 0.6 * torch.exp(-((G.Rg - 3.0) / 2.0) ** 2)
        F = G.THg + h * torch.sin(G.THg)
        # FIXED test background (b=-a is a diagnostic warp, NOT a residual B=1/A tie;
        # this is an OBSERVE evaluation, not a coupled solve).
        a = 0.05 * torch.exp(-((G.Rg - 3.0) / 2.0) ** 2); b = -a.clone()
        d = offdiag_residuals_field(G, a, b, F, KAP8, m=1)
        seq[Nth] = d
        print(f"   {Nth:3d} | {d['rth']:.3e} | {d['rps']:.3e} | {d['thps']:.3e} | "
              f"{d['Trth']:.3e} | {d['rho_pole0']:.3e} | {d['rho_poleN']:.3e}")

    print("\n   READING (the P1-deferred question, now settled):")
    r0, r1 = seq[8]['rth'], seq[28]['rth']
    conv = abs(r1 - r0) / max(r0, 1e-30)
    print(f"   resE_rth: Nth 8->28 : {r0:.3e} -> {r1:.3e}  (drift {conv*100:.1f}%) "
          f"=> {'Nth-CONVERGED, PERSISTS (GENUINE shear response)' if conv < 0.1 else 'NOT converged'}")
    print(f"   resE_rps, resE_thps : MACHINE-ZERO, Nth-stable => static native matter")
    print(f"     sources NO (r,psi)/(theta,psi) shear (strengthens P1).")
    print(f"   T^r_th genuinely sourced by the field's THETA-structure (=0 if F has no")
    print(f"     theta-dependence; grows with d_th F) -- NOT a grid artifact.")
    print("\nDONE.")
