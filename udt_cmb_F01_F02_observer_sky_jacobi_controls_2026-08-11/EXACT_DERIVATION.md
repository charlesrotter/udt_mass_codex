# Exact derivation — F01/F02 observer-sky Jacobi controls

Date: 2026-08-11  
Primary landing: `LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER`

## 1. Scope and object type

The calculation evaluates one declared observer-sky query on two `CHOSE` controls. It does not ask
which control is physical. In units `c_E=1`, the metrics are

```text
F01: ds^2=-A dt^2+dr^2/A+r^2(dtheta^2+sin^2(theta)dpsi^2),

F02: ds^2=ds_F01^2+2h sin^2(theta)dt dpsi.
```

At `p=(t0,r0,pi/2,psi0)`, define

```text
u       = A^(-1/2) partial_t,
n       = A^(+1/2) partial_r,
E_theta = r^(-1) partial_theta,
D       = A r^2+h^2,
E_psi   = h/[sqrt(A)sqrt(D)] partial_t+sqrt(A)/sqrt(D) partial_psi,
k       = u+n.
```

Direct contraction gives

```text
g(u,u)=-1,  g(n,n)=g(E_theta,E_theta)=g(E_psi,E_psi)=1,
all cross products=0,  g(k,k)=0.
```

The null geodesic with initial tangent `k` is a geometric comparison generator. In the co-present
interpretation it is not being promoted to a local material signal trajectory.

For the two initial screen directions, let

```text
J_B(0)=0,
nabla_k J_B(0)=E_B,
nabla_k nabla_k J_B+R(J_B,k)k=0.
```

With a parallel screen, `mathcal_D_AB=g(E_A,J_B)` obeys

```text
mathcal_D''+mathcal_T mathcal_D=0,
mathcal_D(0)=0,
mathcal_D'(0)=I,
mathcal_T_AB=g(E_A,R(E_B,k)k),
mathcal_D(s)=s I-(s^3/6)mathcal_T(0)+O(s^4).             (1)
```

## 2. Exact F02 local tidal matrix

Write the local jets as

```text
A0=A(r0), A1=A'(r0), A2=A''(r0),
h0=h(r0), h1=h'(r0), h2=h''(r0).
```

The complete coordinate curvature calculation gives

```text
mathcal_T_F02 = [[0,0],[0,tau]],                         (2)

tau = h0 N/[4 A0 (A0 r0^2+h0^2)^2],                    (3)
```

where

```text
N = -4 A0^3 h0+8 A0^3 h1 r0-4 A0^3 h2 r0^2
    -4 A0^2 A1 h0 r0+2 A0^2 A2 h0 r0^2
    -4 A0^2 h0^2 h2+4 A0^2 h0 h1^2
    -4 A0 A1 h0^2 h1+2 A0 A2 h0^3+A1^2 h0^3.           (4)
```

Thus

```text
D_theta_theta = s+O(s^4),
D_psi_psi      = s-tau s^3/6+O(s^4),
D_theta_psi    = D_psi_theta=O(s^4).                    (5)
```

The trace is `tau`; the trace-free plus component under the registered orientation is `-tau/2`;
the cross component and antisymmetric rotation vanish. F02 therefore supplies a local principal
screen axis and a metric-derived area/shear correction on this query. It does not supply a local
rotation at this order.

The sign is not fixed by the admitted local metric stratum. Positive and negative exact rational
controls both occur. Geometry owns the formula; a selected profile would be needed to own its
value along a complete branch.

## 3. Weak-mixing and cancellation structure

Scale the complete mixing jet by one bookkeeping amplitude,
`(h0,h1,h2)->epsilon(h0,h1,h2)`. Odd orders vanish and

```text
tau=epsilon^2 tau_2+epsilon^4 tau_4+...,

tau_2 = h0[-2 A0 h0+4 A0 h1 r0-2 A0 h2 r0^2
            -2 A1 h0 r0+A2 h0 r0^2]/[2 A0 r0^4].       (6)
```

The local screen distortion is therefore quadratic, not linear, in a weak axis-regular mixing
amplitude. This agrees with the earlier angular operator's natural mixing variable
`B=h^2/(A r^2)` without importing that scalar operator as dynamics.

There are two exact zero subloci at cubic Jacobi order:

1. `h0=0`, even when `h1` or `h2` is nonzero;
2. `h0!=0` with the codimension-one local-jet cancellation `N=0`.

These are retained. On either sublocus, higher Jacobi order or a finite path may still distinguish
F02; the present result is not a proof of complete equivalence.

## 4. Independent F01 result and round limit

F01 was rebuilt independently rather than obtained only by deleting terms from F02. Its exact
radial screen tidal matrix is

```text
mathcal_T_F01=0                                             (7)
```

for arbitrary regular `A,A',A''`. The production F02 expression reduces identically to (7) when
`h=h'=h''=0`.

There is a useful exact conditional extension. Along a regular radial F01 null branch, the energy
`E=A dt/ds` is conserved and nullity gives `dr/ds=+E`. Hence `r` is affine and (7) holds along the
whole regular radial segment. With the registered initial data,

```text
mathcal_D_F01(s)=s I                                       (8)
```

until a caustic, chart failure, or query endpoint intervenes. Equation (8) does not select the
remote comparison surface or its affine location.

## 5. What happens to the old affine projection freedoms

The historical F00 comparison fitted a multipole scale and an offset. This control calculation
separates their ownership:

- **scale:** the Jacobi map is the correct geometric home for converting a remote transverse scale
  into an observed angular scale. F01 fixes its radial form conditionally; F02 supplies a
  profile-dependent anisotropic correction. But no physical remote surface, complete F02 profile,
  or source scale is owned, so no numerical CMB angular scale is yet derived;
- **offset:** a mode-ladder offset is boundary/operator phase data, not a screen-Jacobi coefficient.
  This calculation does not derive it and must not hide it inside the angular map.

The complete geometry has therefore replaced the *place where a projection-scale calculation
belongs*, and it has exposed a non-affine directional correction that the old scalar affine map
could not represent. It has not yet removed either historical fitted number from a physical CMB
comparison.

## 6. Evidence

Production constructs `g`, `g^-1`, every Christoffel symbol, and
`R^rho_(sigma mu nu)` before imposing the equatorial query. The independent implementation instead
uses the fully lowered Riemann formula built from second metric derivatives and quadratic
connection terms, and rebuilds F01 as a separate metric. It reproduces the full symbolic F02
formula, the standalone F01 zero, the round limit, screen symmetry, and three exact rational
controls: `6/6` checks.

## 7. Landing and open scope

`LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER`.

The two controls are locally distinguishable on the identical query whenever `h0 N != 0`. F01 is
isotropic and linear on its regular radial branch; generic F02 produces a one-axis cubic
area/shear correction whose value is controlled by the admitted local `A,h` jets.

Still open: the physical CMB observer query; the complete global F02 profile and endpoint;
finite-distance integration and cut/focal branches; the physical angular screen; source/state
covariance and nonzero TT power; boundary/operator phase; polarization source; action, source,
bootstrap, `X_max` value, and dynamics. No control has been selected and no local signalling claim
has been made.

