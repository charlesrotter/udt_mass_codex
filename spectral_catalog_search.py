#!/usr/bin/env python3
"""
spectral_catalog_search.py -- STAGE B robustness + STAGE C catalog search on the
spectral 2-D coupled solver (MATTER FREE).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.
Report whichever way it falls.

THE KEY DIFFERENCE FROM #58: the MATTER deforms.  #58 had to freeze the matter
(FD inner-body EL truncation ~0.2 -> w_matter=0), so matter-shaped catalog types
were never probed.  Here the spectral matter EL is machine-zero on the round
soliton, so we seed ANGULAR matter shapes Theta(r,theta) (multipole l=1..4,
prolate/oblate, ring/toroidal, two-center, large-amplitude) AND metric-shape DOF,
let BOTH relax, and classify: round family, or a disconnected stable type
(persistent gauge-invariant shape AT the residual floor, distinct M_MS).

CLASSIFIER (gauge-invariant): theta-variation of T^t_t (energy density) in the
body -- round => 0; PLUS the metric-shape DOF c,d magnitude; PLUS the final
residual norm Phi (a true solution sits at the floor).  DISCONNECTED signature =
Phi at the gate floor WITH a persistent gauge-invariant shape AND distinct M_MS.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import math
import torch
torch.set_default_dtype(torch.float64)
import sys

from spectral_catalog_solver import (TGrid, round_seed, lm_solve_dense, residual_vector,
                                      diagnostics, unpack, pack, DEV, PI)


def legP(l, x):
    from numpy.polynomial.legendre import Legendre
    cc = np.zeros(l+1); cc[l] = 1.0
    return Legendre(cc)(x)


def perturb_matter(u0, G, kind, amp):
    """Return a new packed state with the MATTER profile Theta perturbed by an
    angular shape (multipole / prolate-oblate / ring / two-center / large-amp).
    Metric a,b,c,d left at the round seed (they relax under the solve)."""
    a, b, c, d, Th = unpack(u0, G)
    a = a.clone(); b = b.clone(); c = c.clone(); d = d.clone(); Th = Th.clone()
    mu = torch.cos(G.THm)        # cos(theta)
    rprof = torch.exp(-((G.R - 2.0)/1.5)**2)   # localize the bump near the body
    if kind.startswith('l') and kind[1:].isdigit():
        l = int(kind[1:])
        Pl = torch.tensor(legP(l, mu.cpu().numpy()), device=DEV)
        Th = Th + amp*rprof*Pl
    elif kind == 'prolate':
        Th = Th + amp*rprof*(3*mu**2 - 1)/2
    elif kind == 'oblate':
        Th = Th - amp*rprof*(3*mu**2 - 1)/2
    elif kind == 'ring':           # concentrate matter near equator (theta=pi/2)
        Th = Th + amp*rprof*torch.sin(G.THm)**2
    elif kind == 'twocenter':      # split toward poles
        Th = Th + amp*rprof*(torch.cos(G.THm)**2)
    elif kind == 'largeamp':       # strong round deepening (matter amplitude)
        Th = Th + amp*torch.exp(-((G.R-1.5)/1.0)**2)
    # keep winding BCs
    Th[0, :] = PI; Th[-1, :] = 0.0
    return pack(a, b, c, d, Th)


def run_seed(G, kind, amp, p=0.4, kap8=0.05, blocks=5, iters_per=10, wmat=1.0):
    u0, rad = round_seed(G, p=p, kap8=kap8)
    u = perturb_matter(u0, G, kind, amp)
    F, rf = residual_vector(u, G, p, kap8, wmat=wmat)
    d0 = diagnostics(G, rf, kap8)
    traj = [(0, float((F**2).sum()), d0['tvar'], d0['M_MS'])]
    for blk in range(blocks):
        u, rf, hist = lm_solve_dense(u, G, p, kap8, maxit=iters_per, wmat=wmat,
                                     lam0=1e-4)
        dg = diagnostics(G, rf, kap8)
        traj.append((blk+1, float((residual_vector(u, G, p, kap8, wmat=wmat)[0]**2).sum()),
                     dg['tvar'], dg['M_MS']))
    dg = diagnostics(G, rf, kap8)
    return dict(traj=traj, final=dg, seed_tvar=d0['tvar'], seed_M=d0['M_MS'])


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'robust'
    Nr, Nth = 48, 8
    G = TGrid(Nr, Nth, rc=0.05, cell=14.0)

    if mode == 'robust':
        print("=== STAGE B ROBUSTNESS: perturbed MATTER (l=2) relax-back ===")
        r = run_seed(G, 'l2', 0.30, blocks=6, iters_per=12)
        print(f"seed: tvar={r['seed_tvar']:.4f} M_MS={r['seed_M']:.5f}")
        print(f"{'block':>5} {'Phi':>12} {'tvar(GI shape)':>15} {'M_MS':>10}")
        for (blk, phi, tv, M) in r['traj']:
            print(f"{blk:>5} {phi:>12.4e} {tv:>15.4e} {M:>10.5f}")
        f = r['final']
        print(f"final residuals: res_tt={f['res_tt']:.2e} res_thth={f['res_thth']:.2e} "
              f"res_rth={f['res_rth']:.2e} res_EL={f['res_EL']:.2e} cdshape={f['cdshape']:.2e}")

    elif mode == 'continuation':
        # Natural-parameter continuation in the depth dial p: follow the round
        # branch, monitor the smallest singular value of the Jacobian (a branch
        # point / bifurcation = sigma_min -> 0) and M_MS(p) for any fold/jump.
        print("=== CONTINUATION in depth dial p (branch map; bifurcation hunt) ===")
        print(f"{'p':>5} {'M_MS':>10} {'Phi':>11} {'sigma_min(J)':>13} {'tvar':>10}")
        import torch as _t
        u = None
        for p in [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]:
            if u is None:
                u, rad = round_seed(G, p=p, kap8=0.05)
            u, rf, h = lm_solve_dense(u, G, p, 0.05, maxit=20, lam0=1e-4)
            dg = diagnostics(G, rf, 0.05)
            # smallest singular value of the Jacobian at the solution
            from spectral_catalog_solver import residual_vector as RV
            Ffun = lambda uu: RV(uu, G, p, 0.05)[0]
            J = _t.autograd.functional.jacobian(Ffun, u.detach(), vectorize=True)
            s = _t.linalg.svdvals(J)
            phi = float((Ffun(u)**2).sum())
            print(f"{p:>5.2f} {dg['M_MS']:>10.5f} {phi:>11.3e} {float(s.min()):>13.3e} {dg['tvar']:>10.3e}")

    elif mode == 'search':
        print("=== STAGE C CATALOG SEARCH: MATTER-shaped seeds (matter FREE) ===")
        seeds = [('l1', 0.30), ('l2', 0.30), ('l3', 0.30), ('l4', 0.30),
                 ('prolate', 0.30), ('oblate', 0.30), ('ring', 0.40),
                 ('twocenter', 0.40), ('largeamp', 0.50)]
        print(f"{'seed':>10} {'seed_tvar':>10} {'fin_tvar':>10} {'fin_Phi':>11} "
              f"{'M_MS':>9} {'dM':>9} {'cdshape':>9} {'res_EL':>9} {'read':>22}")
        Mround = 0.28121
        for kind, amp in seeds:
            r = run_seed(G, kind, amp, blocks=5, iters_per=12)
            f = r['final']
            phi = r['traj'][-1][1]
            dM = f['M_MS'] - Mround
            # classify
            if phi > 1e-2:
                read = "unconverged (Phi high)"
            elif f['tvar'] < 5e-3 and abs(dM) < 5e-3:
                read = "relaxed -> round"
            elif f['tvar'] > 1e-2 and phi < 1e-2:
                read = "DISCONNECTED? persistent"
            else:
                read = "relaxing -> round"
            print(f"{kind:>10} {r['seed_tvar']:>10.4f} {f['tvar']:>10.4f} {phi:>11.3e} "
                  f"{f['M_MS']:>9.5f} {dM:>+9.5f} {f['cdshape']:>9.2e} {f['res_EL']:>9.2e} {read:>22}")
