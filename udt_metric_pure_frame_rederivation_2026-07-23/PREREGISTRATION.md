# Metric-pure frame rederivation — preregistration

Date: 2026-07-23

Base: `db069753808425b8f4cb7df481c8c881918ced80`

Compute: bounded CPU-only exact algebra.

## Trigger

Charles proposed that the WR-L metric may be a limited ansatz built
without complete frame-based reciprocity. This audit restarts above WR-L
and asks what the complete recorded metric parent itself derives.

The new observer-centered correction remains frozen evidence. This
package may supersede its choice of next question, but may not silently
rewrite it.

## Whole question

Starting from the complete recorded four-dimensional
conformal-Lorentzian metric/coframe parent, before selecting a `2+2`
split, observer congruence, center, radial chart, staticity, spherical
symmetry, angular shape, shift, twist, shear, `phi` realization, action,
source, or boundary:

1. Does the metric select a preferred local inertial observer?
2. What exact local relation exists between any two timelike observer
   directions?
3. Which light-cone and frame-reciprocity statements are metric-pure?
4. Does local frame reciprocity imply a global isometry or an
   observer-centered universe chart?
5. How much of the complete metric was frozen in the WR-L reduction?
6. Is the WR-L reduction closed under generic observer changes?
7. Which WR-L profile and observational conclusions remain valid in
   their bounded reduction?
8. What, if anything, does acceleration change without a new metric
   response law?

## Observing or targeting

`OBSERVING`. Frame reciprocity is not inserted as a repair and WR-L is
not targeted for rescue or rejection.

## Metric-pure parent

The parent is:

```text
four-dimensional Lorentzian metric g
or coframe e with g=e^T eta e, eta=diag(-1,+1,+1,+1),
modulo coordinate changes and local Lorentz coframe changes,
with positive common scale treated through the recorded CSN status.
```

The conditional `2+2` bookkeeping

```text
ds2 = h_ij dx^i dx^j
    + q_AB (dy^A + A^A_i dx^i)(dy^B + A^B_j dx^j)
```

contains ten metric slots but does not select its base/screen split.

## Premise classification

All premises appear in `PREMISE_LEDGER.tsv`.

Key controls:

- four-dimensional Lorentzian signature is `pinned-by-THEORY` for this
  recorded parent;
- a local time orientation is supplied only to name the future component;
- no unit normalization is physical before a CSN representative is
  selected, although causal rays and the null cone are conformal;
- `c_E` is the measured calibrated-layer clock/length anchor;
- every local timelike direction is `free-and-explored`;
- the `2+2` split, named reciprocal plane, radial coordinate, center,
  and relation of `phi` to the metric are not selected;
- WR-L is loaded only as a reduction audit;
- no GR field equation, EH action, equivalence principle, matter,
  carrier, or signalling law is used.

## Preregistered derivations

### D1 — no metric-selected local observer

At one tangent space, prove or refute:

> A rule using only a Lorentzian metric cannot select one unit future
> timelike vector while remaining equivariant under the full connected
> Lorentz group.

Use the transitive action of `SO+(1,3)` on the future unit hyperboloid and
an explicit boost that fails to fix any proposed unit timelike vector.

### D2 — metric-pure local reciprocity

For arbitrary future unit timelike `u,v`, derive

```text
gamma(u,v) = -g(u,v)/c_E^2
chi = arcosh(gamma)
```

in the calibrated representative and construct the relative spatial
direction without choosing a center or radial chart. Test symmetry,
normalization, reciprocal null scalings, and cone preservation.

The rapidity is not to be identified with the local UDT field `phi`
without a separately derived join.

### D3 — conformal/CSN layer

For `g -> Omega^2 g`, verify that null and timelike directions survive
while unit normalization changes. Separate pre-scale causal reciprocity
from post-scale `c_E` calibration.

### D4 — local versus global

Determine exactly which statements follow from tangent-bundle frame
transitivity and which would require a global isometry, homogeneous
solution, observer-indexed pair metric, cover, or composition law.

No local theorem may be promoted to an all-observer global recentering
theorem.

### D5 — complete-to-WR-L reduction

Map the ten conditional `2+2` metric slots to

```text
g_WRL = diag(-A(r)c_E^2, A(r)^-1, r^2, r^2 sin^2(theta))
```

and count every frozen slot/dependence:

- `h01=0`;
- all four base/screen shifts zero;
- `q23=0`;
- round areal angular components fixed;
- staticity and all non-radial dependence removed;
- reciprocal base product imposed;
- only one function `A(r)` retained;
- WR-L additionally sets `A=1-r/X`.

### D6 — closure under observer change

Use both:

1. local coframe boosts, which preserve the metric but change the adapted
   observer direction; and
2. an exact base-coordinate mixing witness, which generically produces a
   nonzero shift/cross component from diagonal WR-L.

Determine whether the WR-L **ansatz family in its fixed adapted form** is
closed as a complete observer-frame configuration space.

### D7 — acceleration

For a chosen timelike field `u`, record

```text
a = nabla_u u.
```

For a local Lorentz coframe change, verify the connection and curvature
transformation laws. Distinguish accelerated-frame components from a
physical change of the metric.

### D8 — WR-L survival ledger

Regrade, without recomputing empirical data:

- reciprocal base profile;
- `X` clock/optical asymptote;
- SNe comparison;
- common global `Xmax`;
- no preferred frame;
- native mass;
- physical boundary;
- complete UDT metric status.

## Falsification and certification

The no-preferred-local-observer theorem fails if an equivariant
metric-only unit timelike selection is explicitly constructed.

The local reciprocity theorem fails if the exact observer decomposition
does not preserve norms and null cones.

The WR-L reduction ruling fails if the recorded complete metric parent
already imposes static spherical diagonal areal zero-shift structure, or
if a generic observer-adapted change remains inside the fixed WR-L
one-function chart without activating frozen fields.

The scope ruling fails if this package identifies local observer rapidity
with metric `phi`, global frame recentering, physical acceleration
response, or an action/source theorem.

Certification requires:

1. exact symbolic/rational calculations;
2. independent implementation not importing the production module;
3. exact source hashes;
4. fail-closed semantic mutations;
5. frozen-package, current-path, frontier, test, and dirty-checkout gates.

## Maximum allowed conclusion

```text
THE_METRIC_PURE_PARENT_IS_THE_FOUR_DIMENSIONAL_CONFORMAL_LORENTZIAN_METRIC_COFRAME_CLASS_NOT_WRL;IT_DERIVES_NO_PREFERRED_LOCAL_TIMELIKE_OBSERVER_AND_EXACT_LOCAL_SO_PLUS_1_3_FRAME_RECIPROCITY_WITH_A_COMMON_NULL_CONE;IT_DOES_NOT_DERIVE_GLOBAL_ISOMETRIC_RECENTERING_OR_AN_OBSERVER_INDEXED_PAIR_METRIC;WRL_IS_A_ONE_FUNCTION_STATIC_SPHERICAL_DIAGONAL_AREAL_ZERO_SHIFT_REDUCTION_NOT_CLOSED_AS_A_COMPLETE_FRAME_RECIPROCAL_CONFIGURATION_SPACE;ITS_PROFILE_ASYMPTOTE_AND_SNE_READOUT_SURVIVE_ONLY_IN_THAT_REDUCTION;PHYSICAL_ACCELERATION_INDUCED_METRIC_WARPING_REMAINS_OPEN
```

Maximum grade: `VERIFIED-WITH-CAVEATS`.

No canonization, navigation edit, action, source, carrier, mass closure,
new frame law, GPU work, or repository reorganization is authorized.
