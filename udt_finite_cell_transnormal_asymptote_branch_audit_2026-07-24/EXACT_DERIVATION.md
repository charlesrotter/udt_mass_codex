# Exact branch derivation

## 1. Branch universe

The audit covers two fixed source universes:

- all 12 registered `FC01`--`FC12` completion rows; and
- all 28 registered `B01`--`B28` equation/evidence families.

The source records distinguish a completion type from a complete field
witness. Eleven FC rows contain no complete `(g,phi)` witness. `FC12` is a
conditional open-profile metric control, not a completed endpoint solution.

## 2. Conditional WR-L clock-depth control

The prior metric-native audit gave

```text
B_WRL=exp(2phi)/(4X^2),
D_WRL=2X[1-exp(-phi)],
D_WRL(infinity)=2X.
```

This branch supplies the founding clock relation

```text
T_clock=exp(phi).
```

It does not supply a complete global observer-pair geometry or prove that
its local `X` is the global diameter.

## 3. Conditional reciprocal-toric control

The exact metric is

```text
g=-dt^2+A(phi)^2 dphi^2
  +Omega(phi)^2[exp(-2phi)dxi1^2+exp(2phi)dxi2^2].
```

For the supplied static clock leg `dt`, the observer-rest inverse depth
coefficient is

```text
B_FC12=h^-1(dphi,dphi)=1/A(phi)^2.
```

It is automatically transnormal on the open profile:

```text
dD/dphi=A(phi),
D(phi)=integral A(phi)dphi.
```

The infinite-depth endpoint is finite exactly when `A` is integrable. The
common angular factor `Omega` does not enter this depth integral, although
it remains load-bearing for the global diameter, caps, and angular shape.

This `phi` is reciprocal angular depth. The displayed clock coefficient is
constant. Therefore the metric does not contain
`T_clock=exp(Delta phi)`.

## 4. Conditional round capped Bach control

The round capped solution inside the conditional stationary toric `C^2`
branch has spatial radius `b`. In Hopf coordinates,

```text
h=b^2[deta^2+cos(eta)^2 dxi1^2+sin(eta)^2 dxi2^2].
```

The conditional reciprocal/Hopf correspondence uses

```text
tan(eta)=exp(2phi).
```

Differentiation gives

```text
dphi/deta=1/sin(2eta)=cosh(2phi).
```

Hence

```text
B_B19=cosh(2phi)^2/b^2,
dD/dphi=b sech(2phi).
```

Measuring from the neutral Clifford torus `phi=0`, `eta=pi/4`,

```text
D(phi)=(b/2) atan[sinh(2phi)],
D(+infinity)=pi b/4.
```

The complete round three-sphere has spatial diameter

```text
diam(S3_b)=pi b.
```

Therefore

```text
diameter / one-sided reciprocal depth = 4.
```

This is an exact conditional geometric result. It is not a calculation of
`X_max`, because:

- the lapse is constant on the round branch;
- its `phi` is angular reciprocal depth rather than clock depth;
- `b` is an unselected common scale;
- the action is conditional `C^2`, not the complete native action; and
- the mathematical caps are not a selected physical finite-cell boundary.

The coordinate `phi` diverges at the smooth caps. It is therefore not a
single smooth real scalar on the completed `S3`; it is an open-chart depth.
That is how the control evades the compact critical-point theorem.

## 5. Stronger compact-rest-slice obstruction

Let an observer congruence have integrable compact boundaryless rest slices
with positive metric `h`. At every fixed observer time, a smooth real scalar
`phi` restricted to such a slice attains a maximum and minimum. At each
extremum,

```text
d_space phi=0,
B=h^-1(d_space phi,d_space phi)=0.
```

Therefore no smooth real `phi` can satisfy

```text
B(phi)>0
```

everywhere on a compact boundaryless rest slice.

This is stronger for the distance question than the earlier spacetime
`dphi` survival result. Adding time dependence can keep the full Lorentzian
gradient nonzero, but it cannot remove the spatial critical point of the
restriction on each compact slice.

The exact pure time-live control makes the distinction explicit:

```text
phi=t
```

has nonzero timelike spacetime gradient, while

```text
B=0
```

everywhere in the observer-rest geometry. It supplies no spatial
distance-versus-dilation law.

The obstruction does not reject compact geometry or global diameter. A
global distance function on a compact manifold is normally nonsmooth at a
cut locus. It says only that one smooth real clock-depth scalar cannot
globally coordinate the entire compact rest space with positive `B`.

## 6. Allowed ways around the obstruction

The current metric taxonomy retains, without selecting:

1. a retained/open asymptotic endpoint where `phi` is not required to be
   smooth or finite;
2. multiple depth charts with a cut locus;
3. a circle-valued or twisted depth object;
4. a nonintegrable observer-horizontal distribution and its horizontal
   distance;
5. a relational scalar on observer-pair/configuration space rather than one
   global spacetime scalar; or
6. a branch where the founding clock relation is carried by a different
   complete coframe object.

## 7. Exact missing join

The three strongest controls distribute the needed data:

| control | clock `phi` | angular/global metric | profile/endpoints | global diameter |
|---|---|---|---|---|
| WR-L | yes | incomplete globally | yes locally | open |
| reciprocal toric `FC12` | no; angular `phi` | conditional form | `A` arbitrary | open |
| round Bach `B19` | no; angular `phi` | capped round `S3` | yes conditionally | `pi b` |

No current witness co-locates all four columns.
