# Stability filter stage 2: the full-ladder inertia table — COMPUTED + SPOT-VERIFIED (tolerance-honest form)

**Date:** 2026-07-03. **Pre-registration:** `stability_filter_miniMAP.md`; verified operator +
pinned v₀=0 convention: `stability_operator_results.md`. **Stage-2 agent:** `a19a09f8e3b7cd106`
(30 rungs × 3 columns; 30/30 pre-declared shots; 44/44 validation gates; per-rung checkpoints;
scripts `cascade_s2_*.py`, table `cascade_s2_final_table.json`). **Blind spot-verifier:** agent
`a30f015e4aec2912e` (5 load-bearing rows, own P1-FEM assembly + banded LDLᵀ slicing, pair VALUES
withheld; 6/8 shots; scripts `cascade_bv14_*.py`). **Counts are for the ACTION S (energy = −S
swaps n_neg↔n_pos); NO stability language — the reading is reserved for the ponder.**

## The agent-agreed structure (the banked result)

**Excited rungs (N ≥ 1, below side, FREE = ANCHORED):** pair = **(2, N+1)** — n_neg(S_u)
SATURATES at 2 for every N = 1..22 (spot-verified blind at N=15: (2,16)); the entire
N-dependence lives in **n_pos(V̂) = N+1**. FIXED column: (1, N+1) — one of the two S_u
directions is fold-motion. **The pre-registered hypothesis "Morse index = N" is REFUTED in its
naive form**; the N-count migrated to the V̂-branch, +1.

**Fundamentals (below m=3, m=2 at Z=8; m=3 at Z=1): the only rungs with n_pos(V̂) = 0.** Their
S_u sector: NO solid negatives — but ONE universal ULTRA-SOFT mode (see below).

**Twin fundamental (above-side N=0): pair (2,1) — qualitatively distinct** (both agents): it
alone carries a SOLID S_u negative (−5.0e-4, scaled) beside the soft one, and one V̂ positive.
The twins at N = 8..11 are pairwise IDENTICAL to their below-partners ((2, N+1) both) — the
twin asymmetry lives only at the bottom, consistent with the banked breaking/cap structure.

## The tolerance resolution (the spot-pass catch, resolved honestly)

Stage 2 reported the fundamentals as (0,0)/(0,0)/(1,0); bv14's strict-tolerance recount gives
**(1,0) for all three**. NOT a spectrum disagreement — the two agents' eigenvalues match to 5
digits (B00 −3.84e-7, SM2 −2.80e-7, SZ1 −3.32e-8; stage-2's own almost-zero table contains
exactly these). The split is the tolerance classification of ONE mode:

**THE UNIVERSAL SOFT MODE (the substantive, agent-independent datum):** every FREE/ANCHORED
fundamental column carries one very soft, grid-stable S_u direction — sign NEGATIVE at every
grid tested (M→2M stable to 3 digits), magnitude ~10⁻⁷–10⁻⁸ (unconverged per the banked
caveat), ABSENT in FIXED (⇒ it involves fold motion β), distinct from the deflated translation
(which spans/mixes with it at finite grids — bv14 caveat). Its continuum-limit identity — a true
negative, an exact zero approached from below, or the detuning direction — is OPEN and is a
named ponder/stage-3 item. Pairs in this doc are quoted with the soft mode SEPARATED, not
absorbed: fundamentals = **(0 + 1 soft, 0)**.

**Consequences drawn:** (i) the stage-2 "Z=1 differs from Z=8" reading is WITHDRAWN — all three
fundamentals share the same soft-mode structure; the apparent split was tolerance inconsistency
across rungs (the flagged third Z-channel does NOT survive verification). (ii) The twin
fundamental's distinctness SHARPENS (its extra negative is solid, orders above the soft scale).

## Cross-checks (both agents)
Hyperbolic-pair (+1) and Haynsworth identities exact at every rung/column/grid, both signs of
U'(ρ_c); split-independent invariant exact; translation zero O(h²)-clean and its deflation
lowers n_neg(Q) by exactly 1 everywhere; raw n_neg(Q) ≈ M (no finite raw index) on three
independent schemes now. Backgrounds reproduce banked pins to 7+ digits (rows with banked data).

## Gaps (carried)
Soft-mode continuum identity (the stage-3/ponder item); eigenvalue MAGNITUDES unconverged
(counts are the deliverable); above-side rows N=8..11 banked-L cross-check at 1–2e-6
(quadrature-limited, (ρ_s,q) reproduce); A00 pins at 4–5 s.f.; angular + dynamical stability
scoped out per the MAP; the a=m/2 fold-pair validity edge approached, not hit.

## For the ponder (queued, NOT asserted)
Orientation (S vs energy) and which component carries "minimum"; what n_pos(V̂)=0-only-at-
fundamentals means; the universal soft fold-motion mode's identity; the twin fundamental's
solid negative vs the cap; whether "the universe = the (0+soft, 0) class" is the non-merit
selection this filter was built to deliver. All Charles's.
