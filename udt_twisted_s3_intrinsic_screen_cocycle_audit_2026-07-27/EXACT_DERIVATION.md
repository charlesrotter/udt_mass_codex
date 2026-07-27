# Exact derivation — intrinsic screen, endpoint clock, and forced transport mixing

## 1. Scope and inherited metric certificate

For C01–C06 use the already certified complete coframe

```text
theta0 = exp(-phi)(dt+a sigma3),
theta1 = exp(+phi) sigma3,
theta2 = exp(lambda phi) sigma1,
theta3 = exp(lambda phi) sigma2,
g      = -theta0^2+theta1^2+theta2^2+theta3^2.
```

The parent invariant proof identifies the unique timelike Killing line `span(K)`, where
`K=partial_t`.  Its nonzero twist identifies the unoriented line dual to `theta1`.  No coordinate
line is declared physical by hand in this audit.

Choose a time orientation and representatives

```text
u=K/sqrt[-g(K,K)],
n=unit(clock twist).
```

Changing either sign leaves every unoriented projector below unchanged.

## 2. The transverse screen is metric intrinsic

With signature `(-,+,+,+)`, define

```text
H^a_b = delta^a_b + u^a u_b - n^a n_b,
q_ab  = g_ab + u_a u_b - n_a n_b.
```

In the parent orthonormal coframe both are represented by

```text
diag(0,0,1,1).
```

Exact multiplication gives `H^2=H`, `rank(H)=2`, and `H(u)=H(n)=0`; `q` is positive definite on
the image.  Therefore the same metric that identifies the clock and ruler lines also identifies
their unique orthogonal rank-two screen.  It does not choose a screen orientation or an ordered
basis in that plane.

Given a spacetime orientation, one representative area form is

```text
epsilon_perp = i_n i_u epsilon_g
             = plus_or_minus theta2 wedge theta3.
```

Without orientation, its positive area density remains well defined.

## 3. Exact local screen-area response

Using

```text
d sigma1 = kappa sigma2 wedge sigma3,
d sigma2 = kappa sigma3 wedge sigma1,
d sigma3 = kappa sigma1 wedge sigma2,
kappa=-2,
```

the Maurer–Cartan terms cancel in the exterior derivative of the screen area:

```text
d(theta2 wedge theta3)
  = 2 lambda dphi wedge theta2 wedge theta3.
```

Since `phi` is stationary,

```text
L_u epsilon_perp = 0,
L_n epsilon_perp = 2 lambda n(phi) epsilon_perp.
```

This is a complete-metric local coframe identity.  It is not an optical angular-distance equation:
an optical area is the determinant of a vertex Jacobi map with path and initial data.

## 4. The branch-specific founded clock join closes

The intrinsic Killing norm is

```text
N=sqrt[-g(K,K)]=exp(-phi)
```

in the frozen units.  For an affinely parametrized geodesic tangent `k`, Killing antisymmetry gives

```text
d[-g(K,k)]/ds=0.
```

Call the conserved value `E`.  The intrinsic stationary observers measure

```text
omega=-g(u,k)=E/N=E exp(phi).
```

For the frozen direction convention `Q_pq=omega_q/omega_p`, every supplied geodesic segment between
stationary endpoint observers therefore obeys

```text
Q_pq=exp[phi(q)-phi(p)],
log Q_pq=phi(q)-phi(p).
```

It composes through a matched stationary endpoint and reverses exactly.  Because this is the same
founded `phi` that weights the reciprocal clock/ruler coframe, the old conditional clock-depth join
is closed **inside C01–C06**.  It is not a universal law for arbitrary moving observers, paths, or
future nonstationary UDT solutions.

## 5. Same-metric longitudinal/transverse path cocycle

Along the same supplied geodesic, the transverse deviation state

```text
Y=(xi,Dxi/ds)
```

obeys

```text
dY/ds = [[0,I],[-T,0]]Y,
```

where the screen tidal matrix `T` is symmetric.  The generator is Hamiltonian with respect to

```text
Omega=[[0,I],[-I,0]],
```

so its fundamental matrix `M_gamma` is symplectic, composable, invertible, screen-frame covariant,
and remains invertible when its projected vertex block passes through a caustic.

Consequently

```text
C_gamma=S(log Q_gamma) direct_sum M_gamma
```

is now a same-metric reducible cocycle on every supplied regular geodesic segment in C01–C06.  Its
clock block is nontrivial whenever the stationary endpoint depths differ.  The earlier need to take
the nontrivial clock from WR-L and the complete transverse
geometry from another branch is gone at the level of complete configuration existence.

This does not make the direct sum irreducible.  It also does not yet say that the path's optical
screen remains equal to the local twist-selected screen.

## 6. The newly exposed connection obstruction

Let `E0,E1,E2,E3` be dual to `theta0,...,theta3` and write

```text
dphi=p1 theta1+p2 theta2+p3 theta3.
```

The two null fields naturally associated with the intrinsic pair are

```text
l_plus =E0+E1,
l_minus=E0-E1.
```

An independent Cartan/Koszul calculation gives

```text
nabla_lplus lplus  = -p1 lplus  -2p2 E2-2p3 E3,
nabla_lminus lminus= +p1 lminus -2p2 E2-2p3 E3.
```

All explicit twist and `lambda` coefficients cancel from the transverse acceleration.  Either null
line is pregeodesic exactly where

```text
E2(phi)=E3(phi)=0.
```

At such a point the screen is preserved along the ray up to an internal `SO(2)` rotation.  For the
frozen generic profile, the north-event derivatives are

```text
(E1 phi,E2 phi,E3 phi)=(3/50,1/50,2/50),
```

so every C01–C06 witness fails global aligned-ray propagation already at the certificate event.

There is also an exact global obstruction, not merely a bad profile sample.  If a stationary smooth
`phi` obeyed `E2(phi)=E3(phi)=0` everywhere, then

```text
0=commutator(E2,E3)_on_phi=C^1_23 E1(phi),
C^1_23=-kappa exp[(1-2lambda)phi] != 0.
```

Hence `E1(phi)=0`; stationarity also gives `E0(phi)=0`, so `dphi=0`.  The horizontal screen on the
twisted `S3` is bracket generating.  A nontrivial depth profile therefore cannot support a globally
geodesic null congruence that remains everywhere aligned with the twist-selected ruler.

This is the central new metric-led finding:

> nontrivial reciprocal depth and twisted finite-cell geometry force the intrinsic pair and the
> pathwise optical screen to mix somewhere through the Levi-Civita connection.

It is a kinematic connection statement, not an action, force, matter source, or operational
signalling theorem.  Individual aligned segments or other topologies may still exist.

## 7. WR-L/SNe comparison

The preserved conditional WR-L readout is

```text
1+z=exp(phi),
D_A/X=1-exp(-2phi),
d_L=(1+z)^2 D_A.
```

The raw local screen length in the frozen twisted family is proportional to `exp(lambda phi)`.
There is no constant pair `(A,lambda)` for which

```text
A exp(lambda phi)=1-exp(-2phi)
```

on an open interval containing `phi=0`: evaluation at zero forces `A=0`, while the right derivative
at zero is `2`.

This does **not** damage the SNe result.  It proves that local coframe area and vertex optical area
cannot be conflated.  The conspicuous algebraic complement

```text
1-exp(-2phi)
```

also means the `lambda=-2` local screen weight is compatible with the exponential appearing inside
the WR-L areal law, but only after a vertex/baseline operation.  That is a lead for a prospectively
registered Jacobi calculation, not a `lambda` selection and not a fit.

## 8. Exact boundary

Derived in the bounded complete family:

- intrinsic clock/ruler/screen splitting for C01–C06;
- branch-specific founded depth equal to the stationary endpoint log-frequency ratio;
- a nontrivial same-metric reducible clock-plus-Jacobi path cocycle;
- exact local screen-area response; and
- unavoidable intrinsic/optical mixing somewhere for every nonconstant stationary depth on this
  twisted contact `S3` branch.

Still open:

- a selected path/event rule and endpoint-versus-path ontology;
- the exact Jacobi propagator for every nonhomogeneous geodesic;
- any irreducible connection/response law beyond metric parallel transport and pair reset;
- on-shell selection, physical `lambda`, a complete action, source, carrier, boundary, bootstrap,
  density, mass, `X_max`, dynamics, and operational access.
