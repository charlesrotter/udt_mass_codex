# Preregistration — reduced-holonomy condition audit

Date: 2026-07-27

Base: `1c91169976e3d189dfe0cf1fe5402875459af73f`

Question type: **METRIC-LED EXACT CARTAN CONDITION MAP**.

## Whole question

Within the complete stationary twisted-`S3` coframe, what exact conditions make the intrinsic
reciprocal-screen grading parallel and hence reduce ordinary Levi-Civita holonomy to its stabilizer?
Do any nonconstant, nondegenerate, complete finite-cell branches survive?

This is not a search for a preferred `lambda`.  Every algebraic stratum is retained.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

No co-presence, signalling, action, source, carrier, density, or field equation enters.

## Metric universe

Work on `R_t x S3` with

```text
theta0=e^-phi(dt+a sigma3)
theta1=e^+phi sigma3
theta2=e^(lambda phi) sigma1
theta3=e^(lambda phi) sigma2
g=-(theta0)^2+(theta1)^2+(theta2)^2+(theta3)^2
d sigma1=kappa sigma2 wedge sigma3, cyclically
kappa=-2.
```

Explore `a` as a constant including zero, `lambda` as symbolic real with separate strata
`lambda=+1`, `lambda=-1`, and generic `lambda != +/-1`, and `phi` as an arbitrary smooth stationary
real function.  Exponentials are finite and positive on the regular cell.

Write

```text
dphi=p1 theta1+p2 theta2+p3 theta3,
A=a kappa exp[-(1+2lambda)phi],
B=kappa exp[(1-2lambda)phi],
C=kappa exp[-phi].
```

For a regular nondegenerate `S3`, `B` and `C` cannot vanish.  `A=0` is equivalent to `a=0`.

## Object and stabilizer strata

Use

```text
X_lambda=diag(-1,+1,lambda,lambda).
```

The previously derived connected stabilizer algebras are frozen:

```text
generic lambda: screen so(2)
lambda=+1:      spatial so(3)
lambda=-1:      so(1,2) on clock plus screen
```

For the intrinsic grading, ordinary endpoint closure requires

```text
nabla X_lambda=0.
```

In the adapted frame this is equivalent to every connection coefficient joining unequal
eigenspaces vanishing.  Solve the full Cartan coefficient system pointwise in
`p1,p2,p3,A,B,C`, then impose the metric definitions and global smoothness.  Do not solve only one
favored block.

## Global and degeneracy audit

For every surviving pointwise stratum:

1. impose `p_i=E_i(phi)` and the `S3` bracket relations;
2. determine whether `phi` must be constant;
3. identify whether twist `a` is forced to zero;
4. identify any requirement `B=0`, `C=0`, infinite/zero exponential, rank loss, or topology change;
5. compute the surviving curvature algebra and verify it lies in the registered stabilizer; and
6. determine whether the metric is complete on `R x S3` and whether the ruler remains
   metric-intrinsically distinguished.

`a=0` is a regular metric restriction, not a mathematical degeneracy, but it removes the twist
selector used by the parent audit to identify the ruler.  A round spatial degeneracy at
`lambda=+1` must be reported rather than hidden.

The audit will also record curvature commutators `[R_cd,X_lambda]`.  Accidental curvature
centralization without `nabla X=0` is not sufficient for the intrinsic grading to descend and may
not be called endpoint closure.

## Independent verification

- Primary: exact symbolic Cartan/Koszul construction from the registered structure coefficients.
- Independent: direct exterior-form/Koszul coefficient implementation using rational probes and
  separate case substitution, without importing the primary solver.
- For every claimed surviving metric, coordinate/Torch curvature at three preregistered points
  `P00,P01,P02` must independently reproduce the predicted holonomy rank to scaled error `<=2e-8`.
- Exact symbolic identities must simplify to zero; numerical probes are regression checks only.

## Falsification and maximum conclusion

If all gates pass, the maximum conclusion is an exact classification of **strong intrinsic
`X_lambda`-parallel reductions inside this coframe family**, plus curvature verification of the
surviving strata.

It may not classify every metric outside the family, every accidental curvature-only reduction,
or any on-shell UDT solution.  It may not select `lambda`, a physical branch, seam, quotient,
action, source, carrier, boundary, density, bootstrap, mass, `X_max`, dynamics, signalling law, or
observation fit.

If no nonconstant intrinsic-pair branch survives, the path-groupoid result remains the default for
this family.  That is not a UDT no-go.

## Completeness map

Covered: symbolic real `lambda` split into every eigenvalue stratum, arbitrary stationary `phi`,
twist on/off, full connection blocks, metric substitutions, global `S3` integrability,
nondegeneracy, completeness, ruler identifiability, and surviving curvature.

Dropped: time dependence, other topologies/coframes, nonstationary shifts, other reciprocal lifts,
all action/source/carrier/boundary/bootstrap/density/mass/`X_max` questions, and physical selection.
