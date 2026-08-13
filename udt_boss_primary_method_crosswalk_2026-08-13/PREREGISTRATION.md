# BOSS primary-researcher method crosswalk — preregistration

Date: 2026-08-13
Status: `PREREGISTERED__PRIMARY_PUBLICATIONS_NOT_OPENED__R3_OUTCOMES_CLOSED`

## Whole question

Do the frozen R0--R2 BOSS DR12 observer-coordinate inputs and measurement rules agree with the
catalog, mask, weighting, random-catalog, cap, and estimator semantics documented by the BOSS
collaboration and the original researchers?

This is a method/provenance cross-check run in parallel with R3. It does not ask whether a BOSS
acoustic interpretation is correct, whether R2 contains a preferred feature, or whether UDT fits
the data.

## Bounded local object

The local side is frozen to:

- the eight hash-pinned DR12v5 pre-reconstruction LOWZ/CMASS North/South data and random files in
  `../udt_observed_angular_pattern_raw_restart_2026-08-12/DATA_MANIFEST.tsv`;
- observed `RA`, `DEC`, and `Z` only for locations;
- the frozen LOWZ/CMASS redshift envelopes and exact shell unions;
- all four retained data-weight lanes and unity random weights;
- deterministic `5x`, `10x`, and `20x` subsets of the official random catalogs;
- normalized angular Landy--Szalay pair counts on the frozen angular grid;
- the completed R0--R2 evidence only.

R3 covariance arrays, ranks, scales, curves, and feature descriptors remain sealed until R3 and its
independent verifier complete. This crosswalk may inspect only R3 service health and completion.

## Primary-source universe

After this preregistration is committed, the audit may open only:

1. official SDSS/BOSS release and large-scale-structure catalog documentation;
2. original BOSS collaboration catalog-construction, target-selection, observational-systematics,
   and clustering-method papers;
3. original method papers when BOSS explicitly relies on them.

Secondary summaries, review articles, blog posts, and repository interpretations cannot own a
comparison result. Search results may locate a source but cannot supply evidence.

## Lawful comparison layers

The following may be checked directly when the source and local object have the same type:

- release, file, sample, and Galactic-cap identity;
- row counts before and after an exactly matching published cut;
- catalog-field definitions;
- veto/mask/completeness ownership already encoded in the released products;
- data-weight formulas and the intended role of each factor;
- random-catalog construction, footprint role, and any stated oversampling;
- Landy--Szalay formula and pair-count normalization;
- any published raw angular correlation vector only if its catalog, redshift selection, cap,
  weights, estimator, angle convention, bin edges, and corrections match the local query.

The following may be recorded only as labeled context or `NONCOMPARABLE_MODEL_TRANSFORM`:

- fiducial-cosmology coordinates;
- comoving separations or wavenumbers;
- `D_M`, `D_H`, `D_V`, `r_d`, dilation parameters, or acoustic scales;
- reconstruction, BAO templates, damping models, broadband subtraction, or peak fitting;
- mock-calibrated covariance, significance, or physical interpretation;
- any published feature location transformed through the above machinery.

These quarantined quantities may not tune a local selection, bin, weight, random subset,
covariance, descriptor, feature location, tolerance, or conclusion.

## Comparison procedure

1. Record every primary source, exact claim location, and mathematical object type.
2. Type-match the source object to the frozen local object before comparing a number.
3. Mark every field `DIRECTLY_COMPARABLE`, `COMPARABLE_WITH_DECLARED_TRANSFORM`,
   `NONCOMPARABLE_MODEL_TRANSFORM`, `DOCUMENTATION_ONLY`, or `UNRESOLVED`.
4. Independently reproduce any load-bearing finite comparison from the frozen local artifacts.
5. Report mismatches before proposing any repair. No local rule changes during this audit.

## Premise and choice ledger

- Official released files and their measured contents: `OBSERVED`.
- Collaboration statements about their construction and intended field roles: `OBSERVED_SOURCE`.
- Use of pre-reconstruction DR12v5 files: `CHOSE`, pinned before R0.
- Observer-coordinate shell and angle grids: `CHOSE`, frozen before R2.
- Four weight lanes: `CHOSE__FREE_AND_EXPLORED`.
- Landy--Szalay: `CHOSE__BORROWED_METHOD`, not UDT physics.
- Published cosmological conversions: `COMPARISON_ONLY__QUARANTINED`.
- UDT interpretation, feature selection, and `X_max`: `OPEN__OUT_OF_SCOPE`.

## Preregistered landings

- `METHOD_AND_INPUT_CONSISTENT`
- `DIRECT_OBSERVABLE_CONSISTENT_WITH_CAVEATS`
- `NONCOMPARABLE_MODEL_TRANSFORM`
- `PIPELINE_MISMATCH_REQUIRES_AUDIT`
- `PUBLICATION_DOCUMENTATION_INSUFFICIENT`

More than one landing may apply to different rows. A model-transformed publication result is not a
failure of the raw pipeline; it is simply not a direct cross-check.

## Falsification and stop rules

The audit must return `PIPELINE_MISMATCH_REQUIRES_AUDIT` for the affected layer if a primary source
shows that the local pipeline misstates a released field, applies a catalog weight contrary to its
defined role, omits a required released mask/veto not already encoded by the files/randoms, uses an
incorrect estimator normalization, or compares numerically unequal objects as though they were the
same query.

It must stop a numerical result comparison if any of catalog lineage, selection, weights, binning,
correction state, or coordinate type cannot be matched exactly. It may not weaken the type match
after seeing agreement or disagreement.

## Certification ceiling

Maximum conclusion:

> The frozen R0--R2 pipeline is methodologically consistent, inconsistent in a stated layer, or not
> directly comparable to the primary BOSS publication object under the preregistered type rules.

This audit cannot detect BAO, validate UDT, select an angular feature, establish covariance or
significance, infer a physical scale, or determine `X_max`.
