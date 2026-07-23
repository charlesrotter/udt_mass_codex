# Metric-pure frame rederivation

Date: 2026-07-23

Preregistration commit: `5b74105`

Compute: CPU-only exact algebra

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's proposed regrade is correct:

> WR-L is not the complete UDT metric. It is a one-function,
> static, spherical, diagonal, areal, zero-shift reduction that did not
> retain complete frame-based reciprocity.

The recorded complete parent is not one privileged coordinate formula.
It is the four-dimensional conformal-Lorentzian metric/coframe
configuration class. A conditional `2+2` chart exposes ten metric slots,
all potentially dependent on all four coordinates:

```text
3 base + 3 screen + 4 base/screen shifts.
```

WR-L reduces those ten slots to one independent function `A(r)`, fixes the
round areal screen, removes every mixed shift, removes time and nontrivial
angular dependence, and then conditionally selects
`A=1-r/X`.

The profile and its observational readouts survive in that exact scope.
They do not define the complete frame-reciprocal theory.

## 1. What the metric alone says about observers

At one event, choose any representative of the positive common-scale
class and use the calibrated clock unit. Future unit timelike directions
form a hyperboloid. The connected local Lorentz group acts transitively
on it.

There is no nonzero vector fixed by the full group. The exact verifier
uses three rational boosts,

```text
cosh(chi)=5/4,
sinh(chi)=3/4,
```

along three independent spatial directions. The stacked fixed-vector
system has rank four and only the zero solution. Zero is not an observer.

Therefore the zero-jet Lorentzian metric does not select a preferred
local observer direction.

This is a local kinematic theorem, not a global homogeneity theorem.
Curvature, `dphi`, boundary data, or a selected complete solution can
conditionally distinguish directions. The current parent configuration
does not universally select one.

## 2. Pairwise frame reciprocity is metric-derived

For two supplied future unit timelike directions `u` and `v`,

```text
gamma(u,v) = -g(u,v)/c_E^2
```

after calibrated normalization. The metric symmetry makes this scalar
symmetric. Each observer assigns the same relative rapidity and speed
magnitude, with the spatial direction reversed in the reciprocal rest
frame.

For a standard exact representative,

```text
v = gamma (u + beta n),
g(u,n)=0,
g(n,n)=1.
```

Both null directions remain null. Under positive CSN rescaling, observers
renormalize by the same local factor and `gamma` is unchanged. Thus:

- causal cones and pairwise local frame reciprocity are pre-scale
  conformal structure;
- measured `c_E` calibrates the post-scale clock/length units;
- no global observer-centered universe follows from this local theorem.

This derivation uses the Lorentzian metric itself. It does not import an
Einstein equation, EH action, or GR observer dynamics.

## 3. The angular sector enters full frame reciprocity automatically

The one-dimensional reciprocal subgroup is exact:

```text
B_x(chi1) B_x(chi2) = B_x(chi1+chi2).
```

This is the additive structure that resembles the historical scalar
reciprocal-depth law. But it is only the collinear subgroup.

Two non-collinear metric-preserving frame changes do not commute. For the
exact rational `x` and `y` boosts above,

```text
B_x B_y != B_y B_x.
```

Their product sends the original observer to

```text
v = (25/16, 15/16, 3/4, 0).
```

After factoring out the unique boost to that new observer direction, the
remaining transformation is

```text
R =
[[1, 0,     0,    0],
 [0, 40/41, 9/41, 0],
 [0,-9/41, 40/41, 0],
 [0, 0,     0,    1]].
```

It fixes the observer and rotates the transverse spatial screen.

This is a substantial metric-pure result:

> Complete frame reciprocity is nonabelian, and non-collinear observer
> composition necessarily has angular content.

It is not curvature, a force, a Hopf carrier, or matter emergence. It is
local frame-group geometry. But it shows why the angular sector cannot be
held passive while a single radial `phi` shift is asked to represent all
observers.

The local UDT field `phi` is not thereby identified with observer
rapidity. The collinear algebra is compatible; the physical join remains
open.

## 4. Exactly what WR-L froze

In the conditional `2+2` chart, WR-L assigns

```text
h00 = -A(r)c_E^2,
h01 = 0,
h11 = 1/A(r),

q22 = r^2,
q23 = 0,
q33 = r^2 sin^2(theta),

A2_0 = A3_0 = A2_1 = A3_1 = 0.
```

This retains one independent function from ten metric components:

- the two base diagonal components are tied reciprocally;
- the base shift is removed;
- screen area, round shape, and eigendirections are fixed;
- all four base/screen shifts are removed;
- the base/screen split is selected;
- dependence is reduced from all four coordinates to `r` only;
- a spherical areal center is introduced.

WR-L is therefore a legitimate adapted slice, not a complete
configuration space.

## 5. The WR-L slice is not closed under generic observer-adapted changes

Use the dimensionless clock coordinate `x0=c_E t` and mix the base
coordinates by a constant parameter `b`. The pullback of

```text
diag(-A,1/A)
```

has cross component

```text
g_TR = gamma^2 b (1/A-A).
```

At the exact witness

```text
A=1/2, b=3/5, gamma=5/4,
```

it is

```text
g_TR=45/32.
```

Because the old radial coordinate also mixes with the new time
coordinate, `A(r)` becomes time dependent. The same tensor geometry has
left the static diagonal WR-L chart and activated precisely the shift and
time sectors that the complete metric ledger kept live.

At `A=1`, the cross term vanishes. This explains why the restricted ansatz
can overlap the ordinary flat/terrestrial anchor while failing as a
complete global frame construction away from that regime.

A local internal Lorentz coframe change still preserves the metric
exactly. That is a basis-gauge statement, not a global recentering of the
WR-L spherical chart.

## 6. WR-L results that survive

The following remain valid with their previous premise stamps:

- the reciprocal simple-metric base relation;
- the conditional WR-L profile `A=1-r/X`;
- the clock factor tending to zero at `X`;
- infinite optical depth at `X`;
- the observed Pantheon comparison of that supplied profile.

The following are not supplied by WR-L:

- the complete UDT metric;
- complete frame reciprocity;
- global recentering of all observer charts;
- a common physical or numerical `Xmax`;
- native invariant mass;
- complete boundary topology;
- angular shape, twist, transport, or dynamics.

The July 9 center audit had already identified the compatible alternative:
WR-L may be a residual pair-space/off-diagonal appearance chart rather
than one global center-included spacetime. That was a `WORKING` lead, not
canon. The present derivation recovers the same fork from the later
complete-metric ledger rather than inventing a new ontology.

## 7. Acceleration

A chosen accelerated timelike field can have nonzero

```text
a = nabla_u u
```

even in the unchanged flat metric. The exact control has

```text
g(u,u)=-1,
g(u,a)=0,
g(a,a)=a0^2,
```

while the metric and its null cone remain fixed.

Therefore:

- acceleration changes an observer's adapted frame and connection
  components;
- acceleration alone does not change the invariant metric or cone;
- a UDT law by which acceleration causes a physical metric response
  remains open;
- no GR gravity–acceleration equivalence is imported.

## Four evidence gates

1. **Preregistered:** yes, commit `5b74105`.
2. **Full or bounded:** exact for local Lorentzian observer geometry, the
   conditional ten-slot `2+2` census, and the WR-L reduction. It is not a
   global solution or dynamics audit.
3. **Independent:** required before banking; production currently records
   69 exact checks.
4. **Premises audited:** yes. CSN, `c_E`, time orientation, `phi`, split,
   curvature selection, WR-L, acceleration, `Xmax`, action, and source
   are separately stamped.

## Maximum conclusion

> The metric-pure parent is the four-dimensional
> conformal-Lorentzian metric/coframe class, not WR-L. It derives no
> preferred zero-jet observer and exact local full-frame reciprocity with
> a common cone. Non-collinear composition necessarily rotates the
> transverse screen. It does not derive global observer recentering.
> WR-L is a one-function adapted reduction whose profile, asymptote, and
> SNe readout survive only in that scope. Physical
> acceleration-induced metric warping remains open.

No canonization, navigation edit, action, source, carrier, mass closure,
new frame law, GPU work, or repository reorganization is performed.
