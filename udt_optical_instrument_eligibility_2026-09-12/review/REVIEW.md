# OB2 fresh documentary/adversarial review

**Main verdict: VERIFIED-WITH-CAVEATS at the source-bounded documentary scope.**
Full eligibility for OB1's proposed optical measurement is **not established by
this selected two-page report**. The report documents a useful fiber gyroscope
demonstration and relevant components. It does not supply the required three
optical-frequency signed phasors, their transfer/calibration/error contract or
unused-confirmation provenance. This conclusion survives adversarial review.

One narrow inherited-contract wording defect in INITIAL_ASSESSMENT requires the
clarification below. It does not change the documentary outcome, invent a transfer
law, repair OB1 mathematics or reject the hardware. Preserve the frozen initial
assessment and close the wording issue in an explicit source-preserving overlay.
Same-context re-review/final narrative fidelity is included and will be recorded
separately after the parent's current documents and check receipts are ready.

Reviewed initial assessment SHA-256:
`b28f8025f48f4fb79a86924dcc6a141ab7421b218d22d1fa525998a002fff5ff`.
The complete nine-file INITIAL_REVIEW_FREEZE matches the inspected files.
Primary source PDF SHA-256:
`3e6219b886d19c7ba00e306ff56560263aac1d23bb1690fa78388918ad05feac`.

## Source-first stage and independent evidence

The ONE new reviewer context is `/root/ob2_instrument_review`, first actual clock
2026-09-12 14:46:32 UTC. SOURCE_FIRST_JUDGMENT.md was sealed at
14:50:45.970412 UTC before INITIAL_ASSESSMENT, SOURCE_FACTS, SELECTION_RECORD or
any parent OB2 finding/decision brief was opened. Direct author assessment/fact
exposure occurred after that seal and was complete by the observed 14:51:01 UTC
clock. The parent's draft decision/session/closeout documents were then read by
14:52:01 UTC. The source-first artifact remains unchanged.

Before the seal I read OB1's complete conditional candidate, reviewed result,
clarification and substantive review as the supplied contract. I read the selected
primary paper's full text and visually inspected both pages and Figs. 1-4, including
apparatus and axes. The paper's published performance was documentary exposure;
no points were extracted, digitized, recalculated or treated as untouched target
data. Page 1 was independently rendered from the pinned PDF; page 2 reused the
parent rendering with independently verified hash. There was no second apparatus
search, external contact or target dataset access.

The source-first conclusion already identified the missing full contract. Direct
review did not reverse it. It tested the author's six source facts, their locations,
electrical/optical frequency distinctions, mode counting, phase/amplitude typing,
conditional phase/error reasoning and the limits of the conclusion.

## Source fidelity and strongest positive support

All six bounded facts are supported at their stated locations in Shen et al.,
*Frequency Modulated Laser Optical Gyroscope* ([primary PDF](https://ocaqpi.ece.ucsb.edu/sites/default/files/2021-02/Frequency%20Modulated%20Laser%20Optical%20Gyroscope.pdf)).
Sec. III reports the PM fiber coil dimensions and rotation table (F1); the Sec. II
continuation gives the laser modulation rate and excursion (F2); Fig. 3 contains
the modulator, photodiode and analyzer (F3). Sec. III compares laser without FM,
laser with FM and ASE at matched photocurrent (F4); Sec. IV acknowledges residual
coherent backscatter and intensity modulation (F5). Sec. V leaves additional
integrated-front-end characterization and fiber-loop replacement as future work
(F6). The fact ledger does not turn reported dimensions or specifications into
our calibrated measurements or error guarantees.

The apparatus diagram is meaningful partial support for a common sensing coil and
interferometric access. A rotation table does not itself disprove stationarity in
a suitable supplied frame. Nevertheless, the report does not provide OB1's full
loop/clock/observer mapping, reciprocal phase transfer or stationarity-error
contract. Separate depicted source/detector components likewise should not be
treated as an automatic impossibility: a valid common-reference reduction could
be established with further information. It is not documented here.

Frequency modulation broadens the optical source to suppress coherent-backscatter
noise; it does not entail that every interference phase becomes unavailable. The
candidate correctly avoids that invalid inference. It asks for the actual driven
field-to-record transfer and its error support. The demonstrated fiber loop is
also correctly kept distinct from the proposed future integrated sensing loop.

## Direct adversarial checks

**Three modes are not three frequency samples.** The source's three comparisons
change source operating conditions, including spectrum/coherence. They are not a
registered equally spaced sequence of three proper optical carrier frequencies
with one shared phase-nuisance class. Equal photocurrent is a reported control;
it cannot silently become cross-frequency phase calibration. A tunable laser and
an optical wavelength spectrum show relevant capability, but no calibrated
three-frequency OB1 acquisition is documented. The reported 10 MHz modulation
rate, 3 GHz excursion/broadening, optical carrier and Fig. 4 electrical-frequency
axis have distinct measurement roles. No numerical conversion is justified or
needed to identify that distinction.

**Amplitude information needs an audited route to signed phase.** The displayed
electrical spectrum and amplitude-versus-rotation outputs do not present OB1's
signed optical phasor. The author's map |A|=|exp(i alpha)A| correctly demonstrates
the generic nonuniqueness of a complex quantity reconstructed from its magnitude.
It is expressly not a detector model. Independently, even an ideal two-field
intensity I=a^2+b^2+2ab cos(phi) has a phi/-phi ambiguity. A phase modulator with
specified reference-sensitive demodulation could supply additional information;
neither argument proves hardware incapacity. The report gives no such signed
quadrature/reconstruction equation, conventions or uncertainty. The assessment
correctly leaves the reconstruction undocumented rather than proving it absent.

**Reported performance is not an OB1 error budget.** Noise-floor change and a
rotation-sensitivity threshold do not directly give per-probe phase errors or
frequency errors. A conversion would need the actual estimator, gain/visibility,
bandwidth/averaging, nuisance calibration, stationarity domain and uncertainty
meaning. The source does not supply these for the OB1 statistic. Equal illumination
also does not independently bound frequency-dependent phase response. Residual
backscatter and intensity modulation are acknowledged effects needing treatment;
they are not independently quantified error bounds in this audit.

**Use A and Use B remain distinct.** Nominal coil geometry and external rotation
control are relevant conventional reference ingredients. They do not complete an
independently predicted marked-geometry delay/error contract for Use A. No new
claim that G405 metric records were physically acquired appears. Use B does not
need O9, and a passing affine-frequency closure would not independently identify
geometry or UDT even if its measurement/error gates were closed. The initial
assessment states those limitations correctly.

## Defect, counterexample, survivor and smallest repair

**D1 — omitted qualification on total-delay/alias support.** In its “What would
have to connect” paragraph, INITIAL_ASSESSMENT says the exact OB1 error argument
needs frequency errors weighted by an independently bounded total effective
delay. The O6 and minimum-support wording is similarly unqualified. OB1's actual
candidate/clarification allows exactly controlled actual spacing or another valid
error treatment, and Use B's unused phasor prediction is invariant across aliases.
Read literally as an unconditional requirement, the abbreviated OB2 wording is
stronger than its source contract and the fixed FRAME_AND_SELECTION O6 qualifier.

An explicit counterexample to unconditional necessity is the ideal admissible
sequence Z_j=exp(i[b+(omega0+j Delta)D]) with exact spacing and any fixed real D.
For every D, including without any supplied finite D_max,

    Z_2 Z_0 / Z_1^2 = exp(i[2b-2b+(omega2+omega0-2omega1)D]) = 1.

All D'=D+2pi k/Delta aliases give the same third prediction with adjusted b.
They need not be resolved to test that prediction. More generally, for actual
frequencies omega0+j Delta+eta_j the extra closure phase is
D(eta0-2eta1+eta2); it is this possibly noncancelling term that needs justified
control. Exact affine-correlated eta_j can cancel in that statistic. This is
elementary source-contract reasoning, not a new noise assumption for the device.

**Strongest survivor:** when using OB1 Eq. 8 with noncancelling frequency errors,
the declared D_max must bound total effective delay, including unresolved linear
instrumental delay. A geometric-only bound is inadequate. Unique-delay alias
selection is an additional identification question, not a prerequisite for the
alias-invariant third-phasor test. For Use A an uncorrected instrumental delay must
still be independently corrected or covered by the existing uncertainty contract.

**Smallest repair:** keep all frozen initial files and add an overlay explicitly
restoring “when noncancelling frequency errors enter the stated error treatment;
exact controlled spacing or another justified treatment is permitted.” Distinguish
that requirement from unique alias resolution if absolute delay identification is
claimed. Apply the same qualifier to current decision/closeout minimum-support
phrasing. No new calibration, phase law or numerical bound is supplied by this
repair. No source theorem changes.

**Outcome after that clarification:** the selected report still does not establish
the phase transfer, signed three-optical-frequency records, independent nuisance
calibration, applicable finite error/statistical treatment or unused confirmation
provenance. Missing complete eligibility therefore does not depend on incorrectly
requiring an alias interval in every version of Use B. No other substantive defect
was found in the initial documentary conclusion or six source facts.

## Actual checks, independence and limits

All 16 exact source pins, nine initial freeze entries and three cached-source pins
matched. Source correspondence returned exit 0 in 0.049624 s with empty stderr,
15280 KiB maximum resident usage, Python 3.10.12 and git 2.34.1. Source-first seal
packaging returned exit 0 in 0.017822 s. Both are metadata/provenance operations,
not scientific test counts. Their exact commands/stdout/stderr/JSON and the reused
capture utility provenance are retained. One thread, 180 s and 2 GiB were the
capture ceilings. No new scientific software test or simulation was needed for
this documentary checklist or the elementary ambiguity/second-difference arguments.

I independently checked grok and the local origin/grok ref at
e89bfe9c6c404e1a70aa334e660ae46327f266ab and reproduced the original 46 name/status
fingerprint 55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2.
Top-level startup and successful task fetch are parent-attributed, not rerun here.
The same-session earlier full397 receipt/stdout/stderr was actually inspected:
start 14:04:07.374205 UTC, exit 0, 402.802356 s, empty stderr. Its exact pins and
current registry, premise summary, verifier and AGENTS match SOURCE_PINS. This is
attributed regression evidence, not a fresh OB2 full397 execution or independent
reproof of every scientific source. No protected payload was opened or hashed;
name/status correspondence does not certify backup completeness.

| Independence axis | Actual record |
|---|---|
| Context | One fresh separately allocated reviewer, no old-context reuse or subdelegation |
| Runtime model/version | UNATTESTED; parent configured gpt-6-astra/xhigh is attributed configuration only |
| Different model | UNTESTED |
| Argument | Sealed source-first documentary assessment, then direct attack; independently reconstructed measurement/error object reasoning |
| Implementation | Not a scientific computational comparison; independently written metadata audit only |
| Shared foundations | OB1's full conditional contract/prior review, exact selected paper, standard elementary algebra and existing capture utility |
| Human specialist/formal proof | UNTESTED |

Not performed: OB1/full-registry scientific reruns, a Maxwell/guide solve, apparatus
experiment, finite-wave certification, target-data extraction, statistical analysis,
new optical transfer derivation, instrument survey, present availability inquiry,
contact, protected/archive access, runtime/configuration changes, GPU production,
commit, scientific promotion or successor dispatch. The named evidence gate is
about this source and protocol, not universal optical absence, physical UDT
failure, device incapacity or physical-law adoption. OB1 remains reviewed
CONDITIONAL UNPROMOTED; existing source grades and open native boundaries do not
change. Parent owns navigation/integration; their final fidelity is still pending.
