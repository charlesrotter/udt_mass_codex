# Quiet GR correspondence — proposed next question

Status: DIRECTION/FIDELITY REVIEWED WITH CAVEATS; see review/FINAL_REVIEW.md.
The proposed bound is unproved and its campaign not yet authorized. No research result,
physical adoption, response-law selection or successor campaign launched.

## What Charles's clarification changes

Expect UDT to recover GR's successful predictions, but do not use that
expectation to declare every possible departure exactly zero. Exact recovery
remains a legitimate outcome; a sufficiently small departure remains a
possibility to assess, not a desired effect or an established UDT prediction.
The intended extension-of-GR relationship is a research objective; its actual
scope must be demonstrated. Present evidence supplies no numerical probability
for departures from UDT, whose governing response connection remains open.

GR has many precise tests, not one universal decimal-place accuracy. For
example, the2003 Cassini result constrained the particular PPN parameter gamma:
gamma-1=(2.1+/-2.3)x10^-5. The2021 Double Pulsar paper reports agreement for
GR's quadrupolar radiation prediction at1.3x10^-4 (95% confidence). These are
different quantities and experiments, not rival universal error bars or a
current best-bound survey. [Bertotti et al.2003](https://www.nature.com/articles/nature01997);
[Kramer et al.2021, author abstract](https://arxiv.org/abs/2112.06795).
Neither is a tolerance for a UDT angular residual.

Keep three claims separate:

1. Exact correspondence: equality in a stated mathematical limit/domain.
2. Controlled correspondence: a specified small geometric departure gives a
   bounded departure in specified readouts, with hypotheses and error control.
3. Empirical compatibility: predicted measured quantities agree with records
   under justified calibration, transfer and uncertainty assumptions.

None of these, by itself, identifies UDT's response formula. Observational
agreement is judged against data, not merely closeness to a GR formula; shared
model/calibration errors and unused test information remain relevant. A finite
error bar cannot prove exact equality in every regime.

## Recommendation: quantify the quiet-to-readout connection

Ask: **Does nearly cancelling native angular response imply nearly GR-like
clock and tidal readouts after ordinary comparison data are fixed? If so,
on what domain and with what error bound?**

This uses the original metric's angular structure, not another chosen
response recipe. G260 already establishes, for the COMPLETE one-function
static spherical metric,

    ds²=-f(r)c_E²dt²+f(r)^-1dr²+r²dOmega²,  f>0,
    C_ang[f]=A_parallel+A_perp=r²f''/2-f+1.

Its exact zero set is f_ref=1+a r²+b/r. The angular sectors need not
individually vanish. This is an Einstein comparison family with a constant
curvature term; cancellation does NOT select a=0, b, an absolute scale or
physical source. G260's identities are admitted conditional geometry, not
an adopted universal equation. Current G312 authority qualifies all use.

The missing implication for this question is quantitative: a bound on this
native residual is not yet a reviewed bound on the chosen readout differences.
Do not assert that theorem before doing the proposed work.

Proposed framing: fix a nontrivial compact areal-radius interval K away from
r=0 and retain explicit positive lapse margins. Fix a reference radius r0
and calibrated time convention. Use two predeclared comparison data, such as
f(r0) and f'(r0), to determine a,b in the exact reference family. These are
ordinary supplied geometric data, not two new physical laws or a fit of the
remaining readout profile. Require an admissible positive reference on K;
if the data do not give one, report that comparison-domain obstruction.

Then ask for a bound of the form

    || O[f]-O[f_ref] || <= B(K,margins,normalization,reference/data bounds) * epsilon,
    where || C_ang[f] ||_(infinity,K) <= epsilon,

with O explicitly chosen from static proper-clock ratios, lapse gradients
and orthonormal tidal components. Define dimensionless/readout-specific
norms before deriving the bound; the arguments shown for B are illustrative,
not a proved exhaustive list. Derive and disclose any dependence on fixed
reference values/gradients or comparison-data bounds needed for each readout.
Do not presume uniformity across unbounded reference data from positivity
alone. B is not an adjustable calibration parameter or a new physical law.
Also separate residual-induced differences from uncertainty in supplied
comparison data. Epsilon is a symbolic mathematical control, not an adopted
observational accuracy or a physical law fixing C_ang(r). No instrument
identification or native emergence of light is required for these ideal
geometric comparisons; actual measurements require their own explicit bridge.

For eventual empirical use, epsilon control and reference calibration must
come with documented information independent of the designated consequence
records. Computing the residual from the same held-out tides or clock profile
and feeding it back into their purported prediction would be circular. The
separation is informational, not a demand for statistically uncorrelated
errors; shared errors require justified joint treatment. The
mathematical bound alone supplies neither a UDT-predicted residual nor an
independent empirical test. This campaign would establish the conditional
bridge, not assert that those further information requirements are met.

The one-function spherical restriction is deliberate and supplied. A result
there would not certify nonspherical or time-dependent GR correspondence.
The retained residual profile C_ang(r) and legitimate comparison data are not
selected by the study; its achievement would be an implication, not a law
creating or evolving those data. ND1/ND2 are reviewed unpromoted context only;
this proposal does not need to adopt their Q comparator.

## What would discriminate the outcomes

- A controlled bound would show exactly how close the specified ideal readouts
  must be when the angular residual and data errors are small, within the
  declared domain. It would supply a calculable bridge for later calibration.
- A sharp limitation could show that pointwise cancellation, finite sampled
  smallness, a shrinking lapse margin, or a growing comparison domain is
  insufficient. Identify the specific missing control, not a new physical law
  by default. Do not count known free a,b as a new obstruction.
- If the admitted source definitions cannot support the proposed readout
  comparison, identify the exact missing mathematical or measurement connection.
  Do not repair it by importing a response law or adopting a carrier.

An adverse result would concern this quietness criterion and its comparison
scope, not failure of UDT. A positive result would not establish general
dynamics, physical content, cosmology, stability or a distinguishing prediction.

## Scope, budget and return point

Propose at most TWO substantive reviewed steps or THREE hours, whichever first.
First derive/check the residual-to-readout implication at fixed admissible
domain/data; then, only if useful, test its sharpness and exact failure of
weaker controls. These are not two prefabricated example campaigns.
Use analytical work and small CPU/exact checks, one library thread,512 MiB
and60 seconds per ordinary check, at most two simultaneous author/reviewer
checks; no GPU or long solve. Each new load-bearing result gets fresh-context
adversarial review, with one same-premise repair/re-review. Preserve original
candidates, failed inferences and complete review caveats. Results remain
conditional/unpromoted; no banking is bundled.

Stop for a necessary new physical commitment, unresolved review objection,
no useful in-scope continuation, resource/access blocker or budget. Do not
extend into another response model, nonspherical evolution, observations,
instrument dossiers, source/Hopf rescue, or a selected tolerance. Return a
reviewed conditional bound, scoped counterexample, or precise unresolved
connection plus a lay decision brief. This proposed campaign has NOT begun.

This is more directly useful now than further S-versus-Q classification:
it asks what the native geometric cancellation actually controls. It does
not replace the longer-term native dynamics question, and cosmological or
carried-structure research remains available in parallel under future scope.

## Controlling repository sources

- Current authority: udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md.
- Accepted identity/classification: udt_g260_gr_quiet_angular_nondiscard_audit_2026-08-25/EXACT_DERIVATION.md.
- Completed ND limits: udt_native_response_discrimination_2026-09-09/DECISION_BRIEF.md and original reviews.
- Geometric readout/measurement separation: udt_local_clock_metric_benchmark_campaign_2026-09-07/DECISION_BRIEF.md.
- Calibration/test independence: udt_tidal_measurement_feasibility_campaign_2026-09-07/DECISION_BRIEF.md.

The last two are reused conditional benchmarks, not re-adopted instrument
laws; their inherited Einstein-arena wording is qualified by current G312.
No fixed manuscript, scientific grade, canon or protected work changes.
