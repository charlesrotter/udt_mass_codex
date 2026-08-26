# G270 preregistration — completed-pair transported-screen ownership

Date: 2026-08-26
Status: `PREREGISTERED_BEFORE_OUTCOME_COMPUTATION`

## Whole question

Does the working completed-pair Dual Reciprocity condition, together with the already derived
null-germ and carry identities, force or otherwise determine the G269 transported screen mismatch
`W`? Or does a complete supplied ambient realization evaluate `W` while the intrinsic completed
pair metric and reciprocal normalization leave it unrestricted across admissible realizations?

## Mode

`METRIC_LED`, observing rather than targeting. No new residual or physical constraint may be added.

## Frozen alternatives

1. `A__UNIVERSAL_TRANSPORTED_PLANARITY`: completed-pair Dual Reciprocity forces `W=0`.
2. `B__DEPTH_DETERMINES_SCREEN_MISMATCH`: existing equations force
   `||W||^2=F(r)` for one nontrivial coefficient-free function.
3. `C__REALIZATION_EVALUATES_W__INTRINSIC_COMPLETED_PAIR_DOES_NOT_SELECT_IT`: `g`, the branch, and
   the supplied endpoint/pair realization determine `W`, but completed-pair Dual Reciprocity and
   the intrinsic pullback do not; an exact same-pullback family with different `W` survives.
4. `D__TYPE_OR_ALGEBRA_FAILURE`: the G269/G176--G225 structures cannot be joined consistently.

## Planned exact separator

Use flat `1+2` spacetime with source clock and affine null tangent

\[
U_A=(1,0,0),\qquad k=(1,1,0).
\]

For positive `r` and real `w`, define

\[
\Gamma=\frac12\left(r+r^{-1}+rw^2\right),
\qquad
a=\Gamma-r^{-1},
\qquad
U=(\Gamma,a,w).
\]

At each point set `omega=1/r`, `K=k/omega=rk`, and `N=K-U`. The calculation must establish or
reject:

- `U` is unit timelike;
- `N` is unit spacelike and orthogonal to `U`;
- `K=U+N` is the completed pair's normalized null direction;
- the auxiliary null-ribbon pullback in basis `(U,k)` is
  `h_sigma=[[-1,-1/r],[-1/r,0]]`, independent of `w`;
- completed normalization gives `m=1/r` and the same determinant-one `h_s` for all `w`;
- the transported screen mismatch relative to the source plane is `||W||^2=w^2` and therefore
  varies at fixed `r` while every intrinsic completed-pair scalar stays fixed.

For the smooth-family gate, take positive smooth `r(lambda)` and real smooth `w(lambda)`, set
`gamma(lambda)=lambda k`, and use the local ribbon

\[
F(\tau,\lambda)=\gamma(\lambda)+\tau U(\lambda).
\]

The result is required only on a sufficiently small neighborhood of `tau=0`, where regularity
follows if the pullback determinant remains negative.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| smooth Lorentzian metric | `SUPPLIED_CONDITIONAL` | contractions and transport |
| affine null branch | `SUPPLIED_CONDITIONAL_QUERY` | common frequency/transport path |
| completed pair germ/ribbon | `SUPPLIED_CONDITIONAL_QUERY` | full ambient realization |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | intrinsic determinant-one calibration |
| endpoint clocks | `SUPPLIED_CONDITIONAL_QUERY` | frequency and transported-clock comparison |
| Levi-Civita transport | `DERIVED_FROM_SUPPLIED_METRIC` | cross-event plane comparison |
| flat family | `MATHEMATICAL_COUNTERMODEL` | selection separator only |
| physical population/history | `OPEN_OMITTED` | forbidden promotion |

No value is `pinned-by-HABIT`.

## Certification and falsification contract

1. exact symbolic reconstruction of the target frame, pullback, completed normalization, and
   transported mismatch;
2. an implementation-distinct exact-rational census with fixed-`r`, varying-`w` separators;
3. a smooth-ribbon local regularity calculation including nonconstant `r(lambda),w(lambda)`;
4. mutations for forcing `W=0`, inserting `W` into the intrinsic determinant, confusing `W` with
   Jacobi area, deleting query dependence, or promoting the result to population/history;
5. source hashes, no-write replay, premise audit, and fresh external review before a strong grade.

Alternative A or B fails if two regular completed realizations have the same intrinsic completed
pullback and reciprocal depth but different nonnegative `W^2`. Alternative C fails if `W` is not
uniquely evaluable once the full ambient metric, branch, and endpoint realization are supplied.

## Omitted sectors

Singular/caustic/cut/multiple branches, observer population, global completion, observations,
distance, `X_max`, action, source, matter, mass, transfer, bootstrap, and signalling are omitted.
The G225 screen isometry and G188 Jacobi map remain distinct from the G269 endpoint-clock mismatch.

## Maximum conclusion

At most G270 may classify whether completed-pair Dual Reciprocity owns a universal value of `W` or
only normalizes the intrinsic pair metric while a supplied ambient realization evaluates `W` as a
separate bilocal channel. It may not choose physical relations or add a history law.

