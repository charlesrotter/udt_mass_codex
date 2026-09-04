# G342 preregistration — full metric Jacobi and beam-area response

Date: 2026-09-04
Outcome status: computational and independent-replay outcomes unseen

## Frozen question and inputs

Freeze the exact G341 metric, regular component `T>0`, normal-observer congruence, one positive
emission time, the whole future null cone, and all supplied compact-lattice lifts. Momentum scale is
affine gauge; its projective direction is free and fully explored. Set emitted frequency to one only
to state the standard vertex data `D(0)=0`, `D'(0)=I`; any other positive affine normalization must
rescale the displayed map without changing its zero set or dimensionless optical rates.

No endpoint distance convention, light/radiative model, source, detector, flux, luminosity,
observational outcome, route population, topology selection, matter model, scale, `X_max`, or canon
may enter.

## Preregistered primary alternatives

1. `A__FULL_METRIC_JACOBI_MAP_CLOSES__POSITIVE_AREA_WITH_COMPLETE_DIRECTION_CLASSIFICATION`:
   the exact endpoint variations give a rank-two Jacobi map satisfying the independently rebuilt
   curvature equation and vertex data for every direction; its determinant stays positive for all
   positive affine time, with regular principal limits.
2. `B__FULL_MAP_CLOSES_WITH_POSITIVE_AREA_BUT_DIRECTIONAL_REFOCUSING_OCCURS`:
   the determinant never vanishes, but one screen eigenresponse has a negative affine rate on a
   nonempty regular set; mean expansion and shear must be reported without calling the branch a
   caustic.
3. `C__G341_CONE_RANK_DOES_NOT_LIFT_TO_THE_VERTEX_NORMALIZED_JACOBI_MAP`:
   fixed-affine endpoint variation reveals a missed rank loss, off-diagonal response, singular
   principal limit, or failure of the curvature/Jacobi equation.
4. `D__ONLY_NUMERICAL_OR_LOCAL_BEAM_CLASSIFICATION_IS_CERTIFIED`:
   exact formulas or global sign proofs fail even though a bounded numerical census survives.

## Preregistered secondary alternatives

- expansion: `E1__BOTH_SCREEN_RATES_POSITIVE`, `E2__ONE_RATE_CHANGES_SIGN`, or
  `E3__MEAN_EXPANSION_CHANGES_SIGN`;
- shear: `S1__ZERO_ONLY_ON_SYMMETRY_FORCED_LOCUS`, `S2__ADDITIONAL_EXACT_ZERO_LOCUS`, or
  `S3__IDENTICALLY_ZERO`;
- screen mixing: `M1__DIAGONAL_BY_AXIAL_REFLECTION` or `M2__NONZERO_OFFDIAGONAL_TIDE_OR_MAP`;
- quotient: `Q1__EACH_LIFT_RETAINS_ITS_OWN_POSITIVE_AREA_AND_MULTIPLICITY_IS_PATH_LABELLED` or
  `Q2__QUOTIENT_IDENTIFICATION_CREATES_A_PER_LIFT_JACOBI_DEGENERACY`.

## Required evidence

1. Derive the map by differentiating the exact null-geodesic family with source-sky unit
   variations at fixed affine parameter. Explicitly prove why the induced endpoint-time variation
   is tangent/null gauge and drops from screen projection.
2. Rebuild the Levi-Civita connection, Riemann tensor, parallel quotient screen, and tidal matrix
   directly from the metric. Verify `D''+T D=0` rather than defining the tide from `-D''D^{-1}`.
3. Give analytic positivity or counterexamples for the two eigenresponses and determinant on the
   entire open domain. Sampling alone cannot support a global statement.
4. Give exact formulas for affine eigenrates, total/mean expansion, shear, and both principal
   limits. Any unresolved zero/sign locus remains explicitly open.
5. Production must cover at least 4,000 logarithmically distributed mixed and near-axis cases.
   Independent code may not import production or G341 implementation and must use a distinct
   curvature/Jacobi route on at least 2,000 cases.
6. Raw double-precision residual tolerance is `5e-9`; exact identities are required where
   available. Hostile mutations must catch at least: fixed-coordinate-time substituted for
   fixed-affine without proof, lost azimuth normalization, screen swap, curvature sign flip,
   off-diagonal injection, affine-normalization error, determinant absolute-value masking,
   principal-axis chart loss, quotient-path deletion, and promotion to luminosity/distance/scale.
7. Every script must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve evidence bytes in
   no-write mode.

## Premise and completeness gate

This is one exact-spacetime, one-observer-congruence, one-null-cone tile. The four-metric and all
directions are live; generic G332 developments, perturbed metrics, accelerated observers, nonlinear
congruence stability, physical branch population, matter, and radiative transfer are dropped and
remain capable of carrying additional structure. The computation characterizes every result; it
does not filter branches by expected behavior.

## Maximum conclusion

The maximum allowed landing is an exact, independently checked geometric Jacobi/area
classification on the supplied G341 spacetime and supplied labelled null branches. No result may be
called a luminosity prediction, physical distance, selected signal path, generic UDT spacetime,
physical scale, `X_max`, or canon.
