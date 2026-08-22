# G213 audit report — determinant-one spatial remainder and completed rank closure

Date: 2026-08-22

## Landing

```text
FIVE_MODE_DETERMINANT_ONE_SPATIAL_REMAINDER
__G207_G208_COVER_FOUR_LOGARITHMIC_COORDINATES
__ONE_RADIAL_VERSUS_SCREEN_GRADING_COORDINATE_WAS_NOT_INDEPENDENTLY_CENSUSED
__COMPLETED_PAIR_PLUS_RULER_DENSITY_RETAINS_THE_FULL_PULLBACK
__THE_G129_SIX_PAIR_NETWORK_RETAINS_EXACT_RANK_TEN
__NORMALIZED_COMPLETED_METRICS_WITHOUT_DENSITIES_ARE_NOT_FAITHFUL
__NO_NETWORK_VALUES_OR_PHYSICAL_PAIR_POPULATION_DERIVED
```

Status: `DERIVED_CONDITIONAL__INDEPENDENTLY_VERIFIED__EXTERNAL_REVIEW_REPAIRS_ACCEPTED`.

## Result

After the supplied G211 spatial-volume scalar is removed, the positive spatial metric has exactly
five determinant-preserving pointwise coordinates. Relative to a supplied radial line and screen,
they split uniquely into:

- one radial-versus-screen grading mode;
- two radial-screen mixing modes;
- two trace-free screen-shape modes.

G207 represented the two screen-shape directions. G208 represented the two mixing directions in
the unique trace-free logarithm. They did not independently census the grading mode. This is a
coordinate inventory, not a new selected physical function.

The more consequential result is the completed-pair information theorem. The G176 completed metric
`h_s` has determinant `-1`, but the typed relation also contains the positive ruler density
`m=sqrt(-det h_sigma)`. The identities

\[
h_s=\operatorname{diag}(1,m)^{-T}h_\sigma\operatorname{diag}(1,m)^{-1},
\qquad
h_\sigma=\operatorname{diag}(1,m)^Th_s\operatorname{diag}(1,m)
\]

are exact. Therefore `(m,h_s)` contains exactly the same local metric information as the full
auxiliary pullback. Replacing all six G129 pullbacks by these completed tuples preserves the exact
rank-ten reconstruction of the ambient Lorentz metric.

Deleting `m` fails sharply. A positive common spatial rescaling changes the ambient metric and
every auxiliary pullback density while leaving every normalized completed metric unchanged. The
density is not bookkeeping that can be discarded; it is the carried spatial calibration channel.

## Evidence

- Production: 23 exact dependency-free integer/Fraction algebra checks.
- Independent: exact mode ranks `5/4/5`, 10,000 exact rational Lorentz metrics, 300,004
  assertions, independent row reduction, and 10,000 distinct density-blind countermetrics.
- G129 design rank: exactly 10 in both implementations.
- Hostile mutation catches: 32 registered in the package replay.
- Source provenance: fixed hashes of the 12 load-bearing G129/G176/G207/G208/G211/G212 files.
- Fresh external review: no bounded scientific defect; replay/certification repairs implemented.
- Repair-only external follow-up: accepted; registered repairs and unchanged bounded landing
  independently verified.

## Four banking gates

1. **Preregistered:** PASS, committed and pushed before execution.
2. **Full space or bounded scope:** PASS WITH CAVEATS — complete positive determinant-one local
   spatial stratum and complete regular local completed-tuple map; no global pair population.
3. **Independent verification:** PASS — separate stdlib/Fraction implementation imports no
   production code.
4. **Premise audit:** PASS WITH CAVEATS — split, reference, known germs, G176 working clarification,
   and G129 witness remain explicit supplied/conditional premises.

## Maximum conclusion

The local kernel-to-metric information bridge is closed conditionally: a supplied, valued,
rank-complete network of typed completed reciprocal relations can be the metric state. G213 does
not predict that state from finite anchors or prove which observer germs populate the network.
