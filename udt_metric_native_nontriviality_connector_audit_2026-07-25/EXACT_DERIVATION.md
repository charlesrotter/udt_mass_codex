# Exact nontriviality-connector derivation

## 1. The coupled tuning operator

Let `X` be the complete finite-cell configuration and `O` independent global
data. The owner mutual-tuning hypothesis requires both

```text
A(X,O)=0,
O-R[X]=0.
```

The full linearization is

```text
J_C = [[A_X, A_O],
       [-R_X,  I ]].
```

The second row gives `delta O=R_X delta X`. Substitution into the first row
gives the exact reduced tuning operator

```text
S = A_X + A_O R_X.
```

On the common tangent/operator domain of both differentiated equations,

```text
ker J_C = {(xi,R_X xi): S xi=0} ~= ker S.
```

This graph identity needs `A` and `R` differentiable at the same root, with
the same boundary domain; it does not need `A_X` to be invertible. For
compatible finite square blocks, `det J_C=det S`. The executable scalar and
matrix controls reproduce both statements exactly.

This formula exposes the chicken-and-egg effect. `A_X` is the local branch
response at fixed global data. `A_O R_X` is the feedback obtained when a local
change alters the recomputed global data and those data act back on the local
branch equation.

Exact controls show that feedback can:

- make `S` singular even when `A_X` is regular; and
- make `S` regular even when `A_X` alone is singular.

This is an exact conditional architecture. Current UDT has not supplied the
complete `A`, `R`, their common domain, or their placement on one physical
finite-cell branch.

## 2. What a kernel means

A nonzero vector in `ker S` is a necessary infinitesimal condition for loss of
regularity or a tangent branch of the coupled closure. It is not sufficient
for matter emergence.

Three exact countercontrols enforce the distinction:

1. `A=x+o+x^3`, `R=-x` reduces to `x^3=0`. Its unique realized root is zero
   and its linearization is singular, yet it has no nearby nonzero real root.
2. A rank-one operator can have a kernel consisting entirely of a declared
   gauge coordinate.
3. A local kernel can be eliminated by one compatible finite-cell boundary
   condition.

A stronger branch control holds the linearization fixed. Both
`x^2+lambda^2=0` and `x^2-lambda^2=0` have zero first derivative at the
origin. Over the reals the first has only the isolated origin, while the
second factors into the two crossing branches `x=+lambda` and `x=-lambda`.
Thus even the same singular linearization does not determine whether a
nontrivial nonlinear branch exists.

Therefore a physical nontriviality claim additionally requires gauge
reduction, the complete boundary domain, global descent, nonlinear branch
existence, and ultimately a persistence or stability law.

The same-root counterfamily also proves that a realized closed universe does
not determine whether its closure linearization is regular or singular.

## 3. The local clock-curvature candidate

For a two-dimensional screen tidal operator `T` and reciprocal clock rate
`a`, the exact candidate is

```text
det(T+a^2 I)=0.
```

In a screen eigenframe this is

```text
(k1+a^2)(k2+a^2)=0.
```

When exactly one eigenvalue equals `-a^2`, the kernel is one-dimensional and
the intrinsic projector is the previously derived `P_clock`. When both
eigenvalues equal `-a^2`, the screen is degenerate and no unique line is
selected.

This is the strongest concrete local nontriviality candidate in the source
universe. It supplies no complete global branch, parallelism, finite-cell
descent, recomputation map, or bootstrap feedback.

## 4. Why scalar traces are too coarse

For the candidate curvature integral `I_R=integral sqrt(h) R`, the trace-free
bulk response in an orthonormal Ricci eigenframe against
`H=diag(1,-1,0)` is

```text
-r1+r2.
```

The two algebraic Ricci triples

```text
(1,2,3),
(0,3,3)
```

have the same scalar trace `6` but responses `1` and `3`. Thus an unstructured
scalar curvature value alone does not determine the pointwise trace-free Ricci
response. This is not a pair of globally realized same-branch metrics with
equal integrated curvature; the candidate functional remains boundary
incomplete and unselected.

Proper-volume variation is trace-only. Density adds

```text
delta rho=(delta M-rho delta V)/V,
```

so its trace-free response requires the still-absent native mass variation.

Consequently neither one density scalar nor one unstructured scalar-curvature
datum can implement the owner orchestra hypothesis. A successful closure may need
structured tensorial, spectral, directional, boundary, or holonomy data—or a
native mass/energy response. Which data are native remains open.

## 5. Local transport versus global descent

A local connection transports vectors along a path. A globally descending
section requires its closed-loop holonomy to fix the section. The exact
rotation control gives

```text
det(Hol(theta)-I)=4 sin^2(theta/2).
```

At `theta=pi/2`, local transport is perfectly defined but no nonzero fixed
vector exists. Likewise a `GL(2,Z)` exchange preserves the full toric
character module while exchanging two individual lines.

This blocks promotion of Kato transport, a local projected toric connection,
or a systolic chamber line into a global section without monodromy, cap,
mirror, and boundary data.

## 6. Critical strata do not yet form one mechanism

The source universe contains several exact rank or transition loci:

- the coupled tuning kernel;
- the clock-tidal kernel;
- angular shortest-character walls;
- null `dphi` degeneration of the reciprocal `3+3` split;
- curvature reducibility strata; and
- determinant-one cap topology.

They are catalogued in `CRITICAL_STRATA_ATLAS.tsv`. Their repeated appearance
is a useful structural pattern, but they act on different objects and have no
derived common selector. Conflating them would recreate the cross-branch
splicing error the audit is designed to prevent.

## 7. Candidate result

No row in the effective thirteen-candidate universe passes all nine gates.
The original twelve-row universe is preserved, with C13 added through the
preregistered append-only correction rule.

- `C01` supplies the exact conditional two-arrow nontriviality skeleton.
- `C02` is the strongest local kernel candidate.
- `C03` is the strongest concrete object with both local trace-free response
  and a global integral type.
- `C10` supplies the unavoidable moving-boundary response slot.
- Its global-to-local use is provenance-blocked until a native boundary
  functional is selected; varying the seal cannot select that functional.
- No one complete branch co-locates those three roles.
- `C12`, native energy/mass response, remains absent.
- `C13`, general Levi-Civita curvature holonomy, is a bounded local atlas only;
  no closed-loop theorem or bootstrap arrow exists.

The smallest missing object is not another critical condition. It is a pair
of complete, same-branch maps `A(X,O)` and `R[X]`, including gauge-reduced
field domains, moving boundary/corner data, global descent, and nonlinear
branch regularity.

## 8. Maximum conclusion

```text
EXACT_COUPLED_NONTRIVIALITY_SKELETON
NO_COMPLETE_METRIC_NATIVE_BOOTSTRAP_CONNECTOR
```

The result makes the bootstrap hypothesis more precise and more testable. It
does not derive matter, energy, mass, an action, or a physical branch.
