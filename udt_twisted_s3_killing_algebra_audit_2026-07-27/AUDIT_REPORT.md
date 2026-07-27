# Audit report — twisted reciprocal S3 full Killing algebra

## Result

The same-branch **configuration-existence** gap is closed.

There is an explicit globally smooth, globally spatially complete, strictly regular twisted
reciprocal metric on `R x S3` for which:

1. the unrestricted full Killing algebra is exactly one-dimensional;
2. its unique line is the everywhere-timelike stationary line;
3. its norm supplies the nonconstant signed depth `phi(q)-phi(p)`; and
4. its nonzero Killing twist supplies the founded unoriented reciprocal ruler line.

The load-bearing certificate is intrinsic, not visual or coordinate-based: the exact determinant of
the spatial gradients of `R`, `trace(Ric^2)`, and `trace(Ric^3)` is

```text
330801319823081673814309577 / 159252480000000000000000000000 != 0.
```

This annihilates the spatial component of every possible Killing vector on an open set, including
time-dependent and time-space-mixed candidates. The Killing equation and finite-type propagation
then prove globally that every Killing vector is a constant multiple of `partial_t`.

Here “complete” means the registered complete global `S3` coframe/configuration rather than a local
chart or cap. Lorentzian geodesic completeness was not tested or claimed.

## Independent check

A separate CPU implementation retained the full `sqrt` unit-quaternion chart and exponential metric
instead of using the primary exact jet algebra. Nested automatic differentiation reproduced all nine
curvature-gradient entries with maximum relative error `6.01e-16`; the determinant agreed to
`1.01e-12` relative and retained rank three.

## Degeneracy map

- Constant profiles are homogeneous and have at least three spatial Killing generators in addition
  to time translation: the line is not unique.
- A continuous stabilizer of the complete profile/coframe data likewise defeats uniqueness.
- The same asymmetric profile at `a=0` still has a unique Killing line, but no twist ruler.
- Exact `lambda=0` and `lambda=1` controls retain rank three; those values do not automatically
  restore a hidden symmetry.
- For this fixed profile the symbolic determinant is a nonzero ninth-degree polynomial in `lambda`.
  Its isolated real roots are certificate-degeneracy points only: uniqueness there remains open,
  because a zero determinant does not imply an additional symmetry.
- Every smooth `phi` and other quotient/boundary completions were not exhausted and remain explicitly
  open.

## Scientific grade

`VERIFIED-WITH-CAVEATS`.

The result is stronger than the earlier W01 lead because uniqueness, depth, and twist now occur in
one complete metric. It is not a physical branch-selection theorem. The profile and parameters were
free Category-A witnesses; no UDT action or bootstrap rule selected them.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

No action, EOM, source, carrier, boundary, density, bootstrap closure, mass, `X_max`, dynamics,
signalling, observational fit, GPU work, canonization, or startup-control change was made.

## Four evidence gates

1. **Preregistered:** yes, commit `b64e56a`, pushed before calculation.
2. **Full or bounded scope justified:** yes; full unrestricted Killing algebra for one explicit
   complete witness plus registered degeneracy controls. The whole parameter/function space is not
   claimed.
3. **Independently verified:** yes; different full-expression CPU automatic-differentiation method,
   plus fresh adversarial review before banking.
4. **Every premise audited:** yes; configuration choices and all excluded physical selectors remain
   explicit.

## Current open gate

The metric family can internally carry the complete stationary reciprocal clock/ruler structure.
What remains missing is not another kinematic component: it is the native whole-solution law, if
any, that selects a profile/configuration or relates this available structure to the still-open
action/bootstrap closure.
