# Exact derivation — native radiative-current and energy-readout ownership

Date: 2026-08-15

## 1. Result first

The complete UDT metric supplies a genuine **Maxwell-shaped geometric response complex** after an
oriented Abelian connection has been supplied or conditionally derived:

```text
mathcal A  ->  mathcal F=d mathcal A  ->  mathcal H=*mathcal F
           ->  mathcal J=d mathcal H,

d mathcal F=0,
d mathcal J=0.
```

The two conservation-looking equations are exterior-calculus identities. They do not select the
source-free equation `d(*mathcal F)=0`, an action, a physical carrier, or a radiative normalization.

The metric also supplies canonical null Hamiltonian flow and its phase-volume preservation. It does
not supply a populated distribution or the collisionless transport equation for that distribution.

Consequently neither open G94 factor is metric-owned without a carrier statement:

```text
eta     remains OPEN,
epsilon remains OPEN as physical ownership.
```

There is, however, a sharp conditional theorem: once one physical carried covector `p` is identified
with a constant multiple of the query's affinely transported null covector, the endpoint energy
readout `E_u=-p(u)` gives `epsilon=1/Z` exactly; the unknown normalization cancels. A Planck-scale
anchor is not needed for this ratio.

The landing is therefore

```text
GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY
__PHYSICAL_TRANSFER_OPEN
__ONE_CARRIER_COVECTOR_PREMISE_GIVES_EPSILON_EQUALS_ONE_OVER_Z
__CLOSED_CARRIER_MEASURE_STILL_NEEDED_FOR_ETA_EQUALS_ONE
```

## 2. Where an Abelian connection can come from

Let `(M,g)` be one supplied oriented Lorentzian four-geometry.

The full Levi-Civita connection is `so(1,3)`-valued. Its Cartan curvature and covariant Bianchi
identity are metric-derived, but no real one-dimensional component is invariantly selected by a
generic Lorentz metric. Projecting one component by hand would be an imported generator choice.

Three conditional reductions are already present in the UDT record:

1. a supplied oriented `2+2` reduction over a four-dimensional region gives an oriented screen
   `SO(2)` connection;
2. a supplied pair immersion gives an `SO(2)` normal connection over its two-dimensional pair
   surface;
3. the conditional toric/Hopf branch gives a principal-circle connection on that completion.

These objects have different bases. The pair-surface normal curvature is a two-form on `Sigma`, not
a spacetime two-form, and cannot silently become a four-dimensional radiative field. The toric
connection likewise becomes a spacetime object only after its branch and time extension are
supplied.

For a four-dimensional oriented screen reduction, choose a local oriented orthonormal screen frame
`(e_2,e_3)` and set

```text
mathcal A(X)=g(e_2,nabla_X e_3).
```

Under a local screen rotation by `lambda`,

```text
mathcal A -> mathcal A+d lambda,
mathcal F=d mathcal A -> mathcal F.
```

Thus `mathcal F` is a well-typed curvature two-form on the supplied reduction. Through the Ricci
equation it contains ambient curvature and the commutator of the off-diagonal/extrinsic connection
blocks. In UDT language, the angular sector and mixing orchestra are inside this curvature; they are
not appended after it.

The founding reciprocal presentation alone does not provide a nontrivial alternative. Its local
Abelian scale connection is proportional to `d phi`, whose curvature is `d(d phi)=0` wherever the
presentation is smooth. Nonzero curvature requires angular/mixing/global structure.

## 3. The exact Maxwell-shaped form complex

On any one supplied Abelian reduction, let

```text
mathcal F=d mathcal A.
```

Then

```text
d mathcal F=d^2 mathcal A=0.                              (1)
```

The metric and orientation supply the Hodge star. For the simplest metric constitutive readout,

```text
mathcal H=kappa * mathcal F,
mathcal J=d mathcal H,                                    (2)
```

where even the nonzero normalization `kappa` is not fixed by the metric. Equations (1)--(2) imply

```text
d mathcal J=d^2 mathcal H=0.                              (3)
```

Equation (3) says that the **defined geometric response** is consistent. It is not an independent
inhomogeneous field equation because `mathcal J` was constructed from `mathcal F`. If instead a
physical source three-form is supplied independently, `d mathcal H=mathcal J_phys` becomes an
equation and (3) becomes its compatibility condition.

Nor does the metric force the vacuum equation

```text
d(*mathcal F)=0.                                          (4)
```

The exact catch witness in the primary and independent implementations is

```text
mathcal A=t^2 dx,
mathcal F=2t dt wedge dx,
*mathcal F=-2t dy wedge dz,
d(*mathcal F)=-2 dt wedge dy wedge dz != 0.
```

It obeys `d mathcal F=0` and `d[d(*mathcal F)]=0` exactly while violating (4). Therefore neither
Cartan compatibility nor exterior nilpotence selects the source-free branch.

The choice `mathcal H=*mathcal F` is itself only the simplest constitutive candidate. Scaling it
changes the response normalization, and more general local constitutive maps can be built once
additional invariants or scales are admitted. “Choose the simplest” would be a minimality premise,
not a metric derivation.

## 4. Why the closed response is not `eta=1`

A physical carried amount would be represented by a three-form `mathcal N` whose integral over a
beam cross-section/world-tube cut counts the same cargo used in G94. If

```text
d mathcal N=0
```

and the beam tube has zero side flux, Stokes' theorem gives equal endpoint fluxes and hence
`eta=1` on that regular branch.

The geometric response `mathcal J=d(*mathcal F)` cannot simply be renamed `mathcal N`:

- it is a source/response current associated with the chosen connection;
- on the proposed source-free branch it vanishes, so it carries no nonzero radiative count;
- its normalization and physical units are unowned;
- pair-normal holonomy may live on `Sigma` rather than on spacetime;
- no current premise identifies its integral with emitted or received luminosity cargo.

A quadratic field stress does not repair the problem. Its normalization and divergence law depend
on a constitutive/action choice and the field equation. A Bianchi/Killing current can be conserved
on special stationary branches, but it is likewise not the null carried amount of the G94 query.

Thus the smallest missing object for `eta=1` is not “some conserved current.” It is a **physically
identified closed null-carrier measure** on the same query, with its side-flux and branch rules.

## 5. Canonical null phase-space flow

The metric does provide a more general transport arena without Maxwell. On `T*M`, use the canonical
symplectic form and the metric Hamiltonian

```text
H(x,p)=(1/2) g^ab(x) p_a p_b.
```

Its Hamiltonian vector field is

```text
X_H
 = g^ab p_b partial_(x^a)
   -(1/2)(partial_a g^bc)p_b p_c partial_(p_a).
```

Hamiltonian flow preserves the canonical symplectic/Liouville volume exactly. The symbolic proof
reduces its phase-space divergence to equality of mixed partial derivatives; an independent exact
polynomial implementation reproduces zero.

But a physical population is a distribution `f(x,p)`. Its conservation requires

```text
X_H f=0                                                    (5)
```

plus initial data and collision/absorption rules. Equation (5) is not true for an arbitrary `f`.
The catch witness `f=x^0` on flat phase space gives `X_H f=-p_0`, nonzero. The metric supplies the
flow and preserved empty measure; it does not populate that flow with radiative cargo or impose
collisionless evolution.

Therefore Liouville geometry does not by itself set `eta=1`. It provides the cleanest mathematical
home for a future carrier law.

## 6. The endpoint energy ratio

Suppose one physical carried unit has a covector

```text
p=C k_flat,
```

where `k` is the same affinely transported null query tangent and `C>0` is constant along that unit.
For an endpoint observer `u`, define the measured carried energy by the metric pairing

```text
E_u=-p(u)=C[-g(k,u)]=C omega_u.
```

Then

```text
epsilon
 = E_o/E_s
 = omega_o/omega_s
 = 1/Z.                                                   (6)
```

The unknown `C` cancels. Thus neither an absolute quantum nor `hbar` is required for the ratio.
What remains unowned is the type identification: the query's geometric null tangent/frequency must
also be the covector and energy readout of the physical carried unit. Co-presence and metric causal
accessibility do not presently supply that material identification.

Equation (6) is therefore a one-premise conditional theorem, not a present metric-only result.

## 7. Relation to a full Maxwell theory

A full Maxwell-like dynamics would require, at minimum:

1. a physically selected oriented Abelian reduction/connection;
2. a constitutive relation and its normalization;
3. an independent source or a source-free selection rule;
4. a variation/evolution domain and boundary data;
5. a physical stress/energy and radiative carrier identification.

The complete UDT coframe supplies candidate geometry for item 1 on conditional branches and the
Hodge machinery used in item 2. It does not yet own the remaining selection chain. Adding the
standard `F^2` action would close much of it, but that would currently be an ansatz/import, not a
derivation from the two founding postulates.

For the narrower SNe propagation problem, a full field theory is unnecessary. One transparent
null-carrier premise could supply both missing factors:

```text
physical carried covectors follow the canonical null Hamiltonian flow,
their populated measure is collisionlessly conserved on the declared regular branch,
and endpoint energy is -p(u).
```

That premise would give `eta=1` and `epsilon=1/Z`; it is not adopted by this audit.

## 8. Solution-space and scope audit

The candidate atlas retains:

- trivial reciprocal curvature;
- non-Abelian Cartan curvature;
- conditional four-dimensional screen curvature;
- pair-surface normal curvature with its distinct base type;
- conditional toric/Hopf curvature;
- nonzero and source-free Hodge-response branches;
- empty and populated null phase-space flows;
- conditional covector energy readouts;
- special stationary Bianchi/Killing currents.

No candidate was discarded for failing to resemble electromagnetism. The negative ownership result
is premise-scoped: a future physical reduction, action, global completion, or carrier law can change
it and must trigger regrading.

This is a local regular-branch result. It does not cover caustics, multiple images, absorption,
scattering, topology-changing reductions, detector response, source luminosity, global completion,
or a selected metric history.

