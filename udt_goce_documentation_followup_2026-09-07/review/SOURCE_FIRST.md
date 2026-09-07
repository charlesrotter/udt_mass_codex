# Source-first documentation assessment

Reviewer `/root/goce_docs_review`, fresh separate context, 2026-09-07.
Prepared before reading the main follow-up assessment or enquiry. This is a
review working record, not a product eligibility or scientific verdict.

The smallest useful documentation request should identify the actual release,
what calibration and processing can absorb, which proposed contrast remains
responsive, and a justified uncertainty/support account for that contrast.
Obtaining every raw sample is not inherently necessary. A release-applicable
transfer/estimator description or trusted validation with suitable bounds can
be sufficient. Conversely, a product schema, final-stage formula or stated
noise model alone cannot establish the required end-to-end property.

## Independently reconstructed source findings

1. **Release applicability is a separate join.** The 2008 issue2/rev0 handbook
   describes historical `Software_Ver`, processor configuration reference and
   auxiliary reference fields (printed32,40–41). It gives specific metadata
   locators to request, but does not prove that baseline0202 retains the same
   schema or reveal the deployed configuration. PE1's indexed one-item
   processor07.00 witness is metadata evidence, not an authenticated release
   configuration or a census. A release-applicable crosswalk, processing
   manifest or equivalent authoritative statement could close this join.

2. **The calibration fit is load-bearing; model assistance is not a verdict.**
   TN3397 printed33–36 gives quadratic/coupled accelerometer calibration,
   model/star-tracker assistance, two calibration stages and interpolation
   between selected coefficient epochs. The April2018 author presentation
   slide7 identifies the gravity-model/orbit and calibration input routes;
   slides11–15 describe nonlinear dependencies, science-mode fitting,
   parameter/drift families and stochastic weighting. These are useful method
   facts, not proof of the deployed0202 fit specification. Request its fitted
   quantities, constraints/priors or regularization, basis/time windows,
   reference inputs and selection/adaptation rules, or equivalent validated
   end-to-end response information. In particular, ask whether the target
   scalar condition or its proposed departure is enforced, used for fitting,
   or left in a residual subspace. The answer may depend on the contrast and
   frequency/time domain. A DC degeneracy is not universal scalar erasure;
   calibration against a model is not proof of either survival or erasure.

3. **Unused support includes decisions, not just observations.** Coefficient
   fits, interpolation, angular-rate reconstruction and quality selection can
   connect otherwise disjoint output rows. Historical handbook Table43,
   printed92–94, is particularly relevant: it lists a trace-of-GGT threshold
   monitoring flag (`Qual_Flag_Ggt`) among output flags. This is evidence of a
   historical flag definition, not evidence of0202 rejection/censoring or
   trace projection. The request should ask whether the corresponding rule
   exists in0202 and only annotates records, filters them, informs coefficient
   choice, or affects downstream recommended selection. A flag-driven sample
   restriction could compromise an unused trace test even if the numerical
   output retains trace. A support/dependency account with adequate temporal
   extent and calibration/exposure history can suffice; raw archive transfer
   is not the default requirement. Shared support requires honest conditioning
   and joint errors; it does not by itself prove that no valid test exists.

4. **The uncertainty must belong to the proposed scalar contrast.** TN3397
   §8.2 printed54–55 explicitly recognizes time correlations and then uses a
   block-diagonal approximation for attitude reconstruction. That calculation
   is not a validated complete error covariance for arbitrary scalar-gradient
   contrasts. The request should distinguish calibration uncertainty and
   reference-model error, component/time correlations, angular-rate correction
   errors, and selection effects where material. A justified conservative
   bound is an alternative to a full covariance/distribution model. A nominal
   covariance or PSD is neither a hard error bound nor automatic significance
   calibration. No numerical tolerance should be selected in this follow-up.

5. **Ask the arm question neutrally and at the implementation boundary.**
   TN3397 Eqs.(6)–(10), printed8, use half-difference acceleration and position;
   Eq.(9) labels the resulting position entries `L`. Algorithm16, printed61,
   writes a diagonal `-2 a_d/L` term. Those written conventions motivate a
   request to identify the actual arm-length quantity and acceleration
   normalization used by the release/auxiliary fields, with an erratum or
   authoritative clarification if available. Neither the observed notation
   nor this source review establishes a deployed factor-of-two error.

## Minimum decision information, not a completeness theorem

The documentation route succeeds for one prospective test if it supports a
declared, release-specific scalar departure/contrast with nonzero end-to-end
response after allowed calibration/nuisance absorption, plus usable justified
errors and a defensible unused-support/exposure account. Equivalent documented
response and uncertainty bounds can replace a complete processing replay.

TM2's fixed-linear `P,N` is one conditional analysis framework. The actual
GOCE method cannot silently be identified with it: a supported local reduction
with a controlled remainder, or another justified nonlinear/adaptive response
description, is needed. Nonzero response establishes noiseless separation,
not attainable detection. An unsupported join stays open; none of the method
sources alone certifies eligibility or ineligibility.

A concise enquiry can group requests into: (i) release/configuration mapping;
(ii) calibration, filtering and trace-monitoring role/support; (iii) retained
scalar response and justified uncertainty; (iv) arm convention. It should seek
existing documents or a referral, avoid requiring a new mission-team study,
and describe the proposed work as a scalar consistency test. No distinctive
UDT signal or internal research claims are needed. It remains an unsent local
draft for Charles's approval, with no attachments or repository disclosure.

## Exposure and scope

Actual HEAD was independently read as
`1e89bc9fd3c21c5c937400cb1903d565294dbc3b` on `grok`. Git status showed only
untracked work at reviewer startup. Protected names appeared only in status
and mandatory instruction/status records; their payloads were not read.

Read on-disk AGENTS; bounded LIVE/HANDOFF current blocks; research program and
premise orientation; CLAUDE method, trigger and discipline text; completeness,
verifier-before-record and no-shortcuts protocols; compact INDEX/MEMORY;
CROSS_MODEL_VERIFY. Per dispatch, no checkout/fetch/pull or tracking change,
and no duplicate heavyweight premise verifier was launched. Remote freshness
and the main audit outcome are not independently certified by this review.

Task WORK_ORDER/FOLLOWUP_LOG and PE1 SOURCE_LEDGER/ACCESS_AND_EXPOSURE were
read before primary sources. Their inherited findings, candidate status and
prior review descriptors were exposed. Source URLs/local PDF pointers came
from main; source discovery is shared. The full reviewed unpromoted TM2
argument was read as the controlling conditional framework; its proof and
examples were not independently re-proved here. Main's new conclusions,
draft and prior direct reviews were not read before this record was sealed.

No observation payloads, quality reports, calibration files or measured
residuals were retrieved. Primary method-page text unavoidably exposed
historical qualitative performance motivation and §8.2's illustrative
variance/cofactor constants. None was used to select a test, interval, model,
threshold or claim. Presentation pages beyond15 were not opened. This is not
pristine future observational exposure. No fits, simulations, new scientific
arguments, physical commitments, accepted grades or canon changes occurred.

Context independence is real. Exact runtime model is unexposed/UNKNOWN;
different-model and human-specialist review remain UNTESTED. Implementation
independence is not applicable to this documentation review. Argument stage
is source-first reconstruction with shared sources and disclosed historical
verdict exposure, not a fully blind independent scientific review.
