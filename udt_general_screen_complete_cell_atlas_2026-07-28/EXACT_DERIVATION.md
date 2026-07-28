# Exact derivation — general screen on the complete stationary S3 control

## Scope

This is exact geometry inside the preregistered stationary, off-shell, block-screen
`R x S3` control family. The `S3` completion and stationarity are
`CHOSE_EXISTENCE_CONTROL`; they are not selected UDT physics. “Complete cell” below means a smooth
global coframe on the compact spatial cell. It does **not** mean Lorentzian geodesic completeness.

No action, field equation, source, carrier, density, bootstrap value, boundary law, matter state,
or observational prediction is used or obtained.

## 1. Full screen matrix and its honest degrees of freedom

Use

```text
(theta2,theta3)^T = P(x) (sigma1,sigma2)^T,   P in GL(2,R).
```

On the orientation-preserving component, write

```text
P = R(chi+beta) diag(exp(u+v),exp(u-v)) R(-beta).
```

For any supplied direction, write the corresponding increments as
`du,dv,dbeta,dchi`. Direct differentiation gives

```text
(dP) P^-1 = a I + w R + s1 S1 + s2 S2,

a  = du,
w  = dchi + dbeta[1-cosh(2v)],
s1 = dv cos(2gamma) - dbeta sinh(2v) sin(2gamma),
s2 = dv sin(2gamma) + dbeta sinh(2v) cos(2gamma),
gamma = chi+beta.
```

The exact shear norm is

```text
s1^2+s2^2 = dv^2 + sinh(2v)^2 dbeta^2.
```

Thus the coframe response has four slots: area, two shears, and frame rotation. The metric

```text
h = P^T P
```

is independent of `chi`, so it has only three screen degrees of freedom. The fourth slot is local
`O(2)` coframe gauge, not an extra metric field.

The polar chart loses the axis angle at `v=0`. This is not a geometric singularity. In regular
logarithmic coordinates

```text
log H = u I + q1 S1 + q2 S2,
```

the isotropic tangent is

```text
du I + dq1 S1 + dq2 S2 + dchi R.
```

Both shear directions therefore remain present at isotropy. The rank loss in `(v,beta)` is solely a
polar-coordinate failure.

## 2. The angular structure seen by the deformed screen

Let `R` be the standard Maurer–Cartan rotation generator on `(sigma1,sigma2)`. In the physical
screen frame it becomes

```text
C = P R P^-1,
C^2=-I,  tr(C)=0,  det(C)=1.
```

Its exact screen decomposition is

```text
C = cosh(2v) R
    + sinh(2v) sin(2gamma) S1
    - sinh(2v) cos(2gamma) S2.
```

Consequently an anisotropic screen makes the inherited angular structure carry displayed shear
components with invariant squared norm `sinh(2v)^2`. This is a geometric interaction already in the
coframe. It is not a force, matter coupling, or action term.

## 3. Global existence on the registered S3 cell

The pair sector is

```text
theta0 = exp(-phi)(c_E dt + alpha sigma3),
theta1 = exp(+phi) sigma3.
```

Relative to `(c_E dt,sigma3,sigma1,sigma2)`, the coframe determinant is `det(P)` and the metric
determinant is `-det(P)^2`. Hence every smooth finite `phi` and smooth `P:S3->GL(2,R)` gives a global
nondegenerate Lorentzian configuration in this family.

For `det(P)>0`, polar decomposition gives `P=O H`, with `H` smooth positive definite. Because `S3`
is simply connected, `O:S3->SO(2)` has a global angle lift. `log H` supplies globally regular
`u,q1,q2` coordinates even where the polar shear axis fails. The negative-determinant component is
a fixed reflection times the positive component and spans the same screen metrics.

If the induced `t=constant` slice is positive definite, compactness of `S3` makes that Riemannian
slice geodesically complete. Zero and negative slice-sign strata are retained. They do not make the
four-metric degenerate. `det(P)=0`, by contrast, really degenerates the coframe and four-metric.

An explicit all-symmetric global witness is

```text
P(x)=exp[u(x) I + q1(x) S1 + q2(x) S2].
```

It is positive and invertible for all finite smooth functions. At an isotropic point its arbitrary
first jet spans `I,S1,S2`; adding `O(chi)` supplies the fourth coframe-gauge direction.

## 4. Full stationary first-jet Cartan system

Define

```text
dphi = p1 theta1+p2 theta2+p3 theta3,
L_A = (E_A P)P^-1,  A=1,2,3,
m  = kappa exp(-phi),
t0 = alpha kappa exp(-phi)/det(P),
t1 = kappa exp(+phi)/det(P).
```

Stationarity fixes `E0(P)=0`; it is not tested. The exact exterior system is

```text
dtheta0 = -dphi wedge theta0 + t0 theta2 wedge theta3,
dtheta1 = +dphi wedge theta1 + t1 theta2 wedge theta3,
d(theta_screen)
        = sum_A L_A thetaA wedge theta_screen
          + m theta1 wedge C theta_screen.
```

The production derivation reconstructs all four lowered `4 x 4` connection matrices. It checks
metric compatibility and zero torsion coefficient by coefficient. The independent implementation
rebuilds the same matrices from separately assembled exterior coefficients.

For `l_plus=E0+E1` and `l_minus=E0-E1`, the exact accelerations remain

```text
nabla_lplus lplus   = (-p1,-p1,-2p2,-2p3),
nabla_lminus lminus = (+p1,-p1,-2p2,-2p3).
```

Thus either aligned null direction is pregeodesic exactly when `p2=p3=0`. A general screen matrix
does not erase this contact obstruction.

The congruence area rates are `+tr(L1)/2` and `-tr(L1)/2`. The two shear components now contain the
symmetric trace-free parts of `L1+mC`. The screen-frame connection along either null direction is
pure skew, as metric compatibility requires, but its displayed rotation depends on the local
`O(2)` gauge. Exact matrices and all component formulas are in `GENERAL_CARTAN_RESULT.json` and
`CARTAN_RESPONSE_ATLAS.tsv`.

## 5. Bounded no-go: the pair/screen split cannot be parallel on this S3 family

Setting every pair-to-screen connection block to zero produces two off-diagonal equations

```text
S+t1=0,
S-t1=0.
```

Their difference requires `t1=0`. But on the registered twisted `S3` coframe,

```text
t1 = kappa exp(phi)/det(P),
```

which is nonzero for nonzero Maurer–Cartan coefficient `kappa`, finite `phi`, and invertible `P`.
Therefore no choice of the general screen matrix makes the pair and screen into an all-direction
parallel Levi-Civita splitting within this bounded family.

The independent proof does not use the connection-block algebra. Since
`dtheta1(E2,E3)=t1`, the angular screen distribution is nonintegrable. Any parallel distribution of
a torsion-free connection would be integrable. The same nonzero `t1` therefore gives the no-go by
Frobenius directly.

This does **not** forbid a screen projector, pathwise transport, an aligned ray at isolated regions,
or a different complete topology/coframe. It says only that the registered complete twisted `S3`
cell cannot be globally decomposed into two Levi-Civita-parallel two-planes by adjusting `P`.

## 6. Completion scope

`FC04_TWO_CAP_P1` has the actual global `S3` coframe and therefore receives the constructive
calculation above. Lens quotients and other transition completions remain conditional on explicit
deck/transition equivariance. Cap, seam, stratified, and other classes without supplied joined
metrics remain blocked. `FC11_NONINTEGRABLE_DISTRIBUTION` is a property realized inside the `S3`
witness, not a separate disjoint metric class.

## Maximum conclusion

The general screen closes the local and global **configuration-space vocabulary** of the angular
block on the stationary complete `S3` control: three metric modes, one coframe-gauge mode, both
shears at isotropy, exact first-jet interaction with the pair sector, and a bounded contact no-go for
an all-direction parallel split. It selects no physical branch or UDT dynamics.
