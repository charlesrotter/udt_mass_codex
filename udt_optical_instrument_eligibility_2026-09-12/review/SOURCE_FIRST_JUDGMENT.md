# OB2 source-first documentary judgment

Reviewer: `/root/ob2_instrument_review`, the ONE fresh separately allocated context.
First actual clock observed: 2026-09-12 14:46:32 UTC. Source-first reasoning was
written before exposure to OB2 INITIAL_ASSESSMENT.md, SOURCE_FACTS.md, selection
narrative or any parent OB2 finding/decision brief. SOURCE_FIRST_SEAL.json records
the actual later seal time and hashes. Hashing the nine frozen files did not expose
their prose. This is staged source-first review, not observational blindness.

Verdict before author assessment exposure: **the selected two-page report does not
document a complete eligible OB1 measurement contract**. It supports several
relevant apparatus components and a reported gyroscope demonstration. The published
mode differs from the fixed three-optical-frequency protocol, while essential
phase-transfer, calibration, error and unused-confirmation joins are undocumented.
Neither physical impossibility nor a claim that this hardware cannot be adapted
follows. Adaptations and other instruments are outside this review.

## Sources, exposure and scope

I read the complete OB1 INITIAL_CANDIDATE, REVIEWED_RESULT, SOURCE_PRESERVING_CLARIFICATION
and substantive review/REVIEW. OB1's earlier review and parts of FINAL_FIDELITY were
therefore exposed: OB1 is the supplied conditional audit contract, not the candidate
being independently assessed here. The combined first tool output was truncated;
the full clarification and substantive review were then read in a bounded call.
The OB1 mathematics and its prior numerical outputs were not replayed or certified
anew. Its full ideal-geometry/guide/clock/quadrature/error hypotheses remain in force.

I read the selected primary report's complete cached text and visually inspected
both PDF pages, including Figs. 1-4, axes and diagram labels. Page 2 was the parent's
cached rendering; I independently rendered page 1 with `pdftoppm -f 1 -l 1
-singlefile -scale-to 1800 -png` from the pinned PDF. Published plots and stated
performance were exposed documentary information, not reserved UDT data; no points
were digitized, fitted or reanalysed. No other apparatus, appendix or target dataset
was opened and no external contact occurred.

Primary source: Y. Shen et al., *Frequency Modulated Laser Optical Gyroscope*,
[author-hosted PDF](https://ocaqpi.ece.ucsb.edu/sites/default/files/2021-02/Frequency%20Modulated%20Laser%20Optical%20Gyroscope.pdf).
PDF SHA-256: `3e6219b886d19c7ba00e306ff56560263aac1d23bb1690fa78388918ad05feac`.
Publication date and present apparatus availability are not established by this audit.
The source record already supplied parent cautions about these points and plot
exposure; that limited framing exposure is disclosed rather than called blind.

## Fixed-requirement assessment from the source

| Requirement | Source-first judgment and exact documentary basis |
|---|---|
| O1 common path/marking/stationarity | Partial hardware support. Sec. III and Fig. 3 show one PM fiber coil, source path, polarizer/circulator/coupling, LiNbO3 phase modulator, photodiode and analyzer. Coil length and diameter are reported, and the setup is on a rotation table. This is relevant loop-interferometer structure; the report supplies no complete OB1 chart/observer/marked-loop mapping or stationarity uncertainty over a three-frequency sequence. Stationary rotation in an appropriate supplied frame is not ruled out merely by the rotation table. |
| O2 coherent delay-to-phase transfer | Missing full join. The report concerns Sagnac interferometry, but suppresses backscattering by deliberate laser frequency modulation/linewidth broadening and compares broadband ASE. That does not prohibit useful interference. It does mean the reported modes do not themselves establish OB1's stationary monochromatic pure-delay transfer with controlled medium, modulation, boundary, polarization and finite-wave corrections. No transfer equation or remainder bound for the OB1 phasors is supplied. |
| O3 recoverable signed complex phase | Undocumented. Fig. 3 shows photodiode to electrical spectrum analyzer; Fig. 4 presents electrical spectral amplitude and amplitude versus rotation. No signed optical comparator/quadrature convention, complex transfer record or calibrated phase recovery is given. Presence of a phase modulator alone does not certify that recovery; it also does not prove phase recovery impossible. |
| O4 three equally spaced proper optical frequencies | The published comparison differs. Sec. III compares the on-chip laser without FM, with FM and the ASE at the same photocurrent. These are three source conditions, not three registered equally spaced monochromatic optical frequencies. The 10 MHz laser modulation rate is not the carrier frequency; the 3 GHz excursion/broadening is not a three-probe specification. Fig. 4's electrical kHz frequency axis is likewise not an optical carrier axis. Fig. 2 does show an optical wavelength spectrum, but supplies no three-clock-calibrated probe sequence. |
| O5 independent response/offset calibration | Undocumented for this use. Equal photocurrent controls detector illumination, not the frequency dependence of optical phase offset, gain or group/phase transfer. Secs. II/IV discuss residual coherent backscatter and additional intensity modulation; those are relevant unbounded contributions here, not evidence that an eligible correction cannot exist. No target-independent phase calibration and residual bound across OB1 probes is given. |
| O6 total effective delay and aliases | Undocumented. Nominal coil size does not by itself bound the entire signed differential/effective delay including unresolved frequency-linear instrument phase. The report gives no OB1 alias interval or calibrated frequency-spacing-error treatment. It would be incorrect to substitute geometric delay alone into the clarified OB1 D_max requirement. |
| O7 applicable finite error or statistical contract | Undocumented. Reported noise-floor improvement, sensitivity threshold, linewidths and amplitude behavior belong to this experiment's quantities and mode. They do not establish finite per-probe phase/frequency/training/calibration errors, correlations, geometry uncertainty or a probability law for the OB1 closure statistic. No conversion to a hard bound is justified. |
| O8 unused confirmation/raw provenance | Undocumented for OB1. The published source-mode comparisons and rotation sweeps are not a fixed unused third-frequency reading. Raw OB1 signed-phase records, processing provenance and exposure split are not supplied by the inspected report. This is no claim about whether unpublished records exist. |
| O9 independent geometric prediction for Use A | Undocumented full contract. Nominal coil dimensions and an externally controlled rotation table are relevant conventional geometric/reference ingredients. The report supplies neither the independent marked metric records and uncertainties of the proposed Use A nor a fully audited alternative geometry-to-delay prediction/error contract. Use B does not require O9, but still lacks O2-O8 and would test only affine-phase consistency. |

The experimental fiber coil in Fig. 3 must not be conflated with a completed
integrated Si3N4 sensing loop: the latter replacement remains future work in Sec. V.
The proposed on-chip front-end and demonstrated fiber apparatus are related but
distinct evidence scopes. A reported tunable laser is also not proof of calibrated
three-frequency phase operation.

## Independent load-bearing reasoning

The mismatch is one of measurement objects and documentary support; it needs no
new scientific software test. Even an ideal two-field intensity readout with
known positive amplitudes a,b has I = a^2+b^2+2ab cos(phi), invariant under
phi -> -phi. A signed phasor exp(i phi) is not generally determined by that one
number. Known modulation and phase-referenced processing might restore suitable
information, but that requires its own specified transfer/calibration. The paper's
modulator plus magnitude output does not provide that specification.

For OB1, phase_j = b+(omega0+j Delta+eta_j)D+e_j. Taking the second difference
leaves D(eta0-2eta1+eta2)+(e0-2e1+e2). Thus the absolute frequency-error term
requires a bound on total effective D, or a justified alternative treatment such
as exact controlled spacing; linewidth, rotation sensitivity or nominal fiber
length cannot simply be inserted as that bound. Changing source mode can also
change transfer and offset, so the cancellation cannot be claimed solely because
there are three experimental traces. These elementary arguments independently
check the relevant object/error joins without reproducing OB1's full computation.

## Startup, provenance, independence and omissions

On-disk AGENTS, CLAUDE method/trigger/repo sections, CROSS_MODEL_VERIFY and the
no-shortcuts, completeness-map and verifier-before-record protocols were read.
The parent's top-level startup and same-session earlier actual full397 are
attributed via STARTUP_RECORD; no fresh sync or verifier execution is claimed.
The first guessed STARTUP_RECORD.md filename was absent; the actual JSON was then
read. A first abbreviated git query returned names rather than hashes; the proper
hash query and captured correspondence audit then independently verified the pins.

The captured source_correspondence audit returned exit 0 at 14:48:41 UTC in
0.049624 seconds, with empty stderr. All 16 source pins, nine frozen initial-file
pins and three cached-source pins match. grok and local origin/grok both equal
e89bfe9c6c404e1a70aa334e660ae46327f266ab. The original 46 untracked name/status
entries reproduce 55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2.
This is name/status correspondence, not protected-payload or backup certification.
The metadata-only script used the existing capture wrapper, one thread and a
180-second/2-GiB ceiling; it is not counted as a scientific eligibility test.

Actual runtime model/version: UNATTESTED. Parent configured gpt-6-astra/xhigh is
attributed configuration only. Context is fresh; source-first reasoning is separate
from direct review; implementation independence is not computational here except
for independently written metadata checks. Different-model, human specialist and
formal-proof axes are UNTESTED. Shared OB1 definitions, the source report and prior
OB1 review are explicit shared foundations. No new physical premise, native optical
law, empirical UDT constraint, metric/scale selection, scientific promotion or
successor dispatch follows. No GPU, target-data analysis, protected payload,
archive, source-package edit, runtime change, commit or subdelegation occurred.
