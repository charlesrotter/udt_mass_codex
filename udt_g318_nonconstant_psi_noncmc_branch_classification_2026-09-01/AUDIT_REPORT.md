# G318 audit report

Date: 2026-09-01
Status: `EXTERNALLY_ACCEPTED_BOUNDED`

## Bounded landing

```text
NONCONSTANT_PSI_FORCES_A_POWER_LAW_NONCMC_INTERLOCK
__G317_DIRECT_FORM_IS_OBSTRUCTED
__POSITIVE_PERIODIC_TIDAL_BRANCH_EXISTS
__NO_PHYSICAL_DATA_SELECTION
```

## What was established

- Freeing `psi` obstructs the unchanged G317 `K=diag(tau,q,-q)` form in the registered
  sign-definite nonconstant branch.
- Constant-ratio separability instead forces `tau=C psi^n`, with the TT mean and longitudinal
  derivative fixed by periodic descent.
- The conformal and direct physical constraints independently give the same full nonlinear scalar
  ODE.
- Nonnegative-`Lambda` periodic branches with `n<=-3` are obstructed in this family, while an
  `n=-2` strict-center class has positive nonconstant periodic solutions.
- Direct electric and magnetic Weyl reconstruction proves the registered periodic family is tidal.
- The conformal orbit and all construction parameters remain free or interlocked, not selected.

## Executable evidence

- 14,043 dependency-free exact production assertions;
- 4,440 implementation-distinct tensor assertions;
- 48 of 48 hostile mutations caught;
- 27 independent Weyl reconstructions;
- 16-row branch atlas and four strict-center witnesses.

## Scope and remaining work

This is a full classification only of the declared sign-definite constant-ratio separability
family. Nonseparable, sign-changing, nonflat, nondiagonal, multidimensional, boundary/asymptotic,
low-regularity, full-evolution, and global-completion sectors remain open. No physical data,
history, topology, population, scalar magnitude, scale, source, matter/mass law, observation, fit,
or physical `X_max` is selected. Metric, kernel, angular cancellation, and observational interfaces
are unchanged.

## External adversarial review

The fresh `gpt-5.4` reviewer authenticated all 33 manifest payloads, reproduced the five generated
artifacts byte-for-byte, independently rederived the load-bearing constraints and Weyl tensors, and
accepted the bounded landing without repair:

```text
G318_ACCEPTED__NONCONSTANT_PSI_BRANCHING_AND_TIDAL_PERIODIC_FAMILY_UPHELD
```

The accepted scope remains the declared diagnostic family. It is not a general non-CMC theorem and
does not select physical data or a universe.
