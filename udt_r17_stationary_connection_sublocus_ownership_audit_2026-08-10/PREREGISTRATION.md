# Preregistration — R17 stationary connection subloci and ownership

Date: 2026-08-10

Base commit: `64b5319c1115589928317008548224600881b252`

Mode: metric-led exact analytic/CPU classification. No fitting, eigensolve, ODE solve, GPU work,
action, source, matter model, or desired branch.

## Whole question

On the already supplied regular stationary R17/W01 family

```text
theta0=u^-1(dt+a sigma3), theta1=u sigma3,
theta2=v sigma1,          theta3=v sigma2,
u=exp(phi), v=exp(lambda phi), T(phi)=0,
lambda in {-2,-1,0,1/2,1,2},
```

classify every compatible smooth stationary subfamily on the inherited `R x S3` completion for
which the complete projected normal connection is:

1. fully flat;
2. locally horizontal with respect to the `R x S1` pair fibers;
3. globally descended through those fibers, separating an abstract parallel-quotient descent from
   descent through the inherited Hopf tangent identification; or
4. reduced-holonomy on the complete total space.

Only after that classification, determine whether any existing R17 field equation, on-shell rule,
or global completion datum selects one surviving subfamily.

## Frozen arena

- All six supplied `lambda` strata are retained and none is preferred.
- The R17 all-gate twisted sector has `a>0`; formulas are derived symbolically and then specialized
  to the registered `a=1/64`. The registered `a=0` and `phi=0` rows are controls only.
- `phi` is any smooth stationary scalar on compact `S3`; noncommuting first and second jets obey all
  Maurer--Cartan compatibility relations.
- `u,v` are positive and the stationary spatial slice remains regular.
- The completion is exactly the inherited smooth `R x S3`; quotients, seals, null/rank-changing
  strata, time-live configurations, and other branch families are excluded.
- The complete connection and six curvature components are frozen to G49; they may be
  independently reconstructed but not reassigned.

## Descent types

The audit must not use one ambiguous word `descent` for different objects.

- `LOCAL_CURVATURE_HORIZONTAL`: `i_T F=i_Z F=0`.
- `ABSTRACT_PARALLEL_QUOTIENT_DESCENT`: local horizontality plus trivial vertical holonomy, so
  `D` defines a connection on a vector-bundle quotient over `S2`.
- `CANONICAL_HOPF_TANGENT_DESCENT`: the descended connection is compatible with the inherited
  `d pi:H->TS2` identification, not merely some parallel quotient.

The period convention must be inherited from the banked R17 leaf audit and stated explicitly.

## Ownership census

The ownership test searches the complete tracked repository at the frozen base for R17/W01 field
equations, action equations, on-shell conditions, profile equations, boundary/completion selectors,
and explicit branch-selection rules. Filename or repeated use is not ownership. A frozen witness,
sampled profile, conditional coframe, or test control cannot be promoted to an equation.

## Falsification and certification

The result fails if it:

- drops a supplied `lambda` or the nonzero twist;
- treats compatible frame jets as independent coordinate jets;
- calls leafwise flatness complete flatness;
- treats curvature horizontality alone as global descent;
- ignores vertical holonomy or the inherited Hopf action;
- invents a proper nontrivial connected subgroup of `SO(2)` holonomy;
- calls an off-shell witness an R17 equation;
- says compactness or simple connectedness selects a profile or `lambda`; or
- infers a physical path, non-isometric observer arrow, action, source, matter, bootstrap, `X_max`,
  CMB, signalling, or dynamics.

Certification requires an exact symbolic derivation, an independent implementation that does not
import the production controller, global compactness/holonomy proofs with precise hypotheses, an
exercised mutation suite, the full ownership census, and fresh manifest-confined adversarial review.

## Maximum conclusion

At most this audit may classify the stationary special subfamilies, state the complete holonomy of
the supplied `R x S3` connection on each, and determine whether an already registered R17 equation
or completion datum owns any of them. It cannot select R17, `lambda`, `phi`, a physical path, a
physical observer arrow, or downstream physics.
