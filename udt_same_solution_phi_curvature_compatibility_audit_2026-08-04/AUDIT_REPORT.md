# Same-solution founded-phi/curvature compatibility audit

## Result first

The parent second-jet audit left a real but narrow ambiguity: its curvature atlas and its `dphi`
causal atlas were separately supplied algebraic axes. This audit closes the local-existence part of
that ambiguity.

In the registered factorized complete-coframe architecture, a fixed founded-depth first jet and a
full algebraic curvature tensor can occur in one and the same local two-jet. Both the full
eight-generator family and the seven-generator determinant-one screen family have exact curvature
rank 20, in every retained causal stratum of `dphi`.

The audit also finds the corresponding ownership obstruction. Releasing the reference coframe gives
an exact factorization freedom that shifts `phi`, `dphi`, and its Hessian while leaving the complete
coframe unchanged. The metric therefore does not yet identify the physical founded-depth field by
itself. Same-solution compatibility is `CONDITIONAL` on the supplied realization; it is not a unique
section or a native law.

## Exact family atlas

```text
F01 full factorized                 rank 20 / codim 0
F02 determinant-one screen         rank 20 / codim 0
F03 founded + mixing               rank 19 / codim 1  (R_2323=0)
F04 founded + screen               rank 19 / codim 1  (R_0123=0)
F05 founded spectator              rank  8 / codim 12
F06 locked founded/angular         rank 10 / codim 10
F07 locked founded/shift           rank 10 / codim 10
F08 released complete reference    rank 20 / codim 0, phi not identifiable
F09 independent scalar             not typed; no metric action supplied
```

The rank-10 locked counterfamilies are a genuine structural observation: reciprocal/angular and
reciprocal/mixing combinations carry more curvature structure than the rank-8 founded spectator.
Neither lock is selected, and neither is curvature-complete.

## First-jet and causal-stratum result

At fixed zero jet and first jets, curvature is affine in the allowed generator Hessians. The
connection-quadratic term shifts the affine origin, but the Hessian coefficient map does not depend
on the causal type or amplitude of `dphi`. Exact ranks are consequently the same for zero,
timelike, spacelike and nonzero-null representatives.

This is a local two-jet statement. It is not a time-live equation and says nothing about which
curvature a physical solution follows.

## Factorization ownership result

The exact finite identity

```text
E(phi+chi,D,S D(chi)) diag(D(chi)^-1,I_2) = E(phi,D,S)
```

shows that an unfixed reference presentation can absorb a local shift of founded depth. The linear
first-jet map has rank 16 and nullity 8 per coordinate direction; the second-jet coefficient map has
the same per-slot rank/nullity. Explicit kernel vectors shift the founded jet and compensate it in
the reference coframe.

The correct reading is not that `phi` is fake. The abstract reciprocal parameter remains derived.
The result says that its **physical spacetime assignment is relational/section data not recoverable
from the complete coframe without an additional ownership rule**.

## What was learned

1. The previous curvature and causal axes can be joined inside one local realization; they are not
   algebraically incompatible.
2. Full local compatibility is abundant enough that it does not select a curvature or extension.
3. Screen and mixing sectors are jointly sufficient for full curvature even when screen area is
   removed, while removing either complete sector leaves one extra restriction.
4. Locked reciprocal/angular and reciprocal/shift motifs leave distinct rank-10 fingerprints.
5. The actual remaining seam is no longer local algebraic compatibility. It is the native ownership
   of the founded-depth assignment and its differential/global law.

## Maximum conclusion

```text
DERIVED_FACTORIZATION_NONIDENTIFIABILITY__
CONDITIONAL_FULL_LOCAL_PHI_CURVATURE_COMPATIBILITY_IN_F01_F02__
DERIVED_RESTRICTED_FAMILY_CODIMENSIONS__
NO_METRIC_NATIVE_PHI_ASSIGNMENT_OR_CURVATURE_SELECTION
```

No preferred frame, unique extension, action, source, carrier, boundary, density feedback,
bootstrap fixed point, `X_max`, matter, mass, observation fit, or canon statement is derived.

## Verification

- preregistration commit: `7c99952f`;
- frozen-universe commit: `32222612`;
- primary exact SymPy calculation and separate standard-library `Fraction` reconstruction agree;
- three rank-20 families have exact saved 20-by-20 inverse witnesses;
- 23/23 fail-closed checks pass;
- 16/16 exercised mutation catches pass;
- 28/28 fixed-base source hashes replay exactly.
- fresh read-only `gpt-5.4` semantic review: `ACCEPTED`, no repairs and no blocking findings;
- repository gates: 18 premise guards, 166 checked links, six frozen manifests/127 members/133
  paths, 1,114 current paths, 306 frontier rows/101 targets, tests `70 passed, 1 xfailed`, and all
  83 unrelated untracked metadata identities unchanged.
