#!/usr/bin/env python3
"""
migration_convergence_guard.py -- SOLVE-LEVEL N-convergence guard for the p1
extension migration.

Driver: Claude (Opus 4.8). 2026-06-24. INFRA. DATA-BLIND.

WHY: the fast pytest harness checks OPERATOR-level N-convergence (operator on an
ANALYTIC metric at rising Nr).  It does NOT catch a SOLVE-level divergence -- the
class of bug that sank the branchGP prototype (matter-on floor stuck ~0.18 with
metric warps a..d ~3-7 that GROW with Nr, vs p1 which floors a matter solve to
~1e-14 with small warps a,b~1/c,d~0.3).  This guard RUNS the production solver
matter-on at two grids and ASSERTS (a) it floors below tol, (b) the metric warps
do NOT grow with Nr.  Run it after EVERY migration increment; the increment that
turns it RED is the divergence culprit.

Baseline (current p1, a=-1 GR baseline, S^3 winding, kap8=0.05): GREEN
  Nr=10: Phi=1.0e-14, max|a|=1.08 |b|=1.00 |c|=0.38 |d|=0.23.

Usage: python3 migration_convergence_guard.py   (exit 0 = green, 1 = red)
As the solver gains phi/gtw/S^2, update _solve() to the new pack/interface.
"""
import os, sys, math, time
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from full3d_spectral import Grid3D, attach_coord_weight

GRIDS = (8, 10)           # two resolutions; the dense-jacrev X-continuation is heavy at
                          # Nr>=12 (Nr=12 was 8.6h). (8,10) still catches a branchGP-type
                          # warp-growth (which showed clearly at the smallest grids).
FLOOR_TOL = 1e-6          # a clean solve floors well below this; branchGP stuck ~0.18
GROW_TOL = 1.5            # max-warp may not grow by more than this factor across grids
KAP8 = 1.0; P = 1.0; M = 1; MAXIT = 8   # M4a: kap8 0.05 -> 1.0 (the DERIVED round-gate value)
X_TARGET = -2.0e5         # M2+: the production (Cassini-bounded, stiff) X-kinetic value
BRANCH = "P"              # M3+: the Branch-P operator (adds the e^{2phi}-1 U potential)


def _solve(nr):
    """Run the CURRENT production solver matter-on at Nr=nr; return (Phi, max_warp).
    UPDATE THIS as the migration adds phi/gtw/native-S^2 (pack8 -> pack9 -> ...)."""
    import p1_residual_general_einstein as P1
    G = attach_coord_weight(Grid3D(Nr=nr, Nth=6, Nps=8, rc=0.1, cell=8.0))
    dev = G.dev; r = G.Rg; s = (r - G.rc) / (G.ri - G.rc)
    z = torch.zeros(nr, G.Nth, G.Nps, device=dev)
    a = -1.0 * (1 - s); b = 1.0 * (1 - s); Th = math.pi * (1 - s)
    u0 = P1.pack6(a, b, z.clone(), z.clone(), Th, z.clone())
    # M2: continue X -1 -> production -2e5 (the stiff value); guard N-convergence there.
    u, hist, Xfin = P1.continuation_solve_p1(u0, G, P, KAP8, X_target=X_TARGET, m=M,
                                             core_mode='deg1', branch=BRANCH, verbose=False)
    a, b, c, d, Th, phi = P1.unpack6(u, G)
    F = P1.residual_vector_p1(u, G, P, KAP8, m=M, core_mode='deg1', X=Xfin, branch=BRANCH)
    Phi = float((F * F).sum())
    mw = max(float(x.abs().max()) for x in (a, b, c, d))
    return Phi, mw


def main():
    t0 = time.time(); res = []
    print(f"[migration guard] matter-on N-convergence; grids={GRIDS} "
          f"floor_tol={FLOOR_TOL:.0e} grow_tol={GROW_TOL}", flush=True)
    for nr in GRIDS:
        Phi, mw = _solve(nr)
        res.append((nr, Phi, mw))
        print(f"  Nr={nr}: Phi={Phi:.3e}  max|warp(a..d)|={mw:.3f}  "
              f"t={time.time()-t0:.0f}s", flush=True)
    phi_ok = all(p < FLOOR_TOL for _, p, _ in res)
    mws = [m for _, _, m in res]
    grow_ok = mws[-1] <= mws[0] * GROW_TOL
    print(f"  FLOOR: {'PASS' if phi_ok else 'FAIL'} (all Phi<{FLOOR_TOL:.0e})", flush=True)
    print(f"  N-CONVERGE: {'PASS' if grow_ok else 'FAIL'} "
          f"(max-warp {mws[0]:.2f}->{mws[-1]:.2f}, <= x{GROW_TOL})", flush=True)
    green = phi_ok and grow_ok
    print(f"  ==> GUARD {'GREEN' if green else 'RED'}", flush=True)
    return 0 if green else 1


if __name__ == "__main__":
    sys.exit(main())
