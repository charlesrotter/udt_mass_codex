#!/usr/bin/env python3
"""
full3d_campaign.py -- the FULL-3-D validation gate + non-axisym robustness +
NON-AXISYMMETRIC and HIGHER-WINDING catalog search.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

Reports WHAT IS THERE.  The discriminant for a DISCONNECTED non-axisym type:
a perturbed seed must ARREST at finite gauge-invariant psi-shape (psivar) WITH the
Einstein+EL residual at the floor.  Relax-back (psivar -> round floor) = NO type.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys, time, math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, residuals, diagnostics,
    field_dn, build_metric, DEV, PI)
from full3d_solver import round_seed, lm_solve, residual_vector, unpack, pack
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT


def legP(l, x):
    from numpy.polynomial.legendre import Legendre
    cc = np.zeros(l+1); cc[l] = 1.0
    return Legendre(cc)(x)


def diag_full(G, u, p, kap8, m=1):
    a, b, c, d, Th = unpack(u, G)
    out = residuals(G, (a, b, c, d, Th), p, kap8, m=m)
    dg = diagnostics(G, out, kap8)
    F = residual_vector(u, G, p, kap8, m=m)
    dg['Phi'] = float((F*F).sum())
    dg['elmax'] = float(out['el'][G.body].abs().max())
    return dg


def perturb(G, u0, kind, amp=0.25):
    """Add a NON-AXISYMMETRIC / lobed / higher-structure deformation to Theta."""
    a, b, c, d, Th = unpack(u0, G)
    Th = Th.clone()
    rprof = torch.exp(-((G.Rg-2.0)/1.5)**2)
    cth = torch.cos(G.THg); sth = G.STHg
    ps = G.PSg
    if kind == 'psi1':                 # m=1 azimuthal lobe (l=1,|m|=1 real harmonic)
        Th = Th + amp*rprof*sth*torch.cos(ps)
    elif kind == 'psi2':               # m=2 azimuthal (bar/ellipsoidal in psi)
        Th = Th + amp*rprof*sth**2*torch.cos(2*ps)
    elif kind == 'psi3':               # m=3 azimuthal (3-lobe)
        Th = Th + amp*rprof*sth**3*torch.cos(3*ps)
    elif kind == 'tetra':              # tetrahedral-like Y_3 combination
        Th = Th + amp*rprof*(sth**3*torch.cos(3*ps) + 0.8*cth*(5*cth**2-3))
    elif kind == 'cube':               # cubic/octahedral Y_4-like
        Th = Th + amp*rprof*(sth**4*torch.cos(4*ps) + 0.7*(35*cth**4-30*cth**2+3))
    elif kind == 'lobed2c':            # two off-axis lobes (non-axisym dipole)
        Th = Th + amp*rprof*sth*torch.cos(ps)*cth
    elif kind == 'axi_l2':             # axisymmetric l=2 control (must also relax)
        Pl = torch.tensor(legP(2, cth.cpu().numpy()), device=DEV)
        Th = Th + amp*rprof*Pl
    else:
        raise ValueError(kind)
    Th[0, :, :] = m_global*PI; Th[-1, :, :] = 0.0
    return pack(a, b, c, d, Th)


m_global = 1


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "gate"
    Nr, Nth, Nps = 40, 8, 8
    p, kap8 = 0.4, 0.05
    G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)

    if mode == "gate":
        print("=== VALIDATION GATE: round #56 recovery in 3-D basis ===")
        for (nr, nt, npp) in [(40, 8, 8), (48, 10, 8), (40, 8, 12)]:
            Gg = Grid3D(nr, nt, npp, rc=0.05, cell=14.0); Gg = attach_coord_weight(Gg)
            u0, sol = round_seed(Gg, p=p, kap8=kap8)
            d0 = diag_full(Gg, u0, p, kap8)
            u, hist = lm_solve(u0, Gg, p, kap8, maxit=20, lam0=1e-2, tol=1e-9)
            dg = diag_full(Gg, u, p, kap8)
            print(f"  Nr={nr} Nth={nt} Nps={npp}: seedPhi={d0['Phi']:.2e} -> "
                  f"Phi={dg['Phi']:.3e} M_MS={dg['M_MS']:.5f} (#56 {sol['M_MS']:.5f}) "
                  f"tvar={dg['tvar']:.2e} psivar={dg['psivar']:.2e} EL={dg['elmax']:.2e}")

    elif mode == "robust":
        m_global = 1
        print("=== NON-AXISYM ROBUSTNESS: perturbed seeds relax back? ===")
        u0, sol = round_seed(G, p=p, kap8=kap8)
        for kind in ['psi1', 'psi2', 'tetra', 'axi_l2']:
            us = perturb(G, u0, kind, amp=0.25)
            ds = diag_full(G, us, p, kap8)
            u = us
            print(f"\n seed={kind}: seed psivar={ds['psivar']:.3e} tvar={ds['tvar']:.3e} Phi={ds['Phi']:.2e}")
            for blk in range(4):
                u, h = lm_solve(u, G, p, kap8, maxit=8, lam0=1e-2, tol=1e-10)
                dg = diag_full(G, u, p, kap8)
                print(f"   block {blk+1}: Phi={dg['Phi']:.3e} psivar={dg['psivar']:.3e} "
                      f"tvar={dg['tvar']:.3e} M_MS={dg['M_MS']:.5f}")

    elif mode == "winding":
        print("=== HIGHER-WINDING SEARCH: m=1,2,3,4 (no symmetry imposed) ===")
        for m in [1, 2, 3, 4]:
            Gg = Grid3D(48, 8, 8, rc=0.05, cell=14.0); Gg = attach_coord_weight(Gg)
            u0, sol = round_seed(Gg, p=p, kap8=kap8)   # round m=1 metric seed
            a, b, c, d, _ = unpack(u0, Gg)
            L = 1.0; rc = Gg.rc
            Thm = (m*PI)*0.5*(1 - torch.tanh((Gg.Rg - (rc+2*L))/(0.8*L)))
            Thm[0, :, :] = m*PI; Thm[-1, :, :] = 0.0
            um = pack(a, b, c, d, Thm)
            d0 = diag_full(Gg, um, p, kap8, m=m)
            print(f"\n m={m}: seed Phi={d0['Phi']:.2e} M_MS={d0['M_MS']:.5f}")
            u = um
            for blk in range(6):
                u, h = lm_solve(u, Gg, p, kap8, m=m, maxit=8, lam0=1e-2, tol=1e-10)
                dg = diag_full(Gg, u, p, kap8, m=m)
                if blk in (0, 2, 5):
                    print(f"   block {blk+1}: Phi={dg['Phi']:.3e} M_MS={dg['M_MS']:.5f} "
                          f"tvar={dg['tvar']:.3e} psivar={dg['psivar']:.3e} EL={dg['elmax']:.2e}")

    elif mode == "search":
        m_global = 1
        print("=== NON-AXISYM CHARGE-1 CATALOG SEARCH (lobed/platonic seeds) ===")
        u0, sol = round_seed(G, p=p, kap8=kap8)
        for kind in ['psi1', 'psi2', 'psi3', 'tetra', 'cube', 'lobed2c']:
            us = perturb(G, u0, kind, amp=0.30)
            ds = diag_full(G, us, p, kap8)
            u = us
            for blk in range(5):
                u, h = lm_solve(u, G, p, kap8, maxit=8, lam0=1e-2, tol=1e-10)
            dg = diag_full(G, u, p, kap8)
            read = ("ARREST-non-axisym?" if dg['psivar'] > 3e-2 and dg['Phi'] < 1e-2
                    else "relaxed->round")
            print(f"  {kind:8s}: seed psivar={ds['psivar']:.3f} -> final psivar={dg['psivar']:.3e} "
                  f"tvar={dg['tvar']:.3e} Phi={dg['Phi']:.2e} M_MS={dg['M_MS']:.5f}  [{read}]")
