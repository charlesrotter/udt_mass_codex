# Source ledger — complementary wave-observable campaign

Baseline grok9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd. Retrieved2026-09-07.
Hashes identify bytes, not truth, independent calibration, or historical flight
deployment. Only numerical/query metadata and our notes are preserved here;
the original third-party PDFs/header/pages remain temporary public-source cache
files. Fetch commands, HTTP statuses, errors and times are preserved in root
`*_fetch.json/.stdout/.stderr`. No strain arrays or parameter posteriors read.

## Controlling repository sources

| Source | SHA256 | Use and limit |
|---|---|---|
| G261 EXACT_DERIVATION.md |26897a999e6ad83e1f50c75ba76efe47e9c4c02edd896022a54a69810e57dc12|Working physical metric W4; not an instrument derivation. Later adoption controls its old dynamics-gap language.|
| G276 AUDIT_REPORT.md |cc66be850523fac561b411b32d7532069d838a6d6e6800568afd72f5560b862d|Proper-clock/c_E calibration distinction.|
| startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md |ebeae075307e7a325a840f4c2d9dcd973c18d9a3be21e6e6eccacce1ae8856f1|Owner-provisional bounded Einstein-vacuum premise, not metric-only derivation.|
| G313 EXACT_DERIVATION.md |7bf8dd3b081ff0d37ee23c8ea462abc451f9f4a3510283ea5e9ef87dd042b6bf|Ric=Lambda g arena and constant-profile Ricci-flat wave witness; no selected Weyl history.|
| G313 AUDIT_REPORT.md |b7df75cee891ed23dcf4796aba0a3d25e101ee89e4c1add95c8ef842987e418e|Scope and source caveats.|
| ORS SOURCE_LEDGER.md |7c1f34922e77c44bebae18ee47b9223ce3abcfc401bed2c17a6fe644eb1e46d0|Reuse prior clock/radio/wave survey; no repeated GOCE work.|
| ORS step01 candidate/review |91fd8ac38452f3449b3c1f85bb81f2988f2d73f2ad49b72bffb9fd983ca1992b /15158494b1da3e53a2c28f18d0de7987f78f92840dd87def27f44e90e4a9d898|Previous GW170814 sky/conditioning limits and supplied transfer assumptions.|
| LC2 FINAL_REVIEW.md |113fae20d9b203b4cad01b2e96e448937e5ca82ae1976800736ad2428605c488|Local stationary clock-gradient benchmark does not reconstruct full metric.|

Exact G261/G276/G313 package paths are supplied by the current exact registry;
ORS and LC are `udt_observational_route_selection_campaign_2026-09-07/` and
`udt_local_clock_metric_benchmark_campaign_2026-09-07/` respectively. The
349-row full startup premise audit is separately saved; no grades are changed.

## Primary public sources

1. [LAL detector construction](https://lscsoft.docs.ligo.org/lalsuite/lal/group___create_detector__c.html)
   documents Earth-fixed arm tensor D=(aa-bb)/2. Native cached response tensors
   can be single precision; this campaign instead contracts the published arm
   constants in float64. That does not improve the metrological input precision.
   Header: [official GitLab LALDetectors.h](https://git.ligo.org/lscsoft/lalsuite/-/raw/master/lal/lib/tools/LALDetectors.h),
   SHA82ac49e8042d4eab0f890e63e3599ae227967aee16c76cd5f6b6b729c8798684.
   H1/L1/V1 vertex, unit-arm and arm-MIDPOINT constants; midpoint is half the
   declared arm length. Retrieved master snapshot, not certified2017 processor.
   [LIGO survey catalogue T980044](https://dcc.ligo.org/T980044/public) gives a
   provenance pointer; its survey PDF was not needed or read for the calculation.
2. [Swope discovery circular GCN21529](https://gcn.nasa.gov/circulars/21529),
   cached text SHAfacff054809d017d2d411dd9ee48ff89f4bd210a192454cf8d120d98dc89aede.
   Nominal13:09:48.089, -23:22:53.35. Optical follow-up was triggered by GW
   localization, initially a potential association. Coordinate error/frame is
   not established by this circular alone; the nominal ICRS interpretation and
   stress offsets are explicit design choices, not precision astrometric data.
3. [GW170817 tests paper](https://dcc.ligo.org/public/0150/P1800059/008/main.pdf),
   SHAd86fc8bc15abdac47b75960218aefd247f7adeddc00237e9c329b492962584b7.
   Polarization section uses the optical counterpart position and GR waveform
   phase, comparing pure tensor/vector/scalar families. Its published odds do
   not certify an arbitrary-waveform null contrast or exclude all mixtures.
4. [Original GW170817 release](https://gwosc.org/events/GW170817/),
   SHA3053c37d5d0b1f8d1ad6423e4ca237449bd687e0eb786c24b12fcf19d91aa288.
   GPS1187008882.43; original2048s CLN and pre-clean products are distinct.
   Noise subtraction, L1 glitch, data-quality exclusions and H1 end-window
   corruption are disclosed. Virgo had low coupling/sensitivity for this event.
   [Original special frames P1700349](https://dcc.ligo.org/P1700349/public)
   identify H/L C00 special cleaned channels and V1O2Repro1A. DO NOT transfer
   C02 uncertainty estimates silently to these original special C00 files.
5. [GWTC-1 GW170817 v3](https://gwosc.org/eventapi/html/GWTC-1-confident/GW170817/v3/),
   [metadata JSON](https://gwosc.org/eventapi/json/GWTC-1-confident/GW170817/v3/),
   SHA2cd7e903b895f5d3a406383362172a411b127efdcf9be65590a8234b9352ddcb.
   Catalog release includes the L1 glitch; not identical to original CLN.
   Provides32s/4096s strain links. Source-fit posterior quantities in its
   metadata were not used as new metric/waveform inputs.
6. [O2 release details](https://gwosc.org/o2_details/),
   SHA3ee0ff6cc0fd87d02b160dfc272c301913649f0c538d7c02d1e2853934cc2ab6.
   H1/L1 DCH-CLEAN_STRAIN_C02; V1 Hrec_hoft_V1O2Repro2A_16384Hz. Public strain
   with witness-noise subtraction, quality/injection masks and calibration
   pointers. This matched archival route is preferable for a proposed early-
   inspiral contrast, subject to actual file headers/time coverage later.
   Calibration valid10–5000Hz;4kHz anti-aliasing limits analysis above~1700Hz.
7. [Calibration uncertainty T2100313 v3](https://dcc.ligo.org/T2100313/public),
   [README](https://dcc.ligo.org/public/0177/T2100313/003/README),
   SHAfb4650601da797badc8bf9e068f798788842667a5bc27ae035ae5ffd0d311d7e.
   O2 H/L C02 hourly frequency-dependent complex response-error estimates;
   Virgo one O2 run file. Median and +/-1sigma columns, not deterministic
   bounds or a joint channel/frequency covariance. C00 lacks well-established
   uncertainty in this release. Archives located, not downloaded/validated.
8. [Astropy IERS](https://docs.astropy.org/en/stable/utils/iers.html) and
   [ERFA c2t06a](https://github.com/liberfa/erfa/blob/master/src/c2t06a.c)
   supply conventional coordinate/time methods, not UDT premises. Offline
   bundled IERS-B and IAU2006/2000A rotation are adequate declared finite-design
   inputs; version/hash and actual interpolated parameters belong in CO2 output.
   GCRS-to-ITRS rotation is not a complete optical observation model or an
   astrometric uncertainty certificate. Barycentric/geocentric direction
   differences and precise signal-transfer corrections remain controlled later.

The metadata batch returned five200 statuses with nonempty parseable records;
its last-command exit0 alone was not used to infer all transfers succeeded.
Failed404 generated LAL header URL and nonexistent GitHub mirror are preserved
in `detector_constants_fetch.*` and `detector_constants_mirror_fetch.*`.
The official GitLab source succeeded; no repeated failing search is needed.
Two focused search batches were sufficient; subsequent opens were exact source
verification. No comprehensive documentation or release-eligibility claim.
