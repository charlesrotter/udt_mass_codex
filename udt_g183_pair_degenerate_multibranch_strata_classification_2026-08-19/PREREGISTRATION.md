# G183 preregistration — pair degeneracy and multibranch strata

Date: 2026-08-19

## Whole question and bounded regime

Classify what happens to the accepted completed-pair kernel when a supplied pair realization meets
one of five qualitatively different situations:

1. a null curve inside an otherwise regular Lorentzian pair plane;
2. a null chosen clock direction while the pair plane remains nondegenerate;
3. true pullback/rank degeneracy;
4. focal/caustic rank loss of a query-generated realization; or
5. several regular cut, crossing, or winding branches with the same endpoint data.

The arena is a smooth Lorentzian four-metric of index one, a supplied calibrated two-dimensional
pair germ `F`, its coframe-valued tangent matrix `V=EJ`, and `h=V^T eta V`. The completed kernel is
tested only where `h00<0` and `det(h)<0`.

This is metric-led classification of the accepted kernel domain. It is not a new kernel, path law,
branch selector, singularity theorem, or global completion.

## Preregistered claims to test

1. A null curve in a regular Lorentzian pair plane does not invalidate the pair kernel.
2. `h00=0, det(h)<0` is a failure of the supplied timelike-clock calibration, not intrinsic
   degeneracy of the two-plane. The plane contains timelike directions, but choosing one is a new
   calibration/query unless already supplied.
3. If `h00<0`, then `det(h)=0` if and only if the second tangent is proportional to the timelike
   clock tangent. Thus this stratum is genuine rank loss and the completed density vanishes.
4. A focal/caustic point breaks the pair kernel exactly when the differential of the particular
   supplied realization loses rank in the sampled two-dimensional variation. A conjugate direction
   outside that variation is not sufficient.
5. Cut, crossing, and winding multiplicity can occur with every local branch regular. The kernel is
   then branch-valued; it neither fails nor selects a branch.
6. Equal scalar depth, and even equal completed pair metric, need not erase branch tangent,
   orientation, winding, or holonomy labels.

## Exact witnesses fixed before outcomes

- null curve in `diag(-1,1)`;
- null clock with Gram matrix `[[0,1],[1,1]]` and a timelike replacement basis vector;
- proportional-tangent rank collapse with determinant zero;
- flat Rindler normal-exponential focus
  `F(tau,s)=((a^-1+s)sinh(a tau),(a^-1+s)cosh(a tau))`;
- upper and lower unit semicylinder branches with identical completed metrics and endpoints but
  different endpoint tangents;
- `R x S^1` winding immersions, including the two equal-length antipodal branches.

## Physical-choice ledger

- Lorentz signature and complete pullback: `pinned-by-THEORY` through G179.
- Completed-pair normalization on regular strata: `WORKING_FOUNDATIONAL_CLARIFICATION`, G176--G182.
- Incident query, branch, clock calibration, endpoint matching, circle radius, acceleration, and
  winding label: `free-and-explored` controls.
- `X_max`, action, source, matter, bootstrap, radiative transfer, observations, signal law, and
  global completion: omitted and inactive.
- No `pinned-by-HABIT` physical value, boundary, fit, carrier, or action enters.

## Verification contract

- Production: exact symbolic/rational proofs plus at least 12,000 rational timelike Gram trials.
- Independence: a separately written implementation using orthogonal decomposition, direct rank,
  and explicit embeddings; at least 20,000 rational trials.
- Mutation catches must kill sign swaps, determinant/rank conflation, null-curve conflation,
  clock-null intrinsic-degeneracy promotion, focal-overreach, branch scalarization, and winding loss.
- Package replays must be dependency-free, read-only, hash checked, and premise audited.
- A fresh adversarial review is required before banking a positive classification.

## Falsifiers

The preregistered landing fails if any of the following occurs:

- a null curve forces degeneration of a regular Lorentzian pair metric;
- a Gram matrix with `h00=0, det(h)<0` lacks a timelike direction;
- `h00<0, det(h)=0` survives with two independent tangent vectors in a Lorentz-index-one ambient;
- the Rindler focus remains rank two;
- regular equal-endpoint branches are forced to have one tangent, one winding, or one scalar owner;
- the classification silently selects a branch or imports a path law.

## Maximum conclusion

At most G183 may classify the local domain failures and the regular multibranch output type of the
already accepted completed-pair kernel on supplied queries. It may not decide which branch is
physical, identify a metric-space distance, derive holonomy from the scalar, or make any global,
observational, dynamical, source, matter, `X_max`, or signalling claim.
