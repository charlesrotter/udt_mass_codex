VERIFIED_WITH_CORRECTIONS

## Load-bearing independent result

For

```text
g = E^T eta E,  eta = diag(-1,1,1,1),  E = [[B,0],[QS,Q]],
B = [[T,T beta],[0,L]],  Q = [[u,0],[v,w]],  S = [[s00,s01],[s10,s11]],
```

with `T,L,u,w>0`, write `g=[[G,C],[C^T,H]]`. Independent recomputation gives

```text
H = Q^T Q,
C = S^T H,
A := G - C H^-1 C^T = B^T diag(-1,1) B.
```

Thus

```text
w = sqrt(H33),  v = H23/w,  u = sqrt(det(H)/H33),
S = H^-1 C^T,
T = sqrt(-A00),  beta = A01/A00,  L = sqrt(det(A)/A00).
```

This verifies the constructive inverse on the connected component `T,L,u,w>0`, positive-definite
`H`, `A00<0`, and `det(A)<0`. Independent differentiation of the ten ordered metric components
reproduces

```text
det(dg/dq) = 16 L T^3 u^5 w^6.
```

For jets, the point diffeomorphism prolongs with block-triangular Jacobian

```text
det J^kF = [16 L T^3 u^5 w^6]^(binomial(4+k,k)).
```

No hidden contact or coframe-anholonomy constraint changes that local statement.

## Required corrections

The negative result is chart-bounded and source-bounded: it does not cover every global
admissibility law, branch, or split-changing/null/rank-changing stratum. A perturbation supported
away from the boundary preserves its full boundary germ, and may preserve a chosen end, but does
not automatically preserve chronology, global hyperbolicity, causal faithfulness, completeness,
or selected global descent. The preregistration verifier is not transport-correct for the sealed
`sources/` layout and needs an explicit packaging correction.

No already-owned missed mandatory restriction was found in the ten frozen sources. `X_max` is a
working asymptotic requirement on an open law, not a current boundary law. Global causal
faithfulness is a possible filter but remains open. Global descent owns structure, not a complete
selector or time-live equation.

## Maximum justified conclusion

```text
COMPLETE_REGULAR_CHART_IS_LOCALLY_JET_OPEN_ON_THE_DECLARED_POSITIVE_SCREEN_TIME_ORIENTED_COMPONENT;
NO_CURRENTLY_OWNED_NONIDENTITY_HISTORY_RESTRICTION_IS_FOUND_IN_THE_TEN_FROZEN_SOURCES.
```

This refutes extracting a local nonidentity differential equation merely by expanding the same
complete regular factorization. It is not a universal no-go against future native laws, global
completion rules, causal-faithfulness filters, or branch-selecting premises.

## Smallest next joint

The first type-correct owned global selector has the type

```text
R(j^k g; G_global) = 0,
```

where the global datum must specify branch, query, reset, and boundary semantics. In the reviewed
corpus this remains only a type, not a formula.
