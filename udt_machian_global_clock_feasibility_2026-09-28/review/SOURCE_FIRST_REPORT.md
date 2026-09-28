# MGC1 source-first adversarial report

Status: **SOURCE-FIRST STAGE SEALED; DIRECT CANDIDATE VERDICT PENDING.**
Reviewer `/root/mgc1_review`, 2026-09-28, fresh separate context, same inherited
Codex model, exact deployment identifier unavailable. Parent source-first
dispatch and WORK_ORDER disclosed the homothety and ultrastatic-GR ideas before
this review. No author's MGC1 candidate, code or results have been read.
The parent's top-level startup/synchronization is attributed; the reviewer
independently verified branch `grok` and HEAD
`e569de0a06849c4c97bceb9898ee3a64dae9932c`. Unrelated untracked names stayed
visible and untouched. The parent premise audit was pending at this stage.

## Source ownership findings

The required mass authority map supplies conditional branch readings, no
current global physical mass law. Founding W4's WORKING/POSIT universal metric
coupling identifies clock/ruler/free-fall geometry but no field/source law.
W5's WORKING projective position leaves dimensional distance, path population
and X_max open. W6's WORKING co-presence does not select a global time slice,
population or concrete constraint. Accepted OBSERVED c_E and G_obs are usable
inputs; they are not an equation for the metric profile.

G351's standard finite nonnegative label measure and G352's chosen continuous
phase product/readout do not identify physical mass. The area density is
`s/J`, with supplied magnitude and label population. Multiplying the measure
by any positive alpha preserves its source-free conservation and transfer
ratios. G352 cancels that same factor in regular clock-intensity ratios.
Identifying the total measure with cosmic mass would add an unsupported join,
even if a conversion factor were inserted for units. A conditional independently
observed mass attachment remains a legitimate separate possibility.

G374/G375 constrain conformal Einstein metrics on a FIXED supplied local base,
with global positivity/completion and physical size still open. The 2026-09-09
GR authority record controls their inherited G312 labels: Einstein use remains
conditional under GR FILTER ONLY; full class membership is unclosed. One may
not transfer their local equations or finite scale-data count into a native
global matter equation. An independently fixed nonzero curvature scalar also
breaks a naive homothety symmetry: scaling that scalar along with the metric
changes the input. The particular source assumptions must be retained.

G275/G276 already distinguish dimensional attachment from physical prediction:
one matched independent nonzero-weight datum fixes a supplied history's single
homothety. Self-evaluating the same metric and calling that result its anchor
is circular. W5 norm saturation is a populated-boundary issue distinct from
the dimensional multiplier. FSL1 adds a directional clock divergence condition;
ICN1 adds actual two-leg inequalities and echo availability. Neither a finite
spatial extent nor a compactness number supplies them. FCV1 shows why a finite
query cannot be replaced directly by a smooth local response coefficient.

These source records support an **unresolved ownership join**, not a proof that
no consequence of current UDT can exist or that a new physical premise is
necessary. The bounded audit does not exhaust all native arguments.

## Independent seam: equal aggregate inputs, unequal clock ratios

Use the explicitly supplied smooth metric on R x T^3,

    g_epsilon=-[1+epsilon sin(x)]^2 c_E^2 dt^2
              +a^2(dx^2+dy^2+dz^2),
    a>0, |epsilon|<1, x,y,z periodic with period2pi.

The lapse is positive; the spatial metric and its slice volume
`V=(2pi a)^3` do not depend on epsilon. Assign an arbitrary constant scalar
rho on that specified slice. Its integral `M_int=rho V` also does not depend
on epsilon. This is a **supplied scalar integral**, not an identified physical
matter source, conserved universe mass, or native UDT solution. No field
equation is imposed. The topology, foliation, lapse and density are explicit
free-and-explored controls.

The static clocks at x=pi/2 and3pi/2 are freely falling: their spatial
acceleration is proportional to `N N'`, which vanishes at those locations.
Their ordinary proper intervals are `d tau_i=N_i dt`. A chosen stationary
null branch satisfies `dt/dx=a/(c_E N)`; hence its fixed travel delay is
independent of emission time and `dt_o/dt_e=1`. Therefore

    Z=d tau_o/d tau_e=N_o/N_e=(1-epsilon)/(1+epsilon).

At epsilon0 this equals1; at epsilon1/3 it equals1/2, with identical V and
M_int. Reversing the leg gives the reciprocal; the stationary echo product is1.
The branch is chosen explicitly and no inverse-comparison/later-return identity
is assumed. Regularity is needed only for the selected finite comparison.

This construction attacks an unstated inference from aggregate integral and
extent to clock geometry. It establishes that these supplied aggregate data
alone do not fix lapse/clock comparison in this kinematic class. It is **not**
a pair of admitted UDT histories, a Machian-theory refutation, or a claim that
the native conditions cannot distinguish the controls. A candidate may use
such a separator only with that ceiling.

## Scale and boundary checks

At fixed physical units, geometric mass of length-weight1 scaling as
`M_geom -> lambda M_geom` and `R -> lambda R` leaves
`G_obs M_geom/(R c_E^2)` invariant. Holding an independently supplied mass fixed
instead makes this ratio scale as `1/lambda`. Those are different hypotheses.
Thus a compactness relation could fix scale with an independent M, or restrict
dimensionless shape, even though it cannot fix the simultaneous geometric
homothety by itself. Reject a stronger claim that every Machian compactness
relation is devoid of information. Ordinary numerical unit relabelling also
leaves compactness invariant but is not physical homothety; checked separately.

For the exact boost family `r=(k^2-1)/(k^2+1)`, `gamma=(k^2+1)/(2k)`, FSL1 gives
`Z_parallel=1/k` and `Z_transverse=(k^2+1)/(2k)`. As k tends to infinity the
same norm r approaches1, while one clock ratio tends to0 and the other diverges.
At k100 the exact pair is1/100 versus10001/200. Finite rational checks support
the displayed exact identities; their limits follow algebraically, not from
finite sampling. Norm/size language alone cannot be promoted to the directional
clock asymptote or physical X_max.

## Actual checks, limitations and direct-review targets

`source_first_checks.py` passed **24 recorded check groups**:19 symbolic
identities,1 four-case rational family,4 deliberately wrong-formula rejections.
This is not24 independent proofs. The weaker normalization and boundary catches
are diagnostic witnesses, not a general production harness mutation audit.
Run exit0,0.29524069499166217s, maxrss48792KiB, empty stderr. Python3.10.12,
SymPy1.13.1, one process, CPU/wall limit60s, address space512MiB, threads1.
The coordinate Christoffel computation is independently implemented from the
metric definition; the clock ratio uses null arrival/proper intervals. Source
formula checks share mathematical identities with their sources. Same library
and same inherited model are disclosed; different-model/library, human and
formal-proof independence are UNTESTED.

Exact command and receipt: `source_first_run.json`; complete stdout/stderr are
saved alongside it. The shared existing run_capture helper is reused without
modification. Read commands included `git status --short --branch`,
`git rev-parse HEAD`, `cat AGENTS.md`, bounded `sed` of the required CLAUDE
sections and founding sections, `cat` of the exact named reports/protocols,
and a DictReader selection of exact registry IDs. `SOURCE_FIRST_SEAL.json`
pins all load-bearing files and review artifacts. Hashes establish byte
correspondence, not truth or authenticated chronology.

Before any positive direct verdict, inspect:

1. Each R/extent and M/content definition, slice, support, observer and units.
2. Independence of mass attachment; whether the same geometry defines both
   sides of a proposed relation, making the asserted law an identity.
3. Fixed physical data versus co-scaling family parameters; any dimensionless
   shape constraint surviving homothety, and exact candidate domains.
4. A stated causal/null/query route from global relation to ordinary clock
   ratio; retained direction, screen/frame carry and populated asymptote.
5. Current GR FILTER ONLY precedence and label-measure non-identification.
6. External-model labeling and whether a counterexample was falsely admitted
   as native; no unsupported necessity claim for new premises.

Not repeated: underlying historical/source package check suites, full406 audit,
Einstein/global completion proofs, matter-emergence/stability calculations,
observational benchmarks or any protected local work. These omissions bound the
verdict. No candidate-level defect can yet be assigned because no candidate was
read. The narrow surviving direction is a precise conditional attachment or
explicit unresolved matter-geometry-clock join, with no science promotion.
