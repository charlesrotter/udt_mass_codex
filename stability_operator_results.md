# Stability filter stage 1: the constrained second-variation operator — DERIVED + BLIND-VERIFIED (convention pinned by theorem)

**Date:** 2026-07-03. **Pre-registration:** `stability_filter_miniMAP.md` (Charles's three pins).
**Derivation agent:** `a539d9bf24e756fd8` (CAS C1–C15; no STOP-fork; scripts `cascade_sf_*.py`).
**Blind adversarial verifier:** agent `a4f02d46f973babb7` (own moving-endpoint machinery validated
on an off-shell toy; own discretization; 2/12 shots; scripts `cascade_bv13_*.py`; a first attempt
`a6d46d759e5c31824` TIMED OUT on unchunked CAS — process lesson banked: chunk symbolic jobs,
~2-min caps, checkpoint, honest-partials priority order). **Verdict: operator core CONFIRMED with
exact coefficients; ONE ±1 convention inconsistency caught and resolved by theorem (below).**

## The operator (verified)

Second variation with moving folds, about a rung of L = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2 − U(ρ):
- **PIN 2 CONFIRMED:** all endpoint quadratic self-terms (α², β², αβ, second-order shifts and
  boundary fields) CANCEL exactly, class by class — the a″/b″ cancellation coefficient is
  exactly **−H(fold)**: the cancellation IS the transversality closure (U(ρ_c)=2 load-bearing in
  a third role). φ''(fold)=0 is DERIVED from the EOM (not assumed). Survivors: the essential
  odd-fold constraint u(r_s) + φ'_s β = 0 and exactly two boundary bilinears —
  L_ρ(r_s)·β·v(r_s) with L_ρ(r_s) = −4ρ''(r_s) (EOM-exact) and U'(ρ_c)·α·v(0).
- Constraint content = the two linearized transversality scalars as natural BCs:
  δH(r_s) = q·u'(r_s) + (Zρ_sφ'_s²+U'(ρ_s))v(r_s) = 0; inner pairing δH(r_c) = U'(ρ_c)v(0).
  No pointwise constraint, no einbein, no reparametrization gauge.
- Columns: FREE (P1-primary, δφ_c free), ANCHORED (u(0)=0 ⟺ δ(Δφ)=0 — equivalence verified),
  FIXED diagnostic. Exact bulk form and per-column BCs in the derivation report.

## The counting (the scar's payoff)

- **The raw Morse index of every rung is INFINITE** (kinetic block diag((Z/2)ρ², −2e^{−2φ}),
  no cross-kinetic; discretized n_neg ≈ M, verified on two schemes). No finite raw count exists;
  any per-rung "index" quoted without the labeled decomposition is meaningless.
- **Honest counting = two exact inertia identities** (both verified as matrix theorems AND
  numerically exact at every grid): (1) hyperbolic pair — n_neg(Q_ext) = 1 + n_neg(Q̂) (valid iff
  U'(ρ_c) ≠ 0; the +1 = the labeled "fold-pair"; U'(ρ_c) = 2(m−2a*): +0.0746 (N=0), +0.0285
  (N=5) — soft near a = m/2, pre-named); (2) Haynsworth — n_neg(Q̂) = n_neg(V̂) + n_neg(S_u).
- **CONVENTION PINNED BY THEOREM (bv13's catch):** the hyperbolic-pair congruence CONSUMES v(0),
  so V̂ and S_u are defined on the v(0)=0 subspace — **the v₀=0 convention is forced, not
  chosen**. The stage-1 report's quoted pairs mixed conventions (±1/slot); corrected converged
  values in the pinned convention: **N=0 → (n_neg(S_u), n_pos(V̂)) = (0, 0); N=5 → (2, 6)**
  (grid-stable M=800→51200 on the verifier's scheme). Split-independent invariants
  (n_neg(Q_ext) = 1 + n_neg(V̂) + n_neg(S_u); full-column signatures) hold in any convention.
- Definite-reduction criterion: a single "index" exists iff n_pos(V̂)=0 — TRUE at N=0 in the
  pinned convention, FALSE at N=5 (residual indefiniteness = reported structure, per the MAP).
- Method limit realized as pre-stated: conjugate-point/Morse void (Legendre fails); replaced by
  the exact identities + grid-doubling of the invariant pair.
- Orientation flag: counts are for the ACTION S; energy = −S reading swaps n_neg ↔ n_pos.

## Zero/soft inventory (PIN 3 resolved; verified)
- ONE exact zero in FREE and ANCHORED: the translation (−φ', −ρ', α=1, β=1) — the r_c=0 gauge;
  deflate before counting. Excluded in FIXED. (O(h²)-clean on both schemes.)
- Fixed-U homothety is NOT soft: Jacobi residual J_ρ = −(e^{2φ}/4)(ρU''+U') — specific to the
  r-rescaled direction (pure ρ-scaling gives the opposite U' sign; sharpening banked).
- The shooting-family direction is NOT a zero — excluded by the **v(r_s)-natural BC** (residual
  ~3% of scale), NOT by δH (which it satisfies automatically). **HAZARD BANKED: any zero-mode
  test keyed only to δH(r_s) falsely passes this direction.**
- Near-cap almost-zeros must beat: the deflated translation + the fold-pair softness
  (U'(ρ_c) → 0 at a = m/2, where the hyperbolic step degenerates — validity edge, flagged).

## Stage-2 protocol (per the MAP; ready)
Per rung, all three columns, PINNED v₀=0 convention only: (n_neg(S_u), n_pos(V̂)) + labeled
parts + lowest eigenvalues + near-cap soft-mode data; M ≥ 800 with doubling of the invariant
pair (derivation flag: M=400 under-resolved at N≥5; count via full form + identities — S_u
eigenvalue MAGNITUDES pass through near-singular V̂ and are not converged even where counts
are); identities checked per rung; NO stability language in-run; the definition of "stable"
(which component, S-vs-energy orientation) is set at the PONDER with Charles.
