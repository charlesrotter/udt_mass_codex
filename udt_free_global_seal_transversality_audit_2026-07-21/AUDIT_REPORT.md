# UDT free-global-seal transversality audit

Date: 2026-07-21

Base: `6c17a36e3693d21de73b18827324ef68923c285c`

Preregistration: `c95009f`

Mode: CPU-only exact variation and constraint audit; no numerical evolution.

## Result first

Treating the finite-cell seal as a free boundary whose position must be varied is productive, but it
does not by itself close the boundary problem.

The primary classification is:

```text
FREE_BOUNDARY_ADDS_TRANSVERSALITY_BUT_REMAINS_FUNCTIONAL_DEPENDENT
```

The new premise adds one position/shape stationarity equation:

- one **integrated scalar equation** if only a global cell modulus is varied; or
- one **local normal shape equation** if the full codimension-one embedding is varied.

It does not select the boundary functional that appears in that equation, and it does not replace
the independent metric/coframe boundary equations. Zero of 21 lane/field pairs is P06-ready.

The free-boundary premise is recorded as `CHOSE / CONDITIONAL / OWNER-AUTHORIZED TEST`. This audit
does not promote it to canon.

## Why a free endpoint cannot select its own functional

The exact finite-dimensional control is

```text
S[q,T] = integral_0^T L(q,qdot) dt + B(q(T),T).
```

Let `Delta q` be the total endpoint field variation and `Delta T` the endpoint displacement. With
`p=partial L/partial qdot` and `H=p qdot-L`, direct variation gives

```text
delta S|endpoint
 = (p+B_q) Delta q + (-H+B_T) Delta T.
```

Consequently a free endpoint supplies transversality conditions only **after** `B` is specified.
The exact two-parameter family

```text
B = lambda q^2/2 + mu T
```

leaves the same bulk equation while changing the endpoint equations to

```text
p+lambda q=0,
H=mu.
```

This is a comparison theorem, not a proposed UDT boundary action. Its logical consequence is exact:
“vary the endpoint” does not imply `B=0`, and therefore cannot derive its own boundary functional.
The gravitational lanes already possess in-family versions of this ambiguity through the Euler
coefficient, exact divergences, potential improvements, Legendre transforms, and corners.

## Global position has two inequivalent meanings

Moving a coordinate endpoint and changing the overall physical scale are different variations.
Both were retained.

### Coordinate/embedding motion

For an outward embedding displacement `chi`, the bulk moving-domain identity is

```text
delta S_bulk
 = integral_M E.delta g
 + integral_boundary [Theta(g,delta g)+i_chi L].
```

Adding a boundary functional contributes its field, embedding, and corner variations. The normal
coefficient defines a shape equation only after those data are supplied.

### Constant homothety

For the separate global-size realization

```text
g_R = R^2 g_hat
```

on a fixed dimensionless four-cell, the conditional P05 bulk lanes scale exactly as follows.

For L01:

```text
S_L01(R) = alpha C2_hat + beta E4_hat,
dS_L01/dR = 0.
```

The four-dimensional pre-scale curvature-square bulk is exactly scale-flat. Varying the global size
does not select `R`; this is consistent with CSN rather than a failure of the variation.

For L02:

```text
S_L02(R)
 = kappa [R^2 A_hat - 2 Lambda R^4 V_hat] + beta E4_hat,

dS_L02/dR
 = 2 kappa R [A_hat-4 Lambda R^2 V_hat].
```

For positive `R`, a nonzero `Lambda` gives the conditional root

```text
R^2 = A_hat/(4 Lambda V_hat)
```

only when that ratio is defined and positive. The shape, `Lambda`, physical representative, and
boundary completion must already have been supplied. In the `Lambda=0` subcase stationarity requires
`A_hat=0` and leaves `R` unselected. A boundary contribution `B=b R^p` adds
`p b R^(p-1)` and changes the equation without changing the bulk metric equation.

This gives a useful two-stage clue but not a bridge theorem:

- pre-scale `C^2` cannot pick the global scale by homothety;
- post-scale EH can carry a conditional scale equation;
- nothing here derives the transition, `Lambda`, the shape, or `B`.

## The moving-seal correction

If the moving seal is conditionally represented as a regular `phi=0` level surface, the quantity
preserved under a varied embedding is the total variation

```text
Delta phi = delta phi + chi^a nabla_a phi = 0.
```

Because `phi` is constant tangentially on the seal, the regular local relation is

```text
delta phi + chi_normal nabla_normal(phi) = 0.
```

This is not the old fixed-surface condition `delta phi=0`. At a regular seal with nonzero normal
slope, imposing both equations gives a rank-two system and forces

```text
chi_normal=0.
```

Therefore the free-boundary premise cannot simply be stacked on top of the fixed-seal variation. It
requires a correlated moving-surface tangent in which `delta phi` changes as the boundary moves.
This does not contradict the static canon; it marks the limit of that canon's fixed-surface scope.

If the full gradient vanishes, the displacement is algebraically free, but `phi=0` no longer defines
a regular level surface there. If the free boundary is not locked to `phi`, it remains a distinct
geometric object and the boundary/seal identification must be separately derived.

## Global versus local equation count

A single global size variable yields one number `dS_on-shell/dR_cell=0`. It cannot supply local
boundary conditions for several metric functions at every boundary point.

A local embedding `X^a(y)` has four component functions in four dimensions. Three are tangential
reparameterizations, leaving one physical normal shape function. Varying it yields one scalar shape
equation. The L02 metric boundary phase space still contains six induced-metric channels. L01 has
induced-metric, trace-free normal-jet, presymplectic, and corner channels. One shape equation does not
choose their polarization.

For a `phi`-locked embedding, one correlation joins `delta phi` and normal displacement, but all
angular, off-diagonal, common-scale, extra-field, and corner channels remain.

## Covariance can make displacement redundant

For either diffeomorphism-covariant conditional lane,

```text
J_chi = Theta(g,L_chi g)-i_chi L,
dJ_chi = -E.L_chi g.
```

If an unmarked boundary and every field are merely dragged by the same diffeomorphism, the
displacement may be gauge/reparameterization data. On shell, the corresponding current is closed;
this is a Noether identity or charge statement, not automatically a new physical shape equation.

A physical shape equation requires a relationally marked boundary, a declared embedding-field
split, and the boundary primitive. Current UDT data do not uniquely choose among those realizations.

## Conditional mirrored-seam cancellation

A finite mirrored cell might instead use the seal as an internal seam between two copies. Opposite
orientations give the exact two-sided structure

```text
Theta_total = Theta_plus-Theta_minus,
T_total = T_plus-T_minus.
```

Both vanish when the complete fields and shape responses match. This is a real conditional route by
which an apparent external boundary flux could cancel.

But the cancellation presupposes the missing object: the complete time-on/angular/normal coframe
soldering, orientation, field matching, boundary functional, and corners. With unmatched data the
variation gives jump equations rather than automatic cancellation. A common seam displacement may
also be quotient gauge. The word “mirror” does not provide the full matching law.

## Application to the conditional lanes

For L01, the raw field channels remain

```text
4 alpha C*nabla(delta g)-4 alpha nabla(C)*delta g + Euler + corners.
```

For L02 they remain

```text
kappa[nabla_b(delta g^ab)-nabla^a(delta g)] + Euler + completion/joints.
```

The extra displacement term `i_chi L` occupies an embedding channel. It cannot cancel arbitrary
independent `delta g`, normal-derivative, and corner channels. One relational-seal correlation still
leaves multiple independent channels in both lanes.

The free-boundary premise also does not provide equations for an independent `phi`, coframe,
projector, multiplier, connection, carrier, or bridge. L03 still has no functional to vary.

## `R_cell` is not yet `X_max`

The audit distinguishes:

- the conditionally varied `R_cell` modulus;
- the static `phi=0` fold;
- the WR-L asymptotic endpoint; and
- global `X_max`, an owner-locked output whose value and exact origin remain open.

No equation presently identifies these. A future global functional might let cell-size stationarity
participate in determining `X_max`, but only after the complete metric, boundary, matter/source,
total mass, proper volume, and observational-anchor placement are known. This audit does not insert
that join by definition.

## Remaining functional dependence

Eight exact classes remain visible after varying the seal:

1. the boundary functional itself;
2. Euler `beta` and its boundary completion;
3. exact bulk divergences;
4. symplectic-potential improvements;
5. boundary Legendre transforms;
6. intrinsic boundary or embedding counterterms;
7. orientation, reference, generator, and joint choices; and
8. overall action normalization.

Their survival is why the correct result is “adds transversality,” not “derives the boundary
action.”

## Evidence gates and stop

1. **Preregistered:** yes, commit `c95009f` before algebra.
2. **Full or bounded scope:** complete for one global modulus, a local codimension-one embedding,
   relational `phi` lock, pure diffeomorphism, null/type-changing branches, mirrored internal seam,
   both P05 bulk lanes, and all 21 field pairs. It is not a complete global solution.
3. **Independently verified:** a non-importing implementation reconstructed 22 algebraic checks and
   rejected 67 deliberate corruptions. A fresh adversarial-context scientific review is not yet
   complete, so the package remains `LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW`.
4. **Premises audited:** yes. Free-boundary status, global-versus-local variation, homothety,
   relational locking, action lanes, functional choices, mirrored matching, and `X_max` separation
   are explicit.

Maximum conclusion:

```text
FREE_GLOBAL_SEAL_TRANSVERSALITY_SELECTOR_STATUS_CLASSIFIED
```

No P06 solve, time integration, GPU work, native action, boundary functional, carrier, source,
mass, scale value, `X_max`, or canon entry was selected.
