# Decision brief — a bounded-data bridge is still needed

The approved design campaign reached a reviewed early stop after RD1. Fresh
separate-context review finds the conditional mathematics VERIFIED-WITH-CAVEATS,
with no repair needed. The practical response/support gate is NOT CLEARED,
so RD2's robust-statistic design was not started. This is a limitation of the
proposed unrestricted-waveform finite-window procedure, not a verdict against
UDT, gravitational-wave measurements or another response model.

## What was learned

Three measured channels can constrain two waveforms when the complete
measurement map and its errors are controlled. Merely counting three channels
and two functions does not establish that control. In a deliberately simple
point-sampling model, even exactly band-limited functions can interpolate any
finite collection of asynchronous samples if their size is unrestricted. This
does not establish a fit to actual processed data, or that such a fit would be
weak: the required waveform can be enormous. It exposes the missing finite-
support/approximation assumption behind an exact finite-vector cancellation.

There are constructive alternatives to selecting every waveform value. A
stable training response can bound waveform size from training measurements
alone, allowing a withheld contrast to remain testable. Alternatively, a
justified size bound can give a sharp prediction interval while leaving
infinitely many waveforms free. These are conditional mathematical routes,
not newly adopted laws, actual source bounds or observational results.

The exact framing is in [RD1](step_01/CANDIDATE.md):

- If B A_T=I and training/contrast error budgets satisfy kappa<1, then
  H_train=(||B y_T||+eta_B)/(1-kappa) bounds ||h|| and
  ||y_V-A_V B y_T||<=rho H_train+eta_r.
- For exact noiseless Hilbert-space training and a supplied ||h||<=H_max,
  the sharp unused-readout radius is
  ||p|| sqrt(H_max^2-||h0||^2), where h0 is the minimum-norm training solution
  and p is the holdout functional's component invisible to training.
- The supplied stationary arm-transfer model has an analytic error bound;
  nominal arm-only sensitivity values are finite. They do not bound the
  remaining calibration, time dependence, cleaning or support errors.

The first conditions are sufficient, not necessary for every useful prediction.
The second interval is exact only in its stated noiseless model. The arm bound
controls a conventional instrument formula, not an instrument-independent UDT
law. General arguments and finite checks are explicitly separated in the review.

## The actual blocker, and what remains free

The present sources do not instantiate the complete response/support and noise
allowances at the earlier 1e-21 strain sqrt(second) query. Pointwise one-sigma
calibration tables are not simultaneous hard bounds; finite processing checks
are not uniform arbitrary-waveform retention guarantees. A justified aggregate
or probabilistic error model could suffice: every raw sample, full covariance
or unique input selection is not demanded. No such missing control is silently
assigned a favorable number here. The 33 already exposed backgrounds cannot
be relabeled independent validation and were not reopened in this campaign.

Waveform functions and the unresolved admissible size/support class remain
free. Sky/time are supplied query data; c_E is an observed clock/ruler scale,
not a metric-selected absolute geometric scale. Instrument and weak-wave
transfer assumptions stay supplied. Admitted geometry supplies the conditional
wave arena, not these apparatus relationships. No observational geometric
constraint, physical-content identification or uniquely UDT prediction follows.

## Recommendation and next decision

Park this particular unrestricted-waveform finite-window procedure at this gate;
do not optimize its statistic or unseal the event. Continuing it productively
would first require a defensible bounded waveform/support or prediction-only
error class, fixed before confirmation, and a target-level allowance for the
composed measurement. Establishing that bridge need not require a new physical
premise, but this campaign neither chooses the class nor establishes its
applicability to the source. Charles's next direction decision is whether to
authorize that narrower bridge or redirect the observational route. No next
campaign is automatically authorized. Geometry/calibration and possible
emergence remain parallel, neither dependent on this instrument gate.

## Verification and preservation

One reviewed step completed within the two-step/three-hour ceiling. Separate
review reconstructed the argument, recomputed kernel norms and sharp interval
endpoints, checked source correspondence, replayed the author output exactly
and rejected direct formula defects. Source-first mathematical contributions
were exchanged and disclosed; fresh context is not a claim of different model,
no communication, human review or formal verification. No repair was required.

The actual fresh349 premise audit passed. No new strain, event, fit, accepted
grade/premise/canon or fixed-snapshot manuscript change. Protected local payloads
were not inspected. GOCE remains PARKED with eligibility OPEN/UNRESOLVED and
the enquiry UNSENT. Backup completeness and pre-reboot unsaved state remain
UNVERIFIED; ScratchDisk blocks only archive-dependent work. The compact log,
review and exact commands/pins preserve the campaign evidence.
