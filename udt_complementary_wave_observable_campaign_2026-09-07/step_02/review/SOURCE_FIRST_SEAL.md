# CO2 source-first review seal

2026-09-07 22:18 UTC. Reviewer `/root/co2_design_review`, fresh separate
context; exact model UNKNOWN. Baseline independently checked: grok
9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd. Pinned read-only audit startup,
no git mutation/sync; remote freshness not independently verified. Parent's
three current-status edits/campaign visible; protected untracked payloads
untouched. This reviewer owns only step_02/review/.

## Exposure and source pins before seeing CO2 target

Read AGENTS, bounded LIVE/HANDOFF current blocks, current research and premise
summaries, relevant CLAUDE sections, no-shortcuts/completeness-map/
verifier-before-record skills, CROSS_MODEL_VERIFY, INDEX/MEMORY pointers;
then the frozen campaign log and source ledger, exact G261/G312/G313 rows,
G261 exact W4 derivation, later G312 adoption, G313 exact derivation.
Read the final CO1 candidate and review as disclosed dependencies. Read primary
LAL detector constants, GCN21529, calibration README, and focused official
GWOSC event/O2 source passages from the parent's source cache. No CO2
candidate, code, output or numerical result has been opened. CO1's review
history is known, and published weak Virgo coupling is known; no blind
observational claim is intended.

Independently hashed source bytes:

| Source | SHA256 |
|---|---|
| STARTUP_PREMISE_AUDIT.json |31691c686f06aca6b5eafe221b4d760b5b5ff4b81a9f17b78f7e58f438cfb48c|
| CO1 CANDIDATE.md |c5dd7945858f287845ebfbf6f38e0bdf9bc929e66463abd8b08105959a3d7ad0|
| CO1 FINAL_REVIEW.md |31c578ab9a26beb1e762c4c994c8c92291ed6300c4ae11149a737cdb63cbb11f|
| LALDetectors_gitlab.h |82ac49e8042d4eab0f890e63e3599ae227967aee16c76cd5f6b6b729c8798684|
| gcn21529.txt |facff054809d017d2d411dd9ee48ff89f4bd210a192454cf8d120d98dc89aede|
| calibration_README.txt |fb4650601da797badc8bf9e068f798788842667a5bc27ae035ae5ffd0d311d7e|
| gwosc_event.html |3053c37d5d0b1f8d1ad6423e4ca237449bd687e0eb786c24b12fcf19d91aa288|
| gwosc_o2.html |3ee0ff6cc0fd87d02b160dfc272c301913649f0c538d7c02d1e2853934cc2ab6|

The actual full349-row audit is inspected: exit0, empty stderr,401.315662s;
not independently replayed. Source hashes establish correspondence only.

## Independently reconstructed design criteria

Use the published decimal arm vectors without renormalization. Given an
orthonormal transverse sky basis p,q and a supplied orthogonal celestial-to-
terrestrial map R, the direct scalar arm contractions are

    F_I+ = ((a.p)^2-(a.q)^2-(b.p)^2+(b.q)^2)/2,
    F_Ix = (a.p)(a.q)-(b.p)(b.q).

This supplies a second implementation route independent of constructing D
and contracting two outer-product polarization tensors. No detector physics
is proved by agreeing contractions. The coordinate rotation, distant-source
ICRS-like-to-GCRS identification, time and arm metrology remain supplied.

For F with columns u,v form A=u.u, B=u.v, C=v.v. The eigenvalues of F^T F
are ((A+C) +/- sqrt((A-C)^2+4 B^2))/2; singular values are their positive
square roots. Also det(F^T F)=||u cross v||^2, the sum of squared 2-by2
minors. These independent identities detect false rank passes and avoid an
SVD replay. Compute every two-row determinant, normalize u cross v, and
verify original q^T F residuals. Holdout coefficients may be independently
recovered as -q_training/q_heldout, then checked against each response
column. For unit independent channel variance, residual variance is the
squared norm of the coefficient row (-a,1); training amplification alone is
||a||. With covariance C it is b C b^dagger for centered errors, with b mu
as separate bias. A whitening weight changes rank only if invertible and
changes conditioning. Use separate declared Virgo standard-deviation ratios,
never infer an actual PSD or sensitivity from them.

An algebraic rank2 network supplies one unused contrast for two unrestricted
waveforms. The three possible detector holdouts are proportional versions of
the SAME single contrast, not three tests. A rank1 negative control yields
two null directions but only one waveform combination. A small heldout q
coefficient creates large training-noise amplification after normalizing that
heldout coefficient to one. A small Virgo antenna row can place almost all
unit null weight on Virgo; this gives a formally available constraint whose
actual power against a specified alternative can still be poor. Null tests
cannot detect alternatives lying within col(F).

Rotating p,q by any angle rotates the columns by twice the angle, hence
leaves singular values, row norms, normalized null direction up to sign,
and physical training predictions invariant. Rotation/sky finite stress
points are diagnostic samples, not confidence regions or supremum bounds.
An actually lower-bounded sigma_min exceeding a justified DeltaF norm would
give a conditional perturbation guarantee; merely inspecting finite points
does not. epsilon_L=2 pi f L/c and Earth rotation controls are parameters,
not certified instrument-transfer errors. Geocentric delay signs must be
consistent with a direction TO the source and propagation FROM it.

## Release and inference rejection criteria

Reject any empirical power/significance, untouched-data or independent-test
claim based on design algebra alone. The fixed EM direction is legitimate
query data conditional on association/astrometry; GW-triggered selection and
published outcome exposure must survive. Two free waveform functions do not
remove the supplied weak tensor plane-wave response, calibrated laser readout,
delays, astrometry, finite-arm/time response, error or selection assumptions.

The original special GW170817 cleaned files and their C00 channels must not
inherit C02 calibration uncertainty silently. O2 archive H/L C02 and V1
Repro2A plus the O2 calibration route are a documented NEXT route, subject to
actual file headers, time support, flags and channel/version confirmation.
Hourly pointwise frequency uncertainty medians/+/-1sigma are not deterministic
bounds or a full covariance model. A pre-glitch proposed window must account
for preprocessing support/leakage, not only exclude the central glitch time.
No strain/PSD fit, release certification, binary waveform restriction, new
physical premise, physical identification, grade/canon promotion or GOCE work.

## Execution and return ceiling

At most one short independent CPU child through the already inspected
run_capture.py;512MiB address space,60s CPU/wall, no GPU or installation.
Use standard-library scalar contractions and eigen2x2/minor identities, with
explicit original residuals and a meaningful intentionally broken rank
control. Candidate/source hashes, actual output/versions and skipped checks
will be recorded. This seals method/criteria, not a desired numerical answer.
Review budget35minutes, one same-premise repair/focused rereview if needed.
Maximum return: reviewed conditional static design and bounded practical next
work order, or a narrowed/refuted result/unresolved objection. Different-model,
human-specialist, formal and independently calibrated astrometry axes remain
UNTESTED; fresh context is not any of these.
