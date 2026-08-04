# Factorized whole-spacetime skeleton

## Result first

The current post-July UDT geometry fits into one coherent factorized configuration skeleton without
choosing an action, carrier, boundary, preferred frame or desired physical branch.

The important correction is structural:

> The seven angular/mixing extension directions need not be eliminated by a separate pointwise
> kinematic selector before a spacetime theory can exist. They can be coordinates on the allowed
> configuration bundle. A native law, together with global and boundary data, may select whole
> solution sections rather than one algebraic member at every point.

This does not derive that law. It removes an unnecessarily strong intermediate demand and shows the
domain on which a future law would have to act.

## 1. Abstract founded layer

Let `M` denote the four-dimensional configuration manifold and let `B` denote the abstract rank-two
reciprocal clock/ruler representation over it. The founding audits supply

```text
H = diag(-1,+1),
D(phi) = exp(phi H) = diag(exp(-phi),exp(+phi)),
D(phi2) D(phi1) = D(phi1+phi2).
```

Here `phi` is the founded additive logarithmic reciprocal-depth parameter. It is not an extra
independent scalar placed beside the metric. The founding result does not by itself assign one
global scalar field to spacetime. In a supplied local physical realization we write its potential as
`phi_i(x)`; the observer/path assignment and overlap law for those local potentials remain open.
The abstract pair representation is derived; its unique physical embedding into a complete coframe
is not.

Full observer covariance means that `H` and its reciprocal plane transform equivariantly with the
frame. It does not mean that one fixed two-plane is invariant in every frame.

## 2. Local complete-coframe chart

On a chart `U_i`, choose a reference coframe only as a presentation,

```text
bar_theta_i = (beta_i, sigma_i),
```

where `beta_i` is a two-slot clock/ruler reference pair and `sigma_i` is a two-slot screen reference.
In the registered positive-triangular section the complete extension is

```text
E_i(phi_i,D_i,S_i) = [[D(phi_i),     0],
                    [D_i S_i,    D_i]],

theta_i = E_i bar_theta_i.
```

`D_i` is an invertible positive-triangular `2 x 2` angular-screen block and `S_i` is a general
`2 x 2` base-angular mixing block. Their generator form is

```text
X_i = [[H, 0],
       [C, K]],

K = [[a,b],[0,d]],       C in Mat(2,R).
```

After the founded base generator `H` is fixed, `K` contributes three chart directions and `C`
contributes four. These seven directions are an exact pointwise extension-chart count and have
rank-seven metric response at the chart identity. They are **not** seven propagating fields or seven
physical modes.

The factorization preserves the useful exact identities

```text
det(E_i) = det(D(phi_i)) det(D_i) = det(D_i),

E_i^-1 = [[D(phi_i)^-1,               0],
          [-S_i D(phi_i)^-1,    D_i^-1]].
```

In the registered Lorentzian coframe reading,

```text
g = eta_ab theta_i^a tensor theta_i^b,
eta = diag(-1,+1,+1,+1).
```

This defines the local metric configuration. It does not impose an Einstein, Bach or other field
equation.

## 3. Gauge and physical variation are different questions

The complete local presentation carries:

- coordinate changes on `M`;
- local Lorentz changes of coframe that leave `g` unchanged; and
- a local `O(2)` screen rotation that changes the screen coframe but not its metric.

The general-screen result makes the last distinction explicit. A screen coframe has area, two shear
responses and one rotation response; its metric has area and two shears, while the displayed
rotation is coframe gauge. At isotropy the two shears remain present even though polar coordinates
hide one direction.

The generic metric count `F4[6]` is a configuration-arena count modulo coordinate presentation. It
is not the selected native UDT field rank and not a propagating-mode count. The parent skeleton does
not assign a physical mode count before the law, its gauge constraints and its initial-value problem
exist.

## 4. Metric identities and derived configuration data

Once a complete local metric is supplied, its Levi-Civita connection and Cartan curvature are
defined by

```text
d theta^a + omega^a_b wedge theta^b = 0,
omega_ab + omega_ba = 0,
Omega = d omega + omega wedge omega.
```

These are geometric definitions and identities, not UDT equations of motion.

On a supplied local depth realization, its first jet supplies the scalar

```text
s_phi = g_inverse(dphi_i,dphi_i).
```

Where `s_phi < 0`, `dphi` gives the audited local timelike-depth projector and spatial leaves. Where
`s_phi > 0`, it gives spatial-depth leaves with an unresolved timelike direction inside them. The
null and zero-gradient strata remain part of the configuration space. Geometry does not select one
causal branch merely by classifying them.

Regular metric-derived projectors, their Cartan data and their compatible transport also belong to
the configuration geometry. They add useful structure without becoming new independent fields or
physical evolution.

## 5. Observer comparison layer

The observer/event layer is a typed query layer over the metric, not an additional dynamical field.
Given a physical pair, signed additive depth and typed path, the repository supports the conditional
comparison data

```text
C_gamma = (D(rho_gamma), U_gamma),
```

where `U_gamma` is Levi-Civita coframe transport. The depth may be endpoint-only while the complete
coframe comparison remains path-labelled.

On a complete stationary branch with an intrinsic timelike Killing line, the bounded metric-native
depth is

```text
delta_K(p,q) = log(
  sqrt(-g(K,K)) at p / sqrt(-g(K,K)) at q
).
```

That is an exact reduction witness. Arbitrary observers, nonstationary realization, cut-locus path
semantics and the global separation functional remain open.

## 6. Globalization layer

Local objects become a complete spacetime configuration only when overlap data `T_ij` satisfy their
cocycle and equivariance conditions. The skeleton therefore retains, without selecting:

- chart and coframe transitions;
- extension-bundle transitions;
- topology, quotient, cap, seam and finite-cell sector;
- boundary/seal/corner data and orientation; and
- observer/path behavior across overlaps and cut loci.

The existing completion atlases provide bounded constructive families. They do not yet supply an
arbitrary global classification or a native selection law.

The local factorization should therefore be read as charts on a proposed complete extension bundle.
Its global existence and precise associated-bundle transition law remain open. Crucially, a native
law could be posed on sections of this full bundle; kinematics need not first collapse every fiber to
one point.

## 7. Identities are not the missing law

The skeleton separates five classes:

```text
FOUNDING IDENTITIES
  reciprocal depth, character, reversal and frame equivariance

GEOMETRIC DEFINITIONS/IDENTITIES
  coframe factorization, metric, connection, curvature and transition cocycles

CONDITIONAL EQUATIONS
  stationary comparison, stationary S3 Cartan control, EH, Bach, Hopfion

OBSERVATIONAL ANCHORS
  c_E and G_obs

OPEN LAW SLOTS
  global extension glue, physical variation domain, native law,
  boundary/completion law, bootstrap return, Xmax operator and matter source
```

No number of additional Cartan identities automatically fills an open law slot. Conversely, the
existence of open law slots does not invalidate the mapped configuration geometry.

## 8. Dependency structure

```text
founded reciprocal pair
          |
          v
pointwise complete extension charts ----> observer comparison queries
          |
          v
global transition/completion bundle
          |
          v
physical configuration + variation domain
          |
          v
native covariant law + boundary law
          |
          +----------> time-live initial-value system
          |
          +----------> global-local bootstrap test
          |
          +----------> observer-pair separation / Xmax
          |
          +----------> native matter/source/persistence
```

The diagram is a dependency order, not a claim that every downstream object must be a separate
mechanism. One future law might jointly determine several slots.

## 9. Exact reductions retained

The parent skeleton reproduces, as premise-stamped reductions:

- the founded reciprocal pair;
- the direct-sum spectator witness;
- determinant-one, angular and shift counterfamilies;
- the complete stationary general-screen `R x S3` control;
- timelike- and spacelike-`dphi` local branches;
- stationary Killing-depth comparison;
- path-labelled complete-coframe comparison; and
- smooth global stationary `S3` existence witnesses.

None of these reductions selects the parent law or the realized universe.

## 10. What Phase A accomplishes

The existing pieces do form a coherent whole configuration arena. The arena is richer than the
original reciprocal pair but remains sparse and factorizable. The principal missing object is now
well typed: a covariant law on global sections of this arena, together with its admissible variation
and boundary/completion data.

This phase does not establish that the metric already contains a unique hidden action or response.
It supplies the correct domain for testing that question without using computation time as a
scientific criterion and without assuming that local kinematics must select one algebraic branch.
