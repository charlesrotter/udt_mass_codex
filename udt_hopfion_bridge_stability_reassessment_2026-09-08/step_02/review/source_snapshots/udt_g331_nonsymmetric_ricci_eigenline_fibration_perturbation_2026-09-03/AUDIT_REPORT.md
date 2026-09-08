# G331 audit report — nonsymmetric Ricci eigenline and fibration boundary

Date: 2026-09-03
Status: `EXTERNALLY_ACCEPTED__BOUNDED_EIGENLINE_FIBRATION_BOUNDARY`

## Bounded landing

```text
UNIFORM_RICCI_GAP_PRESERVES_GLOBAL_SMOOTH_EIGENLINE
__ARBITRARILY_CLOSE_NONHOMOGENEOUS_METRICS_CAN_HAVE_IRREGULAR_NONCLOSED_RICCI_EIGENFLOW
__HOPF_FIBRATION_AND_G330_PERIOD_NORMALIZATION_ARE_NOT_PERTURBATION_OPEN
__LOCAL_DYNAMIC_CARRY_REMAINS_CONSTRAINT_COMPATIBLE_AND_GAP_CONDITIONAL
```

## Result

The metric-native line found in G330 survives much more broadly than the Berger symmetry. On the
complete class of sufficiently `C2`-close smooth spatial metrics, a uniform separation of the
simple Ricci eigenvalue gives a global smooth rank-one spectral projector. Because every real line
bundle on `S3` is trivial, the line has a global unit representative up to unselected sign.

Closed Hopf fibres do not share that openness. A global weighted contact-metric family approaches
every non-round Berger metric. Its exact spatial Ricci tensor selects the weighted Reeb line. For
irrational ratios of arbitrarily close weights, generic line orbits are nonclosed and dense on
invariant two-tori. Thus the spatial metric can retain a simple intrinsic Ricci line while losing a
circle fibration. A separate compactly supported conformal bump verifies that even the old Berger
vertical direction tilts under a genuinely local nonhomogeneous metric change.

G330's absolute integer used a common closed-fibre length. That normalization is unavailable for
the irregular flow. This does not rule out differently defined framed/contact invariants; it blocks
calling any such replacement the already-derived G330 quantity.

For active-equation dynamics, the claim is narrower. Any independently constraint-compatible
smooth datum in the gap-open neighborhood retains the line on a nonzero local interval by smooth
Cauchy evolution and gap continuity. Neither explicit metric family has been proved to solve the
vacuum constraints with some extrinsic curvature. Hence G331 does not yet provide a lawful
nonsymmetric history which dynamically destroys or retains the fibration.

## Evidence

- preregistration committed and pushed at `31d907ab` before any outcome implementation;
- 59 exact standard-library production checks using second-order rational jets and direct
  coordinate Ricci reconstruction;
- 44 implementation-distinct exact rational-function checks over the full interior `x` domain,
  with no production import or result read;
- 10/10 hostile mutations caught, including eigengap normalization, weighted metric form,
  curvature projector, irrational-flow classification, conformal sign, line-bundle topology,
  constraint promotion, and fibre-period promotion;
- full sufficiently small `C2` metric neighborhood covered analytically for the spectral-line
  result; no symmetry ansatz in that theorem;
- explicit nonhomogeneous U(2)-breaking toric metric counterfamily for fibration openness;
- no historical carrier, action, source, matter, mass, observation, scale, physical `X_max`, or
  protected local work.

## Four gates

1. **Preregistered:** yes, `31d907ab`.
2. **Full bounded space:** yes for the declared gap-open spatial metric neighborhood. The active
   constraint manifold and global evolution are explicitly not classified.
3. **Independent:** yes internally and by fresh external adversarial rederivation. The reviewer
   authenticated all 39 payloads, reproduced all four registered JSON artifacts byte-for-byte, and
   independently checked the weighted contact metric and Ricci eigenline.
4. **Premises:** audited in `PREMISE_LEDGER.tsv`; the response equation and Cauchy theorem retain
   their conditional/imported stamps.

Maximum present grade:

```text
DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_BOUNDED_GEOMETRIC_BOUNDARY
```

## Fresh external review

The sealed 41-file intake was authenticated without discrepancy. The reviewer reran all four
registered commands in a writable ephemeral copy; every regenerated JSON artifact was
byte-identical to its sealed counterpart. It independently rederived the common-bundle spectral
argument, weighted contact metric, exact Ricci eigenline, irrational-flow counterfamily, conformal
bump, and loss of G330's common-period normalization. It enforced the constraint boundary and
returned:

```text
ACCEPT__G331_BOUNDED_EIGENLINE_FIBRATION_BOUNDARY
```

The reviewer noted that two hostile mutations are shallow scope-flag flips. That is a limitation of
the mutation suite as a standalone guard, not a defect in the mathematical result, because those
same boundaries were checked directly in the independent derivation and fresh review.

## Open boundary

The next unresolved bridge is not another Fourier tile. It is whether the active vacuum constraint
manifold actually contains nearby nonsymmetric data whose metric Ricci line is irregular, or
whether the constraints impose additional orbit rigidity. No energetic/long-time stability,
occupancy, matter/mass, scale, or `X_max` result follows.
