# Branch-P native-S² coupled OBSERVE — BOUNDED PARTIAL (throughput-limited, INCONCLUSIVE)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** BOUNDED PARTIAL — NOT a verdict.
Mode: OBSERVE, DATA-BLIND. Files: `branchGP_native_s2_coupled_OBSERVE.py` (the coupled residual + LM
driver). Fields saved (inconclusive) to /tmp/branch[GP]_native_s2.npz.

## What was built (Step B of the Branch-P push)
A STATIC coupled residual `branchGP_native_s2_coupled_OBSERVE.py` — 6 LIVE nodal fields (no frozen
DOF): metric warps a,b,c,d + the depth field φ (INDEPENDENT player) + **gtw, the native S² radial
twist (the very DOF the rigid n=x/r slice FROZE — now LIVE)**. Matter = the genuinely native S²
3-vector n=(sinθ cos(mψ+gtw), sinθ sin(mψ+gtw), cosθ), |n|=1 exact (free_s2_matter machinery, NOT the
S³ 4-vector). Gravity = `branch_operator.E_mixed_branch` (Branch G/P switch). gtw FREE at both ends
(no BC = no import). Constraint-respecting (all fields coupled). Solver = jacrev dense-LM (full3d_newton
vmap-safe inv/det).

## What ran (Step C) — and the honest result
Bounded GPU solves (V100, float64), Nr=12/Nth=8/Nps=8, cell=8, single process sequential, ~260s cap.
**Both throughput-limited at 3 LM iterations (~113s/iter for the dense jacrev Jacobian, ~3900 rows):**

| | Branch G (control) | Branch P (test) |
|---|---|---|
| Phi final | 37.5 (≈floored) | 14,580 (FAR from floored) |
| M_MS | 1.6207 | 1.6216 |
| rho(r) | ~1/r² (peak/edge 25.2) | ~1/r² (peak/edge 25.5) |
| twist gtw | ~1e-14 (inactive) | ~1e-14 (inactive) |
| φ depth span | 4.3e-4 | **2.1e-3 (~5× deeper)** |

- **Branch G CONTROL VALIDATED:** reproduces the scale-free DEFECT (rho ~ 1/r² = proper-rho flat
  across the whole cell; M_MS spread; twist inactive). The pipeline is sound.
- **Branch P: the ONLY reliable signal is φ pulled ~5× deeper** — the U(φ) potential (scale-breaker)
  IS acting, as predicted. Everything else (rho, M_MS, localization) is SEED-DOMINATED and
  indistinguishable from G *because P did not converge* (Phi=1.5e4, 3 orders from floored).
- **INCONCLUSIVE on the real question (does Branch P localize / select a native scale).** Reading "P
  is also a defect" from this would be narrating false convergence — NOT done.

## Diagnosis (SOLVER-FIRST, not physics)
The wall is **solver throughput**, not the metric: (1) the dense jacrev Jacobian is ~113s/iter at this
grid; (2) **Branch P is STIFFER** — its U potential makes LM descend far slower (G dropped 6000× in 3
iters; P only 16×). This is the KNOWN coupled-solve conditioning wall (SOLVER_COMPLETENESS_MAP "off-round
COUPLED solve does NOT converge at production grid (#60); needs research-grade preconditioned/Newton-
Krylov upgrade"). The localization verdict must wait for a FLOORED Branch-P solve.

## NEXT (Charles decision 2026-06-23 = option 2: build the proper solver)
Build the research-grade **JFNK (Jacobian-Free Newton-Krylov) / preconditioned** coupled solver
(COMPLETION-flagged; prior JFNK exists — `p5a_prime_jfnk_fast.py`). Wire it to the branchGP residual_vec.
It unblocks ALL downstream coupled solves: Branch-P static (floor it → localized body vs defect?), the
SEAL-INDEPENDENCE gate (native scale vs imported seal), off-round, and the time-live native S² build.
Then re-run Step C floored. Gate (Charles): observe for emergence; if none after sufficient development,
import under Postulate A.
