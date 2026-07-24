# Exact center-free observer optical correspondence

## 1. What the metric supplies

Given a complete Lorentzian metric `g`, an ordered observer event `o`, an
observer tangent `u_o`, and a null geodesic `gamma` joining `o` to an event
`s` on another observer history, the metric supplies:

```text
- the Levi-Civita connection;
- the null tangent k along gamma;
- the endpoint clock ratio from -g(u,k);
- the two-dimensional null screen k-perp / span(k);
- geodesic-deviation transport on that screen.
```

In parallel orthonormal screen bases, the transverse Jacobi matrix obeys a
second-order equation determined by the screen projection of the Riemann
tensor. With vertex normalization

```text
J(0)=0,    J'(0)=I,
```

the pathwise transverse area radius is

```text
D_A(gamma)=sqrt(abs(det J)).
```

Independent orthogonal changes of source and observer screen bases act as

```text
J -> R_s J R_o^T.
```

The absolute determinant is unchanged. Therefore `D_A` is a
chart/coframe-independent scalar attached to the supplied path and
normalization.

The metric does not guarantee a unique path. A source history can intersect
one null cone zero, one, or several times, and several null geodesics can
join the same events. The natural metric object is therefore a set:

```text
O_null(o,Gamma_s)
 = {(s,gamma,clock_ratio,J_gamma,D_A_gamma)}.
```

This is geometric null correspondence. Calling it physical light or
information propagation requires an additional field/readout premise.

## 2. The observer-rest alternative

Given a positive observer-rest geometry `h` and a supplied event pairing,
each spatial geodesic from `p` to `q` has a transverse Jacobi map. For a
unit-speed geodesic, its screen is the two-plane perpendicular to the
geodesic tangent. The corresponding object is

```text
O_rest(p,q)
 = {(gamma,d_h(p,q),J^h_gamma,sqrt(abs(det J^h_gamma)))}.
```

At a cut locus, the scalar intrinsic distance can remain unique while the
minimizing geodesics and screen transports form a family.

The null and rest-space constructions use the same metric machinery but
different event and path types. They are not universally identical. In the
time-dependent conformal control

```text
g=a(eta)^2[-deta^2+dchi^2+chi^2 dOmega^2],
```

a radial null interval `chi` has

```text
D_A(null)=a_source chi,
```

while the simultaneous rest distance on the observation slice is

```text
D_rest(observer slice)=a_observer chi.
```

They differ whenever `a_source != a_observer`.

Likewise, for two static worldlines separated by `L` in flat spacetime, an
observer event at `t=0` pairs with the other history at:

```text
t=0       under equal-time pairing,
t=-L/c_E  under past-null pairing.
```

The metric permits both constructions after their inputs are stated; it does
not choose which represents co-presence.

## 3. Round center-free witness

For round spatial `S3_b`, geodesic polar form about any observer is

```text
h=dD^2+b^2 sin(D/b)^2 dOmega^2.
```

The transverse Jacobi radius is

```text
j(D)=b sin(D/b).
```

It satisfies

```text
j''+j/b^2=0,
j(0)=0,
j'(0)=1.
```

Consequently:

```text
D_A(D)=b sin(D/b),
D_A(pi b/2)=b,
D_A(pi b)=0.
```

The antipode is both the spatial cut locus and a transverse caustic. Its
scalar distance is `pi b`, while its minimizing paths and frame transports
form a family.

For the ultrastatic product

```text
g=-c_E^2 dt^2+h_round,
```

the time direction has zero product curvature and the null screen tidal
matrix equals the spatial radial sectional curvature `1/b^2`. With matched
vertex normalization, null-screen and rest-screen Jacobi laws coincide:

```text
D_A_null=D_A_rest=b sin(D/b).
```

The static clock ratio is one. Thus the conditional B19 branch supplies a
complete, center-free optical geometry but no reciprocal clock dilation.

## 4. General centered warped geometry

For

```text
g=-N(D)^2 c_E^2 dt^2+dD^2+R(D)^2 dOmega^2,
```

the spatial radial and tangential sectional curvatures are

```text
K_rad=-R''/R,
K_tan=(1-R'^2)/R^2.
```

The central radial Jacobi equation is solved identically by `j=R`:

```text
j''+K_rad j=0.
```

With a regular central vertex, `R(0)=0` and `R'(0)=1`, so both rest-space
solid-angle transport and the centered null solid-angle construction give

```text
D_A=R(D).
```

The proper radial distance is `D`, not `R(D)`. For static observer tangents,
the conserved metric time symmetry gives

```text
1+z=N_observer/N_source.
```

These are distinct outputs of the same metric.

## 5. Exact WR-L substitution

On the conditional WR-L branch,

```text
A=1-r/X=exp(-2phi),
dD=dr/sqrt(A).
```

The proper-coordinate form is

```text
N(D)=1-D/(2X),
R(D)=D-D^2/(4X),
0<D<2X.
```

Exactly:

```text
R/X=1-N^2=1-exp(-2phi),
D=2X[1-exp(-phi)],
1+z=1/N=exp(phi).
```

For the centered radial construction,

```text
D_A=R(D),
```

which is the areal factor used in the registered SNe readout. It is not the
proper pair distance `D`.

The spatial curvatures are

```text
K_rad=1/[2X R(D)],
K_tan=1/[X R(D)].
```

They differ by a factor of two and vary with `D`. Moreover,

```text
R''(0)=-1/(2X) != 0,
```

whereas a smooth regular three-dimensional polar center requires
`R(D)=D+O(D^3)`. This reproduces the registered center obstruction directly
in transverse geometry.

Thus the WR-L clock/area assembly is exact in its centered residual domain,
but that domain has not supplied one smooth global geometry in which every
observer can be recentered.

## 6. All-observer isotropic recenterability

Suppose a connected smooth three-dimensional observer-rest geometry has the
same direction-independent polar law about every observer. At each point
all sectional curvatures then equal some `kappa(p)`, so

```text
Ric=2 kappa h,
scalar curvature=6 kappa.
```

The metric's contracted Bianchi identity gives

```text
div Ric = (1/2)d(scalar curvature),
2 d(kappa)=3 d(kappa).
```

Therefore `d(kappa)=0`: the sectional curvature is constant.

This theorem is scoped to all-observer directional isotropy. Homogeneous
anisotropic spaces, such as the squashed-`S3` control, can remain centerless
while having direction-dependent Jacobi and cut data.

WR-L fails the stronger isotropic-recenterability test because
`K_rad != K_tan`; its scalar curvature also varies with the centered
coordinate. This agrees with the prior invariant atlas proof that WR-L
residual recentering is not an ordinary coordinate transformation on one
global manifold.

## 7. A static-endpoint countercontrol

The positive constant-spatial-curvature reciprocal static control has

```text
A(r)=1-r^2/b^2,
r=b sin(D/b),
N=cos(D/b).
```

Its radial and tangential spatial curvatures both equal `1/b^2`. The static
lapse vanishes at

```text
D=pi b/2,
```

while the completed round spatial diameter is

```text
pi b.
```

Therefore an infinite-dilation static endpoint can be half the complete
pair diameter. A lapse horizon, optical caustic, areal maximum, proper radial
endpoint, and global observer diameter are not interchangeable.

This is a mathematical comparison control, not a selected UDT branch.

## 8. Fixed branch census

All twelve finite-cell completion rows still lack a complete `g,phi`
witness. Of the twenty-eight equation/evidence families:

- B19 supplies the conditional round center-free optical geometry but has
  constant lapse;
- B21 supplies the local centered WR-L clock/area readout but no complete
  global pair geometry;
- no other family supplies a complete metric optical witness.

The homogeneous squashed control defines pathwise null/rest Jacobi
correspondences but remains off shell, direction dependent, and without a
closed cut/area atlas. The conditional temporal-`phi` family defines a
positive rest geometry only if its branch, representative, ranges, and
global completion are supplied.

## 9. Exact ruling

The complete metric contains a native geometric core:

```text
observer events + path
  -> endpoint clock comparison
  -> transverse screen transport
  -> pathwise area radius.
```

Because event pairing and paths can be nonunique, the honest object is a
set-valued bilocal correspondence.

Current registered branches split the desired physical structure:

```text
round B19:
  global center-free transverse geometry
  + no reciprocal clock dilation;

WR-L:
  reciprocal clock dilation + centered transverse area
  + no smooth global center-free recentering.
```

No cross-branch splice is allowed. A single complete branch containing both
halves has not been derived.
