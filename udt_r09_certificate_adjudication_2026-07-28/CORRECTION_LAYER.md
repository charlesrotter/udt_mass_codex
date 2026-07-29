# CORRECTION LAYER — gate (b) R09 adjudication (append-only)

Date: 2026-07-28. Source: blind adversarial verifier pass (required change + findings), applied
before banking. The banked verdicts (F-b2 NOT FIRED; F-b1 FIRED leg-free; NO-CONFLICT
with-rates) are UNAFFECTED by every item below.

## C1 (required) — "crowns span(K,V) uniquely" was a scope slip

EXACT_DERIVATION.md §4.2 and DERIVATION_RESULT.json field `T_b2...C_restricted_status`
("crowns span(K,V) uniquely") over-scoped the selector theorem's uniqueness: P-SEL T5 proves
uniqueness only over the topology-supplied TWO-candidate set {span(K,V), span(K,Y)}; its
general-(m,n) row (T6) is record-only. On the §4.2 conflict-witness member the general-(m,n)
uniqueness is FALSE: the verifier exhibited **span(K, V−2Y)** passing all three C_restricted
legs (`det G = -25 c_E^2` constant; diagonal restricted response; rates exactly
`(-2chi, +2chi)`; zero-residual checks R4–R6 of the verifier's independent script). §4.2 is
corrected in place (visible in git); the generated JSON is NOT hand-edited — read its
`C_restricted_status` as "crowns span(K,V) within the {V,Y} candidate set."

Consequence, recorded: the CONFLICT verdict STANDS and is strengthened — on the witness the
C_restricted satisfier set {span(K,V), span(K,V−2Y)} is disjoint from the C_full satisfier set
{span(K,2V+Y), span(K,−3V+Y)}. A new bounded observation for any future certificate work: over
the general-(m,n) candidate class, C_restricted is not single-valued on all members; its
single-valuedness is currently proven only for the topology-supplied pair.

## C2 (cosmetic) — K06 gate vacuous as encoded

The cap-closure corollary's machine gate K06 encodes its contradiction as the trivial
`2/n != 0`; the logic it stands for (independently re-derived by the verifier via the
invariance ODE `X(s) = df(n^2 s - z^2)/(nz)`, `s = bu`) is correct. Gate strengthening left to
any future revision; the corollary remains "record, conditional" and does not soften F-b1.

## C3 (note) — C_full quantifier frozen pre-use, not in the preregistration

The preregistration left C_full's everywhere-vs-pointwise quantifier unfrozen; the derivation
froze it (region-wide) in §2 BEFORE use and disclosed the pointwise formal case separately
(§5). Acceptable per the verifier; recorded here so the freeze's location is explicit.
