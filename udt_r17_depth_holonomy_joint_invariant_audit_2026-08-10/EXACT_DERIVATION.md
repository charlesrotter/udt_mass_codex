# Exact derivation — stationary R17 endpoint depth and normal holonomy

Date: 2026-08-10

Current grade: `VERIFIED_WITH_CORRECTIONS` by fresh external review; corrections incorporated.

## 1. Declared objects

On the supplied smooth regular stationary R17/W01 family, the metric owns two different objects:

```text
delta_K(gamma)=phi(q)-phi(p),
U_gamma:H_p -> H_q.
```

Here `gamma:p->q` is a supplied piecewise-smooth path, `delta_K` is the already-derived endpoint
reciprocal depth, `H` is the metric-owned rank-two angular normal bundle, and `U_gamma` is parallel
transport for the projected metric connection `D`. The metric supplies the transport after the
path is supplied; it does not select the path.

The endpoint depth obeys

```text
delta_K(gamma_2 o gamma_1)=delta_K(gamma_2)+delta_K(gamma_1),
delta_K(gamma^-1)=-delta_K(gamma).
```

The normal transport obeys

```text
U_(gamma_2 o gamma_1)=U_gamma2 U_gamma1,
U_(gamma^-1)=U_gamma^-1.
```

Thus the first object is endpoint-exact and the second is path-labelled. Globally, `U_gamma` is
an isometry between two generally different fibers. It becomes a matrix in one fixed copy of
`SO(2)` only after oriented frames are chosen at both endpoints.

## 2. The metric-owned joint functor

The pair

```text
J_gamma=(delta_K(gamma),U_gamma)
```

is an exact path-groupoid functor into the product of the additive reciprocal-line groupoid and
the oriented normal-isometry **groupoid**. In local oriented screen frames, this product is
represented by `R x SO(2)` and one may write

```text
U_gamma=R(theta_gamma) in SO(2).
```

Then composition is simply

```text
(delta_2,R_2)(delta_1,R_1)
  =(delta_1+delta_2,R_2 R_1).                  (1)
```

For every real weight `w`, this has a conformal screen representation

```text
C_w(gamma)=exp(w delta_K(gamma)) U_gamma in CO^+(2),              (2)
```

and the scalar dilation commutes with the rotation, so

```text
C_w(gamma_2 o gamma_1)=C_w(gamma_2)C_w(gamma_1),
C_w(gamma^-1)=C_w(gamma)^-1.                                    (3)
```

Equation (2) is globally a conformal isomorphism `H_p -> H_q`; it is a matrix in `CO^+(2)` only
after endpoint frames are chosen. It is a one-parameter representation family if only the abstract
pair `(delta,U)` is given. It is not yet weight selection.

## 3. What the complete R17 coframe fixes

The supplied complete coframe has

```text
q_H=v^2(sigma1^2+sigma2^2),
v=exp(lambda phi),
(e2,e3)=v^-1(X,Y).
```

Let `B=(X,Y)` be the inherited global Hopf reference vector frame. If normal parallel transport
has matrix `U_gamma` in the physical orthonormal frames, its matrix on reference-vector
coefficients is

```text
v(p)/v(q) U_gamma
 =exp[-lambda delta_K(p,q)]U_gamma.                              (4)
```

On the dual reference coframe the factor is instead

```text
v(q)/v(p) U_gamma
 =exp[+lambda delta_K(p,q)]U_gamma.                              (5)
```

Therefore the complete coframe fixes the weight inside these two declared rank-two
representations:

```text
screen vectors:   w=-lambda;
screen covectors: w=+lambda.                                    (6)
```

There is no sign conflict with the finite metric lift `exp(delta X_lambda)`, whose screen
eigenvalue is `+lambda` on the abstract graded tangent slots. Equation (4) instead describes
coefficients in the inherited global reference-vector frame `(X,Y)`: because the physical
orthonormal vectors are `v^-1(X,Y)`, their reference coefficients carry the inverse factor and
therefore weight `-lambda`. Equation (5) is the variance-dual reference-coframe statement; its
rotation may be written with inverse transpose according to arrow direction, which equals the
same oriented rotation under the stated `SO(2)` convention.

This is conditional on each supplied complete R17 coframe. It does not select one `lambda` across
the branch family, and tensor powers or other associated bundles have their own representation
weights. Equations (4)--(6) are not the missing four-dimensional physical observer arrow; they are
the exact conformal screen-component lifts of the already-supplied endpoint depth and isometric
normal carry.

The corresponding joint connection has a rotational `SO(2)` part and an exact scalar part
proportional to `dphi`. Since `d(dphi)=0` and the scalar generator commutes with screen rotation,
its curvature is just the already-derived rotational curvature `F`. The reciprocal factor changes
open-path scale but does not alter loop holonomy.

## 4. Endpoint gauge covariance

Under independent oriented endpoint frame rotations by `alpha_p,alpha_q`,

```text
U_gamma -> R(-alpha_q) U_gamma R(alpha_p),
theta_gamma -> theta_gamma+alpha_p-alpha_q.                       (7)
```

The depth is unchanged and every `C_w` obeys the same endpoint covariance. This is the correct
global type: an open-path arrow is covariant at both endpoints, not a scalar invariant.

The independent left/right action in (7) is transitive on `SO(2)`. Given any two open-path
rotation matrices `U,V`, endpoint gauges can map `U` to `V`. Consequently any real order-zero
function

```text
f(delta_K,U_gamma)
```

that is invariant under independent endpoint screen gauges must be independent of `U_gamma`.
The determinant and singular values of (2) likewise return only `exp(2w delta_K)` and
`exp(w delta_K)`. No representative-free angular scalar survives for one unframed open path.

## 5. Complete continuous real-character theorem

After choosing a model oriented screen fiber, consider every continuous group character in the
declared order-zero local joint group,

```text
chi:R x SO(2) -> (R,+).
```

The restriction of `chi` to compact `SO(2)` has compact image. The additive real line has no
nontrivial compact subgroup, so that restriction is zero. The restriction to the additive real
factor is `a delta`. Therefore

```text
chi(delta,U)=a delta.                                             (8)
```

Pure reciprocal normalization `chi(delta,I)=delta` fixes `a=1`. Thus, without assuming linearity
in an angle,

```text
THE UNIQUE NORMALIZED CONTINUOUS REAL CHARACTER FACTORING THROUGH THE LOCAL ORDER-ZERO
R x SO(2) REPRESENTATION IS delta_K.                              (9)
```

Angular transport has not disappeared. It simply cannot be compressed into a continuous real
additive character of `SO(2)`. This is not a classification of arbitrary cocycles on the full path
groupoid; endpoint coboundaries and derivative-dependent line integrals are treated separately.

Circle-valued characters do retain it:

```text
exp[i(k delta+n theta)],  k in R, n in Z.                         (10)
```

For an unframed open path, the angular factor in (10) is endpoint-gauge covariant rather than
invariant. A real unwrapped angle requires a lift to the universal cover plus a frame/trivialization
choice, and is not representative-free global data.

## 6. Loops and path pairs

For a closed loop, endpoint exactness gives

```text
delta_K(loop)=0.                                                  (11)
```

The normal holonomy remains. In an oriented screen it is an angle modulo `2 pi`; after allowing
screen reflection, its representative-free datum is its `O(2)` conjugacy class, equivalently
`2 cos(theta)`.

For two paths `gamma,eta:p->q`, the relative return

```text
H_(eta,gamma)=U_eta^-1 U_gamma                                  (12)
```

transforms by conjugation at the common source. It is invariant in oriented `SO(2)` and reduces to
an `O(2)` conjugacy class if reflections are allowed. Both paths have the same endpoint depth, so
the representative-free data are

```text
(delta_K(p,q), [H_(eta,gamma)]).                                 (13)
```

This is genuinely joint data, but it requires two paths and does not select either one.

Depth does not determine the angular return. The registered constant-depth C08 control has

```text
delta_K(loop)=0,
B_0(1)=4097/4096,
F23=-4097/2048 !=0.                                               (14)
```

Small contractible loops therefore carry nontrivial angular curvature despite zero reciprocal
endpoint depth. In the actual nonconstant C01--C06 witnesses, complete holonomy is full `SO(2)`.

## 7. No continuous depth-driven semidirect action

A nontrivial continuous semidirect product would require a continuous homomorphism

```text
R -> Aut(SO(2)).
```

Continuous automorphisms of the circle group are only `z->z` and `z->z^-1`, so
`Aut(SO(2))` is the discrete group `Z2`. A continuous map from connected `R` to that discrete group
is constant. Hence reciprocal depth cannot continuously act on screen rotation by a nontrivial
semidirect law inside this group class. Orientation reversal can invert holonomy, but it is a
separate discrete channel, not a depth-generated interaction.

The order-zero joint structure is therefore a commuting/direct-product structure, not a hidden
nonlinear coupling.

## 8. Higher-jet line integrals: composition is general; stationary non-exactness is open

The character theorem (9) is deliberately order-zero in the supplied joint arrow. Once local
metric derivatives are admitted, the complete metric supplies infinitely many candidate one-forms.
For example, with an `O(2)`-even curvature invariant `I(F,g,E,H)`,

```text
alpha=I dphi,
Delta_alpha(gamma)=integral_gamma alpha.                          (15)
```

Every line integral composes under concatenation and reverses under path reversal. It is generally
path-dependent because

```text
d alpha=dI wedge dphi
```

need not vanish. The exact local control `phi=y`, `I=x` gives `alpha=x dy`; its rectangle integral
is `(x1-x0)(y1-y0)`, which is nonzero. Exact one-forms `dH(phi,I,...)` give an infinite endpoint-
potential family. Orientation-odd examples such as contraction of `F` with `grad(phi)` require an
orientation local system.

Thus the preregistered claim that local depth-curvature constructions were only diagnostics is
**refuted at the level of composition**: a line integral of any supplied one-form is a genuine path
cocycle. But the rectangle is a differential-form control, not an R17 solution witness. It proves
that non-exact members exist in the general local construction class; it does not prove that the
stationary cohomogeneity-one R17 family realizes that two-coordinate control. Within stationary
R17, whether a metric-natural, endpoint-frame-invariant one-form independent of `dphi` is non-exact
is `OPEN`. Choosing `I`, a function of invariants, coefficients, derivative order, or a particular
one-form would in any case be a new premise unless an additional UDT rule owns it.

## 9. Flat control versus generic family

On a completely flat `D` connection over simply connected `R x S3`, normal transport is
path-independent and admits a global parallel frame. The joint map then reduces to an endpoint
conformal map in that frame. This is a valid special control, not a selected physical branch.

The actual C01--C06 witnesses instead have full `SO(2)` complete holonomy. Their generic metric-
owned object is the path-labelled normal-isometry groupoid functor and its local
direct-product/`CO^+(2)` representation, not an endpoint-only angular scalar.

## 10. Bounded landing

```text
CONDITIONAL_STATIONARY_R17_DEPTH_NORMAL_ISOMETRY_GROUPOID_FUNCTOR_DERIVED__
LOCALLY_DIRECT_PRODUCT__
COMPLETE_COFRAME_FIXES_SCREEN_CO2_WEIGHT_BY_VARIANCE__
UNIQUE_NORMALIZED_CONTINUOUS_REAL_ORDER_ZERO_CHARACTER_IS_ENDPOINT_DEPTH__
ANGULAR_DATA_REMAINS_PATH_OR_LOOP_VALUED__GENERAL_HIGHER_JET_LINE_INTEGRALS_COMPOSE_BUT__
STATIONARY_R17_NONEXACT_REALIZATION_OPEN__
PHYSICAL_PATH_AND_ARROW_OPEN
```

This result identifies a real geometric joint: reciprocal scale and angular transport assemble
exactly into conformal screen transport. It also proves why that joint does not automatically
become one new physical scalar. No path, branch, `lambda`, on-shell equation, action, source,
bootstrap return, universal `c_eff`, CMB observable, signalling law, or dynamics is selected.
