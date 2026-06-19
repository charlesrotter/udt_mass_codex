#!/usr/bin/env python3
"""
coupled_tl_gates.py -- STAGE 2: RUN + OBSERVE the coupled time-live breather under
the CONTRACT gates A/B/C.

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  OBSERVE, not targeting.  DATA-BLIND.
Frame: coupled_timelive_solve_CONTRACT.md S2 (the gates), S4 (decision table).

GATE A -- BOX-CONTROL (3 criteria; a level claimed INTRINSIC must pass ALL):
  A1 no 1/R scaling: level flat (<few%) across >=8x cell-size range.
  A2 wall-relocation invariance: seal out by >=2x shifts level <few%.
  A3 intrinsic-lock NEGATIVE control: level must NOT equal l(l+1)W_inf (the angular
     charge barrier, already banked) NOR a cavity j_l-zero.  A level EQUAL to
     l(l+1)W_inf is the OLD charge barrier re-read, explicitly NOT new.

GATE B -- SOLVER-STRENGTH / CONVERGENCE (a stall = INCONCLUSIVE, not null):
  B1 a known-convergeable control (the static round soliton + the A=0 mode) MUST
     converge to floor on the SAME machinery at the SAME grid.
  B2 grid convergence: reported quantity stable across >=2 grid refinements.

GATE C -- STABILITY (constraint-respecting): the lowest-mode w2 sign IS the
  constraint-respecting stability indicator for the BREATHING mode (w2>0 = stable
  oscillation; w2<0 = tachyon/unstable).  This is NOT a fixed-metric Hessian count
  (which over-counts off-constraint negatives); it is the COUPLED breather frequency
  re-solved with the metric responding.  m=1 round = sign calibration.

THE DECISIVE QUESTION (S4): does the FINITE-A back-reaction produce a discrete bound
level passing Gate A that the A=0 proxy lacked (POSITIVE) -- or {l(l+1)W_inf floor +
box continuum} with no new bound structure (SCOPED NEGATIVE) -- or fail to converge
(INCONCLUSIVE)?
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
torch.set_default_dtype(torch.float64)
PI = math.pi

from radial_Bfree_soliton import grad_central, stress, make_grid
from coupled_tl_timelive import solve_coupled_breather, lowest_mode


def Winf_estimate(out):
    """Exterior W_inf = e^{2 v0}|_exterior for the angular barrier l(l+1)W_inf.
    v0 = -a (the dilaton); W = e^{2 v0_exterior}.  Read at the seal-adjacent body."""
    r = out['r'][0]; a = out['a'][0]
    # exterior region (Th0~0, unwound): take the outer 20% body average of e^{2(-a)}?
    # The angular barrier coefficient in the standing-wave operator is the exterior
    # e^{2 v0} = e^{-2 a} (the dressed-Laplacian weight).  Use the outer body value.
    ext = (r > r[-1]*0.7) & (r < r[-1]*0.97)
    W = torch.exp(-2.0*a)[ext].mean().item()
    return W


def gate_A_boxscan(xi, kap, A, cells=(8.0, 14.0, 28.0, 56.0), N=500):
    """A1/A2: R-scan of the lowest breather level + the l(l+1)W_inf negative control."""
    rows = []
    for cell in cells:
        rc = 0.05; ri = rc + cell
        r = make_grid(1, N, rc=rc, rint=ri, geom=False)
        out = solve_coupled_breather(r, xi, kap, A=A, outer=30)
        w2 = out['w2']
        Winf = Winf_estimate(out)
        # l=1 angular barrier l(l+1)W_inf = 2 W_inf (the banked charge floor)
        bar1 = 2.0*Winf
        rows.append((cell, w2, Winf, bar1, out['M_MS']))
    return rows


def gate_B_grid(xi, kap, A, grids=(300, 500, 800), cell=14.0):
    """B2: grid convergence of the lowest level + M_MS."""
    rows = []
    for N in grids:
        rc = 0.05; ri = rc + cell
        r = make_grid(1, N, rc=rc, rint=ri, geom=False)
        out = solve_coupled_breather(r, xi, kap, A=A, outer=30)
        rows.append((N, out['w2'], out['M_MS']))
    return rows


if __name__ == "__main__":
    xi = kap = 1.0
    print("="*78)
    print("STAGE 2 -- GATES on the coupled time-live breather")
    print("="*78)

    # pick a finite amplitude where the back-reaction is substantial (from 1c scan)
    A_TEST = 4.0

    print(f"\n--- GATE A (box-control), A=0 (proxy) vs A={A_TEST} (back-reaction) ---")
    for A in [0.0, A_TEST]:
        print(f"\n  amplitude A={A}:")
        rows = gate_A_boxscan(xi, kap, A)
        print("   cell    w2_low     W_inf    l(l+1)W_inf(=2W)   w2/bar1    M_MS")
        w2s = [rw[1] for rw in rows]
        for (cell, w2, Winf, bar1, M) in rows:
            print(f"   {cell:5.0f}  {w2:9.5f}  {Winf:7.4f}   {bar1:9.4f}        "
                  f"{w2/bar1:7.4f}  {M:.5f}")
        spread = (max(w2s)-min(w2s))/max(abs(max(w2s)), 1e-12)*100
        print(f"   --> w2_low spread over 7x cell range = {spread:.2f}%  "
              f"(A1: <few% => intrinsic; large => box-controlled)")

    print(f"\n--- GATE B (grid convergence), A={A_TEST} ---")
    rows = gate_B_grid(xi, kap, A_TEST)
    print("    N      w2_low      M_MS")
    for (N, w2, M) in rows:
        print(f"   {N:4d}  {w2:9.5f}  {M:.5f}")
    w2s = [rw[1] for rw in rows]
    print(f"   --> w2_low grid spread = "
          f"{(max(w2s)-min(w2s))/max(abs(max(w2s)),1e-12)*100:.2f}% "
          f"(B2: stable across refinements?)")

    print(f"\n--- GATE C (stability sign), A-scan ---")
    rc = 0.05; ri = rc + 14.0
    r = make_grid(1, 500, rc=rc, rint=ri, geom=False)
    for A in [0.0, 1.0, 2.0, 4.0, 8.0]:
        out = solve_coupled_breather(r, xi, kap, A=A, outer=30)
        w2 = out['w2']
        sign = "STABLE (w2>0)" if w2 > 0 else "TACHYON (w2<0)"
        print(f"   A={A:4.1f}: w2_low={w2:9.5f}  {sign}")
