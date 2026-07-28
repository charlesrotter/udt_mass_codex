# PREREGISTRATION — Exceptional-stratum remainder (can anything metric-native select there?)

Date: 2026-07-28. Branch: `grok` (base `55ae6be`). Authorized by Charles (gate (d),
2026-07-28). CPU-only symbolic derivation; no solve, no GPU, no canonization.

## Question (declared: METRIC-LED)

On the selector theorem's exceptional stratum `{alpha = 0, S := bu + f² = const = c}` both
planes satisfy the banked certificate and it is silent. At exchange-symmetric members
selection is provably impossible (parent isometry). The remainder question: for
NON-exchange-symmetric stratum members, does ANY metric-native datum distinguish the two
planes — or is the silent set genuinely larger than the symmetric locus?

## Premise ledger

| Premise | Tag |
|---|---|
| Family + registration | CHOSE — inherited P06/P07/P14-class |
| Stratum definition {alpha=0, S=c} | DERIVED (theorem package, blind-verified) |
| Founded-area VALUE leg candidate: det G_P = -c_E² exactly (not merely constant) | PROVENANCE TO BE DERIVED in T-d1 — legitimate only if the founded pair's normalization + primitive lattice fix the value; if the provenance fails, the leg is CHOSE and unusable |
| Primitive lattice normalization of V and Y (no free rescaling of circle generators) | DERIVED-inherited (parent free-circle-classes: primitivity fixes the generator up to sign) |
| Principal orbits; cap feedback | any T-c3 result from the parallel cap-gluing package is NOT assumed here; if it lands, it is cited as a separate package's result |

## Frozen targets

- **T-d1 (area value):** at alpha=0 on the stratum: det G_KV = -c_E², det G_KY = -c_E²·c.
  Derive whether the founded-pair normalization + primitivity make the VALUE -c_E² a
  legitimate certificate leg (provenance argument, cited to the founded-pair parents). If
  legitimate: for c ≠ 1 the extended certificate selects span(K,V); the silent set shrinks to
  {alpha=0, S=1}. If not derivable: record the leg as CHOSE and do not use it.
- **T-d2 (all-orders identity at c=1):** for c = 1 stratum members, prove or refute: the
  plane-restricted data of the two planes (Gram entries and ALL X-jets thereof) are identical
  identically in the free profile. (Candidate proof: at alpha=0, c=1, G_KY = diag(-c_E²u, u⁻¹)
  = G_KV as functions of u alone; then all jets agree. Verify exactly; hunt hidden asymmetry.)
- **T-d3 (ambient data):** for c = 1 members, inventory the metric-native AMBIENT quantities
  that differ between the two planes' completions: g(V,Y), the complementary direction H and
  its geometry, orientation/sign data, holonomy of the relevant circle bundles. Which, if any,
  is (i) nonzero/asymmetric for generic stratum profiles, (ii) certificate-grade (well-defined
  given (g, K, line, X), no presentation dependence)? Record an exact candidate list with
  provenance tags — no promotion to a selector without a derivation.
- **T-d4 (exchange-isometry characterization):** derive necessary and/or sufficient conditions
  on a c = 1 stratum profile for an isometry swapping the two planes to EXIST (sufficient:
  witness-type even profiles — verify; necessary: derive or bound). The truly-impossible set =
  members admitting the swap isometry; the certificate-silent-but-possibly-selectable set =
  the rest. Classify as far as exact computation reaches; UNRESOLVED remainder is recorded as
  OPEN, not forced.

## Falsifiers

- F-d1: T-d2 refuted (a jet distinguishes at c=1) — first-class: plane-restricted selection
  EXTENDS onto the stratum and the theorem's silent set was overstated.
- F-d2: T-d1's provenance argument fails — the area-value leg is CHOSE; c ≠ 1 stays silent.
- F-d3: algebra error (independent implementation).

## Maximum conclusion (pre-committed ceiling)

A sub-classification of the exceptional stratum: (i) area-value-selectable (c ≠ 1, IF T-d1's
provenance holds), (ii) provably-impossible (swap-isometry members), (iii) certificate-silent
remainder with an exact inventory of ambient candidate discriminators (tagged, underived), and
the T-d2 all-orders statement. No new certificate leg is ADOPTED (adoption = Charles); no
physics, no branch, no canonization.

## Method

Derivation agent (sympy, zero-residual gates; witness + at least one NON-symmetric c=1 profile
as controls) writes derive_stratum_remainder.py + EXACT_DERIVATION.md +
DERIVATION_RESULT.json into this package; blind adversarial verifier before banking;
AUDIT_REPORT.md with scope stamps.
