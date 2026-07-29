# CORRECTION LAYER — P4 Route A Stage 1 (amendments A1–A4, per VERIFIER_REPORT.md)

Date: 2026-07-29. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md` §6).
The two amended items are F-A6-class universal-quantifier slips (exactly what the pass
hunts); in BOTH cases the verifier proved the forcing SURVIVES in a corrected form —
nothing here changes the outcome class, the tallies, F-RA3/F-RA4, the census
fork-typing, or the gate count/sequence.

## 1. Original claims (as they stood pre-amendment)

- **F-RA1 K₄ clause** (EXACT_DERIVATION §1 forced box; POSED §2.1 bullet 3; script
  FORCED statement + JSON; census rows 13–14): "on the registered chart every
  component's dependence on (k10, C) must factor through the exact K₄ invariants —
  bare k10- or C-linear dependence is not well defined on the quotient domain."
- **F-RA2 channel clause** (EXACT_DERIVATION §2 forced box; POSED R4 row; script
  FORCED statement + JSON): "any response whose screen sector factors through
  trace/volume/density channels has identically zero pairing with the k_mod
  direction" — i.e. EVERY trace/volume/density-built screen functional claimed
  k_mod-blind.
- **SIX_GATE_SPECS gate 2 FAIL clause**: "... or bare-k10/C-linear (non-K₄-honest)
  dependence → FAIL"; **gate 4 step 2**: "every component's (k10, C)-dependence
  factors through the exact invariants."
- **POSED §3.2 clash scan**: recorded only the trace-free-slot vs volume-only-pairing
  near-tension; the φ=0-interface vs shift-equivariance tension and the
  K₄-torsion-period vacuity were unscanned.

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifacts
preserved in `VERIFIER_INDEPENDENT_CHECK.py`, **31/31 checks, exit 0**)

- **A1 (F-RA1 component quantifier FALSE as written; §2/§6).** Exact counterexample:
  **ω = k10·dk10 = ½d(k10²)** — an EXACT, K₄-INVARIANT one-form (component and dk10
  flip together under R12/R13, so it is perfectly well defined on the quotient) whose
  R_k10 component is BARE k10-linear (`V3_ATTACK_*`). The correct forced rule:
  **character-matched RELATIVE invariance per component** — R_v must transform with
  the K₄ character of its paired direction dv; verbatim
  factor-through-the-11-invariants holds ONLY for components along K₄-invariant
  directions (δφ, base data, δλ, δk_mod, boundary data); R_k10 must be χ_a-relative,
  R_C components χ_b/χ_c-relative.
- **Positive finding recorded WITH A1 (the generation direction, PROVEN by the
  verifier).** The 11 listed generators (k10²; the six within-character-class C
  quadratics; the four mixed cubics) DO generate the full invariant ring of polynomial
  functions of (k10, C) — proven two independent ways: (a) the character/parity
  argument (invariance ⇔ e+p+q even AND e+r+s even; e≥2 ⇒ divisible by k10²; e=1 ⇒
  divisible by a mixed cubic; e=0 ⇒ product of within-class quadratics), and (b)
  exhaustive factorization of all 127 invariant monomials of degree ≤ 6
  (`V2_direction2_generation_to_degree6`, `V2_direction2_parity_structure`). This
  strengthens the record: the invariant list is a certified GENERATING set, not just a
  certified invariant list.
- **A2 (gate-spec infection; §6).** As written, gate 2's FAIL clause and gate 4 step 2
  would WRONGLY FAIL the legitimate candidate shape d(k10²). The failure condition is
  character-MISMATCHED dependence, not bare-linear dependence.
- **A3 (F-RA2 channel quantifier FALSE as written; §2/§6).** Exact counter-channel:
  **tr(X²) = 2 + 2λ² + 2k_mod²** is trace-BUILT and pairs with k_mod (∂/∂k_mod =
  4k_mod ≠ 0) (`V4_ATTACK_*`). The proven blind class: functionals of tr X (first
  trace) and of det e^{φX}. The downstream forcing SURVIVES exactly: the slot theorem
  ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0 (a screen kernel with zero trace-free part has
  identically zero k_mod-pairing), and d(tr X²)'s kernel 2K = 2λI₂ + 2k_mod·diag(−1,1)
  pairs with k_mod precisely THROUGH its trace-free slot (`V4_slot_theorem_*`,
  `V4_trX2_kernel_carries_tracefree_slot`) — so "determined branch reachable only with
  the trace-free slot (and/or mixing slots)" stands.
- **A4 (clash-scan omissions; §5).** (i) The φ=0 mirror/seal interface anchors an
  absolute φ zero-point while F-RA4/census row 6 forbid components from depending on
  one; mirror and shift do not commute (−(φ+s) ≠ −φ+s;
  `V8_clash1_mirror_breaks_shift`). Not a proven clash — boundary data are SUPPLIED
  structure and the anchor is absorbable into c_E — but the §3.2 scan omitted it.
  (ii) The gate-6/R9 period condition on K₄-orbifold cycles is VACUOUS for closed
  one-forms (2·period = period over γ² = 0; `V8_clash2_torsion_periods_vacuous`) —
  spec scope note owed.
- **Confirmation record (§1–§2).** Contract-first VERIFIED in git (PREREGISTRATION.md
  sole file of commit 940c8fe; artifacts later-stamped). Byte-identical rerun twice
  (34/34, exit 0; JSON sha256 match). Independent re-derivation with own
  constructions: F-RA1 core (96×16 stacked Kronecker commutant operator, rank 15,
  nullspace = span{I}; no invariant member), K₄ actions vs Route B T1(b) verbatim,
  F-RA2 computations (actual matrix exponential for det e^{φX}), F-RA3 (own solves),
  F-RA4 (additivity/shift/anchor + a further-forcing attempt that found none —
  near-null stamp honest). Prose hunts F-A1/F-A2/F-A3/F-A4: CLEAN; F-A6: the two
  slips above. TA4 classification audit (5 rows): correct.

## 3. Changes made (this amendment pass)

1. **`derive_routeA_stage1.py`** —
   - F-RA1 FORCED statement (script + JSON) restated as character-matched relative
     invariance, with the generation-direction citation and the counterexample on
     record; checks list extended with `A6_*`.
   - **New zero-residual checks (A1):**
     `A6_counterexample_omega_k10_dk10_invariant_component_not_verbatim` (ω is
     K₄-invariant as a one-form AND exact while its component is not
     verbatim-invariant), `A6_character_matching_rule_generic_component_set` (the
     corrected rule on a generic component set in every character class: component
     character × direction character = trivial ⟹ invariant),
     `A6_character_mismatch_breaks_invariance_contrast` (characterize-not-filter
     contrast: MISMATCH is the failure mode).
   - F-RA2 FORCED statement (script + JSON) narrowed to the proven class + the slot
     theorem; checks list extended with `B5_*`.
   - **New zero-residual checks (A3):** `B5_counter_channel_trX2_pairs_with_kmod`
     (tr(X²) = 2+2λ²+2k_mod², ∂/∂k_mod = 4k_mod ≠ 0),
     `B5_slot_theorem_pure_trace_kernel_zero_kmod_pairing` (⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0),
     `B5_trX2_kmod_pairing_routes_through_tracefree_slot` (the pairing routes exactly
     through the trace-free part; pure-trace part contributes 0).
   - JSON gains an `amendments` field; docstring notes the amendment and the
     pre-amendment 34/34 run; the `B3_volume_density_channel_blind_to_kmod` detail
     string ("every volume/density-built channel") re-worded to the A3-narrowed class
     ("every functional of the volume density det e^{phi X}") — the check's
     mathematics is unchanged.
2. **`EXACT_DERIVATION.md`** — §1: A1-amended forced box + amendment bullet
   (counterexample + characters) + the verifier's generation-direction finding
   recorded; §2: A3-amended forced box + counter-channel/slot-theorem bullet; §5 items
   2–3 re-worded to the amended conditions; §6 updated (verifier pass complete; the
   two F-A6 slips recorded); header updated to 40/40 with the amendment banner.
3. **`POSED_INVERSE_PROBLEM.md`** — §2.1 bullet 3 restated (character-matched relative
   invariance); R4 row corrected (narrowed class + slot theorem); R7(a) and J10 rows
   re-worded to character-matched; §3.2 gains the two A4 additions (mirror-vs-shift
   tension with its typed resolution; torsion-period vacuity note); header updated.
4. **`SIX_GATE_SPECS.md`** — gate 2 step 4 + FAIL clause and gate 4 step 2 corrected
   to character-MISMATCHED-dependence failure conditions (bare-linearity explicitly
   marked legitimate when character-matched); gate 6 scope note added; header
   amendment banner.
5. **`VARIATION_DOMAIN_CENSUS.tsv`** — rows 13 (k10) and 14 (C) consequence fields
   restated to the character-matched rule with the counterexample and generating-set
   citations.
6. **Regenerated deterministically by rerun:** `routeA_stage1_results.json`,
   `DERIVATION_STDOUT.txt`.
7. **Rerun record:** `python3 derive_routeA_stage1.py` → **40/40 checks PASS, exit 0**
   (34 original + 3 `A6_*` + 3 `B5_*`), < 5 s, single CPU process. Two consecutive
   reruns: `routeA_stage1_results.json` byte-identical (sha256
   e56025cb79121d8d99309bc67a5038b053a4779f65c5db88beef6b3e487101f6) and
   `DERIVATION_STDOUT.txt` byte-identical — determinism reconfirmed post-amendment.

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The outcome class** — OA1/OA2 MIXED (F-RA1/F-RA2/F-RA3 forced and nontrivial in
  amended form; F-RA4 near-null) — untouched, and re-adjudicated by the verifier as
  standing WITH the amendments (`VERIFIER_REPORT.md` §7).
- **The PW/WS/GC tallies** — 8 pointwise / 2 whole-solution / 4 global-completion +
  R11 per-row — untouched (verifier recount: correct).
- **No OA3** — the one new tension found (mirror vs shift) is resolvable and
  resolution-recorded, not a requirement clash — unchanged.
- **F-RA3 and F-RA4** — statements, witnesses, scope stamps: byte-identical
  (independently confirmed by the verifier's own solves).
- **The census fork-typing** — all 16 rows' fork options and their consequence typing
  (const-vs-field, varied-vs-held, within-vs-over, α active-vs-frozen): untouched
  except the rows-13/14 K₄-honesty wording (no fork was decided; F-A2 clean).
- **The gate COUNT and SEQUENCE** — six gates, same order, same sequence discipline;
  only the two failure-condition wordings and one scope note changed.
- **All 34 original checks** — names, math, and results byte-equivalent (the
  amendment only ADDED `A6_*`/`B5_*`).
- **The pairing enumeration (P1/P2/P3), the L6 both-ways formalization, the
  §2.4 posed problem, and the maximum-conclusion ceiling** — untouched: still no
  candidate, no existence/uniqueness verdict, no physics.
