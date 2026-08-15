# Preregistration — reciprocal-kernel release-candidate interface audit

Date: 2026-08-15  
Mode: bounded no-fit interface audit

## Whole question

Determine whether the current bounded kernel results form one coherent calculation:

```text
supplied complete coframe E=(B,Q,S)
+ supplied pair realization J=(Y,Z)
-> pair metric h
-> terminal (T_pair,L_pair,beta_pair,phi_pair,c_eff/c_E),
```

while separately retaining supplied endpoint-coframe transitions, including the restricted
`mu_lock` channel. Test exact reversal, matched-middle three-observer composition, live-channel
retention, and the type of the SNe-facing output.

This is not a fit, profile selection, action derivation, or new physical history law.

## Controlling sources

- G87: calibrated terminal-state composition and reversal.
- G89: full uncompressed `B,Q,S,Y,Z` pair evaluator and first variation.
- G90: overlap compatibility and all-instruments-live nonselection result.
- G92: endpoint-transition `mu_lock` crosswalk and pair-pullback separation.
- Native SNe replay: conditional `phi_pair=log(1+z)` retyping and frozen area/flux premises.
- G79: one same-geometry conditional redshift-plus-Jacobi-distance query.

## Type ledger

- ambient coframe `E`: `CONDITIONAL`, supplied regular chart representative;
- pair Jacobian `J`: `CONDITIONAL`, supplied regular query realization;
- pair metric `h=J^T E^T eta E J`: `DERIVED CONDITIONAL`;
- terminal pair coframe and reciprocal readout: `DERIVED CONDITIONAL` on regular `h`;
- ambient endpoint transition: `CONDITIONAL` on an explicit tangent-space carry;
- endpoint terminal transition: `DERIVED CONDITIONAL` from matched calibrated terminal states;
- redshift identification `1+z=exp(phi_pair)`: registered `CONDITIONAL READOUT`;
- Jacobi angular distance: `DERIVED CONDITIONAL` on a supplied null/screen query;
- luminosity/flux law: `CONDITIONAL`, not currently derived by the reciprocal kernel;
- physical history, pair family, and source population: `OPEN`.

## Required tests

### K1 — one exact complete pipeline

For three dense regular rational states, independently vary every block `B,Q,S,Y,Z`, form `E,J,h`,
reconstruct the unique terminal coframe, and verify the reciprocal endpoint identity without a
post-processing `mu` or orchestra correction.

### K2 — two distinct compositional structures

With a supplied common carry, test ambient transitions

```text
A_ij=E_j E_i^-1
```

and terminal transitions

```text
R_ij=Bpair_j Bpair_i^-1.
```

Both must compose and reverse exactly on a literally matched middle state. They must not be silently
identified with one another.

### K3 — reciprocal and `mu_lock` channel separation

Verify that the terminal character telescopes through `phi_pair`, while the restricted `mu_lock`
belongs to the ambient endpoint transition. Exercise an exact `S/Z` compensation that preserves
`h` but changes the ambient transition.

### K4 — all-channel retention

At a generic regular state, independently perturb `B,Q,S,Y,Z`. Every exact contribution to
`delta h` and `delta phi_pair` must be nonzero. This is a sensitivity test, not a dynamics or score.

### K5 — SNe interface ownership

Classify, without fitting:

```text
h -> phi_pair -> z,
screen Jacobi map -> d_A,
(z,d_A) -> flux/d_L/magnitude.
```

Identify which arrows are kernel-derived, query-conditional, observed, or still unowned. Audit the
existing SNe replay and G79 route for frozen profiles, compressed Gram use, old strain extraction,
or appended mixing corrections.

## Preregistered blockers

- `B-TYPE`: ambient endpoint arrow, terminal endpoint arrow, and pair pullback are conflated.
- `B-COMPOSE`: reversal or matched-middle composition fails in either declared groupoid.
- `B-KERNEL`: any `B,Q,S,Y,Z` channel is silently frozen or added after `phi_pair`.
- `B-MU`: `mu_lock` is appended to the terminal result or called its unique scalar.
- `B-SNE-Z`: the SNe code uses old strain depth instead of terminal `phi_pair`.
- `B-SNE-AREA`: the area/Jacobi output is absent or silently replaced by a scalar radial profile.
- `B-SNE-FLUX`: a conditional flux law is called metric-derived.
- `B-HISTORY`: an arbitrary all-active target history is called selected physics.

## Candidate landings

- `KERNEL_RELEASE_READY_FOR_FULL_SNE_VALIDATION` — every interface including native flux and physical
  history is owned. This is the strongest and least expected return.
- `KERNEL_COHERENT__GEOMETRIC_SNE_QUERY_READY_CONDITIONALLY` — kernel, composition, redshift, and
  screen-distance interfaces are coherent; physical history and/or flux remain explicit premises.
- `KERNEL_COHERENT__SNE_INTERFACE_BLOCKED` — internal kernel passes but a required geometry-facing
  SNe output is missing or mistyped.
- `KERNEL_INTERFACE_DEFECT` — one of K1--K4 fails.
- `MIXED`.

## Falsification and certification

All exact identities must be checked symbolically or by exact rational arithmetic. Load-bearing
claims require a separate no-import implementation and hostile mutations. Existing results may be
reused as provenance but not as the sole check. A fresh semantic adversary is still required for an
external grade.

## Maximum conclusion

At most, this audit may declare the conditional kernel interface ready for a geometry-level SNe
replay. It cannot select a physical history, derive the SNe flux/source law, improve a fit, infer
`X_max`, or claim cosmological validation.
