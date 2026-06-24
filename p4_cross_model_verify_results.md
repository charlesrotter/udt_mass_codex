# P4 — CROSS-MODEL VERIFY (SOLVER_INTEGRITY_UPGRADES_SPEC P4)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** DONE (mechanism documented +
exercised on a real import classification; disagreement logged + folded back).
Files: `CROSS_MODEL_VERIFY.md` (protocol), `.claude/skills/verifier-before-record/SKILL.md`
(escalation added), `solver_action.py` (matter_weight evidence refined), `tests/test_operator_from_action.py`.

## What it does
For LOAD-BEARING calls (native-vs-import classifications, "must-quantize"-class verdicts, CANON
candidates), escalate beyond the same-context same-model verifier: run an ADDITIONAL blind verifier
on a DIFFERENT Claude tier, fresh zero-context, pointed at the source docs (not the prior verdict).
Disagreement is logged + resolved/escalated, never dropped.

## Scope (Charles ruling 2026-06-23)
Realized cross-check = **fresh zero-context Claude, optionally a different tier**. True non-Claude
(external API) is DEFERRED. NOTE: Fable was attempted as the "different family" and is NOT accessible
in this environment, so the different-MODEL axis is realized as a different Claude TIER
(opus-driver -> sonnet-verifier). The fresh-zero-context axis (no shared conversation blind spot) is
the load-bearing part and is fully available.

## Acceptance (per spec) — MET
- **Documented command/flag:** `CROSS_MODEL_VERIFY.md` (when/how/logging) + the Agent `model=` param
  is the mechanism; the `verifier-before-record` skill now carries the escalation rule.
- **Used on the next import classification:** YES — exercised on the `e^{2phi}` matter-weight call.
- **Disagreement logged, not dropped:** YES — see below; folded back into the source-of-truth.

## First use — the e^{2phi} matter-weight classification
- **Primary (opus, P2):** "the e^{2phi} matter weight is UNTRACED -- appears NOWHERE in F2/scale-
  symmetry/CANON."
- **Cross-model (Sonnet, fresh zero-context, agent af66e7f4a8b64ad09):** **PARTIALLY-TRACED.**
  - `a(phi)=e^{+phi}` IS derived — but only for a STATIC POINT-PARTICLE rest-mass
    (native_dilation_weight_derivation D2; the verifier added a STATIC-ONLY restriction).
  - Extending it to the full FIELD-matter Lagrangian as `e^{2phi}L_m` is an explicitly-FLAGGED
    **CHOSE** in `matter_regrade_derived_operator_results.md` (R3, line 240); the author's own
    "Attack-Here" block calls it unresolved.
  - The scale-symmetry principle applied to the (all-angular) field-matter terms L2/L4 gives shift-
    weight 0 -> weight 1 (e^0), NOT e^{2phi}. CANON is silent. Live code has no e^{2phi} on L_m.
- **DISAGREEMENT (logged):** the cross-model REFINED "appears nowhere" -> "appears as a NAMED CHOSE
  with a derived point-particle cousin." The CORE conclusion is UNCHANGED and better-grounded: the
  field-matter e^{2phi} is NOT derived; canonizing it would be smuggling.
- **FOLDED BACK:** `solver_action.py` matter_weight evidence updated UNTRACED -> PARTIALLY-TRACED
  (citing matter_regrade R3 + the cross-model agent id); the P2 guard now asserts the CHOSE flag.
  Suite still 16 passed / 5 xfailed.

## Value demonstrated
The cross-model pass caught that the same-model chain's wording was too strong AND surfaced the exact
provenance (a named CHOSE + a derived static-point-particle cousin) the opus chain had missed — a
concrete, load-bearing refinement. This is the cross-model axis earning its place for import-class
verdicts. (For migration: the matter weight is a documented open posit, not a total unknown.)

## Next
P5 — shrink the live state into a ruthlessly-pruned LIVE.md, then the integrity arc is complete and
the physics frontier (time-live native S^2) resumes.
