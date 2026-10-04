<a id="r8oev"></a>

#### Observational constraints and finite metric evaluation — OEV1

Charles authorized PRT1's steps 4 and 5. **The return is a source-conditional
observational constraint table and a checked supplied-metric evaluator; native
geometry selection remains open.** Step 4A assessed three channels. Step 4B
returned the permitted narrowed observable constraints because no astronomical
metric/query/readout candidate was specified for a likelihood. Step 5A ran the
finite evaluator. Step 5B did not acquire native evolution equations from it.
The open field law does not prevent observation design or testing a subsequently
declared candidate; an evaluator pass does not identify that candidate.

**What observations actually constrain.** Eight primary papers/releases support
the [source map](udt_observation_metric_evaluation_2026-10-04/observation/CHANNEL_MAP.md)
and its versioned ledger. Ranking concerns independent distance provenance and
identifiable readouts, not expected agreement with UDT or all of astronomy.

| Channel | Usable quantity | Retained inference limit |
|---|---|---|
| Megamaser disk observations | Conditional angular-size distance and frame-labeled systemic spectral shift | Distance avoids a redshift-distance cosmology but retains source dynamics, gravity, disk geometry, calibration and posterior correlations; not PSW initial proper L. |
| Direct spectroscopic drift | Change of identified spectral features over reception time | Calibration, absorber history and nuisance acceleration remain; drift is not separation variation or a curvature sign by itself. |
| Supernova temporal widths | Received time-profile comparison under a source-population relation | No independent geometric distance; source diversity, wavelength matching, selection and shared reference curves remain. |

The selected published-data diagnostic uses all six rows of MCP XIII Table 1,
[Pesce et al. 2020, v2, p4](https://arxiv.org/pdf/2001.09213v2).
Reported distance medians span 7.58–132.1 Mpc. With the source's CMB-frame
optical convention v=c_E z and observed unit calibration c_E=299792.458 km/s,
the median z values span 0.0022659009–0.0339988540. The saved
[constraint table](udt_observation_metric_evaluation_2026-10-04/observation/MCP_CONSTRAINTS.tsv)
keeps the asymmetric distance marginal intervals and maps each velocity marginal
monotonically through z=v/c_E and ell=log(1+z). NGC4258 retains its separately
combined statistical/systematic distance uncertainty. The quoted source errors
do not create a joint confidence region, likelihood or zero covariance.

These are processed spectral proxies, not local recession speeds, unreduced
detector-clock ratios or isolated positional slowing. The companion disk model
uses inverse-square/Keplerian dynamics, relativistic Doppler and gravitational
corrections before systemic redshift; those are labeled conventional source-
readout assumptions, not native UDT equations. The later H0/FLRW stage is not
used. No peculiar-flow correction, slope, preferred scale or D_A-to-L conversion
is fit. A CMB reduction frame is a comparison convention, not a native preferred
observer. R13's area identities alone do not supply a source luminosity model.

The other sources retain useful positive evidence and their actual limitations.
Darling2012's 2.2 m/s/yr is an uncertainty around the reported -5.5, not an
absolute zero-centered bound. The newer ESPRESSO results share observations
with the earlier analysis and revise its weighting; they are not independent
confirmations. White2024's first free-exponent flux-scatter method supplies
separate source-conditional temporal evidence. Its tight second-method exponent
uses reference times divided by(1+z), and the authors explicitly call that
method a consistency check. The preserved source-precision repair attaches
that scope to the number without discarding the first method or the whole study.
None of these channels automatically supplies the prepared query of R8PRT.

The diagnostic rules were frozen before parent table extraction; the researcher
had already seen published outcomes. Exact input/code were frozen before the
conversion. This is exploratory source reuse, not held-out confirmation. A fresh
reviewer visually checked the primary table and independently replayed sixty
converted numeric fields using 60-digit Decimal arithmetic; differences are
ordinary floating representation error, with log differences below 1e-17.
That verifies transcription/conversion, not the source disk fit or astrophysics.

**Original-equation evaluation on declared controls.** Use the supplied metrics
g=-dt^2+a(t)^2 sum dx_i^2, with a=1,1+t^2,1+t^3 on unquotiented R^3; the cubic
time domain is t>-1, and the other two have t in R. Each k=1 or b=1 is a
separate control-unit normalization, not a physical scale. Restrict to the
invariant radial slice with zero transverse tangent. Comoving clocks are exact
unit geodesics; a(0)=1,a'(0)=0 makes t=0 preparation parallel and L proper.
These are evaluator controls, not native-admitted cosmologies or construction
inputs for a new UDT response.

For future affine state(t,x,T,X) and the radial coordinate transport matrix P,
the same metric connection gives

    t'=T, x'=X, T'=-a(da/dt)X^2, X'=-2[(da/dt)/a]TX,
    P'=-[[0,a(da/dt)X],[((da/dt)/a)X,((da/dt)/a)T]]P.

Launch T=1, X=+/-1/a(t_e), P=I and stop at actual x=+/-L. Endpoint contractions
give Z=1/T_receive. Centered arrival differences at two emission steps, with
Richardson extrapolation, hold clock histories fixed. Selected reverse first
signals use this control's reflection symmetry; selected echoes start at the
actual first reception. Skipped echo queries are not numerical nonexistence
findings. Analytic control horizons remain owned by the prior source arguments;
the engineering time/affine caps are not physical endpoints.

The frozen matrix is 14 queries at three tolerances, with 42 center trajectories
and 246 ray solves. All coarse and tight results remain. The tight 14 satisfy
the frozen thresholds: largest null-relative defect 2.03e-10, metricity defect
1.53e-9, sampled original scaled residual 1.66e-11 and arrival/frequency
discrepancy 2.29e-9. Coarse settings are refinement diagnostics and exceed some
tight thresholds. Dense-trajectory differentiation versus the original shared
RHS is an unpreconditioned residual check, not independent certification.

A separate implementation uses 60-digit metric quadrature/root inversion,
affine integrals and a metric-frame transport expression, without parent code
imports. It checks all 246 endpoint roles and 6393 saved trajectory samples
using 190 distinct scalar anchors, with selected 90-digit repeats. Tight maximum
relative frequency error is 6.79e-11; parent arrival derivative versus the
independent Z differs by at most 2.355e-9. Wrong-frequency, wrong-direction and
shifted-incidence mutations are rejected. Small-L amplification is explicitly
measured. These are finite floating/high-precision checks and observed refinement,
not rigorous enclosures, universal convergence order or numerical proof of an
asymptote. R6/R7 and the analytic control arguments retain their own hypotheses.

Actual-workload smoke checked readable trajectories, constraints/residuals,
SIGINT after a completed query, exact restart agreement, and config mismatch
rejection. An incomplete in-flight query is not certified resumable. Both smoke
paths and production totaled 284 rays/101368 RHS calls within the stated caps.
The finite CPU production took about1.36s; no GPU or multi-hour run was needed.
The [frozen numerical evidence](udt_observation_metric_evaluation_2026-10-04/numerics/FREEZE.json)
and [independent checks](udt_observation_metric_evaluation_2026-10-04/review_math/INDEPENDENT_RESULT.json)
retain the actual equations, domains, commands, tolerances and omissions.

**Remaining scientific gate.** A useful astronomical confrontation must predict
the same angular-distance and spectral quantities, with actual source/observer
histories, ray/area geometry, declared disk/frame/source reductions or justified
recalibration, motion nuisance treatment and a joint uncertainty model. The six
marginal constraints remain usable while that package is being developed; their
existence does not identify positional attribution or force a new postulate.

A native time-live search additionally needs an admitted equation/constraint
class for metric degrees of freedom, chart/gauge, domain and sufficient initial/
boundary data. R6/R7 evaluate a supplied geometry; they do not supply its native
evolution. Existing conditional field/action branches do not restart or become
adopted here. More samples of these three controls would not close this join.
R18 owns the current return and next gate. [Initial result and chronology](udt_observation_metric_evaluation_2026-10-04/INITIAL_RESULT.md)
and [work record](udt_observation_metric_evaluation_2026-10-04/WORK_RECORD.md)
preserve discovery, review and repair; no registry or CANON promotion follows.
