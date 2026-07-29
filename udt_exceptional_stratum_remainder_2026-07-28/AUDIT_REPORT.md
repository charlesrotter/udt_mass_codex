# Exceptional-stratum remainder — AUDIT REPORT (gate d)

Date: 2026-07-28. Branch: `grok`. Preregistration committed `ed01bda` BEFORE the derivation
ran. CPU-only symbolic derivation; no solve, no GPU, no canonization.

**GRADE: VERIFIED-WITH-CAVEATS** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, not a hosted external model) returned **BANKABLE-AS-SCOPED after
one required documentation amendment**, applied (EXACT_DERIVATION.md §4(A) +
CORRECTION_LAYER.md C1–C3): the verifier found a genuine proof-record gap in the necessity
argument (an unstated constant-combination lemma), DERIVED the missing lemma itself,
machine-checked it (4/4; preserved in-package as `VERIFIER_LEMMA_B1.py`), and confirmed the
theorem closes. Sufficiency was independently rebuilt from the family metric (exact single
obstruction term), all mechanics byte-identical (44/44), and the verifier tested its own
doubly-asymmetric c=1 control.

## Result first — the stratum dichotomizes; the middle class is EMPTY

On the exceptional stratum `{alpha = 0, S := bu + f^2 = c constant}`:

- **T-d4 (headline): a plane-swapping isometry exists ⇔ c = 1.**
  - *Sufficiency, constructive:* in cap-cycle coordinates the reflection
    `J: phi_+ -> -phi_+` is an isometry for EVERY c=1 profile — symmetric or not — because
    the ENTIRE obstruction is the single cross term `g(v_-, v_+) = (1-c)/(4u)` (verified
    exact; all other J-odd metric entries vanish identically at alpha=0). J swaps the free
    lines V and Y, fixes K and the transverse direction, is cap-fixing and
    orientation-reversing (det = -1 forced wherever f != 0), and extends smoothly to
    completions. The anticipated curvature obstruction for asymmetric profiles DISSOLVES —
    it applies only to the cap-swapping subclass.
  - *Necessity (amended):* via the constant-combination lemma (CORRECTION_LAYER C1) +
    compactness + primitivity + freeness, any two-sided plane-swapping isometry forces
    `Phi_*V = ±Y`, `Phi_*Y = ±V`, and norm matching gives `c = 1` exactly. Scope note C3 on
    the one-directional corner travels; no conclusion rides it.
- **T-d2: all-orders identity at c = 1 — F-d1 does NOT fire.** `g(Y,Y) = 1/u = g(V,V)` is an
  identity, so both plane Grams are the SAME matrix function `diag(-c_E^2 u, 1/u)` under the
  canonical correspondence (K shared; V -> Y the unique other free line; signs
  Gram-irrelevant): every X-jet agrees; NO plane-restricted certificate of any order can
  distinguish.
- **T-d3: no metric-native ambient discriminator exists at c = 1.** The P-defect of the full
  G3 is exactly `diag(0, (c-1)/u, (1-c)/u)` — the norm gap is the ONLY orbit-Gram
  discriminator, and it vanishes at c=1; since J maps `(g, K, V-line, X) -> (g, K, Y-line, X)`,
  ANY natural function of certificate inputs takes equal values on the two planes. Only
  orientation-relative signs differ — not certificate-grade (a metric does not orient);
  nothing promoted.
- **T-d1: the area-VALUE leg grades DERIVED-WITHIN-REGISTRATION.** The u-cancellation is the
  G02 unit-determinant pair action (DERIVED); primitivity leaves sign-only freedom (DERIVED);
  but the ABSOLUTE value `-c_E^2` load-bears on the registered c_E — the FIRST certificate
  leg to do so (flagged). The clock-free derived core is the ratio
  `det G_KY / det G_KV = c = g(Y,Y)/g(V,V)`, presentation-relativity derived (relabel maps
  c -> 1/c; at c=1 all presentation scalars are fixed). Consequence: `c != 1` members are
  objectively distinguished by the pointwise ratio.

**Synthesis (within the preregistered ceiling):** `c != 1` (which, citing the banked gate-(c)
result 5291b63, exists only on NON-complete/principal-orbit-only members): the planes are
pointwise-ratio-distinguished — selectable within registration. `c = 1` (ALL complete two-cap
members): selection is PROVABLY IMPOSSIBLE (the swap isometry exists for every profile). The
preregistration's category (iii) — "certificate-silent but possibly selectable" — is EMPTY.
Combined with the selector theorem and gate (c): **on complete two-cap members of the
registered family, the metric either selects its reciprocal plane uniquely (everywhere off
the exceptional stratum) or provably cannot (on it); there is no middle ground.** The
selector theorem's LIMITS #5 (stratum remainder OPEN) is RESOLVED.

## Falsifiers

F-d1 NOT fired (T-d2 proven, no distinguishing jet). F-d2 NOT fired in the frozen sense —
the leg is not CHOSE-unusable; the honest downgrade (within-registration; c_E load-bearing)
is exactly the contract's anticipated handling. F-d3 NOT fired (44/44 zero-residual;
byte-identical reruns; verifier independent rebuild 22/23 with the single "fail" being the
verifier's own probe-design flaw, resolved by its corrected 4/4 staged lemma check).

## Evidence

`derive_stratum_remainder.py`: 44/44, exit 0, deterministic; verifier rerun byte-identical to
committed outputs; verifier scripts (adversarial rebuild from the family expression at
general alpha; lemma proof preserved as `VERIFIER_LEMMA_B1.py`, re-run in-package exit 0);
package asymmetric control + verifier's own second doubly-asymmetric control (different u
AND f profiles, nontrivial n(s), c_E = 3/2): J-defect exactly zero at c=1, exactly
`-(1-c)/(2u)` at c = 7/5.

## Limits

1. Family CHOSE (P06/P07/P14-class); clock = K conditional; alpha = 0 stratum of the
   registered family. 2. NO certificate leg is ADOPTED — the area-value leg's status
   (within-registration, c_E-load-bearing) is recorded for Charles's adjudication, not
   enacted. 3. The one-directional inequivalence corner (C3) is OPEN; nothing rides it.
4. The swap-GROUP structure (beyond existence) is not classified — OPEN. 5. Orientation
   data are CHOSE, excluded from certificate grade. 6. Gate (c)'s c=1-forcing is CITED for
   scoping only; no derivation here consumes it (verifier-checked, no circularity). 7. No
   physics, no alpha value, no branch, no canonization.

## Verifier record

Blind adversarial pass, 2026-07-28 (scratch /tmp/scratch_verify_d/; independent
implementation 22/23 + corrected staged lemma check 4/4). Attack 1 (sufficiency): CONFIRMED
airtight — 4x4 metric rebuilt from the family expression, only-off-diagonal claim verified,
obstruction term exact, own control passes. Attack 2 (necessity): CONFIRMED WITH AMENDMENT —
found the unstated lemma, derived and machine-checked it, identified the freeness-vs-
injectivity wording slip and the one-directional corner; all applied (CORRECTION_LAYER
C1-C3). Attack 3 (all-orders): CONFIRMED (checked to order 7). Attack 4 (provenance):
CONFIRMED, grade right, no hidden dial found. Attack 5 (synthesis): STANDS — dichotomy
total, no circularity in the gate-(c) citation. Attack 6 (mechanics): byte-identical, ceiling
respected, LIMITS complete. Overall: **BANKABLE-AS-SCOPED** after the amendment — applied.
