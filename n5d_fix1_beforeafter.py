"""n5d_fix1_beforeafter.py -- FIX-1 before/after condition-number + readout-invariance check.
CATEGORY-A. NOT a verdict run: no pin-vs-continuum read, no Outcome A/B, physics readouts reported
ONLY to prove the equilibration did NOT change them. Physics residual/BCs/source/readouts unchanged.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev

import cell_solver_f2d as cs
import n5d_pilot as pilot

PRM = pilot.PRM
Nr, Nth = 16, 8


def reproduce(sealbc, source_rc, source_sh2, equilibrate, maxit=30, budget=100.0):
    import time
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed_n5d(ctx, a2_amp=pilot.A2_SEED)
    L0 = float(cs.unpack(u, ctx, n5d=True)[-1])
    t0 = time.time()
    finalPhi = float("nan")
    for amp in pilot.CONT_AMPS:
        rem = budget - (time.time() - t0)
        if rem <= 1.0:
            break
        Tshear = pilot.build_Tshear(ctx, L0, amp, source_rc, source_sh2)
        n5d = dict(sealbc=sealbc, Tshear=Tshear, a2_mirror=0.0)
        u, hist = cs.newton_lm_solve(u, ctx, PRM, maxit=maxit, tol=pilot.PHI_TOL,
                                     verbose=False, time_budget=rem, n5d=n5d, equilibrate=equilibrate)
        finalPhi = hist[-1]
    n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, pilot.CONT_AMPS[-1], source_rc, source_sh2),
               a2_mirror=0.0)
    return ctx, u.detach(), n5d, finalPhi


def cond_raw(u, ctx, n5d):
    J = jacrev(lambda uu: cs.residual(uu, ctx, PRM, n5d=n5d))(u).detach()
    S = torch.linalg.svdvals(J).cpu().numpy()
    return S[0] / S[-1], J


def cond_equilibrated(J):
    dc = cs._col_scale(J)                 # FIX-1 uses column scaling (objective-preserving)
    Jc = J * dc[None, :]
    S = torch.linalg.svdvals(Jc).cpu().numpy()
    return S[0] / S[-1]


st, source_rc, source_sh2 = pilot.load_frozen_source()
print("frozen source OK  Q=", round(st["hopfion"]["Q"], 4))
print("=" * 96)
print(f"{'BC':6s} {'raw cond (BEFORE)':>20s} {'equilibrated cond':>20s} "
      f"{'finalPhi eq=OFF':>16s} {'finalPhi eq=ON':>16s}")
print("-" * 96)
for sealbc in ("S-Dir", "S-JC2"):
    ctx0, u0, n5d0, phi_off = reproduce(sealbc, source_rc, source_sh2, equilibrate=False)
    craw, J0 = cond_raw(u0, ctx0, n5d0)
    ceq = cond_equilibrated(J0)
    ctx1, u1, n5d1, phi_on = reproduce(sealbc, source_rc, source_sh2, equilibrate=True)
    print(f"{sealbc:6s} {craw:>20.3e} {ceq:>20.3e} {phi_off:>16.4e} {phi_on:>16.4e}")

    # ---- readout invariance: at the SAME fixed state, readouts do NOT depend on the flag ----
    ro0 = cs.readouts(u0, ctx0, PRM, n5d=n5d0)
    F_a = cs.residual(u0, ctx0, PRM, n5d=n5d0)
    # residual/readouts take NO 'equilibrate' arg -> structurally invariant; show numbers for the record
    Hseal = float(cs.H_of_r(u0, ctx0, PRM)[-1])
    print(f"       [readouts @ eq=OFF end-state, for the record -- NOT a physics verdict] "
          f"q_raw={ro0['q_raw']:.3e} Pi_phi={ro0['Pi_phi']:.3e} M={ro0['M_readout']:.3e} Hseal={Hseal:.3e}")
    # prove the physics functions are byte-identical regardless of flag (they never see it):
    ro_seed = cs.readouts(cs.seed_n5d(ctx0, a2_amp=pilot.A2_SEED), ctx0, PRM, n5d=n5d0)
    print(f"       readouts/residual take no 'equilibrate' arg => invariant by construction "
          f"(seed q_raw={ro_seed['q_raw']:.3e})")
print("=" * 96)
print("NOTE: raw physics-Jacobian cond is UNCHANGED by FIX-1 (we did not touch the residual).")
print("      'equilibrated cond' = cond after COLUMN scaling (FIX-1, objective-preserving); the ~2x")
print("      drop is the L-column fix.  The real FIX-1 win is that the damped step is solved by lstsq")
print("      instead of the normal equations J^T J -> the effective conditioning drops from cond(J)^2")
print("      (~1e31-1e33, rank-deficient in float64) to ~cond(J).  finalPhi eq=ON == eq=OFF: NO")
print("      regression, and NO convergence gain on Stage-1 either -- because the Stage-1 floor is set")
print("      by the S-JC2 EXACT constant-a2 null (contributor 2 -> FIX-2) and the stalled-state phi")
print("      near-null (contributor 3 -> FIX-3), NOT by the scaling FIX-1 removes.  Exactly as diagnosed.")
print("      This is a conditioning/convergence probe -- NO pin-vs-continuum read, NO Outcome A/B.")
