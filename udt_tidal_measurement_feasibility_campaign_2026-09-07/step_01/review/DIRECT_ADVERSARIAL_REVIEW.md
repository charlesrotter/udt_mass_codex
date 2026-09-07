# TM1 direct adversarial review — one bounded repair required

Reviewer /root/tidal_tm1_review, 2026-09-07. Fresh separate-context source-first
stage preceded TM1 author candidate exposure. Model UNKNOWN; different-model,
human-specialist and formal-verification axes UNTESTED. This is a substantive
argument/source review, not scientific promotion or flight validation.

Initial candidate SHA-256:
589eff684d768831a1390b525e2257ba78f0048b6966c8ae2579097585d1ec44.
check_interface.py:
25321733e08c54d9c2eea7de1b2d8472a61f3682e142166d45765b58e74b768e.
SOURCE_LEDGER.tsv:
5f7f67d531f9cf7b66b96783020a80fc04971c34af09c96deec4aedd0f757ad6.
SOURCE_ACCESS_AND_EXPOSURE.md:
5f14ff6ffe0153e9b0023693d496bda31eb1f76d354a8abcaabff89c25a8a762.
CANDIDATE_FREEZE.md:
6b98030926e0096d8650b65e527735b0944a38e286328d09e17146cea2544d20.
All hashes independently checked against supplied files.

## Verdict and required defect

REPAIR_REQUIRED: one statement is too broad as written; the conditional
kinematic, calibration-provenance and unresolved-eligibility conclusions
survive. No additional required defect was found in this direct pass.

R1, Section 4: H1=0 does not imply blindness to arbitrary constant signals for
an unrestricted operator H. For componentwise H(x)=x(x-1), H(1)=0 but H(2)=2.
The smallest same-premise repair is to say "a fixed linear operator H with
H1=0" (or explicitly require annihilation of every constant). Then
H(kappa 1)=kappa H1=0, and adding kappa 1 to arbitrary input is also invisible.
The author confirmed that the intended class was fixed linear. This adds a
missing mathematical hypothesis, not physics. Initial text and the concrete
counterexample must remain preserved. A focused review can close this one
repair without redoing sound source/kinematic work.

## Argument adjudication

Geometry: the explicit Q convention matches G358, including its sign, future
unit observer and orthonormal spatial frame. Ric(U,U)=sum_i Q_i00i=-Lambda
gives trace(T)=-c_E^2 Lambda. Converting affine proper arclength to calibrated
proper time explains c_E^2; it is not a gain fitted from this trace. G313's
contracted Bianchi argument gives connected constancy only in the admitted
regular bounded arena, whose actual Earth-orbit application remains open.
W4/G261 do not provide electrostatic suspension, metrology, star-camera
response, or error control. The candidate makes these limitations explicit.

Kinematics: independently reconstructing the inertial acceleration of a
rotating fixed arm gives dotOmega+Omega^2. Subtracting freefall acceleration
-T xi gives holding acceleration (T+dotOmega+Omega^2)xi. Pair differencing
cancels common acceleration only in that ideal model. Because A_d is a half
difference over a full baseline, S=2 A_d L^-1. Symmetric and antisymmetric
parts yield exactly the candidate matrix equations and trace correction.
The E2 conventional Hessian has V=-T under this holding-force sign convention.
The argument does not derive a finite device response from UDT. In actual
measurements all unbounded finite-size, control, self-gravity, calibration and
frame effects remain in D; no numerical smallness claim is made. The trace
error expression including delta omega is exact given the stated additive D.

Sources: independently read the old handbook and EWP-2384 methods before the
candidate. The old Eq.4/Eq.5 sign conflict is real, and E2 equations 6–38 agree
with the independent reconstruction. The old handbook also has a yy component
transcription error recorded in Stage A; the candidate does not rely on it.
E2 zero-trace redundancy/ideal adjustment is distinct from its band-limited
negligible-gradient calibration. The angular-rate integration-constant filter
is not automatically a filter on the gravity-gradient DC channel. None of
these is evidence that every L1b trace is zeroed or that every discrepancy is
removed. Candidate Section 3 states these distinctions correctly.

For the newly exposed E3 source I independently opened the primary 2019
publisher abstract/method summary, DOI 10.1007/s00190-019-01271-9. It identifies
the 2018 reprocessing method and use of star-tracker rates, GRACE-model
gradients, equal common-mode conditions, and shaking data. That supports a
calibration-dependency warning, not a complete modern algorithm audit. No
performance conclusion from the abstract was used. E5 full algorithm access
remains unverified here; no universal access impossibility is asserted.

Identifiability: z_a=kappa+b+e_a has the exact translation alias stated when
b is an unknown constant. The candidate does not imply every real bias is
constant. Constant contrasts can test departures only when changing errors
and signal retention are independently controlled; their zero response to
kappa is not evidence of Lambda=0. Pointwise trace-free projection removes
the scalar algebraically. R1 supplies the missing hypothesis for generic H.
The candidate's continuation is a conditional nuisance/calibration question,
not an assumption that a released product has an unused rejection direction.

No requirement for a uniquely selected universe or all initial data appears;
no physical identification, empirical claim, native device law or all-instrument
no-go is inferred. A calibrated scalar alone would not select the full metric.
This is the strongest surviving interpretation of the stated landing.

## Independent checks and their limits

Source-first stage_a_exact.py used an independently constructed rotation jet
and symbolic holding forces before seeing author formulas/code. Twelve checks
passed; its general symbolic variables cover the stated ideal matrix algebra.
No author code was imported. It shares SymPy and capture infrastructure, so
software-library independence is not claimed.

After candidate exposure, direct_exact.py used standard-library exact rational
cross products and explicit component inversion, without SymPy or author-code
import. A non-diagonal synthetic T, all nonzero omega/alpha components and
unequal positive baselines reconstruct the complete matrix, with trace 8.
The nontrivial trace-error control gives 670114078241/821494211835 exactly.
The script also verifies scalar/bias alias, contrasts and the R1 counterexample.
Eleven checks passed in 0.018 seconds, max RSS 12,096 KiB. One of these checks
only authenticates the saved author's 13-item output consistency; it is
packaging evidence, not an independent scientific check. A finite fixture
does not bear the analytic quantifiers.

The unchanged author checker was replayed separately: 13 checks passed in
0.203 seconds, max RSS 44,568 KiB. cmp reported byte-identical saved stdout.
That replay is regression only. The original source-first reasoning and new
rational reconstruction supply independent scrutiny. Saved stdout alone has
boolean guards, not calibrated data, and does not establish device eligibility.

Commands used the unchanged shared run_capture.py with absolute output stems
inside this review directory, one completed CPU child at a time, 512 MiB
address space and 60-second CPU/wall limits. Exact commands, times and outputs
are in direct_exact.json/.stdout/.stderr and author_replay.json/.stdout/.stderr.
No failures, timeout or resource escalation occurred for these calculations.

## Exposure and omitted checks

Source-first exposure/seals remain in STAGE_A.md, STAGE_A_SHA256SUMS and
STAGE_A_PRIMARY_ADDENDUM.md (SHA a1761f6e9b48394816166c07cd2559ecb86dae8f8bc90631b69cfa713a0095b5).
Only after those seals did I read the frozen TM1 candidate, source ledger,
access/exposure record, author code and outputs. Primary-source retrieval and
the E3 abstract included incidental qualitative historical outcome prose;
this is disclosed exposure, not pristine observational blindness. No flight
arrays, measured residual series, results chapters or plotted outcomes were
used, and no data payload was downloaded.

The parent's full 349-row audit was not repeated. Old UDT suites, a full modern
GOCE processing audit, real noise/bias estimation, finite-baseline and relativistic
error bounds, and a complete Einstein-observation protocol were not performed.
No human or different-model review occurred. Source versions are authenticated,
not independently re-proved wholesale. One same-premise repair/focused review
is now pending; no downstream use as an accepted reviewed finding until it closes.
