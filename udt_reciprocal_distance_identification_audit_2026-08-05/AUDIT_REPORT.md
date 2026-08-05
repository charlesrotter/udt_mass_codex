# Reciprocal distance-identification audit

Date: 2026-08-05

Status: **DERIVED BOUNDED SPLIT RESULT; EXTERNAL ADVERSARIAL REVIEW ACCEPTED WITH MECHANICAL REPAIR**

## Result first

The central intuition has an exact mathematical core:

> A supplied founded reciprocal observer-pair arrow already contains both a signed ordered depth
> and a symmetric nonnegative reciprocal magnitude. They are not two separately attached objects.

For

```text
D(delta)=diag(exp(-delta),exp(+delta)),
```

the two readouts are

```text
delta(D) = (1/2) log(D_22/D_11),
rho(D)   = arcosh(Tr(D)/2) = abs(delta).
```

The signed readout composes additively and reverses sign. The magnitude is reversal-even,
nonnegative, faithful, and satisfies the triangle inequality. On the one-dimensional founded group,
it is the invariant geodesic distance from identity after the registered unit is fixed.

That proves the algebraic statement “one reciprocal relationship, two aspects.”

## What does not yet follow

The proof does not identify `rho` alone with complete physical positional separation for arbitrary
observer pairs.

1. `rho` is dimensionless and unbounded, whereas physical separation must approach finite `X_max`.
   A calibration profile remains necessary.
2. Two exact profiles—`X_max tanh(kappa rho)` and
   `X_max[1-exp(-kappa rho)]`—share the same origin, ordinary-regime slope, monotonicity,
   subadditivity, and `X_max` asymptote but differ. Thus `c_E` and the limiting behavior do not choose
   the global law.
3. Equal-depth observers can still have nonzero angular separation. Scalar reciprocal magnitude is
   one instrument, not the complete orchestra.
4. Exact reference shifts change representative endpoint depth while preserving complete coframes.
   A bare complete coframe therefore does not universally recover the scalar.
5. Levi-Civita transport is metric-isometric and is not automatically the founded reciprocal
   physical operation. Generic full holonomy also obstructs endpoint-only descent of a non-scalar
   complete reciprocal generator.

## Strongest honest reformulation

Physical separation need not be imagined as a scalar already present before dilation is applied.
The proof instead supports this architecture:

> The fundamental object is one complete observer-pair comparison. Signed reciprocal depth and its
> nonnegative magnitude are exact readouts of its founded reciprocal component. Angular, mixing,
> path, and global information belong to that same comparison. A scalar physical separation, if
> required, must be a reference-independent readout of the complete object.

This is holistic and avoids tacking on the angular sector later. The physical identification is an
owner-proposed conceptual frame; the frozen sources do not yet construct the complete comparison
map for all observers.

## Positive branch anchor

On a stationary branch with an intrinsic timelike Killing line,

```text
delta_K(p,q)=log[N(p)/N(q)],
rho_K(p,q)=abs(delta_K(p,q))
```

provide a genuine metric-native example. It remains branch-local and does not close the
nonstationary, angular, path, cut-locus, or `X_max` profile problem.

## Sharpened missing object

The remaining target is no longer an unexplained scalar `phi`. It is a metric-natural complete
comparison map from complete global geometry plus an ordered observer/event query to a complete
comparison arrow, together with:

- a reference-independent reciprocal projection;
- explicit path or endpoint semantics;
- retention of angular and mixing information; and
- a full-coframe scalar separation readout only if the theory requires one.

The observer-pair law must reduce to the exact stationary result where available and obey the
ordinary `c_E` and `X_max` gates. No action, source, carrier, boundary, bootstrap return, mass, or
dynamics was derived.

## Evidence

- Primary SymPy 1.13.1 derivation: `21/21` exact checks.
- Independent standard-library/Fraction reconstruction: `40/40` checks, including an independently
  assembled rational rank-15 Lorentz-centralizer system.
- Frozen source set: 13 files, exact SHA-256 identities.
- The complete derivation is `EXACT_DERIVATION.md`; machine statuses are in `STATUS_LEDGER.tsv`.
- Fresh read-only Codex `gpt-5.4` adversarial review: `ACCEPTED_WITH_REPAIRS`. It could not refute
  the bounded theorem or its open-scope conclusions. It found one mechanical evidence defect: the
  original scope gate saw tracked diffs but not the untracked audit packet. The preregistered repair
  now requires the exact 13-path package across tracked and untracked state, rejects every other
  untracked path except the protected 83-path curvature set, and exercises an extra-path catch-proof.

## Four gates

1. Preregistered: yes, commit `f4f72c78` before computation.
2. Scope: complete for the founded one-dimensional reciprocal subgroup and the registered exact
   countermodels; not a census of all future complete-comparison constructions.
3. Independent verification: separate standard-library/Fraction implementation passes; fresh
   external semantic review accepted the theorem with one mechanical scope-gate repair, now applied
   and exercised.
4. Premises: audited explicitly; physical distance identification, complete extension, path,
   profile, `X_max` value, action, source, boundary, matter, mass, and dynamics remain unselected or
   open.

Maximum conclusion:

```text
DERIVED_SIGNED_DEPTH_AND_RECIPROCAL_MAGNITUDE_FROM_ONE_SUPPLIED_FOUNDED_ARROW__
COMPLETE_PHYSICAL_OBSERVER_SEPARATION_IS_A_FULL_COMPARISON_READOUT_NOT_YET_DERIVED
```
