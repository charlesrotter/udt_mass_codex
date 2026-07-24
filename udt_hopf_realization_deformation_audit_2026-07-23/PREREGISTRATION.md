# Hopf realization deformation audit — preregistration

Date: 2026-07-23
Mode: metric-led, CPU-only exact algebra and frozen-evidence crosswalk
Base: `24420146bc6abe15bec931a3673932756a5054c7`

## Whole question

The established conditional seed is

```text
n(phi,delta) = (
  sech(2phi) cos(delta),
  sech(2phi) sin(delta),
  -tanh(2phi)
).
```

The complete registered coframe chart contains ten fields,

```text
E(A,D,S) = [[A,0],[D S,D]],
```

plus the separately represented scalar `phi`. The prior bridge uses only an
aligned angular reciprocal-depth character and a supplied phase
`delta=xi1-xi2`.

The bounded question is:

> Do variations of the complete coframe and conditional reciprocal-toric
> quotient induce the full tangent freedom of a sphere-valued field, a
> restricted seed deformation, or no well-defined globally descending
> carrier deformation map?

The test observes the deformation image. It does not demand a particle,
stable shape, action, or unit Hopf result.

## Complete variation census

The audit must classify separately:

1. three base-block variations;
2. angular common scale;
3. angular reciprocal depth;
4. angular upper-triangular shear;
5. all four base-angular shifts;
6. the independent scalar variation;
7. common-scale/CSN representative changes;
8. local Lorentz coframe changes;
9. torus-coordinate and target-phase changes;
10. discrete torus lattice/gluing changes;
11. variations of a supplied celestial/screen section; and
12. arbitrary tangent sections of the comparison round-`S2` carrier.

No zero effect may be assigned merely because a variable is inconvenient.
Each direction must be typed as an induced map variation, a kernel direction,
a gauge/coordinate variation, a connection/transport variation, a discrete
global change, or an undefined direction of the existing bridge.

## Exact algebra contract

### A1 — target tangent rank

Differentiate the displayed seed with respect to both `phi` and `delta`.
Compute its exact Gram matrix and rank for finite `phi`. Re-express the map in
the smooth polar variable defined by `tan(eta)=exp(2phi)` and distinguish
coordinate degeneration at the poles from loss of the target tangent plane.

### A2 — complete-coframe differential

Differentiate the actually established bridge with respect to every one of
the ten coframe fields and the independent scalar. Do not extend the bridge
through angular shear or through an unselected scalar/character
identification by definition. Record the rank only on the exact domain where
the source bridge is defined.

### A3 — shift-sector phase test

From the complete coframe form derive the angular one-forms

```text
theta_ang = D(dxi + S dx).
```

Test whether the row-difference one-form built from `S` is:

- a phase scalar;
- a phase connection;
- locally integrable only under a curvature condition; and/or
- globally integrable only under a period/holonomy condition.

Derive its transformation under base-dependent torus-coordinate changes.
An exact/gauge part may not be counted as a physical carrier deformation
without a derived section or boundary framing.

### A4 — angular-shear/eigenaxis test

Test the strongest metric-only phase candidate obtainable from the
determinant-normalized angular metric, including its behavior under angular
basis changes and at the isotropic locus. No eigenaxis angle may be promoted
unless it descends as a global, frame-independent `S1`-valued object.

### A5 — fiber-versus-section test

Compare the abstract two-dimensional vertical tangent space of the
conditional celestial/screen `S2` fiber with the image of metric/coframe
variations. The existence of a fiber or of arbitrary variations of a
separately supplied section may not be counted as a metric-selected section.

### A6 — global completion test

Carry every locally admitted deformation type through all twelve registered
finite-cell completion classes. Test cap regularity, torus-coordinate
existence, orientation, monodromy, phase descent, null/zero-`dphi`
interfaces, and boundary/framing requirements. `FC04` and `FC12` receive no
preference.

### A7 — bootstrap brackets

Keep four roles separate:

- no bootstrap in the local tangent calculation;
- current after-solution admissibility;
- a future explicit representative/section map `Sigma`;
- a future explicit varied global functional.

No total density is inserted into local equations and no density scan is
run.

## Ansatz, boundary, and provenance ledger

- **free-and-explored:** all eleven registered field directions, every
  completion class, both causal-sign strata where the prior object exists,
  and every phase candidate listed in `DEFORMATION_CANDIDATES.tsv`;
- **pinned-by-THEORY:** the complete coframe chart and its exact group law,
  CSN behavior, the local nonnull-`dphi` intrinsic fiber, and the registered
  completion taxonomy, each with cited source manifests;
- **conditional/supplied:** the toric periods, aligned axes, quotient action,
  caps, orientation, full reciprocal range, and round comparison target;
- **not adopted:** the round carrier as native, `L2+L4`, any field equation,
  physical boundary, transport selector, density center, mass, or time law.

There is no merit filter. Singular, boundary, nonorientable, stratified, and
nonintegrable completions are characterized rather than discarded.

## Fail-closed catches

The independent verifier must reject:

1. counting the supplied phase as a coframe-derived field;
2. counting a fixed or constant phase rotation as arbitrary local phase
   freedom;
3. counting a torus-coordinate gauge transformation as physical carrier
   motion;
4. treating a phase connection with nonzero curvature as a scalar phase;
5. ignoring global periods/holonomy;
6. identifying an angular eigenaxis across its isotropic degeneracy;
7. promoting angular shear to target phase without a descent law;
8. promoting an `S2` fiber to a section;
9. reporting a full-coframe rank from a bridge defined only on the aligned
   diagonal submanifold;
10. equating a two-dimensional target tangent space with a two-dimensional
    metric-induced image;
11. silently selecting `FC04`, `S3`, the free quotient, chirality, or round
    completion;
12. propagating the local bridge across null or zero-`dphi` interfaces;
13. turning current bootstrap into a local deformation selector;
14. inserting total density or running a density fit;
15. inferring an action, stability, time-live persistence, mass, or carrier
    emergence.

## Conclusion ceiling

The strongest permitted result is an exact dependency/rank/descent
classification. Candidate maximum labels are:

```text
FULL_METRIC_INDUCED_CARRIER_DEFORMATION_SPACE
RESTRICTED_CONDITIONAL_SEED_DEFORMATION_ONLY
NO_WELL_DEFINED_FULL_COFRAME_TO_CARRIER_MAP
SHIFT_SECTOR_SUPPLIES_CONNECTION_NOT_SECTION
GLOBAL_REALIZATION_REMAINS_COMPLETION_DEPENDENT
```

More than one may apply at different declared domains. Even a full local
tangent correspondence would not derive an action, source, physical
boundary, global branch, density window, stable dynamics, mass, or native
carrier.
