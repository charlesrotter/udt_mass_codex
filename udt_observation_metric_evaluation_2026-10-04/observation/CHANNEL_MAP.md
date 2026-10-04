# OEV1 observation map — exposed research candidate

Scope: three channels and eight primary papers/releases, accessed 2026-10-04.
This is the observation researcher's source map, not a fresh adversarial review
or native UDT admission. `../WORK_ORDER.md` and the PRT1 handoff control scope;
`SOURCE_LEDGER.json` pins sources and `EXPOSURE.md` records exposure and limits.

The recommended immediate product is **all six megamaser distance/redshift
summary constraints, with their imported disk/readout assumptions attached**.
It is executable as a published-data conversion diagnostic. There is presently
no specified native metric/readout candidate to confront with those numbers.

The ranking below prioritizes independent distance provenance, then how directly
the readout identifies clock/null geometry and how explicitly its nuisance
assumptions can be carried. It does not rank expected agreement with UDT, and
is not an exhaustive ranking of astronomy. Drift ranks above supernova widths
for readout identification, despite substantially weaker current sensitivity.

| Rank/channel | Actual observable and independent geometry | Source/observer histories and readout | Error, selection, and operational status |
|---|---|---|---|
| 1. Megamaser angular-size distance plus systemic redshift | Angular locations, line frequencies and their monitored changes inform a disk fit returning angular-size distance and systemic redshift. Distance is not obtained by substituting redshift into a cosmology. | Accelerating masing gas orbits a central object; Earth-based observations are frame-corrected. Systemic redshift is inferred after disk-motion/gravity treatment. These are not PSW parallel-prepared clocks or measured initial proper separations. | Six summaries available in M1. Small sample selected for suitable detectable disks; posterior/model correlations remain. Table 1 is suitable for marginal readout conversion, not a reconstructed joint likelihood. |
| 2. Direct spectroscopic drift | Repeated absorption spectra yield frequency/velocity shifts versus reception time. No independent distance is supplied or needed for that narrower derivative. | Absorbing gas against a background radio/quasar source, changing observer motion, line blends and instrumental wavelength stability enter. Stable transition identification is conditional. This is reception-time drift, not a separation derivative. | R1 gives radio limits; R3 supplies the newer optical three-epoch result. Published summaries are available; raw-spectrum reanalysis is outside this task. Earlier and newer optical estimates share epochs. |
| 3. Supernova received-time stretching | Observer dates, fluxes in filters, and redshifts constrain light-curve widths. There is no independent geometric distance in this channel. | Width is a source-population comparison, not a recurring proper clock on one emitter. Intrinsic evolution, wavelength matching, classification and peak estimation must be controlled. | S1 reports 1504 accepted objects and a tight conditional exponent. S2 exposes the photometry schema; S3 contains analysis products. Shared reference curves and repeated bands preclude treating every width as independent. |

## Megamaser source fields and the exact distinction being retained

[M1, Pesce et al. 2020, arXiv:2001.09213v2](https://arxiv.org/pdf/2001.09213v2),
printed/PDF page 4, Table 1 and its note, is the sole input for the proposed
six-row diagnostic. Local bytes: `primary/M1_Pesce_2001.09213v2.pdf`, SHA-256
`c9f2d2b626fee60d77928856d217a2cbe546f06c69cd9e7ac804f4ab652e731a`.
The table was read from PDF text and cross-checked against a rendered
page. These are direct transcriptions, without transformations:

| Galaxy | D median (Mpc) | D lower error (Mpc) | D upper error (Mpc) | optical v, CMB frame (km/s) | quoted v error (km/s) |
|---|---:|---:|---:|---:|---:|
| UGC 3789 | 51.5 | 4.0 | 4.5 | 3319.9 | 0.8 |
| NGC 6264 | 132.1 | 17 | 21 | 10192.6 | 0.8 |
| NGC 6323 | 109.4 | 23 | 34 | 7801.5 | 1.5 |
| NGC 5765b | 112.2 | 5.1 | 5.4 | 8525.7 | 0.7 |
| CGCG 074-064 | 87.6 | 7.2 | 7.9 | 7172.2 | 1.9 |
| NGC 4258 | 7.58 | 0.11 | 0.11 | 679.3 | 0.4 |

M1 reports posterior medians and 16th–84th-percentile intervals; NGC 4258's
distance error additionally combines statistical and systematic terms in
quadrature. The velocities use the optical convention in the CMB frame.
They are neither raw detector velocities nor peculiar-motion-subtracted flow
velocities. M1's subsequent H0/flat-Lambda-CDM inference is a separate stage
and is excluded. Error floors and priors enter the source distance fit
(M1 section 2, pp. 2–3); Table 1 does not furnish a joint D–redshift covariance
or a cross-galaxy systematic covariance.

[M2, Pesce et al. 2020, arXiv:2001.04581v1](https://arxiv.org/pdf/2001.04581v1)
makes the source bridge explicit: inverse-square acceleration and Keplerian
speed (Appendix A, A7/A10), relativistic Doppler and Schwarzschild gravitational
redshift (A12–A15), then optical `v=c z` (A16). Its CGCG disk model includes
warping/orbit choices and correlated D–mass inference (section 4; Figure 4).
These are imported observational modeling assumptions, not native UDT laws.

M2 Table 4 (p. 7) advertises machine-readable spot type, barycentric optical
velocity, flux/error, x/y angular positions/errors, acceleration/error and an
acceleration-measured flag. Flag 0 means modeled, not an independent measured
acceleration. Table 5 (p. 11) gives fitted D and barycentric systemic velocity;
the stated CMB conversion adds 263.3 km/s. The flow-model velocity used for
M2's H0 stage must not replace M1's systemic value. The full spot table is
advertised through the [publisher article](https://doi.org/10.3847/1538-4357/ab6bcd);
its downloadable attachment was not fetched or verified here.

Our inference from this source structure: independence from a redshift-distance
cosmology does **not** establish independence from source dynamics, or statistical
independence of D and z. A comparison at better precision must recover the
joint disk posterior/likelihood and instrument/model nuisance information.
Marginal intervals are insufficient to invent those missing dependencies.
Neither D nor systemic z identifies an actual two-free-clock preparation.

## Drift and width constraints that can be carried only with their scope

[R1, Darling 2012](https://arxiv.org/pdf/1211.4585v1), Table 1 (p. 3), provides
barycentric mean absorption redshift, component/epoch counts, last MJD,
baseline, redshift drift and spectroscopic velocity-drift errors. Sections 2–4
describe digital-epoch selection, Gaussian component fits, variability and
observer/absorber acceleration. The reported ensemble velocity drift is
`-5.5 +/- 2.2 m/s/yr`; **2.2 is its quoted uncertainty, not an absolute
zero-centered bound**. Its formal offset must not be silently zeroed. The
single-object 3C286 value is `2.8 +/- 8.4 m/s/yr`. No native inference follows
from either number.

[R2, Trost et al. 2025](https://arxiv.org/pdf/2505.21615v1), sections 2, 5–7,
reports the first two-epoch ESPRESSO result on the SB2 Ly-alpha forest.
[R3, Trost et al. 2026](https://arxiv.org/pdf/2603.02318v1), sections 2–5,
extends that same sightline to three epochs: its pixel method gives
`-3.43 +/- 3.56 m/s/yr`, and likelihood method `-3.63 +/- 3.65 m/s/yr`
(p. 5). They share spectra and a spline model, and are not independent
observational confirmations. R3 changes R2's weighting because it underestimated
uncertainty (section 4.3). Thus the older estimate must not be combined as an
independent datum.

R3 Table 1 records dates/exposure information; barycentric correction,
FP+ThAr/LFC comparisons, masks and simulation-calibrated forest modeling remain
part of the readout. The sky source's emission redshift is not the absorber
redshift of every pixel. A model for absorption histories and nuisance
accelerations is needed before attributing a drift solely to geometry.
Published program identifiers and observation metadata are available, but no
raw spectral archive or independently complete pixel covariance was retrieved.
R1 and R3 may motivate different redshift-regime constraints; this map does not
assume a common drift across those regimes.

[S1, White et al. 2024](https://arxiv.org/pdf/2406.05050v2), pp. 1–4, 10–12,
reports `b=1.003 +/-0.005 (stat) +/-0.010 (sys)` for
`Delta t_obs=Delta t_em(1+z)^b`. Its population-duration assumption matters.
The first method varies time scaling directly and provides separate flux-scatter
evidence near b=1 under source-population assumptions. The tight quoted b value
comes from the second width-reference method, which begins by dividing reference
times by `(1+z)`. On p2 the authors explicitly classify that second method as a
consistency check; its tight estimate is not an assumption-free independent
confirmation. SALT3 supplies peak normalization/time;
classification, flux-error/count/convergence cuts select the analyzed set.
Appendix A considers source-population drift. This is useful evidence about
received temporal width under that readout, not a geometric distance or native
metric selection. Same-event bands and shared reference populations require
covariance treatment in any independent reanalysis.

[S2, DES-SN5YR release](https://zenodo.org/records/12720778) pins DOI
`10.5281/zenodo.12720778`; its listed archive is `DES-SN5YR-1.2.zip`, 1.5 GB
(not downloaded). The [official schema](https://des-sn-dr.readthedocs.io/en/latest/0_DATA.html)
defines HEAD fields `SNID`, `RA/DEC`, `REDSHIFT_HELIO[_ERR]`,
`REDSHIFT_FINAL[_ERR]`, `VPEC_[ERR]`, and host redshifts. FINAL is CMB without
peculiar-velocity correction. PHOT supplies `MJD`, `BAND`, `FLUXCAL`,
`FLUXCALERR`, flags and image identifiers. Redshift provenance must be checked
per object: the generic best-redshift field permits photometric values.

[S3, author analysis release](https://github.com/ryanwhite1/DES-Time-Dilation/tree/8ebec41f9a4c82dbccd0eaea700ac4ba91e5baca)
is pinned at `8ebec41f9a4c82dbccd0eaea700ac4ba91e5baca`. It lists per-band
pickled width/analysis products plus `StretchMethod.py`, `Methods.py`, and
`Plot_Generation.py`. Underlying photometry is obtained separately. No pickle
was deserialized, no analysis code executed, and no full covariance product
was verified. Its commit predates S1 v2; exact final-paper correspondence is
unverified and would be a replay gate.

## Narrowed executable proposal for the parent freeze

The parent accepted this scope, not a physical interpretation. **No conversion
program or fit was run by this researcher.** The parent owns the operative
freeze and execution. Proposed question: what marginal angular-distance and
frame-labeled spectral-ratio summaries do all six published rows imply under
the stated optical velocity convention?

Use M1's six rows without outcome exclusions, with original asymmetric distance
errors intact. Freeze the bookkeeping constant `c_E=299792.458 km/s` as an
observational unit calibration, not a selected UDT scale. Deterministically
map `z_CMB=v_opt,CMB/c_E`, `Z_CMB=1+z_CMB`, and optionally `log Z_CMB`.
Map each quoted velocity interval endpoint through the same monotonic functions;
do not replace the distance asymmetry by a symmetric Gaussian. Preserve
NGC 4258's distinct error convention. Retain the frame label on every output.
An endpoint transformation preserves a marginal interval's meaning; it does
not create a simultaneous confidence region.

No slope, H0, FLRW distance law, peculiar-flow subtraction, disk refit, source
evolution fit, joint significance, or curve selection enters this diagnostic.
Decision: pass only transcription/unit/interval/roundtrip checks; any mismatch
is a processing defect to repair. There is no UDT pass/fail hypothesis here.
Published values are exposed exploratory constraints, not held-out confirmation.
This small CPU-only diagnostic needs no GPU or new observational download.

The family later eligible for confrontation is any explicitly declared metric
candidate **plus** source/detector clocks, actual null branch, motion/gravity
readout and nuisance distribution that predicts these very quantities. It is
currently unspecified. Its missing bridges are native metric evolution/admission,
source clock/transition identification, emission/reception histories, angular
distance transport, and justified source-dynamics recalibration or import.
The CMB conversion also requires a specified comparison frame; it is not a
native preferred frame supplied by this table.

One may preserve the marginal observable constraints while these joins remain
open. One cannot infer the complete event/path-to-depth assignment, local
slowing sign, PSW coefficients, X_max, a large-distance pole, or native dynamics.
The PRT1 flat/quadratic/cubic controls remain evaluator controls and supply none
of those missing astronomical bridges. No future observation split is declared
held out; new confirmation would require a separately frozen candidate/readout
and an actually unexposed dataset.
