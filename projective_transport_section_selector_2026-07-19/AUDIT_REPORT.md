# Projective Transport and Physical-Section Selector — Audit Report

Date: 2026-07-19

Base: `75c62d1a357821d4957588e640ba03f0bc0f285e`

Preregistration commit: `9a357c5`

Mode: CPU-only, metric-led exact conformal transport and bounded section classification

## Result

`CONFORMAL_NULL_GEODESIC_PROPAGATION_DERIVED_CONDITIONAL; LEVI_CIVITA_TANGENT_RAY_COMPARISON_CSN_REPRESENTATIVE_DEPENDENT; CONDITIONAL_STATIC_PHI_ROUTE_SELECTS_ONLY_A_LONGITUDINAL_NULL_PAIR; PHI_ANGULAR_PHYSICAL_SECTION_UNDERDETERMINED; CONFORMAL_TRACTOR_AND_HOPF_CONNECTIONS_TRANSPORT_REPRESENTATION_DATA_BUT_DO_NOT_SELECT_A_SECTION; GLOBAL_HOLONOMY_AND_PROJECTIVE_TO_PHYSICAL_SOLDERING_OPEN; PHYSICAL_PROJECTIVE_REALIZATION_GATE_NOT_PASSED`

The metric supplies more than the preceding audit had established, but less than a carrier bridge.
After the inherited/conditional four-dimensional conformal-Lorentzian readout, the conformal metric
canonically propagates every already-chosen null ray as an unparametrized null geodesic. This is an
exact Common-Scale-invariant causal-flow result.

It does not choose the initial ray. Ordinary Levi-Civita comparison of rays in arbitrary base
directions depends on the metric representative. The normal conformal Cartan/tractor connection
does provide canonical representation transport, but not a selected tangent-null section. The
conditional Hopf connection similarly transports phase data after a projective path and lift have
been supplied; pulling it back to spacetime already requires the section being sought.

`phi` and angular curvature contain real local selector candidates. A nonzero null `d phi` on an
open eikonal region gives a conformally natural geodesic null line. Petrov types II, III, and N have
a locally unique highest-multiplicity Weyl principal null direction. Neither stratum is forced by
the registered foundation, and neither is presently proved global, smooth through type changes, or
the physical carrier section. In the conditional static spacelike-gradient branch, `phi` supplies
only the familiar inward/outward longitudinal null pair after a time direction is also supplied.

The physical projective-realization gate therefore remains unpassed. The result narrows the next
question from an unspecified soldering principle to a concrete metric-solution question: does UDT
force a globally coherent null-gradient or algebraically-special curvature branch whose selected
null line survives transport and boundary closure?

## Lay interpretation

The metric gives us the road system for light. If we place a light arrow at one point, the conformal
geometry tells us the path that arrow follows, and changing the common ruler/clock calibration does
not change the path—only how quickly we label progress along it.

But road rules do not decide which road an arrow begins on. Nor does a rule for carrying an arrow
between points create the first arrow. That is the distinction between **propagation** and
**selection**.

`phi` sometimes provides an arrow-like object. In an ordinary static radial setting it gives the
inward and outward radial light directions, but it does not choose the angular/Hopf direction. On
special geometries, the curvature itself can contain one unusually repeated light direction. That
is the most promising metric-only selector found here. The unresolved question is whether UDT's
whole metric equations force that special situation everywhere needed, rather than merely allowing
it locally.

So the search is narrower again: not “invent a connection,” but “test whether UDT forces a unique
conformal null line and its global closure.”

## Three distinct geometric levels

Let `Z -> M` denote the conditional bundle of projective future null directions, with celestial
`S2` fiber.

1. **Propagation:** a vector field on `Z` carries any chosen null initial direction along its own
   null trajectory.
2. **Comparison:** a connection compares fiber data over arbitrary nearby base points.
3. **Selection:** a section `s:M->Z` chooses one direction at each point.

The conformal null spray certifies level 1. A representative Levi-Civita connection supplies a
version of level 2 but is not CSN-independent. Normal conformal tractor geometry supplies canonical
comparison in a larger representation bundle. None of these facts supplies level 3.

## Exact conformal null propagation

For

```text
H=(1/2) g^(ab) p_a p_b,
g_tilde=Omega^2 g,
H_tilde=Omega^-2 H=f H,
```

Hamiltonian vector fields obey

```text
X_(fH)=f X_H + H X_f.
```

On the nonzero null shell `H=0`,

```text
X_(H_tilde)=Omega^-2 X_H.
```

The characteristic line field is unchanged. Its integral curves differ only by positive
reparametrization, so the projected unparametrized null geodesics are Common-Scale invariant.

The same fact follows from the exact conformal connection change. With
`Upsilon=d log(Omega)`,

```text
nabla_tilde_k k = nabla_k k + 2 Upsilon(k) k - g(k,k) Upsilon-sharp.
```

For null `k`, the new term along its own path is proportional to `k`. This certifies propagation of
every supplied ray. Because every ray receives the same status, it supplies no selector.

## Why arbitrary Levi-Civita comparison is not CSN-invariant

For arbitrary base direction `X`,

```text
nabla_tilde_X k - nabla_X k
= Upsilon(X) k + Upsilon(k) X - g(X,k) Upsilon-sharp.
```

Only the first term is automatically projectively invisible. The other terms generally contain a
component transverse to `k`.

The exact controller counterexample uses Minkowski signature,

```text
k=(1,0,0,1),
X=(0,1,0,0),
d log(Omega)=(0,0,0,a).
```

Then

```text
nabla_tilde_X k - nabla_X k = a X,
```

which is not proportional to `k`. The independent adversary strengthened this to an integrated
example: along a transverse flat-space path, exact parallel transport in a conformally related
metric rotates a formerly constant null direction even when `Omega=1` pointwise on that path; its
transverse gradient is enough.

Thus a chosen representative or Weyl structure can supply arbitrary tangent transport, but CSN does
not make that choice physical.

## Normal conformal Cartan and tractor transport

A smooth conformal structure in dimension at least three conditionally supplies its normal conformal
Cartan connection, standard tractor bundle, tractor metric, curvature, and holonomy. In four
dimensions the standard tractor bundle has rank six. This is a genuine canonical comparison
structure at the conformal representation level; it is not being rejected.

It does not supply a canonical Levi-Civita connection on the tangent bundle, a preferred conformal
representative, or a tangent-null section. In a metric splitting,

```text
nabla^T_a (sigma, mu_b, rho)
= (nabla_a sigma-mu_a,
   nabla_a mu_b+P_ab sigma+g_ab rho,
   nabla_a rho-P_a^c mu_c).
```

The splitting itself changes with representative. A chosen flat null geodesic can be encoded by a
parallel tractor two-plane, but transporting that plane in a transverse base direction does not
generally leave it decodable as a tangent-null ray containing the canonical tractor line. Recovering
ordinary tangent transport requires a Weyl structure/scale or another reduction.

The honest result is therefore `CANONICAL_CONDITIONAL_REPRESENTATION_TRANSPORT`, not a physical
section theorem.

## Complete `d phi` branch census

Let

```text
p=d phi,
P=g^-1(p,p).
```

The zero/sign classification of `P` is Common-Scale invariant, and wherever `p` is nonzero its
metric-dual projective line is invariant because

```text
sharp_(Omega^2 g)(p)=Omega^-2 sharp_g(p).
```

The complete local census is:

| Stratum | Strongest metric result |
|---|---|
| `d phi=0` | No direction; the celestial `S2` remains. |
| `d phi !=0`, `P=0` | One conformally invariant local null line. |
| `P<0` | A timelike line, leaving a spatial-direction `S2`. |
| `P>0` | A spacelike line; a time direction is additionally required to form null rays. |
| type change or `d phi ->0` | Normalized constructions become singular; continuation is open. |

If `P=0` throughout an open region, the gradient line is geodesic by the metric identity

```text
p^b nabla_b p_a = (1/2) nabla_a(P)=0.
```

Being null only at an isolated point does not establish that conclusion.

In a separately supplied static branch with a future unit time direction `u` orthogonal to a
spacelike `d phi`, define unit `n` along increasing `phi`. Then

```text
k_plus=u+n,
k_minus=u-n
```

are future null rays. For the reciprocal static representative,

```text
u=exp(phi) partial_t,
n=exp(-phi) partial_r.
```

This is a genuine conditional metric result. It uses static time data not derived by C0/C1, returns
two longitudinal rays, and does not produce the angular/projective carrier section. Choosing one
also invokes radial orientation or an incoming/outgoing convention; `phi -> -phi` exchanges their
roles.

## Angular interaction with `phi`

For the scalar Hessian,

```text
H_tilde_ab
=H_ab-Upsilon_a phi_b-Upsilon_b phi_a+g_ab Upsilon^c phi_c.
```

On a supplied transverse two-screen:

- if `d_A phi` is nonzero, the projected trace-free Hessian generally changes with the conformal
  representative;
- if `d_A phi=0`, its transverse change is pure trace, so the transverse STF part is
  Common-Scale compatible;
- a nonzero STF tensor has two eigenlines, not one oriented line;
- at zero or repeated-eigenvalue strata, the axes disappear; and
- local eigenlines need not have closed orbits, integral periods, or global continuation.

This is a meaningful conditional angular selector, but it presupposes the transverse screen and a
nondegenerate branch. Intrinsic two-dimensional Ricci curvature cannot improve it because
`Ric_AB=K h_AB` has zero trace-free part.

### Weyl principal-null directions: strongest metric-only route

The Weyl tensor is conformally natural, so its principal null directions avoid the representative
problem. The exact root multiplicities give:

| Petrov type | Principal-null structure | Selector status |
|---|---|---|
| I | four simple lines | no canonical winner |
| II | one double plus two simple | one local highest-multiplicity line |
| D | two double lines | two-way ambiguity |
| III | one triple plus one simple | one local highest-multiplicity line |
| N | one quadruple line | one local line |
| O | Weyl zero | every null line/no selector |

Types II, III, and N therefore offer an honest local, conformally natural candidate. Current UDT
does not force any of those types. Petrov transitions and discriminant loci can destroy smooth
global continuation. A principal null direction is also not automatically geodesic without extra
curvature/field-equation conditions; no GR equation is imported to supply them.

This is the main surviving positive lead from the angular-curvature sector.

## Why the Hopf connection cannot select its own spacetime section

On the conditional normalized spin lift,

```text
A=-i z-dagger dz
 =cos(eta)^2 d xi1 + sin(eta)^2 d xi2.
```

It is an exact principal-`U(1)` connection on the representation bundle `S3->S2`. Given a path on
the projective `S2` and an initial phase lift, it determines horizontal phase transport.

To obtain a spacetime one-form, however, one must pull it back:

```text
a=z-star A.
```

That expression already requires `z(x)` or at least a projective map `n(x)`, plus lift data. The map
is precisely the open physical section. Using `A` to derive `z(x)` would therefore be circular.

The Hopf connection transports representation data after selection. It does not solder the
representation to spacetime or identify it with the existing carrier.

## Global section and holonomy

For a chosen connection, a path-independent parallel projective section from seed `[k_x]` requires

```text
[k_x] in Fix(Hol_x).
```

The exact counterfamilies show three representative possibilities rather than an exhaustive
conformal-holonomy census:

- identity holonomy fixes the entire celestial `S2`, giving many parallel sections and no unique
  choice;
- a single spatial-axis rotation fixes an unoriented line/two celestial antipodes;
- two nonparallel rotational holonomies have no common nonzero fixed direction;
- a special reduced holonomy could fix one projective ray, but no current UDT theorem forces that
  reduction.

Parallel transport also needs an initial seed. Curvature and holonomy may preserve, multiply, or
obstruct seeds; they do not generally create one.

## Foundation-compatible counterfamilies

### Flat neutral family: many selectors

The mathematically allowed `phi=0` conformal-flat member has zero `d phi`, zero Hessian, zero Weyl
tensor, and trivial local holonomy. Every constant future null direction is parallel. This refutes a
universal selector theorem from the registered foundation, while respecting the separate ruling
that nonzero dilation in the realized universe is `OBSERVED` rather than axiomatically forced.

### Nonzero reciprocal warped family: longitudinal pair only

On

```text
R_t x [-L,L]_r x D2,
g=diag(-exp(-2 k r),exp(2 k r),1,1),
phi=k r,
```

the exact reciprocal block and odd seal parity hold. With its conditional static time direction,
`d phi` gives the two radial null rays. The transverse plane retains `SO(2)` isotropy and supplies no
angular axis or carrier-like section.

### Isotropic curved finite family: no natural parallel selector

A finite cell cut from a static product with round spatial `S3` and `phi=0` has vanishing `d phi`,
isotropic Hessian, and conformally flat Weyl tensor. Spatial rotational holonomy has no invariant
nonzero spatial vector and hence no invariant null ray after a time direction is supplied. Arbitrary
null fields can still be chosen; none is naturally selected by the registered data.

These are kinematic foundation-compatible counterfamilies, not certified complete on-shell UDT
universes. The absent action, boundary equations, and bootstrap evaluation map prevent that stronger
claim. They establish `UNDERDETERMINED_NOT_DERIVED`, not an unconditional future no-go.

## Finite cell and bootstrap

The finite-cell authority specifies a finite mirrored domain, no spatial infinity, and limited
static `phi` seal parity/value. It does not specify a null seed, screen, representative, connection,
holonomy reduction, section boundary value, or carrier map.

Bootstrap remains working on-shell admissibility wording. Without the completed field census,
action, boundary law, and comparison map, it cannot rank the retained section/holonomy families.

## Mechanical adjudication

| Question | Ruling | Reason |
|---|---|---|
| Does the conformal metric propagate a chosen light ray? | `YES / DERIVED_CONDITIONAL` | The null Hamiltonian spray changes only by reparametrization. |
| Does that choose the initial ray? | `NO` | The spray exists for every null ray. |
| Is arbitrary Levi-Civita ray comparison CSN-invariant? | `NO` | The conformal connection change has transverse terms. |
| Does normal conformal tractor transport exist? | `YES / CONDITIONAL` | It is canonical representation transport for a conformal structure. |
| Does tractor transport select a tangent-null section? | `NO` | A tangent reduction/scale and a seed remain absent. |
| Can `d phi` select a null line? | `ONLY ON STRATA` | Directly when null; conditionally as a longitudinal pair with added time data when spacelike. |
| Can angular Hessian data select axes? | `CONDITIONAL_STRATIFIED` | Only with a supplied screen and nondegenerate STF tensor. |
| Can Weyl curvature select a line? | `LOCAL LEAD` | Types II, III, N have one highest-multiplicity line; UDT does not force or globalize those types. |
| Does the Hopf connection give the spacetime map? | `NO` | Its pullback requires the map being sought. |
| Does holonomy select a seed? | `NO IN GENERAL` | Fixed sets can be all, a pair, one only under special reduction, or empty. |
| Is the physical projective gate passed? | `NO` | No global frame-independent carrier-like section is derived. |

## Revised smallest missing theorem

The next genuinely missing object is not an invented new principle. It is a theorem, if the UDT
metric can supply it, that complete admissible solutions possess a smooth conformally natural null
line—most concretely from either:

1. a globally null/eikonal `d phi`; or
2. a globally coherent algebraically special Weyl branch with one distinguished repeated principal
   null direction—

and that this line is compatible with transport, finite-cell boundary closure, and the required
physical type.

No current result says that theorem is true. The two candidates are now exact targets for the next
metric solution-space audit rather than premises to adopt.

## Completeness map

This result is one conformal-transport/section tile:

- **fields:** conformal metric and scalar `phi`; no matter field varied;
- **action/equations:** absent and open;
- **domain:** local smooth 4D conformal-Lorentzian geometry plus bounded symmetry/holonomy families;
- **boundary:** current static `phi` seal information only;
- **topology:** local celestial/projective bundle and conditional Hopf lift; no physical spatial
  topology selected;
- **branches:** complete local `d phi` causal census and representative Petrov strata, not all
  conformal holonomies or global manifolds;
- **dynamics, stability, mass:** not entered.

The absent full equations, solution census, boundary variational law, and global holonomy
classification could change the physical result in a future completion.

## What is not claimed

- No carrier or fixed round target is derived.
- No transverse torus, period, spatial `S3`, or cap is selected.
- No unique observer, foliation, conformal representative, spin frame, or global lift is selected.
- No Weyl/Petrov type is claimed to be forced by UDT.
- No action, source, boundary charge, time-live topology law, stability, or mass follows.
- No GR field equation, quantum spinor, or Standard Model structure was imported.
- No canonization, GPU work, repository reorganization, or particle solve was performed.

## Four evidence gates

1. **Preregistered:** yes, commit `9a357c5` before load-bearing algebra.
2. **Scope:** bounded conformal transport, `phi`/curvature selectors, and holonomy counterfamilies;
   not a full action or global-manifold theorem.
3. **Independent verification:** controller exact algebra and fail-closed verifier are recorded in
   `DERIVATION_RESULT.json` and `VERIFICATION_RESULT.json`; fresh zero-context review is recorded in
   `EXTERNAL_ADVERSARIAL_REVIEW.md`. The 54 controller checks include exact identities,
   classification locks, and some deliberately simple self-consistency checks; they are not claimed
   to be 54 independent scientific facts. The independently reconstructed algebra and semantic
   geometry carry the verdict.
4. **Premises:** explicit in `PREREGISTRATION.md`, `SOURCE_INVENTORY.tsv`, `CANDIDATE_FAMILY.tsv`, and
   `STATUS_LEDGER.tsv`.
