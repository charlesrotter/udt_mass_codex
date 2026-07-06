# N5d Stage-2 PILOT-PREFLIGHT — conditioning readiness (π₂ tile; DESIGN / PROVISIONAL / Outcome D)

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M) · script `n5d_stage2_pilot_preflight.py`.
**Category-A numerical diagnostic only** — forward residual + ONE `jacrev` Jacobian + SVD at a bounded
STRUCTURED (non-collapsed) state. **NO solve, NO pilot, NO verdict, NO Outcome A/B, NO continuum lead.**
Purpose (Charles-gated, DESIGN §8): confirm the implemented co-relaxed π₂ solver is numerically READY at a
structured (not collapsed-degenerate) state BEFORE any Stage-2 pilot solve is authorized.

## Setup
`main` @ `aed1e04` (includes Stage-2b impl `6a0ac15`). Full suite: **pytest 67 passed / 1 xfailed.**
State = `seed_n5d(a2_amp, amp=0.02)`: structured band-limited matter deviation u + small nonzero ℓ=2 shear
a2, L=1, ρ=1/√2, φ=0 (a genuinely structured, non-collapsed state — no solve). PRM=(Z,XI,KAP,N)=(8,1,1,1).
S-Dir seal, ℓ=2 only, live source −(ρ²/4)T_s (λ=−½), no flat source.

## Results (a2_amp=1e-2 primary scan)

| Nr | square | finite | collapsed | cond_raw | **cond_equil (FIX-1)** | s_min_eq | equil near-null |
|---|---|---|---|---|---|---|---|
| 8  | ✓ | ✓ | **no** | 4.0e7 | **5.6e6** | 3.8e-7 | uf (99%) |
| 12 | ✓ | ✓ | **no** | 2.0e8 | **3.3e7** | 6.9e-8 | uf (99%) |
| 16 | ✓ | ✓ | **no** | 6.9e8 | **1.2e8** | 2.0e-8 | uf (99%) |

- **Square + finite** residual and Jacobian at every Nr; `Phi=||F||²`≈4.6–10.9 (structured, off-solution — expected).
- **Not collapsed-degenerate:** L=1 (not near 0), ρ∈[0.707,0.707] finite+positive, φ finite, a2 finite, Hseal
  finite (~5e-4) at every state.
- **FIX-1 equilibrated conditioning** (the Jc=J·diag(1/colnorm) system the LM step actually solves by
  damped lstsq/QR — NOT the normal equations J^T J, whose cond would be squared): **5.6e6 → 1.2e8** for
  Nr=8→16 — **~7 orders below the float64 usable floor (~1e15).** FIX-1 removes the L-column under-scaling
  (raw cond ~7× higher); the raw single soft mode is ~95% the **L free-boundary column** (the known
  under-scaled cell-length mode, not a physical soft mode).
- **After equilibration the residual soft direction is a matter-deviation (uf) high-radial-frequency mode**
  (~99% uf), softening slowly with Nr (s_min_eq 3.8e-7→2.0e-8) — a spectral-collocation feature, benign under
  the damped-lstsq path, but the reason to keep the pilot **BOUNDED (Nr≤16, at most 24)**.
- **The a2 (shear) block carries only ~1% of any soft mode** → the S-Dir shear operator is full-rank (no
  ill-posed shear equation; consistent with DESIGN §4 "S-Dir shear operator is full-rank/solvable").

## a2-amplitude sensitivity (Nr=16, S-Dir)
| a2_amp | cond_equil | near-null a2-content |
|---|---|---|
| 1e-3 | 1.2e10 | ~0.01% (shear decoupled) |
| 1e-2 | 1.2e8  | ~1% |
| 3e-2 | 1.4e7  | ~8% |
The shear **stiffens** the conditioning as it activates (degrading only toward the degenerate a2→0 end) —
so a pilot should start from a genuinely structured a2, not a near-zero one.

## Premise ledger (for the pilot, if authorized)
- **π₂ axisymmetric S² tile ONLY** — CANNOT bank Outcome A/B for the π₃ hopfion (open premise for Charles).
- **ℓ=2 shear only** (single P2 mode); higher-ℓ not included.
- **S-Dir seal first** (Dirichlet a2(r_s)=a2_mirror; constant-a2 mode pinned). **S-JC2 constant-a2 null
  UNRESOLVED / unchanged (no FIX-2).**
- **λ = −1/2** matter→geometry source (`−(ρ²/4)T_s`); **no flat source** (frozen sh2/npz out of the residual).
- Z=8 CHOSE; XI=KAP=1 CHOSE-units (κ/ξ sets absolute scale; ratios are the observables). N=1 DERIVED-topological.
- **NO** finite-L target/penalty/barrier/anti-collapse/fitted-scale/mass-anchor.

## Verdict (numerical readiness only — NOT a convergence guarantee, NOT a physics claim)
**READY.** The Stage-2 solver at a structured, non-collapsed state is square, finite, and its FIX-1-equilibrated
conditioning (~1e6–1e8 for Nr≤16) is manageable in float64 via the damped-lstsq LM path — **DESIGN §8's
"FIX-1-equilibrated conditioning manageable at a structured state" is satisfied.** A **bounded Stage-2 S-Dir
pilot is ALLOWED as the next SEPARATE Charles gate** (bounded Nr≤16 (≤24 hard cap), structured a2 start,
ONE foreground process, anti-hang, never background-poll). This preflight confirms READINESS, not convergence —
whether the bounded pilot converges (and whether the converged S-Dir readout is a pin or continuum LEAD) is the
pilot's job, and any converged readout is at most a SCOPED S-Dir TILE LEAD, never Outcome A/B.
