# CROSS-MODEL VERIFY — protocol (SOLVER_INTEGRITY_UPGRADES_SPEC P4)

**Purpose:** for LOAD-BEARING calls, run the blind verifier on a DIFFERENT model (and/or a fresh
zero-context instance), not another same-context same-model subagent — which shares blind spots.
**Charles ruling (2026-06-23):** the realized cross-check axis is a **fresh zero-context Claude**,
optionally a **different Claude tier**. (True non-Claude needs an external API — DEFERRED; Fable was
attempted and is not accessible in this environment.)

## WHEN (load-bearing only — not every result)
- NATIVE-vs-IMPORT classifications (is X derived, or an imported/posited assumption?).
- "MUST-QUANTIZE"-class verdicts and other conclusions that would gate a major direction.
- CANON candidates and any value/identity about to be banked as evidence.
(Routine results get the normal single blind verifier; this is the escalation tier.)

## HOW
1. Run the standard blind pass (`verifier-before-record`) first.
2. For a load-bearing call, ALSO spawn a verifier with **a different model** via the Agent `model`
   param — fresh zero-context, adversarial, self-contained (point it at the source docs/code, NOT
   at the prior verdict). Available tiers here: opus / sonnet / haiku. Use a tier different from the
   driver (e.g. driver=opus -> cross-check on sonnet). Non-Claude is deferred.
3. The cross-model agent reaches its OWN verdict from the documents.

## LOGGING (binding — disagreement is NEVER silently dropped)
- Record in the result's doc: the cross-model agent's **id + model + verdict**, and any
  DISAGREEMENT or REFINEMENT vs the primary verdict.
- A disagreement is RESOLVED or ESCALATED to Charles — never dropped. If the cross-model check
  refines a classification, UPDATE the source-of-truth (e.g. `solver_action.py` ACTION_TERMS
  evidence) to the more accurate wording.

## FIRST USE (2026-06-23 — the e^{2phi} matter-weight classification)
- Primary (opus, this session, P2): "the e^{2phi} matter weight is UNTRACED -- appears NOWHERE."
- Cross-model (Sonnet, fresh zero-context, agent af66e7f4a8b64ad09): **PARTIALLY-TRACED.**
  a(phi)=e^{+phi} is DERIVED for a static POINT-PARTICLE rest-mass; the extension to the full
  field-matter Lagrangian (e^{2phi}L_m) is an explicitly-FLAGGED **CHOSE** (matter_regrade R3,
  l.240), NOT derived; scale-symmetry gives angular field-matter weight 1, not e^{2phi}; CANON silent.
- DISAGREEMENT (logged, not dropped): the cross-model REFINED "appears nowhere" -> "appears as a
  named CHOSE." Core conclusion (NOT derived for field matter; unsafe to canonize) UNCHANGED and
  better-grounded. ACTION: `solver_action.py` matter_weight evidence updated to PARTIALLY-TRACED;
  the P2 guard now asserts the CHOSE flag. (= P4 acceptance "used on the next import classification;
  disagreement logged.")
