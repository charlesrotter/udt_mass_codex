# G301 audit report

Date: 2026-08-30

## Primary internal landing

```text
TWO_INEQUIVALENT_FULL_METRIC_QUIET_PRINCIPAL_CLASSES_SURVIVE
__GENERIC_RICCI_FLAT_AND_TRACEFREE_RICCI_WITH_ONE_CONSTANT_SCALAR_DATUM
```

Initial fresh review selected `INTERNAL_CERTIFICATION_FAILURE` while retaining the mathematics.
After preregistered repairs R1--R5, the repair-only reviewer returned `ACCEPT_REPAIRS` and found no
remaining defect inside the repair scope.

## What was established

- Differentiability at the flat curvature origin plus exact positive weight-one homogeneity forces
  a candidate two-jet residual to be exactly linear in curvature.
- In the frozen unoriented natural symmetric rank-two lane, the residual is
  `a Ric_ab + b R g_ab`.
- All coefficients with `a != 0` and `a+4b != 0` are related by an invertible trace adjustment and
  form one Ricci-flat residual-equivalence class.
- `a+4b=0` is an inequivalent trace-free Ricci class. Bianchi carry fixes its scalar curvature to
  one connected-region constant but does not force that constant to zero.
- At nonzero quiet frequency the trace-free class reduces to the same Ricci-flat principal
  equations. Its difference is a zero-mode/integration datum, not an extra local polarization.
- The scalar-only and identity-zero strata fail preregistered gates.
- Identity divergence freedom would select the generic class, but remains an unowned G259
  candidate premise.

## Executable evidence

- Production: 169 exact coefficient-grid cases, 7,880 exact generic inversions, 4,000 principal
  covectors, and 27,829 assertions.
- Independent coefficient-strata replay: 12,000 random rational cases and 49,609 assertions,
  importing no production function. This replay is explicitly conditional on the two-term basis.
- Independent full-space basis census: begins with the 20-dimensional algebraic-curvature space
  and an arbitrary 200-component map to symmetric two-tensors. Six Lorentz generators give 1,200
  equivariance rows of rank 198 under two primes; Ricci and scalar-times-metric are two exact
  independent integer null vectors. It passes 53,605 assertions and imports no production code.
- Hostile catches: 12 of 12 registered mutation and semantic catches pass.
- All four registered G301 replays pass under dependency-free `python3 -S`.
- After the current startup block was compacted from 973 to 848 words without changing scientific
  content, the repository-wide harness reports 197 passed and one expected xfail. The package and
  startup surface are green for banking.

## Four evidence gates

1. **Preregistered:** yes, commit `accfc6b9` was pushed before production outcomes.
2. **Full space or justified scope:** exact coefficient-stratum classification inside the bounded
   rank-two two-jet lane; global/nonlocal and other tensor types remain explicitly open.
3. **Independent verification:** the downstream coefficient replay agrees, the repair adds a
   full-space Lorentz-intertwiner census of the load-bearing basis, and a fresh repair-only
   external reviewer reran all registered checks and returned `ACCEPT_REPAIRS`.
4. **Premise audit:** every class hypothesis remains explicitly candidate/free-and-explored; no
   field equation or UDT law was adopted.

## Scientific boundary

The result narrows a local candidate-law class. It neither selects the UDT dynamics nor derives
the loud regimes. It does not alter the metric, complete pair pullback, reciprocal kernel, angular
cancellation, W5/W6, observations, sources, or `X_max`.
