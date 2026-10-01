# PSW1 cross-review — premise fidelity and prepared-clock meaning

Verdict: **VERIFIED-WITH-CAVEATS for the frozen conditional diagnostic and
source-faithful decision scope.** No mandatory scientific repair identified in
this review. No native selector, physical attribution, new premise, empirical
result or canon is accepted. The review does not upgrade any source grade.

Reviewer `/root/psw_fidelity`, 2026-10-01, inherited parent model; exact backend
identifier not exposed. Separate context from the parent/other specialists,
same context that authored fidelity/SOURCE_FIRST.md. This is an exposed
cross-review, not a fresh blind review of its own proposed clock coefficients.
Different-model, human-specialist and formal-proof axes UNTESTED.

## Exact exposure and checks

I independently verified the frozen hashes in CANDIDATE_FREEZE.json:

| File relative to PSW1 | SHA-256 |
|---|---|
| INITIAL_CANDIDATE.md | 95ed91cca818cd6f1b7de819396f61ad2a24dc741f763334ed52e7bf769ad1b1 |
| PRIMARY_METHOD_REFERENCES.md | e7cc54b1e39305d0ad8240bcd1a453a5a6a6366b126c1d7f5a6e4454fed0a43f |
| geometry/SOURCE_FIRST.md | 08d7e12be225f71d02cb2b68766c92b05b26d3af8bca23af5cfb507f44e3be98 |
| tests/SOURCE_FIRST.md | d26c04d1bbae469a32835702b75ebea0a25c154a07f84e268b855c37985880c8 |
| workspace/fidelity/SOURCE_FIRST.md | 7bd0823e27cf9d8210b07e04466cab822978981a7410cb797f58108e1eb0466b |

WORK_ORDER.md and SNAPSHOT.json also matched that freeze. Git still reported
grok at 4953c9ae806d42f0042d4fac14682db12c93143c; no tracked edits were present
at this inspection. The initial source-first files remain unchanged.

All three fixed notes, the parent's synthesis and its method-reference record
were visible before this report. Prior TPS1 compact outcomes and original source
verdicts were already exposed. No scientific scripts or numerical outputs from
the other contexts were used as proof; their reported check counts are attributed,
not independently rerun here. Parent startup/full406 evidence remains attributed
as recorded in my source-first note.

Beyond the already pinned source set, I directly inspected NCI1's
INITIAL_CANDIDATE.md and REPAIR.md and the G402 banking summary. The hashes are
a2769dd02500970475225939f0606ba212bdde6b6a54a3bebdd5023ced1385e1 and
38f0bf9512a426e23e76acba8bca71dcef36b0d1e126ce5f45eabbe269b98dc4.
I opened the primary method links read-only. Ito–Soda equations4–6 state the
quadratic Fermi metric used here; their detector dynamics are not inputs.
[Published Fermi-method source](https://link.springer.com/article/10.1140/epjc/s10052-020-8092-6).
Puetzfeld–Obukhov–Lämmerzahl provide nearby clock-compass context, not evidence
that their protocol equals PSW1's future-null protocol.
[Version2 bibliographic/abstract record](https://arxiv.org/abs/1805.10673v2).
I did not re-read that paper's full technical proof or claim literature-wide
novelty. No external data, field equation or physical model was adopted.

## Adversarial premise audit

1. **Net versus positional.** The candidate's section1 correctly reuses SGE1:
   an additional observable condition must restrict (g,Q), because the fixed
   interface already evaluates Z[g,Q]. Section2/J1 explicitly declines to call
   either the net local coefficient or a GR-matched contrast positional without
   a justified physical implication. This is the chief caveat, not a minor
   qualification. A later presentation must retain it adjacent to the Ricci test.

2. **No preferred observer versus supplied clocks.** The geometric lab data
   (o,U,n,L) define repeated comparisons and transform covariantly. Selecting
   data for a test is not adopting a universal frame or population. Conversely,
   covariance does not prove that Nature selects this preparation or demands
   its sign for every U. The candidate preserves both directions of that
   distinction. A future all-U claim would add a quantifier requiring authority.

3. **Ordinary local physics.** Proper times remain metric proper times. Fermi
   coordinates and lapse factors here express comparisons, not anomalous local
   clock behavior. Finite tidal terms tending to zero with L do not contradict
   the founder's ordinary-local clarification. They also do not certify finite
   SR/GR experimental agreement or select a solar-distance threshold.

4. **Inverse maps versus future signals.** The candidate applies q at the
   actual relay, keeps the same prepared receiver across neighboring emissions,
   and does not substitute q=1/p. The explicit return construction and tests
   below support its physical event matching. F3's ordered inverse law survives
   without being misapplied to the later future leg.

5. **Response versus curvature.** Parent synthesis names electric tidal
   curvature T and DDR's unidentified response E separately. No E=Ric,
   E=T, local response conservation, Einstein law or positive Lambda is inferred.
   The conditional Ric=Lambda g sentence is correctly a mathematical comparison.

6. **Controls versus native countermodels.** The signed lapse and homogeneous
   time-dependent families are supplied controls. They refute only an alleged
   sign inference from their matched preparation/readout, not the complete UDT
   premises. Flat recession is a different initial-motion preparation; it shows
   why net mutual redshift alone does not identify a positional contribution.

7. **Grades.** W4–W6 remain working/provisional; G176/G220 retain conditional
   query scopes; DDR remains OWNER_ADOPTED_PROVISIONAL_POSTULATE; GR remains
   FILTER ONLY and Local Metric Sufficiency owner-provisional. Neither the
   classical geometry used nor this review strengthens CSN, X_max or scale claims.

## Direct challenge to the two future-leg coefficients

I reconstructed a second general4D argument, using R6's endpoint frequency law
rather than differentiating the candidate's truncated arrival map. This is an
analytic cross-check, not a new independently coded implementation. It also
explains why a totally geodesic two-surface is unnecessary at the stated order.

Write e=T(n,n). In the Fermi chart around A, t,x=O(L), the metric has quadratic
spatial corrections and time-dependent curvature coefficients on A. Hence

    partial_t g_mu_nu=O(L^2).

Normalize the affine ray frequency at one endpoint to order one. The exact
geodesic identity for the coordinate-energy quantity C=-k_t is

    dC/dlambda=-(1/2)(partial_t g_mu_nu)k^mu k^nu.

The ray's affine length is O(L) in the regular rescaled lab. Therefore C changes
by a relative O(L^3) on either leg. This is approximate conservation to the
stated order, not an assumed Killing symmetry or imported stationary field law.

At the relay, the coordinate-stationary observer W=partial_t/N has

    N=sqrt(-g_tt)=1+e L^2/2+O(L^3).

W is only a local measurement frame, not the receiver's physical worldline.
The prepared geodesic receiver has physical radial velocity

    v_parallel=-e L^2+O(L^3),
    v_transverse=O(L^2),       gamma=1+O(L^4).

To see why general4D terms do not alter the displayed coefficient: parallel
transported U has no radial spatial component at preparation through this
order, by the radial Riemann antisymmetry; the radial geodesic acceleration is
-eL+O(L^2). Transverse displacement is O(L^3). The initial/received photon
direction differs from +/-n only by O(L^2), so its contraction with the
transverse O(L^2) velocity first enters at O(L^4). The quadratic g_0n and g_nn
radial corrections vanish by the same antisymmetries. No restriction eliminates
the actual transverse degrees of freedom; they are order-counted.

Because -g(k,W)=C/N exactly, local Lorentz contraction at the same relay gives

    p=N/[gamma(1-v_parallel)]+O(L^3),
    q=gamma(1+v_parallel)/N+O(L^3).

At A, N=1 and W=U. Each leg has its own affine normalization, which cancels in
that leg's ratio. Substitution gives

    log p=-e L^2/2+O(L^3),
    log q=-3e L^2/2+O(L^3).

The receiver's radial motion contributes to both legs. Replacing it by a
stationary receiver changes p's leading sign and makes the stationary lapse
return reciprocal, which is exactly the proposed negative control. Replacing
the later return by an inverse correspondence similarly destroys q's coefficient.

This argument uses a fixed smooth compact local geometry and regular rescaled
intersection; smooth ODE dependence yields uniform bounds on the finite
rescaled template. It establishes local asymptotic orders, not a numerical
error constant. R6's exact endpoint identity supplies the proper arrival slope,
so differentiating a bare, uncontrolled flight-time remainder is not needed for
this cross-check. The candidate's C1 qualification is nevertheless necessary
for its own arrival-map derivation and is correctly stated.

## Exact controls, matching and trace limits

For the tests context's a_i(t)=1+kappa_i t^2 controls, at t=0 the spatial metric
is Euclidean and all relevant first derivatives vanish. Thus the radial
spacetime preparation geodesic is straight there, parallel transported U stays
coordinate temporal, and the chosen comoving curves are geodesic. This verifies
the operational matching in this family, not in arbitrary TPS1 coordinates.

Along the selected axis define I(t)=integral_0^t du/a_i(u). The same prepared
worldlines give I(t_b)-I(s)=L and I(t_a)-I(s)=2L. Differentiating these exact
equations at s=0 yields p=a_i(t_b), pq=a_i(t_a); q is their quotient at the
matched relay. The tangent and hyperbolic-tangent formulas follow by direct
integration, with the positive-case 2kL<pi/2 restriction. Every scale factor
must stay positive on the complete experiment; the tests source states this,
and the synthesis's smooth local/metric-degeneracy restrictions inherit it.

These controls corroborate the ratio three and its future-leg interpretation.
They do not independently prove arbitrary4D claims or provide Ric=0 examples.
Their kappa_i carry dimensions and are supplied curvature-control coefficients,
not selected UDT physical scales. The PSD/negative trace claim does not depend
on treating them as native solutions.

The trace statements are exact for the quadratic coefficient:
sum_i T(e_i,e_i)=Ric(U,U). A nonzero real symmetric trace-free T has both
positive and negative eigenvalues; T=0 leaves higher orders open. Thus:

- A positive leading angular mean requires Ric(U,U)<0.
- Positive leading shifts in every direction require negative-definite T.
- Ric=0 forbids those particular nonzero positive quadratic requirements,
  but does not forbid selected positive shifts, higher-order effects, finite
  separation effects, or a different physical assignment.

The synthesis distinguishes all three. A finite triad measures a trace and
does not certify all-direction signs. Comparing g with g_0 at matched initial
frames/proper length/velocity/protocol gives their separate Ricci contractions;
holding coordinate curves fixed would not. An independent matching rule is
still required before the contrast receives physical positional attribution.

## Route B and novelty

NCI1's exact property uses every sufficiently short future null segment, a
single smooth Psi on the domain, and a specified U. The parent preserves these
quantifiers. The equivalence exp(-Psi)U conformal Killing is correctly signed:
constancy of exp(-Psi)omega gives log(omega_B/omega_A)=Psi_B-Psi_A=-log Z.
Local sigma=0 and d alpha=0 do not dispense with global periods; the parent
retains that distinction. Unequal kappa_i fail in a time neighborhood despite
vanishing shear at t=0; equal kappa_i admit either sign. Therefore passing the
criterion cannot by itself isolate an additional positional effect.

Nearest prior work is properly credited: DCI1's congruence-based clock-curvature
map, SGE1's assignment/recovery restrictions, ICN1's actual-return bookkeeping,
CES1's prepared clocks, NCI1's endpoint criterion, and classical clock-compass
methods. The useful increment is the specified release-and-return coefficient
and trace test, not new differential geometry or a native UDT selector. Parent
integration should retain that restricted novelty claim.

## Objection, survivor and decision utility

**Strongest remaining objection:** the test has not obtained an implication
from the founded positional interpretation to its particular positive L^2
coefficient or endpoint-only representation. Choosing either just to select a
desired geometry would introduce a new physical premise. This blocks the
physical-selection claim. It does not block the scoped geometric calculation.

**Smallest repair if a later text overclaims:** restore the adjacent J1 gap,
name the exact extra preparation/quantifier/leading-order requirement, label it
UNADOPTED, and restrict any exclusion to that conjunction. Do not repair by
changing clocks, adding Lambda, subtracting a fitted GR response or discarding
unwanted valid geometries. The frozen candidate already obeys this boundary;
no such repair is presently required by this review.

**Survivor:** a specific, reviewable diagnostic now says what Ric=0 fixes and
what clock preparation is needed to expose it. It is useful to reject a claimed
local implementation once that implementation actually entails the tested
coefficient. A larger Ric=0 survey cannot discover a nonzero value of its
already-fixed Ricci coefficient. This narrow resource conclusion is sound;
it is not a ban on investigating higher-order/finite-distance vacuum geometry
under a separately justified question.

No new scientific CPU check was needed. Omitted: full406 rerun, prior numerical
check replays, TPS1 raw arrays, global geometry, empirical recovery, independent
human/different-model review and final central integration review. Final
integration must bind this report and the other actual reviews to the same
settled text; this report alone does not certify that future integration.
