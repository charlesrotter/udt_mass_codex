# G317 audit report

Date: 2026-09-01
Status: `EXTERNALLY_ACCEPTED_BOUNDED__NO_SCIENTIFIC_DEFECT`

## Bounded landing

```text
EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES
__CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED
__NO_PHYSICAL_DATA_SELECTION
```

## What was established internally

- The registered non-CMC vector equation integrates exactly to
  `w'=p^6(tau-mean(tau))/2`, modulo the translation kernel.
- Pointwise scalar closure for nonconstant `tau` is necessary and sufficient exactly when the TT
  mean channel and connected scalar obey the registered relations.
- Physical reconstruction gives `gamma=p^4 delta`, mixed
  `K=diag(tau,q,-q)`, and `Lambda=-q^2`; both direct constraints vanish.
- The `q=0` subclass has zero initial Weyl data, while `q!=0` has the invariant witness
  `E_x^x=2q^2/3`.
- Arbitrary smooth periodic nonconstant `tau`, positive `p`, and continuous `q` remain. The
  construction interlocks fields but selects no member.

## Executable evidence

- 1,637 dependency-free production assertions;
- 1,191 implementation-distinct dependency-free assertions;
- 29 of 29 hostile mutations caught;
- 48 registered family instances across three Fourier-profile classes;
- 14-row solution-space atlas.

The exact 299-row current premise registry passes its verifier. The full repository regression
suite passes with `214 passed, 1 known xfailed`.

## Scope and remaining work

This is a full classification only of the declared exact ansatz. General non-CMC construction,
nonconstant conformal factor, nonflat or nondiagonal seeds, boundaries/asymptotics, global
development, topology population, scalar magnitude, calibrated scale, source, matter/mass,
observations, and physical `X_max` remain open.

The fresh zero-context `gpt-5.4` reviewer authenticated all 34 manifest payloads, reran all four
registered commands, reproduced all five generated artifacts byte-for-byte, independently
rederived every load-bearing equation and tide classification, and found no scientific defect.
Its verdict was:

```text
G317_ACCEPTED__EXACT_NONCMC_INTERLOCK_AND_TIDE_SPLIT_UPHELD
```

The externally accepted grade remains bounded to the declared ansatz and selects no physical data.
