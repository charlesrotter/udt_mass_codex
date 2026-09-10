# QC1 fresh-context adversarial review

Verdict: **VERIFIED-WITH-CAVEATS**, conditional mathematics only, UNPROMOTED.
No required mathematical repair or unresolved load-bearing objection remains.
The single author-check repair is accepted after focused inspection and replay;
it does not change the scientific candidate. The full365 G325 failure remains.

Reviewer `/root/quiet_step1_review`; date2026-09-10. Exact model UNKNOWN.
Starting HEAD2a3e64befd72b801cdd54e528d9a7c68362cdd7b, branch grok. Parent later
created ee213282f57ac0da1c2ef19549026745eee4cf4c, independently observed during
review; no reviewer Git mutation/sync was performed. Work order supplies scope
and resource authority, not scientific evidence. All own writes are confined
to step_01/review; protected payloads have not been read, hashed or changed.

## Exact target and source versions

Reviewed CANDIDATE.md, unchanged throughout scientific review:
`1a2a8439f2591631fd52e92b6c1c45c8a6e4e8e60a59c5e4b8642045cd2d5571`.
Source-first report was saved and its hash sent before candidate exposure:
`a4057835afbd2aa48638a680d3cc7d6f9ebbac875065982b2825ca742e9a805a`.
The seven-entry step_01/SOURCE_SHA256SUMS has hash
`c8d29b00629ef148b113e42d4237a6237623830ecf06020dd31f790155ca92b2`;
all seven entries independently passed sha256sum -c. The additional LC1 clock
contract hash and exact source roles are in SOURCE_FIRST_REPORT.md.

Source use: G260 supplies the complete positive static spherical metric and
the exact angular sum/zero family. G312 current authority forbids treating that
sum or GR comparison as an adopted universal response law. G261 supplies only
the qualified WORKING/POSIT_NOT_CANON physical-metric interpretation; its old
necessity/adoption language is not imported as current authority. LC1's
geometric lapse/acceleration definitions are reused; its empirical observations,
uncertainty numbers and instrument assumptions are not QC1 inputs.

## Mathematical judgment

The candidate proves its actual quantifier: for every C2 supplied profile on
a fixed compact positive-radius interval containing the anchor, a continuous
supremum bound on the exact G260 residual plus two bounded anchor-data errors
controls the profile through its second derivative. The reference retains both
homogeneous constants. Positivity is needed where the candidate says it is,
not silently used to manufacture linear ODE control.

The key proof is not the finite tests. Its integral representation follows from
the two Euler homogeneous solutions and the Green derivative jump. For x<1,
both the undifferentiated kernel and integration orientation reverse; the
absolute kernel mass is still U-1. The derivative kernel stays positive and
only its integration orientation changes; its absolute mass is abs(U').
The original identity then supplies the second derivative without requiring a
derivative of the residual. All endpoint-supremum constants in(3) are valid:
U and abs(V) have endpoint maxima, U' is increasing, V' decreases to1 then
increases, U'' decreases, and abs(V'') has endpoint maxima. In particular,
the sharper eta1*abs(V'') term is justified by exact homogeneous differentiation.

A second algebraic reconstruction checks the same representation without
assuming the proposed Green kernel. Set z=x*y. The identity becomes

    (z'/x^2)' = 2*c(x)/x^3,
    z(1)=delta0, z'(1)=delta0+delta1.

Two ordinary integrations give

    z(x)=delta0+(delta0+delta1)*(x^3-1)/3
         +2*integral_1^x u^2*integral_1^u c(t)/t^3 dt du.

For either anchor orientation, changing integration order and dividing by x
recovers exactly(1). The continuous forcing and compact positive-radius domain
justify those integrations. This is a source-preserving factorization argument,
not another physical equation. It agrees with the independently reconstructed
variation-of-constants proof recorded before candidate exposure.

The residual-only sharpness statement also survives: constant c=epsilon gives
y=epsilon*(U-1). It attains each listed component norm on the full interval,
including the derivative's opposite sign left of the anchor. Taking p=1 yields
a positive witness for every epsilon>=0. This proves only the stated component
sharpness; it does not optimize every nonlinear or combined-noisy-data bound.

The logarithmic clock-ratio bound follows from the derivative of log on[m,infinity).
It controls a relative clock ratio, with no hidden uniform absolute-ratio claim.
The two lapse-gradient/support-acceleration estimates correctly separate
coordinate and proper radial components and disclose the reference derivative
factor. Comparison occurs at the same supplied areal radius with each metric's
own static frame; it does not claim equal-proper-distance point identification.

Direct full-metric Christoffel/Riemann reconstruction confirms the curvature
sign convention and all six independent sectional entries. The tidal quantities
use second/first derivatives only; the sphere-sphere entry retains its unit
curvature term. Restoring r0^-2 and, for acceleration tides, -c_E^2 is correct.
The argument makes no unsupported local signal-speed or detector identification.

## Actual checks, repair and false-pass audit

The following runs use the existing run_capture.py, absolute output stems,
one library thread,512MiB address space and60CPU/wall seconds. Full commands,
UTC starts, stdout/stderr and resource receipts accompany each run.

1. Source-first independent_check.py, SHA
   `177bef92163627f79159df6b7df5cf4b071423ce5e34cc0bdf4eeaa5c00dd9db`:
   Python3.10.12/SymPy1.13.1, reported84 checks, rc0,0.654s,52016KiB.
   It constructs monomial and logarithmic-resonance particular solutions
   independently of the Green solver, verifies both anchor conditions and the
   residual, compares the integrated kernel, and reconstructs curvature from
   diagonal metric coefficients. Of84 reported rows, the SEVEN named
   `saturated profile` rows compare an expression with itself and are EXCLUDED
   as verification evidence. They are preserved as disclosed sanity rows,
   not counted as independent support. The six final nonzero formula checks
   are narrow mutation discriminators, not an exhaustive guard catch-proof.

2. rational_readout_check.py, SHA
   `2a47d878bc1881c45b02f70642eb11fd5c7d090361b9cd88922f85a14ff3219d`:
   Python3.10.12, rc0,0.198s,11520KiB. This uses no SymPy/Green constructor.
   Thirty-six arbitrary signed rational Laurent perturbations are supplied
   first; their exact residuals and noisy-data reference are then recomputed
   directly. Analytic coefficient bounds certify a common positive margin.
   At13 rational radii each,1404 exact profile inequalities and2340 separate
   60-digit Decimal clock/gradient probes pass, with72 positivity checks.
   Four explicitly corrupted control-omission inequalities are required to
   raise AssertionError and do. Maximum sampled exact profile/bound ratio1.
   The log probe uses1e-56 solely as a Decimal rounding allowance; these finite
   Decimal probes are not an interval-arithmetic certification. A redundant
   preliminary residual assignment in this preserved script is overwritten
   immediately; all residuals used by assertions are the following explicitly
   Fraction-valued recomputation. No claim relies on the discarded assignment.

3. Parent's preserved initial author run reported494 assertions. Parent found
   that some denominator probes used Python floating division and that one
   numeric nonzero-anchor assertion was vacuous. CHECK_REPAIR.md preserves
   this disclosure; original source is in ee213282 and raw output is retained.
   The one same-premise correction converts all four probe inputs to SymPy
   Rational and removes the vacuous assertion and its evidence label. This
   reviewer inspected the complete original-to-current diff and current code.
   Current check_candidate.py SHA
   `8d6c190f6fac2a958b574053ee3f2590cacaabf0d913e0182ecf390e201c3513`.
   The corrected parent run reports493,rc0,1.354s. Independent reviewer replay
   of that exact corrected script reports493,rc0,1.334s,59828KiB, matching its
   output. This last replay is SHARED-CODE REGRESSION, not an independent proof.
   The repair is closed; no scientific candidate text or theorem changed.

The initial premise verifier independently failed at
`G325 replay_exact:DERIVATION_RESULT.json`. No subsequent global premise gate
is reported passed. The seven source-manifest checks passed, the candidate
hash remained fixed, and scoped git diff --check produced no diagnostics.
No production solver, observations, raw arrays, physical evolution, GPU or
protected payload was used. Source-package full historical replays were not
repeated; this review validates the new argument against their exact definitions.

## Independence, exposure and limits

| Axis | Actual status |
|---|---|
| Context | Fresh separate agent context |
| Model | Exact identifier UNKNOWN; different-model review UNTESTED |
| Source-first exposure | Dispatch/question, current sources, prior reviewed proposal and its data-dependence warnings; no QC1 proof/code/results |
| Later exposure | Parent disclosed source-first concurrence and check plan after report/script creation; frozen candidate then author check repair/code/output |
| Implementation | Independently written source-first symbolic code; separate stdlib direct-profile implementation; final repaired-author replay is shared code |
| Mathematical method | Independent reconstruction from the same linear identity; main Green method overlaps author method; factorized integration supplies another derivation |
| Argument | Actual representation, norm, regularity, positivity, data and readout reasoning examined; tests do not substitute for it |
| Human/different-model specialist | UNTESTED |

The full original Charles conversation was not independently replayed. Work
order authorization is the parent record; no statement claims transcript
authentication. Checksums establish correspondence, not chronology, truth,
model independence or physical validity.

The theorem concerns only the supplied one-function static spherical class.
It supplies neither a law making the residual small nor the information needed
to bound it independently in an empirical test. It does not infer continuous
smallness from samples, uniform behavior as the lapse margin vanishes or the
domain grows, nonspherical/dynamical correspondence, physical stability or an
observational prediction. Current G312 authority remains intact and both
homogeneous comparison parameters remain supplied. Full365 failure excludes
scientific banking. These are exact scope limits, not unresolved defects.

## Permitted closeout and useful continuation

The author may label this exact candidate reviewed-with-caveats/unpromoted,
link this complete review, and append factual preservation/publication receipts.
No theorem, source grade or physical premise is promoted by that administration.
All initial false-pass disclosures, repair history and excluded review rows
must remain visible in the package. Any changed scientific claim needs its
applicable review; this verdict does not pre-review a successor.

Within the already authorized possible step2, a useful boundary question is
whether finite sampled quietness can replace the continuous hypothesis. A
positive profile with a smooth bump supported between samples and away from
the anchor can preserve both data while hiding large unsampled curvature.
That is a direction suggestion only here, not a reviewed second-step theorem.
