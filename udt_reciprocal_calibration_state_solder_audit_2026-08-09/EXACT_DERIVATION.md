# Exact derivation — the reciprocal calibration-state solder

Date: 2026-08-09

## 1. Landing

```text
ABSTRACT_RECIPROCAL_CALIBRATION_LINE_DERIVED;
PAIR_RELATIVE_CAUSAL_FLAG_CONDITIONALLY_CONSTRUCTIBLE_ON_REGULAR_QUERIES;
NO_NONZERO_ORDER_ZERO_OR_FIRST_METRIC_JET_NATURAL_SOLDER;
STATIONARY_KILLING_SOLDER_CONDITIONAL_POSITIVE;
GENERAL_BILOCAL_GLOBAL_CALIBRATION_STATE_FUNCTOR_OPEN.
```

This is a real narrowing. The missing observer-pair law is not hidden in ordinary local
orthonormal-frame transport. Metric-compatible transport preserves precisely the clock/ruler
densities whose unequal scaling the founding reciprocal law needs.

The foundation owns an abstract reciprocal calibration representation. A regular observer query
can conditionally supply its causal directions. The still-missing object is a physical calibration
state—an unnormalized relational standard, section, or global/bilocal structure—whose comparison
can be non-isometric.

## 2. The derived abstract calibration line

For a supplied causal flag

```text
F=(L subset P),  dim L=1, dim P=2,
```

the reciprocal-root character is

```text
delta_RF=(1/2)b2-b1,
```

where `b1` is clock-line logarithmic density expansion and `b2` is clock/ruler-plane logarithmic
area expansion. This is the logarithmic character of the positive density line

```text
C_F = |Lambda^2 P|^(1/2) tensor |L|^(-1).
```

The equivalent multiplicative clock calibration is

```text
Lambda_RF=exp(-2 delta_RF)=rho1^2/rho2.
```

On the founded reciprocal operator

```text
D(t)=diag(exp(-t),exp(+t),1,1),
```

one has

```text
rho1^2=exp(-2t),  rho2=1,  Lambda_RF=exp(-2t).
```

Thus the associated calibration line is not invented. It is the exact representation carried by
the conditional flag law. But a representation is not yet a physical state or trivialization of
that line. The latter is the solder problem.

## 3. What a regular ordered query can construct

If the query supplies:

1. a future unit observer clock `u_p`;
2. an ordered event pair `(p,q)` joined by a unique regular spacelike branch; and
3. a choice of that branch,

then the normalized initial tangent `n_p` gives

```text
F_p=(span(u_p) subset span(u_p,n_p)).
```

The exact flat control

```text
u=(1,0,0,0),  n=(0,3/5,4/5,0)
```

has Gram matrix `diag(-1,+1)`. This is a valid pair-relative causal flag and does not introduce a
global preferred congruence.

The construction remains conditional for three reasons:

- an abstract founding observer comparison does not itself supply worldlines, simultaneity, or the
  event pairing needed to define a spacelike branch;
- at a cut locus or with multiple branches the direction is multivalued;
- exact cocycle composition requires carrying the target flag of the first leg into the second.
  Independently recomputing a preferred flag for each leg need not give the same intermediate
  state.

Most importantly, Levi-Civita transport of this flag preserves its Gram densities. It constructs
directions, not reciprocal calibration.

## 4. Endpoint coframe matching cannot provide nonzero depth

Let endpoint coframes be linear maps `E_p,E_q` with

```text
g_p=E_p^T eta E_p,
g_q=E_q^T eta E_q.
```

The natural map matching their orthonormal components is

```text
A=E_q^-1 E_p.
```

Exactly,

```text
A^T g_q A=g_p.
```

Therefore `rho1=rho2=1` and `delta_RF=0`. If the endpoint coframes are only presentations of the
metric, changing their independent Lorentz gauges changes their component-matching map but not the
zero-density result.

The tempting coordinate identity is not a replacement. Consider the same flat geometry written at
the two endpoints with

```text
g_p=eta,
g_q=T^T eta T,
T=diag(1/2,2,1,1).
```

Using component identity `A=I` produces the false strain

```text
g_p^-1 g_q=diag(1/4,4,1,1),
```

which looks exactly like reciprocal depth `log 2`. The correct component map is `T^-1`, and it is
an isometry with zero depth. Thus chart identity can manufacture the answer from presentation.

## 5. The local no-go through first metric jets

### Order zero

At a point, the Lorentz metric and a normalized flag contain only the fixed Gram values

```text
g(u,u)=-1, g(n,n)=+1, g(u,n)=0.
```

No nonconstant calibration scalar follows. Endpoint orthonormal coframes give the isometric result
above.

### First metric jet

At every regular point one may choose normal coordinates with

```text
g=eta, partial g=0, Gamma^g=0
```

at that point. A diffeomorphism-natural local one-form depending only on `(g,partial g)` must have
the same value in this control and transform under the full Lorentz isotropy. There is no nonzero
Lorentz-invariant covector. Hence no nonzero metric-natural first-jet calibration one-form exists.

The complete coframe does not evade the theorem if endpoint-frame covariance is retained. Its 24
first-jet components beyond the 40 metric jets are local Lorentz presentation directions.

The raw coframe current displays the issue explicitly. For `J=dE E^-1`, a local frame change gives
an inhomogeneous term `dLambda Lambda^-1`. The reciprocal self-adjoint projection happens to
annihilate a pure Lorentz term when the flag is transformed correctly, but coordinate
reparameterization still creates a false current. Flat space in the coordinate `t=exp(t')` has

```text
E'=diag(exp(t'),1,1,1),
(1/2)Tr(H dE' E'^-1)=-1/2 dt',
H=diag(-1,+1,0,0).
```

The Levi-Civita covariant derivative cancels it exactly. Covariantizing does not uncover hidden
dilation; it removes the presentation artifact.

The no-go is sharply scoped to local order-zero/first-metric-jet constructions. It does not rule
out curvature, global completion, branch symmetry, boundary-normalized data, or dynamics.

## 6. Metric-derived path candidates

### Levi-Civita transport

It is the unique torsion-free metric-compatible first-order connection. It composes and reverses
exactly, but

```text
P_gamma^T g_q P_gamma=g_p
```

so every graded density character is zero.

### World function and separation

The world function supplies regular branch directions and a symmetric separation magnitude. It is
not a signed additive cocycle. In a flat spatial triangle with side lengths `1,1,sqrt(2)`,

```text
1+1 != sqrt(2).
```

This is not a defect: distance and ordered reciprocal depth are different types.

### Differential of the exponential map

This map is curvature sensitive but does not compose as a four-dimensional subdivision functor.
On a unit constant-curvature control, the transverse factor is `sin(r)/r`. For two segments of
length `pi/6`,

```text
[sin(pi/6)/(pi/6)]^2 = 9/pi^2,
sin(pi/3)/(pi/3) = 3 sqrt(3)/(2 pi),
```

and the values differ. The map also becomes singular at conjugate points and branches at cut loci.

### Full Jacobi propagation

The phase state `(J,nabla J)` has an exact compositional propagator. For one unit-curvature
transverse mode,

```text
F(r)=[[cos r,sin r],[-sin r,cos r]],
F(a+b)=F(b)F(a).
```

Its position block does not compose: `sin(a+b) != sin(a)sin(b)`. Reducing the eight-dimensional
state to a four-dimensional arrow needs a congruence, Lagrangian polarization, optical/Riccati
state, or other supplied reduction.

### Cartan development

Development composes in an affine group after a path and initial frame are supplied. Its linear
part is Levi-Civita and isometric. The translation records displacement but is not the linear
reciprocal-root density character.

### Van Vleck/focusing data

These are valid metric-derived bilocal scalars on a regular geodesic branch, but generic focusing
does not multiply under arbitrary subdivision. They do not satisfy the exact calibration cocycle
without extra state.

## 7. Higher-order naturality proves nonuniqueness, not impossibility

The prior flag audit supplied the exact family

```text
nabla^(c)_X Y = nabla^g_X Y
  + c[(dR)(X) Ric^sharp(Y)+(dR)(Y) Ric^sharp(X)].
```

On its registered warped control, it gives

```text
delta_RF=-3c.
```

Every `c` is diffeomorphism-natural and its parallel transport composes. Other curvature tensors
and functions generate still more families. Therefore metric naturality, covariance, and
composition do not uniquely select a higher-order nonmetric arrow.

The conclusion is not that higher-order geometry is irrelevant. It is that an additional branch,
global, or dynamical owner must select it.

## 8. The stationary positive branch

If a complete branch has an intrinsic timelike Killing line `K`, its unnormalized norm

```text
N=sqrt(-g(K,K))
```

defines

```text
delta_K(p,q)=log[N(p)/N(q)].
```

It composes, reverses, and is independent of constant rescaling of `K`. Unlike unit-vector
parallel transport, the common unnormalized symmetry generator supplies a genuine calibration
state whose norm can vary between endpoints.

This is the prototype of the missing solder and an important positive result. It is only
`CONDITIONAL_BRANCH_LOCAL`: nonstationary branches need not have such a line, and no current
premise selects a universal replacement.

## 9. Global and degenerate strata

| Situation | Exact status |
|---|---|
| transported clock line becomes null | `rho1=0`; logarithmic character fails/diverges |
| clock/ruler plane degenerates | `rho2=0`; density line and reciprocal root fail |
| ruler direction is ambiguous | flag becomes a family/set; no unique scalar without a selector |
| multiple paths exist | path-labelled values may differ; endpoint descent needs zero periods |
| pair approaches coincidence | identity depth is zero, but separation direction can lose a unique limit |
| conjugate point/cut locus | `dexp` can become singular; geodesic branch is nonunique |
| no global flag section | local/query groupoid survives; one global endpoint field does not |

These are genuine domain boundaries, not reasons to add a cutoff or choose a convenient branch.

## 10. `c_eff` and the physical calibration join

The associated-line multiplier

```text
exp(-2 delta_RF)
```

is derived mathematics. On the founded pure reciprocal branch it equals the established
`exp(-2delta)` calibration factor. Calling it the universal physical
`c_eff(q)/c_eff(p)` requires the physical calibration state, arrow, and trivialization that this
audit finds still open.

The stationary Killing branch supplies one conditional realization. The general mixed complete
case remains an `OPEN_CONSISTENT_EXTENSION`, not a contradiction and not a silent redefinition.

## 11. What was actually ruled out

Ruled out within exact scopes:

- a chart/component identity as the physical comparison;
- endpoint orthonormal coframe matching as nonzero dilation;
- Levi-Civita transport as nonzero dilation;
- metric distance as signed additive depth;
- the four-dimensional exponential differential as a compositional arrow;
- a raw local coframe first-jet current as a universal metric-natural answer; and
- uniqueness from higher-order metric naturality alone.

Not ruled out:

- branch-derived unnormalized symmetry or recurrent lines;
- complete-solution/global calibration sections;
- bilocal structures with a carried internal state;
- boundary-normalized structures if a genuine boundary is derived;
- a native dynamical selector; or
- stratified laws with explicit transition ownership.

No action, source, matter, mass, boundary completion, `X_max` value, CMB spectrum, signaling law, or
canonization follows.
