#!/usr/bin/env python3
"""
migration_convergence_guard.py -- SOLVE-LEVEL CHARACTERIZER for the p1 extension migration.

Driver: Claude (Opus 4.8). 2026-06-24; REFRAMED filter->characterizer 2026-06-25. INFRA. DATA-BLIND.

*** REFRAMED (Charles 2026-06-25, skill: solution-space-not-imposition). ***
This was a FILTER: it asserted "warp floors AND does NOT grow with Nr -> GREEN, else RED."  That
demands SMOOTHNESS -- it would stamp a REAL strong-field feature (a forming horizon at strong matter
coupling) as a "failure," which is an IMPOSITION (judging MERIT, the thing the gate must never do).
It is now a CHARACTERIZER: it REPORTS what the solve did and CLASSIFIES it, and never throws a
solution away on physics grounds.  The provenance/honesty-not-merit split it obeys:

  - NUMERIC HEALTH (did the solve converge -- residual drop, no NaN/Inf?) is a numeric fact, NOT a
    physics-merit judgment.  A solve that cannot reduce its own residual is broken numerics; that is
    the ONLY thing the exit code reflects (so it still catches a jacrev/codegen regression).
  - WARP-vs-Nr is AMBIGUOUS: N-growth is EITHER under-resolution (numeric) OR a real strong-field
    feature (horizon).  The characterizer CANNOT tell which -- that is resolved by ANALYSIS (GR
    corpus, the kap8 strong-coupling question), NOT by demanding smoothness here.  So warp behavior
    is REPORTED and CLASSIFIED (N-stable / N-growing), never failed.

WHY the solve-level run still matters: the fast pytest harness checks OPERATOR-level N-convergence on
an ANALYTIC metric.  It does NOT exercise the SOLVE.  This runs the production solver matter-on at two
grids so a NUMERIC regression (won't floor, NaN) is caught and the warp behavior is characterized for
the human/analysis step.

Usage: python3 migration_convergence_guard.py   (exit 0 = numerically converged, 1 = broken numerics;
       the warp CHARACTERIZATION is in the report, never in the exit code.)
As the solver gains phi/gtw/S^2, update _solve() to the new pack/interface.
"""
import os, sys, math, time
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from full3d_spectral import Grid3D, attach_coord_weight

GRIDS = (8, 10)           # two resolutions; the dense-jacrev X-continuation is heavy at
                          # Nr>=12 (Nr=12 was 8.6h). (8,10) still resolves a warp-vs-Nr trend.
CONVERGE_TOL = 1e-6       # NUMERIC-HEALTH only: a solve that floors below this has converged
                          # numerically.  This is NOT a physics filter -- a converged solve with a
                          # large/growing warp is a RESULT to characterize, not a failure.
GROW_FLAG = 1.5           # warp-growth factor above which we CLASSIFY the solve "N-growing" (report
                          # it for analysis; NOT a pass/fail line).
KAP8 = 1.0; P = 1.0; M = 1; MAXIT = 8   # M4a: kap8 0.05 -> 1.0 (the DERIVED round-gate value)
X_TARGET = -2.0e5         # M2+: the production (Cassini-bounded, stiff) X-kinetic value
BRANCH = "P"              # M3+: the Branch-P operator (adds the e^{2phi}-1 U potential)


def _solve(nr):
    """Run the production solver matter-on at Nr=nr; return (Phi, max_warp).  COMPLETE static
    solver: derived operator + off-diagonals live + NATIVE-S^2 3-component matter (seed = the
    canon degree-1 winding n=x/r; core FREE -- no Theta pin)."""
    import p1_residual_general_einstein as P1
    G = attach_coord_weight(Grid3D(Nr=nr, Nth=6, Nps=8, rc=0.1, cell=8.0))
    u0 = P1.seed_round_native(G, p=P, m=M)
    # M2: continue X -1 -> production -2e5 (the stiff value); characterize the warp there.
    u, hist, Xfin = P1.continuation_solve_p1(u0, G, P, KAP8, X_target=X_TARGET, m=M,
                                             branch=BRANCH, verbose=False)
    a, b, c, d, n1, n2, n3, phi, e_rt, e_rp, e_tp = P1.unpack11(u, G)
    F = P1.residual_vector_p1(u, G, P, KAP8, m=M, X=Xfin, branch=BRANCH)
    Phi = float((F * F).sum())
    mw = max(float(x.abs().max()) for x in (a, b, c, d))
    return Phi, mw


def _classify(res):
    """CHARACTERIZE the solve from (nr, Phi, warp) samples.  Returns (numeric_ok, lines).
    numeric_ok = did the solve CONVERGE NUMERICALLY (floored, finite) -- the only exit signal.
    The warp behavior is described, never failed."""
    phis = [p for _, p, _ in res]
    mws = [m for _, _, m in res]
    finite = all(math.isfinite(p) and math.isfinite(m) for _, p, m in res)
    floored = all(p < CONVERGE_TOL for p in phis)
    numeric_ok = finite and floored
    lines = []
    # numeric health (provenance/health, not merit)
    if not finite:
        lines.append("  NUMERIC HEALTH: BROKEN -- NaN/Inf in residual or warp (solve diverged numerically)")
    elif floored:
        lines.append(f"  NUMERIC HEALTH: converged (all Phi<{CONVERGE_TOL:.0e}); residual={phis[0]:.2e}->{phis[-1]:.2e}")
    else:
        lines.append(f"  NUMERIC HEALTH: did NOT floor (Phi={phis[0]:.2e}->{phis[-1]:.2e}); residual-limited solve")
    # warp characterization (NOT a verdict -- the ambiguous physics-vs-numeric signal)
    if mws[-1] <= mws[0] * GROW_FLAG:
        lines.append(f"  WARP vs Nr: N-STABLE (max|warp| {mws[0]:.2f}->{mws[-1]:.2f}, x{mws[-1]/max(mws[0],1e-30):.2f})")
    else:
        lines.append(f"  WARP vs Nr: N-GROWING (max|warp| {mws[0]:.2f}->{mws[-1]:.2f}, x{mws[-1]/max(mws[0],1e-30):.2f})")
        lines.append("    -> AMBIGUOUS: under-resolution OR a real strong-field feature (horizon).")
        lines.append("    -> RESOLVE BY ANALYSIS (GR strong-coupling corpus), NOT by demanding smoothness.")
    return numeric_ok, lines


def main():
    t0 = time.time(); res = []
    print(f"[migration characterizer] matter-on solve; grids={GRIDS} "
          f"converge_tol={CONVERGE_TOL:.0e} (CHARACTERIZER, not a pass/fail filter)", flush=True)
    for nr in GRIDS:
        Phi, mw = _solve(nr)
        res.append((nr, Phi, mw))
        print(f"  Nr={nr}: Phi={Phi:.3e}  max|warp(a..d)|={mw:.3f}  "
              f"t={time.time()-t0:.0f}s", flush=True)
    numeric_ok, lines = _classify(res)
    print("  --- characterization ---", flush=True)
    for ln in lines:
        print(ln, flush=True)
    print(f"  ==> NUMERICALLY {'CONVERGED' if numeric_ok else 'NOT CONVERGED'} "
          f"(exit reflects numeric health ONLY; warp behavior is characterized above, not failed)",
          flush=True)
    return 0 if numeric_ok else 1


if __name__ == "__main__":
    sys.exit(main())
