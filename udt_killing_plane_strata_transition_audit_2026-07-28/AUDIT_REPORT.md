# Killing-plane and two-stratum transition audit

Date: 2026-07-28

Preregistration: `0d6d83b`

Final bounded grade after correction and fresh adversarial re-review:
`VERIFIED-WITH-CAVEATS_BOUNDED_STATIONARY`

## Result first

Conditional on the registered `(K,V)` Killing plane, the fully Hopf-descended branch is not
generically missing a clock selector. Whenever the
reciprocal depth is nonconstant somewhere on the connected quotient base, the complete metric's
Gram form on its Abelian Killing plane changes with two exact, basis-independent eigenlines:

```text
timelike clock:    K,                       response -2 X(phi),
spacelike ruler:   V-(alpha/c_E)K,          response +2 X(phi).
```

Their norms are exactly the founded reciprocal weights. The construction uses only the complete
metric and its descended Killing algebra; under every constant change of Killing basis its response
endomorphism transforms by conjugation, so the lines are not coordinate artifacts. The exact
depth-mixed part of the twist of every `K+Omega V` independently selects the same timelike line when
`dphi` is nonzero. This is not a claim that the full twist vanishes; contact-twist components
generally remain.

This supplies the missing selector inside the two-symmetry plane for the nonconstant-depth stratum.
It does not use strong local CSN, an action, carrier, source, density, or dynamics.

## Both forks can coexist geometrically

The fully descended stratum and the earlier rank-three unique-clock stratum remain disjoint under
the old certificate, but they are continuously adjacent within the same registered stationary
configuration family. An explicit analytic positive-metric path joins a nonconstant descended
configuration to any exact old C01--C06 witness. The old invariant-gradient determinant is nonzero
at the witness endpoint and therefore is nonzero at points arbitrarily close to the descended
endpoint. At the endpoint the new Gram-response certificate selects `K`; rank-three points exist
arbitrarily near it and the old certificate selects `K` at those points. The analytic argument does
not assert that every sufficiently small deformation has rank three.

This is an exact geometric handoff between two selection methods. It makes the proposed idea that
the strata might later describe different physical regimes geometrically plausible, but it does
not identify either as macro, micro, or mass emergence.

## Why the result is mixed rather than universal

If `phi` is constant everywhere, the Gram map does not change and the new selector vanishes. Circle
topology identifies the compact line `V`, but not one of the noncompact helices. When `V` is
spacelike, its metric-orthogonal complement is unique, yet for nonzero `alpha` it differs from the
founded clock `K`. Null and timelike compact-fiber strata have further causal degeneracies. Only the
special constant-depth, twist-off control makes that orthogonal line equal `K`. If both depth
variation and contact curvature vanish, every constant Killing line is twist-free while the Gram
response also vanishes, so neither certificate selects the founded clock.

The primitive-circle lattice permits exactly `K -> rK+bV`, `V -> +/-V`, with `r` nonzero and `b`
real. This fixes the registered compact line but leaves every noncompact helix available. Metrics
with a larger Killing algebra are a separately retained scope boundary: the audit does not select
the registered plane from additional Killing planes or circles.

Accordingly the primary classification is

```text
MIXED_PARAMETER_STRATA
```

with the sharper positive statement

```text
UNIQUE_METRIC_FOUNDED_CLOCK_AND_RULER_LINES
```

on the fully descended nonconstant-depth subfamily.

## Evidence gates

1. **Preregistered:** yes, commit `0d6d83b`, before calculating the Gram response or transition.
2. **Full or bounded:** full real projective Killing line, constant/nonconstant depth, twist, causal,
   and transition classification inside the stationary constant-`alpha` block-screen `R x S3`
   family; not generic spacetime or on-shell dynamics.
3. **Independent:** 31 production symbolic identities and 209 exact/rational/repository checks in a
   separate implementation that imports no production functions; 24 exercised mutation catches.
   It reconstructs all four twist components, directly re-evaluates the zero-contact/depth control,
   checks the universal-cover kernel conditions and representatives of the derived lattice subgroup,
   checks exact endpoint identities and rational convex-path samples, and actually executes the
   repository gates. Universal path positivity rests on the analytic convexity of the positive-
   definite cone, not on the finite samples. The
   analytic identity-theorem inference remains assigned to the fresh semantic reviewer rather than
   disguised as a machine string check.
4. **Premises:** every physical choice is recorded in `PREMISE_LEDGER.tsv`; counterbranches and
   exceptional strata are retained rather than filtered.

All three fresh reviews are preserved unchanged. The final reviewer confirmed every mathematical
and verifier correction, returning `PASS_WITH_REQUIRED_CORRECTIONS` only because the file containing
its own output could not yet exist in its read-only view. The outer review runner then saved that
output at the exact registered path, and navigation was rerun. Final repository gates are recorded
with the frozen package.

## Maximum conclusion

Within the registered stationary constant-`alpha` full-screen family, conditional on its registered
`(K,V)` plane, the complete descended metric
with nonconstant depth intrinsically recovers the founded reciprocal clock/ruler pair. Constant
depth remains a distinct framing/degeneracy stratum. The descended and old rank-three unique-clock
strata are continuously adjacent and hand off the same `K` line. No macro/micro identification,
mass emergence, action, source, carrier, density law, dynamics, or physical branch is derived.
