# Preregistration endpoint-type correction

Date: 2026-08-15

Recorded after the first primary symbolic execution and before saving or banking a derivation
result. No BAO curve, descriptor, covariance, singular vector, or feature location was read.

## Category error caught

The first preregistration used one local pair matrix `V_a` both to construct the sky direction at
the observer and to compute the observer--source redshift. Those are not generally the same
evaluation:

- the sky direction is the oriented positive pair-ruler tangent at the observer endpoint;
- the redshift is the accumulated reciprocal depth between the observer and source endpoints.

They belong to the same full pair-relation branch but need not be functions of the same local
matrix. Equating them would silently collapse endpoint carry into an observer-local snapshot.

## Correction

Use `V_a^O,h_a^O` only for the common-observer direction. Carry a separately typed terminal scalar

```text
DeltaPhi_a=phi_pair(q_a)-phi_pair(O),
Zobs_a=exp(DeltaPhi_a),
```

on that same pair-relation label. G99 conditionally supplies the middle-regime `Zobs` identification;
the physical relation/history that generates the endpoint carry remains open.

The first symbolic script must be revised and rerun. Its local `phi_argument` witness may remain an
algebra check, but it may not be called the source redshift. The maximum landing gains
`ENDPOINT_DEPTH_CARRY_CONDITIONAL`.

This is a type correction, not numerical retuning. It changes no synthetic angle, pair-count
fixture, bin, estimator, tolerance, observational input, or source-law conclusion.
