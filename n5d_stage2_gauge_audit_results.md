# N5d Stage-2 φ/ρ SOFT-MODE GAUGE AUDIT — results (π₂ static S-Dir; DESIGN/PROVISIONAL/Outcome D; blind-verified)

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M) · script `n5d_stage2_gauge_audit.py` (+ an inline
2-pin/L-modulus probe). **Category-A conditioning/formulation diagnostic — NO physics fork, NO S-JC2/FIX-2/higher-ℓ/
time-live, NO finite-L target/penalty/anchor.** Status: **DESIGN / PROVISIONAL / Outcome D.** π₂ static S-Dir tile
ONLY. **NO Outcome A/B, NO pin/continuum, NO π₃ claim, NO physics verdict.**

## Purpose
Decide whether the blind-verified fixed-L φ/ρ near-null mode (the collapse's soft direction) is a GAUGE / free-
boundary redundancy (⇒ quotient it, category-A, no physics change) or a physical flat direction, and find an
admissible category-A pin that removes it without adding physics or selecting L by hand.

## 1. Mode diagnosis — a global ρ-rescale + φ-offset GAUGE (blind-CONFIRMED)
Fixed-L (L=1) drop-Hseal Jacobian smallest-singular-value right vector (state space): block fractions **~81% ρ, ~19% φ,
~0% uf, ~0% a2**, and
- **cos(v_ρ, ρ) = +1.000** ⇒ the ρ-part is a **global ρ-rescale** (ρ→(1+ε)ρ);
- **cos(v_φ, 1) = +1.000** ⇒ the φ-part is a **constant φ-offset** (φ→φ+εc); locked together (cos(v_φ,v_ρ)=+1);
- cos(v_ρ, ρ′)=0, cos(v_φ, φ′)=0 ⇒ NOT a radial reparameterization.

**Invariants along the mode** (u→u+εv): ρ_s/ρ_c = 1.00000 (shape invariant), matter moments Ith/Is/I4th invariant
(uf frozen), ‖F_field‖ invariant (stays on the field manifold), **Hseal MOVES** (~2.5e-3 over the range), q_raw ~0
and invariant. ⇒ Hseal is **gauge-dependent** along this mode; the direction is an unphysical redundancy.

## 2. 2-pin gauge-fix — removes the gauge, physics unchanged (blind-CONFIRMED, with a conditioning caveat)
At a Hseal=0 state (keep-Hseal solve, Phi~2e-10), adding TWO category-A gauge conditions — **fix ρ(r_c) and fix φ(r_c)**
(an areal-radius normalization + the φ depth-offset already implied by the boundary convention) — removes the near-null
mode: equilibrated **cond 3.4e8 → 7.6e7**, s_min 6.7e-9 → 3.0e-8 (~4.5×), and **q_raw unchanged to Δ~1e-13**. So the
gauge is category-A removable with no physics change. **Caveat (blind verifier):** "well-conditioned" is generous —
cond is still ~8e7 with a soft near-null (~3e-8) remaining; the pins IMPROVE conditioning and remove the gauge, they
do not make it crisp. **A well-conditioned gauge-fixed representative closed cell at FIXED L: YES** (Phi~1e-10,
Hseal~0, cond~8e7, workable).

## 3. L is an UNDETERMINED flat direction — unique closure OPEN (blind-CONFIRMED conclusion)
Even after the 2-pin gauge-fix, the static S-Dir H(r_s)=0 closure does **not** pin the cell length L: a free-L solve
(L a genuine unknown, 2 pins on) **runs L away** (to ~1e3, 1e6, even negative L over 5 starts) while keeping
Hseal~1e-9 and Phi~1e-8. So **L is unpinned by this closure; a unique finite-L closed cell is OPEN** — the static
S-Dir tile is underdetermined by one condition on L.

## 4. CORRECTION (blind-caught) — the "q_raw ∝ L ⇒ L is a physical modulus" claim is RETRACTED
My follow-up probe read a monotonic q_raw-vs-L trend (9e-6→3.5e-8 across L∈[2,0.25]) as "physically-distinct L-cells."
**The blind verifier (agent `a2969cef559b1ac72`) refuted this evidence:** `q_raw = Z·ρ_s²·φ'(r_s)` and **φ'(r_s)=0 is
an imposed mirror BC at BOTH ends**, so **q_raw ≡ 0 on-shell for every closed Class-A mirror cell** in this tile. The
apparent q_raw-vs-L growth was the **convergence residual** (larger L = stiffer = looser φ'(r_s) BC), not a physical
charge — in the free-L solve q_raw is ~1e-7 noise uncorrelated with L. **⇒ q_raw does NOT distinguish the L-family;
whether L indexes physically-distinct cells or is a residual scaling freedom is ITSELF OPEN.** (This is my SECOND
residual-artifact-as-physics over-read this session — the −0.96 valley was the first; the neutrally-framed verifier
caught this one before it was banked.)

Structural note (observation, not a fork): because both ends are mirror seals (φ'=0), the **seal flux q_raw and the
M_readout are structurally ZERO for every Class-A mirror cell** in this static S-Dir tile.

## 5. Blind adversarial verification — verdict
Agent `a2969cef559b1ac72` (2026-07-06; own harness; forbidden `n5d_stage2_gauge_audit.py`/reconcile/audit docs/
`tests/`; framed neutrally to adjudicate gauge-vs-modulus): **Claim 1 (ρ-rescale+φ-offset gauge) CONFIRMED; Claim 2
(2-pin gauge-fix) CONFIRMED (cond ~8e7 caveat); Claim 3 (L a physical modulus) PARTIAL — the conclusion "no unique L,
closure OPEN" CONFIRMED, but the q_raw evidence REFUTED (q_raw≡0 for mirror cells).** Synthesis: the degeneracy is a
**MIX — a removable ρ/φ GAUGE + an undetermined L flat direction** that H=0 does not pin.

## 6. Classification + answers to the required items
- **Soft-mode transformation:** global ρ-rescale + locked φ-offset (a gauge); NOT a reparameterization.
- **Invariants along the gauge:** ρ-shape, matter moments, ‖F_field‖, q_raw all invariant; only Hseal moves ⇒ Hseal
  is gauge-dependent.
- **Admissible category-A pins:** fix ρ(r_c) (areal-radius normalization) + fix φ(r_c) (φ depth-offset) — these remove
  the gauge and leave q_raw invariant. INADMISSIBLE (correctly rejected): fixing L to a target, using observed masses,
  changing λ or source strength, barriers, added physics. (A null-orthogonal pin to the gauge vector is admissible in
  principle but must NOT be aligned with the closure direction — naively it freezes the Hseal=0 approach.)
- **Best category-A formulation fix:** the 2-pin gauge-fix [ρ(r_c), φ(r_c)] on the keep-Hseal (Hseal-in-objective)
  system. It removes the gauge and yields a workable (cond~8e7) closed cell at a chosen L.
- **Well-conditioned gauge-fixed representative at fixed L:** YES (workable, cond~8e7 — not pristine).
- **Unique physical closure:** NO / OPEN. The gauge is removable; the L flat direction is NOT category-A removable
  without either fixing L (inadmissible) or adding a physical L-selection condition (a fork). Whether L is a physical
  modulus vs a scaling redundancy is undetermined (q_raw≡0 can't tell). **This is exactly the category-A/physics
  boundary:** the numerical/gauge ambiguity is now removed; what remains (what selects L) is a genuine physics question.
- **Exact blocker (item 10):** a MIX of (i) a removable ρ/φ GAUGE (resolved) and (ii) an undetermined L flat direction
  = a MISSING CLOSURE CONDITION on the cell size L (physical selection absent) — NOT gauge-unresolved, NOT a numerical
  precision limit, NOT structural incompleteness of the code.

## 7. Not a physics verdict
This is a category-A gauge/conditioning diagnostic. It removes the φ/ρ gauge ambiguity and localizes the remaining
open question to L-selection. It makes **no** physics claim: no Outcome A/B, no pin, no continuum, no π₃ verdict.

## 8. Scope warning
π₂ axisymmetric static S-Dir tile only (Nr=12, Nth=8, ℓ=2 shear, λ=−½ live source, Z=8/ξ=κ=1/N=1). Cannot bank
Outcome A/B for the π₃ hopfion. DESIGN / PROVISIONAL / Outcome D.
