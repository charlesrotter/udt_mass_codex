# Exact derivation — `lambda` certificate intervals

## 1. Fixed complete slice

Use the parent complete `R x S3` metric with `phi=f/50`, `a=1/64`, `R=1`, and arbitrary real
`lambda`. At the north event, define

```text
D(lambda)=det[dI1,dI2,dI3],
```

using scalar curvature, Ricci squared, and Kretschmann scalar of the complete four-metric.

The four premise stamps remain:

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

They do not enter the polynomial calculation.

## 2. Why the determinant is a polynomial

At the certificate event, `phi=0`. An order-`n` spatial derivative of
`exp(lambda phi)` is polynomial in `lambda` of degree at most `n`. A first gradient of a curvature
scalar uses the metric three-jet, so each of the nine entries in the `3 x 3` gradient matrix has
degree at most three. Its determinant therefore has degree at most nine.

Exact rational metric-jet evaluations at the ten preregistered integer nodes uniquely reconstruct
that polynomial. Seven additional exact rational holdouts all agree. The two highest reconstructed
coefficients vanish, so the actual degree is seven.

Up to its positive denominator, the exact polynomial is

```text
P(lambda) =
  543066446569033728 lambda^7
  + 25984556589396660224 lambda^6
  - 2573065782025855974852 lambda^5
  - 26008130030205351622456 lambda^4
  + 154264432976904187713665 lambda^3
  - 215812777468162263903826 lambda^2
  + 76052330196388598500442 lambda
  - 4749545519575013079625,

D(lambda)=P(lambda)/12800000000000000000000.
```

The exact ascending rational coefficients are preserved in `POLYNOMIAL_COEFFICIENTS.tsv`.

## 3. Complete real-root census

Exact rational isolation gives seven distinct simple real roots:

| root | approximate `lambda` | multiplicity |
|---|---:|---:|
| R01 | -92.9285479653 | 1 |
| R02 | -13.6287179277 | 1 |
| R03 | 0.0792964331 | 1 |
| R04 | 0.4106917200 | 1 |
| R05 | 1.6106372544 | 1 |
| R06 | 2.4299527417 | 1 |
| R07 | 54.1788474775 | 1 |

`REAL_ROOTS.tsv` contains exact rational isolating bounds. An independent standard-library
`Fraction` Sturm sequence proves that the polynomial is square-free, that it has exactly seven
distinct real roots, and that every registered bracket contains exactly one.

Because all roots are simple, the determinant sign alternates across the eight intervals:

```text
negative, positive, negative, positive,
negative, positive, negative, positive.
```

All other registered gates are independent of `lambda` on this frozen slice and remain strictly
positive throughout the real axis.

## 4. Existing-center assignments

- C01 (`lambda=-2`), C02 (`-1`), and C03 (`0`) share I03, between R02 and R03.
- C04 (`1/2`) and C05 (`1`) share I05, between R04 and R05.
- C06 (`2`) lies in I06, between R05 and R06.

Thus the previously sampled centers occupy three connected intervals of this one-dimensional
certificate atlas. C03 and C04 are separated by two certificate roots and the intervening I04;
C05 and C06 are separated by R05.

## 5. Cross-method geometry replay

The independently implemented Torch/autodiff full-Riemann geometry evaluated five preregistered
non-node values. All five agree with the exact polynomial under the inherited frozen tolerance. The
maximum absolute determinant error is `3.410605131648481e-13`; the maximum scaled error is
`4.951594689828198e-14`.

The exact polynomial and Sturm calculation control the root verdict. Torch is a separate geometry
check, not a root-isolation authority.

## 6. Exact interpretation boundary

At a root, this fixed set of three invariant gradients loses rank at this fixed event. The depth,
twist, slice, and coframe do not fail. Therefore the root is not by itself evidence of:

- loss of the intrinsic clock line;
- extra symmetry;
- a metric singularity;
- a physical phase boundary; or
- selection of a preferred `lambda`.

It partitions the certified one-dimensional atlas. Whether the underlying intrinsic-pair geometry
continues through a root must be tested using other events, invariants, or the Killing system itself.

## 7. Bounded verdict

```text
THE_FROZEN_COMPLETE_S3_LAMBDA_SLICE_IS_PARTITIONED_INTO_EXACT_CERTIFICATE_COMPONENT_INTERVALS;
C01_TO_C06_HAVE_EXACT_INTERVAL_ASSIGNMENTS;
CERTIFICATE_DEGENERATION_POINTS_ARE_MAPPED;
NO_FULL_CONFIGURATION_COMPONENT_OR_PHYSICAL_LAMBDA_SELECTION_IS_DERIVED.
```
