# Full-coframe first-jet and stratified-transition atlas

Date: 2026-08-04
Preregistration: `18916943`
Frozen source/sector/stratum universe: `2242893f`
Status: `VERIFIED_WITH_CAVEATS`

## Result first

Releasing the complete first jet reveals a genuine reciprocal–angular transition structure, but no
physical evolution law.

For each spacetime direction, all ten symmetric metric first-jet components survive the sixteen
coframe first-jet components; the six-dimensional kernel is exactly local Lorentz presentation
gauge. Across all four directions the exact map has rank `40` and nullity `24`. Thus this atlas does
not freeze a time or spatial metric amplitude.

In the exact complete block chart,

```text
s_phi = u^T eta_base u + v^T v,
u=A^-T(p_base-S^T p_screen),
v=Q^-T p_screen.
```

Holding coordinate `dphi` fixed, mixing alone gives `s_phi=-3,0,+1`; unit-area screen shear alone
gives `-3/4,0,+3`. The causal type of founded depth is therefore a joint property of the complete
reciprocal/angular metric, not a property of a frozen `phi` sector.

At a nonzero-null crossing, `dphi` and its metric-dual vector remain finite but the normalized
projector has a simple pole. At `dphi=0`, timelike and spacelike approaches have unequal projector
limits. At coframe or screen rank loss the metric becomes degenerate and the inverse/Levi-Civita
construction fails, although the metric adjugate may remain finite.

The covector stabilizer algebra changes intrinsically:

```text
timelike so(3), spacelike so(1,2), nonzero-null iso(2), zero so(1,3).
```

These are real geometric transition strata. They do not choose which stratum or path is physical.

## Bounded verdict

```text
DERIVED_FULL_METRIC_FIRST_JET_SURJECTION__
DERIVED_JOINT_RECIPROCAL_ANGULAR_CAUSAL_STRATA__
NORMALIZED_REDUCTION_HAS_NO_UNIVERSAL_STRATIFIED_EXTENSION__
NO_KINEMATIC_EVOLUTION_RETURN
```

This is not a time-live numerical solve. An arbitrary configuration-space path is not physical time
evolution, and the Maurer–Cartan relation starts at second-jet order as an identity for an actual
coframe. A physical solve still requires the missing bulk/global return and boundary law.

## Scope and consequences

The result closes the frozen-sector concern only on the preregistered local, finite-`phi`,
nondegenerate first-jet tile: all ten metric directions in all four derivative slots are active.
The `phi -> +/- infinity` entries are limit strata, not regular released sectors. The result does
not close second-jet curvature, nonlinear evolution, global branch, topology, boundary, or
stability scope.

The nonzero-null result also corrects a possible overreaction to projector singularity. A failed
normalized reciprocal/screen split need not mean a singular spacetime. Future cross-stratum laws
should be tested first in unnormalized coframe/depth variables. That is a mathematical routing clue,
not authorization to adopt a new fundamental variable or law.

Finite founded `phi` never causes rank loss because its reciprocal pair determinant is one. Its
infinite limits lack a finite nondegenerate fixed-chart metric limit but do not derive a physical
endpoint or `X_max`.

## Mass, stability, and bootstrap status

Unchanged. F01/F02 remain separate conditional geometry-only mass-bearing routes. F04 remains the
separate carrier/action-conditional static finite-box Hopf result. The working global/local
bootstrap posit receives a richer joint configuration atlas but no return map, density selection,
fixed point, source, mass, species, or dynamics.

## Verification and fresh adversarial review

- primary exact algebra: SymPy `1.13.1`;
- independent standard-library rational reconstruction: exact agreement on every load-bearing
  rank, witness, transition, determinant, codimension, and stabilizer invariant;
- all 26 source hashes are frozen at base `d666cbab`;
- all 15 sectors, 15 strata, 17 observables, 12 operations, and 20 premises are enumerated;
- fail-closed verifier: `13/13` grouped checks and `23/23` exercised mutations caught;
- fresh read-only `gpt-5.4` review: `VERIFIED_WITH_CAVEATS`, zero blocking errors, all three exact
  entrypoints independently replayed.

The reviewer retained three scope caveats. The displayed Lie-algebra names are supported by the
computed stabilizer brackets and Killing invariants but are not independently named in the saved
rational JSON. The independent replay checks the decisive invariants but does not separately emit
the symbolic block-inverse identity. Finally, “all sectors released” is confined to the finite-phi
local first-jet tile described above. None of these caveats changes the bounded algebraic result.

## Maximum conclusion and stop line

This audit may characterize first-jet and rank/causal transitions only. It does not derive a native
action, response, source, carrier, boundary, density, bootstrap law, physical time evolution,
matter, mass, stability, observation fit, or canon statement.

After verification, the next scientific decision is whether the surviving unnormalized
reciprocal/angular data justify a bounded second-jet curvature-solder audit. No time-live solve,
GPU work, density scan, or new premise follows automatically.
