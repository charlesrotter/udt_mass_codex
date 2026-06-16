#!/usr/bin/env python3
"""
full3d_final_run.py -- consolidated validation + honest search-attempt log for the
full-3-D spectral coupled solver.  Run blocking.  DATA-BLIND.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys, time, math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, build_metric, residuals,
    diagnostics, matter_el_3d, einstein_mixed_weyl, DEV, PI)
from full3d_solver import round_seed, lm_solve, residual_vector, unpack, pack
from full3d_campaign import perturb, diag_full
import whole_metric_3d_core as CORE
import spectral_radial_soliton as SR

stage = sys.argv[1] if len(sys.argv) > 1 else "all"


def banner(s): print("\n"+"="*70+"\n"+s+"\n"+"="*70)

if stage in ("all", "einstein"):
    banner("A. ANALYTIC 3-D EINSTEIN -- flat=0, Schwarzschild exponential")
    for (Nr, Nth, Nps) in [(20, 6, 8), (30, 12, 8)]:
        G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)
        z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
        Gm = einstein_mixed_weyl(G, z, z, z, z)
        print(f"  flat Nr={Nr} Nth={Nth} Nps={Nps}: max|G| body = {float(Gm[G.body].abs().max()):.2e}")
    M = 0.3
    for Nr in [16, 32, 48]:
        G = Grid3D(Nr, 6, 8, rc=1.0, cell=14.0); G = attach_coord_weight(G)
        f = 1 - 2*M/G.Rg; a = 0.5*torch.log(f); b = -0.5*torch.log(f); z = torch.zeros_like(a)
        Gm = einstein_mixed_weyl(G, a, b, z, z)
        print(f"  Schwarzschild Nr={Nr}: max|G| body = {float(Gm[G.body].abs().max()):.2e}")

if stage in ("all", "el"):
    banner("B. CORRECT 3-D MATTER EL -- machine-zero on round soliton")
    for Nr in [48, 64]:
        sol = SR.solve(Nr-1, rc=0.05, cell=14.0, p=0.4, kap8=0.05, maxit=80, tol=1e-12)
        for (Nth, Nps) in [(8, 8), (8, 12)]:
            G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)
            def E(x): return torch.tensor(x, device=DEV)[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()
            z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
            a, b, c, d, Th = E(sol['a']), E(sol['b']), z, z, E(sol['Th'])
            el = matter_el_3d(G, a, b, c, d, Th, m=1)
            print(f"  Nr={Nr} Nth={Nth} Nps={Nps}: max|EL| body = {float(el[G.body].abs().max()):.2e}")

if stage in ("all", "gate"):
    banner("C. VALIDATION GATE -- round #56 recovered in 3-D basis")
    for (nr, nt, npp) in [(40, 8, 8), (48, 10, 8), (40, 8, 12)]:
        G = Grid3D(nr, nt, npp, rc=0.05, cell=14.0); G = attach_coord_weight(G)
        u0, sol = round_seed(G, p=0.4, kap8=0.05)
        d0 = diag_full(G, u0, 0.4, 0.05)
        t0 = time.time()
        u, h = lm_solve(u0, G, 0.4, 0.05, maxit=18, lam0=1e-2, tol=1e-9)
        dg = diag_full(G, u, 0.4, 0.05)
        print(f"  Nr={nr} Nth={nt} Nps={npp} (t={time.time()-t0:.0f}s): "
              f"seedPhi={d0['Phi']:.1e}->Phi={dg['Phi']:.2e} M_MS={dg['M_MS']:.5f} "
              f"(#56 {sol['M_MS']:.5f}) tvar={dg['tvar']:.1e} psivar={dg['psivar']:.1e} EL={dg['elmax']:.1e}")

if stage in ("all", "robust"):
    banner("D. OFF-ROUND RELAX ATTEMPT -- non-axisym + axisym CONTROL (honest)")
    G = Grid3D(32, 6, 6, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=0.4, kap8=0.05)
    for kind in ['axi_l2', 'psi1', 'psi2']:
        us = perturb(G, u0, kind, amp=0.25)
        ds = diag_full(G, us, 0.4, 0.05)
        u = us; t0 = time.time()
        for blk in range(6):
            u, h = lm_solve(u, G, 0.4, 0.05, maxit=10, lam0=1e-2, tol=1e-11)
        dg = diag_full(G, u, 0.4, 0.05)
        print(f"  {kind:7s}: seed(Phi={ds['Phi']:.1e},psivar={ds['psivar']:.2f},tvar={ds['tvar']:.2f}) "
              f"-> (t={time.time()-t0:.0f}s) Phi={dg['Phi']:.2e} psivar={dg['psivar']:.2e} "
              f"tvar={dg['tvar']:.2e} M_MS={dg['M_MS']:.5f}")
