# PREREGISTRATION — R09 certificate adjudication (restricted-plane vs full-response ownership)

Date: 2026-07-28. Branch: `grok` (base `55ae6be`). Authorized by Charles (gate (b),
2026-07-28). CPU-only symbolic derivation; no solve, no GPU, no canonization.

## Question (declared: METRIC-LED, adjudicative)

The repo carries two candidate "the metric owns this plane" criteria that are known to
disagree in extension (parent R09): **C_restricted** — the founded-pair certificate on the
plane-restricted response (the selector theorem's certificate: constant area, K-eigenline,
founded rates ±2χ of D_P = G_P⁻¹X(G_P)); **C_full** — the plane is an invariant subspace of
the full three-direction response D₃ = G₃⁻¹X(G₃) (with founded rates on it). Parent R02/R09:
span(K,V) is D₃-invariant only on the df=0 stratum. The adjudication: **can the two criteria
ever crown DIFFERENT planes, or is C_full simply EMPTY wherever C_restricted selects?** This
does NOT decide which criterion is "the" ownership definition (that is a foundational call for
Charles); it classifies their compatibility.

## Premise ledger

| Premise | Tag |
|---|---|
| Family + registration (constant alpha, stationary, descended, Hopf bundle) | CHOSE — inherited P06/P07/P14-class |
| Candidate planes: 2-planes containing K spanned with W = mV + nY (real (m,n) ≠ (0,0)) | DERIVED-inherited (parent scan superset); the two free lines {V,Y} are the topology-supplied primitives |
| D₃, G₃, derivative rules | DERIVED (parent §2, verifier-confirmed) |
| C_restricted | the selector theorem's certificate (banked 6cd9a15), R09-relative by construction |
| C_full: D₃-invariance of the plane + founded rates on it | DERIVED-inherited (parent R02's invariance analysis); "founded rates" leg optional — test with and without |
| Principal orbits only (b > 0) | THEORY (parent: D₃ undefined at caps) |

## Frozen targets

- **T-b1:** derive the COMPLETE set of D₃-invariant 2-planes containing K, stratified by
  (alpha = 0 / ≠ 0) × (df = 0 / ≠ 0) — exact conditions on (m,n) for span(K, mV+nY) to be
  D₃-invariant, from the parent's exact D₃ entries.
- **T-b2 (the adjudication):** does there exist an admissible member and a plane P ≠ span(K,V)
  with P satisfying C_full while span(K,V) satisfies C_restricted? Outcomes: NO-CONFLICT
  (C_full empty or agreeing wherever C_restricted selects) / CONFLICT (exhibit it exactly).
- **T-b3:** on the df = 0 stratum (where parent says span(K,V) IS D₃-invariant): do C_full and
  C_restricted agree in crowning there? Include the alpha = 0 exceptional overlap.
- **T-b4 (record only):** the rate spectrum of D₃ restricted to each invariant plane found in
  T-b1 — founded (±2χ) or not; no claim frozen.

## Falsifiers

- F-b1: a CONFLICT in T-b2 — first-class outcome; would make R09 certificate-relativity a live
  wound in the selector theorem's standing (the theorem's LIMITS #3 already carries the risk).
- F-b2: algebra error vs the parent's D₃ entries (independent implementation must reproduce
  them before use).

## Maximum conclusion (pre-committed ceiling)

A criteria-compatibility classification on the registered family, principal orbits, clock=K
conditional. If NO-CONFLICT: the R09 caveat is downgraded from "criteria disagree" to
"the full criterion is empty where the founded certificate selects — no crowning conflict is
possible in this family," strengthening the selector theorem's standing WITHOUT adjudicating
which criterion is the ownership definition. If CONFLICT: banked with equal standing. No
physics, no alpha value, no branch, no canonization.

## Method

Derivation agent (sympy, zero-residual gates, numeric spot checks) writes
derive_r09_adjudication.py + EXACT_DERIVATION.md + DERIVATION_RESULT.json into this package;
blind adversarial verifier (independent implementation) before banking; AUDIT_REPORT.md with
scope stamps; commit only after the verifier pass.
