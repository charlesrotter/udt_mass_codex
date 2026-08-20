# G189 preregistration — P1-free metric/flux interface

Date: 2026-08-20

## Whole question

On the bounded regular central-static-spherical observer query, can the accepted completed-pair
kernel, metric-derived Jacobi screen, and the already authorized temporary transparent-transfer
bridge produce a supernova magnitude curve without the frozen P1 radius-frequency profile?

This is a metric-led interface and no-shape-fit test. It is not a derivation of electromagnetism,
a physical metric history, `X_max`, or a general cosmology.

## Premise ledger

- `pinned-by-THEORY / DERIVED_CONDITIONAL`: the primary metric
  `ds^2=-c_E^2 exp(-2 phi)dt^2+exp(2 phi)dr^2+r^2 dOmega^2` on a supplied smooth regular profile.
- `pinned-by-THEORY / DERIVED_CONDITIONAL`: for static source and observer on one regular radial
  null branch, conserved `k_t` gives `Z=omega_s/omega_o=exp(phi_s-phi_o)`.
- `pinned-by-THEORY / DERIVED_CONDITIONAL`: G119/G188 give
  `d_A^2=abs(det D_sky)=R^2` in the central spherical specialization.
- `pinned-by-OBSERVED_QUERY`: Pantheon+ uses the frozen release cut and `Z=1+zCMB`; DES-SN5YR
  uses the frozen `IDSURVEY=10` cut and `Z=1+zHD`. These are conditional frequency-slot adoptions,
  not metric derivations.
- `pinned-by-CHARLES / IMPORTED_CONDITIONAL`: transparent conserved null cargo,
  `eta=1`, `epsilon=1/Z`, hence `d_L=Z^2 d_A` on the declared regular branch.
- `CHOSE/PROVISIONAL_CONTROL`: test the simplest normalized-position/screen join
  `R=R0 chi`, where `chi=tanh(phi)` and the constant `R0>0` is absorbed only by the usual catalog
  magnitude zero point. This join is not preregistered as derived.
- `FROZEN_REFERENCE_ONLY`: P1 with `n=1.0559332414320268` supplies comparison scores only. It is
  forbidden from entering the new curve.
- `pinned-by-HABIT`: none.

## Exact candidate

Set the observer zero `phi_o=0`. On the declared query,

```text
phi=log Z,
chi=tanh(log Z)=(Z^2-1)/(Z^2+1),
d_L/R0=Z^2 chi.
```

Only one additive magnitude offset is analytically profiled per catalog. No shape parameter,
optimizer, redshift switch, angular coefficient, `X_max`, or P1 value may enter this candidate.

## Exact ownership test

The derivation must also prove the general profile identity

```text
d_L(Z)=Z^2 phi^{-1}(log Z+phi_o)
```

on every monotone static branch. It must exhibit two smooth profiles with the same coincidence
value and slope but different finite curves, proving that the metric form alone does not select
`R(Z)`. It must identify P1 exactly as the particular profile

```text
phi_P1(R)=-(n/2) log(1-R/(n X_eff)).
```

## Observational classification fixed before evaluation

Let `N_P=1367`, `N_D=1623`, with one profiled offset. Define the conservative no-large-residual
ceilings

```text
C_P=(N_P-1)+5 sqrt(2(N_P-1)),
C_D=(N_D-1)+5 sqrt(2(N_D-1)).
```

Classify:

1. `COEFFICIENT_FREE_P1_REPLACEMENT_LEAD` only if both new chi-squares are no more than 25 above
   their frozen P1 values.
2. `P1_FREE_JOIN_DATA_COMPATIBLE_BUT_NOT_P1_LEVEL` if both lie below `C_P,C_D` but condition 1 fails.
3. `R_PROPORTIONAL_CHI_JOIN_REJECTED_IN_DECLARED_SNE_INTERFACE` if either exceeds its ceiling.

These labels concern only the provisional `R=R0 chi` join under imported transfer. They cannot
reject the reciprocal kernel or prove a native flux law.

## Certification contract

- verify all frozen source hashes;
- exact symbolic redshift, screen, transfer, inverse-profile, P1-profile, and nonselection checks;
- production Cholesky likelihood replay on both catalogs;
- implementation-distinct precision-domain replay using a Pantheon precision solve and DES Schur
  complement;
- assert no shape optimizer, P1 candidate call, post-readout angular factor, or `X_max` use;
- add mutation catches for deleting the screen, changing the transfer exponent, replacing `chi`
  by P1, and silently fitting a shape coefficient;
- rerun the current premise verifier and repository tests before banking.

## Omitted scope

Nonspherical/displaced sources, multiple images, caustics, absorption, scattering, source
evolution, bandpass, intrinsic-luminosity populations, physical ray population, time-live history,
global completion, BAO, CMB, action, source, matter, bootstrap, mass, and signalling are omitted.

## Maximum conclusion

At most G189 can classify whether the already adopted dimensionless position `chi`, joined
provisionally to the central areal screen with one absorbed scale, is a P1-free SNe shape lead. It
can close the algebraic metric-to-flux interface conditionally and localize any remaining P1 role
to the `phi(R)` profile. It cannot promote the provisional join or imported transfer to canon.
