# Exact derivation — complete two-screen response on registered branches

## Scope

This is a kinematic map of the fixed registered branch universe.  It does not select a branch,
path, screen orientation, action, source, carrier, boundary, density, scale, particle, or force.
The twelve `FC` rows are completion taxonomies; they are not silently treated as metric solutions.

## 1. The complete local screen vocabulary

On an oriented positive two-screen, use

```text
I  = [[1, 0], [ 0, 1]]
R  = [[0,-1], [ 1, 0]]
S1 = [[1, 0], [ 0,-1]]
S2 = [[0, 1], [ 1, 0]].
```

Every real screen endomorphism has the unique decomposition

```text
K = a I + w R + s1 S1 + s2 S2,
a  = (K11+K22)/2,
w  = (K21-K12)/2,
s1 = (K11-K22)/2,
s2 = (K12+K21)/2.
```

Thus

```text
End(S) = R I + so(2) + Sym0(2),       dimensions 4 = 1+1+2.
```

The exact brackets are

```text
[R,S1]=2 S2,   [R,S2]=-2 S1,   [S1,S2]=-2 R,   [I,*]=0.
```

The traceless algebra is therefore `sl(2,R)` and the complete algebra is `gl(2,R)`.  These are
generic matrix identities, not a UDT gauge group, interaction, or particle classification.

## 2. What is invariant and what is not

For a supplied screen and direction,

```text
tr K       = 2a,
det K      = a^2+w^2-s1^2-s2^2,
shear norm = s1^2+s2^2.
```

The trace and shear norm are screen-basis invariant.  The shear pair rotates by twice the screen
angle.  The displayed sign of `w` needs an orientation, and a connection coefficient also changes
under a path-dependent screen-frame gauge.  Congruence vorticity
`<nabla_(screen) k,screen>` and rotation of a screen frame *along* `k` are distinct objects; the
atlas records them separately in `ROTATION_OWNERSHIP_ATLAS.tsv`.

## 3. Complete homogeneous controls Q01/Q02

For

```text
de1=p e2^e3,  de2=p e3^e1,  de3=q e1^e2,
u=ultrastatic clock, n=dual(e3), S=span(e1,e2),
```

the exact conditional-pair response is

```text
congruence vorticity of n on S = (q/2) R,
screen-frame connection along n = (p-q/2) R,
area response = shear response = 0.
```

Q01 is conditionally complete/on shell only in its registered `C^2` scope and its round metric does
not select a Hopf line.  Q02 is a complete off-shell control whose nonround metric selects only an
unoriented Ricci line.  Neither is promoted.

## 4. Complete twisted reciprocal S3 configuration W01

The inherited complete coframe is

```text
theta0 = exp(-phi)(dt+alpha sigma3),
theta1 = exp(+phi) sigma3,
theta2 = exp(lambda phi) sigma1,
theta3 = exp(lambda phi) sigma2.
```

Write

```text
dphi=p1 theta1+p2 theta2+p3 theta3,
l_plus=E0+E1,  l_minus=E0-E1.
```

### Screen metric response

Both angular legs carry the same weight, so direct differentiation gives

```text
K_phi = lambda I.
```

Along the two intrinsic null directions, the symmetric screen response is

```text
K_sym(l_plus)  = +lambda p1 I,
K_sym(l_minus) = -lambda p1 I,
s1=s2=0.
```

This exact zero is scoped to this equal-weight response.  It does not set generic optical/Jacobi
shear to zero.

### Screen-frame connection

With the frozen Maurer–Cartan coefficient `kappa`, exact Cartan reduction gives

```text
w_plus  = kappa[-alpha+exp(2phi)-2exp(2lambda phi)]
          exp[-(2lambda+1)phi]/2,
w_minus = kappa[-alpha-exp(2phi)+2exp(2lambda phi)]
          exp[-(2lambda+1)phi]/2.
```

Equivalently,

```text
w_u = -alpha kappa exp[-(2lambda+1)phi]/2,
w_n = kappa[exp(2phi)-2exp(2lambda phi)]exp[-(2lambda+1)phi]/2.
```

These are displayed-basis connection coefficients.  They are not frame-independent scalars.

### Pair-screen mixing

The exact accelerations are

```text
nabla_lplus  lplus  = -p1 lplus  -2p2 E2-2p3 E3,
nabla_lminus lminus = +p1 lminus -2p2 E2-2p3 E3.
```

The mixing vector is therefore `(-2p2,-2p3)`, with invariant squared norm
`4(p2^2+p3^2)`.  At the registered C01–C06 north event it is `(-1/25,-2/25)` and its squared norm is
`1/125`.  The contact identity already established in the source package implies that global
alignment (`p2=p3=0` everywhere) forces `dphi=0`.  Nonconstant depth in this complete twisted
family consequently forces pair-screen mixing somewhere.

## 5. The shear gap is an ansatz diagnosis, not a negative theorem

If the two screen weights were only algebraically distinguished,

```text
theta2 ~ exp(lambda2 phi),  theta3 ~ exp(lambda3 phi),
```

then

```text
a  = (lambda2+lambda3)/2,
s1 = (lambda2-lambda3)/2.
```

This counterfactual calculation proves only that the registered equal-weight choice removes one
shear axis from the `phi`-parameter response.  It does not construct a new complete branch.  A fully
general screen matrix would be needed even to expose the second shear component.  Separately, an
arbitrary geodesic's Jacobi tidal matrix can contain both shears; its path, profile, and initial data
are not supplied in the current registry, so those coefficients remain `OPEN`, not zero.

## 6. Global result and boundary

- The exact intersection over all 52 rows is undefined because many rows are taxonomy-only or
  blocked.  Over all evaluated pointwise responses the intersection is the zero algebra because
  explicit zero-response rows occur.
- The union of explicitly evaluated nonzero screen components contains trace and rotation.
- Generic nonconstant twisted depth additionally realizes pair-screen mixing outside `End(S)`.
- No explicitly evaluated registered response realizes either shear component, but current data do
  not establish their absence from the complete metric solution space.
- Q01/Q02 retain full spatial `so(3)` holonomy in their registered controls; a pathwise `SO(2)`
  display is not a globally parallel screen reduction.
- W01 has a global intrinsic screen projector on its regular complete configuration, but its full
  path holonomy and nonhomogeneous Jacobi atlas remain uncomputed.

Maximum conclusion:

```text
MIXED_MULTIPLE_OUTCOMES;
BOUNDED_REGISTERED_BRANCH_ATLAS;
NO_PHYSICAL_SELECTION.
```
