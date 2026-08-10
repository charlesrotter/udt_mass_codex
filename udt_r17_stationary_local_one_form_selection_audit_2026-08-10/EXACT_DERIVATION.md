# Exact derivation — stationary R17 local one-form selection

Date: 2026-08-10

Current grade after external review: `CONSTRUCTIVE_NONUNIQUENESS_ONLY`.

The external reviewer accepted every load-bearing calculation. The scope is constructive: the two
explicit surviving families prove nonuniqueness, but this package does not claim an exhaustive
classification of every finite-jet natural one-form.

## 1. Result first

The complete regular stationary R17 metric naturally constructs several local one-forms beyond
`dphi`. It does **not** select one of them as an additional physical reciprocal transgression.

The sharp distinction is:

```text
geometric ownership of a form != selection of that form as the observer-pair law.
```

At order zero, after the metric-owned clock/ruler/screen split is retained, the residual screen
`SO(2)` leaves a two-dimensional covector space:

```text
span{tau,nu},
```

where `tau` is the time-oriented unit clock coform and `nu` is the unit twist-ruler coform, with
the sign of `nu` carried by the orientation local system. Both are nonclosed on the regular twisted
R17 family.

At a generic first jet where the screen projection of `dphi` is nonzero, the four forms

```text
tau, nu, s=H*dphi, J_H s
```

span the full cotangent space. Here `H` is the metric-owned screen projector and `J_H` is its
orientation-dependent quarter-turn. Higher jets generate further tensorial modules and exact
endpoint-potential families.

Most decisively, for every real dimensionless `c`,

```text
alpha_c=dphi+c H*dphi                                      (1)
```

agrees with `dphi` on every intrinsic reciprocal pair leaf, composes exactly when integrated over
concatenated paths, and is generically nonclosed. Therefore the founded pair-leaf reduction and
path composition do not select `c=0`.

Even adding endpoint/path-independence does not produce local uniqueness. On the nonzero-twist
family define

```text
I_H=|H*dphi|^2,
W=|omega_K|^2,
J=I_H/(I_H+W).
```

`J` is dimensionless and metric-natural. The exact family

```text
beta_c=dphi+c dJ=d(phi+cJ)                                 (2)
```

reduces to `dphi` on the pair-pure locus `H*dphi=0` but differs on complete mixed configurations.
No supplied R17 equation fixes `c`.

Thus local metric algebra owns a vocabulary, not a distinguished new sentence. The smallest
possible further owner is an explicit physical query/measurement premise. An on-shell equation or
a global-completion/period rule could also select a member. This audit does not decide which kind
of owner UDT ultimately supplies.

## 2. Supplied stationary geometry

Use the complete coframe

```text
theta0=u^-1(dt+a sigma3), theta1=u sigma3,
theta2=v sigma1,          theta3=v sigma2,
u=exp(phi), v=exp(lambda phi), T(phi)=0,
```

with `a>0`, `u,v>0`, and Maurer--Cartan sign `epsilon=+1` or `-1`:

```text
[X,Y]=2 epsilon Z, [Y,Z]=2 epsilon X, [Z,X]=2 epsilon Y.
```

The exact dual frame is

```text
e0=u T,
e1=u^-1(Z-aT),
e2=v^-1 X,
e3=v^-1 Y.
```

The complete metric owns the regular projector split

```text
E=span(e0,e1), H=span(e2,e3).
```

The time orientation fixes `e0`. The nonzero Killing twist fixes the ruler line `span(e1)`; a
spacetime/screen orientation fixes its sign. The previous audits derive

```text
delta_K(p,q)=phi(q)-phi(p),
```

so `dphi` is already selected as the infinitesimal generator of this existing endpoint depth. The
question here is whether the same local algebra selects another one-form for the complete
cross-leaf relation.

## 3. Order-zero invariant covectors

The full projector triple has residual connected isotropy `SO(2)` rotating `(e2,e3)` and fixing
`e0,e1`. Let a local covector be

```text
z=z0 theta0+z1 theta1+z2 theta2+z3 theta3.
```

Invariance under the screen quarter-turn forces

```text
z2=z3=0.
```

Therefore the complete order-zero invariant covector space is exactly

```text
span{theta0,theta1}.                                       (3)
```

With the owned time and orientation typing, set

```text
tau=theta0,
nu=theta1.
```

This is already enough to refute uniqueness of a bare order-zero geometric one-form. It does not
yet make either form a physical depth law.

## 4. Exact closedness and twist algebra

Write

```text
dphi=(p1/u)theta1+(p2/v)theta2+(p3/v)theta3,
p1=Z(phi), p2=X(phi), p3=Y(phi).
```

Direct exterior differentiation gives

```text
d tau=-dphi wedge tau
      -2 epsilon a/(u v^2) theta2 wedge theta3,              (4)

d nu= dphi wedge nu
      -2 epsilon u/v^2 theta2 wedge theta3.                  (5)
```

Because `a,u,v` are positive, both forms are nonclosed throughout the regular twisted family. A
line integral of either is additive under concatenation but is path-dependent.

Let `K=T` and `kappa=K^flat=-u^-1 theta0`. With orientation
`theta0 wedge theta1 wedge theta2 wedge theta3`, the Killing twist is

```text
omega_K=star(kappa wedge d kappa)
       =2 epsilon a/(u^3 v^2) theta1.                         (6)
```

Thus the raw twist one-form is not a third order-zero direction. It is an orientation-odd scalar
multiple of the ruler form. The normalized Killing coform likewise reproduces the clock form.

Reconstructing the two distribution mean-curvature vectors from the full brackets and the Koszul
formula gives

```text
Mean(E)=0,
Mean(H)=-2 lambda p1/u e1.                                  (7)
```

So these familiar first-jet candidates add no new direction on this family: the pair leaves are
minimal and the screen mean curvature is ruler-directed.

## 5. Generic first-jet completion of the cotangent space

Define the orientation-even screen one-form

```text
s=H*dphi=(p2/v)theta2+(p3/v)theta3.
```

If an orientation is supplied, the screen metric defines its quarter-turn

```text
J_H s=-(p3/v)theta2+(p2/v)theta3.
```

In the coframe `(theta0,theta1,theta2,theta3)`, the determinant of the four covectors

```text
tau,nu,s,J_H s
```

is

```text
(p2^2+p3^2)/v^2.                                            (8)
```

Hence they span all of `T*M` whenever the screen gradient is nonzero. At `H*dphi=0`, the screen
axis is not selected and the order-zero rank-two space remains. This is a stratum change, not a
branch selection.

The consequence is structural: after first jets are admitted, local naturality cannot pick one
direction merely by asking for a metric-owned covector. The metric generally owns enough data to
construct every covector direction.

## 6. Exact nonuniqueness while preserving the pair-leaf law

Since `H` annihilates `E`,

```text
s(V)=0 for every V in E.
```

Therefore every member of (1) restricts to `dphi` on every intrinsic `R x S1` pair leaf. For any
supplied path `gamma`,

```text
Delta_c(gamma)=integral_gamma alpha_c
```

obeys identity, reversal, and concatenation exactly. Those facts hold for every `c`; composition
cannot choose a member.

This is not merely a formal local rectangle. Take the actual smooth global unit-quaternion model

```text
S3={w^2+x^2+y^2+z^2=1}
```

with the MC-minus left-invariant frame

```text
X=(-x,w,-z,y),
Y=(-y,z,w,-x),
Z=(-z,-y,x,w),
```

and choose

```text
phi=w, lambda=0, a=1/64.
```

This is a smooth stationary R17 configuration. It is globally regular because
`exp(2w)>=exp(-2)>1/64`. Here

```text
s(X)=-x, s(Y)=-y, s(Z)=0,
[Z,Y]=2X.
```

At

```text
(w,x,y,z)=(1/2,1/2,1/2,1/2)
```

one obtains

```text
d s(Z,Y)=Z[s(Y)]-Y[s(Z)]-s([Z,Y])=1/2.                       (9)
```

Thus `alpha_c` is genuinely nonclosed for `c!=0` on a complete smooth stationary R17 geometry.
This closes G51's earlier caveat that only a general differential-form control—not an R17
witness—had been shown.

## 7. Path independence still does not select a unique endpoint potential

On the same family let

```text
I_H=|s|^2.
```

For the global witness above,

```text
I_H=x^2+y^2.
```

At the same point,

```text
(Z I_H,X I_H,Y I_H)=(0,0,1),
(Z phi,X phi,Y phi)=(-1/2,-1/2,-1/2),
```

so

```text
dI_H wedge dphi(Z,Y)=1/2.                                  (10)
```

The scalar `I_H` is not merely a reparameterization of `phi`.

To keep all coefficients dimensionless, use the nonzero twist norm

```text
W=|omega_K|^2
```

and define

```text
J=I_H/(I_H+W).                                               (11)
```

On regular twisted R17, `J` is a dimensionless scalar differential invariant. On the pair-pure
locus `H*dphi=0` identically, both `J` and `dJ` vanish. Equation (2) is therefore an infinite exact
family that preserves the pure reciprocal reduction. On the global witness, `W` is a function of
`phi`, so (10) implies

```text
dJ wedge dphi !=0.                                           (12)
```

The members are genuinely inequivalent endpoint potentials. Requiring closedness or endpoint-only
composition therefore still does not select `c=0`; it only changes which nonunique family remains.

## 8. Curvature, Hodge, and connection families

Arbitrary finite metric jets supply scalar differential invariants, curvature tensors, the
projectors, `dphi`, and their covariant derivatives. Contracting these with `g` generates
orientation-even tensorial one-forms. Including the volume form/Hodge star generates separately
typed orientation-odd forms. Multiplication by arbitrary smooth dimensionless scalar invariants
closes these into modules. Examples include

```text
dI,
I dphi,
i_e1 F,
F_mu_nu F^nu_rho (dphi)^rho,
star(dphi wedge F),
f(I_1,...,I_k) alpha.
```

For `I=I_H`, (10) also proves that

```text
d(I dphi)=dI wedge dphi
```

is nonzero on the actual global R17 witness.

These are structural construction classes, not a claim that every formal expression is physically
independent. Finding further generators could only enlarge the nonunique family; it could not by
itself select one.

The projected screen connection is different in type. In an oriented local screen frame its
representative is

```text
A=A0 theta0+A1 theta1+A2 theta2+A3 theta3,
```

but under a local screen rotation

```text
A -> A+dchi.
```

Only the connection and `F=dA` are globally owned. One chosen `A` is not an endpoint-frame-
invariant scalar one-form. Connection transgressions therefore require a reference connection,
trivialization, loop, or other global data.

## 9. Existing equation and completion ownership

The exact 18-source manifest contains the controlling G51 status and the complete R17
clock/ruler/screen, connection, holonomy, grading, and scalar-descent records. They own:

- `dphi` for the already-derived endpoint depth;
- the canonical geometric forms and projectors above;
- the normal connection after a path is supplied; and
- branch-conditional representation weights for each supplied `lambda`.

They explicitly do not own:

- an on-shell R17 profile or branch equation;
- one `lambda`;
- a physical path or observer query;
- a complete non-isometric observer arrow;
- a global period/boundary rule selecting a transgression; or
- a physical mixed-geometry scalar law.

Constant-`phi`, flat, and descended loci have already been classified and none is selected.
Moreover `dphi=0` on a constant-depth locus while `tau` and `nu` remain nonclosed, so the special
loci do not secretly produce a unique replacement.

## 10. Bounded landing

```text
CANONICAL_STATIONARY_R17_GEOMETRIC_ONE_FORMS_BEYOND_dphi_DERIVED__
ORDER_ZERO_INVARIANT_COVECTOR_SPACE_IS_span_tau_nu__
GENERIC_FIRST_JET_SPANS_FULL_COTANGENT__
ACTUAL_SMOOTH_GLOBAL_R17_NONEXACT_TRANSGRESSION_WITNESS_DERIVED__
PAIR_LEAF_REDUCTION_AND_PATH_COMPOSITION_DO_NOT_SELECT_THE_COEFFICIENT__
EXACT_DIMENSIONLESS_PAIR_PURE_PRESERVING_ENDPOINT_FAMILY_SURVIVES__
NO_DISTINGUISHED_RECIPROCAL_TRANSGRESSION_SELECTED_BY_LOCAL_METRIC_ALGEBRA__
ADDITIONAL_QUERY_ON_SHELL_OR_GLOBAL_OWNER_REQUIRED.
```

This is a stationary local-finite-jet classification plus one complete smooth R17 witness. It does
not select the missing owner or derive a path, arrow, branch, action, source, matter, bootstrap
law, `X_max`, universal `c_eff`, CMB observable, signalling law, or dynamics.
