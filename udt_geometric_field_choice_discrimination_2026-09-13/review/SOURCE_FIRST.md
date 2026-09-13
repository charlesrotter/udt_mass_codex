# NR2 independent source-first reconstruction

Saved before exposure to any NR2 candidate, proof, implementation or outcome.
This reviewer saw the dispatched problem inputs, WORK_ORDER, SOURCE_MAP,
SOURCE_PINS and SELECTED_PREMISES, and the relevant NR1/source reports listed
below. Thus this is an independent argument within an exposed research direction,
not an independent choice of question or premises.

Fresh context `/root/field_choice_review`; runtime model UNATTESTED;
different-model axis UNTESTED; no subdelegation. First actual reviewer tool clock
was 2026-09-13 12:52:20 UTC. Parent's conservative allocation start is 12:51:59
UTC, source-first deadline 12:59:59, total deadline 13:31:59. Latest observed
clock before writing was 12:54:22 UTC. Parent completed startup/sync and the
new full406 audit (reported PASS, start12:43:14.428401 UTC,404.300133551s,
exit0); these are attributed parent evidence, not a reviewer rerun. Independently
observed branch `grok` and HEAD `f2e5c94d6418dbcd5ca09545f87a208dde7913b0`.
Git status showed pre-existing untracked names plus this untracked package;
protected payload contents were not accessed. All reviewer writes are confined
to this package's review directory; no git mutation.

## Scope and source checks

The complete supplied metric, observer and transverse axes are fixed problem
data (free-and-explored), not a selected physical geometry or detector. The
question is a bounded exact family discrimination question on connected open
intervals in u>0. No boundaries, matter, energy, physical Maxwell identification,
source/readout law, whole-isometry classification or whole-field classification
is supplied. Maximum conclusion: conditional unpromoted geometric identities,
discrimination/degeneracy map and a control. Analytic reasoning here uses no
approximation, grid or scientific subprocess. Future scientific captures, if
needed, use one CPU subprocess/library thread, <=180s/2048MiB via the existing
capture utility, within the allocation deadline.

Read AGENTS.md and CLAUDE.md How we work, DRIVER TRIGGERS and Repo discipline;
applied `.claude/skills/no-shortcuts/SKILL.md` and
`.claude/skills/completeness-map/SKILL.md`. These govern method, not premises.
Read NR1 INITIAL_CANDIDATE, PROFILE_SCOPE_CLARIFICATION, REVIEWED_RESULT and
DIRECT_REVIEW, and the pinned G179, G348, G351 and G352 audit reports and current
GR-filter AUTHORITY_RECORD. NR1's reviewed source exposed the q=u^2 witness,
general Killing identity and pp-wave connection pattern; the new NR2 ODE,
discrimination and cubic-control algebra below was independently reconstructed.

Independently recomputed all 13 entries in NR2 SOURCE_PINS.json with Python
standard-library hashlib: 13 matches, zero mismatches. This certifies byte
correspondence only. Python version observed:3.10.12. SELECTED_PREMISES confirms
G179 regular-pair evaluation, G348 infinitesimal supplied null-screen geometry,
G351 owner-provisional measure conservation and G352 chosen continuous phase
product readout. G312 current GR FILTER ONLY and owner-provisional DDR/locality
do not establish native response-class membership. None selects the fields below.

Read-command record: `cat AGENTS.md`; `cat review/SOURCE_FIRST_REQUEST.md`;
`rg -n '^#{1,4} |DRIVER TRIGGERS|repo discipline' CLAUDE.md`; exact `sed` ranges
1,84 and121,144; `cat WORK_ORDER.md SOURCE_MAP.md SOURCE_PINS.sha256` (last
guessed name absent; read-path error, no scientific failure), then `rg --files`
restricted to this package's PIN/PREMISE names and `cat SOURCE_PINS.json
SELECTED_PREMISES.json`; exact listed skill/source `cat` calls; `git status
--short --branch`; `git rev-parse HEAD`; `python3 --version`. Hash-check command
loaded SOURCE_PINS.json, SHA-256 hashed exactly its 13 `sources` entries, and
reported `{checked:13,mismatches:[],meaning:"byte correspondence only"}`.
No NR2 candidate filename was opened or NR2 scientific code imported.

## Independent family and identification map

Write H0=2(x^2-y^2)/u^2 and

    K=q(u) d_x+r(u) d_y+(q'(u)x+r'(u)y) d_v+c d_v,
    q''=2q/u^2, r''=-2r/u^2, c constant.

Direct metric lowering, including the central direction, gives

    K_flat=q dx+r dy-(q'x+r'y+c)du,
    F=d(K_flat)=2du wedge(q' dx+r' dy).

The prescribed transverse family has

    q=a u^2+b/u,
    r=sqrt(u)[c1 cos(nu log u)+c2 sin(nu log u)], nu=sqrt(7)/2.

These follow from indicial equations m(m-1)=2 and m(m-1)=-2.
The only kernel over an interval is the constant central direction: F=0 forces
q'=r'=0; the nonzero ODE potentials then force q=r=0. At an isolated event F
can vanish for nonzero family data. It is a nonzero null form exactly where
(q',r') is nonzero; its two usual quadratic null invariants vanish also at zero.

Fix the signed convention X=F(U,d_x),Y=F(U,d_y), U=(d_u+d_v)/sqrt(2) at x=y=0.
Then X=sqrt(2)q', Y=sqrt(2)r'. A single event gives only two linear conditions
on four transverse constants and cannot reconstruct the family. A first u-jet
does reconstruct it:

    q=u^2 X'/(2sqrt(2)), q'=X/sqrt(2),
    r=-u^2 Y'/(2sqrt(2)), r'=Y/sqrt(2).

ODE uniqueness supplies the rest. Signed profiles on any nonempty connected
open interval therefore determine q,r and F exactly, leaving only the central
generator kernel. This uses fixed supplied axes and normalization; if axes or
calibration change, the corresponding map must change too.

Two signed samples have a sampling caveat: the q' basis (2u,-u^-2) is independent
at any two distinct positive u. The r' sample matrix is singular when
nu log(u2/u1) is an integer multiple of pi. Otherwise those two samples recover
all four constants. This is a concrete finite-sampling alias, not loss of
continuous-profile identifiability.

Squared coordinate profiles X^2,Y^2 on an interval determine each nonzero real
analytic component only up to its own constant sign. Analyticity rules out
arbitrary sign flips through zeros. A further oblique squared projection,
(X+Y)^2 (or its normalized half), gives the product XY and links component signs
where both components are nonzero, leaving the unavoidable common F -> -F
ambiguity. If one component vanishes identically, its sign is meaningless; if
F=0, orientation and normalization are not recovered. A single-time square map
has larger continuous ambiguity. No claim that finitely many squared samples
give the same classification as full interval profiles is made.

All these forms share the same geometry-only clock/beam outputs when the metric
and the complete query protocol, including supplied phase/labels if used, are
held fixed. Added F contractions are additional mathematical inputs. They do
not cause the metric-only kernel to become a field selector.

## Two distinct phase notions

With R>=0, r=R sqrt(u) cos(nu log u-delta). For R>0, delta is defined modulo
2pi and changes the field profile. Its derivative is

    r'=R u^-1/2[(1/2)cos(theta)-nu sin(theta)]
      =sqrt(2) R u^-1/2 cos(theta+alpha),
    theta=nu log u-delta, alpha=atan(sqrt(7)).

Thus delta+pi negates the y component, invisible to its square alone. R=0
makes delta undefined; delta+2pi gives the identical profile. This parameter
must not be called the uniquely supplied null phase or phase-count label.

Independently, for any smooth h(u) with h' nowhere zero, the SAME form factors as

    F=d[h(u)] wedge {2(q'dx+r'dy)/h'(u)}.

The nonzero null gradient of h does not select h: its time orientation must be
chosen consistently if it is used as the supplied G352 phase. Different h with
the compensating transverse factor leave F unchanged. At the central observer,
the magnitude of phase rate is |h'|/sqrt(2). G352's readout additionally fixes its
own phase spacing and phase-independent label measure; changing h alone while
retaining a fixed spacing can change that chosen readout. Common positive affine
phase/spacing rescaling is a distinct gauge-type freedom already controlled by
G352. No equality between profile delta, factorization h or physical clock counts
is implied by F or the metric.

## Full cubic metric control

Take H_e=H0+epsilon P3, P3=x^3-3xy^2, in the FULL metric
g_e=-2du dv+dx^2+dy^2+H_e du^2. Both determinant -1 and Lorentz signature remain.
P3 is transverse harmonic, so Ric_uu=-(H_xx+H_yy)/2=0 still. For the specified
baseline-ODE K, all Lie components vanish except the possible uu component:

    (L_K g_e)_uu=3epsilon[q(x^2-y^2)-2rxy].

For epsilon!=0 this vanishes identically in x,y precisely when q=r=0. Hence all
nonzero members of the specified transverse family lose Killing status; the
central d_v symmetry remains. This is not a classification of all isometries.

Metric lowering of this K is unchanged because K^u=0. Its form F is therefore
unchanged and remains closed and divergence-free. More generally, for ANY smooth
p_x(u),p_y(u), F=du wedge[p_x dx+p_y dy] has raised components F^{vi}=-p_i,
F^{iv}=p_i. With determinant -1, partial_a F^{ab}=0 directly, and dF=0.
This works for every supplied smooth H(u,x,y) of this metric form, without a
Ricci-flat or Killing hypothesis. It does not exhaust all Maxwell-form fields.
Failure of the sufficient symmetry proof is therefore demonstrably distinct
from failure of the actual field equations.

At x=y=0 the cubic term and its first/second derivatives vanish, so the two full
metric 2-jets agree along the central curves. The connection vanishes there;
the central null curve tangent d_u and timelike curve tangent U retain their
stated normalization/geodesic properties. Central metric clock contractions and
infinitesimal screen/Jacobi transport with the same supplied initial/endpoint
data agree. This does not imply equality of neighboring finite beams or global
observables.

The curvature components, with NR1's convention R_uiuj=-H_ij/2, differ by

    Delta R_uxux=-3epsilon x,
    Delta R_uxuy=+3epsilon y,
    Delta R_uyuy=+3epsilon x.

Thus an explicitly supplied neighboring screen probe at (x,y)=(a,0), a!=0,
with null direction L=d_u+(H_e/2)d_v and axes d_x,d_y detects the curvature
change -3epsilon a in its xx tide. Covariant transverse curvature derivatives
on the center also distinguish it, e.g. Delta(nabla_x R)_uxux=-3epsilon,
because the center connection vanishes. These are third-metric-jet information,
outside the central 2-jet/infinitesimal-Jacobi map. The full transverse geodesic
equations acquire exact quadratic terms:

    x''=2x/u^2+(3epsilon/2)(x^2-y^2),
    y''=-2y/u^2-3epsilon xy.

Their linearization at the central null curve agrees while the nonlinear terms
differ. No finite-beam solution, completeness or physical optical result has
been computed or claimed.

## Source-first conclusion and omissions

The supplied family allows exact profile discrimination with explicit kernel,
sign, sampling and phase ambiguities. The cubic control loses the specified
transverse symmetries but preserves an explicitly wider source-free null-form
family and central 2-jet blindness. These are independent hand reconstructions
for subsequent direct comparison, not an acceptance verdict on an unseen NR2
candidate. No scientific subprocess, independent numerical implementation,
parent-result replay, full406 rerun, generic isometry classification, finite-beam
calculation, observational test, physical adoption or promotion was performed.
