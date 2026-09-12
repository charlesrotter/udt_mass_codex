# LSB1 adversarial scientific review

Verdict: VERIFIED-WITH-CAVEATS for the conditional mathematical benchmark in
INITIAL_CANDIDATE.md together with CANDIDATE_CLARIFICATIONS.md. No scientific
promotion, physical adoption or canon. Final documentation fidelity is a separate
pending seal; this report by itself does not review forthcoming prose or pointer edits.

## Exact conditional survivor

On the supplied complete one-function spherical metric
L²[-f dT²+f^-1 dr²+r²dΩ²], f=1+a r²+b/r, with a positive margin on a fixed
compact positive-radius window, three distinct supplied static clock radii and
two time-tag slope ratios identify a,b exactly within this family. The determinant
in candidate (4) is nonzero for every consistent positive datum. Known areal radii,
normalization, layout, clock calibration and branch are independent supplied inputs;
they are not selected by this construction. One ratio is insufficient.

Given the explicit conditional null-probe rule and a supplied regular one-periapse
branch with finite static endpoints, local apparent direction and one-clock elapsed
round-trip time follow without separately retuning a,b. A fixed coordinate path
can be unchanged as a varies while its nonturning endpoint sky angle changes strictly.
Round-trip time retains metric and source-clock normalization; the finite examples
show a-dependence, with no universal time-monotonicity theorem asserted. An ideal
instantaneous direction-reversing relay is essential to the stated round trip.

This is a finite-layout conditional comparison contract. G395/G397 do not select a
native metric law, G220's null correspondence remains query-typed, and G176's
clock-leg interpretation remains a working clarification on supplied completed pairs.
No native event/path/pair assembly, response-class membership under FILTER ONLY GR,
physical signal/EM/source/mass/energy interpretation or absolute scale is closed.
Other theories given the same metric and protocol give the same readouts.

## Independent argument and source-first exposure

SOURCE_FIRST_NOTES.md records the calibration determinant, full null Killing
integrals, inverse-radius orbit equation, local tetrad angle and proper-time formula
before the LSB1 candidate was read. That derivation agrees with candidate (1)–(12).
The reviewer then directly inspected the frozen candidate, its quadrature transform,
parent CHECK_CONTRACT.md and scientific implementation, exact/current G176 label
and G176 audit after the chi clarification, and actual captured outcome files.
13 initially checked source/candidate pins matched; checksums prove correspondence,
not mathematical truth or chronology. Current source hash correspondence is recorded
separately. The preserved ND1/QC1 initial headers are qualified by current banked
G395/G397 grades, not silently treated as new promotion.

Source logic examined: the full metric retains the angular sector; its chosen
one-function form and constant term are substantive assumptions. Static time tags
have a stationarity-induced slope, independent of additive flight-time offset.
Calibration uses two ratios, not one scalar. The basis determinant gives exact
identifiability while allowing ill-conditioning. Inverse-radius coordinate-orbit
cancellation is tied to fixed path/periapse rather than fixed impact ratio; the
static tetrad restores lapse dependence in the endpoint angle. The turning-point
and no-barrier conditions support the finite integrals; square-root substitution
is valid only on the positive leg. Static reversal supports equal outgoing/return
coordinate durations; source proper time multiplies by sqrt(f_A). Matched flat
control is a declared areal-layout comparison, not equal proper-distance matching.

## Objections and smallest repairs

1. Positivity under small coefficient perturbations was not scoped explicitly in
   the one-ratio underdetermination paragraph. A positive compact margin guarantees
   it on K, whereas an arbitrary noncompact I need not admit the same guarantee.
   Smallest repair: specify K. CANDIDATE_CLARIFICATIONS item 1 does so. The affine
   one-parameter relation and exact two-ratio determinant survive unchanged.
2. chi_clock's working premise stamp was implicit in G220 compatibility. A reader
   could mistake the clock-leg expression for completed native pair construction.
   Smallest repair: explicitly retain G176 WORKING, supplied completed clock leg,
   and unclosed remaining germ. Item 2 does so; no additional physical premise
   is adopted, and no new kernel/evaluator is claimed.
3. “Independent calibration” and “unused prediction” could be misread as stochastic
   independence of errors, particularly when time tags/hardware are shared.
   Smallest repair: distinguish exclusion from parameter fitting from statistical
   independence, requiring covariance/systematics for an observational use.
   Item 3 does so. No noise model or real observation has been supplied.

All three source-preserving clarifications are accepted. No equation, sample,
resource limit or numerical tolerance required scientific repair. Initial candidate
and review history remain preserved. No unresolved scientific objection was found
within this bounded review; that is not proof against every possible future objection.

## Computation and actual evidence

Independent exact implementation exact_checks.py imports no parent scientific code:
12 symbolic identities passed, including general determinant and both coefficient
recoveries, original null tangent, frame normalization, orbit equation, angle
derivative, and squared transformed integrands with positive-sign hypotheses checked
analytically. Three independently introduced algebraic omissions produced nonzero
residuals. Exact symbolic support is distinct from the argument and from sampling.

Independent affine-geodesic implementation independent_geodesic.py was saved and
run before reading parent numerical output or implementation. It integrates
(r,v,T,phi) from periapse using DOP853, including the radial second-order equation,
and locates endpoint events; it does not use the parent's transformed radial
quadrature. The nine supplied (a,b) cases were run at two predeclared tolerances/
step caps (18 final boundary-value case/control replays), with 126 finite checks.
Each replay calls multiple affine IVPs while bracketing/root finding; the total IVP
call count was not instrumented and is not asserted to be 18. Captured run elapsed 1.598081110 s,
max RSS 79,968 KiB, exit 0, no timeout. All figures below are FLOAT64 diagnostics:

- Maximum original null constraint residual: 2.5598307921883726e-15.
- Maximum angular boundary residual: 1.9984014443252818e-15.
- Maximum coarse/fine absolute output change: 4.618527782440651e-14.
- Independent ODE versus parent tighter quadrature, all nine cases:
  maximum absolute periapse difference 6.661338147750939e-15;
  apparent-angle difference 1.1657341758564144e-15 radians;
  normalized RTT difference 3.197442310920451e-14.
- Maximum scaled cross-method difference: 2.074447861690642e-15,
  below the predeclared reviewer bound 2e-8.

The b=0 comparison is particularly direct. For a=-0.002,0,+0.002 the same coordinate
periapse is 3.68944124604339 to the displayed precision, while psi_B is respectively
0.4518592035260343, 0.4793247824206295, 0.5043895124551820 radians and tau*c_E/L is
23.766015886217726, 23.660101124764942, 23.585190473497562. It is a finite witness to
coordinate cancellation retaining measured readouts, not a physical parameter choice.

The reviewer reran the three frozen parent defect injections through separate
no-overwrite captures. All returned exit 1 at the intended guards: inverted
clock ratio -> calibration_recovery; omitted receiver lapse -> receiver_tetrad_angle;
omitted source-clock lapse -> source_proper_clock. These are shared-code regression
catch proofs, not another independent scientific confirmation. They are deliberate
failed runs and are preserved with stdout, stderr and receipts. Reviewer scientific
checks otherwise had no failure, resource overrun or discarded numerical case.

Both implementations share the metric premises, FLOAT64 platform, NumPy/SciPy and
Brent scalar root library. The independent axes are separate context, source-first
argument and separately written affine-ODE versus radial-quadrature methods.
Different model, human review, formal proof assistant and interval certification
were not established. Numerical residual sampling is finite; it does not bound every
point by itself. No global branch uniqueness is inferred from a root bracket.

## Current audit, environment and omissions

The parent current 398-row verifier receipt and actual stdout were inspected:
start 2026-09-12T23:22:17.961692+00:00, elapsed 404.18802595802117 s,
exit 0, no timeout. Parent numerical start was later, 23:29:37.789705 UTC;
parent audit/numerical serialization is supported by those receipts. The reviewer
attributes the full current audit to the parent and did not independently rerun it.
Source-package historical verification counts were not repurposed as current checks.

Python 3.10.12, SymPy 1.13.1, NumPy 2.2.6 and SciPy 1.15.3 were recorded. Reviewer
captures use one library thread, PYTHONDONTWRITEBYTECODE=1, <=180 seconds and
<=2048 MiB each, at most one scientific subprocess in this reviewer context.
Runtime model/version UNATTESTED; configured parent gpt-6-astra/xhigh is attribution
only. No subagent, second review, GPU, production grid, external dataset, protected
payload, archive, runtime configuration, disk operation, git mutation or source
package modification was performed by this reviewer.

No reproof of G395's full branch classification, G397's all-profile bounds or every
G220 source test was attempted; only the exact load-bearing family/clock premises
and this benchmark's joins were reviewed. Omitted: horizons, arbitrary/nonspherical/
nonstatic metrics, caustics/multiple images/winding classification, actual clock
noise and covariance, physical apparatus, backreaction, nonzero relay delay,
absolute-scale selection, empirical fit and native dynamics/response adoption.

Allocation records: parent conservative spawn bound 2026-09-12 23:22:18 UTC;
review deadline 2026-09-13 00:02:18 UTC. SOURCE_FIRST_NOTES initially used the rounded
00:03 deadline from dispatch; the precise bound above supersedes that rounding.
No exact first server allocation timestamp was exposed; first reviewer status reads
were at approximately 23:23 UTC. Final fidelity seal must record actual final time
and elapsed upper bound from 23:22:18, including this review and clarification cycle.

## Subsequent finite-hypothesis check

After drafting this report, a targeted check distinguished a simple radial turn
from regularity of the scalar endpoint root. The original candidate already
assumes a regular branch; no equation defect was found. REGULAR_ROOT_NOTE.md
records a credited reviewer derivation, checked by the parent, of strict negative
endpoint derivative on the reviewer diagnostic bracket [2,5.5]. It closes that
finite branch-regularity concern with an analytic bound, rather than treating the
saved sign bracket as proof of a nonzero derivative. Original numerical freezes,
code and results are unchanged. The note is part of the final review scope, with
its exact bounded hypotheses and no general-family uniqueness claim.
