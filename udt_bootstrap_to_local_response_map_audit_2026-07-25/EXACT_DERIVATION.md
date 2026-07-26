# Exact bootstrap-to-local response derivation

## 1. The complete two-arrow multi-observable skeleton

Let the complete, still-unselected UDT configuration be `X`, including local
metric/coframe and matter variables, the finite-cell boundary and corners,
gluing/global moduli, and a topology sector. Let independent global variables
be `O`, and let the recomputed native observables be

```text
R^I[X] = (E_total, rho_total, curvature data, boundary/global data, ...).
```

The owner's broadened bootstrap hypothesis permits several such parameters but
does not supply their exact census. The later chicken-and-egg clarification
requires two arrows, not merely a function of recomputed observables:

```text
A^a(X,O)=0,
O^I-R^I[X]=0.
```

Here `A=0` says which local matter-and-geometry configurations are admissible
for given global data, while `O-R[X]=0` recomputes the global data from the
realized configuration. For dual covectors `lambda_a` and `mu_I`, the full
conormal response on the extended `(X,O)` space is

```text
alpha[delta X,delta O]
  = lambda_a (D_X A^a[delta X] + D_O A^a[delta O])
    + mu_I (delta O^I - D R^I_X[delta X]).
```

Along the recomputation constraint, `delta O=D R_X[delta X]`, and the branch
part reduces to

```text
lambda_a (D_X A^a + D_O A^a D R_X)[delta X].
```

This exposes the direct local branch term `D_X A` that the earlier
observable-only formula omitted. To calculate how a local branch moves when
global data change, `D_X A` must also be invertible modulo gauge and branch
degeneracies. A global functional can have a local functional derivative, so
it need not be inserted as a fitted local coupling. Cross-entries of this
complete Jacobian are the exact place where energy, density, curvature,
boundary, and other sectors can act together.

This architecture is `DERIVED_CONDITIONAL_RESPONSE_SKELETON`, not a derived
physical response. The present premises do not select `A`, `R`, their exact
observable census, target set, Jacobian, dual covectors, normalization,
branch-regularity conditions, complete domain, or boundary/corner extension.

The older form `B(O[X])=0` remains a valid special observable-only closure, but
it is not the complete architecture of the owner's two-way hypothesis.

An invertible remix of residual components has the same zero set but
changes a named dual response unless the dual covector transforms with it.
Thus the closure zero set alone supplies a conormal space, not one preferred
response one-form.

## 2. Density is one projection, not the whole bootstrap

For same-solution native total mass and proper volume,

```text
rho = M/V,
delta rho = (delta M-rho delta V)/V.
```

For a scalar density constraint with multiplier `eta`,

```text
alpha_rho[delta X]
  = eta F'(rho) (delta M-rho delta V)/V.
```

No density value substitutes for `delta M`. The center, width, equality, `F`,
and `eta` are all unsupplied.

The owner correction is load-bearing: this density formula does not exhaust a
multi-observable bootstrap. Native energy or curvature components could carry
local response independently or through cross-couplings.

There is a concrete curvature *candidate*: for
`I_R=integral sqrt(h) R`, a covariant metric variation `H_ij` has bulk
coefficient `(R h^ij/2-R^ij)H_ij` and boundary flux
`n^i(nabla^j H_ij-nabla_i tr H)`. In an orthonormal Ricci eigenframe,
`H=diag(1,-1,0)` gives `-r1+r2`, generically nonzero. This establishes only
mathematical availability of a trace-free curvature response. The foundation
does not select `I_R`, its target, derivative order, or boundary completion.
No parallel energy computation is available because native total energy is
not yet defined.

## 3. Exact angular result

For a spatial metric `h`, the bulk proper-volume response is

```text
delta V_bulk
  = 1/2 integral sqrt(h) h^ij delta h_ij.
```

The two independent angular trace-free directions—diagonal anisotropy and
off-diagonal shear—both obey

```text
h^ij delta h_ij = 0,
delta V_bulk = 0.
```

Therefore the density projection gives

```text
alpha_rho[delta h_TF]
  = eta F'(rho) delta M[delta h_TF]/V.
```

If the native mass variation is absent or trace-only, the density projection
cannot supply the angular response. This is scoped to the density channel. It
does not exclude an angular response from native energy, curvature, holonomy,
boundary, or another closure component. The executable three-observable
control gives

```text
alpha_angular
  = lambda_E D E_total|TF + lambda_K D K|TF
```

when the density-volume row is zero.

## 4. A window is not an equation

The owner principle requires matter-bearing complete solutions to occupy a
narrow density window. Every interior point of a nonempty inequality window
has an open neighborhood of admissible density values. The condition therefore
does not impose an Euler equation or a conormal response in its interior.

An exact equality `rho=rho_star` would be a stronger premise. It could define a
conormal line if `rho` were differentiable, but neither the equality nor
`rho_star` is supplied. Even then, multiplying a defining function by an
arbitrary positive function leaves the same level set and changes its conormal
normalization. Positive higher-order extensions also share the zero set but
differ away from it.

## 5. Realized roots do not recover the response

Two exact integrable response maps

```text
alpha_1=(q,s),
alpha_2=(q+s/2,s+q/2)
```

have the same unique root `(0,0)` and different off-shell responses. Their
Jacobians are symmetric and nonsingular, so even assuming local action
integrability would not make the realized root select the response.

Likewise the fixed-point maps `F_1(z)=0` and `F_2(z)=z/2` have the same unique
fixed point but residual derivatives `1` and `1/2`. The statement “the universe
is self-consistent” does not select a self-map or its linearization.

The owner chicken-and-egg hypothesis gives the stronger two-way type

```text
X in MatterGeometryBranches(O),
O = RecomputeGlobalObservables(X).
```

This usefully identifies the two arrows that must close: global matter,
energy, density, and curvature condition locally admissible matter/geometry,
while the realized configuration recomputes those global observables. Current
premises do not yet define either complete arrow. This agreement is
“optimization” in the owner's broad tuning sense. It must not be conflated
with scalar extremization, which would additionally require a native objective
or ordering.

## 6. Finite-cell response

Even volume has a moving-boundary channel. In the exact product-cell control
`V=A L`,

```text
delta V=A delta L+L delta A.
```

The first term is the normal-size/shape channel and disappears if the boundary
is silently fixed. A complete bootstrap response must likewise include the
moving-boundary, corner, gluing, and global-modulus variations of every energy,
mass, curvature, and other observable. Static `phi=0` seal parity and candidate
gluing data do not provide those functionals.

## 7. Metric-ontology fork

On the calibrated-metric branch, proper volume is defined once the physical
slice and boundary exist. Native mass and closure remain missing.

On the conformal-class branch,

```text
h -> Omega^2 h,
sqrt(h) -> Omega^3 sqrt(h)
```

in three spatial dimensions. Proper volume and density therefore do not descend
to the class unless native mass has a compensating transformation or a physical
representative is selected. Strong local CSN is challenged rather than
derived, so the audit cannot choose this branch or import a section.

Measured `c_E` and `G_obs` calibrate dimensions but do not select the response
functional. Exact dimensional rank confirms that those two constants alone
form neither a length nor a mass density.

## 8. Candidate-placement result

All nine preregistered placements are classified in
`CANDIDATE_RESPONSE_MAP_MATRIX.tsv`.

- `R01` is the only placement directly entailed by the current bootstrap
  words, and it is on-shell only.
- `R02-R03` supply exact density-response skeletons only after stronger
  unsupplied premises.
- `R04` is the correct general type under the owner multi-observable
  clarification, but its complete section and dual pairing are absent.
- `R05-R08` remain compatible representations or candidate families, not
  selected maps.
- `R09` would supply response by assuming the still-open action and therefore
  is provenance-blocked in this derivation direction.

No placement passes all eight gates.

## 9. Minimum missing object

The smallest missing object is now sharper:

> a metric-native differentiable coupled global-local closure section on the
> full extended finite-cell configuration space, together with the native dual
> pairing and branch regularity that turn its derivative into a physical local
> response.

It may be multi-observable. It must define both the global-to-local branch map
and local-to-global recomputation map, state the native energy/mass/curvature
and other functionals actually used, cover local and finite-cell variations,
and resolve or natively branch the calibrated-metric/conformal-class ontology.

This is one structural tile. It does not yet supply fields, action terms, full
equations, boundary functional, topology, dynamics, solution branches,
stability, or a density regime. Only after the response exists is Helmholtz
integrability or downstream action reconstruction a well-posed next question.
