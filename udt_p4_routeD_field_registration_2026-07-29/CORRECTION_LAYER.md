# Route D — CORRECTION LAYER (post-verifier; slim — NO corrections were required)

Date: 2026-07-29. Package: `udt_p4_routeD_field_registration_2026-07-29/`.
Verifier verdict (`VERIFIER_REPORT.md`): **PASS — no required amendments** (the
arc's first no-required-amendments verdict). Three non-blocking observations,
all adopted below. Same-session-spawned blind verifier, not a hosted external
model — caveat travels.

## 1. The verdict

PASS. Contract-first verified in git (prereg in faf9294, all derivation
artifacts untracked at verification time); rerun ×2 byte-identical, exit 0;
36/36 split audited (29 substantive + 7 guards, no disguised guard); exact
SymPy only; independent script 15/15 exit 0 with own constructions throughout,
preserved as `VERIFIER_INDEPENDENT_CHECK.py`.

## 2. The three observations and their adoption

1. **V7 — the Route-B T2-analog (bracket layer).** The one Route-B Stage-1
   layer without an explicit Route-D check. The verifier computed it:
   [X₁(x), X₂(x)] lands in the class tangent V pointwise and is traceless —
   verbatim extension, zero residual. **ADOPTED as the credited substantive
   check `ADOPTED_T2analog_bracket_pointwise`** (in-script, ← V7): the
   Route-B-grade comparison is now airtight requirement-for-requirement
   (T1/T2/T3/T4-analogs all on record; T5/T6 out of grade). §6 of
   `EXACT_DERIVATION.md` notes the closure.
2. **V2e — the finite-level anchored orbit.** The derivation's singleton leg
   was infinitesimal (honestly graded, same as Route B T1(a)); the verifier
   showed the finite orbit ODE L′ = X̃L − LX is LINEAR in L with the same
   Picard structure — the anchored-singleton claim holds at the FINITE level,
   not just infinitesimally (not a linearization artifact). **ADOPTED as the
   credited substantive check `ADOPTED_finite_level_orbit_linear`** (← V2e);
   §1.5 of `EXACT_DERIVATION.md` carries the grading upgrade note.
3. **Wording.** DECISION_SURFACE item 3's parenthetical "(honest, small)" —
   "small" is a merit adjective on the residual asymmetry. **REMOVED**; the
   stakes-bearing content stays carried in item 2, unchanged.

Rerun after adoption: **38/38, exit 0 = 31 substantive + 7 guards**,
deterministic ×2 (stdout, JSON, and TSV byte-identical across reruns). The two
adopted checks are the ONLY count change; the ledger's i-class-coherence basis
rows and the JSON summary credit them explicitly.

## 3. The verifier's strengthenings and attack record

- **Two outside-K₄ constructions mounted and KILLED exactly** (the success-side
  attack — the live false-clean risk, since the tempting outcome was FAILS):
  an x-dependent screen rotation (only θ ∈ {0, π}, θ′ = 0 — both
  K₄-compatible) and an x-dependent boost in closed form (w = y = 0 only —
  confirming the L01-loophole kill by an independent parametrization).
- **Non-commuting cocycle instance:** K(x) = diag(1,−1) + xE21 with
  [K(x₁), K(x₂)] ≠ 0 — strictly beyond the derivation's commuting witnesses;
  two-sided law + reversal/loop-triviality hold exactly. The transition-law
  closure is not an artifact of commuting instances.
- **Grade comparison made airtight via V7** (adopted, above); mirrored-quotient
  continuity shown DERIVED (L(x) = ẼE⁻¹ automatically C¹), so the
  locally-constant/global-K₄ step's hypothesis is not a choice.
- **Falsifier hunts F-R1..F-R6: NONE fired** (F-R3 hunted first; F-R1 run both
  directions — success attacked by construction, failure audited for glossing;
  F-R4 grep-clean, no parity value anywhere; F-R5 includes the
  no-Route-P-unbanked-citation check).

## 4. Did NOT change (everything substantive)

- **Outcome class OR2** (REGISTERS, both moduli sectors) — unchanged.
- **All theorems and computed claims** (connection-type gauge law; chart
  stability; trivial class-wide stabilizer; pointwise-global K₄; anchored
  singletons; J07 items 1–4 closed, 5/6 supplied/GC; alphabet
  exclusions; J05/J06 instantiations; stratum level-set promotion) — unchanged.
- **`REGISTRATION_LEDGER.tsv` statuses** — all 12 rows unchanged (only the
  count stamp and the credited basis citations updated).
- **The N1–N3 alphabet declarations and their derived exclusions** — unchanged.
- **The decision surface's CONTENT** (items 1–4, the stakes attachment, the
  no-recommendation posture) — unchanged; only the cosmetic adjective removed
  (observation 3) and the status line brought current (verifier pass complete).
- **The map-fact restatement, the ε_m SUPPLIED status, and the ceiling** —
  unchanged; no census branch adopted, no mass claim, no physics.
