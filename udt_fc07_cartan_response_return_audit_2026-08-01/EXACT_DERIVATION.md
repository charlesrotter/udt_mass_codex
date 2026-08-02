# Exact derivation — FC07 Cartan response and global-to-local channel

Date: 2026-08-01  
Preregistration: `45ebc7e`  
Source freeze: `f9fb990`

## 1. Bounded complete metric

Use proper base distance `r=L exp(phi0) s` and write

```text
g = -tau^2 dt^2 + dr^2 + dy^T h(r)dy,
tau = c_E exp(-phi0),
h(r) = h0 + chi(r) Delta,
Delta = M^T h0 M-h0.
```

The eight frozen `M` controls, every positive-definite `h0`, both orientation strata, and general
local `h,h_dot,h_ddot` are retained. Constant `phi0`, zero shift, zero reciprocal-screen mixing,
and this interpolation remain bounded construction choices.

## 2. Full connection and curvature

Define the screen shape operator

```text
K = (1/2) h^-1 h_dot,
K_dot = (1/2)h^-1 h_ddot-(1/2)(h^-1 h_dot)^2,
T = K_dot+K^2.
```

The only nonzero coordinate Christoffel blocks are

```text
Gamma^r_ab = -(1/2) h_dot_ab,
Gamma^a_rb = Gamma^a_br = K^a_b.
```

The complete spatial curvature is

```text
R_rarb = -(h T)_ab
        = -(1/2)h_ddot_ab+(1/4)(h_dot h^-1 h_dot)_ab,
R_1212 = -(1/4)det(h_dot),
R_rabc = 0,
Ric_rr = -tr(T),
Ric_screen^# = -(K_dot+tr(K)K),
R_scalar = -2tr(K_dot)-tr(K^2)-tr(K)^2.
```

These identities were derived as full tensors and checked by an independent coordinate
Christoffel/Riemann construction.

For an orthonormal screen coframe `Pdy`, set

```text
Q = P_dot P^-1 = S+W,
S^T=S,  W^T=-W.
```

The Cartan connection contains

```text
omega^A_1 = S^A_B theta^B,
omega^A_B = -W^A_B theta^1.
```

Thus both screen shear modes are present; the skew `W` is coframe gauge. No diagonal-screen
shortcut was used.

## 3. Exact unimodular endpoint theorem

Let `h1=M^T h0 M` and `B=h0^-1 h1`. Since `M` is unimodular,

```text
det(B)=1,
det(Delta)=det(h0) det(B-I)=det(h0)[2-tr(B)].
```

`B` is similar to a positive-definite matrix with determinant one, so `tr(B)>=2`. Equality occurs
exactly when `B=I`, equivalently `h1=h0`. Therefore

```text
det(Delta)=0  iff the screen is constant,
det(Delta)<0  for every nonconstant registered interpolation.
```

Inside the cell `chi_dot>0`, and

```text
det(K) = chi_dot^2 det(Delta)/(4 det(h)) < 0
```

for every nonconstant member. This statement covers the full SPD `h0` domain, not only the generic
rational control. Parabolic and hyperbolic monodromy admit no positive fixed screen, so their
variation is forced. Order-four, order-six, exchange, and reversing-glide have both constant and
varying strata. Identity and minus-identity are constant in this registered interpolation.

## 4. Rank-one relative projector response

For the bundle base line `n` in the positive three-space, let

```text
P_n=n tensor n_flat,  Q_screen=I-P_n.
```

The complete parent response is

```text
Omega_rel(X,Y)=Q_screen[(D_X P_n),(D_Y P_n)]Q_screen.
```

In an orthonormal screen frame the only potentially nonzero block is

```text
Omega_rel(e2,e3)|screen = det(S) [[0,1],[-1,0]],
det(S)=det(K)=det(h_dot)/(4det(h)).
```

A screen reflection conjugates the skew matrix and preserves `det(S)` and its norm. The response
therefore descends through both orientation strata. It vanishes smoothly at the seam because every
positive endpoint jet of `chi` vanishes.

Consequently every nonconstant registered interpolation has nonzero **bundle-relative** response
at every interior point. This is metric-intrinsic only where the base/ruler line passes the
independent selection gate below.

## 5. Symmetric midpoint control

At the flat-step midpoint,

```text
chi=1/2,  chi_dot=2/ell,  chi_ddot=0,
ell=L exp(phi0).
```

Equal endpoint determinants imply `tr(K)=0`. In two dimensions,

```text
K^2=-det(K) I,
-(K_dot+K^2)=K^2=-det(K)I,
R_2323=-det(K).
```

All three spatial sectional curvatures are therefore equal and positive for a varying member.
The spatial curvature operator is invertible, so the four-dimensional curvature nullity is exactly
the parallel timelike line. This supplies a sufficient metric-intrinsic clock certificate for all
six generic varying controls.

Because the spatial curvature is isotropic at that point, it does **not** select one spatial ruler
axis. The separate global harmonic/cohomology gate below is load-bearing for the ruler selection.

The isotropic midpoint depends on the registered symmetric interpolation and must not be promoted
to a general UDT law or dynamics.

## 6. Completion cohomology and the harmonic return channel

For a torus mapping torus,

```text
b1(Sigma_M)=1+dim ker(M^T-I).
```

The eight frozen controls give

```text
b1=1: minus-identity, order-four, order-six, hyperbolic;
b1=2: parabolic, exchange, reversing-glide;
b1=3: identity.
```

On the registered spatial product, the base class has harmonic representative

```text
alpha(r) = dr/[I_h sqrt(det h(r))],
I_h = integral_cell dr/sqrt(det h(r)),
```

after unit-period normalization. It is closed, and co-closure is exactly

```text
d/dr[sqrt(det h) alpha_r]=0.
```

When `b1=1`, the complete metric has only one harmonic one-form line, so no cohomology-class choice
remains. Its local amplitude depends on the integral over the entire completed cell. This is a
genuine nonidentity global-to-local geometric map when `h` varies.

Combining the intrinsic clock certificate with `b1=1` yields three varying metric-intrinsic global
ruler channels in the frozen set:

```text
order-four, order-six, hyperbolic.
```

Hyperbolic is the only frozen control for which both variation and the unique harmonic line are
forced for every SPD `h0`. Parabolic also forces variation and response, but `b1=2`; its displayed
base line remains bundle-relative unless another metric-native discriminator is found.

The minus-identity row has `b1=1` but is flat and has zero response. It remains an important
degeneracy/control case.

The specific harmonic realization emerged while evaluating the preregistered C06 global-return
candidate class; it was not named as a preferred answer. It is independently reconstructed and is
retained with this disclosure rather than retroactively presented as a narrower preregistration.

## 7. Constant-screen holonomy and observer reciprocity

On a constant-screen subfamily the local curvature and projector response vanish. Global discrete
holonomy still acts as `M` on the screen and fixes the `(time,base)` directions. Its full fixed-space
dimension is

```text
2+dim ker(M-I).
```

For minus-identity, order-four, and order-six this dimension is exactly two. The metric therefore
recovers a global Lorentzian reciprocal two-plane but does not choose one clock/ruler axis inside
it. The remaining boost freedom is the appropriate observer-frame family, not a defect to be
removed.

Identity has trivial holonomy and no proper plane selection. Exchange and reversing-glide have a
three-dimensional fixed space and likewise no unique reciprocal plane.

## 8. Bootstrap and `X_max` type gates

The harmonic construction is stronger than a pointwise forward curvature readout: global
completion determines a normalized local field. It is therefore a concrete geometric
global-to-local channel and a candidate component of a future return architecture.

It is not bootstrap closure. No native equation requires the harmonic projector, no local
admissibility family is changed by it here, and no same-solution feedback relation to total
mass-energy was supplied.

This bounded family also does not derive `X_max`:

- `c_E` supplies the inherited observational calibration;
- `ell=L exp(phi0)` remains a free witness circumference;
- constant `phi0` supplies no position-dependent observer-pair dilation; and
- `I_h` is a completion-dependent Hodge modulus, not an observer-pair asymptote.

## Maximum conclusion

```text
FC07_FULL_SCREEN_CARTAN_AND_CURVATURE_DERIVED;
ALL_NONCONSTANT_REGISTERED_INTERPOLATIONS_HAVE_NONZERO_BUNDLE_RELATIVE_PROJECTOR_RESPONSE;
THREE_VARYING_UNIQUE_H1_CLASSES_HAVE_A_METRIC_INTRINSIC_GLOBAL_HARMONIC_RULER_CHANNEL;
ONE_OF_THEM_HYPERBOLIC_IS_FORCED_IN_THE_FROZEN_SET;
THREE_CONSTANT_SUBFAMILIES_HAVE_A_HOLONOMY_FIXED_RECIPROCAL_PLANE_WITHOUT_SELECTED_AXES;
NO_UNIVERSAL_PROJECTOR_BOOTSTRAP_CLOSURE_XMAX_SELECTION_DYNAMICS_OR_MATTER.
```
