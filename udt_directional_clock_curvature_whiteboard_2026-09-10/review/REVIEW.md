# DCI1 fresh adversarial review and focused R1 review

**Verdict: VERIFIED-WITH-CAVEATS. R1 accepted. No load-bearing mathematical objection
remains in the frozen candidate.** This is a reviewed conditional geometric application,
UNPROMOTED, with no scientific adoption, new physical premise, or canon consequence.

Reviewer: `/root/clock_kernel_adversarial_review`, a fresh separate context assigned only
adversarial review, not construction. Exact runtime model/version UNATTESTED; inherited
model, no different-model claim. Start 2026-09-10 20:24:33 UTC; scientific and R1 evidence
completed through 20:33:02 UTC, within the authorized window and review allocation.

## Versions, exposure and independence

Independently observed branch `grok`, HEAD
`896da97dc2484b72fa346d0c0ab17055a1dd6fcd`, and the dispatched untracked package.
Scoped status, rather than inspection of unrelated payloads, was used. Top-level startup,
fetch/ff-only synchronization and the required 365-row premise-verifier pass are attributed
to the parent; I did not rerun or independently certify those processes.

Read WORK_ORDER and DATA_FREEZE first, then AGENTS and required CLAUDE sections and
the assigned verifier-before-record, solution-space-not-imposition and no-shortcuts
protocols. PRE_CANDIDATE_REASONING.md was saved before opening the candidate text or
constructor code/results. It contains my own data-map derivation and planned attacks.
This is not blindness to the task, data freeze or proposed motion channels. Subsequently
read the candidate, source notes, relevant pinned reports, constructor argument/results,
and later constructor implementations. Both independent review scripts were written
without importing the author, partner or reused NCI1 geometry implementations. The first
script was written and executed before constructor-code exposure; the second followed
the discovered author-test weakness. No blindness is claimed after exposure.

The frozen scientific candidate was checked repeatedly and remains SHA256
`b11326b4f316f675a9c3ecc596d47e33c0e39215c591fddde1013c37c68d2375`.
SOURCE_CHECKS.json verifies all 15 supplied source hashes and equality of all six frozen
registry rows to the current exact rows. FREEZE_PRESERVATION_CHECK.json verifies all
ten initial-freeze entries; the initial author script is checked at its preserved path.
These establish correspondence, not scientific truth or independent chronology.

## Argument attacked and strongest survivor

The strongest surviving statement is exactly the factorization through the declared
ideal map, for every supplied smooth local four-dimensional Lorentz metric and smooth
future unit observer congruence:

    Ric(U,U) = 3 dot(m) - 3 m^2 - (15/2) V + A + W.

It uses the frozen curvature sign, A=the full spacetime divergence of acceleration, and
W=w_ab w^ab, without a factor 1/2. No field equation or physical interpretation of null
queries is required. This does not prove arbitrary record tuples realizable, recover the
whole metric/curvature, or establish a unique minimum encoding. Only A+W is required
from those two scalars for this target.

My derivation, independently formed before text exposure, follows these load-bearing
steps. For affine null k, metric compatibility gives k(omega)=-k^a k^b nabla_a U_b.
With k=omega(U+n), dividing by omega squared gives q=-a.n-S(n,n). The symmetric
spatial derivative S is H times the rest metric plus shear. Unit normalization removes
the other time slots, and antisymmetry removes vorticity. The exact sphere second and
fourth moments give m=-H and V=2 sigma_ab sigma^ab/15; the dipole and full trace-free
quadrupole inversions in candidate equation (2) have the correct coefficients and signs.

For the positive curvature result, expand div(nabla_U U). The contracted commutator is
U^b[nabla_a,nabla_b]U^a=Ric(U,U) in the stated convention. The remaining derivative
product is tr((S+w)^2)=theta^2/3+sigma^2-W. The acceleration block does not contribute
to this trace; adding an extra acceleration-square term here would be wrong. Substituting
theta=-3m gives the displayed formula. The linear-lapse control independently distinguishes
full divergence from projected spatial divergence, whose difference is acceleration norm
squared. These are mathematical statements about the supplied geometry.

Constant positive affine rescaling multiplies omega and the logarithmic slope by the
same factor, so their quotient is invariant. Reporting an unnormalized slope would fail
away from the specified initial omega=1 convention. The angular mean is a scalar under
smooth rotations of reporting frames; U(m) needs neither a physical frame-transport law
nor a derivative along the null branch. Congruence vorticity cannot be removed by rotating
the reporting frame. The candidate respects all these distinctions.

## Independent actual-metric evidence

The first program independently differentiates metric and observer expressions to their
point jets. It computes inverse-metric derivatives from d(g^-1 g)=0, Christoffels and
coordinate Ricci directly, before comparing them to kinematic quantities. It never defines
Ricci from the target formula. A separate noncoordinate Koszul implementation computes
the twist example's tidal components as (b^2/4,b^2/4,0), confirming the Ricci sign and
full vorticity norm. Explicit coframes or positive lapse/scale factors establish local
Lorentz signature and smoothness; unit observers are checked as fields.

| Metric test | Mean | Mean drift | V | A | W | Direct Ric(U,U) |
|---|---:|---:|---:|---:|---:|---:|
| Drift family at t=0 | 0 | -beta | 0 | 0 | 0 | -3 beta |
| Static central lapse | 0 | 0 | 0 | 3 kappa | 0 | 3 kappa |
| Unit Killing twist | 0 | 0 | 0 | 0 | b^2/2 | b^2/2 |
| Opposite diagonal rates | 0 | 0 | 4 s^2/15 | 0 | 0 | -2 s^2 |
| Linear lapse | 0 | 0 | 0 | 0 | 0 | 0 |
| Mixed metric | -2/3 | -1 | 28/45 | 9 | 8 | 8 |

The mixed metric is explicitly saved in check_independent.py. It has nonzero expansion,
shear, acceleration and vorticity simultaneously; it was added to probe interactions
hidden by the separate witnesses, not to claim a census. The linear-lapse acceleration
at the event is (0,alpha,0,0), while its projected spatial divergence is -alpha^2 and
full divergence is zero. Wrong omission, vorticity factor, curvature-sign, total-variance,
and divergence substitutions give nonzero exact residuals in saved output.

The first program computes m and its derivative via the analytically established trace
relation. To avoid presenting that as a separate clock-data extraction, the second program
independently computes q=-L_U g(k,k)/2, retains t along the central observer, normalizes
the spatial frame there, averages q, and only then differentiates the mean. It obtains
m=-beta t for the drift family and m=-(3t+2)/3 for the mixed metric. For the static lapse
q=0 with t still free. For the twist, L_U g=0 is checked before any worldline restriction.
Both exact programs pass; their outputs are witness evidence, while the argument above
owns the universal quantifier. Generated metric-derived records in these tests are not
claimed to be independently acquired physical measurements.

## Omitted data, source ownership and limits

Each actual-metric example genuinely defeats exact reconstruction under its specified
reduced map. The static central observer acceleration and its time derivatives vanish,
but neighborhood divergence can vary. The unit Killing family agrees on the whole scalar
slope field and A while Ric(U,U) changes. Its constant null energy also implies zero
finite scalar depths along each metric's own branches. The candidate correctly excludes
equality of branch-incidence domains, endpoint maps, flight times, paths, full pullbacks
and screen/frame transport. Retaining those labels could supply extra geometric data;
the scalar-value witness is not a counterexample to every possible observation map.

Omission does not mean absence of every constraint. W is nonnegative because it is a
squared spatial tensor norm. Thus known A and clock terms imply
Ric(U,U)>=3 dot(m)-3m^2-(15/2)V+A, with equality iff w=0 at the event.
The brief's bound is correct; it claims neither exact recovery without W nor necessity of
each separate channel under every alternative encoding.

G220 supplies the regular query and its orientation/sign. G215/G216 preserve the distinction
between unit proper time and a supplied comparison germ. NCI1 already owns the directional
contraction and homogeneous shear kinematics; DCI1 re-derives rather than upgrades that
reviewed UNPROMOTED bridge. Its endpoint-potential criterion is not silently assumed.
G333's reviewed report concerns a restricted Gaussian-normal spatial pair first jet;
G358 concerns ideal Jacobi tides in a conditional Einstein arena. Neither scoped result
is the complete present data map. No repository-wide or literature-wide nonduplication
claim was verified. G312's current filter-only authority is preserved.

The curvature identity is standard Raychaudhuri geometry. I checked the primary
[Abreu–Visser paper](https://arxiv.org/pdf/1012.4806), whose retrieved PDF header identifies
v1, section II equations (1)–(9). It treats arbitrary unit timelike congruences and uses
the same full shear/vorticity squared norms. No physical-fluid or gravity equation is
needed for that identity. The initial explicit-v1 URL had a cache-miss retrieval failure;
the unversioned arXiv PDF then succeeded. This is attribution and method verification,
not a new scientific premise or novelty claim.

Operational access to calibrated infinitesimal null slopes, direction labels, observer-time
mean drift, A and W remains OPEN. Separately supplied is an input-role declaration,
not statistical independence or proven instrument accessibility. Using a fully known metric
to compute A/W and then claiming independent clock-only curvature recovery would be circular.
The candidate and brief explicitly avoid that claim.

## Initial diagnostic defect and focused R1 review

Initial scientific verdict: VERIFIED-WITH-CAVEATS, with one non-load-bearing diagnostic
objection. In the original author script, static_time_constancy differentiated q0 after
the origin substitution had already set t=0. This cannot establish time constancy. The
mathematical survivor was the full candidate: stationarity, the partner's spatial-only
calculation, and the independent retained-t review check establish the assertion directly.
Smallest repair: retain t until after the central-worldline derivative and preserve/exclude
the old diagnostic. No equation, premise, metric or data-map repair was needed.

The parent implemented exactly this check-only R1. I inspected the source diff and verified:

- Original source at checks/INITIAL_check_candidate.py has SHA256
  `227480dfe2f1da4b54be493a8cba3e2f9d8f87ee3a33fc69742aed7bd74137e4`.
- Corrected check_candidate.py has SHA256
  `0c7f7a3075fb72e94a2bd461eff6022e0241ba92786614dc7f31628830fa1d3f`.
- REPAIR.md has SHA256
  `13d0b4287e0b1242d51113821dac002295ea5e5484be0074948d015bc77fbd37`.
- The original exit-zero run and source remain unchanged; AUTHOR_01_EXCLUSION.json
  excludes the vacuous check as evidence instead of altering its historical outcome.
- The repaired central expression is restricted only in x,y,z. Its null-at-origin vector
  is valid on the central worldline, where the lapse is one at every t; no off-line null
  assertion is needed from the intermediate expression.
- The deliberately time-dependent q+t diagnostic exposes the old evaluate-time-first
  result zero, while the repaired derivative is one and is rejected. This mutant tests
  the derivative-order mechanism, not a new physical condition or a metric solution.

I independently executed the corrected full author script. It exited zero with 51 reported
diagnostics (41 exact identities and 10 rejection controls); the new mutant residual is one.
This execution is labeled same-code repair regression, separate from the new review
implementations and analytical argument. R1 is accepted; the candidate bytes did not change.

The decision brief's substantive text at SHA256
`f696a37dc917d42996f9ba9ee785e45d29bf232845c4531f000e4b1c8233c296`
is fidelity accepted with these boundaries. It correctly adds the W>=0 implication,
retains the finite-depth/full-incidence distinction, discloses R1 and the initial failure,
and avoids claiming every full record necessary. Its pending-review status may be updated
to this verdict and linked to this review; such factual status changes do not expand the
scientific conclusion. No successor work or scientific promotion follows from this review.

## Executed commands, resources and omissions

The exact computational subprocess commands were:

    python3 udt_directional_clock_curvature_whiteboard_2026-09-10/review/check_independent.py
    python3 udt_directional_clock_curvature_whiteboard_2026-09-10/review/check_record_data.py
    python3 udt_directional_clock_curvature_whiteboard_2026-09-10/check_candidate.py

Each was wrapped with timeout=120 seconds and stdout/stderr capture. run_01, run_02 and
run_03_author_replay files preserve UTC timing, exact command, script hash, exit code and
actual outputs. All exit codes were zero, all stderr empty, and no reviewer computation
failed or timed out. Versions independently printed: Python 3.10.12, SymPy 1.13.1.
CPU exact symbolic/rational arithmetic only; no floating-point tolerance, GPU, grid,
long solve or source/package mutation. All reviewer-created files are under review/.

Read-only hash/registry checks and scoped git status/HEAD checks are saved separately.
No claim is made to have replayed the original G220/G215/G216/G333/G358 campaigns,
NCI1 global integrability proof, all author mutation cases with independent code,
all historical repairs, the 365-row verifier, unrelated repository regressions, physical
instrument behavior, noisy/finite sampling, global causal structure, full field equations,
protected work, backup completeness, or final commit/push. The author repair replay
does not become independent scientific evidence by being executed in this context.
