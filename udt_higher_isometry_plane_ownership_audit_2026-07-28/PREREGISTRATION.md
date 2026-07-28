# Preregistration — higher-isometry Killing-plane ownership audit

Date: 2026-07-28

Base: `99cbec700add7f72f3ff9e67f3bdfaa89cfd1724`

## Whole question

The preceding audit recovered the founded clock/ruler pair from the complete metric on the
registered descended Killing plane `span(K,V)` whenever `phi` is nonconstant, but explicitly left
the plane itself conditional. This audit asks whether the complete stationary metric distinguishes
that plane when additional compact Killing circles are present.

This is an observation/classification problem. It does not ask the geometry to retain `K`, the
Hopf circle, a particle, or any desired physical interpretation.

## Exact bounded family

The fixed family is the fully descended stationary block-screen metric on the chosen
`R_t x S3` control,

```text
g=-u(c_E dt+alpha A)^2+u^-1 A^2+q_B,   u=exp(-2 phi)>0,
```

where `A=sigma3` is the registered Hopf connection, `phi` and the positive base metric `q_B` are
basic, and the full two-shear screen remains contained in unrestricted positive `q_B`.

Higher-isometry strata are represented without choosing a preferred extra circle:

1. the generic `R x S1` control with only `K,V`;
2. every connected additional commuting compact circle, hence the full `R x T2` orbit algebra,
   written with arbitrary connection moment `f=A(Y)` and arbitrary positive horizontal norm
   `b=q_B(Y-fV,Y-fV)`;
3. every primitive circle in the registered toric cap lattice, including all free and non-free
   circle classes rather than only the Hopf class;
4. constant-depth, twist-off, axisymmetric, Berger/homogeneous, and round enhanced-isometry
   controls, including compact circles related by the enhanced group;
5. noncommuting enhanced generators only to the extent that their circle subgroups are conjugate
   into the classified maximal tori. Any exotic higher-isometry family not preserving the
   registered Hopf bundle is retained as an explicit open boundary, not assigned an answer.

No direct pair/screen metric off-block, variable `alpha`, nonstationarity, field equation, action,
source, carrier, density, bootstrap value, boundary law, or dynamics is admitted.

## Planned exact computations

1. Derive the full `3 x 3` orbit Gram matrix on `(K,V,Y)` for arbitrary symbolic
   `(u,alpha,c_E,f,b)` and its determinant, causal inertia, and constant-basis covariance.
2. Derive `D_X=G^-1 X(G)` with independent first jets `(X(phi),X(f),X(b))`; classify its rank,
   eigenlines, invariant subspaces, and every degeneracy without assuming the old answer.
3. For every real projective constant Killing direction `W=aK+pV+qY`, derive the exact residual
   for the founded clock response and solve/classify the generic and exceptional coefficient
   conditions. A direction is reported, never filtered, if it is null, spacelike, closed,
   non-free, or fails the founded response.
4. Enumerate primitive toric circle classes against both cap vectors and separately classify
   closure, freeness, and metric-response behavior. Topology and metric selection remain distinct.
5. Evaluate exact axisymmetric and homogeneous controls, including the registered Hopf and
   anti-Hopf free circles on standard `S3`, constant `phi`, `alpha=0`, and enhanced compact
   isometry.
6. Decide only whether the registered plane is `UNIQUE_METRIC_SELECTED`,
   `SELECTED_ON_GENERIC_STRATUM`, `MULTIPLE_EQUIVALENT_PLANES`, `DEGENERATE`, or
   `OPEN_OUTSIDE_BOUNDED_FAMILY` in each stratum.

## Preregistered falsification and certification

- Refute universal plane selection if one admitted smooth positive complete metric has two
  inequivalent planes satisfying the same registered metric-only certificate.
- Refute the claim that topology selects `V` if another primitive free circle exists for the same
  cap data.
- Refute the claim that the old `2 x 2` selector automatically extends if the exact `3 x 3`
  response fails to preserve `span(K,V)` or fails to retain its simple causal eigenspaces.
- Certify a generic-stratum result only from symbolic necessary-and-sufficient conditions plus
  exact representative controls; sampled points alone cannot certify it.
- A special homogeneous or constant-depth degeneracy cannot erase a generic result, and a generic
  result cannot be promoted over that degeneracy.
- Catch-proofs must break every load-bearing formula, plane count, cap classification, and status
  gate.
- Before banking: independent no-production-import implementation, fresh adversarial semantic
  review, current-premise replay, full tests, frozen manifests, navigation, and dirty-metadata gate.

## Maximum allowed conclusion

A bounded exact classification of whether and where the complete descended stationary metric
selects the registered reciprocal Killing plane among additional compact symmetry directions.
No macro/micro assignment, physical branch, Hopf carrier, action, source, density/bootstrap law,
boundary, dynamics, mass emergence, observation, or canonization may follow.

