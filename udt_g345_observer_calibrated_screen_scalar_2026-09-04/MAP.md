# G345 map — observer-calibrated endpoint screen scalar

Date: 2026-09-04
Status: preregistration stage

## Whole question

Starting only from G340's metric-owned normal-observer endpoint frequencies and G344's
affine-weighted mixed-Hessian screen bidensity, does the supplied metric already provide enough
endpoint structure to form an affine-gauge-invariant and screen-coordinate-invariant scalar on
each fixed labelled null ray? If so, how does that scalar reverse, compose through an intermediate
endpoint, behave at coincidence and both principal directions, and transform between separately
unit-frequency endpoint conventions?

This is `METRIC_LED` and observing rather than targeting. It tests a typed contraction of two
already-derived metric objects. It does not add a light model, flux law, detector, probability,
distance convention, path population, source, action, scale, or observational datum.

## Exact bounded arena

Use one supplied G323/G324 Taub/Kasner spacetime, its supplied normal-observer congruence, one
supplied fixed labelled G340--G344 null ray and compact lift, arbitrary distinct positive endpoint
times, all projective ray directions including both principal limits, and the complete G344
two-screen endpoint generator. Every common positive affine rescaling, every admissible marked ray
event, and arbitrary invertible passive endpoint screen-coordinate changes remain live.

At endpoint `i`, let

```text
omega_i = -g(k,n_i) > 0
```

be G340's metric-measured ray frequency for the supplied normal observer, let `q_i` be the
metric-induced positive screen metric, and let `K_10=B_10^-T` and
`Delta_10=abs(det K_10)` be the G344 mixed Hessian and its orthonormal-screen coefficient.

The candidate is not selected for observational usefulness. It is the minimal contraction whose
affine and screen weights can be balanced by the endpoint structures already present in the
metric.

## Candidate object to test

In orthonormal endpoint screens, freeze

```text
Khat_10 = K_10 / sqrt(omega_1 omega_0),
Dhat_10 = abs(det Khat_10)
          = Delta_10 / (omega_1 omega_0).
```

In arbitrary screen coordinates, test the intrinsic determinant norm

```text
Dhat_10 = abs(det K_10)
          / (omega_1 omega_0 sqrt(det q_1 det q_0)).
```

For stationary composition, freeze the candidate joined-endpoint scalar

```text
hhat_1 = abs(det(H_1 / omega_1)) / det(q_1)
```

and test, rather than assume,

```text
Dhat_20 = Dhat_21 Dhat_10 / hhat_1.
```

Naive multiplicativity without the stationary Hessian is an explicit hostile alternative, not an
allowed repair.

## Pure and easy routes

- Pure route used here: balance the derived affine weights with the derived endpoint frequencies;
  contract the endpoint screen covector determinants with metric screen area; then derive every
  covariance and composition rule from G340/G343/G344.
- Easier but forbidden as proof: quote a luminosity-distance, Etherington, Van Vleck, geometric
  optics, probability, or quantum-propagator formula and identify the result by familiarity.

## Required classifications

1. Classify every monomial `Delta omega_0^a omega_1^b`; determine whether common-affine invariance
   plus endpoint-reversal symmetry fixes `a=b=-1` when the determinant occurs to first power.
2. Prove or refute invariance of `Dhat` under common affine rescaling, marked-event conversion, and
   arbitrary invertible endpoint screen-coordinate changes when the metric screen areas are kept.
3. Prove or refute equality under common-affine reversal and under separately unit-frequency
   source conventions using G343's exact endpoint frequency ratio.
4. Derive the correctly typed stationary-composition law for every nonidentity endpoint triple and
   explicitly reject bare multiplication.
5. Eliminate reference-event and affine variables from the mixed-direction formula if possible;
   recover exact longitudinal and transverse principal limits and the coincidence singularity.
6. Retain every compact lift separately. No sum, weight, preferred route, or physical population
   may appear.
7. State exactly what remains observer-, ray-, path-, and spacetime-dependent. Coordinate-scalar
   status must not be promoted to a unique physical observable.

## Maximum conclusion

At most G345 may derive one observer-calibrated endpoint screen determinant scalar, unique only in
the explicitly classified symmetric first-power monomial class, on the supplied G340--G344
spacetime, normal observers, and fixed labelled rays. It may not establish luminosity, flux,
probability, amplitude, observational distance, a native theory of light, route or observer
population, a generic spacetime theorem, stability, matter/mass, a physical scale, `X_max`, or
canon.
