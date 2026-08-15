# Exact derivation — null-carrier measure ownership from the complete query

Date: 2026-08-15

## 1. Result

A supplied regular null-query realization gives an exact closed **geometric query-label
three-form**. If source proper-time and sky labels are held fixed along each ray, their label measure
pushes through the realization unchanged. This closure is tautological query bookkeeping, not a new
UDT field equation or metric-owned conservation law. The complete metric/coframe supplies its
invariant volume, density, focusing, and Jacobi representation.

That statement is not yet physical radiative survival. The label current counts the query's labels;
the metric does not identify emitted light, wave action, particle number, or any other physical cargo
with it. The exact landing is therefore

```text
LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL
__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING
__METRIC_DENSITY_AND_JACOBI_REPRESENTATION_EXACT
__PHYSICAL_CARRIER_IDENTIFICATION_POPULATION_ZERO_SIDE_FLUX_AND_ETA_OPEN
```

This sharpens the type boundary but does not narrow physical ownership beyond G94/G95. A new
differential equation is not needed merely to push forward a supplied label measure. What remains
missing is the physical statement that the radiative amount used in G94 is represented by this
transported measure and has physical zero side flux.

## 2. Full regular query-tube construction

Let `(M,g)` be a supplied oriented, time-oriented Lorentzian four-geometry. Let one supplied regular
null-query realization be

```text
R:(lambda,s,y1,y2) -> M,
```

where `lambda` is affine position along a null generator, `s` is source proper time, and `(y1,y2)`
are source-sky labels. On the bounded regular branch, `R` is locally invertible. Its tangent

```text
K=R_*(partial_lambda)
```

is null and affinely geodesic by the query construction.

Pull the metric volume form back to the label domain:

```text
R^*(vol_g)=J(lambda,s,y) dlambda wedge ds wedge dy1 wedge dy2,
```

with nonzero signed Jacobian `J` on the orientation-preserving branch. The complete coframe and the
complete query realization both enter `J`; no angular or mixing block is discarded.

Let the fixed source-label measure be

```text
nu_0=C(s,y) ds wedge dy1 wedge dy2.
```

For the unweighted observer query, the metric-calibrated source clock and oriented local sky supply
`ds wedge dOmega_s`. More general `C(s,y)` records a supplied weighting. The defining fact about a
label is only

```text
partial_lambda C=0.
```

There is a unique three-form `N_C` on the regular image of `R` whose pullback is `nu_0`. Equivalently,

```text
j_C=(C/J)K,
N_C=i_(j_C) vol_g,
R^*(N_C)=C ds wedge dy1 wedge dy2.                       (1)
```

Taking the exterior derivative gives

```text
R^*(dN_C)
 = (partial_lambda C)
   dlambda wedge ds wedge dy1 wedge dy2
 =0.                                                     (2)
```

Therefore `N_C` is exactly closed. Its pullback to a coordinate side surface of fixed sky label
vanishes by construction, while its integral on any two transverse endpoint sections is the same.
This does not prove zero side flux for a physical carrier. In vector language,

```text
div_g[(C/J)K]=(1/J)partial_lambda C=0.                   (3)
```

Equations (1)--(3) are a conditional query-label bookkeeping theorem. Closure follows because
pullback and exterior differentiation commute and the supplied label form is constant along its
propagation coordinate. The metric is load-bearing for `vol_g`, `J`, and the density/vector
representation, but closure itself is already encoded in query typing. The theorem does not say
what physical substance, if any, `C` counts.

## 3. Screen/Jacobi form of the same theorem

Let the orientation-preserving screen Jacobi map be an invertible `2x2` matrix `D(lambda)`, and set

```text
B=D' D^-1,
theta=tr B,
A=det D>0.
```

Exact matrix differentiation gives

```text
A'/A=tr(D'D^-1)=theta.                                  (4)
```

For any first-integral label weight `C`, define the geometric label density per physical screen
area by

```text
n=C/A.
```

Then

```text
n'+theta n=0,
n A=C.                                                   (5)
```

Thus the inverse-area law is not an added optical correction. It is the local density of the
conserved query-label measure inside the complete Jacobi map. Every angular and mixing effect that
changes `D` changes `A` and `n` together, leaving the label amount `nA` fixed.

Under a source-screen relabelling, both the coordinate area density `A` and label density `C`
acquire the same Jacobian factor. Their ratio `n=C/A` is invariant. The result is therefore not an
artifact of the label coordinates.

The van Vleck/geodesic-spreading density is the same regular focusing information in a different
presentation. It introduces no physical population and fails or branches at the same focal/cut
strata excluded here.

## 4. Why this does not yet set physical `eta=1`

The query automatically carries its labels because the labels were defined to remain constant
along `K`. Therefore

```text
eta_label=1.                                             (6)
```

But G94's `eta` is the survival fraction of a physical radiative amount. Replacing it by (6) requires
the additional type identification

```text
physical radiative count or wave-action measure
  = supplied source amount attached to N_C.              (7)
```

Equation (7), together with physical zero side flux, says that physical cargo follows the query
transport without absorption, scattering, branch exchange, creation, or loss. That is exactly the
transparent carrier premise the prior audits left open. The geometry supplies the density and
focusing representation of the bookkeeping map; it does not state that Nature's radiative cargo is
represented by it.

There is also an infinite family of geometric label measures: multiplying the source label form by
any nonzero `C(s,y)` gives another closed current. Once a particular source label measure is supplied,
its pushforward is unique, but the metric does not select the source's physical angular/time
population or normalization.

Consequently the sharp conditional statement is

```text
physical carrier identified with N_C  => eta=1
```

on the declared regular transparent branch. It is not an unconditional metric theorem.

Together with G95's separate conditional identification

```text
p=C_p k_flat,
E_u=-p(u),
```

one compact null-carrier premise could give both `eta=1` and `epsilon=1/Z`. Neither identification
is adopted here.

## 5. Competing spacetime three-forms

The positive label-current result does not arise because every natural-looking coframe form is
closed.

### Metric volume

The four-form `vol_g` is parallel and `d vol_g=0` by top degree. It is not a three-current and has no
three-surface flux until a vector/density is supplied.

### Raw coframe triples

The complete coframe supplies many triples, none selected as cargo. They are not generally closed.
For the regular coframe

```text
theta0=dt,
theta1=dx,
theta2=(1+x)dy,
theta3=dz,
```

the triple `theta0 wedge theta2 wedge theta3` has nonzero derivative proportional to
`dx wedge dt wedge dy wedge dz`.

### Null dual

For any vector `K`,

```text
d(*K_flat)=(div K)vol_g.
```

The outgoing affine null congruence `K=partial_t+partial_r` in flat spherical coordinates has
`div K=2/r`, so its raw metric-dual three-form is not closed. The compensating inverse-Jacobian
density in (1) is essential.

### Reciprocal gradient

Conditionally treating `phi` as a spacetime scalar gives

```text
d(*dphi)=(box phi)vol_g.
```

Closure is a field equation, not an identity. The flat witness `phi=t^2` has `box phi=-2`.

## 6. Null phase space and projectivization

On `T*M`, the metric Hamiltonian

```text
H=(1/2)g^ab p_a p_b
```

and the canonical symplectic form provide a preserved Gelfand–Leray measure on the regular future
null shell `H=0`, excluding zero momentum. This is a real metric-derived transport arena.

It still does not select a populated distribution. Locally every initial function on a transverse
phase-space section has a transported solution of `X_H f=0`; `f=0` and every constant are simple
members. A flat catch gives `X_H(x0)=-p0`, proving that arbitrary functions are not automatically
transported.

Null momentum also has a positive scaling freedom. Under `p -> a p` in four dimensions,

```text
d4p -> a^4 d4p,
delta(H) -> a^-2 delta(H),
mu_null -> a^2 mu_null.                                  (8)
```

Thus the shell measure is not basic under projectivization. Removing momentum magnitude retains a
canonical ray/contact-type structure but not a normalized carrier measure. An observer-frequency
section or another scale choice is needed, and it still does not populate the rays.

## 7. Response and topological candidates

The conditional screen `SO(2)` response of G95 remains correctly typed:

```text
F=dA,
J3=d(*F),
dJ3=0.
```

It is a defined geometric response, not the query-label current. On the proposed source-free branch
`J3=0`, so it cannot represent a nonzero carried count.

The Abelian Chern–Simons form is not a replacement:

```text
d(A wedge F)=F wedge F.
```

For `A=t dx+y dz`, `F wedge F=2 vol_4`, so it is not generally closed. It is also gauge-dependent as
a local form up to an exact term and is not intrinsically null-directed.

Special Killing, Bianchi, Kodama-like, or topological currents can exist on restricted branches.
Their conservation and energy interpretation require their branch/symmetry data and do not identify
them with the general G94 null-query cargo.

## 8. Ownership classification

The thirteen preregistered homes yield three distinct kinds of object:

1. **metric identities/structures:** volume, null-shell measure, Hamiltonian flow, and conditional
   response compatibility;
2. **query-derived kinematic transport:** the exact closed label current `N_C`, with its
   metric-derived inverse-Jacobi density and equivalent van Vleck spreading;
3. **physical cargo:** still open because no active premise identifies a material/radiative amount
   with either geometric class.

The complete coframe influences the detailed Jacobian and focusing but does not select the physical
population. No candidate was rejected for failing to look like light, and no desired transfer law
was inserted into an acceptance test.

## 9. Scope and completeness

This result covers one supplied local regular null-query tube and its complete metric/Jacobi
response. It drops physical history/query selection; caustics, cut/focal points, multiple images,
and branch aggregation; absorption, scattering, creation, detector response, and side exchange;
source population, luminosity, anisotropy, spectrum, and normalization; action, constitutive law,
source dynamics, matter, and boundary completion; and `X_max`, SNe fitting, BAO/CMB interpretation,
bootstrap, mass, and signalling.

Any dropped sector can change physical survival. This is one local ownership tile, not a complete
radiative theory.
