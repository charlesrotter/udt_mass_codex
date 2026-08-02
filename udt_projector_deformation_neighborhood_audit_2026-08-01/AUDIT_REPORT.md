# Projector deformation-neighborhood audit — report

Date: 2026-08-01  
Frozen base: `4fa6de0d52b0be976cb39a5b91ab49cd33164c66`  
Preregistration commit: `edf79d5`  
Grade: **VERIFIED-WITH-CAVEATS; FRESH EXTERNAL SEMANTIC REVIEW OPEN**

## Result first

The intrinsic-projector result is functionally persistent inside the registered stationary complete
off-shell family.  It is not confined to six isolated configurations.

Every C01--C06 center lies in an open `C3` neighborhood of smooth complete `R x S3` configurations
in which the metric retains:

- the rank-three curvature-fingerprint certificate for one intrinsic timelike clock line;
- the nonzero twist-selected global spacelike ruler line;
- the rank-one ruler projector and unique rank-two screen complement;
- a globally smooth Lorentzian coframe and positive displayed spatial slice; and
- nonzero relative projector curvature somewhere.

The profile and the complete screen were released.  The screen neighborhood contains its area mode,
both metric shear modes, and its `O(2)` coframe-gauge direction.  No action, carrier, bootstrap rule,
or field equation was imposed.

The maximum conclusion is:

```text
DERIVED_CONDITIONAL_ON_THE_REGISTERED_STATIONARY_COMPLETE_OFFSHELL_FAMILY:
EACH_C01_C06_CENTER_LIES_IN_AN_OPEN_CONFIGURATION_NEIGHBORHOOD_WITH_THE
INTRINSIC_CLOCK_RULER_PROJECTOR_GATES_AND_NONZERO_RELATIVE_CURVATURE_SOMEWHERE.
```

This is configuration-space geometry.  It is not on-shell selection, energetic stability, matter,
or mass.

## Why an infinite-dimensional scan was not needed

The clock certificate uses only the metric's third jet at one event.  Its exact determinant is
nonzero at all six centers, hence remains nonzero under sufficiently small `C3` profile and screen
perturbations.  The response witness uses first jets and is likewise open.  Global invertibility and
positive-slice inequalities have uniform `C0` margins on compact `S3`.

These continuity arguments cover the full released functional directions near every center.  They
prove existence of open neighborhoods but do not calculate explicit radii.  The audit supplements
them with exact finite-dimensional charts to expose rather than hide cancellation walls.

## New exact response algebra

For a general screen first jet, define the two-component ruler-to-screen connection vectors

```text
v1=(-p2,-p3),
v2=(A,B+t1/2),
v3=(B-t1/2,D).
```

The three relative-curvature scalars are the exact determinants

```text
W12=det(v1,v2),  W13=det(v1,v3),  W23=det(v2,v3).
```

All three must vanish for the complete local relative response to vanish.  This corrects a possible
shortcut in which one displayed component could be mistaken for the whole response.

For the symmetric screen chart

```text
P=exp[phi(lambda I+mu S1+nu S2)],
```

the registered north event gives

```text
W12=(6lambda+6mu-3nu+50)/2500,
W13=(-3lambda+3mu+6nu+100)/2500,
W23=1+(9/2500)(lambda^2-mu^2-nu^2).
```

The equal-screen axis has `W23=1+(3lambda/50)^2`, so it is nonzero for every real `lambda`.  The
six sampled weights were not exceptional points.  Releasing shear reveals real cancellation strata:

- `S1`-only: one north-event zero at `(lambda,mu)=(25/2,-125/6)`;
- `S2`-only: one north-event zero at `(lambda,nu)=(-200/9,-250/9)`;
- both shears: the affine north-event zero line

```text
lambda=5nu/4+25/2,
mu=-3nu/4-125/6.
```

These are retained off-shell local-response walls.  The response may still be nonzero elsewhere on
those complete configurations.

## What is robust and what is not selected

Robust in this family:

- all six center certificates;
- the intrinsic clock/ruler/projector construction under small full profile/screen changes;
- global descent for smooth invertible screens;
- nonzero response on a neighborhood of each center; and
- nonzero north-event response along the entire equal-screen `lambda` axis.

Still unselected or open:

- why a native equation or same-solution bootstrap return occupies this family;
- the profile, screen, `lambda`, shear, topology, or wall stratum;
- any action or relative coefficient;
- the `S2` carrier or its emergence;
- source, boundary, dynamics, stability, mass, and physical-family meaning; and
- nonstationary, non-block, and other-completion neighborhoods.

## Stability/bootstrap interpretation

This is a useful advance for the stability hypothesis because a possible metric-native structural
ingredient is not a fine-tuned single example.  The advance is upstream of stability: no Hessian,
time evolution, energetic functional, or native mass was tested.

Bootstrap remains `WORKING_ON_SHELL_ADMISSIBILITY`.  It was deliberately excluded here.  A future
test may intersect an independently stated same-solution global/local closure rule with this atlas.
It may not define that rule by asking it to select the positive region.

## Evidence

- exact SymPy 1.13.1 derivation of the general first-jet response and all subfamily loci;
- exact reconstruction of all six parent clock-certificate determinants and response fractions;
- independent standard-library `Fraction` implementation from exterior forms through the Cartan
  connection: 49 checks;
- four arbitrary general rational probes, five affine-wall samples, both one-shear wall points, and
  two rational `SO(2)` gauge rotations;
- 24/24 exercised semantic mutation catches;
- fifteen preregistered source paths frozen by Git blob and SHA-256;
- six frozen native-action manifests / 133 paths replayed;
- current premise, current-path, frontier, link, and repository-test gates replayed; and
- tests: `70 passed, 1 xfailed`.

## Four banking gates

1. **Preregistered:** yes, commit `edf79d5`, before the general response or wall loci were calculated.
2. **Full or bounded:** full functional neighborhoods for stationary smooth profile and complete
   block-screen directions around all six centers; explicitly not nonstationary, non-block, other
   topology, or on-shell solution space.
3. **Independently verified:** yes for the load-bearing new algebra using a no-SymPy implementation;
   fresh external semantic review was not authorized, so the grade remains caveated.
4. **Premises audited:** yes; every retained, freed, excluded, and open object is in the premise and
   outcome ledgers, and all wall types remain separate.

No GPU work, physics adoption, canonization, or repository reorganization was performed.

