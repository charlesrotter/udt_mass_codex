# G267 preregistration

Date: 2026-08-26

## Question

If `M=sech(delta)` is provisionally supplied as the physical mutual-clock projection on the G266
kernel, does it:

1. follow uniquely from existing UDT premises and close physical distance/history;
2. require a new premise but then close a coefficient-free compact pair state and physical
   distance/history;
3. require a new premise and close a coefficient-free compact pair state while distance/history
   remain open;
4. fail reversal, composition, or compatibility with the signed clock arrow?

## Alternatives fixed before outcome algebra

- `A__SECH_UNIQUELY_DERIVED_AND_CLOSES_DISTANCE_HISTORY`
- `B__SECH_NEW_PREMISE_CLOSES_COMPACT_PAIR_STATE_AND_DISTANCE_HISTORY`
- `C__SECH_NEW_PREMISE_CLOSES_COMPACT_PAIR_STATE__DISTANCE_AND_HISTORY_OPEN`
- `D__SECH_INCONSISTENT_WITH_SIGNED_RECIPROCAL_KERNEL`

## Required exact checks

1. Derive or refute `M^2+chi^2=1` from `M=sech(delta)` and `chi=tanh(delta)`.
2. Determine whether `(M,chi)` reconstructs `Gamma`, `Xi`, `r`, and `delta` on finite depth.
3. Verify reversal: `M` even and `chi` odd.
4. Derive the exact two-channel composition law for `(M,chi)` and verify identity, inverse, and
   associativity through its equivalence with additive depth.
5. Prove by an exact counterexample whether `M` alone can compose without the sign of `chi`.
6. Derive the exact differential interlock and quiet-point jets. Check whether the candidate has no
   linear mutual effect at `delta=0` and is symmetric at the two loud ends.
7. Compare `1/Gamma` against at least two other positive, normalized, coefficient-free smooth
   functions of `Gamma` admitted by F1--F4, W1, W4, and G266.
8. Determine whether supplying the projection rejects any smooth valued metric history or merely
   evaluates every supplied `delta` history.
9. Determine exactly what separation information `M` owns: signed depth, absolute depth,
   dimensionless position, dimensionful distance, or none.
10. Keep the one-way signed redshift/clock arrow distinct from the mutual projection.

## Certification and falsification contract

- Exact algebra must close symbolically or by exact rational identities after denominator clearing.
- A separate implementation must not import the production derivation or read its result and must
  cover deterministic rational points on the right unit semicircle plus exact composition cases.
- Mutation catches must reject: a linear quiet mutual term, reversal-odd `M`, composition without
  signed `chi`, `M` confused with `r`, uniqueness inferred from evenness alone, dimensionful
  distance inferred from a dimensionless state, and history selection inferred from evaluation.
- Landing `A` requires an already-owned premise to select `1/Gamma` and a distance/history law.
- Landing `B` requires the newly supplied candidate to reject at least one previously admitted
  history and to own a dimensionful distance protocol.
- Landing `C` applies if the candidate gives a coherent coefficient-free compact pair state but
  remains a supplied projection that evaluates arbitrary histories and fixes no absolute distance.
- Landing `D` requires an actual failure of reversal or two-channel composition.

## Maximum conclusion

Bounded candidate-consequence classification only. No canonization, observational calibration,
distance scale, `X_max`, field equation, profile, source, history, or signalling claim.
