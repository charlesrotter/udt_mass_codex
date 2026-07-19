# Reciprocity off-shell constraint selector — derivation report

Date: 2026-07-18
Branch: `codex/reciprocity-offshell-constraint-selector-2026-07-18`
Preregistration commit: `750d48b`
Authority: bounded selector theorem and route classification; not canonization

## Ruling

The displayed representative relation

```text
(-g_tt/c^2) g_parallel_parallel = 1
```

is not a nontrivial diffeomorphism- and CSN-invariant scalar constraint of the metric alone. In the
preregistered local order-zero class, no such `C[g]` exists: the general linear group acts
transitively on Lorentz metrics of fixed signature at a point, so every algebraic natural scalar of
one metric is constant.

After a time/parallel pair and representative are chosen, the two positive block coefficients have
the exact decomposition

```text
a = exp(2 sigma-2 phi),
b = exp(2 sigma+2 phi),
sigma = (1/4) log(a b),
phi   = (1/4) log(b/a).
```

Common-Scale Neutrality shifts `sigma` and leaves `phi` unchanged. Therefore `a b=1` sets
`sigma=0`: it is representative gauge fixing. The reciprocal depth is the ratio, not an equation
that fixes the common scale.

The preregistered outcome is
`NO_L0_CONSTRAINT_REPRESENTATIVE_IDENTITY_IS_GAUGE_READOUT`. This is a theorem only for a local,
pointwise, algebraic scalar of one metric. It does not exclude a derived coframe/vector structure,
curvature or other derivative law, nonlocal finite-cell selector, or post-scale constraint. None of
those broader routes is presently supplied, and no auxiliary field is required by this result.

Consequently Reciprocity remains a derived kinematic comparison with a conditional metric readout;
it is not currently a derived off-shell metric constraint. The field census is narrowed but remains
`OPEN`.

## T1 — controlling premise audit

The current C1/final ledger separates four layers that older shorthand can blur:

| Layer | Current status | Consequence here |
|---|---|---|
| Reciprocal-c and dual UDT Reciprocity | `FOUNDING` | Their faithful internal pairing gives determinant-one comparison `uv=1`. |
| Reciprocal exponential comparison | `DERIVED / CONDITIONAL` | Requires positive additive depth, composition, reversal, regularity, and chosen sign/unit. |
| Lorentzian reciprocal metric block | `CONDITIONAL` | Requires a quadratic readout, CSN representative, and spatial-slot identification. |
| Off-shell fields/constraint domain | `OPEN` | Metric-only, coframe, scalar, multiplier, hard restriction, and readout routes remain live. |

The dimension-matched pair in C1 is a faithful formalization of the founding duality. It is not a
derived global spacetime coframe field. The parallel slot is conditional outside a gradient-adapted
frame. Bulk diffeomorphism covariance remains a trial, and the full mirror-preserving boundary group
is open. Those qualifications control the conclusion.

## T2 — the component product is not a scalar

Write the adapted two-coordinate block, suppressing the fixed conversion unit `c`, as

```text
g = diag(-a,b),  a>0, b>0.
```

Under independent coordinate rescalings

```text
t_new=alpha t,  x_new=beta x,
```

the components become

```text
g_tnew,tnew = -a/alpha^2,
g_xnew,xnew =  b/beta^2,
```

and their positive product becomes

```text
a b -> a b/(alpha^2 beta^2).
```

Thus a unit product maps to `1/4` under `alpha=2`, `beta=1`. Coordinate covariance is restored only
if the time/parallel frame is carried as additional geometric data. Without that data, the raw
component equation cannot be a spacetime scalar constraint.

This does not reject a preferred chart categorically. It says that such a chart or frame would have
to be derived as native structure; current Reciprocity does not silently supply it.

## T3 — Common-Scale Neutrality separates gauge from depth

Every positive diagonal pair admits the exact decomposition

```text
a b = exp(4 sigma),
b/a = exp(4 phi).
```

Under `g -> Omega^2 g`, both `a` and `b` acquire `Omega^2`, so

```text
sigma -> sigma + log(Omega),
phi   -> phi.
```

The founding CSN equivalence quotients the first transformation. Choosing `Omega=exp(-sigma)` gives
the determinant-one representative `a b=1`. No equation for `phi` has been imposed. Conversely,
`phi=(1/4)log(b/a)` is a CSN-invariant definition of reciprocal depth once the paired slots exist.

Therefore the determinant-one comparison is physical at the internal dual-pairing layer, but its
metric component product is a representative statement after the conditional metric readout. The
same mathematics cannot be counted twice as both a derived kinematic identity and a new physical
off-shell constraint.

## T4 — order-zero metric-only natural-scalar theorem

Let `V` be a four-dimensional tangent space. Any two nondegenerate symmetric bilinear forms on `V`
with Lorentz signature are related by a general linear change of frame. In particular,

```text
eta = diag(-1,1,1,1),
A   = diag(sqrt(a0),sqrt(a1),sqrt(a2),sqrt(a3)),
g   = A^T eta A = diag(-a0,a1,a2,a3).
```

A pointwise scalar `F(g)` natural under diffeomorphisms must obey

```text
F(A^T g A)=F(g).
```

Because the `GL(4)` action is transitive on the fixed-signature orbit, `F` is constant on the entire
space of Lorentz metrics at a point. It can report dimension, signature, or a numerical contraction
such as `g^{mu nu}g_mu nu=4`, but it cannot distinguish a reciprocal component block.

This closes `L0_METRIC_ONLY_ORDER_ZERO` exactly. It does not use field equations, an approximation,
or a search over examples.

Natural tensors and densities must be distinguished from this scalar theorem. The metric, inverse
metric, and—after choosing orientation—metric volume form are natural objects, but an order-zero
tensor equation made from them alone is an identity, a constant contraction, or an inconsistent
zero condition unless another tensor/density supplies a comparator. They do not select a
time/parallel component product.

### Why the determinant does not evade the theorem

`det g` is not a scalar. Under a change of frame it acquires the square of the Jacobian determinant,
and `sqrt(|det g|)` is a density. An equation such as

```text
sqrt(|det g|) = fixed density
```

requires a reference volume form or coordinate density. That is extra structure and, if fixed
locally as physical, conflicts with the pre-scale CSN equivalence. A dynamically or globally
selected volume form remains an L2/L4 possibility, not an L0 construction.

## T5 — strongest structured covariant candidate

Suppose explicit vector fields or geometric structures provide a timelike direction `T` and
parallel direction `N`. Then

```text
a = -g(T,T)/c^2,
b =  g(N,N)
```

are diffeomorphism scalars. This repairs the chart defect, but the construction is now
`C[g,T,N]`, not `C[g]`. It also does not repair CSN by itself:

```text
a b -> Omega^4 a b,
b/a -> b/a.
```

One may assign compensating Weyl weights to `T,N`, but those transformation laws and their global
existence are added premises. A coframe formulation uses one-form norms built with `g^{-1}` and hence
the opposite unweighted Weyl sign; it must be audited separately rather than conflated with the
vector formula. In either convention the common product is representative-dependent while the
relative ratio can be neutral after the transformation laws are declared. If `T,N` are normalized
by definition, the product equals one tautologically and supplies no dynamical equation. If
curvature eigenvectors are used to generate them, the construction becomes derivative-dependent,
is degenerate on flat/conformally symmetric configurations, and requires a branch/regularity rule.
The mathematically allowed `phi=0` geometry therefore blocks any universal curvature-eigenframe
shortcut.

L2 remains `OPEN_EXTRA_STRUCTURE_NOT_DERIVED`. This is the most concrete escape from the L0 theorem,
but current C1 does not select its fields, weights, normalization, or bulk extension.

## T6 — readout, hard gauge, and multiplier

Let a pre-scale action be CSN invariant and depend only on the depth coordinate. The exact anchor

```text
S_0=(phi-phi_star)^2
```

is independent of `sigma`. Three implementations then give the same physical depth equation:

1. **Quotient/readout:** vary `phi`; leave `sigma` absent as gauge.
2. **Hard representative:** set `sigma=0`; vary `phi`.
3. **Gauge multiplier:** use `S=S_0+lambda sigma` and vary all declared variables.

The multiplier equations are

```text
2(phi-phi_star)=0,
lambda=0,
sigma=0.
```

The reaction vanishes. At field level, a complete differentiable action invariant under local CSN,
including its boundary terms and every Weyl-transforming field, supplies the corresponding Ward
identity. In a metric-only action this is the conformal trace identity; with weighted vectors,
coframes, or compensators it mixes their Euler terms. Holding those fields fixed would not justify
`lambda=0`. The runnable anchor certifies only the metric-only interior case.

The term `lambda sigma` is gauge-fixing bookkeeping, not a CSN-invariant physical interaction. Its
global equivalence to quotient/readout variation additionally requires that the gauge slice be
reachable by transformations preserving the finite mirror, allowed boundary data, and corners.

A nonzero reaction can be manufactured by inserting `kappa sigma` into `S_0`; the multiplier then
gives `lambda=-kappa`. But the action shifts under `sigma -> sigma+omega` and violates founding
pre-scale CSN. The reaction is evidence of the inserted scale dependence, not evidence that
Reciprocity natively requires a physical multiplier.

This exact anchor does not prove universal equivalence of every gauge-fixing procedure. A complete
action, gauge group, boundary data, and representative-selection regime would still be needed. It
does show why the generic reactive multiplier example from the preceding trial cannot be assigned
to the reciprocal product without first proving that the constrained direction is physical rather
than calibrational.

After bootstrap or matter selects a physical representative, common scale may cease to be gauge in
the same way. A post-scale constraint could then be reactive, but its selection law and action are
additional physics and remain open.

## T7 — curvature does not rescue the component equation

Derivative natural scalars such as curvature invariants are genuine diffeomorphism scalars, and
some conformal combinations exist. They constrain the metric jet—derivatives as well as its value—so
they are not automatically equivalent to a pointwise calibration condition.

The direct counterexample is flat space in rescaled Cartesian charts:

```text
diag(-1,1)       has product 1 and curvature 0,
diag(-1/4,1)     has product 1/4 and curvature 0.
```

Hence `R=0`, `C_abcd C^abcd=0`, or any other condition depending only on the vanishing flat curvature
cannot be equivalent to the raw unit-product equation. More generally, satisfying a derivative
condition on one reciprocal ansatz proves only one implication and is insufficient for
equivalence.

This refutes the curvature shortcut, not all L3 theories. A derivative or nonlocal law might govern
the invariant depth after the needed spacetime structure is supplied. No complete inventory or
native selector presently exists, so L3 remains open.

## T8 — the finite cell does not yet supply the missing bulk structure

The mirrored cell gives a native global arena and, in the static `phi` sector, the seal parity
`phi=0` with free normal derivative. A boundary normal exists at the seal once the boundary structure
is declared. That does not by itself produce:

- a bulk timelike/parallel two-plane;
- a normalized coframe throughout the cell;
- a CSN representative or reference volume;
- a unique inward extension from the boundary;
- the complete mirror-preserving gauge group, corners, action, or generator.

A global boundary-value problem or spectral/geometric construction could potentially derive these
objects. A global `sigma=0` gauge would also need a positive `Omega` compatible with the mirror and
boundary data. That is the L4 route and remains `OPEN_NOT_SUPPLIED`; it is not excluded by the local
natural-scalar theorem.

## T9 — metric-led ontology and bootstrap

“The metric is the theory” prohibits importing an independently physical mechanism in place of
metric geometry. It does not turn a component into a scalar or derive a metric-only off-shell
closure theorem. The present result actually makes the metric-only limitation precise: the metric
alone has no nontrivial order-zero scalar capable of carrying the requested constraint.

The current bootstrap statement remains on-shell global closure/admissibility. It supplies neither
the missing paired spacetime structure nor a local constraint/multiplier. Neither maxim changes the
L2-L4 statuses.

## T10 — route ledger and next falsifiers

| Route | Ruling | Exact scope | What could change it |
|---|---|---|---|
| L0 metric-only order-zero `C[g]` | `REFUTED_IN_CLASS` | One Lorentz metric; local pointwise algebra; full bulk covariance trial | Reject covariance via a derived preferred frame, or enlarge fields/derivative order |
| L1 unit component product | `CSN_GAUGE_READOUT_CONDITIONAL` | Chosen paired frame and representative | Derive a different invariant interpretation or make common scale physical post-selection |
| Invariant reciprocal depth ratio | `DERIVED_CONDITIONAL_READOUT` | Same paired slots; `phi=log(b/a)/4` | Derive/revise the spacetime slot realization |
| L2 metric plus frame/projectors | `OPEN_EXTRA_STRUCTURE_NOT_DERIVED` | Covariant after structures are supplied | Derive their field status, weights, normalization, and global extension |
| Gauge multiplier for `sigma=0` | `ALLOWED_BOOKKEEPING` | CSN-invariant pre-scale anchor; zero reaction | Complete gauge theory and finite-cell boundary equivalence theorem |
| Physical reciprocal multiplier | `NOT_DERIVED` | No native physical `C[g]` or reaction supplied | Derive a post-scale or non-gauge constraint and its action |
| L3 derivative metric law | `OPEN`; curvature shortcut refuted | Curvature equality is not the raw component relation | Derive a two-way invariant law governing depth, including degenerate branches |
| L4 finite-cell/global selector | `OPEN_NOT_SUPPLIED` | Current mirror/parity record | Derive a covariant/nonlocal frame and representative-selection map |
| Metric-only off-shell closure | `NOT_DERIVED` | Current C0/C1 and accepted ledgers | Native configuration-space theorem |
| Auxiliary field requirement | `NOT_DERIVED` | L0 failure does not force an enlargement | Exact premise selecting a coframe/vector/scalar/multiplier |

## Smallest genuinely missing object

The immediate missing object is a **native natural selector/realization of the paired line
directions**:

```text
Are they only an internal comparison/readout, or a derived global line-pair/projector structure with
specified relative normalization, transformation law, degeneracy handling, and finite-cell
extension?
```

Only after that is known can a variation rule distinguish quotient, gauge-fixed, hard, multiplier,
or post-scale representative dynamics. This is earlier than choosing `C^2`, EH, locality, derivative
order, source, or mass.

## Completeness map — one bounded tile

| Criterion | Covered | Still open and capable of hosting structure |
|---|---|---|
| Fields | L0 one-metric class closed; L2 field additions exposed | Native coframe/vector/scalar census |
| Action terms | Gauge anchor only | Every physical invariant and coefficient |
| Full equations | Every anchor variable varied | Complete UDT equations and Ward identities |
| Domain/coordinates | Chart dependence and CSN quotient separated | Time-live charts, global frame, variation placement |
| Boundary/regularity | Current mirror content audited | Boundary/corner action, frame extension, generators |
| Topology | Not used | Line/coframe bundle existence and sectors |
| Dynamics | No dynamics inferred from kinematics | Local/nonlocal/derivative native law |
| Branches | L0-L4 route map | Degenerate structured and global branches |
| Stability | Not used | Stability of any completed realization |
| Regime | Exact local algebra/naturality plus logical route audit | Post-scale/material regime and controlled matching |

This result is one logical tile. It does not close the complete action or solution space.

## Four banking gates and authority boundary

1. `PREREGISTERED`: commit `750d48b` precedes the derivation.
2. `BOUNDED_SCOPE_JUSTIFIED`: L0 is exhaustive by the Lorentz-orbit theorem; L2-L4 are explicitly
   retained.
3. `INDEPENDENT_VERIFICATION_REQUIRED_BEFORE_BANKING`: recorded separately with exercised corrupt
   fixtures and two fresh adversarial reviews.
4. `PREMISES_AUDITED`: every field, frame, scale, covariance, boundary, and action premise is exposed
   in the ledger.

The work is CPU-only, carrier-free, and density-normalization-free. It promotes no action, edits no
frozen package or research artifact, does not integrate `grok`, and leaves repository reorganization
paused.
