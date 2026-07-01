#!/usr/bin/env python3
"""
phase1_geon_boxtest.py -- PHASE-1c step 3: the CONVENTION-ROBUST box-control test
of the nonlinear geon frequency bend.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE. c=1.

WHY: phase1_geon_solve.py found a genuine, N-converged, backreaction-driven bend
w(A) (bend vanishes when phi-dressing is switched off -> it IS the geon stress).
But the bend's R-scaling (dw/dA^2 ~ 1/R^2) was read with A = ||Psi||_2, whose
units carry R. The intrinsic-vs-box verdict must NOT depend on that convention.

THIS TEST fixes amplitude by R-INVARIANT, dimensionless measures and reports the
FRACTIONAL frequency shift (w-w0)/w0 -- itself dimensionless -- at fixed amplitude:
  measure 1: peak warp  p := max_r |Psi(r)| / max_r |Psi_lin(r)|   (dimensionless,
             = the actual metric-warp amplitude relative to the linear shape; this
             is the physical "how nonlinear is the wave" knob, R-independent).
  measure 2: the dimensionless backreaction depth  d := max_r |phi(r)| = max|A^2 F|
             (the geon's own gravitational potential depth -- a truly INTRINSIC
             quantity: the field's self-binding, not the box).

READ:
  * If (w-w0)/w0 at FIXED peak-warp p is R-INVARIANT -> the bend is set by the
    wave's own nonlinearity, intrinsic, NOT box -> GEON ESCAPE.
  * If (w-w0)/w0 at fixed p still falls with R -> the bend, though real and
    backreaction-driven, is still controlled by the box (bigger box = weaker
    self-gravity at the same warp) -> NO escape; the object is a box-confined
    nonlinear cavity mode, not a self-bound geon.
  * The phi-depth view: a self-bound geon should show (w-w0)/w0 a function of the
    backreaction depth d ALONE, collapsing across R. Test that collapse.
"""
import numpy as np
import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from phase1_geon_solve import GeonProblem, continue_amplitude, j2_first_zero
from scipy.special import spherical_jn


def branch_at_R(N, R, A_list, dress=True):
    prob, rows, w0 = continue_amplitude(N, R, A_list, dress=dress)
    # peak of the LINEAR shape on this cell (for normalizing peak-warp)
    r = prob.r
    Psi_lin = r * spherical_jn(2, w0 * r)
    nrm = np.sqrt(prob.cc @ (Psi_lin**2))
    peak_lin_unit = np.max(np.abs(Psi_lin / nrm))   # peak of unit-L2 linear shape
    out = []
    for rw in rows:
        # peak warp relative to unit-L2 linear shape, per unit A:
        # solver normalizes ||Psi||_2 = A, so unit-L2 shape scaled by A => peak = A*peak_lin_unit
        # actual max|Psi| stored as maxPsi
        p = rw['maxPsi'] / peak_lin_unit          # dimensionless peak-warp (= A if linear)
        # backreaction depth d = max|phi| = max|A^2 F| -- recompute from F
        # (Fmax stored; phi peak = A^2 * Fmax, but Fmax may be at different r; ok approx)
        d = (rw['A']**2) * rw['Fmax']
        frac = (rw['w'] - w0) / w0
        out.append(dict(A=rw['A'], w=rw['w'], frac=frac, p=p, d=d, ok=rw['ok'],
                        mR=rw['mR']))
    return w0, out


if __name__ == "__main__":
    np.set_printoptions(precision=6, linewidth=130)
    print("=" * 80)
    print("PHASE-1c CONVENTION-ROBUST BOX-CONTROL TEST of the geon frequency bend")
    print("=" * 80)
    N = 100
    A_list = [1e-3, 0.02, 0.05, 0.08, 0.1, 0.15, 0.2]
    R_list = [1.0, 2.0, 4.0]

    branches = {}
    for R in R_list:
        w0, out = branch_at_R(N, R, A_list, dress=True)
        branches[R] = (w0, out)

    # ---- View 1: fractional shift vs dimensionless PEAK WARP p ----
    print("\n[VIEW 1] fractional freq shift (w-w0)/w0  vs  peak-warp p  (per R).")
    print("If columns at MATCHED p agree across R -> intrinsic. If they fall with R -> box.")
    print(f"  {'p(target)':>10}", end="")
    for R in R_list:
        print(f" | R={R:<4.1f} frac/p^2", end="")
    print()
    # interpolate frac vs p at common p-targets
    p_targets = [0.05, 0.1, 0.15, 0.2]
    for pt in p_targets:
        print(f"  {pt:>10.3f}", end="")
        for R in R_list:
            w0, out = branches[R]
            ps = np.array([o['p'] for o in out if o['ok']])
            fr = np.array([o['frac'] for o in out if o['ok']])
            if ps.max() >= pt >= ps.min():
                fval = np.interp(pt, ps, fr)
                print(f" | {fval/pt**2:>13.6f}", end="")
            else:
                print(f" | {'(out of range)':>13}", end="")
        print()
    print("  [frac/p^2 = the dimensionless bend coefficient at fixed peak-warp.")
    print("   R-INVARIANT column -> intrinsic/geon escape; R-falling -> box-controlled.]")

    # ---- View 2: does fractional shift collapse as a function of backreaction depth d? ----
    print("\n[VIEW 2] fractional freq shift (w-w0)/w0  vs  backreaction depth d=max|phi|.")
    print("A self-bound geon: frac should be a function of d ALONE (collapse across R).")
    for R in R_list:
        w0, out = branches[R]
        print(f"  R={R:>4.1f}:")
        for o in out:
            if o['ok']:
                ratio = o['frac'] / o['d'] if o['d'] > 0 else float('nan')
                print(f"    A={o['A']:.3f}  d=max|phi|={o['d']:.4e}  frac={o['frac']:.4e}  frac/d={ratio:.4f}")
    print("  [If frac/d is the SAME constant across ALL rows and ALL R -> the freq")
    print("   shift is set purely by the geon's own potential depth (intrinsic).]")

    # ---- View 3: raw absolute bend scaling (recap, for the record) ----
    print("\n[VIEW 3] absolute bend recap: dw/dA^2 and its R-power (A=||Psi||_2 convention).")
    for R in R_list:
        w0, out = branches[R]
        oo = [o for o in out if o['ok']]
        a0, a1 = oo[0], oo[-1]
        dwdA2 = (a1['w'] - a0['w']) / (a1['A']**2 - a0['A']**2)
        print(f"  R={R:>4.1f}  w0={w0:.6f}  dw/dA^2={dwdA2:.6f}  *R={dwdA2*R:.6f}  *R^2={dwdA2*R**2:.6f}")
    print("=" * 80)
