# OAA1 mathematical exposed review

Verdict: **VERIFIED-WITH-CAVEATS** for INITIAL_CANDIDATE.md as narrowed by
CLARIFICATIONS.md, together with the exact affine-ceiling counterexample.
This verdict concerns the conditional mathematical derivation and retained
finite evidence. It supplies neither physical/native admission nor canon,
observation confirmation, whole-theory completeness or a global X_max.

The source-first work was sealed before exposure. SOURCE_FIRST_SEAL.json binds
that work; SOURCE_FIRST.md records context/model, source reading, independent
derivation, communication exposure and startup attribution. The parent candidate
and code were read only after the parent explicitly authorized exposure.
EXPOSED_RECOMPUTE_FREEZE.json binds their inspected versions. The candidate hash
is d984271a263fb7b1e1268b27e95512863f29b847820efc08fe6c67f08e88ec69.

## Argument checked against sources

The endpoint frequency times the chosen affine interval is invariant under
affine gauge rescaling. D_e=Z D_o follows exactly, but is not evidence selecting
an observer family or physical distance convention. The tangent-space spatial
projection interpretation is correct on a specified branch and does not require
a globally unique exponential inverse. The candidate properly distinguishes
endpoint normalization from SGE1's integral along an auxiliary observer field.

The actual circular-emitter incidence retains varying b(R), and the independent
source-first calculation agrees with the general constant term C(b), receiver
frequency expansion and resulting D_o->1/H. The source bound supplies uniform
regularity. Smooth x=1/R tails plus a nonzero limiting incidence Jacobian justify
the claimed derivative expansion. For b_*=0, the independently obtained
coefficient is K=a/H+E/H²>0 and the pole residue is (a+E/H)/sqrt(h).
The recovery inequality D_*>=sqrt(a³/(m epsilon)) follows under its stated
same-geometric-data squared-rate tolerance; it is not full recovery or a scale
selection theorem.

The outer-horizon causal obstruction follows from the timelike gradient of r
and the fixed future orientation. It applies to future return from the given
late event, not to every possible two-way query based at another clock or earlier
events. The static radial-clock control is explicitly a separate accelerated
source query. Its logarithmic radar divergence and finite static-slice tail have
the correct coefficients. The original circular-clock radar, if an echo exists,
also has the divergent lower bound derived in SOURCE_FIRST.md; the candidate
does not need an unproved globally unique circular return to establish its
stated late-event obstruction.

The endpoint boost formula changes a physical observer rather than affine gauge;
the candidate correctly avoids treating those boosted endpoint observers as one
fixed-E geodesic history. It also respects the owner's circumstance-dependent
same-law universality. Identical physical metric/query matching to GR gives
identical records. Thus the positive affine construction and the still-open
additional-effect identification are consistently separated.

## Defect, survivor and repair

INITIAL_CANDIDATE section3 originally said that D_* is attained only at infinite
receiver proper time, without restricting the statement to the eventual tail.
The local expansion alone excludes finite attainment only on that tail; it does
not exclude an earlier crossing on the full fixed history. CLARIFICATIONS.md
explicitly repairs that quantifier. I checked and accept this source-preserving
repair. The initial candidate is retained and its equations/checks are unchanged.

The phrase “genuine finite-distance pole” is mathematically defensible only as
the declared endpoint-affine construction in the body. For final central/lay
wording, “receiver-normalized affine-distance pole” is the precise label. It
must not imply a directly measured radar distance, a physical population selected
by UDT, or an unqualified universal maximum. The candidate body already retains
these limitations; this is a clarity recommendation, not an additional defect.

The strongest survivor is a conditional one-way distance-clock asymptote on the
actual circular-source history, a receiver-normalization-specific finite limit,
an explicitly limited pole on the b_*=0 tail, and a causal obstruction to the
particular late source-return echo. The physical positional attachment is OPEN.

## Independent saved-value replay

I inspected the parent freeze, source code, CONSTRUCTION_RESULT.json, actual
parent_initial stdout/stderr and capture receipt. The receipt reports real
returncode0, no timeout, 2GiB address-space enforcement and duration
2.103987434064038 seconds. This is inspection of the recorded parent run, not
a claim to have rerun its implementation.

The separately frozen recompute_saved.py loads only saved 70-digit records,
never calls the parent code, and recomputes four incidences (E=1,10 and
R=10^3,10^6) at 60/100 digits. It integrates the affine interval and U/P directly
in logarithmic radius, checks original incidence equations using saved b,t_e,
contracts the original EF metric vectors, and reconstructs both affine lengths,
Z, deficits and the residue comparison from independently derived coefficients.
It also recomputes two static radial radar/slice interval controls at both
precisions using a near-horizon integration variable.

All twelve exposed finite cases passed without retries. Maximum scaled saved-
value error was 2.296837151367574e-57 for the eight incidence checks and
1.4362709791311182e-53 for the four radar/slice checks. The frozen thresholds
were respectively 1e-50 and 1e-45. The run took 2.4065284729003906 seconds.
All raw values, input/code hashes, stdout/stderr and failures policy are saved
in the assigned review directory. These are high-precision finite checks,
not interval certification; the argument owns the limiting statements.

Together with the 18 source-first cases, there are 30 finite floating-point
cases in this review. No unreported numerical failures, parameter changes,
root-stop relaxation or discarded outcomes occurred.

## Exact above-limit certificate

The parent provided a separate rational certificate for the source-first
counterexample m=1,a=3001/1000,H=9/50,E=1,
b_*=-999*a/(1000 sqrt(f(a))). I inspected its written proof, frozen code,
result and run receipt. Independently, check_exact_certificate.py uses SymPy
rationals to rebuild b²,S² and the source inequalities, prove

    d(s²/S²)/dr = 2b²(r-3m)/(S²r^4)>0,

and verify all nine stored right-endpoint lower bounds. The intervals cover
[a,6] without gaps. The omitted tail is strictly positive because r>2m and
b²>0 imply s/S<1. The certificate's J_lower=341133/100000 and S_lower=14/5
therefore give the exact positive bound

    B > 8991379/1134000 > 0.

All nine deliberately doubled q bounds were independently rejected, so the
certificate test is not vacuous. This certifies the sign by exact rational
arithmetic and analytic monotonicity, not by rounding the finite decimal result.
The counterexample invalidates a universal below-limit/ceiling interpretation
within the admitted circular-test-clock family. It does not refute the b_*=0
tail, a stable-orbit subfamily not tested here, a different distance convention,
or the UDT postulate set.

Resource-history disclosure: the first exact rational pass passed mathematically
but its reviewer script omitted enforcement of the declared 2GiB address-space
cap. Its original code/freeze/result/stdout/stderr are preserved in exact_initial/.
I added only RLIMIT_AS enforcement, froze that resource-wrapper repair and reran
the same certificate and negative controls successfully. No science or numerical
tolerance changed. The 30 floating-point cases plus both sets of nine rational
checks and nine negative controls total 66 if every certificate/control replay
is conservatively counted toward the work-order's 100-case budget. The per-run
EXACT_CERTIFICATE_RESULT count48 includes one certificate run plus the30 floats;
the complete history count is66 as recorded in the resource-repair freeze.

## Review limits and next stage

Fresh-context/same-model, independent argument and implementation are actual
properties of this review. Different-model/human review is unavailable and is
not implied. Same-code ratio/assertion checks are consistency checks only.
I did not replay the full premise registry, CPR1 curvature/geodesic derivation,
all parent finite inputs, native response admission, astronomical source/angular
reduction or observations. These are unchanged source premises or open gates.

No protected payload, registry, CANON or maintained central document was changed
by this reviewer. Exact final integration/version-binding review remains a
separate stage after the parent supplies the concrete changed central files.
