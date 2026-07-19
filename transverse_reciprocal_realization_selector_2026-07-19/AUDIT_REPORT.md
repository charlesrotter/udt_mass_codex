# Transverse Reciprocal Realization Selector — Audit Report

Date: 2026-07-19

Base: `4f5cb5d18b4f3658789a0b0e5f88d1f9439e811a`

Preregistration commit: `5becdc1`

Mode: CPU-only, metric-led exact algebra and global-structure classification

## Result

`EXACT_REPRESENTATION_LEVEL_RECIPROCAL_HOPF_CORRESPONDENCE_CONDITIONAL_ON_LORENTZ_SPIN_REALIZATION; PHYSICAL_TRANSVERSE_SPATIAL_PERIODICITY_UNDERDETERMINED; GLOBAL_UNIT_HOPF_LIFT_AND_SOLDERING_OPEN; FINITE_CELL_CAP_GATE_NOT_ACTIVATED`

The prior reciprocal Hopf match is not a random resemblance. It is the exact projective geometry of
the same diagonal two-weight subgroup when that subgroup is conditionally realized in the
two-component Lorentz spin representation.

That correspondence does **not** derive two transverse physical spatial circles. The two component
phases have different roles: their relative phase is a celestial azimuth after an axis and frame are
chosen, while their common phase is the projective/Hopf fiber gauge. Neither is automatically a
second spacetime direction. Moreover, the bare oriented metric frame bundle over a direction sphere
has `SO(3) ≅ RP3` total space; the unit `S3` Hopf lift requires the `SU(2)` spin double cover.

The audit therefore sharpens the first gate rather than passing it. UDT now has an exact conditional
representation-level bridge from reciprocal dilation to projective/Hopf geometry. It still lacks a
native realization or soldering rule that makes this representation data a physical transverse
metric structure or a carrier field. Because physical transverse periodicity was not derived, the
finite-cell spatial cap-completion gate is not activated.

## Lay interpretation

The reciprocal pair behaves like two components that grow and shrink by opposite amounts. In
four-dimensional light-cone geometry, the standard square-root representation of a light direction
also has two complex components. A boost multiplies one component down and the other up by exactly
those reciprocal factors.

Remove their shared size and the pair lies on a three-sphere. Remove their shared phase as well and
what remains is a two-sphere of light directions. The familiar Hopf map is exactly that second
quotient. This explains why the earlier angular calculation found UDT's exponentials sitting inside
Hopf coordinates.

But the two angles in that description are not automatically two circles in physical space. One is
the direction around the celestial sphere. The other is the unobservable common phase used to
represent the same light ray. To make the phase lift global one also needs a spin lift of the metric
frame bundle. To make any of it physical matter one needs a rule attaching the representation to a
field over the cell and telling neighboring fibers how to compare.

So the hidden-in-plain-sight point is real but one level different from the previous guess: the Hopf
structure appears naturally in the metric's conditional representation geometry before it appears
as physical spatial topology or matter.

## Direct physical-spacetime routes

### Direct vector extension

The founding two-weight action is

```text
P(phi)=diag(exp(-phi),exp(phi)),
P^T K P=K,
K=[[0,1],[1,0]].
```

Its faithful block-diagonal extension to a Lorentz-signature four-vector representation is

```text
P4=diag(exp(-phi),exp(phi),1,1).
```

The exact script verifies `P4^T K4 P4=K4`. Its transverse two-plane is the identity. Thus the most
direct extension preserves the two transverse vector directions; it does not put reciprocal weights
on them.

This is not a theorem that all structured embeddings are impossible. It is a catch against claiming
that the founding pair automatically duplicates itself transversely.

### Scalar-to-shear equivariance obstruction

After a longitudinal axis is supplied, an isotropic oriented transverse plane has residual `SO(2)`
symmetry. A symmetric trace-free tensor on that plane has the form

```text
T=[[x,y],[y,-x]].
```

Requiring `R^T T R=T` under the transverse rotations forces `x=y=0`. Therefore a scalar `phi`, the
transverse metric, and orientation alone cannot naturally produce the nonzero shear
`diag(-phi,+phi)`. A director, derivative tensor, frame reduction, or other non-isotropic datum is
required.

Hodge duality does not evade this result. The Hodge dual of the longitudinal two-form is the
transverse area form. An area form or determinant constrains area; it does not split the plane into
two ordered line fields.

### Metric-derivative candidates

Projected Hessian, curvature, or shear tensors can select transverse eigenlines on a declared
nondegenerate stratum. Those are honest metric-derived candidate routes, not forbidden imports. They
do not provide a universal result:

- the exact finite countermodel has zero projected transverse Hessian;
- rotationally symmetric warped products have a projected Hessian proportional to the transverse
  metric;
- eigenlines become undefined where eigenvalues coincide;
- no current identity forces their eigenvalues to be `-phi,+phi`; and
- eigenline integral curves need not be Killing orbits, closed, or periodic.

The route remains `CONDITIONAL_STRATIFIED`, not rejected.

### Periodicity is global data

The same flat local transverse metric can be placed on a plane, disk, cylinder, or torus by changing
global identifications. Local C0/C1 algebra cannot distinguish their periods. Finite compactness also
does not imply a two-torus action: a round `S2` is compact but has no free effective `T2` action.

Two exact bounded kinematic families remain:

```text
R_t x [-L,L]_r x D2,
g=diag(-exp(-2 k r),exp(2 k r),1,1),
phi=k r,
```

and the analogous finite mirrored-depth product with a round transverse `S2`. Both have odd `phi`,
`phi=0` at the mirror, and the exact reciprocal longitudinal block, but neither has two transverse
reciprocal circle directions.

These are kinematic foundation-compatible counterfamilies, not claimed complete realized
matter-bearing universes. The action, boundary functional, and bootstrap admissibility equations do
not exist, so completeness cannot be certified. That caveat limits the result to
`UNDERDETERMINED_NOT_DERIVED`; it does not support an unconditional no-go.

Even granting a transverse `T2`, reciprocal axes do not imply periodic eigen-circles. On the standard
torus choose the constant orthonormal eigen-coframe obtained by rotating `dx,dy` through the
irrational slope `sqrt(2)`, and give its two axes weights `exp(-2phi),exp(2phi)`. Both eigenvector
flows are dense because their slopes are `sqrt(2)` and `-1/sqrt(2)`, not rational. For `phi=k s`, the
projected Hessian is nondegenerate and selects exactly those dense axes. Thus even a successful
metric-derivative axis selector still needs a separate integral lattice/closed-orbit theorem.

## Exact conditional spin/projective correspondence

### Null directions as projective doublets

Under the separately stamped four-dimensional conformal-Lorentzian readout, write a future null
Hermitian matrix as

```text
K=z z-dagger,
z=(z1,z2) in C2 minus {0}.
```

Its determinant vanishes identically. Multiplying `z` by a nonzero complex scalar does not change
the projective null direction. Consequently

```text
(C2 minus {0}) / C-star = CP1 = S2.
```

The Pauli bilinears give the unit direction

```text
n=(z-dagger sigma1 z, z-dagger sigma2 z, z-dagger sigma3 z)/(z-dagger z),
n dot n=1.
```

Positive Common-Scale multiplication cancels from this expression exactly.

This is geometric spin representation language, not a Dirac field, quantum spin, fermion
statistics, or an imported matter carrier.

### Reciprocal subgroup

The diagonal special-linear element

```text
B(a)=diag(exp(-a),exp(a)),
det B=1,
```

acts on the component magnitude ratio by

```text
|z2/z1| -> exp(2a)|z2/z1|.
```

For a normalized representative

```text
z=(cos(eta) exp(i xi1), sin(eta) exp(i xi2)),
```

the boost therefore translates reciprocal depth:

```text
tan(eta)=exp(2phi),
phi -> phi+a.
```

The induced phase-orbit block on the unit representative is

```text
diag(cos(eta)^2,sin(eta)^2).
```

Dividing by its positive orbit-area factor gives exactly

```text
diag(cot(eta),tan(eta))
=diag(exp(-2phi),exp(2phi)).
```

This is the previously banked reciprocal Hopf orbit block. The present audit identifies its
representation-theoretic origin.

The unshifted identification also contains a balanced-reference premise. Starting from generic
component magnitudes `a,b`, the determinant-normalized block is

```text
diag((a/b) exp(-2phi),(b/a) exp(2phi)).
```

It equals the prior block at the physical `phi=0` seal only when `a=b`. Algebraically the imbalance
can be absorbed into an additive depth offset, but the finite-cell seal already fixes the physical
zero of `phi`; the equal-amplitude ray must therefore be derived or retained as `CHOSE`.

The real positive diagonal embedding is not selected by the metric magnitudes alone. The family

```text
A_alpha(phi)=diag(exp[(-1+i alpha)phi],exp[(1-i alpha)phi])
```

also has determinant one and exactly the same Hermitian magnitude weights. It adds a relative phase
rotation. Literal preservation of the founding real positive action sets `alpha=0`; an embedding
specified only through metric weights does not. Thus the untwisted spin realization retains an
explicit representation-map premise.

The projective direction is likewise exact:

```text
n(phi,delta)=(sech(2phi) cos(delta),
              sech(2phi) sin(delta),
              -tanh(2phi)),
delta=xi2-xi1.
```

Thus reciprocal depth is celestial latitude in the conditional projective realization, while the
relative phase is celestial azimuth.

### What the two phases mean

The component phase torus is easy to misread.

- `xi1,xi2 -> xi1+gamma,xi2+gamma` is the common phase. It leaves every null direction unchanged and
  is the Hopf-fiber gauge.
- `xi1,xi2 -> xi1+beta,xi2-beta` changes the relative phase by `-2beta` and rotates celestial
  azimuth about the chosen boost axis.
- A generic common-phase matrix has determinant `exp(2 i gamma)` and is not itself in `SL(2,C)`;
  the relative-phase matrix has determinant one.

The periodic `T2` coordinate description is therefore one gauge circle plus one directional circle,
not two physical spacetime circles.

## Positive-scale quotient and its normalization premise

Quotienting a nonzero complex doublet only by positive real scale gives a manifold diffeomorphic to
`S3`. Selecting the familiar unit representative requires a positive Hermitian norm.

No positive Hermitian norm is invariant under the full Lorentz boost subgroup. For the exact boost
`diag(1/2,2)`, invariance of a Hermitian matrix forces both diagonal entries to zero, leaving
nonpositive determinant. A unit `S3` representative therefore uses an observer, compact-frame
reduction, or chosen Hermitian norm. Its topology is robust; its round metric and normalization are
not bare Lorentz invariants.

This is compatible with Common-Scale Neutrality but is not selected by it. CSN removes positive
common scale; it does not choose the norm used to draw the unit representative.

The boost acts conformally, not isometrically, on the round Fubini–Study sphere. In projective
coordinate `w`, the real rescaling `w -> lambda w` changes the round metric by

```text
lambda^2 (1+|w|^2)^2 / (1+lambda^2 |w|^2)^2.
```

At `lambda=2`, `|w|=1`, the factor is exactly `16/25`, not one. The topological/conformal celestial
`S2` is Lorentz-natural; a fixed round target metric is not.

## Bare metric frames versus the unit Hopf lift

There are two global bundles that must not be conflated:

```text
SO(2) -> SO(3) -> S2,
U(1)  -> SU(2) -> S2.
```

The first is the oriented rotation-frame bundle supplied after choosing an observer in bare metric
geometry. Its total space is `SO(3) ≅ RP3`, and its circle bundle has Euler-class magnitude two.
The second is its spin double cover. Its total space is `SU(2) ≅ S3`, and its Hopf bundle has
first-Chern-class magnitude one.

The exact connection calculation on the conditional unit-spinor lift gives

```text
A=cos(eta)^2 dxi1+sin(eta)^2 dxi2,
integral A wedge dA=-4 pi^2,
Q=1
```

in the registered normalization. This unit class is exact once the spin lift is supplied. Bare
metric direction geometry alone gives the `SO(3)/RP3` frame bundle, not the unit `S3` lift.

Local spin frames always exist on a contractible chart. A global lift requires the appropriate
topological spin condition and a choice among spin structures when more than one exists. Current
C0/C1 does not derive the complete time-live manifold or such a choice. Particular future product
geometries with oriented three-dimensional slices may admit a spin lift automatically, but that is
a conditional global theorem about those geometries, not a present selector.

Likewise, the full abstract range `phi in R` covers the open principal-orbit chart of the
representation `S3`, with one component vanishing at each endpoint. C0/C1 does not establish that a
physical depth field spans that range or reaches those limits. Representation caps are not physical
finite-cell caps.

## Soldering and physical meaning

The spin/projective theorem improves the type map but does not finish it. It gives a standard
representation of a conditionally realized Lorentz subgroup and a projective null-direction bundle.
It does not supply:

- a section choosing one projective direction at every event;
- a native rule identifying the common phase with physical data rather than gauge;
- two transverse tangent line distributions;
- a global spin structure and spin-frame transition law;
- a Common-Scale-compatible transport/connection selected for the physical field;
- finite-cell boundary data for that field; or
- an action determining how the section varies.

Calling the complex doublet a matter spinor would add precisely the missing physical field by hand.
Calling its two phases spatial angles would add precisely the missing soldering by hand. Neither move
is allowed by the derivation.

## Finite cell and bootstrap

The finite-cell canon supplies a finite mirrored monotone depth domain, no spatial infinity, and the
static `phi` seal value/parity. It supplies no transverse topology, period lattice, spin lift,
observer, section, or boundary functional.

The bootstrap principle requires complete self-consistent matter-bearing solutions but contains no
present equation or map that compares the disk, sphere, torus, frame-bundle, or spin-lift families.
It may eventually select among complete solutions after the missing action and boundary law exist.
It cannot currently be used as the selector itself.

## Mechanical adjudication

| Question | Ruling | Reason |
|---|---|---|
| Does the direct reciprocal vector action shear the transverse plane? | `NO` | Its faithful direct extension is the identity transversely. |
| Can scalar `phi` plus transverse isotropy select two axes? | `NO IN THAT CLASS` | `SO(2)` equivariance forces the trace-free tensor to zero. |
| Can metric derivatives select axes? | `CONDITIONAL_STRATIFIED` | Possible on nondegenerate strata; no universal spectrum or closed-orbit theorem follows. |
| Does finite compactness imply a transverse `T2`? | `NO` | Disk and `S2` bounded families remain; periods are global quotient data. |
| Do reciprocal axes on a supplied `T2` imply periodic eigen-circles? | `NO` | Irrational-slope eigenflows are dense, even when a nondegenerate projected Hessian selects them. |
| Is the reciprocal Hopf match accidental? | `NO` | It is the exact diagonal `SL(2,C)` spin-representation/projective correspondence. |
| Is that representation foundation-level physical spacetime data? | `NO / CONDITIONAL` | Lorentz embedding, spin frame, normalization, global lift, and soldering remain premise-stamped. |
| Do the two phases give two spatial circles? | `NO` | One is celestial azimuth; one is common projective gauge. |
| Does the bare metric give the unit `S3` Hopf bundle? | `NO` | Bare rotation frames give `RP3`; `S3` requires the spin double cover. |
| Is the physical first gate passed? | `NO` | No physical transverse reciprocal line pair with compact orbits is derived. |
| Is the cap gate active? | `NO` | Its physical periodic-spatial prerequisite is absent. |
| Is a carrier/action derived? | `NO / OPEN` | Representation topology supplies neither a field section nor dynamics. |

The exact seven-family census is `CANDIDATE_FAMILY.tsv`; the premise-stamped 22-row result is
`STATUS_LEDGER.tsv`.

## Revised smallest missing gate

The representation result suggests that the earlier first gate had two possible branches:

1. derive reciprocal periodic directions in the **physical transverse metric**; or
2. derive a **spin/projective realization plus soldering** that makes the naturally periodic
   representation geometry a physical field or carrier without calling it physical space.

The first branch remains underdetermined. The second now has an exact mathematical middle but open
ends. Its smallest missing object is:

> a native realization/soldering rule connecting reciprocal projective geometry to a physical
> section, transverse metric datum, or carrier, including its global lift, transport, and finite-cell
> boundary status.

This is a description of the gap, not a new UDT principle. A complete action may ultimately provide
the rule, or a parent whole-solution law may make the representation physical. The present audit
does not choose between them.

## Completeness map

This result is one kinematic/representation tile:

- **fields:** metric/conformal frame data only; no matter field varied;
- **action/equations:** absent and open;
- **domain:** local 4D Lorentz representation plus finite disk, sphere, plane/torus, and bundle
  counterfamilies;
- **boundary:** current static `phi` seal data only;
- **topology:** local projective `CP1`, metric frame `RP3`, conditional spin lift `S3`, and nontoric
  bounded transverse families;
- **dynamics, branches, stability, mass:** not entered;
- **global time-live spin cobordism and all off-toric manifolds:** not classified.

The result does not exhaust the full solution space because the complete theory is not yet present.

## What is not claimed

- No physical transverse torus or angular period is derived.
- No spatial `S3` universe or finite-cell cap is selected.
- No matter spinor, spin-1/2 statistics, Dirac equation, or quantum structure is imported or derived.
- No carrier section, fixed target metric, transport law, `L2+L4` action, source, boundary charge,
  time-live stability, or mass follows.
- No action/variation bridge is closed.
- No canonization, GPU work, repository reorganization, or particle solve was performed.

## Four evidence gates

1. **Preregistered:** yes, commit `5becdc1` before load-bearing algebra.
2. **Scope:** bounded local representation and registered counterfamily classification; not a full
   action or manifold theorem.
3. **Independent verification:** controller replay and catch-proofs are recorded in
   `VERIFICATION_RESULT.json`; fresh zero-context semantic review is recorded separately in
   `EXTERNAL_ADVERSARIAL_REVIEW.md`. The controller's hard-coded classification checks are treated
   as self-consistency evidence; independently reconstructed algebra and counterfamilies carry the
   load-bearing conclusion.
4. **Premises:** explicit in `PREREGISTRATION.md`, `SOURCE_INVENTORY.tsv`, `CANDIDATE_FAMILY.tsv`, and
   `STATUS_LEDGER.tsv`.
