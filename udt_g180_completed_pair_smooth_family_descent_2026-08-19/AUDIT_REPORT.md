# G180 audit report — completed-pair smooth-family descent

Date: 2026-08-19

## Primary result

G180 reaches the preregistered landing:

```text
COMPLETED_PAIR_SMOOTH_FAMILY_DESCENT__ORCHESTRA_ENTERS_THE_PHYSICAL_TAPE_MAP
```

On every supplied connected smooth regular pair family, the already derived density

\[
m(\sigma)=\sqrt{-\det h_\sigma(\sigma)}
\]

is smooth and positive. Its integral defines one completed ruler coordinate up to origin and
orientation. In that coordinate, the full pair metric has determinant `-1`, reciprocal clock/ruler
factors, retained shift, and

\[
\Phi=-\frac12\log(-h_{00}).
\]

No extra scalar or carry rule is required.

## Primary-metric orchestra result

For

\[
F(x^0,\sigma)=(x^0,r(\sigma),\gamma(\sigma)),
\]

the complete metric gives

\[
\frac{ds}{d\sigma}
=\sqrt{v^2+e^{-2\phi}r^2b^2},
\qquad
\Phi(s)=\phi(r(s)).
\]

Thus the angular sector changes the physical tape and the map from separation to areal radius. It
does not need a post-readout angular correction. Radial turns and pure-angular segments remain
regular whenever the complete spatial tangent is nonzero.

## What changed

G172's angular logarithm remains correct for its arbitrary areal-radius calibration, but is now
regraded as a control readout. In the completed reciprocal pair, the same angular factor belongs to
the ruler density. This also removes the old conformal-blindness concern inside the completed
kernel: a common metric scale changes both the tape and completed depth. The supplied common-scale
profile is still not selected by this theorem.

## Evidence

- preregistration commit: `ae24ebbc`;
- generic interval proof and primary exact specialization;
- 29/29 production symbolic checks;
- 20,000 independent exact-rational families and 341,579 assertions;
- 1,461 turning, 1,461 pure-angular, and 118 radial independent controls;
- nine frozen source hashes match.

## Scientific grade and ceiling

`DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS_PENDING_FRESH_ADVERSARIAL_REVIEW`

The result is conditional on the working completed-pair clarification and on a supplied smooth
regular family. It does not select events or families, prove a positive metric-space distance,
globalize across singularities or branches, close non-scalar transport, derive `X_max`, or validate
observations or dynamics.
