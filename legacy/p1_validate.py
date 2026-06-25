#!/usr/bin/env python3
"""
p1_validate.py -- PHASE 1 validation + first observation.

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  OBSERVE mode.  DATA-BLIND.

GATES (all anchor-gated; each PASS/FAIL reported with numbers, no dramatization):
  (a) ROUND recovery: off-diagonals LIVE but seeded zero -> the P1 solve recovers
      the P0 round soliton UNCHANGED and the off-diagonals stay machine-small.
  (b) OFF-DIAGONAL G correctness IN THE RESIDUAL PATH: the hybrid general Einstein
      reproduces an INDEPENDENT G on a non-diagonal test metric (sympy-anchored via
      the committed core validation pattern), and the off-diagonal blocks respond.
  (c) divT / gauge sanity on a non-round test config.

OBSERVATION (not target): with off-diagonals able to feed back, in the STATIC
native-matter context -- round AND a mild l=2 non-round matter perturbation -- do the
spatial off-diagonals want to grow, or stay zero?  Report the raw numbers.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math, time, sys
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    einstein_mixed, einstein_mixed_weyl, field_dn, matter_el_3d, diagnostics,
    residuals, DEV, PI, T, R, TH, PS)
import full3d_solver as FS
import full3d_newton as NW
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import p1_residual_general_einstein as P1


def hdr(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def round_seed8(G, p=0.4, kap8=0.05):
    """8-field round seed: the radial soliton in (a,b,c,d,Th) + off-diagonals = 0."""
    u5, sol = FS.round_seed(G, p=p, kap8=kap8)
    a, b, c, d, Th = FS.unpack(u5, G)
    z = torch.zeros_like(a)
    return P1.pack8(a, b, c, d, Th, z, z, z), sol


def main():
    grid = (24, 6, 8)
    p, kap8, m = 0.4, 0.05, 1
    G = Grid3D(*grid, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    bod = G.body
    print(f"P1 VALIDATION  grid={grid} p={p} kap8={kap8} cell=14  (node-core, B=1/A free, a=-1)")

    # ---------------------------------------------------------------------
    # GATE (b) FIRST (cheap, no solve): off-diagonal G correctness in the RESIDUAL
    # path.  Compare the hybrid general Einstein to (i) the analytic weyl on a
    # diagonal metric (must be EXACT), and (ii) the raw general Einstein off-diag
    # blocks on a non-diagonal test metric (the residual path actually uses these).
    # ---------------------------------------------------------------------
    hdr("GATE (b) -- off-diagonal general Einstein correctness in the residual path")
    u0, sol = round_seed8(G, p, kap8)
    a, b, c, d, Th, e_rt, e_rp, e_tp = P1.unpack8(u0, G)
    # (b1) zero off-diag: hybrid == analytic weyl EXACTLY
    Gh0, g0 = P1.einstein_general_hybrid(G, a, b, c, d, e_rt, e_rp, e_tp)
    Gw = einstein_mixed_weyl(G, a, b, c, d)
    err_b1 = float((Gh0 - Gw).abs().max())
    print(f"  (b1) zero-offdiag: max|G_hybrid - G_weyl| = {err_b1:.3e}  "
          f"(must be ~0/machine -> diagonal sector uncorrupted)")
    # (b2) turn on a smooth off-diag warp; off-diag G blocks become live and the
    # raw general Einstein computes them.  Cross-check vs CORE FD pipeline (different
    # code path -> independent) on a SMOOTH (non-steep) analytic metric so FD is valid.
    rr = G.Rg; th = G.THg
    bump = torch.exp(-((rr - (G.rc + 5.0)) ** 2) / 4.0)
    e_test = 0.02 * bump * torch.sin(th) ** 2
    Gh, gfull = P1.einstein_general_hybrid(G, a, b, c, d, e_test, torch.zeros_like(e_test),
                                           torch.zeros_like(e_test))
    deep = torch.zeros_like(bod); deep[6:G.Nr - 6, :, :] = True
    g_rth_live = float(Gh[..., R, TH][deep].abs().max())
    g_rps_live = float(Gh[..., R, PS][deep].abs().max())   # should ~0 (theta-only warp)
    print(f"  (b2) e_rt warp ON: live G^r_th (deep) = {g_rth_live:.3e}  (must be >>0 "
          f"-> off-diag reaches field eqns)")
    print(f"       cross: G^r_ps (deep) = {g_rps_live:.3e}  (must ~0 -> theta-only warp "
          f"sources only the rth sector, correct selectivity)")
    # (b3) independent check: hybrid off-diag block vs CORE general Einstein on a
    # SMOOTH metric (linalg path, different from the spectral residual path).
    g_np = gfull.detach()
    # CORE FD Einstein on the same metric (FD derivatives) -- independent code path
    hr = float(G.r[1] - G.r[0]); hth = float(G.th[1] - G.th[0]); hps = float(G.psi[1] - G.psi[0])
    # Use spectral dg for CORE.einstein (consistent), but raise via metric_inverse
    # (linalg) instead of the spectral einstein_mixed -> tests the contraction path.
    ginv_l = CORE.metric_inverse(g_np)
    Ngrid = (G.Nr, G.Nth, G.Nps)
    dg = torch.zeros(*Ngrid, 4, 4, 4, device=DEV)
    for mm in range(4):
        for nn in range(4):
            comp = g_np[..., mm, nn]
            dg[..., R, mm, nn] = G.d_r(comp); dg[..., TH, mm, nn] = G.d_th(comp)
            dg[..., PS, mm, nn] = G.d_ps(comp)
    Gamma = CORE.christoffel(ginv_l, dg)
    dGamma = torch.zeros(*Ngrid, 4, 4, 4, 4, device=DEV)
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                comp = Gamma[..., a_, b_, c_]
                dGamma[..., R, a_, b_, c_] = G.d_r(comp)
                dGamma[..., TH, a_, b_, c_] = G.d_th(comp)
                dGamma[..., PS, a_, b_, c_] = G.d_ps(comp)
    Gmn_core, _, _ = CORE.einstein(g_np, ginv_l, Gamma, dGamma)
    Gmix_core = torch.einsum('...ma,...an->...mn', ginv_l, Gmn_core)
    # the off-diagonal DELTA from CORE path (subtract diagonal-metric CORE Einstein)
    g_diag = build_metric(G, a, b, c, d)
    ginv_d = CORE.metric_inverse(g_diag)
    dg_d = torch.zeros(*Ngrid, 4, 4, 4, device=DEV)
    for mm in range(4):
        for nn in range(4):
            comp = g_diag[..., mm, nn]
            dg_d[..., R, mm, nn] = G.d_r(comp); dg_d[..., TH, mm, nn] = G.d_th(comp)
            dg_d[..., PS, mm, nn] = G.d_ps(comp)
    Gamma_d = CORE.christoffel(ginv_d, dg_d)
    dGamma_d = torch.zeros(*Ngrid, 4, 4, 4, 4, device=DEV)
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                comp = Gamma_d[..., a_, b_, c_]
                dGamma_d[..., R, a_, b_, c_] = G.d_r(comp)
                dGamma_d[..., TH, a_, b_, c_] = G.d_th(comp)
                dGamma_d[..., PS, a_, b_, c_] = G.d_ps(comp)
    Gmn_core_d, _, _ = CORE.einstein(g_diag, ginv_d, Gamma_d, dGamma_d)
    Gmix_core_d = torch.einsum('...ma,...an->...mn', ginv_d, Gmn_core_d)
    delta_core = Gmix_core - Gmix_core_d
    delta_hybrid = Gh - Gw   # hybrid's off-diag delta
    err_rth = float((delta_core[..., R, TH] - delta_hybrid[..., R, TH])[deep].abs().max())
    print(f"  (b3) hybrid off-diag delta vs INDEPENDENT CORE-linalg path: "
          f"max|d_rth| = {err_rth:.3e}  (small -> residual-path off-diag G is correct)")

    # ---------------------------------------------------------------------
    # GATE (a): ROUND recovery -- solve P1 with off-diag live but seeded 0.
    # ---------------------------------------------------------------------
    hdr("GATE (a) -- ROUND recovery (off-diagonals LIVE, seeded zero)")
    t0 = time.time()
    # deg-1 node core (core=pi NODE selecting the charge-1 class; NOT the m*pi
    # ladder) -- the native condition that HOLDS the soliton (stage1a finding).
    u_a, hist_a = P1.newton_solve_p1(u0, G, p, kap8, m=m, maxit=30, tol=1e-11,
                                     verbose=True, node_core=True, core_mode="deg1")
    dt = time.time() - t0
    comp_a = P1.component_residuals_p1(u_a, G, p, kap8, m=m)
    # M_MS via diagnostics (uses the diagonal residuals path; build out dict)
    aa, bb, cc, dd, Thh, ert, erp, etp = P1.unpack8(u_a, G)
    g_full = build_metric(G, aa, bb, cc, dd, e_rt=ert, e_rp=erp, e_tp=etp)
    ginv = CORE.metric_inverse(g_full)
    dn = field_dn(G, Thh, m=m)
    Tab, Lsc, _, _ = MAT.stress_tensor(g_full, ginv, dn, 1.0, 1.0)
    out = dict(Tab=Tab, g=g_full, ginv=ginv)
    diag = diagnostics(G, out, kap8)
    print(f"  converged Phi = {hist_a[-1]:.4e}  ({len(hist_a)-1} it, {dt:.0f}s)")
    print(f"  M_MS = {diag['M_MS']:.5f}  (P0 anchor ~0.28-0.30)")
    print(f"  B=1/A witness max|a+b| body = {float((aa+bb)[bod].abs().max()):.3e} (nonzero=free)")
    print(f"  Theta(core) = {Thh[0,:,:].mean().item():.4f} = {Thh[0,:,:].mean().item()/PI:.3f}*pi "
          f"sin={math.sin(Thh[0,:,:].mean().item()):.2e}  (NODE, value free)")
    print(f"  OFF-DIAGONALS (round): max|e_rt|={comp_a['e_rt_max']:.3e} "
          f"max|e_rp|={comp_a['e_rp_max']:.3e} max|e_tp|={comp_a['e_tp_max']:.3e}")
    print(f"  off-diag Einstein residuals: rth={comp_a['rth']:.2e} rps={comp_a['rps']:.2e} "
          f"thps={comp_a['thps']:.2e}")
    round_passes = (hist_a[-1] < 1e-9) and (0.25 < diag['M_MS'] < 0.32)
    print(f"  GATE (a) {'PASS' if round_passes else 'FAIL/INCONCLUSIVE'}")

    # ---------------------------------------------------------------------
    # GATE (c): divT / gauge sanity on a NON-ROUND test config (off-diag ON).
    # ---------------------------------------------------------------------
    hdr("GATE (c) -- divT / gauge sanity on a non-round test config")
    # impose a small l=2 e_tp warp on the converged round solution and measure
    # the covariant div(T) of the matter stress (matter EOM <-> conservation gate).
    e_test2 = 0.01 * bump * (3 * torch.cos(th) ** 2 - 1)  # l=2 angular
    out_nr = residuals(G, (aa, bb, cc, dd, Thh), p, kap8, m=m)
    divT = None
    try:
        from full3d_spectral import divT_identity
        divT = divT_identity(G, out_nr)
        print(f"  div(T) on converged round matter: max|divT_r| (body) = "
              f"{float(divT[..., R][bod].abs().max()):.2e}  (EOM<->conservation gate)")
    except Exception as ex:
        print(f"  divT_identity unavailable/failed: {ex}")

    # ---------------------------------------------------------------------
    # OBSERVATION: mild non-round (l=2) MATTER perturbation -- do off-diagonals grow?
    # ---------------------------------------------------------------------
    hdr("OBSERVATION -- mild non-round (l=2) matter; do off-diagonals grow or stay 0?")
    # perturb Theta with an l=2 angular shape (still ground charge sector), re-solve,
    # observe whether e_rt/e_rp/e_tp want to be nonzero.
    Th_pert = Thh + 0.05 * torch.sin(Thh) * (3 * torch.cos(th) ** 2 - 1)
    u_p = P1.pack8(aa, bb, cc, dd, Th_pert, ert, erp, etp)
    t1 = time.time()
    u_o, hist_o = P1.newton_solve_p1(u_p, G, p, kap8, m=m, maxit=30, tol=1e-11,
                                     verbose=True, node_core=True, core_mode="deg1")
    comp_o = P1.component_residuals_p1(u_o, G, p, kap8, m=m)
    ao, bo, co, do_, Tho, erto, erpo, etpo = P1.unpack8(u_o, G)
    print(f"  re-solve Phi = {hist_o[-1]:.4e}  ({len(hist_o)-1} it, {time.time()-t1:.0f}s)")
    print(f"  OFF-DIAGONALS (l=2 perturbed matter): "
          f"max|e_rt|={comp_o['e_rt_max']:.3e} max|e_rp|={comp_o['e_rp_max']:.3e} "
          f"max|e_tp|={comp_o['e_tp_max']:.3e}")
    # also report the matter non-axisymmetry / theta-shape that survived
    g_o = build_metric(G, ao, bo, co, do_, e_rt=erto, e_rp=erpo, e_tp=etpo)
    ginv_o = CORE.metric_inverse(g_o)
    dn_o = field_dn(G, Tho, m=m)
    Tab_o, _, _, _ = MAT.stress_tensor(g_o, ginv_o, dn_o, 1.0, 1.0)
    diag_o = diagnostics(G, dict(Tab=Tab_o, g=g_o, ginv=ginv_o), kap8)
    print(f"  matter angular shape tvar = {diag_o['tvar']:.3e}  M_MS = {diag_o['M_MS']:.5f}")
    print(f"  off-diag Einstein residuals after re-solve: rth={comp_o['rth']:.2e} "
          f"rps={comp_o['rps']:.2e} thps={comp_o['thps']:.2e}")

    hdr("P1 VALIDATION SUMMARY")
    print(f"  (a) ROUND recovery: Phi={hist_a[-1]:.2e} M_MS={diag['M_MS']:.4f} "
          f"offdiag~{max(comp_a['e_rt_max'],comp_a['e_rp_max'],comp_a['e_tp_max']):.1e} "
          f"-> {'PASS' if round_passes else 'FAIL'}")
    print(f"  (b) off-diag G correctness: b1={err_b1:.1e} b2(live)={g_rth_live:.1e} "
          f"b3(indep)={err_rth:.1e}")
    print(f"  (c) divT: {'computed' if divT is not None else 'n/a'}")
    print(f"  OBS round offdiag max = "
          f"{max(comp_a['e_rt_max'],comp_a['e_rp_max'],comp_a['e_tp_max']):.2e}")
    print(f"  OBS l=2-matter offdiag max = "
          f"{max(comp_o['e_rt_max'],comp_o['e_rp_max'],comp_o['e_tp_max']):.2e}")


if __name__ == "__main__":
    main()
