# Direct adversarial review

Date: 2026-09-28 UTC. Reviewer `/root/metric_bridge_review`, fresh separate
Codex context, GPT-6-family runtime; exact model identifier unavailable.
Verdict: **VERIFIED-WITH-CAVEATS** for the scoped projection/variation result.
No mathematical refutation found. Two wording refinements are requested below;
they do not change the formulas or scientific landing.

## Versions and independence

Direct input is the immutable CANDIDATE_INITIAL.md, SHA-256
`ed96806781d1ce1ba940a8f66283c521b9c8545fe81b59a4be6472ddf8766f0a`.
At initial dispatch CANDIDATE.md matched those bytes. Also inspected parent
check_bridge.py and construction.stdout.json only AFTER the source-first
argument and 47-check run were frozen. DECISION_BRIEF.md and ROADMAP_INSERT.md
were subsequently read for fidelity; their exact reviewed bytes are pinned
in DIRECT_REVIEW_RECORD.json. Parent text construction had received the frozen
reviewer's refinements; parent code/checks preceded that exposure, as disclosed.

Context is separate. Model diversity and human review are UNTESTED. The initial
argument is source-first; the direct stage is candidate-exposed. The 4D connection
implementation was independently written without parent imports. Both authors
use the same standard metric-curvature definition and SymPy, so implementation
independence is not independence of the symbolic engine or mathematics itself.
The direct squared-curvature check uses varied-density coefficients and explicit
integration by parts, plus a minimal two-Christoffel Hessian calculation.

## Attempts to break the argument

1. **Lost components and symmetry.** The pullback is exactly P-Q in the stated
   covariant-metric convention. The metric volume is profile-independent. A
   general time-independent spherical tensor could have a tr entry, but the
   candidate explicitly adds reflection symmetry for the three-component count
   and correctly observes that natural G301 responses inherit it. Angular
   curvature is retained. Rank one and the P=Q, Z arbitrary annihilator follow
   by linear algebra, not from the example count.
2. **Coefficient and degeneracy tests.** Direct curvature gives U,U,V,V, so all
   a,b pullbacks vanish. Scalar-only and zero algebraic strata are retained
   without being smuggled through the original nondegeneracy gates. The positive
   r^4 control is non-Einstein while retaining the zero projection; the candidate
   does not represent it as a model of all UDT premises.
3. **Complementary variations and DDR.** The fixed-volume diagonal map has rank
   two and pure-trace kernel. Its angular-radius direction leaves the original
   areal family and is clearly labelled a chosen mathematical probe. For a!=0,
   the remaining Euler ODE yields exactly the prior conditional Einstein family;
   its two integration constants and positivity restriction are retained. The
   result is neither full nine-direction DDR derivation nor native G301 membership.
4. **A potential false no-go.** Full divergence evaluated on g_f does distinguish
   b when imposed for every profile. Independent direct covariant differentiation
   gives (a/2+b)R', and the candidate now explicitly retains that positive result.
   Its open join is ownership of the off-shell identity, not failure to compute it.
   Zero pullback does not supply unrestricted Helmholtz integrability.
5. **Action reduction.** Exact full 4D curvature with independent N proves the
   displayed boundary identity and both Euler derivatives. Early N=1 restriction
   loses a genuine equation. Compact radial support and per-time/local treatment
   avoid an unstated global boundary or action-integrability assumption. Angular
   inference is explicitly dependent on the full Bianchi identity; lapse testing
   alone is not claimed to reconstruct an arbitrary response. Fixed Lambda
   stationarity remains distinct from DDR's free constant trace datum.
6. **Overgeneralization beyond curvature-linear response.** Independently varied
   the existing R+alpha R^2 density at f+epsilon h. Exact integration by parts
   yields -2alpha r^2 R'', with fourth-derivative coefficient 2alpha r^2. The
   radial/time Hessian difference yields the same full projected response and
   sign. The positive r^4 control is nonzero. A further test-only profile 1+c r^3
   makes the reduced equation vanish but leaves a nonidentity clock/angular
   response difference; it is not proposed as a complete solution or physical
   profile. Thus the candidate's necessary-versus-full distinction survives.

## Actual computations and controls

| Check | Result | Scope |
|---|---|---|
| source_first_checks.py | 47 exact checks PASS; exit 0; 1.298863 s wall | Full connection/Ricci, determinant, covector pairing, rank/annihilator, full divergence, known DDR family, nonidentity controls, full lapse action |
| direct_checks.py | 12 exact checks PASS; exit 0; 0.593910 s wall | Independent B14 varied density, integration-by-parts identity, Hessian projection, signs/weights and controls |

Python 3.10.12, SymPy 1.13.1. CPU only, exact symbolic arithmetic, 120 s cap
per subprocess, no approximation/tolerance/grid/GPU or new physical parameter.
All stdout, stderr, commands, timestamps and script hashes are saved in the
corresponding execution JSON. Empty stderr and zero exits are independently
observed. No executed scientific check failed. During direct-script drafting,
an unexecuted hand-written expected polynomial for the extra r^3 control was
corrected by recomputing U,V before the first run; no failed run was discarded.
An initial read command also attempted a then-absent EXECUTION_RECORD.json;
that non-scientific read failure is recorded in the direct review record.

The nonzero controls are not reported as a full mutation campaign. No new
production guard or general certification harness was introduced. Existing
G301/G310 classification, all-plane proof, prior Helmholtz/canonical work,
R^2 mode/critical-branch results, numerical solvers and global dynamics were
not re-proved or re-run. The parent full406 verifier is separately attributable;
this review does not substitute for its actual completion record.

## Source fidelity and refinements

Current G312 authority owns GR filter-only and affirmed owner-provisional Local
Metric Sufficiency. DDR is owner-provisional, not unadopted, derived or canon.
The candidate's ownership table respects those statuses and the founding
F1--F4/W1/W4--W6 boundaries. G233/G259 delimit prior results rather than being
re-advertised as new discoveries. No source, physical equation, physical speed,
action, response order, foliation, canonical phase space or new correction term
is supplied by the review method.

The cited primary methods were checked on 2026-09-28. Deser and Tekin explicitly
retain two radial functions in equations (1)--(2); their equation (5) has the
opposite scalar-curvature sign to this packet. This supports the narrowly stated
method comparison, not UDT premise ownership. [Deser and Tekin](https://arxiv.org/html/gr-qc/0306114v1)
Fels and Torre distinguish restricted equations and the equations obtained from
a reduced action, with conditions for their equivalence. The candidate correctly
does not assume their general theorem for the extra one-function restriction.
[Fels and Torre](https://arxiv.org/html/gr-qc/0108033v3)

R1, small clarity repair: explicitly state that the three diagonal component
and variation counts precede the coordinate/gauge quotient, and are not physical
degree-of-freedom counts. The strongest surviving statement is the exact raw
pointwise covector projection already proved. No new calculation is needed.

R2, scope refinement: replace the concluding universal-sounding prescription
"Future response selection must use..." by a formulation restricted to continuing
this response-class selection route. The rest of the paragraph already states
the proper bounded ceiling; this avoids unintentionally prescribing every
possible native or global discovery method. No mathematical repair is needed.

The lay brief and roadmap are faithful to the limited result: a concrete failed
shortcut, the retained usefulness of full geometry, known conditional DDR
restriction, conditional full divergence test, and an open native join. They
do not assert all-UDT insufficiency or necessity of a new postulate. Final focused
review should pin the clarified candidate and final brief/roadmap bytes.
