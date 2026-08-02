# Preregistration — intrinsic two-form distribution and complete-cell degeneration audit

Date: 2026-08-02  
Branch: `grok`  
Preregistration base: `9cf6b7dc8c5d268e7da64c9054bb118a287dcd10`

## Whole question

On the unchanged stationary, off-shell, complete `R x S3` screen ensemble, determine what metric
structure is carried by the already verified intrinsic two-form

```text
W=dPhi_contact wedge dSigma_contact
```

wherever the unique-Killing/nonzero-twist projector gate passes. Decompose `W` into ruler/screen
parts, construct its Hodge dual and kernel, classify every zero/alignment/mixed/blocked stratum, and
test whether its projective dual line continues through the complete cell.

This is metric-led and outcome-neutral. It does not target a carrier, Hopf section, particle,
preferred direction, nonzero result, or selection law.

## Inherited ensemble — no new metric candidate

The 18 candidates are exactly those in
`udt_intrinsic_general_screen_neighborhood_audit_2026-08-02/CANDIDATE_UNIVERSE.tsv`, SHA-256
`a8c7c8f8c2c3992256e8b27d1e20bdd26b4f1e12d9ad5996b435531276ec2c9d`. Their parent projector and
configuration-level alternating statuses are frozen in `CANDIDATE_BINDING.tsv`.

No candidate, profile, `lambda`, `a`, point, or epsilon may be added or removed after outcome. The
same unit-quaternion profile is used:

```text
u=3+q0^2+2 q1^2+4 q2^2+8 q3^2,
V0=q0^2+3 q1^2+7 q2^2+9 q3^2,
V=1+(1/10)V0,
sum q_i^2=1.
```

The registered screen determinant is `D=u^lambda V` on independent-area candidates. The inherited
screen shears, twist controls, constant/slaved controls, and degenerate control remain exactly as
frozen by the parent.

## Intrinsic definitions under test

On a parent branch with unique unit timelike Killing line `T`, nonzero twist line `S`, and intrinsic
screen projector `H`, define

```text
alpha=dPhi_contact,
beta=dSigma_contact,
W=alpha wedge beta.
```

Stationarity should imply `alpha(T)=beta(T)=0`; this is tested. Decompose

```text
alpha=alpha_S S_flat+alpha_H,
beta = beta_S S_flat+ beta_H,

W_HH=alpha_H wedge beta_H,
W_SH=S_flat wedge (alpha_S beta_H-beta_S alpha_H),
W=W_HH+W_SH.
```

Using the four-metric Hodge star, define the orientation-dependent one-form and its sign-independent
line/projector

```text
N_flat = star(T_flat wedge W),
L_W=span(N)                         when N != 0,
Pi_W = N tensor N_flat / g(N,N)    when N != 0.
```

The expected algebraic identities are tests, not accepted outcomes:

```text
i_T W=0,
i_N W=0,
ker(W)=span(T,N) when W != 0,
dim ker(W)=2 when W != 0,
dim ker(W)=4 when W=0.
```

Orientation or either representative-line sign may flip `N` but must not change `L_W` or `Pi_W`.

## Relative line types

On `W != 0`, classify exactly one of:

```text
RULER_ALIGNED:   L_W=L_S,
SCREEN_CONTAINED:L_W subset H but L_W != L_S,
GENERIC_MIXED:   L_W has both ruler and screen components.
```

In an oriented orthonormal spatial coframe `(theta1,theta2,theta3)` with `theta1` on `S`, the exact
coordinate-free tests are

```text
RULER_ALIGNED    iff W_SH=0 and W_HH!=0,
SCREEN_CONTAINED iff W_HH=0 and W_SH!=0,
GENERIC_MIXED    iff W_HH!=0 and W_SH!=0.
```

The implementation must derive and record the component/orientation convention before translating
these tests into indexed components. A mutation catch must fail if the coframe indices are guessed
rather than derived.

`ZERO`, `PROJECTOR_BLOCKED`, and `METRIC_DEGENERATE` are retained separate from the three nonzero
line types.

## Complete-cell algebra

Let `X1,X2,X3` be the exact vector fields dual to the frozen Maurer-Cartan coframe. For the
independent-area profile, compute

```text
w_ij=(Xi(u) Xj(V)-Xj(u) Xi(V))/(2 u V).
```

Clear only globally positive denominators. The primary route will use exact polynomial
factorization and ideal/support analysis on `sum q_i^2=1` to classify:

1. the full zero locus `Z(W)`;
2. the ruler-aligned, screen-contained, and generic-mixed loci;
3. intersections and higher degeneracies;
4. connected components of `S3\Z(W)` only when an exact topological argument is supplied; and
5. whether the projective line `[N]` has a unique, path-independent limit across each irreducible
   zero component and intersection.

A vanishing unnormalized `N` never automatically proves that its line cannot extend. Conversely,
factoring out one common scalar never proves a global extension unless all approach directions give
the same projective limit. Unresolved singular intersections remain `OPEN`, not filled by plotting.

## Frozen cross-check points

Exact global algebra is primary. The following stereographic points are frozen for coordinate and
numerical cross-checks only:

```text
p1=(1/5, 1/7, 1/11),
p2=(1/3,-1/5, 1/7),
p3=(-1/4,2/7,1/9),
p4=(2/5,1/6,-1/8),
p5=(0,1/3,1/5),
p6=(1/4,0,1/6),
p7=(1/4,1/6,0).
```

Failure to realize a line type at these points does not prove that the type is absent globally.

## Controls and falsification

- all 18 inherited candidates remain in the atlas;
- nine inherited intrinsic-zero candidates remain zero;
- six inherited intrinsic-nonzero candidates receive the full distribution analysis;
- C14, C15, and C18 remain blocked/degenerate controls and may not acquire an intrinsic line;
- all configuration-level quantities at blocked controls are labeled as such;
- the two-form is decomposable, so its nonzero antisymmetric-matrix rank is two;
- passive coframe, screen-frame, orientation, and representative signs are varied algebraically;
- all zero and singular strata remain in the result even if no physical interpretation is apparent;
- every mutation in `FALSIFICATION_CONTRACT.tsv` must be exercised and typed honestly.

Production will use exact CPU algebra. A fresh adversarial implementation must independently rebuild
the dual coframe, `W`, Hodge/kernel identities, and global zero/type-locus claims without importing
production functions. No GPU, fit, ODE/PDE, or relaxation is authorized.

## Maximum allowed conclusion

At most: a verified bounded intrinsic distribution and complete-cell degeneration atlas for the
unchanged stationary ensemble, including any exact local/global line-extension theorem or
obstruction actually proved.

No carrier, Hopf section, topology charge, preferred branch, field equation, dynamics, action,
source, boundary, density/bootstrap value, `X_max`, matter, mass, stability, phenomenology, or
canonization may follow.
