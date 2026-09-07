# Minimum GOCE documentation assessment

Initial candidate, separate-context review pending. Document follow-up only;
product eligibility OPEN. Source snapshot1e89bc9f; PE1 and TM1/TM2 unchanged.
Exact URLs, hashes, new reads and exposure: SEARCH_AND_EXPOSURE.md and prior
PE1 step_01/SOURCE_LEDGER.tsv. No data fitted or new theorem claimed.

## What is now resolved, and what is not

1. **Release identity has a precise verification route.** Prior official
   catalogue evidence identifies EGG_NOM_1B baseline0202; prior cached
   single-item metadata gives EGG_NOM07.00, not a release census. The2008
   handbook §4/Table5 explicitly directs users to MPH `Software_Ver`;
   Table9 also names `Ref_Doc`, `Proc_Center`, `Proc_Time`. Tables11–12
   describe reference DSD filenames, including `Proc_Config_Params_File`,
   constants, inverse calibration and EGG auxiliary database. This supplies
   concrete support-record questions. It does NOT authenticate actual0202
   headers, complete2018 calibration provenance, or07.00 configuration.
   That handbook's processor table contains placeholders VV.rr, not modern
   version assignments. A trusted release/configuration attestation with
   validity scope could suffice; no whole-product download is demanded.

2. **Calibration is better characterized, not certified.** The April2018
   ESA author presentation, slides10–15, displays gravity-model gradients,
   star-tracker angular information and equal-common-mode observation
   equations; science-mode estimation includes inverse calibration/drifts,
   quadratic factors, angular couplings and misalignment. Its stochastic
   slide specifies robust PSD estimation and additional0.8–10mHz weighting.
   This is already identified, pre-final method context—not proof of the
   settings/constraints used for0202. Neither this weighting nor parameter
   drift proves scalar erasure, a delivered-product band limit or an additive
   affine scalar nuisance. The final objective, constraints/priors, fitted
   epochs, parameters and response to departures remain release questions.
   The separately retrieved GO-TN-AI-0069 is actually2008 preflight, not the
   missing modern external-calibration specification.

3. **Processing support is localized but not numerically bounded.** PE1
   identifies matrix interpolation, adaptive median/mask replacement, gaps,
   integration, symmetric and edge filters and manual calibration epochs.
   New TN3397 §8.3/Table15 also shows an attitude window K and flag-dependent
   weights. These permit asking for settings/support by stage or an equivalent
   end-to-end support certificate. They do not certify a guard-gap duration
   or that two processed intervals are unused relative to one another.

4. **One covariance has a known limited purpose.** TN3397 §8.2, printed54–58,
   expects temporal and shared-input correlations but uses a block-diagonal
   approximation in the attitude reconstruction for computational cost.
   Its empirical variance functions are processing weights, not a validated
   joint uncertainty of the released diagonal sum. This closes what that
   section supplies; it does not establish that no adequate uncertainty
   product exists elsewhere. Need a supported covariance/error bound for
   the intended contrast, including calibration, angular-rate, acceleration,
   baseline and temporal cross-effects that matter at the claimed precision.

5. **The arm question is narrowed to a convention crosswalk.** Handbook
   §3.2.2.1 describes the pair baseline as approximately50cm and eq6 uses
   the distance between two accelerometers. This supports full-separation
   terminology, not the actual meaning of every2018 symbol/configuration
   field. TN3397 eqs6–9 use half-differences, while Algorithm16's displayed
   factor corresponds to full separation, as the unchanged PE1 review
   established. Ask for the convention/erratum and AUX_EGG_DB/channel map.
   No flight-data normalization defect is established.

## Minimum sufficient dossier, not a demand for all raw inputs

| Question | Trustworthy evidence that could suffice | What remains outstanding |
| --- | --- | --- |
| Which implementation? | Applicable release note/configuration identifiers and validity ranges, representative header reference chain or processing-team attestation |0202 ↔ processor/configuration/TN3397 crosswalk, including exceptions |
| What was fitted or enforced? | External estimator specification with parameter basis, constraints/priors, weighting and input/epoch provenance; equivalent validated end-to-end target-response record | Whether and how constant or varying trace directions were absorbed, constrained or retained, including indirect model conditioning |
| Which information is reused? | Support/selection map for fitted parameters, masks and filters, or justified influence/support bounds | Shared science/shaking/attitude/orbit/gravity-model inputs and validity windows; unused-target claim versus merely separate output rows |
| What uncertainty is justified? | Joint contrast covariance with justified statistical model, or conservative deterministic/systematic bounds including relevant shared effects | Practical sensitivity and correlation/remainder bounds; no independence or Gaussianity assumed |
| Which units/conventions? | Arm/channel/sign/frame mapping tied to applicable auxiliary configuration, plus clarification of the displayed symbols | Half versus full length in intro/Algorithm16, actual calibrated differential-channel normalization |

This is an evidence map, not an iff theorem about documentation completeness.
One authoritative record may answer several rows. Need not uniquely recover
every calibration parameter, metric initial datum, or individual raw sample.
Conversely, a nominal sensitivity curve, list of input files or small final
trace residual alone cannot establish unused information.

## Precise inherited test framing

Under the owner-provisional bounded connected Ric=Lambda g arena, W4
WORKING/POSIT coupling and SUPPLIED TM1 device bridge, ideal
tr(T)=kappa=-c_E²Lambda is constant. The engineering sign identification
V=-T is supplied; it is not a native detector law. TM2's reviewed UNPROMOTED
finite linear model is

    y=P(kappa 1 + N beta + delta)+epsilon,
    M=[P1,PN], CM=0,
    genuine noiseless scalar-test dimension = rank(P)-rank(M).

A fixed contrast needs CP delta nonzero for a specified departure and
justified contrast error to have practical power. No P,N,C,delta,band or
error tolerance is selected for actual GOCE here. This rank criterion is
not automatically applicable to its nonlinear/adaptive pipeline.

The requested response information must include calibration estimation and
selection where they use the same inputs—not just propagation with fitted
coefficients held artificially fixed. A validated local response plus a
remainder bound, or a trustworthy nonlinear/influence description with the
needed scope, may replace an exact fixed-linear description. Trace-free
gradient/attitude or other-channel leakage must be included or bounded;
not every processor output can be assumed to depend only on scalar input.
This is a requirement for a justified reduction, not a newly proved model.

Unused test information does not require statistical independence of every
input. Known shared influence and joint errors may be accounted for. But a
quantity imposed by calibration is not an independent test of that same
condition. Even complete loss of absolute scalar information need not erase
all scalar variations; model-assisted calibration alone decides neither.

## Decision

Recommend **await a reply after Charles approves an enquiry**, rather than
more compatibility examples or immediate abandonment. Public targeted reads
have narrowed the request but not supplied the release-specific retained-
response/error bridge. Draft ESA_ENQUIRY_DRAFT.md is UNSENT, contains only
public product/document references and general metrological questions, and
requests routing through catalogue-linked EOHelp/TellUS to GOCE processing.
Exact form categories/named team are unverified; no direct email invented.

A reply documenting retained response and bounded error would justify a
separately authorized protocol-design decision, not automatic eligibility or
fitting. A demonstrated enforced/absorbed target would close that target,
not every GOCE observable. Inadequate available bounds/support could justify
parking this scalar route and assessing another instrument. Missing records
do not refute the instrument or UDT and do not necessitate a new premise.
Geometric and emergence research remain available in parallel.

No product promotion, premises, registry grades, fixed through-G352 manuscript
or canon change. Backup completeness and pre-reboot unsaved-state disposition
remain UNVERIFIED; ScratchDisk is irrelevant here and blocks archives only.
