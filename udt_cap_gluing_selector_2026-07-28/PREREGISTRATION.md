# PREREGISTRATION — Cap gluing of the plane-selector certificate

Date: 2026-07-28. Branch: `grok` (base `55ae6be`). Authorized by Charles (gate (c),
2026-07-28). CPU-only symbolic derivation; no solve, no GPU, no canonization.

## Question (declared: METRIC-LED)

The selector theorem (banked `6cd9a15`) lives on principal orbits (b > 0); at the two toric
caps the orbit rank drops, b → 0, and D_P is undefined. Question: WHAT HAPPENS to the
certificate's quantities at regular caps, and does cap regularity feed back on the
principal-orbit classification (in particular on the exceptional stratum)?

## Premise ledger

| Premise | Tag |
|---|---|
| Family + registration | CHOSE — inherited P06/P07/P14-class |
| Regular two-cap toric completion: at each cap one primitive circle line closes smoothly | DERIVED-inherited (parent two-cap toric setting + free-circle-classes record); the EXACT regularity conditions on (u, f, b) near a cap are T-c1's job to derive/cite, not to assume |
| Certificate quantities: det G_P, off-eigenline term, tr D_P | DERIVED (theorem package, blind-verified) |
| No claim of a cap-extended response D_P | THEORY — D_P undefined at b = 0; only LIMITS of scalar certificate quantities are in scope |

## Frozen targets

- **T-c1:** derive (or cite exactly from the parents) the regularity conditions at a cap:
  the behavior of b, f, df, u, chi as the cap is approached when the closing circle is (i) the
  registered line V, (ii) the second line Y. State which line closes at which cap in the
  registered completion and what f's cap value is (candidate: f → ±1 for primitive closing —
  derive, do not assume).
- **T-c2:** cap limits of det G_KY = -c_E²(bu+f²), of the off-eigenline term
  -alpha·c_E·df·u²/(bu+f²), and of tr D_KY. Is the witness's df → 0 at caps FORCED by
  regularity, or witness-specific?
- **T-c3 (the feedback question):** if a member lies on the exceptional stratum
  (alpha = 0, bu+f² = const = c) AND has two regular caps, is c forced to a specific value
  (candidate from T-c1: c = f_cap² — derive)? If yes: the COMPLETE exceptional stratum is a
  codimension-refined set, and the (d)-gate's area-VALUE question is decided for complete
  members. Record exactly; no assumption travels from here to (d).
- **T-c4:** does any certificate leg, evaluated as a limit, become singular or discontinuous
  at a regular cap in a way that would obstruct stating the theorem on the full completed
  manifold minus caps? (Continuity atlas; record only.)

## Falsifiers

- F-c1: regularity conditions underivable from the parents' recorded toric structure (gap
  reported, not papered).
- F-c2: a certificate quantity divergent at a regular cap in a way that contaminates the
  principal-orbit classification (first-class outcome — the theorem's scope stamp was doing
  real work).
- F-c3: algebra error (independent implementation).

## Maximum conclusion (pre-committed ceiling)

A cap-limit atlas of the certificate quantities under derived regularity conditions, plus any
exactly-derived feedback on the exceptional stratum for complete two-cap members. The theorem's
principal-orbit scope stamp is either retained (with the atlas as its boundary annotation) or
tightened. No cap-extended response is claimed; no physics, no branch, no canonization.

## Method

Derivation agent (sympy + exact limit computations, witness as control) writes
derive_cap_gluing.py + EXACT_DERIVATION.md + DERIVATION_RESULT.json into this package; blind
adversarial verifier before banking; AUDIT_REPORT.md with scope stamps.
