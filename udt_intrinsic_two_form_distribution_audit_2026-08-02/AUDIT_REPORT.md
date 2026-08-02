# Audit report — intrinsic two-form distribution on the complete finite cell

## What was learned

The six previously certified intrinsic nonzero branches all carry the same exact qualitative
distribution atlas. Where

```text
W=dPhi_contact wedge dSigma_contact
```

is nonzero, its kernel inside the four-dimensional tangent space is exactly two-dimensional: the
clock line plus one metric-derived spacelike line. That spatial line is:

```text
SCREEN_CONTAINED on one exact nonempty locus,
GENERIC_MIXED on another exact nonempty open locus,
never RULER_ALIGNED in the registered ensemble.
```

This is not point evidence. The exact global coefficients factor as `-24 q3(f12,f13,f23)`, and the
complete zero set is

```text
q3=0 union three great circles C03,C13,C23.
```

The nonzero domain has exactly two connected components. The sign-independent line extends uniquely
through the generic part of the equatorial zero sheet, but not through any point of the three great
circles. The obstruction is exact path dependence, including at their two shared poles.

## Evidence grade

`VERIFIED` for this bounded stationary profile ensemble. All four evidence gates pass:

- preregistration commit `942e8790`;
- source-freeze commit `7d3c7296`, 64 sources, manifest SHA-256
  `48dcc11e79a0395e920c159a88346656011d8784118f11620f6996db040be122`;
- exact production plus 32 fail-closed mutations;
- fresh independent exact review, `PASS`, no correction;
- repository gates: six frozen manifests/133 paths, 1,114 current paths, 101 frontier targets,
  current-premise verifier, and `70 passed, 1 xfailed`.

The 32 catches are honestly classified as 26 exact-output/algebra guards, five semantic scope
guards, and one evidence-backed independence guard. Semantic guards are not counted as extra
derivations.

## Candidate census

```text
9  ZERO intrinsic controls,
6  MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI,
2  PROJECTOR_BLOCKED controls,
1  METRIC_DEGENERATE control.
```

The six full distributions are C04, C08, C09, C10, C16, and C17. No candidate or locus is selected
as physical.

## What remains open

The result does not give a global nonsingular line, carrier, Hopf section, action, field equation,
matter source, boundary law, bootstrap value, density, `X_max`, mass, stability, or phenomenology.
It is stationary and off shell. Other profiles or complete-cell topologies can have different zero
and type loci.

The next justified metric-led object is the intrinsic defect/transport atlas registered in
`NEXT_STEP.md`: projective winding and connection/holonomy data around the exact defect graph,
without calling those defects particles or importing a carrier.
