# N5d Stage-2 S-Dir PILOT — results: L-COLLAPSE (tool-limited / Outcome D; π₂ tile; blind-verified)

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M) · scripts `n5d_stage2_sdir_pilot.py`
(+ JSON `n5d_stage2_sdir_pilot.json`). **Charles-gated bounded pilot.** Status: **DESIGN / PROVISIONAL /
Outcome D.** π₂ axisymmetric S² tile ONLY. **NO Outcome A/B, NO pin/continuum, NO π₃ claim, NO physics verdict.**

## Setup
`main` @ `d3a50a0` (Stage-2b impl `6a0ac15` + preflight). Tests: **67 passed / 1 xfailed.** S-Dir seal only,
ℓ=2 shear only, λ=−½ live source (`−(ρ²/4)T_s`), FIX-1 equilibration on. Bounded: Nr∈{12,16}, Nth=8, CPU,
ONE foreground process, hard caps (maxit=30/chunk, time_budget≤80s), no background-poll. PRM=(Z,XI,KAP,N)=(8,1,1,1).
Structured seed: amp=0.02 matter, a2_amp∈{1e-2 primary, 3e-2 check}. **NO** finite-L target/penalty/barrier/
anti-collapse/fitted-scale/mass-anchor (forbidden; none added).

## Required outputs

**1–2. Residual history + convergence status.** All bounded runs (Nr=12 a2=1e-2/3e-2, Nr=16 a2=1e-2) descend
monotonically Phi 7.7–10.9 → ~1.1e-2 in 30 iters — **not converged** (Phi≫tol; still descending). Extending the
cap (Nr=12, a2=1e-2, to 150 iters) reveals the true behavior — **L-COLLAPSE**:

| ~iters | L | Phi=‖F‖² | Hseal | cond_equil |
|---|---|---|---|---|
| 0 (seed) | 1.00000 | 7.72e0 | +5.16e-4 | 3.3e7 |
| 30 | 0.14342 | 1.19e-2 | −1.11e-2 | 1.8e9 |
| 60 | 0.03745 | 7.22e-4 | −6.63e-3 | 1.3e12 |
| 90 | 0.01743 | 1.93e-4 | −6.35e-3 | 6.1e13 |
| 120 | 0.01083 | 9.86e-5 | −6.31e-3 | 6.7e14 |
| 150 | 0.00758 | 6.82e-5 | −6.29e-3 | 2.7e15 |

**Convergence status = TOOL-LIMITED / COLLAPSE.** L marches monotonically toward 0; Phi keeps shrinking only
because draining L trivially satisfies the 1/L, 1/L² field-equation rows; **Hseal (seal closure H(r_s)=0) floors
at ≈−6.3e-3 and never reaches 0**; cond_equil runs to the float64 floor (~1e15). The "L≈0.14 consistency" seen
at the maxit=30 cap was a **cap artifact** (identical iteration count → identical L), NOT a settled length.

**3. Final fields** (at the maxit=30 primary, before the collapse is obvious): L=0.1434, ρ=[0.709,0.711,0.709]
(finite, ~stable), φ=[−0.0026,−0.0026] (finite, flat), a2=[2.41e-4…2.47e-4] (finite). Under extension L→0.0076,
ρ_c/φ_c/a2 frozen while L drains.

**4. Readouts** (existing sign convention, M=−q): q_raw=+1.84e-4, Π_φ=+1.47e-3, M_readout=−1.84e-4 (Nr=12,it30).
These ride the collapsing state — **not physical outputs of a closed cell** (no cell closed).

**5. Jacobian condition before/after.** Before (structured seed): cond_raw=2.05e8, cond_equil=3.3e7. After
(collapsing): cond_equil 1.8e9 (it30) → 2.7e15 (it150). Conditioning degrades as L→0.

**6. Near-null mode.** After the solve the softest direction is ~99–100% the **φ block** (equil s_min→~1e-9),
the soft-φ/L-drain manifold; the a2 (shear) block carries ~0% — the shear equation stays well-posed.

**7. Collapse check.** At the bounded maxit=30 state `collapsed=False` (L=0.14>1e-3, ρ/φ/a2/Hseal finite). Under
extension L→0 (0.0076 at it150; the L0=2.0 seed even crosses to **negative L**) — i.e. the closure is
**collapse-leaning → collapsing**, with all fields finite but L draining.

**8. H consistency + residual row budget.** H-drift(max−min) small (~1e-4) — H is conserved along r (the code is
correct); but **Hseal is stuck away from 0** (~−6e-3), so the cell does not close. Row budget (Nr=12, it30) — the
residual is dominated by the **base mirror BCs + Hseal**, the shear sector is machine-satisfied:
`fr_mirror` 7.4e-2 · `rho_mirror` 6.9e-2 · `Hseal` 1.1e-2 · `rho_ode_int` 3.8e-2 · `f_pde_int` 6.5e-3 ·
`shear_ode` 1.6e-5 · `shear_core_bc` 1.3e-5 · `shear_seal_bc` 2.5e-4 · `phi_ode` 3.6e-4.

## Blind adversarial verification — CONFIRMED
Independent zero-context verifier (agent `ae5e8adcc16071d11`, 2026-07-06), forbidden from the pilot scripts/results
and `tests/`, own harness, adversarially tasked to REFUTE by finding a finite-L closed cell:
- **Finite-L root hunt** over seed-L∈{0.05,0.1,0.3,0.5,1.0,2.0}: **every** seed drains to L≈0.008 with
  |Hseal|~6e-3≠0; **NO finite-L closed cell found** (closed-cell test Phi<1e-6 ∧ |Hseal|<1e-4 ∧ L>0.01 fails for all).
- The small-L limit is a **spurious/degenerate root** (Phi floored, dominated by Hseal + mirror rows; field rows
  ~1e-10–1e-16 satisfied only via the L→0 drain). Hseal stays ~−6e-3 as L→0.
- **Not a FIX-1 artifact** (equilibrate True vs False agree: L→0 both) and **not grid-specific** (Nr=12 vs 16 agree).
- The collapse lives in the **base geometry+matter closure, not the shear sector** (seed base rows ~40× the shear rows).
- **VERDICT: CLAIM CONFIRMED — L-collapse is real; no finite-L closed cell exists in this regime; TOOL-LIMITED/Outcome D.**

## 9. Classification
**COLLAPSE BEHAVIOR / solver-tool-limited (Outcome D).** The bounded static S-Dir co-relaxed π₂ solve has no
finite-L closed cell — L collapses toward 0, the seal-closure Hseal never reaches 0, and the only root the LM
approaches is the degenerate L→0 pass-through. NOT a successful S-Dir tile lead; NOT a conditioning failure (the
solver is progressing correctly — it is the residual system that has no finite-L closure here); NOT unresolved in
the "did the tool run" sense (it ran clean, fast, blind-verified). It is a genuine, blind-verified **scoped
collapse/Outcome-D observation**.

**MISMATCH → SOLVER, not mechanism (what is LEFT OUT — parked for Charles, none added here):** the collapse
indicts the SOLVER/CLOSURE SETUP of THIS corner, never the metric and never a mechanism. Candidates for what the
static S-Dir block-diagonal ℓ=2 π₂ tile omits: (a) higher-ℓ shear (ℓ=2-only); (b) the **S-JC2 seal fork** (a
different closure BC — the constant-a2 null, still unresolved, no FIX-2); (c) the **non-static / time-live sector**
(this is a STATIC solve; Charles's standing hunch + the seal=t→−t canon put dynamics in a separate sector);
(d) unfrozen off-diagonal / Branch fork. These are solver-completeness questions, NOT mechanisms to add.

## 10. Scope warning (binding)
This is the **π₂ axisymmetric S² winding tile only.** Even as a collapse observation it **CANNOT bank Outcome A/B**
for the π₃ hopfion question (π₂ defect vs 3-D Hopf linking — open premise for Charles). Scoped to: static · S-Dir ·
block-diagonal · Branch-P · ℓ=2-only · π₂ · co-relaxed λ=−½ source · Z=8/ξ=κ=1/N=1. Status: DESIGN / PROVISIONAL /
Outcome D. No pin, no continuum, no physics verdict.
