# Exact derivation — native-law home, codomain, and variation ownership

## 1. The phrase “the native law” is not one type

The current ledger already contains two inequivalent exact object types.

The founded reciprocal comparison is an arrow law. For a supplied signed additive depth,

```text
D(rho)=diag(exp(-rho),exp(rho)),
D(rho_2)D(rho_1)=D(rho_1+rho_2),
D(-rho)=D(rho)^-1.
```

It maps the reciprocal pair fiber at the source query to the corresponding fiber at the target.
Under a pair-frame reset it transforms equivariantly. It is therefore naturally a typed morphism on
the observer-pair/path query groupoid, not one bare tensor at an event.

The ambient metric, its Levi-Civita connection, curvature, causal classification, and any supplied
base-boundary geometry live on spacetime `M`. They are independent of which pair query is asked.
The connection is an affine connection rather than a tensor, but it is still base geometry.

These homes cannot be collapsed without erasing information. A faithful current description is
therefore necessarily typed/layered as bookkeeping. This does **not** select one layered dynamical
law.

## 2. Basicness and equivariance remain different

At one base point use

```text
P_01=diag(1,1,0,0),  P_02=diag(1,0,1,0),
A=diag(2,3,5,7),     P_02=R_12 P_01 R_12^-1.
```

The query response

```text
L_Q(P,A)=trace(PA)
```

is equivariant when both inputs transform, but at fixed ambient `A` it returns `5` and `7` on the
two valid pair planes. The basic response `trace(A)=17` does not change with the query. Thus an
equivariant query law need not descend to a base tensor or scalar.

This supplies a logical control, not a UDT field equation. It proves only that covariance cannot by
itself choose the home.

## 3. A query-space formula still needs a quantifier

The same expression `L(g,q)` has different meanings under different quantifiers:

1. `SUPPLIED_QUERY_READOUT`: evaluate it for the pair/path being compared. The query is an argument,
   not a varied field.
2. `UNIVERSAL_ALL_QUERIES`: require `L(g,q)=0` for every query in every fiber. The residual is
   nonbasic, but the resulting set of allowed metrics can be observer independent. Variation is of
   `g`; `q` is quantified, not varied.
3. `EXISTENTIAL_QUERY`: require some witness query. This does not identify a physical reduction.
4. `REALIZED_SECTION`: evaluate `L(g,s(x))` on a physical field `s`; an independent `delta s` exists
   only after physical ownership is supplied.
5. `BRANCH_DERIVED_SECTION`: evaluate `L(g,S[g])`; the section is not varied independently.
6. `SET_VALUED_STRATIFIED`: retain the orbit or tile family where no unique member exists.
7. `FIBER_AGGREGATED`: integrate or quotient over queries; unavailable without native aggregation
   data.

The founding postulates select the first meaning for founded comparison/readout. They do not state
which quantifier defines native dynamics.

## 4. Variation ownership

For a basic candidate law `F(g)=0`, the prospective tangent is `delta g` modulo declared
presentation gauge, but the current foundation has not defined the admissible physical tangent
space or the codomain of `F`.

For a query law `L(g,q)`, changing `q` changes the question. It is not an Euler–Lagrange variation.
Under the universal quantifier one varies `g` while enforcing the family of equations for every
`q`.

For a realized field architecture `L(g,s)=0`, `delta s` is an independent physical tangent only if
UDT first owns `s` as field data. Merely showing that sections exist does not supply that ownership.
Moreover, the project rule “the metric is the theory” makes an independent `s` conditional extra
structure unless it is proved to be metric/coframe configuration data.

For a branch-derived reduction `s=S[g]`,

```text
delta L(g,S[g])
 = partial_g L[delta g] + partial_s L[DS_g[delta g]].
```

The second term cannot be dropped. The exact simple-spectrum control gives a nonzero chain term.
For

```text
A=diag(2,3,5,7),
P=projector onto the first two eigenlines,
delta A_12=delta A_21=1,
```

the spectral-projector derivative has

```text
(delta P)_12=(delta P)_21=-1/2.
```

Against the off-diagonal control `B_12=B_21=1`,

```text
trace((delta P)B)=-1.
```

So treating the derived plane as fixed changes the variation.

At a repeated eigenvalue, two regular isometry-related paths reach the same collision parent with
limits `P_01` and `P_02`. No unique derivative exists there. The same ownership failure applies at
the registered intrinsic-form zeros, null/zero `dphi`, causal-type changes, tie/Jordan/complex
spectra, rank changes, and boundary-defect intersections. A stratified/interface law is still open.

## 5. What the founding postulates actually force

They force the home and codomain of the object they directly derive:

```text
ordered reciprocal comparison
  home: observer-pair/depth query arrows;
  codomain: reciprocal pair-fiber morphisms preserving the dual pairing;
  variation: none as a field equation; query changes are changes of argument.
```

The supplied metric forces the mathematical home of its definitions:

```text
ambient metric geometry
  home: M and its ordinary geometric bundles;
  codomain: metric/connection/curvature/causal/boundary objects;
  variation: not supplied merely by defining those objects.
```

Pair-resolved screen, mixing, projected curvature, and polarization live naturally over the query
bundle. They become base objects only after a realized/branch-derived reduction or a still-open
aggregation/quotient rule.

The founding postulates do **not** specify the input-to-output type of the missing dynamical law.
Exact mutually compatible extensions include a base residual, a nonbasic equivariant query
residual with a declared quantifier, or a regular metric-derived reduction with the chain rule.
None violates the reciprocal character. Therefore current foundations do not select the complete
dynamical home, codomain, or physical variation domain.

## 6. Constraint from “the metric is the theory”

This rule narrows interpretation without manufacturing a law:

- a basic law on metric configurations is compatible;
- an equivariant query law is compatible when the query bundle is derived from the metric and the
  query is an argument rather than a new field;
- a branch-derived reduction is compatible on its regular domain;
- a stratified metric-derived continuation is compatible in principle;
- an independently realized section is extra physical structure unless it is shown to belong to
  the metric/coframe configuration itself;
- fiber aggregation is compatible in principle only if every aggregation datum is metric-derived.

This is a purity constraint, not a selector among the surviving metric-owned routes.

## 7. SNe compatibility anchor

The registered conditional static WR-L branch has distinct readouts

```text
clock:          u=1+z=exp(phi),
areal radius:   r/X=1-u^-2,
optics:         d_L/X=u^2(r/X),
proper pair:    a separately typed pair-distance slot.
```

The exact composition gives

```text
d_L/X=u^2(1-u^-2)=u^2-1=z(z+2).
```

No fit is rerun. The anchor requires a downstream codomain with at least the four distinct typed
slots `clock`, `areal`, `optical`, and `proper_pair`. A formulation that necessarily identifies
them is incompatible with the registered branch.

This does not distinguish a basic, query, realized-section, or branch-derived native **dynamical**
law. Each can feed the same downstream readout map once a solution and observer query are supplied.
Observed equality of readouts would not imply equality of upstream homes. The SNe result therefore
constrains the dashboard interface, not the engine architecture.

## 8. Codomain ruling

The codomains currently forced or bounded are:

- founded kinematics: reciprocal fiber morphisms / the one-parameter `O(1,1)` character;
- ambient geometry: ordinary metric, connection, curvature, causal, and boundary objects on `M`;
- pair response: associated-bundle objects over query space, or their reduction pullbacks;
- SNe compatibility: a product of distinct clock, angular-area, optical, and proper-pair readout
  slots;
- bootstrap: at most a future relation/admissibility object on complete on-shell global/local
  observables, not a presently derived scalar equation;
- native dynamics, source, and boundary response: open target bundles or relation types.

Nothing presently requires the missing native law to be Euler–Lagrange, action-valued, local, or a
single tensor equation.

## 9. Maximum conclusion

```text
FOUNDED_COMPARISON_HOME_AND_CODOMAIN_DERIVED_AS_EQUIVARIANT_TYPED_QUERY_KINEMATICS;
AMBIENT_METRIC_GEOMETRY_HOME_DEFINED_ON_SPACETIME;
PAIR_RESOLVED_RESPONSE_REQUIRES_QUERY_TYPING_OR_METRIC_OWNED_REDUCTION;
FAITHFUL_CURRENT_DESCRIPTION_IS_TYPED_AND_LAYERED;
COMPLETE_NATIVE_DYNAMICAL_HOME_CODOMAIN_QUERY_QUANTIFIER_AND_VARIATION_DOMAIN_NOT_SELECTED;
SNE_IS_A_CONDITIONAL_DOWNSTREAM_CODOMAIN_COMPATIBILITY_ANCHOR_ONLY.
```

No action, source, carrier, boundary functional, bootstrap equation, density, physical branch,
`X_max`, mass, matter, or dynamics is derived.

