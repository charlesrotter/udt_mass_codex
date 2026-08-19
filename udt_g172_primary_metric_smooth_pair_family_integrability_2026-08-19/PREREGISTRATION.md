# G172 preregistration — smooth primary-metric pair-family integrability

Date: 2026-08-19
Mode: metric-led exact classification, no fit and no selected angular profile

## Question

Does the G171 metric-native local reciprocal response assemble smoothly and reversibly along the
entire bounded class of time-orthogonal pair families with nonzero radial component? What is the
first exact obstruction to extending such a family?

## Frozen inputs

Only the 11 sources in `SOURCE_MANIFEST.tsv` may control the derivation. G142--G160, observational
outcomes, and protected local work are excluded.

## Preregistered outcomes

Exactly one primary landing will be selected:

1. `SMOOTH_FAMILY_CLOSURE`: every family in the declared bounded class has a smooth regular
   metric-native scalar response throughout the supplied metric interval, with exact reversal and
   telescoping inside that family.
2. `BOUNDED_SUBCLASS_CLOSURE_ONLY`: closure holds only after an additional precisely stated
   restriction within the registered class.
3. `FROBENIUS_OR_CALIBRATION_OBSTRUCTION`: the metric and areal-radius calibration do not suffice
   to integrate generic registered germs or define a coherent terminal response.
4. `TYPE_OR_REGULARITY_FAILURE`: the proposed family is not a lawful pullback construction.

## Exact derivation contract

1. Use the invariant spherical form

   ```text
   g=-exp(-2 phi) dx0^2+exp(2 phi) dr^2+r^2 gamma_S2.
   ```

2. For `F(x0,r)=(x0,r,gamma(r))`, derive `h`, `det(h)`, `Phi`, conditional `c_eff/c_E`, and the
   endpoint difference without dropping the angular Gram.
3. Retain the entire free angular curve only through the invariant speed
   `a2(r)=gamma_S2(gamma'(r),gamma'(r))`; do not choose a melody or coefficient.
4. Prove local integrability by the explicit immersion and, independently, by Frobenius closure of
   the static time direction with a time-independent spatial separation field.
5. Classify regularity and extendability on an arbitrary connected interval inside the supplied
   primary-metric domain.
6. Recover the radial family exactly at `a2=0`.
7. Classify the `r->0+` limit without promoting the spherical chart limit to a smooth-center
   theorem.
8. Expose the effects of radial reparameterization and prove why areal-radius calibration is
   available only when `dr(s)!=0`.

## Solution-space and catch contract

The computation must characterize, not filter, arbitrary smooth nonnegative angular-speed data.
It must catch or expose:

- dropping the `r^2 a2` angular term;
- replacing the full angular speed by a fitted constant;
- claiming reparameterization invariance without calibration;
- inserting `X_max` or a chosen `phi(r)` profile;
- treating the explicit pair surface as a preferred physical path;
- widening monotone-radial closure to turning or pure-angular strata;
- calling a finite-interval theorem global completion;
- reintroducing G142--G160 carry/score/history machinery;
- calling scalar telescoping complete non-scalar transport closure.

## Certification contract

- exact symbolic derivation;
- independent standard-library numerical/rational replay over at least 10,000 regular samples;
- at least ten algebraic/semantic mutation catches;
- all 11 frozen source hashes checked against the preregistration commit;
- repository premise verifier and full regression tests pass;
- fresh external adversarial review before any `VERIFIED` grade.

## Maximum conclusion

At most, G172 may classify the smooth scalar response and first obstruction for the registered
time-orthogonal monotone-areal-radius family inside the declared primary static-spherical metric.
It cannot select the physical angular curve or pair family, derive a general ambient/time-live
kernel, prove global completion, define positive metric-space distance, or infer `X_max`, dynamics,
observations, matter, source, action, signalling, or canon.
