# FCW1 relational/global initial proposal

Status: SEALED INITIAL WHITEBOARD PROPOSAL, UNREVIEWED, UNADOPTED. One proposal,
not a maintained scientific summary. The Mach-inspired role is a simulated
reasoning lens, not a historical endorsement. No peer FCW1 proposal was read
before this file and its seal were written.

## Context and bounded orientation

This is a scoped child of the continuing parent session. Parent startup evidence
is attributed: refreshed origin, full406 audit and host-process inspection belong
to the parent's work order, not independent executions by this context. I checked
the working directory, actual branch `grok`, HEAD
`b90ede0302bcb9c841df3f594ca25b84b4fea107`, and status myself: no tracked changes
were shown; pre-existing untracked work and the active FCW1 workspace were visible.
I read disk AGENTS, current LIVE/HANDOFF blocks, FCW1 WORK_ORDER, required CLAUDE
sections and the applicable no-shortcuts, completeness-map,
solution-space-not-imposition and verifier-before-record protocols.

Central D1/R1/R3–R7/R8/R16–R18 and the exact sources listed in SOURCE_SEAL.json
were inspected in bounded excerpts. The current honest claim is conditional
finite clock prediction on supplied geometry. Ordinary proper clocks, W4
WORKING/POSIT, W5/W6 working clarifications and provisional Local Metric
Sufficiency are retained; physical geometry/assignment remains open. X_max keeps
its WORKING asymptotic global-completion meaning with value/realization/modulation
OPEN and no local-input role. The proposed bounded action is an analytic test of
one explicit, additional UNADOPTED global regularity condition, followed by
cross-examination. No field/source/action, mass population or new local response
is introduced. No numerical test or long solve has run.

## Why this proposal, and a discarded alternative

Full path-labelled Lorentz transport around a loop can distinguish curvature
that a single clock sheet misses. But LKT1 already owns direction-aware
composition and curvature/holonomy, and ECS1 already says that extra directions
can distinguish its transverse mimic. A four-direction transfer reconstruction
would additionally require an operational interface: different rays generally
have different transports, so one cannot pretend that four actual rays provide
four columns of the same arrow. I do not submit that as a new physical lead.

The surviving proposal instead asks whether a definite *global admissibility
condition* can restrict a finite-comparison curve without first choosing a local
response tensor. It can do so conditionally, but the condition below is not
presently a consequence of UDT's founding interpretation.

## R-G1: regular asymptotic completion and a finite-clock pole

### Physical meaning and hypotheses

The proposed UNADOPTED physical condition is that the relevant future asymptotic
geometry admits a regular spacelike conformal completion: an auxiliary metric
`g_bar = Omega^2 g` extends smoothly and nondegenerately to `Omega=0`, with
`Omega>0` in the physical region and a nonzero timelike `dOmega` there. The
auxiliary endpoint is not an event at which a clock hits a wall. It is not a
material boundary, local cutoff, preferred center or extra signal cone. Physical
proper time can continue indefinitely while conformal coordinates have a finite
endpoint. This condition restricts admissible global geometry, rather than adding
a hidden-history label to local response at a fixed metric jet.

For this first bounded calculation impose the **supplied**, spatially flat
homogeneous geometry and actual-clock protocol already used by RCD1:

```
g = -dt^2 + a(t)^2 delta_ij dx^i dx^j,  a>0, a(0)=1,
d eta = dt/a(t), eta(0)=0,
g = Omega(eta)^(-2) [-d eta^2 + delta_ij dx^i dx^j], Omega=1/a.
```

The comoving clocks are ordinary freely falling proper clocks. Their congruence
is a declared test restriction; no preferred universal observer is adopted.
An outward direct ray emitted at time zero reaches the clock at independently
calibrated initial separation `L` when `eta=L`. Nearby emission times define
the differential received/emitted interval ratio

```
p(L)=a(t(L))=1/Omega(L),    dt/dL=p(L).
```

This uses RCD1's conditional null-clock interface. It is not PSW's generic
parallel-velocity preparation, not a finite pulse ratio, and not a depth/distance
identification. All four metric dimensions remain present. Homogeneity and this
protocol are supplied control restrictions, not derived UDT equations.

Now require, on this test sector, an endpoint `L_*` with `Omega` at least C2 up to
it, `Omega(L_*)=0`, and `Omega'(L_*)=-h<0`, where `h>0` has inverse-length units.
This is the concrete content of the proposed regular completion in the displayed
conformal chart. `L_*` is the supremum of this particular first-arrival range in
initial-distance/conformal labels. **No equality between L_* and X_max is claimed
or proposed here.** Attaching the owner's global quantity is a separate open join.

The h and L_* values are FREE-AND-EXPLORED state/control parameters. Normalizing
a(0)=1 fixes the spatial coordinate convention. No value of them comes from
c_E or G_obs; c_E=1 is only a length-unit convention. The new regularity condition
is an explicit UNADOPTED hypothesis, not PINNED-BY-THEORY. The exact clock relation
is pinned to the RCD1 source at its stated conditional scope. There are no
PINNED-BY-HABIT physical inputs.

### Candidate derivation

Write `delta=L_*-L`. Taylor expansion gives

```
Omega(L) = h delta + O(delta^2),
p(L) = 1/(h delta) [1+O(delta)],
t(L) = -(1/h) log(delta) + O(1).
```

The last expression absorbs the dimensional logarithm's reference into the
integration constant. Thus received slowing diverges while the receiving clock
has infinite future proper time. It is an asymptotic sequence of finite signals;
there is no actual reception at L_*.

RCD1's exact kinematic relations, without its optional response equation, give

```
H=p'/p^2=-Omega',
dot H=-Omega Omega'',
R=6 p''/p^3=12 Omega'^2-6 Omega Omega''.
```

Consequently `H -> h`, `dot H -> 0`, `R -> 12 h^2`. In this homogeneous test
sector the Ricci components approach those of positive constant curvature in
the local orthonormal frame. This is an asymptotic statement only: it neither
requires a space form at finite time nor supplies any response equation.

The coefficient-one pole exponent is the proposed discriminator. Finite
conformal range plus divergent redshift alone does not force it.

### Explicit contrast that can reject the proposed extra condition

For FREE-AND-EXPLORED `h>0`, put `x=1-h eta`, `0<=eta<1/h`, and compare

```
Omega_beta=x^beta,     p_beta(L)=(1-hL)^(-beta),     beta=1 or 2.
H=beta h x^(beta-1),
R=6 beta(beta+1) h^2 x^(2 beta-2).
```

Both histories are smooth physical metrics for every finite time; both have the
same finite first-ray range `L_*=1/h`, divergent received slowing there, ordinary
comoving clocks and infinite future comoving proper time. Direct integration is

```
beta=1: t=-log(x)/h,           a(t)=exp(ht),
beta=2: t=(x^(-1)-1)/h,        a(t)=(1+ht)^2.
```

The first passes the proposed condition in this completion; the second has
`Omega'(L_*)=0`, a double pole, `H->0` and `R->0`, so fails its nonzero-gradient
requirement. The auxiliary flat metric is regular in both: the distinction is
the defining function's transversality, not a coordinate metric blowup.
Under smooth conformal changes `Omega_tilde=omega Omega` with finite positive
boundary omega, a zero derivative remains zero. No claim is made here about a
classification of all singular changes of completion or all four-dimensional
extensions.

This explicitly identifies the extra restriction's work. It does not establish
either control as a native UDT history, or refute UDT when beta=2 is excluded.
The controls were chosen to expose the hypothesis, not selected as physical
answers. Positive curves with finite range and infinite proper time admit far
more than these two examples; no census is claimed.

### Surviving alternatives and counterevidence

The extra condition leaves a large interior freedom. Let `b(x)` be any smooth
nonzero bump supported strictly inside `(0,1)`, and choose epsilon sufficiently
small that `1+epsilon b>0`. Then

```
Omega=x [1+epsilon b(x)]
```

has exactly the same initial neighborhood, endpoint neighborhood, pole residue
and L_* as beta=1, while its intervening curvature can differ. It respects Local
Metric Sufficiency: different global formation is represented by different
geometry, and identical local jets carry no extra independent local response.
This is an analytic kinematic survivor, not an on-shell solution of any selected
local equation. A suitable bump therefore defeats the claim that regular
completion alone selects exponential expansion throughout or a unique clock
history. RCD1 already has the exact exponential curve as a parameter-blind sector
of its optional response; that degeneracy survives.

Most seriously, W4/W5/W6, universal observer law and the working X_max meaning do
not presently justify this smooth nonzero-gradient completion condition. An
asymptotic global meaning does not itself dictate conformal differentiability,
boundary causal type or a pole order. The beta=2 control is counterevidence to
equating the proposed condition with mere received-slowing divergence. A physical
reason for imposing this stronger condition remains OPEN; it must not be claimed
as an uncovered premise already binding UDT.

No relay law is assumed. If an immediate echo is considered in this same sector,
RCD1's existing kinematics require `2L<L_*`; that different availability boundary
is not a return inverse, not L_*, and not X_max.

### Closest prior work and exact novelty ceiling

- FSL1 derives the direction-aware finite Lorentz clock law and the necessary
  angular approach for divergent Z. It does not impose this metric completion
  regularity or derive the proposed pole from it.
- LKT1 owns the Lorentz2 connection, scalar-character obstruction and restricted
  path/curvature identities. This proposal adds none of those as a new result.
- RCD1 already derives `p=a(t(L))`, `H=p'/p^2`, `R=6p''/p^3` and the exponential
  curve's response-parameter blindness. The proposal uses those identities and
  asks a different question: what does one explicit global completion hypothesis
  restrict without invoking that response equation?
- FNA1/FPC1 already distinguish static-chart, first-signal and echo limits in
  their supplied space form. No such limit was identified with physical X_max.
- ECS1 and ICN1 demonstrate restricted-record metric ambiguity; MGC1 distinguishes
  global size/scale attachment from a selected clock curve. The smooth bump above
  retains that warning even after the proposed global condition is imposed.
- PSC1's nonlinear response nonselection remains untouched. No weak-response
  pole, action, source sector or f(R) equation is being inferred from this clock
  pole. They are differently typed objects.

Novelty is limited to a proposed **global regularity-to-clock-asymptote** test in
this supplied sector. It is not a new finite readout identity, native law,
existence/uniqueness theorem for UDT, or general impossibility result.

### Concrete next derivation, test design and stopping point

If selected by the parent after cross-examination, one small exact algebra check
can verify the two control families, the conformal/clock curvature identities,
and the bump survivor; no PDE solver is needed. A reviewer should independently
derive the received frequency from affine null transport, rather than checking
only substitution into RCD1's formulas. The calculation fails if the actual
first-clock ratio is not `a(t(L))` under the specified protocol, if regularity
does not imply the simple pole, or if the asserted interior survivor changes its
endpoint/initial neighborhoods. The full argument and hypotheses matter more
than a finite check count.

Finite observations alone cannot confirm or universally refute an unbounded
asymptotic condition without more information. If h, L_* and a bound
`|Omega''|<=M` on a declared final interval are independently justified, Taylor
gives the genuinely finite inequality

```
|1/p(L)-h(L_*-L)| <= (M/2)(L_*-L)^2.
```

A violation rejects that joint condition/protocol/bound. Fitting h, L_* and an
arbitrarily generous M to those same measurements is not confirmation. No such
measurement or derivative bound is supplied here. The proposed bounded test is
therefore analytic, not empirical or an instrument proposal.

Return point: either a reviewed conditional asymptotic lemma with the hypothesis
cost exposed, a defect/counterexample, or an unresolved physical-admission
objection. If no source justifies the new regularity condition, retain it as an
UNADOPTED option or decline it; do not manufacture a mass source, select a scale,
or launch a search for a favorable history. No automatic successor is requested.

## Exposure and omissions

Fresh proposer context, inherited Codex model, no model override and no claim of
different-model review. Exact model identifier was not exposed to this context.
The source equations and parent task constraints were exposed. No FCW1 peer
proposal, test output or critique was read before sealing. These derivations are
author exploration, not independent verification. No scientific script ran,
no full406 audit was independently repeated, no global inverse theorem or
physical regularity justification was proved, and no protected payload was read
or hashed. Source hashes record byte correspondence, not truth or independence.
