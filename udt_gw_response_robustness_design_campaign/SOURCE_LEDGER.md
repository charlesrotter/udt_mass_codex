# RD1 source and uncertainty ownership

Repository baseline291bbd73584318f87697345cd86c48f17064e5de. This map is not
scientific evidence by itself; named sources and exact review pins own scope.
Full fresh349 audit passed; STARTUP_PREMISE_AUDIT.json SHA
dc7e791fa60c6f5a83df35b90d99453b2c882873615ddd9decdd0edf5149a2c5.

## Admitted geometry and reviewed dependencies

- G261 EXACT_DERIVATION sections1–3: W4 physical-metric coupling remains
  WORKING/POSIT_NOT_CANON. It is not an instrument, source or response equation.
- G312 later owner ADOPTION_RECORD in
  startup_surface_g312_two_premise_adoption_refresh_2026-09-01/: quiet-GR/Local
  Metric Sufficiency are provisional adopted premises, not metric derivations.
- G313 EXACT_DERIVATION sections1/5/6 in
  udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/: bounded
  Ric=Lambda g arena, Ricci-flat wave witness and no selected absolute scale.
- CO1 candidate c5dd7945858f287845ebfbf6f38e0bdf9bc929e66463abd8b08105959a3d7ad0
  and final review31c578ab9a26beb1e762c4c994c8c92291ed6300c4ae11149a737cdb63cbb11f
  in udt_complementary_wave_observable_campaign_2026-09-07/step_01/:
  conditional arbitrary-wave geometry, weak TT tide, supplied instrument map,
  rank/null/covariance/error identities; no full physical response certificate.
- CO2 same campaign/step_02: candidate
  bd06415b173dc2a0b32f05f5beb6cdb0cd3ab3a0e08ad0a055bf7653f4f4c087;
  design_run.stdout b89c8e432788842cdbddc1270c3135043e60f12c557cb24725d2162560fdfac2.
  Static nominal geometry/rank/conditioning, not precise actual response.
- FW1/FW2 in udt_gw170817_fixed_window_test_campaign_2026-09-07/:
  R1 freeze fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324;
  FW1 final review36f44b423cf498c33cb214b1748a7e73b550c6328da82871741717e9721f26b2;
  FW2 final review37485eeaeb63bc3ddf0654d19a1f79215307c2f165d43481f522ae96e2770f79.
  These retain the exact finite cyclic/static scope, actual33 exposed records,
  failed target screen, inclusive-bin repair and no event inspection. They
  do not certify rotating/finite-arm/upstream physical response or confidence.

## Reused primary sources; no repeated retrieval

Cached T2100313v3 calibration README:
/tmp/udt-complementary-wave-sources-C72KZ2/calibration_README.txt,
SHAfb4650601da797badc8bf9e068f798788842667a5bc27ae035ae5ffd0d311d7e.
https://dcc.ligo.org/public/0177/T2100313/003/README .
Hourly discrete H/L true/model ratios and run-wide Virgo estimates have
pointwise median and +/-1sigma boundaries, not joint hard bounds. Their inverse
is the uncorrected released/true response convention. A confidence treatment
needs its declared probabilistic assumptions, not a hard-envelope relabeling.

Cached O2 subtraction paper1809.05348v2, text
/tmp/udt-gw170817-fixed-window-xshnIR/noise_subtraction.txt,
SHAab7cab0c255f4fd8a30d462fb0277e44d21bbbaf66dda45a1e7ae9a155ace750.
https://arxiv.org/abs/1809.05348 . Sections2,4.1,4.2,4.4,4.5 read directly.
Transfer estimates depend on strain/witness data; safety and finite signal/
calibration-line tests support intended use, not uniform arbitrary-waveform
retention. Transient gating and narrow oversubtraction caveats are explicit.
Treating full cleaning as a fixed linear operator is an additional modeling
approximation unless a suitable error relation is justified on the class.

CO2 published detector constants remain in
/tmp/udt-complementary-wave-sources-C72KZ2/LALDetectors_gitlab.h,
SHA82ac49e8042d4eab0f890e63e3599ae227967aee16c76cd5f6b6b729c8798684.
No metrology improvement is inferred from floating precision or exact decimals.

## New, narrowly targeted official response definitions

Retrieved2026-09-08 into /tmp/udt-gw-response-docs-L3JgrF/; commands/status/
byte counts and failures saved in *_fetch*.json/stdout/stderr. No strain.

1. DetResponse.c, official master snapshot:
   https://git.ligo.org/lscsoft/lalsuite/-/raw/master/lal/lib/tools/DetResponse.c
   SHA2e1d5db56170607e655a866165905b5867d537200e90dceb77c81f8832259a40.
   Lines185–211 and response-parts construction read. Exact complex arm
   transfer and separate arm weights, with the mean-arm approximation disclosed.
2. LALSimulation.c, official master snapshot:
   https://git.ligo.org/lscsoft/lalsuite/-/raw/master/lalsimulation/lib/LALSimulation.c
   SHAa10f73a39029b86d4de7c46c11ad269b0ee17a9499dce52b9b42a0bbeb1cb619.
   Lines158–250 and943–1073 read: finite-frequency convention, temporal
   interpolation/padding, midpoint response approximation and error warnings.
   The actual caller uses beta=f*L/c; DetResponse multiplies by pi and uses
   normalized sinc. Its nearby beta comment is inconsistent with that caller.
   This is resolved here by reading both definitions, not a flight-data bug
   claim and not a request to repair external or accepted code. Installed
   /usr/include/gsl/gsl_sf_trig.h lines82--87 was read directly and explicitly
   confirms Sinc(x)=sin(pi x)/(pi x), resolving the implementation convention.

These are public mathematical instrument-model definitions, not certification
of the2017 deployed pipeline. Response-model existence differs from a bound
on residual calibration/cleaning/astrometry errors. Common and differential
response errors must be separated before applying an error budget.

Search history: one guessed official source-page URL returned404, one bounded
search located the official DetResponse API; a second convention/caller search
added no usable caller. DCC T070172 open returned a non-retryable tool error.
Direct GitLab DetResponse retrieval needed network escalation after DNS failure.
The guessed LALSimDetectorStrain.c filename returned404; the LALSimulation.c
source succeeded and resolved the caller. Preserve failures; no further search
is needed for these definitions. No exhaustive documentation claim or GOCE work.
New successful primary-source downloads total103447bytes (21195+82252), below
the50MiB limit. Failed retrievals added no primary-source payload. No raw
strain was downloaded or opened.
