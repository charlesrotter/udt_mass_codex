# N5d Stage-2 Class-B SEAL DIAGNOSTIC — results (π₂ static S-Dir; DESIGN/PROVISIONAL/Outcome D)

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M) · code `cell_solver_f2d.py` (Class-B option) +
`n5d_stage2_classB_diagnostic.py`. **Bounded diagnostic — NO production pilot, NO physics verdict, NO Outcome A/B, NO
pin/continuum, NO π₃, NO S-JC2/FIX-2/higher-ℓ/time-live, NO finite-L target/anchor/mass-data/z_CMB, NO absolute-L
selection.** Status: **DESIGN / PROVISIONAL / Outcome D.** π₂ static S-Dir tile ONLY.

## 1. Files changed / 2. Exact Class-B row change
- **`cell_solver_f2d.py`** `residual()`: added `seal_phi` option to the n5d dict. **Class A (default, unchanged):**
  outer φ row `φ'(r_s)=0` (mirror). **Class B (`seal_phi="B"`):** the OUTER (seal) φ row is swapped
  `φ'(r_s)=0 → φ(r_s)=0` (Dirichlet, φ' FREE); the core row `φ'(r_c)=0` is unchanged. Row count unchanged (square).
  Class A is byte-identical when `seal_phi` is absent/"A" (**pytest 67/1xfail unchanged**). Live source (λ=−½,
  `Tshear=−(ρ²/4)T_s`), S-Dir shear seal, and the Hseal form are all unchanged.
- **`n5d_stage2_classB_diagnostic.py`** (new): the bounded diagnostic below.

## 3. DOF recount — Class B REMOVES the φ-offset gauge (clean positive)
The Dirichlet φ(r_s)=0 pins the φ depth-offset, so the hard φ-offset gauge of Class A is gone. Drop-Hseal Jacobian at
the seed (equilibrated):
| | cond_eq | s_min | s_2nd | near-null |
|---|---|---|---|---|
| Class A | 4.76e9 | **4.8e-10** | 2.29e-4 | 82% φ, 18% ρ (a hard, well-separated gauge) |
| Class B | **1.47e4** | **1.55e-4** | 2.29e-4 | (s_min ≈ s_2nd — NO well-separated null) |
⇒ Class B improves conditioning by ~5 orders and the hard φ-offset null vanishes. The 2-pin gauge-fix is no longer
needed — the Dirichlet seal does the φ-pin physically; only a mild ρ-normalization mode remains.

## 4. Fixed-L Class-B diagnostic table (keep-Hseal, several L; NO L selection attempted)
| L | Phi | Hseal | φ'(r_s) | q_raw | M=−q | 2M/ρ_s | cond_eq |
|---|---|---|---|---|---|---|---|
| 2.0 | 6.0e-5 | −4e-5 | +6.8e-3 | +295 | −295 | −8.0 | 1.8e12 (ρ_s blew up ~73 — degenerate) |
| 1.0 | **0.124** | −0.135 | +0.117 | +0.51 | −0.51 | −1.38 | 1.2e4 |
| 0.5 | 0.048 | −0.063 | +0.025 | +0.10 | −0.10 | −0.28 | 7.3e4 |
| 0.25 | 0.015 | −0.021 | +4e-3 | +0.016 | −0.016 | −0.046 | 5.4e5 |

**Key structural finding — the flip:** at L=1 the conditioning is GOOD (1.2e4) yet **Phi=0.124 is bounded away from 0
(Hseal=−0.135 ≠ 0)** — the fixed-L Class-B system is genuinely **OVER-DETERMINED**. Removing the φ-offset gauge means
**Hseal=0 is no longer gauge-satisfiable** — it becomes a REAL constraint. (This is the exact flip side of Class A,
which was UNDER-determined: Hseal was gauge-slideable to 0 at any L, leaving L unselected.) So in Class B, H=0 should
SELECT L with L free.

## 5. q_raw / M_readout sign report
`q_raw = Z ρ_s² φ'(r_s)` is now a live output (φ' free). At the fixed-L states q_raw>0, `M_readout=−q_raw<0`
(canonical M=−q). **BUT the fixed-L solves do NOT converge (Phi=0.01–0.12, Hseal≠0), and q_raw sits at the residual
floor** (L=1: q_raw=0.51 vs √Phi=0.35 → only ~1.4×). **⇒ the nonzero q_raw is NOT clearly genuine — it tracks the
non-convergence residual** (the same artifact class flagged twice this session). Class-A comparison at L=1:
q_raw=1.9e-6 ≈ 0 (mirror, as expected).

## 6. Is the Class-B charged static tile internally consistent?
- **Square + finite:** YES (free-L 133×133).
- **Fixed-L: OVER-DETERMINED** (Hseal=0 a real constraint, Phi bounded away from 0 at good conditioning) — does NOT
  close at fixed L.
- **Free-L (square 133×133, no pin): STALLS** — from seeds L∈{0.3…2.0} the LM makes no progress on L (L stays at the
  seed, Phi=0.1–0.4, Hseal not →0). **Tool-limited / does not close in the bounded solve.**
- **Verdict: the isolated static Class-B tile does NOT cleanly close in bounded solves.** Whether this is (i)
  ill-posed because the net seal flux has no ambient RECEIVER (flux conservation — an isolated charged cell), or (ii)
  merely tool-limited (LM conditioning on the free-L system), is **UNRESOLVED** here. The fixed-L over-determination
  at GOOD conditioning (cond 1.2e4) leans toward a STRUCTURAL need for L-freedom + an exterior, not pure conditioning.

## 7. Does an exterior / mirror-fold receiver appear required?
**LIKELY YES** (consistent with the prior L-selection audit): a nonzero seal charge q needs somewhere for the flux to
go (Gauss). An isolated Class-B cell has no receiver ⇒ the over-determination/stall is the expected symptom. The
native fix is the embedded/exterior match (JC1 `[√h Z_φ φ']=0`, B4 `H_cell=H_amb`) — which the static-A0 route is
tool-limited on (depth-stiffness wall). **Not proven here (tool-limited), but the evidence points to embedding.**

## 8. Are mass ratios a plausible next deliverable?
**NOT from the isolated Class-B tile as-is** — it doesn't cleanly close and q_raw is non-genuine at the stalled
states. Mass ratios `M_i/M_j=q_i/q_j` would need EITHER a converged isolated Class-B closed cell (tool-limited /
possibly ill-posed) OR the embedded/exterior treatment (walled on the static-A0 slice). So mass ratios remain gated
behind either a solver advance on Class-B or the embedding fork.

## 9. Remaining blocker
The isolated static Class-B tile does not close (fixed-L over-determined; free-L stalled). Blocker = **the missing
exterior/receiver for the seal flux (embedding)** — likely structural (fixed-L over-determination at good
conditioning), though the free-L stall is partly tool-limited. This is the SAME boundary the L-selection audit
reached: nonzero charge and L-selection both live in the EMBEDDING sector, and the static-A0 embedded route is
tool-limited (depth-stiffness wall, CONDITIONS-CHANGED under ω≠0).

## 10. Scope warning
π₂ axisymmetric static S-Dir tile only. NO Outcome A/B, NO pin/continuum, NO π₃ verdict, NO physics verdict, NO
absolute-L selection. DESIGN / PROVISIONAL / Outcome D.

## Net (not a physics verdict)
Class B is well-formed and does its DOF job — it removes the φ-offset gauge and turns Hseal=0 from a gauge-slideable
condition into a REAL closure (the correct behavior for a charged cell). But the ISOLATED Class-B tile does not close
in bounded solves (fixed-L over-determined; free-L stalled), q_raw is not genuine at the stalled states, and no
absolute L is selected — pointing (as the prior audit predicted) to the need for an exterior/embedding to receive the
seal flux. The Class-B code path is banked as a diagnostic branch; the embedding remains the gated frontier.
