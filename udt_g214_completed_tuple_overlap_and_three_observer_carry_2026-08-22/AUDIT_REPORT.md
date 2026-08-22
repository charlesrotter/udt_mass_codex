# G214 audit report — completed-tuple overlap and three-observer carry

Date: 2026-08-22

## Landing

```text
COMPLETED_TUPLE_DESCENT_CLOSES_ON_SUPPLIED_CALIBRATED_PAIR_COVERS
__RULER_DENSITY_CARRIES_THE_OVERLAP_DETERMINANT
__NORMALIZED_PAIR_METRIC_CARRIES_AN_SL2_COCYCLE
__G130_RECONSTRUCTION_TRANSFERS_WITHOUT_DENSITY_LOSS
__ARBITRARY_THREE_OBSERVER_FULL_TUPLE_COMPOSITION_REMAINS_NOT_DERIVED
```

Status: `DERIVED_CONDITIONAL__INDEPENDENTLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.

## Result

G213's local equivalence is natural on the declared positive calibrated pair-chart groupoid. If
\(h_j=P_{ij}^Th_iP_{ij}\), then

\[
m_j=(\det P_{ij})m_i,
\qquad
C_{ij}=J_iP_{ij}J_j^{-1}\in SL(2,\mathbb R),
\qquad
h_{s,j}=C_{ij}^Th_{s,i}C_{ij}.
\]

The induced transitions satisfy \(C_{ij}C_{jk}=C_{ik}\), and reconstructing from the transformed
tuple returns exactly \(P_{ij}^Th_iP_{ij}\). Therefore G130 lawful overlap descent transfers from
full pullbacks to typed density-completed tuples without losing scale.

The theorem also sharpens the object type. The normalized metric is invariant under pure ruler
reparameterization, but under a general calibrated rechart it is equivariant through the induced
determinant-one congruence. The density is a positive pair-area density; it behaves as the ruler
density when clock calibration is held fixed.

This does not close arbitrary three-observer composition. Distinct `AB`, `BC`, and `AC` pair
surfaces are not overlap charts of one surface, and their metrics are not arrows to multiply. The
G171 incidence defect survives exactly. Scalar composition follows on the matched-incidence
subfamily or after explicit incidence identifications are supplied.

## Evidence

- Preregistered and pushed at `b15d5b4d` before outcome execution.
- Production: 23 exact dependency-free rational checks.
- Independent: 10,000 exact rational cases and 200,000 assertions in a separate implementation.
- Hostile controls: 10/10 caught, including wrong density weights, reversed cocycle order,
  false full-rechart invariance, deleted density, false incidence matching, and pair-metric
  multiplication.
- Source provenance: 14/14 frozen G130/G170/G171/G175/G176/G180/G213 files matched.
- No-write aggregate replay: pass.

## Four gates

1. **Preregistered:** PASS.
2. **Full space or bounded scope:** PASS WITH CAVEATS — all regular positive upper-triangular
   calibrated transitions at order zero; singular and non-adapted charts omitted.
3. **Independent verification:** PASS — separate exact `Fraction` implementation imports no
   production code.
4. **Premise audit:** PASS WITH CAVEATS — supplied split, orientations, transition maps, known
   germs, and G176 working clarification remain explicit.

## Maximum conclusion

The local-to-cover information bridge is closed conditionally. G214 proves faithful descent of a
supplied compatible density-completed valuation; it does not generate that valuation, populate its
germs, or produce cross-pair incidence maps.
