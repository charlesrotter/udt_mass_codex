# G233 preregistration — primary-profile Cartan closure discriminator

Date: 2026-08-23

## Question

Does the current G231 state \((R,\nabla R,\nabla^2R)\) close the unrestricted declared primary
static-spherical profile family under one universal local finite-order autonomous derivative law?

## Arena and premises

- Metric-led primary static-spherical reciprocal areal metric only.
- Regular orbit \(r_0>0\), with \(s=\log(r/r_0)\).
- Compare the exact analytic family

  \[
  \phi_b(s)=s^3+c s^4+b s^5
  \]

  near \(s=0\), with positivity enforced on a sufficiently small common neighborhood.
- No fit, transfer, source, action, matter, bootstrap, `X_max`, P1, G116/G189, protected work, or
  fifth-jet dimension census.

## Required load-bearing checks

1. Directly construct the metric and compute the necessary radial curvature quantities from the
   metric, not solely from a previously simplified tidal formula.
2. Prove that two distinct \(b\) values have identical metric four-jets at \(s=0\).
3. Verify equality of all invariant/equivariant data represented by
   \((R,\nabla R,\nabla^2R)\) at that orbit, with isotropy and frame typing stated.
4. Exhibit one explicit component or scalar contraction of \(\nabla^3R\) that differs.
5. Independently replay the load-bearing difference using a separately implemented metric-jet or
   tensor calculation.
6. Separately verify the fixed-member and fixed-\(n\) G204 conditional closure controls.

## Falsification contract

The proposed obstruction fails if the two profiles do not share the complete G231 state, if the
purported next-order difference is coordinate/frame artifact, or if one foundation-owned
family-uniform map reconstructs the differing derivative from the shared state.

## Preregistered landings

Successful obstruction:

```text
FIXED_MEMBER_CARTAN_DESCENT_IS_EVALUATIVE
__FINITE_G204_CLOSURE_IS_FAMILY_CONDITIONAL
__UNRESTRICTED_PRIMARY_PROFILE_HAS_NO_UNIVERSAL_FINITE_JET_AUTONOMOUS_CLOSURE
__VALUED_PAIR_NETWORK_ENCODES_BUT_DOES_NOT_GENERATE_PROFILE
```

Failed obstruction:

```text
G231_STATE_COLLISION_WITNESS_FAILED__FINITE_CLOSURE_REMAINS_OPEN
```

## Maximum conclusion

Even on success, the negative is family-scoped and finite-order/local. It does not exclude nonlocal
or infinite-state closure, derive a physical profile, select a finite family, populate observers,
derive dynamics, or resolve `X_max`.
