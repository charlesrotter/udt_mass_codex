# PE1 source-first reconstruction, sealed before candidate exposure

Source-first seal date: 2026-09-07. Baseline/context/exposure/resources are in
REVIEW_SCOPE.md. Main supplied only the relocated technical-note URL during this
stage; no candidate or main source conclusions were seen. Its bytes were
independently retrieved. This is an independent argument from shared primary
sources, not different-model review or independent flight-data processing.

## Documentary findings

1. The directly retrieved [ESA collection catalogue](https://earth.esa.int/eogateway/catalog/goce-level-1)
   identifies EGG_NOM_1b baseline `_0202`. Its collection DOI version 1.0 is a
   separate identifier. Cached [ESA item metadata](https://eocat.esa.int/eo-catalogue/collections/GOCE_Level_1/items/GO_CONS_EGG_NOM_1b_20091111T013534_20091111T030518_0202?httpAccept=text%2Fhtml)
   specifies EGG_NOM processor `07.00`, processing date 2019-02-06 15:36:26,
   PDS001, product suffix `_0202`. The direct item request timed out; therefore
   the processor value has weaker retrieval provenance than the catalogue
   baseline. One item's metadata does not prove all baseline items identical.
   No Level-2 RL06 identifier was substituted for an L1b version.

2. The directly retrieved [ESA technical note](https://earth.esa.int/eogateway/documents/d/earth-online/goce-level-1b-gravity-gradient-processing-algorithms)
   is ESA-EOPSM-GOCE-TN-3397, issue/revision 1.0, approved, dated 27/08/2018;
   physical PDF length 62 pages, printed pagination through 63. Section 1.1
   links its algorithms explicitly to the 2018 reprocessing. The old URL
   redirects to HTML search; this is a URL failure, not global unavailability.
   Sections 6–7 describe calibration application, outlier replacement and
   angular-rate filtering. Calibration matrices are supplied estimates;
   interpolation reference epochs can reflect observed data quality. The
   algorithm has quadratic terms, proxy angular acceleration, variable-length
   boundary filters and endpoint trend corrections. Final Algorithm 16
   computes each diagonal separately; no trace projection occurs there.

3. The [2019 calibration paper's public publisher page](https://link.springer.com/article/10.1007/s00190-019-01271-9)
   links its calibration method to the official 2018 reprocessing. Its abstract
   identifies star-tracker angular rates, a GRACE gravity model, equality of
   common-mode accelerations, and science plus shaking observations as inputs.
   Its Data Availability Statement says shaking-mode gradiometer data were not
   public and ESA access could be requested. That is a statement at publication,
   not a proved current universal access prohibition. Full article content was
   not retrieved; its present publisher page is a subscription preview.

4. The authors' [13 April 2018 presentation](https://presentations.copernicus.org/EGU2018/EGU2018-5319_presentation.pdf)
   slide 7 independently supplies the processing dependency diagram: nominal
   EGG_NOM_1b acceleration; AUX_ICM_1b calibration; STR_VC2/VC3 quaternions;
   AUX_NOM_1b temperature; AUX_EGG_DB geometry; SST_PSO_2 positions; and
   ITSG-Grace2014s. Slides 10–15 describe nonlinear observation equations,
   calibration intervals, and spectral weighting. This April presentation is
   earlier method context, not proof of every final August setting.

## Source-first challenge to possible conclusions

**Trace erasure is not established.** Summing Algorithm 16's displayed
diagonals gives, using its supplied arm-length conventions,

`tr(V) = -2*(a_d14x/Lx + a_d25y/Ly + a_d36z/Lz + wx^2 + wy^2 + wz^2)`.

For fixed angular-rate inputs, a change in a diagonal differential acceleration
changes this final-stage sum. This algebra defeats a claim that Algorithm 16
itself universally sets trace to zero. It does not show an arbitrary physical
scalar survives the preceding estimation. A nonzero released trace also would
not establish independent scalar sensitivity.

**An unused contrast is not established.** The actual scope must include the
calibration estimator and all its observation/support choices. Fixing delivered
coefficients after they were learned from the same observations does not make
those observations unused. Conversely, calibration reuse alone does not
invalidate every possible contrast: a justified joint model or an appropriately
separated design could account for it. Neither has been demonstrated here.

**A fixed linear P is not established.** The described processing has nonlinear
terms and data-dependent masking/calibration. Treating the complete processor
as TM2's fixed linear P needs an explicitly justified reduction: which controls
and masks are frozen, where a local linearization applies, and how its remainder
is bounded. This is an eligibility gap, not a proof that no useful reduction
exists.

**Named public L1b files alone do not close raw support.** A reviewable
confirmation split would need the calibration estimation intervals, exact
reference epochs and coefficients, nominal/science/shaking dependencies,
star-tracker/temperature/attitude support, flags and interpolation, filter
settings and segment endpoints. Calibration or filtering may share support
across nominal product intervals. File start/end times are not a proved
independence partition. Not all raw shaking samples are necessarily required
if sufficient trusted calibration-support and covariance records exist; that
alternative must be demonstrated, not assumed.

Maximum surviving result before candidate review: an identified baseline and
substantive versioned method dossier support a bounded dependency audit;
eligibility for an unused scalar constancy contrast remains OPEN pending its
estimation/support/error bridge. No physical adoption, flight-performance
verdict, universal product ineligibility or empirical inference follows.

## Checks and omissions

Direct public curl requests used 45-second time limits under the pre-read
capture utility. `retrieve_01` records sandbox DNS failure; `retrieve_02`
catalogue success; `retrieve_03` item timeout; `retrieve_04` old-note HTML
redirect; `retrieve_05` presentation PDF; `retrieve_06` current-note PDF.
`method_text_01` converts the note in temporary storage; `method_pages_01/02`
render only presentation slide 7 and printed technical-note page 61. These two
layouts were visually inspected. `check_01.stdout` records all retrieved-file
and inspected-page hashes. SHA-256 establishes byte correspondence only.

Tools observed: curl 7.81.0, Poppler pdftotext 22.02.0. Inspected note content:
title/contents; sections 1.1–1.3, 6.1–6.2, 7.2–7.4, tables 8–14, Algorithm 16;
targeted text matches for support/trace/version. No trace text match was found;
the final-stage conclusion rests on its equations, not absence of a word.
No calibration-estimator implementation, supplied coefficients, science/shaking
arrays, pipeline replay, sample covariance, observational interval or signal
injection was examined. Full core scientific premise audit belongs to main;
this reviewer did not independently rerun it. Search/abstract/result-prose
exposure is recorded in REVIEW_SCOPE.md and is not used as empirical evidence.

## Reproduction pointers and source hashes

Technical-note PDF SHA-256:
`3ba0639bd03adb2d9cbea49af6840991b0d2c7dfea67dc6d40eed2e0a47e935f`.
Catalogue HTML SHA-256:
`7a04e1079682d2fc98a02cc922815e9f51b3e9443571002783f17d49f1d51c1a`.
Presentation PDF SHA-256:
`ceb0d099b5a66321eeb037c879275711c62c4160ea9d8fc4908930b11ad0b053`.
Public PDFs and their page renders remain temporary, outside repository.
