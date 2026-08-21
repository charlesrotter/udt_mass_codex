# G199 audit report — primary-metric bidirectional radial null response

Date: 2026-08-21

## Landing

```text
PRIMARY_METRIC_RADIAL_NULL_PAIR_IS_REVERSAL_SYMMETRIC
__NO_NATIVE_CHIRAL_SPLIT
__G198_ASYMMETRY_REMAINS_CHOSEN_COMPLETE_COFRAME_CONTROL
```

Grade: `INDEPENDENTLY_VERIFIED_WITH_CAVEATS`

## Result first

The primary static-spherical UDT metric does **not** contain G198's outgoing-loud/incoming-quiet
screen split.  Its two radial null germs are related by ruler reversal and obey the same local
frequency and screen laws.

For

\[
g=-f(dx^0)^2+f^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

the source-normalized future radial tangents are

\[
k_\pm=\frac{\sqrt{f_o}}{f}\partial_0
\pm\sqrt{f_o}\partial_r.
\]

Both are affine.  Both give

\[
Z_{o\to s}=\sqrt{f_o/f_s}=e^{\phi_s-\phi_o}.
\]

Both angular screen bases are parallel, both radial screen tidal matrices vanish, and both
vertex-normalized finite maps are

\[
\mathcal D_\pm(\lambda)=\lambda I.
\]

The zero optical tide is a nontrivial cancellation: all 2,000 independent exact-rational controls
had nonzero ambient curvature.

## What this corrects

The G191 preregistration explicitly stamped its `deta+dz` coframe architecture
`CHOSE_MATHEMATICAL_FUNCTION_FAMILY`.  G192--G196 enlarged that same family, and G198 correctly
derived the response of its opposite germ.  The resulting asymmetry is real for that metric, but
it is not evidence that the primary UDT metric natively chooses one null orientation as loud and
the other as quiet.

The proposed arbitrary `C_eta,C_z` extension is therefore not the next metric-native move.  It
would characterize a larger configuration envelope.  Any physical directional asymmetry must
instead emerge from a derived nonspherical/time-live UDT metric or from endpoint/branch sampling,
not from inserting the missing opposite coefficient by hand.

## What remains active

- The radial reciprocal frequency law remains active and is fixed by the same \(\phi\) history.
- The areal screen remains active; at a regular calibrated center the outgoing limit recovers
  \(d_A=r\).
- Nonradial rays retain G187's two metric-derived tidal modes and generic shear.
- G188 remains the correct full-matrix evaluator for any supplied genuinely complete metric.

Thus G199 does not turn off the orchestra.  It identifies the strict radial primary-metric chord
as a symmetry locus and removes a chosen chiral witness from the native kernel spine.

## Evidence

- preregistered and pushed at commit `1514ed99` before confirmatory implementation;
- 65/65 exact symbolic assertions from a direct inverse-metric, Christoffel, Riemann, screen, and
  Jacobi reconstruction;
- 2,000 independent exact-`Fraction` metric two-jet controls, all nonflat;
- 60,000 independent assertions and 2,000 opposite-sign comparisons;
- no production import or production artifact in the independent replay;
- hostile mutation catches, source hashes, no-write package replay, premise verifier, repository
  tests, and diff checks recorded in `EVIDENCE_GATES.md`.

## Four gates

1. Preregistered: yes.
2. Full or bounded: full for both radial null germs on every smooth positive local primary-metric
   jet with `r>0`; nonradial and generalized ambient metrics are excluded.
3. Independent: yes, exact-rational metric two-jet reconstruction.
4. Premises: audited; the only physical clarification is the already registered completed-pair
   Dual Reciprocity premise.

## Maximum conclusion

The declared primary static-spherical metric owns a reversal-symmetric two-direction radial null
response.  G198's chiral split is a valid conditional response of its chosen complete-coframe
family, not a primary-metric result.  G199 does not choose \(\phi(r)\), construct a full time-live
cosmology, or derive observational transfer.
