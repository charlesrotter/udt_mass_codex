# PIA1 exposed experimental/fidelity review

Reviewer `/root/pia_fidelity`; actual separate context with inherited Codex
model, precise runtime identifier unavailable. Different model is not claimed.
Source-first reasoning and its bindings predate exposure to the parent PIA1
candidate and primary-source ledger. After exposure, this reviewer directly
opened all five primary sources through the web tool on 2026-10-05. No sixth
source was introduced. No observational outcome is blind or held out.

## Direct primary-method verification

- [BACON v1](https://arxiv.org/html/2005.14694v1), main frequency-correction and
  analysis discussion, supplement 3.1 and 4.1–4.5: the manuscript reports
  corrected ratios, Lambda-type counters, cycle-slip/unlock filtering, common
  clock uptime and a white-frequency-noise fit used in uncertainty evaluation.
  It separately discusses dead time, correlations and between-day systematics.
  This supports a real frequency-transfer capability with qualified uncertainty;
  it does not establish FRI1's rectangular true-time means or uniform source
  derivative bound. Both fiber and free-space transfer are present, so it would
  be incorrect to dismiss the whole experiment simply as fiber propagation.
- [IPTA](https://arxiv.org/pdf/1910.13628), PDF p6, especially spin fitting and
  uncertainty discussion in section 3: unknown spin period and spin-down require
  removal of a quadratic residual component. The reported sample uncertainties
  and Bayesian intervals are correlated; their meanings differ. This supports
  the candidate's narrow claim that the quoted residual precision does not
  independently establish the secular proper-source clock needed by FRI1.
  It does not prove all pulsar observables lose every geometry-sensitive mode.
- [MCP XI v1](https://arxiv.org/pdf/2001.04581v1), PDF pp6–8, Tables 3–4 and
  sections 3.2/4: positions use an observational reference, and some listed
  accelerations are model-derived. Nine consecutive epochs are jointly fit
  with evolving Gaussian line centers; the disk model is explicitly warped,
  dynamical and Bayesian. These are useful spectral/angular observables with
  specified reduction assumptions. They are not direct finite means of the
  same proper-clock/parallel-frame quantities appearing in FRI1.
- [MCP XIII v2](https://arxiv.org/pdf/2001.09213v2), PDF p4 Table 1 and note:
  central velocities are optical-convention CMB-frame quantities obtained from
  disk modeling; intervals are posterior summaries. The six published central
  values were independently transcribed and their optical proxies recomputed.
  The range 1.0022659009–1.0339988540 agrees with the parent's rounded comparison.
  These are not direct total-Z measurements for the stipulated clock pairing,
  so no formal FRI1 exclusion follows without the missing transfer map.
- [JCGM 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf),
  sections 5.2 and 6.2–6.3, printed pp21–24: correlation belongs in uncertainty
  propagation; an expanded uncertainty interval requires a qualified coverage
  interpretation. A mean and standard uncertainty alone do not determine exact
  high coverage. This supports retaining FRI1's deterministic label only when
  absolute bounds are actually supplied, or introducing an expressly justified
  probability model. It does not establish that empirical bounds are impossible.

The readable PDF/HTML methods, not headline precision, own these checks.
Screenshot attempts for the three arXiv PDFs returned internal errors; their
complete relevant text passages were successfully opened independently. No
claim depends on visually inaccessible figure contents.

## Argument audit and independent arithmetic

P1 follows from positive factors and the FRI1 supplied box. The independent
exact squared expression is
12477510125000000000000000000/4250000051000000153, larger than 54180 squared.
Its illustrative square root is 54183.80477655202. The necessary HR, R/a and
R/m limits and m/a range were independently recomputed. These constrain the
stated metric/history interpretation, not generic observed distances or UDT.

The source drift map Q_e/Zmin is correctly in receiver seconds when Q_e uses
emitter seconds; its use presupposes a justified positive Z lower bound across
the hull. Arbitrary smooth source drift can absorb an alternative finite Z
record. A source history composed with its own emission map is well-defined
under the stipulated monotonicity; this is an ambiguity construction, not a
new adopted source law.

P3 is analytically sound for a bounded log-frequency curve and a positive
normalized window measure. The tilted-variable variance stays at most one
quarter of the squared range, and integration gives the stated one-eighth
coefficient. For the actual rectangular FRI1 target, changing the measurement
weight or adding gaps is an additional bridge; Jensen alone does not supply it.
Independent long-control arithmetic gives
4012009/128000000000000 = 3.13438203125e-8. The equal-phase witness in the
source-first review has an actual log-mean gap 0.14384103622589045, showing
why the conversion hypothesis is substantive rather than cosmetic.

Seven controls ran once after CONTROL_FREEZE, using independent standard-library
code, exact fractions for rational claims, and binary64 only for illustrative
log/unit values. All seven passed. The parent result was opened only afterward:
the exact P1/P3 values and independent unit conversions agree. The parent code
was not imported or executed. Controls, stdout, empty stderr, limits and
Python 3.10.12 are saved locally. No control establishes physical admission,
continuum coverage or experiment feasibility.

## Required clarifications communicated to the parent

1. Relate actual counter weighting/gating/dead time to the rectangular
   true-time window, rather than treating precision as a substitute. BACON's
   Lambda-type counters and filtered common uptime make this concrete.
2. A tail rejection needs an independently justified total-Z upper endpoint
   below 54180 for the same pairing, not merely a point estimate or a
   frame-reduced systemic proxy.
3. Probability propagation must start with Pr(E | C)>=1-p for the same
   admitted class C. An unconditional probability does not automatically imply
   that conditional coverage; a finite union bound needs no independence once
   its constituent event bounds are valid in that same probability model.
4. Exact B_*=0 preparation cannot be inferred from finite angular errors.
   Clock-rate, width and dead-time calibration are not timestamp-center error.
   CLARIFICATIONS.md has been read and explicitly preserves both distinctions.

The narrow survivor is a conditional measurement-interface audit: the examined
documented protocols supply useful pieces, but none supplies the complete FRI1
class and error interface. This is neither a universal impossibility result nor
an argument that all precision timing is irrelevant. The probability route is
left open, without importing a likelihood or adopting a source law.

## Actual repair and draft-integration re-review

REVIEW_REPAIR.md, CLARIFICATIONS.md, CENTRAL_INSERT.md, DESCENDANT_REVIEW.md
and DECISION_BRIEF.md were subsequently read in full. The repair explicitly
states per-fixed-history joint-event coverage, gives the alternative conditional
class-event formulation, requires a total-Z upper bound for exclusion, and
preserves actual weighting/gating/dead-time requirements. Exact B_*=0 and the
whole-hull limitation remain visible. These close all four clarification items.

The additional base-control clarification is correct: for identical calibrated
time windows the homothetic H/2 history has half C and half K delta; the same
absolute drift allowance gives a different q/K. This prevents silently
rescaling the physical schedule between the competing histories.

The proposed central insertion preserves both FRI1's positive enclosure and
its adverse factor-two witness. Its moderate-regime successor is explicitly
unstarted, needs new authorization and cannot inherit the tail certificate.
The descendant review names omissions and does not convert the failure of these
three protocol interfaces into a general rejection of UDT or all experiments.

Exposed verdict: **VERIFIED-WITH-CAVEATS**, applying to the repaired conditional
interface audit and proposed central wording. The caveats are the actual
unsupplied physical geometry/source/frame/error interfaces, not unresolved
defects in the narrowed audit. No science grade or premise is promoted.
Later final-byte integration still requires actual reading and attestation;
hashes will not substitute for that semantic review. Existing FRI1
solvers/continuum proofs were not rerun: this review checks the newly
load-bearing interface implications and source fidelity.
