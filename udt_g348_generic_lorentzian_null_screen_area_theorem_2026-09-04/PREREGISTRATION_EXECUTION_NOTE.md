# G348 preregistration execution note

Date: 2026-09-04
Preregistration commits: `17c35cc6`, crossing refinement `23e50369`

## First production execution

The first outcome execution returned `39541/39542`. Every phase, observer, coordinate, affine,
area, sewing, rank, and sign check passed. The only failed assertion was the supplemental
`rank_one_zero_order` diagnostic.

That diagnostic compared `|det B(pi-epsilon)/det B(pi+epsilon)|` directly with one for
`epsilon=1e-4`. For the exact witness

```text
det B(L) = sin(L) sinh(L),
```

the zero is simple, but the smooth nonzero `sinh(L)` factor makes the two finite-offset magnitudes
differ at first order in `epsilon`. Equality is not the mathematical definition of a simple zero.

Before rerun, replace only this false finite-offset equality with the centered first derivative at
the rank-one zero and the centered second derivative at the rank-zero witness. Their exact targets
are `-sinh(pi)` and `2`. Retain `epsilon=1e-4` and the preregistered `2e-6` zero-stratum tolerance.

No candidate theorem, sign, rank classification, physical premise, source, tolerance, alternative,
maximum conclusion, or production sample changes. The failed first output remains recorded here;
the corrected diagnostic must be independently reproduced rather than hidden.

## Canonical-momentum typing clarification

The preregistration wrote the phase state in the metric-vector form `p=Dx/dlambda`. During the
arbitrary-`GL(2)` derivation the equivalent canonical form is made explicit:
`v=Dx/dlambda` and `p=v^flat`. In orthonormal quotient frames their components agree; in general
coordinates `v` is a vector and `p` a covector. This is a metric-musical type clarification, not a
new structure or a change to any formula, test, alternative, tolerance, or conclusion.

## First aggregate replay

The first aggregate returned `17/18`. All source, preregistration, script, production, independent,
hostile, provenance, scope, and no-write gates passed. The sole failure was an exact documentary
substring split by a Markdown line wrap between “cannot” and “occur.” Before rerun, shorten only
that phrase hook to the unsplit clause. This changes no evidence or scientific claim.
