# Exact `lambda` component and degeneration atlas

Date: 2026-07-27

Preregistration: `6df7f07`

Preregistration correction: `2ec7a4b` (freezes the inherited Torch tolerance before the new Torch
holdouts)

Grade: `VERIFIED_WITH_CAVEATS_EXACT_ONE_AXIS_CERTIFICATE_ATLAS`

## Result first

The six open intrinsic-pair neighborhoods do not all join along the frozen angular-response axis.

The complete determinant curve has exact degree seven and seven distinct simple real roots. Those
roots partition the full real `lambda` line into eight rank-three certificate intervals. The six
existing witnesses occupy three of them:

- C01, C02, and C03 are connected within one interval;
- C04 and C05 are connected within a second;
- C06 occupies the adjacent third interval.

This is a real angular/`phi` interaction in the complete metric: changing only the angular response
causes the chosen intrinsic clock fingerprint to lose and recover rank repeatedly, while depth,
twist, slice signature, and global coframe remain intact.

## What it does—and does not—mean

The seven roots are exact boundaries of this *certificate atlas*. They are not yet physical
boundaries. At each root, our three chosen curvature fingerprints cease to determine all three
spatial directions at the north event. The clock may still be intrinsically identifiable using a
different event, different metric invariants, or the full Killing system.

Therefore the result does not select one `lambda`, prove three physical phases, or show that the
underlying clock/ruler motif is disconnected in the full metric space.

## Exact census

The roots occur approximately at:

```text
-92.92855, -13.62872, 0.079296, 0.410692,
1.610637, 2.429953, 54.17885.
```

The central four are the immediately relevant boundaries around the sampled witnesses; the two very
large-magnitude roots and the negative `-13.63` root complete the real-axis census without being
discarded as inconvenient.

## Verification

- degree bound: at most 9; actual exact degree: 7;
- production nodes: 10/10 exact;
- exact rational holdouts: 7/7;
- exact real roots: 7, all simple;
- independent standard-library Sturm roots: 7/7;
- interval signs: 8/8;
- center assignments: 6/6;
- independent Torch full-curvature holdouts: 5/5;
- maximum Torch scaled error: `4.951594689828198e-14`;
- fail-closed corruptions: 22/22.

No fresh external-model context was available, so the grade retains a caveat despite the two
independent computational methods.

## Co-presence boundary

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

Nothing in the root calculation promotes co-presence into an access law or supplies the missing
whole-solution selector.

## Next scientific boundary

The next metric-led question is now sharply localized: at each of the seven exact roots, is the rank
loss merely a bad choice of three fingerprints at one event, or does the complete metric actually
gain symmetry or lose the intrinsic clock line?

That root-resolution audit should first vary the evaluation event and invariant basis without
changing the metric. Only unresolved roots would then require a direct Killing-system analysis. This
is preferable to introducing an action or searching new coefficients.

## Four evidence gates

1. **Preregistered:** yes, `6df7f07`, with correction `2ec7a4b` before independent Torch outcomes.
2. **Full or bounded:** full real `lambda` axis of one fixed complete off-shell family; not the full
   profile, topology, or on-shell configuration space.
3. **Independently verified:** exact rational Sturm analysis and separate full-Riemann Torch geometry;
   no fresh external-model verifier.
4. **Every premise audited:** yes; fixed profile, twist, scale, event, invariants, degree bound,
   nodes, tolerances, semantics, and excluded physics remain explicit.
