# G150 audit report — first-order pair-chord freedom ceiling

Date: 2026-08-17
Status: `VERIFIED_WITH_CAVEATS`

## Bounded result

For every fixed regular pair metric

\[
h=\operatorname{diag}(-T^2,L^2),\qquad T,L>0,
\]

the explicit smooth quadratic immersion counterfamily makes

\[
(\dot\phi_{\rm pair},a_n,\Omega_2,\Omega_3)
\]

surjective onto \(\mathbb R^4\). The exact output Jacobian has nonzero rank-four minor

\[
-\frac{1}{2L^3T^5},
\]

and the registered right inverse recovers every target exactly. Therefore no nontrivial universal
pointwise algebraic equation involving only those four outputs follows in the unrestricted smooth
regular local metric/query class.

## Evidence gates

- preregistered: PASS (`24968eb7`)
- bounded scope: PASS
- explicit immersion and exact symbolic derivation: PASS
- full declared four-output target space: PASS by constructive right inverse
- separate implementation regression replay: PASS; maximum error `5.55e-17`
- injected mutation/counterexample catches: PASS
- fresh independent adversarial derivation: initial `REPAIR_REQUIRED`, repaired follow-up
  `FOLLOWUP_PASS`
- premise audit before banking: required

## What this does not say

The registered immersion jets contain other first-order information not classified by these four
readouts. Physical-query restrictions, next pair-frame jets, metric curvature and Jacobi relations,
global completion, dynamics, regime amplitudes, and asymptotic/degenerate strata remain open.

At \(\phi_{\rm pair}=0\), the supplied pair frame remains defined, but the working chord
\(\xi=X_{\max}\tanh(\phi_{\rm pair})n\) vanishes.

## Landing

```text
VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS__
NO_NONTRIVIAL_UNIVERSAL_POINTWISE_ALGEBRAIC_RELATION_AMONG_DOTPHI_AN_AND_TWO_OMEGA_COMPONENTS__
IN_UNRESTRICTED_SMOOTH_REGULAR_LOCAL_PAIR_KINEMATICS__
FOUR_NAMED_READOUTS_SURJECTIVE_AT_EVERY_FINITE_PAIR_DEPTH__
OTHER_FIRST_ORDER_OBJECTS_NEXT_PAIR_FRAME_JET_METRIC_CURVATURE_PHYSICAL_QUERY_GLOBAL_DYNAMICAL_AND_REGIME_CONSTRAINTS_OPEN
```

