# Global two-shear descent witness

The local equivariance solution

```text
h(s)=exp(kappa s R) H0 exp(-kappa s R)
```

is not by itself a global patching proof because a fiber coordinate `s` is local. The global object
is constructed without choosing such a coordinate.

Let `pi:S3->S2` be the supplied Hopf principal bundle and let `q_B` be any smooth positive metric on
`S2`. Then `pi^*q_B` is a smooth, global, positive horizontal tensor on `S3` invariant under the
Hopf circle. The global Maurer–Cartan forms `sigma1,sigma2` span the horizontal cotangent plane, so
there is a unique smooth positive matrix field `h:S3->SPD(2)` satisfying

```text
pi^*q_B=(sigma1,sigma2) h (sigma1,sigma2)^T.
```

Invariance of the tensor and `L_V sigma_screen=kappa R sigma_screen` give

```text
V(h)+kappa(hR-Rh)=0.
```

The matrix positive square-root map is smooth on `SPD(2)`. Hence

```text
P=h^(1/2)
```

is a global smooth `GL(2,R)` screen realizing the metric.

For explicit configuration-space breadth, choose

```text
q_B=q_round+epsilon T,
```

where `T` is a generic smooth trace-free symmetric tensor on `S2`. Because `S2` is compact, small
enough `|epsilon|` preserves positivity. A generic `T` excites both local shear polarizations,
although topology may force zeros of a polarization field. Thus the descended global family is not
restricted to an isotropic or one-shear screen.

In any local fiber trivialization this global pullback reduces to the rotating-matrix formula above;
for `kappa=-2` it is `2 pi` periodic. The local formula verifies the equivariance ODE, while the
pullback construction supplies the actual global compatibility across charts.
