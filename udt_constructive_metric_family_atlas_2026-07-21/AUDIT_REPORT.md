# UDT constructive all-slot metric-family atlas

Date: 2026-07-21

Base: `093114f90721c6f176f78f1823455445a7db40f0`

Preregistration: `485e70b`

Mode: CPU-only constructive configuration observation. No action, equation of motion, ODE, PDE,
relaxation, physical evolution, comparison target, or GPU work.

## Result first

The package does the deliberately unexciting work requested by Charles: it constructs four correlated local
four-dimensional metric families first and records what their complete geometry does. It does not
ask which geometry resembles a desired universe.

Primary classification:

```text
CONSTRUCTIVE_ALL_SLOT_CONFIGURATION_FAMILIES_OBSERVED_IN_REGISTERED_LOCAL_REGIME
```

Four deterministic analytic coefficient banks were traversed through five deformation values and
eight four-coordinate points. This produced 160 retained configuration records and 129 distinct
metric two-jets. All ten conditional metric functions are live: three base functions, three screen
functions including the off-diagonal shape, and all four base–screen shifts. Every nonzero
deformation depends on time, depth, and both angular coordinates.

The maximum metric/Cartan identity residual is `3.3306690738754696e-16`, below the preregistered
`2e-10` gate. The raw configuration ledger SHA-256 is:

```text
41968a7fd682ffebd6c871a440cbcb4ac951355a96a97be7c5c854b0773f454b
```

## What was observed

The deformation origins are constant-coframe references. All 32 sampled origin records have zero
curvature. They represent one metric jet repeated across banks/points and were retained rather than
deduplicated away.

Every one of the 128 nonzero-deformation records in the registered families exhibited:

- Ricci matrix rank four;
- curvature-operator rank six;
- screen-shear map rank two;
- nonzero twist of rank one; and
- nonzero mixed base–screen curvature.

The sampled scalar curvature ranged from approximately `-1.36545` to `1.20771`. Mixed curvature,
shear, and twist varied continuously across the coordinate/deformation records and changed sign or
magnitude without being used as acceptance conditions.

This is an `OBSERVED` finite-family result, not a proof about every metric. In these four correlated
paths, the nonzero sampled records were fully coupled while the undeformed references were not. The
scan does not establish that either behavior is generic, ordinary, open/dense, or physically
important.

## Sampling-rank correction from fresh review

The ten latent fields are all present, and the abstract latent-to-slot coordinate map has rank ten.
But the performed scan does **not** vary ten amplitudes independently. Inside each bank, one common
`lambda` moves all ten latent fields and `phi` together. Including the four coordinates, the sampled
family therefore has at most five local tangent directions.

The actual slot-value tangent ranks with respect to `(lambda,x0,x1,x2,x3)` are:

```text
rank 0:   4 records
rank 1:  28 records
rank 4:  16 records
rank 5: 112 records
```

This distinction was found by the fresh adversarial reviewer and is now machine-recorded in
`SAMPLED_TANGENT_RANK.tsv`. The 128/128 finite-record census remains correct. It is evidence about
four correlated paths, not an independent ten-amplitude scan.

## `phi` and the angular sector

The `C02` field is defined without a metric–`phi` constraint, but its sampled coefficients share the
same common `lambda`. The scalar itself was negative in 54 records, within the registered zero
tolerance in 12, and positive in 94.

For `dphi`:

- 18 records were timelike;
- 32 had exactly zero gradient at the undeformed references;
- zero records had a nonzero numerically near-null gradient; and
- 110 were spacelike.

Thus these constructive families did not reproduce a forced nonzero lightlike `phi` branch. This is
not a no-go theorem: the coefficient banks are finite. The registered records show only that
simultaneous sampled metric/`phi`/angular activity did not force a nonzero null `dphi` gradient.

Every nonzero deformation also carried horizontal and vertical `phi` support, nonzero screen shear,
twist, and mixed curvature. The package records their joint incidence but derives no causal or
dynamical equation between them.

## The all-slot chart

The regular family is generated from six scalar functions and four shifts. A factorized base and
screen coframe guarantees a Lorentzian base and positive screen. The abstract latent-to-slot chart
Jacobian has rank ten in every regular record; the sampled five-parameter tangent ranks are reported
separately and never promoted to ten.

That factorization is a chosen regular coordinate chart, not the whole metric space. Two nontrivial
coordinate orbits and one local Lorentz orbit were evaluated with residuals below `2.3e-16` and
were not counted as new geometries.

The chosen chart was separately released toward its boundary through 20 exact zero-jet closure
records. Four singular records, Euclidean records, and split/two-time signature records were all
retained. The inverse-based P01 evaluator correctly stopped on singular or non-Lorentzian records;
the atlas did not call those configurations failures.

## CSN orbit

Two anchors were rescaled by two positive all-coordinate CSN factors. Inertia was preserved and the
determinant transformed with the verified weight eight. Scalar curvature changed with the local
representative. No representative or physical scale was selected.

## What this does not mean

These configurations are not EOM solutions. There is no selected UDT action against which to test
them. Time dependence is coordinate dependence, not physical propagation. Full curvature rank is
not a stability, matter, or merit statement. No boundary, topology, finite-cell completion,
`X_max`, scale, source, carrier, mass, or bootstrap closure was evaluated.

The finite basis is not exhaustive. It uses smooth quadratic latent functions in one regular
factorized chart, four coefficient banks sharing one amplitude per bank, five deformation values,
and eight points. Higher-order,
nonanalytic, nonsmooth, independently connected coframe charts, moving split/projector, and global
topology families remain open.

## Method consequence

The observation does not justify returning to a targeted physics hunt. It records that setting
shifts, shear, twist, angular dependence, or time dependence to zero would remove behavior present
in every nonzero record of these four correlated paths.

The correct next decision belongs to `PONDER`, not automatic derivation. A later constructive tile
could first release the shared amplitude, polynomial basis, and factorized chart. No genericity
theorem should be inferred or targeted merely because this sample displayed one uniform pattern.

## Four evidence gates

1. **Preregistered:** yes, commit `485e70b`, before family construction.
2. **Full or bounded scope:** bounded and explicit—four analytic banks, five deformations, eight
   points, one regular all-slot chart, gauge/CSN release checks, and zero-jet signature closures.
   Arbitrary functions, global topology, other field realizations, dynamics, and solutions remain
   open.
3. **Independently verified:** a non-importing verifier reconstructs one complete family with SymPy,
   recomputes its curvature independently, replays all raw identities, and exercises deliberate
   corruptions. A fresh zero-context reviewer independently recomputed all 160 records and returned
   `VERIFIED-WITH-CAVEATS`; its sampling-rank correction is incorporated. The package grade is
   `VERIFIED_WITH_CAVEATS`.
4. **Premises audited:** yes. The split chart, coefficient controls, `phi` realization, CSN orbit,
   rank threshold, chart points, excluded dynamics, and unsampled global sectors are explicit.

Maximum conclusion:

```text
CONSTRUCTIVE_METRIC_CONFIGURATION_FAMILIES_CHARACTERIZED_NOT_DYNAMICAL_SOLUTIONS
```
