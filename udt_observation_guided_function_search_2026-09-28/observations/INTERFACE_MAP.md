# Complementary observation map — draft

Parent source assessment, 2026-09-28. Source snapshots/hashes and fetch records
are in SOURCE_DOWNLOAD.json and sources/. No newly analysed quasar light curves
or galaxy catalog is claimed. These interfaces remain conditional; the geometry
is not selected by using a conventional interpretation for a comparison.

| Source class | Useful observable/inference | Contribution to this campaign | Required distinction |
|---|---|---|---|
| Type Ia supernovae | Redshift, calibrated multiband brightness and duration | Data lane reconstructs six explicit relative-distance shape controls and validates them with a covariance-aware object split | Standardization/selection/transfer and motion corrections remain supplied; the free magnitude intercept leaves absolute scale open |
| Galaxy and quasar clustering | Anisotropic BAO likelihood for D_M/r_d and D_H/r_d | Parent freezes the conditional F_AP=exp(x)F/F' cross-probe comparison of the same SNe shapes, without refitting them | Comoving ruler and fiducial clustering templates remain external interfaces; this is not raw physical distance or a selected UDT galaxy model |
| Quasar variability | Source-model-dependent duration or short-term volatility against redshift | Methods and uncertainty constraints; no new numerical fit in this campaign | Intrinsic source variability/evolution, luminosity, wavelength, cadence and stochastic inference cannot be silently replaced by a universal clock |

## Galaxy/clustering interface

The [official DESI product description](https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html)
links the released BAO likelihood, separately from cosmological posterior chains.
The [DR2 analysis](https://arxiv.org/html/2503.14738v3) fits shifted correlation
templates and describes reconstruction and fiducial-model systematics. Its
uncalibrated-ruler treatment supports dimensionless geometric comparisons
without specifying a numerical sound horizon. It does not establish that the
same compressed likelihood applies unchanged to arbitrary UDT spacetimes.

Our proposed F_AP test uses a supplied spatially flat homogeneous conformal
class and the conventional comoving-ruler interface. In that class the SNe
shape supplies an area/derivative ratio; no fitted BAO correction or new length
scale is needed. BAO_COMPARISON_FREEZE.md owns exact outcome/exposure/statistic
choices. A mismatch would concern the stated shape plus comparison assumptions;
agreement would concern their consistency, not native UDT selection.

## Quasar interface

The [source-dependence study](https://arxiv.org/html/2501.04171v2) models inferred
variability timescales using rest wavelength, bolometric luminosity, scatter
and optional evolution. It supplies a useful route to testing received-duration
behavior with source assumptions exposed. These are inferred stochastic
timescales, not individually synchronized emitted/received clock ticks; their
luminosity/distance attachments also need tracing in a UDT application.

The [2026 variability study](https://arxiv.org/html/2606.01496v1) finds that fixing
the light-curve mean can understate timescale uncertainty, and advocates a
short-term volatility statistic that is better constrained in its analysis.
Its redshift dependence also involves source evolution. Consequently this
campaign does not treat published quasar durations as a clean independent
distance curve or refit their summaries with negligible source uncertainty.
This is a reason to carry the correct measurement likelihood into a later
specific test, not to exclude quasars from discovery.

## Which functions can these observations select?

Inference: a supplied received-clock function already links spectral shifting
and differential tick dilation. A finite-source duration adds information only
after its emission history, wavelength selection and duration variation are
handled. BAO can add a geometric derivative constraint under its interface.
Neither, by itself, selects a response equation, a source law or the farthest
asymptotic completion. The SNe data lane, conditional geometric inversion and
separately frozen BAO comparison together make those dependencies explicit.
