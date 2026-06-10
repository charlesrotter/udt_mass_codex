# Dimension Ladder Null Audit

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `null_test_dimension_ladder.py` (all numbers below reproduce from it).
Alters nothing existing; new files only.

## Purpose

`particle_spectrum_native_geometry.md` builds its selector case on exact
rational matches: the five pre-spectrum constants matching reciprocal
dimensions of the `H1` operator ladder (section 6), the `N=3` lock
(section 7), and a growing ledger of downstream exact identities
(sections 15, 27-28, 38, 40-43).

The legacy audit (`mass_emergence_canonical_geometry.md` §2) killed the old
`(rational)·π^k` mass formulas with a dense-family null test (a random
target was hit within 1% with probability 0.98). This audit turns the same
weapon on the new ledger, per audit #7 ("potential for different models"):
the new identities are exact rather than approximate, but they live in a
small-rational universe where exact collisions can also be cheap. The
question is not whether the identities are true (they are; they were
verified by the `native_*` scripts) but **how much independent evidential
weight they carry**.

## Method

Six tests, all exact arithmetic (`fractions`/`sympy`), no fits:

- **A. Dependence collapse + lock census.** Express the five section-6
  matches through the docs' own branch formulas (flow fixed point
  `s=(q−q²)/2`; `ΔΠ/R=q/2`; `η=(q/2)/N`) and count the genuinely
  independent constraints.
- **B. Generalized-N classification.** Re-derive each later celebrated
  identity at general `(q, N)` (using the generic `gl(N)` facts: commutator
  image = traceless sector; `BBᵀ = N·P`) and classify it as FORCED
  (holds identically), reducible to a banked lock, or contingent — and if
  contingent, find its full solution set.
- **C. Naming multiplicity.** Count distinct ladder expressions
  (deduplicated) for each headline value in an explicit grammar.
- **D. Expressibility coverage.** The chance level: what fraction of all
  small rationals is exactly ladder-expressible at the doc's own
  expression complexity?
- **E. Residual look-elsewhere.** What fraction of the achievable channel
  residual lattice (`k/36`, `k = −23..36`) is nameable by the native
  instrument set (with `2/9` excluded as circular)?
- **F. Integer fingerprint coverage** for context on 36/63/84/108/180.

## Findings

### F1. The five-fold consilience is exactly two locks

- `M3 (ΔΠ/R)` is definitionally equivalent to `M1 (q)`; `M5 (η/2)` to
  `M4 (η)`. Two of the five matches are redundancies.
- `M2 (s)` with `M1` reduces to **LOCK-FLOW**: `(N−1)/(2N²) = 1/N²`,
  unique positive solution `N=3` (integer scan 2..1000: only 3).
- `M4 (η)` with `M1` reduces to **LOCK-2F**: `C(N²,2) = 4N²`, i.e.
  `N²−1=8`, unique `N=3` (this is `native_twoform_selector_n3_lock.py`).
- **Parametrization robustness** (verifier amendment): under the
  pre-spectrum doc's own rank-one activation law the general-N branch is
  `q=(N−2)/N`, not `q=1/N`. The lock labels then shuffle (M1 becomes the
  lock, M2 its arithmetic twin; the two-form condition becomes
  `(N−2)(N²−1)=8`) but the result is invariant: **two independent locks,
  both uniquely N=3, under both natural families.**

### F2. The downstream identity ledger adds no third lock

Every celebrated post-section-6 identity classifies as follows
(general-(q,N) solution sets computed exactly):

| Identity | Doc location | Classification |
| --- | --- | --- |
| `(η/2)·N = S_C1/R` (1/36 → 1/12 pushforward) | §15 | FORCED: reduces to `q=1/3` identically in N; `BBᵀ=N·P` is generic gl(N) |
| total T8 image weight = active Λ³ fraction (2/3) | §15 | **not N=3-specific: also holds at N=2** (both sides 1/4) |
| global residual = Λ³ trace-kernel fraction (1/3) | §28 | same polynomial `N⁴−13N²+36=0` → N ∈ {2, 3} |
| local image sum − global image = repeated A3 (11−8=3) | §28 | FORCED identically for all N (generic gl(N) arithmetic), hence "overlap action = W(A3)" too |
| local residual = `S_C1/R` (1/12) | §28 | N=3-specific given q=1/3, but downstream-forced once the locks are banked |
| trace-kernel load = `q·W(T8)` (2/9) | §38 | reduces exactly to `qN=1` = the M1 identification; nothing new |
| quotient completion 1/9+2/9+6/9=1 | §40-42 | downstream of the banked locks (generalized polynomial `(N−3)(N²−1)=0`) |

The later sections are internally consistent arithmetic **unfolding** of the
two locks — valuable as structure and bookkeeping, but the accumulation of
exact identities must not be read as accumulating selector evidence.

### F3. Naming is mostly cheap — with one notable exception

Deduplicated ladder-name counts in the strict grammar (the doc's own
expression forms, coefficients ≤ 2):

```text
1/3: 7 names    1/9: 3    1/6: 5    2/3: 7    2/9: 4    1/4: 4
1/18: 2
1/36: 1 (unique)    1/12: 1 (unique)    5/12: 1 (unique)
```

- AGAINST specificity: values with several names (1/3, 1/9, 2/9, 2/3)
  cannot identify which operator space "produced" them; the chosen name is
  interpretation.
- FOR the two-form selector specifically: **1/36, 1/12, and 5/12 are each
  uniquely named in the strict grammar, and all three route through
  `Λ²End(H1)=36`** (1/36, 3/36, 15/36). The `η/2 ↔ Λ²End(H1)` naming is
  the most specific naming in the whole ledger — consistent with the doc's
  choice of `Λ²End(H1)` as the first selector candidate.

### F4. Chance level for the locks: of order one in 37

Coverage of the strict grammar over all reduced rationals with
denominator ≤ 36: **65/395 ≈ 0.16** (generous grammar: 0.23; unit
fractions 1/2..1/120: 0.22/0.29). Naive chance that two independent
constants both land exactly expressible: **≈ 0.03 (one in ~37)**.
Suggestive, not decisive. (Treating the five matches as independent would
have given ~1×10⁻⁴ — TEST A shows that treatment is not available.)

### F5. Channel-residual matches are individually cheap

Of the 60 achievable residual lattice values, 19 (0.32) are nameable as
`0/±instrument` and 35 (0.58) with products/complements. The four actual
residuals/loads: three are level-1 instruments (−q/2, balanced, η/2), one
needs a level-2 product (2/9 = q·W(T8)). Naive joint chance ≈ 0.02 —
same order as the lock chance level, and a **ceiling**: the uniform
lattice measure is generous to the doc (plausible nulls concentrate
residuals at small |k|, where instrument density is highest). The residual
sum 1/12 is itself forced (36 − 3·11 = 3) and carries no evidence. The
typed boundary-role assignments (§36) are a real extra constraint beyond
value-matching, but qualitative — they need the functional derivation, not
more value identities.

### F6. Integer fingerprints carry only a couple of bits

22% of 1..200 (34% of 1..100) are trivially ladder-expressible.
36/84/108/180 expressible; **63 = 9×7 is NOT** (7 is a filter grade, not a
constructed dimension) — independently confirming the spectrum doc's own
"63 remains weaker" verdict.

## Verdicts

1. **The dimension-ladder selector is NOT the legacy dense-π-fit failure
   mode.** The matches are exact, N=3-locked under two independent
   conditions robust to parametrization choice, and not tuned to data.
   The audit found no fitted parameter and no circular target anywhere in
   the ledger.
2. **But its evidential weight is two locks at chance level ~1/37, not a
   growing body of confirmations.** Every downstream exact identity is
   forced, reducible to a banked lock, or (the §15/§28 "2/3 and 1/3
   fractions" bridge) not even N=3-specific — it also holds at N=2. Future
   sessions should not bank new value identities as selector evidence.
3. **The most specific single naming in the ledger is η/2 ↔ Λ²End(H1)**
   (unique strict-grammar name, together with 1/12 and 5/12 through the
   same 36). This is the right object to spend the functional-derivation
   effort on — exactly the gate the spectrum doc already names
   ("derive that the C1 action acts on Λ²End(H1)").
4. **Recommended discipline going forward:** before celebrating a new
   exact rational identity, run it through the TEST B classifier
   (generalize to (q, N), solve); only identities that produce a NEW
   independent lock condition — or a functional/variational derivation —
   move the selector. The §15 normalization bridge and the §38/§40-43
   quotient identities should be cited as structure, not as evidence.

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `ab04acf527b63cd0b`,
instructed to (1) independently re-derive all math, (2) RESCUE the
five-independent-matches reading, (3) attack the locks as post-hoc, and
(4) attack the methodology. Outcome:

- All quantitative claims **CONFIRMED** by independent re-derivation
  (both lock polynomials and their N=3 uniqueness; the gl(N) forcing of
  the §15 pushforward and §28 overlap identities, including numerical
  verification of `BBᵀ=N·P` for N=2..5; the N=2 degeneracy of the §15/§28
  fraction bridge; all coverage counts).
- Rescue **FAILED**: the pre-spectrum doc itself grades `s=1/9` as
  "postulate or circular backsolve" (no independent third lock), and the
  collapse is arithmetic — any reading reshuffles which match is the lock
  but never raises the count above two.
- Post-hoc attack **PARTIALLY SUCCEEDED**: section 7's general-N family
  was chosen after N=3 was known, and differs from the pre-spectrum doc's
  own `q=(N−2)/N` law. Neutralized by verifying both families give the
  same two unique-N=3 locks; amendment recorded in TEST A.
- Methodology: atom set judged fair-to-conservative; exclusion of 2/9
  from instruments correct; uniform residual lattice generous to the doc
  (amendment recorded in TEST E); B4 relabeled "downstream of banked
  locks" (amendment recorded in TEST B).
- Overall: **audit verdict STANDS with the three amendments**, all of
  which are incorporated in the committed script.

## Relation to existing docs

This audit does not downgrade anything in
`particle_spectrum_native_geometry.md` — that doc's own grades
("CANDIDATE, not yet DERIVED"; "dimension ladder: strong; functional
selector: open") are consistent with these findings. What this audit adds
is the quantitative calibration of "strong": two locks, chance level
~1/37, downstream identities forced. It sharpens the doc's existing
priority: the selector upgrades only through the functional gate, and the
uniquely-named `Λ²End(H1)` family is where that effort should go.
