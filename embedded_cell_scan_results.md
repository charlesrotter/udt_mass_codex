# Embedded-cell scan (test #1) — does H_cell=H_amb admit a finite cell? — SOLVER-LIMITED LEAD

**Date:** 2026-07-01. **Mode:** OBSERVE (Charles's go: "commit and push so I can get input from
claude.ai"). **Driver:** Claude Code. **Script:** `cell_solver_f2d_embedded_scan.py` (reuses the
CAS-verified operators of `cell_solver_f2d.py`). **Status:** PROVISIONAL / a LEAD — NOT a banked
result, NOT a verdict. **No wall numbers. Scoped to round/static/N≤3/Z=8/coarse grid.**
**For the claude.ai session's input.** Foundation: `embedded_cell_closure_H_amb_results.md`
(H_cell=H_amb DERIVED + BLIND-VERIFIED).

## The question
The embedded closure `H_cell(seal)=H_ambient` is derived + blind-verified — it is the scale-pin the
closed cell (H=0) lacked. Test #1 (Charles's plan: "if #1 passes, do #2 = solve the universe cell"):
**does H_cell=H_amb actually ADMIT an isolated finite cell?** Held H_amb FIXED per scan (pre-reg
criterion 5; one ambient value at a time), scanned N=1,2,3.

## What was observed (two instruments)
**MODE A — free-L (L a Newton unknown), closure H(seal)=H_amb.** For every N and every fixed H_amb:
- reachable H_amb → the cell COLLAPSES (L→~0.01–0.3, Phi stalls ~1e-3, the closure H_seal is hit but
  at a degenerate shrinking cell) or does not converge;
- unreachable H_amb → RUNAWAY (L→1e6–1e9, Phi→1e-13 but Derrick identity violated by ~1e6–1e9 →
  SPURIOUS, flagged by the built-in Derrick check).
No finite-L convergence in between. The free-L direction is poorly controlled (see conditioning).

**MODE B — fixed-L (well-conditioned: converges to 1e-13 at every L), read the clean H(seal)(L) curve.**
- **N=1:** smooth MONOTONE H(seal)(L) (≈−0.74→−0.97), free-f relaxes to rigid (max|u|→0). One crossing
  per H_amb → a single cell size at most, no discrete family. (Rigid-collapse branch, Step-0 V7.)
- **N=3, L≳2:** the solver converges CLEANLY (Phi 1e-8→1e-13) to a **scale-free plateau**:
  H_seal ≈ **+4.18 CONSTANT** from L≈2 to 25, ρ_c≈1.45 stable, a genuinely θ-deformed knot
  (max|u|≈0.37) but with **radial structure I_r→0** (~1e-13). Constant H_seal(L) ⇒ every L satisfies
  the closure at that one H_amb ⇒ a **CONTINUUM**, not an isolated cell. (Matches the project's
  standing "classical UDT gives a continuum.")
- **N=2 (all L), N=3 (small L):** the solver STALLS (Phi ~1e-3 to 1e-1, ρ_c inflates to ~50) — NOT
  trustworthy; H_seal jumps around (garbage) where Phi is bad.

## The honest read (why this is a LEAD, not a negative) — SOLVER-FIRST
- **Where the solver converges cleanly, it shows CONTINUUM / scale-free, not isolated cells.**
- **But it STALLS across much of the (N,L) space** — exactly the region (intermediate L, N≥2, a
  radial-structure I_r>0 branch) where an isolated cell would live. Cause is known and NUMERIC, not
  metric: the build flagged **conditioning ~5e9** (Chebyshev endpoint amplification) + a poorly-
  controlled free-L direction. A "no cell" read through a stalling solver is FORBIDDEN (mismatch →
  SOLVER, not mechanism / not metric). This indicts the SOLVER's completeness, not the closure.
- The build already named the remedy it did not install: the **galerkin BC-recombined basis**
  (`galerkin_basis.py`, Category-A reusable machinery) that fixed conditioning by orders of magnitude
  in the old solver, plus L- (or H_amb-) continuation.

## Recommended next (solver-first, for discussion with claude.ai)
1. Install the galerkin BC-recombined basis + continuation so the intermediate-L / N≥2 / I_r>0 region
   converges cleanly (Phi→1e-13 everywhere, not just the extremes).
2. Deliberately seed and continue an **I_r>0 (radial-structure) branch** — the pre-reg's "don't insert
   I_r by hand" stands, but the solver must be ABLE to hold it if it exists; the current stall may be
   hiding it.
3. THEN re-run test #1 cleanly. Only after a clean convergence map is "continuum vs isolated" a real
   answer. If it is still continuum with everything converged and I_r-branch explored → a scoped
   negative pointing at Risk-1 (round-static may wall off discreteness → off-round / non-static next).

## Premises / scope
Constrained-two-player, round, static, N≤3, Z=8, ξ=κ=1, coarse grid (Nr=12, Nθ=14), source-free
Class-A-embedded seal, H_amb held fixed (not a per-solution knob). All CHOSE/held-fixed. The embedded
closure H_cell=H_amb itself is DERIVED+blind-verified (upstream doc); THIS doc is only the numerical
attempt to solve it, and it is solver-limited.

## VERIFIER
Not independently verified — this is a PROVISIONAL lab-log of an OBSERVE run, explicitly labeled
solver-limited, committed for claude.ai's input per Charles. No banked claim rides on it.
