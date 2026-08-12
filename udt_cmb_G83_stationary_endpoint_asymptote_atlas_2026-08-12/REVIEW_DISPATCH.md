# External review dispatch — G83 stationary endpoint-asymptote atlas

Perform a cold, read-only adversarial review of the sealed intake defined by `REVIEW_MANIFEST.tsv`. Do not inspect files outside the intake, edit files, or continue the research.

## Central question

Do the sealed sources and artifacts support exactly this bounded landing:

`BOUNDED_STATIONARY_ENDPOINT_ASYMPTOTE_CANDIDATE_ATLAS`

Specifically:

1. Is it correct that all 591 G75 profiles have finite positive lapse on their declared `0<=x<=1` domain and therefore contain no infinite stationary endpoint depth there?
2. Under an explicitly `FREE_AND_EXPLORED` continuation, does only `AM`, `A=1-x^2/4`, have a positive lapse zero, with stationary `phi_pair -> +infinity` and conditional `c_eff(source)/c_eff(receiver) -> 0` as `x_source -> 2^-`?
3. Is the continued radial proper-length limit finite and receiver dependent, thereby preventing its silent identification with the frame-shared physical `X_max`?
4. Does the 591-row complete path census honestly retain all G75 angular/mixing profiles and support the exact 516 reached, 18 turning, and 57 affine-cap counts with zero solver/nonfinite failures?
5. Do raw residuals certify all 516 reached rows, and do the 18 stratified Radau replays honestly cover all represented behavior classes and all three approach levels?

## Adversarial checks

- Verify every intake hash and the committed preregistration boundary `e4a30822`.
- Inspect the `h=x^2 q(x^2)` derivative implementation, source-surface construction, event handling, caustic sampling, residual definitions, and status classifier.
- Check that the G75 `q` normalization/domain was only `0<=x<=1` and that continuation beyond it is never presented as inherited physical authority.
- Independently recompute the exact lapse, reciprocal-depth, conditional `c_eff`, and radial proper-limit identities.
- Independently recompute all saved row counts, unique identities, status patterns, and residual maxima from the TSV evidence.
- Distinguish exact independent scalar verification from the Radau replay, which deliberately shares the geometry engine and only changes integrator family.
- Inspect and exercise the eight hostile catches for missing/duplicate rows, invalid status, bad residual, nonpositive strict lapse, infinite strict depth, false receiver independence, and continuation promotion.
- Identify any hidden assumption that turns a stationary Killing-lapse zero, chart coordinate, or one-sided proper length into `X_max`.

## Required landing

Return exactly one: `VERIFIED`, `VERIFIED_WITH_CAVEATS`, `CORRECTION_REQUIRED`, or `FAILED`.

Even a perfect review cannot select a physical profile, `R`, source surface, observer-pair separation operator, `X_max` or its value, CMB sky, action, matter source, bootstrap closure, local signalling law, or time-live dynamics.
