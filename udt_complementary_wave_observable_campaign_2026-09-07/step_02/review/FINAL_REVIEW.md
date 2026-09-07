# CO2 final adversarial review and return-packet fidelity

2026-09-07 22:27 UTC. Reviewer `/root/co2_design_review`, fresh separate
context; exact model UNKNOWN. Different-model, human-specialist and formal
verification axes UNTESTED. VERIFIED-WITH-CAVEATS for the pinned conditional
static design, documented next-release route, proposed work order and decision
brief. No load-bearing objection remains at that scope; no repair was required.
This does not certify an instrument/product, evaluate an observed strain
contrast, establish power/coverage, adopt a physical premise, promote science,
or authorize the separately proposed analysis.

## Pinned target and evidence

Paths below are relative to the campaign unless stated otherwise. All listed
hashes were independently checked by this reviewer or inside its saved run.

| Artifact | SHA256 |
|---|---|
| step_02/CANDIDATE.md |bd06415b173dc2a0b32f05f5beb6cdb0cd3ab3a0e08ad0a055bf7653f4f4c087|
| step_02/design_inputs.json |2d17901bfe84069ff4ac2c43eb500f0b3bd844b3136a8ba6d5582a7d710eb38c|
| step_02/design_checks.py |cf836e712dc133a86560cd7d234203b2ec55c40fc5730b51a1697a1b788c0682|
| step_02/design_run.stdout |b89c8e432788842cdbddc1270c3135043e60f12c557cb24725d2162560fdfac2|
| step_02/design_run.json |a0fa6d95af93e0a65e59f2f74ed378e1a7b906fe7795fab15b2cd55a7539c6bc|
| NEXT_WORK_ORDER.md |f9cc992b3c99aec495a56706f379020746cc650a65e9277ed96ca7c517044e70|
| DECISION_BRIEF.md, pending-review header |116d6a2158a1fb61cd93cfba8029ff78c3cf88102d20233054cae6b2082a1292|
| step_02/review/SOURCE_FIRST_SEAL.md |81030b5effa5f19087c20a9969b784d6f22c71051cfb8fa39aaff72aa7b39ff5|
| step_02/review/independent_geometry.py |f5549e2f034fc5025faf0168d27e2a76bdf2110de810015cf46a7dff73086c8a|
| step_02/review/independent_run.stdout |c2a0aaf6364664f3b389568215f63a0795c06557318272c4cd009aed6742b21c|
| step_02/review/independent_run.json |63c49ebadb23047ace194dfddcab5972e45f6e53e67a12453afbbc86317974da|

The CO1 dependency candidate and final review retain hashes c5dd7945858f287845
ebfbf6f38e0bdf9bc929e66463abd8b08105959a3d7ad0 and 31c578ab9a26beb1e762c4
c994c8c92291ed6300c4ae11149a737cdb63cbb11f (line wrapping only). Full unbroken
source hashes are in SOURCE_FIRST_SEAL.md. W4/G261, later G312 adoption and
G313 source hashes independently match the ledger. The current exact registry
hash is ccd1fd2752a5884dfa2864fc9f3904f9dcc7e22557f6d4057e92ec2c54caf81f.
The saved actual349-row audit hash31691c686f06aca6b5eafe221b4d760b5b5ff4b81a9f
17b78f7e58f438cfb48c records exit0/PASS, empty stderr,401.315662s; this audit
was inspected and hashed, not independently replayed.

## Independence and exposure

Before CO2 target exposure, the reviewer read the frozen scope, primary source
constants/coordinates/calibration documentation and admitted scientific sources,
then sealed its own scalar arm-projection, Gram-eigenvalue/minor and null-ratio
derivation. The CO1 proof/review was a disclosed dependency, not CO2 target
proof. Published weak Virgo signal and the event selection were already known.
The source-first seal records those exposures. After sealing, the reviewer
read all producer code/output and candidate/proposal prose directly.

The numerical route is independently implemented standard-library scalar
projections, closed-form 2-by2 Gram eigenvalues, minors and null ratios. It
does not import producer code, NumPy, ERFA or Astropy, and does not call SVD.
The nominal rotation matrix is a SHARED supplied input from the producer:
this axis is not an independent astrometry/IERS certificate. Source arm
constants and nominal sexagesimal query are parsed/reconstructed separately.
Independent coarse GPS/UTC/ERA and fixed-pole rotation checks provide additional
sign/time consistency only. Their equations are conventional methods, not UDT
premises. Exact exposed model identity is UNKNOWN, regardless of context.

## Substantive computation and analytic check

For each detector, the reviewer computes F+ and Fx from the four scalar arm
projections onto the transverse basis. The matrix differs from the producer's
tensor contractions by at most1.1102230246251565e-16. All published arm,
position and midpoint decimals match; lengths are twice midpoints. No arm
renormalization or orthogonality repair occurred. The input precision is not
made metrological exactness by using float64.

The independent Gram entries are A=0.04828399314398574,
B=-0.07129873830189432,C=1.4027041802781652. The sum of squared minors is
0.06264464894014904, agreeing with AC-B². The singular values are
1.185937228829662 and0.21104753658352265, condition5.619289606634778.
All three two-row minors are nonzero. This is a comfortably rank2 nominal
finite design, with one null contrast, inside the declared supplied response.
The independent normalized null is (0.32943652561999254,0.63644277702192,
0.697432553845929), with original response residual8.33e-17.

Null-ratio coefficients independently reproduce all three holdouts and their
original response residuals. H/L training has condition7.660349703188478 and
inverse operator norm6.624486137591255. The V prediction coefficients are
-0.4723561064125047 and-0.912551003695359. The training coefficient norm is
1.0275551691323384. For the declared independent centered-noise comparator,
V residual standard deviations are1.4338304033638667,3.171099119486899 and
10.052654854594909 when Virgo/H-L noise sigma ratios are1,3,10. These are
geometric propagation factors, not measured detector noise.

Rank-nullity and null-ratio algebra show that all three holdouts are
proportional versions of one relation. They are not independent tests.
Covariance propagation requires the centered b C b^dagger convention and
separate b mu bias retained from reviewed CO1. No arbitrary per-channel error
functions may be fitted while claiming a remaining falsifiable relation.

The weighted conditions5.61929,7.28812,7.62411 are consistent with poor
contrast sensitivity despite finite waveform-inference conditioning. In the
analytic limit of infinitely noisy Virgo, the weighted matrix tends to the
rank2 H/L block, while the V-normalized residual noise diverges. Thus a finite
weighted condition number cannot establish useful third-channel test power.
The nominal null is not nearly pure Virgo: all three coefficients matter.
The antenna row norms are0.890432,0.753065,0.301681. A row norm alone is not
an actual signal amplitude for the realized free waveform/polarization, and
the published weak Virgo signal is not equated with that norm.

Three independently recomputed basis rotations preserve the singular values
to5.55e-17 and null direction to numerical tolerance. A non-axis-aligned
rank1 control has singular values sqrt(70),0. A one-sign-corrupted nominal
null produces original response residual0.584519543535652 and is rejected.
Forced-rank2 and double-normalization controls also fail their corresponding
finite assertions. These are explicitly finite reviewer controls. The simple
overhead normalization comparator does not mutate the producer or prove its
real-site normalization correct; independent source-arm contractions supply
that check. No exhaustive catchproof of the producer is claimed.

The nine same-time sky stresses independently agree within1.16e-14 in
condition and5.90e-16 in matrix-change norm. For the other18 cases, an
independently coded fixed-pole ERA rotation comparator differs by at most
1.77e-7 in condition and7.32e-9 in matrix-change norm. This is a disclosed
coarse comparison sharing nominal R, not a replay of full c2t06a or a uniform
time-error bound. The source ERA equation is documented by
[ERFA era00](https://github.com/liberfa/erfa/blob/master/src/era00.c).
The nominal coarse angle discrepancy is5.37e-7rad. GPS-to-UTC and all three
arrival-delay signs/numbers agree. Every displayed arm control parameter
recomputes. Neither finite stress points nor small arm parameters establish
an astrometric or transfer error bound for an empirical null test.

## Primary-source and recommendation audit

Exact official opens independently confirm that
[P1700349](https://dcc.ligo.org/P1700349/public) uses special H/L C00
T1700401 v2/v3 and Virgo Repro1A. The
[GWTC-1 v3 event page](https://gwosc.org/eventapi/html/GWTC-1-confident/GW170817/v3/)
explicitly says its L1 data retain the glitch. The cached
[O2 archive documentation](https://gwosc.org/o2_details/) gives H/L C02 and
Virgo Repro2A and points to calibration documentation. Its
[uncertainty README](https://dcc.ligo.org/public/0177/T2100313/003/README)
identifies hourly H/L complex-response records and a Virgo O2 run record;
pointwise medians/+/-1sigma are neither hard bounds nor a full covariance.
The candidate's separation of these routes is correct. No files' actual
strain headers, calibration archive members, quality masks or time support
were downloaded/validated by this review.

The proposed pre-glitch interval/band is explicitly a candidate for a future
freeze, not a validated or optimized window. Filter support and upstream
witness-noise subtraction must be included in its retained-response/error
check. Injecting signals only after archival preprocessing tests the later
analysis operator; it cannot independently establish what upstream processing
retained. The proposal's requirement for processing provenance and response
leakage must therefore retain its upstream documentation/support component.
This is a controlling implementation limit, not a defect requiring a new
physical premise or unrestricted raw-data/documentation search.

The work order appropriately separates ingestion/off-source work from event
contrast exposure, records prior publication/selection exposure, and requires
release matching and an error/effect-size gate with fresh review before the
one contrast. An inconclusive or power-limited result is a valid stopping
return. No template phase/ellipse/source distance is imposed, while the weak
tensor-plane-wave, association/astrometry and calibrated-instrument assumptions
remain visible. The nominal ICRS-like-to-GCRS identification is not precision
astrometry. Future process timeouts/output/support controls must be fixed in
the proposed execution freeze and measured environment before running.

The decision brief faithfully summarizes the reviewed CO1 dependency and this
CO2 design. Its coefficients/conditioning, one-contrast wording, conditional
instrument law, C00/C02 distinction, power gate, no joint lab/source metric,
no distinctive UDT evidence, no physical adoption and separate proposal
authorization agree with the detailed sources. Its pending-review header may
be replaced with this actual verdict and closure tracking; such status-only
integration does not require another scientific review. Scientific/proposal
content changes would require matching further review.

## Execution, omissions and conclusion ceiling

The sole reviewer CPU child used the inspected existing run_capture.py,
512MiB AS/60s CPU/wall, no GPU/install: Python3.10.12,0.028055804s,
15,360KiB max RSS, exit0, empty stderr, no timeout. Exact command, timestamps,
limits/stdout/stderr are in independent_run.json/.stdout/.stderr. The
producer's saved run reports0.370171s,112,120KiB,exit0/empty stderr and was
inspected, not replayed. No previous source theorem suite, full349 audit,
independent IERS/astrometry calibration, strain/PSD/calibration arrays,
release eligibility, actual sensitivity/significance or coverage was replayed
or inferred. Source-first and target exposure boundaries are preserved.

This review independently observed initial grok HEAD9ed73efe3d7d24a5fd6666
bd904557cf0b24e0fd and the parent's later CO1 integration HEAD
9da534d34fbc4555131244684ce9f2315b6de291. No reviewer git mutation/sync;
remote freshness and a host-wide process inventory were not claimed. A
sandbox ps check found no python3 process at that instant. Only this review
directory was edited. No protected payload reads/hashes, GOCE work, observed
fit, physics/grade/canon/manuscript change or correspondence occurred.

The strongest surviving result is a quantitatively checked static three-site
design and a documented, bounded possible next analysis route. W4 remains
working; G312 premises remain owner-provisional; all supplied response/query
and error assumptions survive. Actual error-controlled information from an
event is still a future gate. CO2 and its return packet are complete at this
conditional reviewed scope, within the35minute review budget.
