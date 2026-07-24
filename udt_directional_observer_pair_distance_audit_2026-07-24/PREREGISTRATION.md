# Directional observer-pair distance audit — preregistration

Date: 2026-07-24

Base: `c63ae3e14963df18e86c4bf4dff82451684b404a`

Compute: bounded CPU-only exact Riemannian geometry and complete source census

## Owner clarification controlling this audit

`X_max` is sought as a consequence of the complete UDT metric. It is the
greatest possible separation between two observers. There is no privileged
center.

Accordingly, this audit may not identify `X_max` with:

- a radius from a universal origin;
- a one-sided coordinate endpoint;
- the distance from a neutral torus to a cap;
- a seal coordinate value; or
- a preferred observer's radial chart.

## Whole question

What do the currently supplied complete observer-rest spatial metrics
actually determine about:

```text
d_h(p,q) = two-point geodesic distance,
X(p,n)   = directional minimizing cut/endpoint distance,
E(p)     = sup_q d_h(p,q),
X_max    = sup_(p,q) d_h(p,q)?
```

Can any existing nonround complete witness calculate a directional band, and
does any existing witness also solder that geometric diameter to the
founding clock-dilation asymptote?

## Exact bounded source universe

The audit covers:

1. all 12 `FC01`--`FC12` completion rows;
2. all 28 `B01`--`B28` equation/evidence families;
3. every complete metric witness named by those registries;
4. the conditional round `S3_b` spatial branch;
5. the local WR-L clock-depth control; and
6. the six clock/angular solder families from the immediately preceding
   audit.

No topology type is promoted to a metric. No quotient receives an invented
round metric, lattice, scale, or observer pairing.

## Definitions frozen before evaluation

For a complete connected observer-rest Riemannian manifold `(Sigma,h)`:

```text
d_h(p,q) = infimum of h-length over curves from p to q.

X(p,n) = supremum of s for which exp_p(t n), 0<=t<=s,
         remains minimizing, for unit n in T_p Sigma.

E(p) = sup_q d_h(p,q).

diam(Sigma,h) = sup_p E(p) = sup_(p,q) d_h(p,q).
```

On a compact complete manifold, `E(p)=sup_n X(p,n)`. The directional spread
at observer `p` is

```text
Delta_X(p)=sup_n X(p,n)-inf_n X(p,n).
```

`X_max` denotes the scalar global supremum. If a later discussion uses
`X_max(n)` informally, it must be translated to `X(p,n)` or another explicit
directional object.

No privileged center merely forbids a distinguished universal base point.
The stronger claim `E(p)=constant` requires observer-frame equivalence,
homogeneity, or a direct metric proof; it is not inferred from vocabulary.

## Candidate classes

| ID | Candidate | Data allowed | Pre-evaluation status |
|---|---|---|---|
| D01 | conditional round `S3_b` | exact complete spatial metric | CALCULABLE_CONTROL |
| D02 | local WR-L branch | supplied local clock/depth metric | INCOMPLETE_GLOBAL_GEOMETRY |
| D03 | `FC01`--`FC12` | registered completion taxonomy and any supplied profiles | CENSUS_REQUIRED |
| D04 | `B01`--`B28` | registered family witnesses without cross-family splice | CENSUS_REQUIRED |
| D05 | lens/torus/mirror/boundary topology families | topology only unless a complete metric is actually supplied | NO_METRIC_BY_DEFAULT |
| D06 | clock/angular solder F01--F06 | exact prior family rulings | CENSUS_REQUIRED |

## Physical and mathematical statuses

- no privileged center: `OWNER_CLARIFIED_FRAME_RULE`;
- pairwise/geodesic distance from a supplied physical `h`: `DERIVED`;
- observer-rest spatial metric and observer congruence: `CONDITIONAL` until
  supplied by a branch;
- exact observer-frame equivalence over the full finite cell: `OPEN` unless
  proved by the metric;
- round `S3_b`: `CONDITIONAL` spatial control;
- scale `b`: physical on the calibrated-metric working branch but
  `UNSELECTED`;
- clock/angular same-scalar compact solder: `OBSTRUCTED_IN_PRIOR_BOUNDED_CLASS`;
- nonround complete clock-soldered witness: `OPEN / AVAILABILITY_TO_AUDIT`;
- CMB comparison: `OBSERVATIONAL_COMPARISON_OPEN`;
- action, source, carrier, mass, density, and scale closure: `OPEN` and
  absent.

## Certification and falsification

Certification requires:

1. one row for each of the 12 FC and 28 equation families;
2. no topology-only row counted as a complete metric witness;
3. exact round two-point distance, cut distance, eccentricity, diameter, and
   directional spread derived without choosing a center;
4. the earlier `pi b/4` neutral-torus-to-cap depth kept distinct from the
   round `pi b` observer-pair diameter;
5. separate gates for complete spatial geometry, no-center two-point
   semantics, frame equivalence, clock solder, and infinite-dilation
   asymptote;
6. no directional variance reported without a complete nonround metric;
7. coordinate changes, coframe rotations, axis exchange, and constant common
   scale distinguished from physical shape changes;
8. independent recomputation and exercised corruption catches; and
9. no CMB, density, mass, action, or desired value used to select a result.

The zero-variance round result is falsified by any unit direction with round
cut distance other than `pi b`. The complete-witness census is falsified by a
missed supplied complete nonround metric. The physical `X_max` pass is
falsified unless one branch supplies both the global pair diameter and the
founding pairwise clock-dilation asymptote.

## Maximum allowed conclusion

At most:

```text
THE_CURRENT_COMPLETE_METRIC_WITNESSES_DO_OR_DO_NOT_CALCULATE_A
DIRECTIONAL_PAIR_DISTANCE_BAND; THE_GEOMETRIC_DIAMETER_IS_KEPT
DISTINCT_FROM_PHYSICAL_UDT_X_MAX_UNLESS_CLOCK_SOLDER_AND_PAIRWISE
ASYMPTOTIC_DILATION_ARE_PRESENT_IN_THE_SAME_BRANCH.
```

No numerical value of physical `X_max`, CMB origin, action, matter source,
mass, or density closure can be claimed.
