# G315 exact derivation — conditional Cauchy and characteristic data interface

Date: 2026-09-01
Scope: bounded regular local G312/G313 metric-only vacuum arena

## 1. Bounded landing

```text
ACTIVE_EQUATION_HAS_A_LAWFUL_CONDITIONAL_DATA_INTERFACE
__CAUCHY_AND_CHARACTERISTIC_DATA_REMAIN_FREELY_SUPPLIED_WITH_DERIVED_CONSTRAINTS
```

Status before external review: `INTERNALLY_DERIVED_AND_IMPLEMENTATION_DISTINCT_VERIFIED_BOUNDED`.

This does not select one universe. It identifies the exact kind of supplied data on which the
owner-adopted-provisional bounded equation has a conditional local development.

## 2. Active equation and ownership

Universal Reciprocity/DDR and the two G312 premises are owner-adopted provisionally, not derived
or canonized. Inside their registered smooth regular local metric-only scale-free vacuum arena,

\[
S_{ab}=R_{ab}-\frac14R g_{ab}=0.
\]

The contracted Bianchi identity gives, on each connected solution region,

\[
R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0.
\]

G315 does not import or vary an action and does not add a source equation. It projects this already
active equation onto regular starting hypersurfaces.

## 3. Spacelike data and constraints

Let `Sigma` be a smooth spacelike hypersurface. Its geometric data are:

- a positive-definite induced metric `gamma_ij`;
- a symmetric second fundamental form `K_ij`, with convention
  `K_ij=-(1/2)L_n gamma_ij` for future unit normal `n`.

Gauss--Codazzi gives the normal projections of the active equation:

\[
\boxed{{}^{(3)}R+K^2-K_{ij}K^{ij}=2\Lambda},
\]

\[
\boxed{D_j(K^{ij}-\gamma^{ij}K)=0}.
\]

These are one scalar Hamiltonian constraint and three momentum constraints. A pair
`(gamma_ij,K_ij)` is lawful conditional data only if it satisfies them. The equation does not say
that every arbitrary seed pair is admissible.

If `Lambda` is not independently supplied, the equivalent connected-slice condition is

\[
\mathcal M_i=0,\qquad D_i\mathcal H=0,
\qquad \Lambda=\frac12\mathcal H,
\]

where `H` is the left side of the Hamiltonian constraint. Thus the extra trace-free-Ricci freedom
is one connected constant, not a freely specifiable function.

### Shape/trace split

Write

\[
K_{ij}=A_{ij}+\frac13\tau\gamma_{ij},
\qquad A^i{}_i=0,
\qquad \tau=K.
\]

Then the same constraints become

\[
\boxed{{}^{(3)}R+\frac23\tau^2-A_{ij}A^{ij}=2\Lambda},
\]

\[
\boxed{D_jA^{ij}-\frac23D^i\tau=0}.
\]

This is a decomposition of the full constraint surface, not a new constitutive law and not a
requirement that the data be homogeneous, round, constant-mean-curvature, or conformally flat.

## 4. What the equation propagates

Choose a regular lapse `N` and shift `beta^i`. They specify how coordinates move from one slice to
the next; they are gauge presentation, not UDT-selected physical data. With the registered sign
convention, the complete local evolution presentation is

\[
(\partial_t-\mathcal L_\beta)\gamma_{ij}=-2N K_{ij},
\]

\[
(\partial_t-\mathcal L_\beta)K_{ij}
=-D_iD_jN+N\left({}^{(3)}R_{ij}+K K_{ij}
-2K_i{}^kK_{kj}-\Lambda\gamma_{ij}\right).
\]

The equation therefore propagates the complete spatial metric and its initial normal rate. It does
not evolve a separate universal radial `phi` profile. `phi` and terminal `phi_pair` remain
presentation/readout quantities extracted downstream from the evolved metric and a supplied germ.

Define `E_ab=G_ab+Lambda g_ab`. Since `dLambda=0`, contracted Bianchi gives

\[
\nabla^aE_{ab}=0.
\]

After the spatial evolution equations are imposed, this identity gives a homogeneous propagation
system for the normal constraint projections. Consequently, initial vanishing of the Hamiltonian
and momentum residuals is preserved locally, conditional on the standard smooth hyperbolic
reduction theorem already caveated in G303. G315 does not prove that general PDE theorem or a
global-completeness result.

## 5. Functional data burden

Before quotienting, `gamma_ij` and `K_ij` contain twelve functions. At a generic regular local point:

- four constraint relations remove four phase-space functions;
- four spacetime-coordinate freedoms remove four gauge functions;
- four physical phase-space functions remain.

They correspond to two local metric configuration modes and their initial rates. This is a generic
principal/local count, not a global parameterization theorem. Constraint existence, topology,
boundaries, symmetries, Killing fields, and degeneracies can change global moduli and are not
classified here.

## 6. Exact spacelike controls

All four preregistered controls satisfy the same constraint form:

1. round positive bounce: `R3=6/X^2`, `K_ij=0`, `Lambda=3/X^2`;
2. flat positive slicing: `R3=0`, `K_ij=-H gamma_ij`, `Lambda=3H^2`;
3. positive product time-symmetric slice: `R3=2Lambda`, `K_ij=0`;
4. G313 Berger-`S3` data at `Lambda=3`: `R3=7/2`, `K_ij=h gamma_ij`, `h^2=5/12`.

The flat-slicing and round-bounce controls also fix the sign `-Lambda gamma_ij` in the `K_ij`
evolution equation. The distinct round, product, flat-slicing, and Berger signatures at the same
positive scalar sector demonstrate that the data interface constrains but does not select a unique
snapshot.

## 7. Characteristic/null data interface

Let `N` be a smooth null hypersurface with twist-free affinely parametrized generator `ell`. Its
two-dimensional screen has metric `q_AB` and null second fundamental form

\[
\chi_{AB}=\frac12\mathcal L_\ell q_{AB}.
\]

Decompose

\[
\theta=q^{AB}\chi_{AB},
\qquad
\sigma_{AB}=\chi_{AB}-\frac12\theta q_{AB}.
\]

The `ell-ell` projection of the active equation is

\[
R_{ab}\ell^a\ell^b
=\Lambda g_{ab}\ell^a\ell^b=0.
\]

Raychaudhuri therefore gives the exact same-null transport constraint

\[
\boxed{\mathcal L_\ell\theta
=-\frac12\theta^2-\sigma_{AB}\sigma^{AB}}.
\]

The connected scalar does not appear directly in this equation. It is not a focusing profile
painted independently along each null generator.

For a second null normal `k`, cross-normalized by `g(ell,k)=-1`, the mixed projection is

\[
\boxed{R_{ab}\ell^a k^b=-\Lambda}.
\]

Thus the scalar is invisible to the same-null Ricci projection but remains present in the complete
two-direction/cross-normal geometry.

A local characteristic problem normally supplies two transversely intersecting null
hypersurfaces, compatible screen/conformal or shear data along them, and compatible corner data at
their intersection. Null constraints transport expansion and other connection variables along the
generators; generator normalization and parameterization retain gauge freedom. One isolated null
sheet is not promoted here to a complete local data set.

The exact minimal list depends on the chosen double-null formalism. G315 therefore claims only the
invariant hierarchy above, conditional on standard regular characteristic existence theorems. It
does not cover caustics, singular corners, timelike boundaries, or global characteristic
completion.

## 8. Reciprocal kernel position in the evolution chain

The metric evolution is upstream. After a metric development and a lawful observer/event germ are
supplied, the complete pullback forms `h=F^*g`; screen, angular, mixing, and shift contributions
enter before terminal reciprocal readout. The pair evaluator reads the evolved geometry. It adds
no independent second-normal Cauchy residual in the registered architecture.

Therefore the conditional chain is

```text
lawful hypersurface data + gauge
    -> local metric development under Ric=Lambda g
    -> supplied observer/event germ and complete pair pullback
    -> reciprocal/projective readout
```

It is not

```text
pair readout -> independently chosen evolution profile.
```

## 9. Meaning of the result

The earlier “physical history” gap is now typed, inside the bounded vacuum arena, as ordinary
conditional initial-data freedom rather than an unrestricted missing `phi(r)` formula. The active
equation constrains and propagates complete metric data, but does not choose which lawful data
Nature supplies.

Unique-universe bootstrap, actualization/population, scalar magnitude, topology, boundary/global
completion, sources, matter, mass, observations, calibrated scale, physical `X_max`, and the full
outside-G312 UDT extension remain open. Metric, reciprocal kernel, angular cancellation, and
observational interfaces are unchanged.
