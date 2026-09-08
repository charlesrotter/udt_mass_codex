# Native Hopfion Topology Audit — Report

Date: 2026-07-19
Base: `28628be883dd37b0982dfb8ceeb41e46f1aa0d9b`
Preregistration commit: `737c05d`
Mode: CPU-only, metric-led, no research-artifact mutation

## Result

`EXISTING_3D_HOPFION_NOT_MISSED__HOPF_STRUCTURE_CARRIER_CONDITIONAL__METRIC_NULL_S2_FIBER_CONDITIONAL__SECTION_AND_BOUNDARY_SELECTOR_OPEN`

The zoom-out was scientifically useful, but the current particle program did not overlook the
three-dimensional Hopfion. The July 5 H3 object and the later corrected no-null carrier are already
explicit full-3D Faddeev-Skyrme Hopfions: a unit three-vector field on a Cartesian `N x N x N` grid,
a degree-one Hopf seed, a toroidal seed, and a Whitehead/Hopf charge implementation. The corrected
energy retains all three spatial derivatives and removes a numerical Nyquist null without changing
the continuum `L2+L4` functional.

The unresolved issue is one level upstream. Exact C0/C1 does not derive the `S2` carrier. It supplies
the round-`S2`, static `E2+E4` branch only as a reopened historical `WORKING / POSIT / CONDITIONAL`
test branch. Thus the repository has genuinely studied and stabilized a 3D Hopfion, but it has not
shown why the UDT metric must carry that Hopfion field.

## What was actually modeled

The original H3 implementation is not a radial Skyrmion:

- `fs_hopfion.py` constructs `X,Y,Z` with a three-dimensional meshgrid and stores
  `n` with shape `3 x N x N x N`;
- `hopf_seed` explicitly performs inverse stereographic `R3 -> S3` followed by the Hopf map
  `S3 -> S2`;
- `toroidal_seed` carries the `(m,l)=(1,1)` toroidal winding;
- `hopf_charge` computes the Whitehead integral from all three pullback components;
- `noNull_energy.py` uses all eight forward/backward orientations in three spatial dimensions;
- `noNull_resolve.py` retains the three-dimensional field and independently evaluates forward and
  orientation-averaged Hopf charges.

The distinction matters. The retired imported object was an `S3 -> S3` Skyrme hedgehog with degree
in `pi3(S3)`. The current object is an `S3 -> S2` Hopf texture with linking charge in `pi3(S2)`.
The repository's solver-integrity guard correctly rejects the former. Some historical test comments
still call the latter “native,” but the July 15 owner clarification and exact C1 prospectively
supersede that wording: the carrier is reopened and conditional.

The banked H3 record reports a localized torus with `|Q|` rising from about `0.985` to `0.992` across
the resolution ladder. The later no-null arc establishes static finite-box stability within the
round-`S2`, `L2+L4`, fixed-boundary, discretization, and operator premises. This audit does not
freshly replay the saved field charge: the large H3/no-null field checkpoints are not tracked in the
clean checkout. It therefore retains the numerical configuration as `OBSERVED_CARRIER_CONDITIONAL`
from banked evidence, not as a newly reproduced raw-field result.

## Exact topology findings

The CPU/SymPy script `derive_topology.py` independently checks:

1. The standard Hopf map built from an `S3` spinor lands exactly on `S2`.
2. In Hopf coordinates, the connection
   `A = cos(eta)^2 d(xi1) + sin(eta)^2 d(xi2)` gives
   `integral(A wedge dA) = -4*pi^2`, hence the registered convention gives `Q_H=1`.
3. A radial `S2` hedgehog has primary flux `4*pi`; it is not the zero-primary-flux localized Hopf
   texture and cannot be substituted for one.
4. A normalized scalar gradient, where defined, satisfies the Frobenius restriction
   `n-flat wedge d(n-flat)=0`; it is not a generic `S2` carrier and becomes undefined at gradient
   zeros.

These are topology controls. They do not derive the carrier, energy, boundary data, or stability.

## The hidden-in-plain-sight metric structure

There is a narrower conceptual lead that the prior carrier provenance audit did not state in this
form. Once the conditional four-dimensional Lorentzian/conformal readout is accepted, every tangent
space has a projective null-line cone:

```text
k = omega (e0 + n),  omega > 0,
g(k,k)=0  iff  |n|=1.
```

Quotienting the nonzero line scale leaves an `S2` of null directions. If a time orientation is
separately `CHOSE`, the positive rays in its future component are likewise an `S2`. A positive
Common-Scale rescaling multiplies `g(k,k)` but does not change which lines are null, so this `S2`
fiber is naturally compatible with CSN. The executable matrix calculation is an exact consistency
check of that conformal fact, not independent evidence for the physical premises. In lay terms, the
metric supplies a sphere of possible light/causal directions at every event.

This is promising for the light/time/co-presence framing, but it is not yet a carrier derivation:

- four-dimensionality is currently `INHERITED`, not derived by C0/C1;
- the local Lorentzian readout is `POSIT / CHOSE` after representative selection;
- this is a celestial topological/conformal `S2`, not automatically the carrier's fixed round-`S2`
  target metric;
- a sphere fiber is not a chosen field: UDT still needs a section selecting one direction at each
  event;
- turning a section over a spatial slice into a map `S3 -> S2` needs a frame/trivialization, or an
  intrinsic bundle-level Hopf construction; comparing directions between events likewise needs a
  connection or intrinsic transport law;
- current Reciprocity/CSN does not select a unique line, as the reciprocal-line audit already shows;
- no `L2+L4` action, time sector, source, or boundary rule follows merely from the null sphere.

Accordingly the strongest honest new bridge candidate is:

`WORKING_CANDIDATE: the reopened S2 carrier may be a section/texture of the conformally natural null-direction sphere bundle.`

This is not UDT-unique yet. Every four-dimensional Lorentzian conformal geometry has the same local
null-direction sphere. UDT would become distinctive only if Reciprocity, finite-cell structure, or
bootstrap closure selected the section, its comparison law, and its admissible topology.

## Boundary and co-presence audit

Given the conditional carrier, a constant-exterior configuration supported in a contractible bulk
cube or ball defines

```text
B3 / boundary(B3) = S3,
S3 -> S2,
Q_H in Z.
```

This makes the local Hopf sector mathematically legitimate without requiring the entire universe to
have global topology `S3`. It remains conditional on a constant exterior and a fixed boundary class.
Exact C1 fixes the static `phi` parity at the finite-cell seal but explicitly leaves boundary data for
every other field open. The H3/no-null pinned layers are solver boundary data, not a derived physical
finite-cell carrier completion; the later boundary-virial audit also finds a non-negligible pinned-wall
skin. Therefore no global or time-live topological-conservation theorem has been established.

Co-presence changes the interpretation, not this mathematical gate. A complete spacetime Hopf world
history could be one whole-solution object, but persistence across slices still requires a time-live
field law and boundary completion. Co-presence alone does not prevent unwinding, boundary escape, or
singular topology change.

## Mechanical adjudication

| Arm | Ruling | Reason |
|---|---|---|
| Metric/foundation-native | `UNAVAILABLE_FROM_REGISTERED_FOUNDATION` | C0/C1 has no selected `S2`-valued field, section, action, or carrier boundary. |
| Metric null-direction fiber | `CONDITIONAL_DERIVED_FIBER` | The projectivized null cone is `S2` and CSN-invariant after the inherited/conditional 4D Lorentzian readout. |
| Existing carrier | `CARRIER_CONDITIONAL_HOPF_SECTOR_AVAILABLE` | The reopened round-`S2` branch plus constant exterior defines `S3 -> S2`. |
| Existing representation | `FULL_3D_HOPF_CAPABLE` | The active H3/no-null code is genuinely three-dimensional and directly measures Hopf charge. |
| Existing configuration | `OBSERVED_CARRIER_CONDITIONAL` | Banked `Q approximately 1` toroidal evidence exists; raw fields were not freshly replayed here. |
| Static stability | `SETTLED_STATIC_FINITE_BOX_CONDITIONAL` | Current frontier result survives with all carrier/box/operator premise stamps. |
| Global/time-live persistence | `OPEN` | Native carrier section, physical boundary, time sector, and propagation/topology theorem are absent. |

The detailed twelve-row result is `TOPOLOGY_STATUS_LEDGER.tsv`. `SOURCE_INVENTORY.tsv` is the curated
load-bearing source set. `CANDIDATE_CENSUS.tsv` separately records the complete preregistered
filename/text discovery universe and every exclusion/supporting disposition.

## Smallest genuinely missing selector

The next conceptual question is not whether Faddeev-Skyrme mathematics supports a Hopfion; that has
already been answered in the conditional branch. It is:

> Does UDT select a conformally natural section or texture of its null-direction sphere bundle, with
> a finite-cell boundary/framing rule, without positing an independent carrier?

A future audit should first test that question at the kinematic/bundle level. It should fail closed
if the section, connection, or boundary is chosen merely to reproduce the existing Hopfion. Only if
the section is selected natively would it be appropriate to ask whether the existing `L2+L4`
functional descends from the metric or bootstrap.

## What is not claimed

- No native carrier or Hopfion has been derived from C0/C1.
- No new action, coupling, source, or boundary condition was introduced.
- No raw saved particle field was opened or recomputed.
- No time-live stability, topology-propagation, mass, or cosmology result follows.
- No canonization, GPU work, repository reorganization, or navigation update was performed.

## Four evidence gates

1. Preregistered: yes, commit `737c05d` before candidate-content inspection.
2. Scope: bounded topology/provenance census; it does not claim full field/action completeness.
3. Verification: `VERIFICATION_RESULT.json` is a self-consistency/regression verifier that reruns the
   exact algebra and exercises mutation catches. Fresh external adversarial verification is recorded
   separately in `EXTERNAL_ADVERSARIAL_REVIEW.md`; it is the independent semantic gate.
4. Premises: recorded in `PREREGISTRATION.md`, `SOURCE_INVENTORY.tsv`, and
   `TOPOLOGY_STATUS_LEDGER.tsv`.
