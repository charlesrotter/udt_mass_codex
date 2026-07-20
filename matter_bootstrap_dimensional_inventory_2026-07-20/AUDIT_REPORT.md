# Matter/Bootstrap Dimensional-Inventory Audit

Date: 2026-07-20
Base: `ab099c9c642d68049cfc4810fd709df638ce591c`
Mode: CPU-only exact scaling and provenance audit

## Result

The existing stable-soliton branch contains a hidden **conditional coefficient ruler**, not a
UDT-native dimensional matter object.

For the exact continuum functional implemented by `noNull_energy.py`, write a scaled three-dimensional
shape as `n_R(x)=n_1(x/R)`. With positive dimensionless shape integrals `A` and `B`,

```text
E(R) = xi A R + kappa B/R,
R_star = sqrt(kappa/xi) sqrt(B/A),
E_star = 2 sqrt(xi kappa A B).
```

Thus the finite stationary size is not fixed by Hopf topology alone. Its dimensional ruler is

```text
ell_coeff = sqrt(kappa/xi).
```

The active and historical production paths expose `xi` and `kappa`; their standard branch uses
`xi=kappa=1`. That assignment absorbs `ell_coeff=1` and `sqrt(xi*kappa)=1` into code units. It does
not derive either physical unit from the UDT metric.

Grade: **VERIFIED-WITH-CAVEATS**. The result was preregistered, the complete bounded tracked
provenance closure was frozen, and the load-bearing algebra and source syntax were independently
replayed. No fresh external-model review was authorized, and this is not the complete UDT matter
solution space.

## Exact dimensional statement

If `E` has physical energy dimensions and `n` is dimensionless, then

| Object | Dimensions |
|---|---|
| `xi` | energy/length = force |
| `kappa` | energy times length |
| `kappa/xi` | length squared |
| `sqrt(xi*kappa)` | energy |

The observational anchors can dimensionally normalize the first coefficient as

```text
xi = (c_E^4/G_obs) f2,
```

where `f2` is dimensionless. They cannot normalize the second coefficient without a length:

```text
kappa = (c_E^4/G_obs) ell_0^2 f4.
```

Consequently,

```text
R_star = ell_0 sqrt(f4 B/(f2 A)),
M_star = E_star/c_E^2
       = 2 (c_E^2/G_obs) ell_0 sqrt(f2 f4 A B).
```

The same missing `ell_0` sets both radius and mass. The particle branch therefore reproduces the
previous global rank result: `c_E` and `G_obs` calibrate mass per length, while one absolute ruler
remains to be selected.

## What the source audit established

The preregistered base-tree census contains 3,924 tracked text records. Forty-one load-bearing
sources were individually adjudicated.

- `noNull_energy.py` states the unchanged continuum `L2+L4` functional with coefficients `xi/2` and
  `kappa/4`; its demonstration sets both to `1.0`.
- The relaxation, Hessian, virial, mass, and behavioral paths load or preserve `L`, `h`, `xi`, and
  `kappa`; they do not derive them from the metric.
- The box scout explicitly requires the source branch `L=6`, `xi=1`, `kappa=1` and enlarges only the
  computational domain at fixed spacing.
- The fixed-charge experiments supply `Q` and use unit coefficient/time normalizations. Their
  inertia scales as `xi C2 R^3 + kappa C4 R`, which factorizes with the same `ell_coeff`; it supplies
  no independent ruler or clock.
- The current topology audit makes `Q_H` dimensionless and keeps the carrier conditional.
- The phase-G code explicitly calls its result an EH/weak-field unit-response readout, uses no
  `kappa_g` value, and calls the carrier boundary a solver boundary rather than a physical wall.
- The virial identity requires a controlled isolated boundary limit before conditional carrier
  energy can equal the conditional mass readout.

No current post-firewall source derives a nonzero dimensional coefficient from the UDT metric before
the carrier/action/domain/readout choices are supplied.

## Topology, stability, and the box

These objects answer different questions:

- Hopf charge can distinguish topological sectors but has scale weight zero.
- The `E2/E4` balance explains why a finite stationary size exists once the coefficient ruler is
  supplied.
- The finite-grid Hessian and behavioral evidence test whether that chosen branch is locally stable
  in its recorded box.
- `L`, `h`, `N`, and `HBW` are numerical/domain controls. The box can distort or exclude a solution,
  but it is not the physical origin of `ell_coeff`.

Therefore the existing stability result remains valid within its exact premises. It is reinterpreted
as stability **in a supplied unit system**, not as derivation of that unit system.

## Xmax reciprocity

The owner-requested `Xmax` reciprocity hypothesis remains included and compatible. The normalized
position `x/Xmax` is invariant under a common rescaling.

If a future native derivation produced

```text
kappa/xi = Xmax^2 (f4/f2),
```

then this branch would select the dimensionless ratio

```text
R_star/Xmax = sqrt(f4 B/(f2 A)).
```

That would be a meaningful particle-to-cell closure, but it would not by itself select the absolute
value of `Xmax`: `Xmax`, `R_star`, energy, and mass retain the same common homothety. Reciprocity is a
compatibility/ratio principle here, not an absolute scale selector.

## Mass ruling

Three steps must not be conflated:

1. `E_star` is the energy of the conditional round-`S2`, `L2+L4` branch.
2. `E_star/c_E^2` is a rest-mass conversion that still contains the undetermined ruler and action
   normalization.
3. Phase G's `M_N^(0)=2E4` is a conditional EH/weak-field unit-response identity; it is not a native,
   unconditional UDT mass and does not fix the physical gravitational coupling.

No unconditional mass, native carrier, native source, complete matter action, or boundary charge is
derived here.

## Four evidence gates

1. **Preregistered:** yes, commit `29a8591`, before detailed candidate inspection.
2. **Full space or bounded scope:** full tracked closure of the existing corrected static/fixed-Q
   branch; not the absent complete metric-plus-matter solution space.
3. **Independently verified:** yes, independent AST/source replay, dimensional algebra, explicit
   derivative-count check, and 25 exercised mutation catches; no fresh external-model review.
4. **Every premise audited:** yes for the bounded branch; carrier, action, coefficients, physical
   boundary, EH readout, and time-live limitations remain explicitly conditional/open.

## Honest frontier

The audit closes a misconception, not the matter action. The apparent soliton radius does not supply
the missing UDT scale; it exposes where the missing scale entered.

The next sharp question is whether the metric, finite-cell angular sector, CSN, bootstrap, and
`Xmax` reciprocity derive the relative normalization of the first admissible two- and four-derivative
angular invariants—possibly as `kappa/xi = Xmax^2 f(state)`—without first adopting the round `S2`
carrier or importing an action. Failure would mean the existing `L2+L4` branch is a conditional model
of stable matter, not the missing native matter law.
