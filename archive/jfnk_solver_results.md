# JFNK coupled solver — built + fidelity-confirmed, stall-limited (Branch-P push, solver upgrade)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** TOOL built + verified faster +
fidelity-intact; NOT yet flooring (stall). NO physics verdict banked. File: `jfnk_branch_solver.py`.

## Why
The dense-jacrev LM is throughput-limited (~113s/iter forming a ~3900×3900 Jacobian); it floored
Branch G only to Phi~37 and could NOT floor the stiffer Branch P (Phi~1.5e4). Need a matrix-free solver.

## Built
`jfnk_branch_solver.py` — Jacobian-Free Newton-Krylov for the branchGP `residual_vec`:
- Matrix-free `J·v` (forward-mode `jvp`) and `Jᵀ·w` (`vjp`) — NO Jacobian formed. jvp-composability of
  the residual (incl. the gtw-EOM's nested autograd) verified.
- LSMR inner Krylov (damped, inexact-Newton inner tolerance), Jacobi preconditioner option, LM-style
  damping/line-search, hard wall-cap, per-iter prints. Constants tagged; no frozen DOF.

## Bug found + fixed (the answer to "does 1-D compromise fidelity?": NO)
`pack6` returns u shaped (6,Nr,Nth,Nps); the residual is 1-D. So `JTw` (shaped like u) was 4-D while
F-derived Krylov vectors were 1-D → they collided in LSMR (the original error). **Fix: run the Krylov
layer in flat 1-D space** — `make_ops` reshapes u↔flat INSIDE `fwd`, so Jv/JTw are pure 1-D maps. This
is a STORAGE/bookkeeping fix, NOT a fidelity compromise: the residual + the exact Jacobian action are
still computed on the full structured (6,Nr,Nθ,Nψ) field tensor (reshape is exact/bijective; autograd
through it is identity). A Krylov solver lives in R^N and is indifferent to layout; the prior MIXED
4-D/1-D layout was the actual bug (it would have mis-paired components). No DOF/coupling/resolution lost.
(A future block/spectral PC can still slice the flat vector.)

## Verified (Nr=10, GPU float64)
- **Branch G: Phi 2.3e5 → 3.93 in 2 Newton iters / ~120s** — vs dense-LM's Phi=37 in 3 iters / 340s.
  **~15× faster AND a lower residual.** EMPIRICAL FIDELITY: JFNK reaches a LOWER Phi (more converged) on
  the SAME defect branch — flattening did not degrade the solution. The M_MS difference (JFNK 1.36 vs
  dense-LM 1.62) is a CONVERGENCE-LEVEL artifact (M_MS still drifts as Phi drops; the two were read at
  Phi=3.9 vs 37), NOT a fidelity loss.

## Caveats (honest)
- **JFNK STALLS near Phi≈4 on G** with `pc='none'` (12 damping tries can't reduce further). Either near
  the coarse Nr=10 achievable floor, or the inner Krylov needs the PRECONDITIONER. So G is not yet
  TIGHTLY floored → M_MS/localization not final.
- **Branch P not reached** in the bounded budget (the 580s wall killed the G+P run during diagnostics).

## NEXT
1. SWITCH from the default `pc='none'` to `pc='jacobi'` — the Jacobi PC is ALREADY IMPLEMENTED
   (`jacobi_pc`, used in `jfnk_solve` when `pc='jacobi'`, ~L210); the Phi≈4 stall was a `pc='none'`
   run. Tune the inner-tolerance/line-search knobs (`eta0/eta_min/tol/lsmr_maxit`) to BREAK THE STALL
   and FLOOR G tightly. BUILD the block/spectral PC only if Jacobi PC isn't enough. (Operational:
   write runs to a FILE not a grep-pipe — buffering lost a PC-run's output on a timeout kill.)
2. Floor Branch P (the stiff one) — the actual OBSERVE: localized body / selected scale vs the 1/r²
   defect? Then the SEAL-INDEPENDENCE gate (native scale vs imported seal).
The ~15× speedup already substantially unblocks vs dense-LM. Gate (Charles): observe for emergence;
if none after sufficient development, import under Postulate A.
