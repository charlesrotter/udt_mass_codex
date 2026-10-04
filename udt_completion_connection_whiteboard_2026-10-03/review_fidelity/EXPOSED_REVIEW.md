# CCW1 reused physical/fidelity review

Verdict: **VERIFIED-WITH-CAVEATS** for the frozen synthesis's conditional
diagnostics, physical scope and optional recommendation. No blocking defect or
required scientific repair was found. This does not adopt RG, establish a native
physical connection, recertify old packages or attest to central integration
that has not yet been reviewed.

Candidate: INITIAL_SYNTHESIS.md, SHA-256
`1b300a65b544cbf63dacfb5a8a449cd4d638694ef62a25bb7bf38271888dea69`.
CANDIDATE_FREEZE.json SHA-256
`e60420c800ebbbd571255bf3296dce1405880866e04e9fd0146a7fa79d87c540`.
The seal independently verifies those bytes and the saved control capture.

## Context and exposure

Reviewer `/root/ccw_physical` is the REUSED physical contributor context, not
a fresh reviewer. It already authored contributor_physical/REPORT.md, including
the clock-gap argument. This is therefore not independent authorship of that
component. Inherited Codex/GPT-6 family is exposed; exact backend identifier
is unavailable. No different-model, human or formal-assistant review is claimed.

New exposure: parent review dispatch; frozen synthesis and freeze metadata;
geometry and adversarial contributor reports; CHECK_PLAN; check_controls.py;
parent_controls stdout, stderr and capture JSON; CROSS_MODEL_VERIFY. I did not
read the separate fresh reviewer's reports or verdict. My earlier source/owner
reads and source-first seal remain attributed rather than rewritten as blind
exposure. I independently rechecked grok, HEAD28efe475 and status; tracked work
was still clean at this review's opening. Protected payloads remained untouched.

Methods: exposed analytical reconstruction, direct substitutions and exact
clock integrals. No scientific program was run by me. Parent's SymPy output is
inspected evidence, not my independent computational replay. Hash/metadata
verification is mechanical only. Historical full406, normal and57 tests remain
parent-attributed; closure and final integration checks are still pending.

## Load-bearing mathematical checks

1. **Clock-gap derivative and residue.** On the stated actual null correspondence,
   ds/dτ=1/Z=xB and dx/dτ=-xγ/N. Thus ds/dx=-NB/γ. Integrating from the supplied
   regular endpoint s_* at x=0 gives the positive gap ε=integral_0^x NB/γ dv.
   Since the integrand tends to N_*B_*>0, ε/x tends to that value and εZ tends
   to N_*. No uncontrolled remainder is differentiated. This checks the
   proper-time signs and the exact endpoint required by the argument.

2. **Conformal curvature and gauge.** I reconstructed the Ricci contraction
   from C at a b-normal point. The derivative terms give
   2Hess(x)/x+b Box(x)/x+[-2dx dx-b q]/x²; the quadratic C terms give
   [2dx dx-2b q]/x². Their sum yields the displayed Ricci formula and scalar
   x²R[b]+6x Box_b x-12q. With C3 nondegenerate data the first two scalar
   terms vanish and q(p)<0 gives R_*=12κ>0. Under x'=a x,b'=a²b,
   dx'=a dx at p, proving κ and N_* invariance. This does not imply constant
   interior curvature or a field equation.

3. **Saved direct-curvature control.** For b=-N(y)²dx²+dy²+dz²+dw²,
   N=1+y², I independently obtained R[b]=-2N''/N=-4/N, Box_b x=0 and
   q=-1/N², giving R[g]=12/N²-4x²/N. The cross Ricci entry is
   -2N'/(xN)=-4y/(xN); Ric_xx=NN''-3/x² and
   Ric_yy=-N''/N+3/(x²N²), matching the actual saved direct-Christoffel
   calculation. This exposed hand check is not an independent implementation.
   The code computes the physical Christoffels/Ricci rather than simply
   substituting the claimed scalar formula. Its leading-term omission check
   is nonzero at the declared regular rational point.

4. **Clock asymptotic algebra.** The FCL finite additive remainder implies
   x exp(τ/N_*) has a finite positive limit. Combining xZ->1/B_* gives the
   positive finite A and log Z/τ->1/N_*. Since κ=N_*^-2, the curvature-clock
   formula follows. The exact identity tanh(-log Z)+1=2/(1+Z²) gives the
   scalar limit. Neither argument implies convergence of the instantaneous
   logarithmic derivative; the candidate explicitly avoids that stronger claim.

5. **Beta controls and invariant obstruction.** Direct incidence supplies
   z_e=r+d, z_o=r, Z=((r+d)/r)^β. Integrating ds=dη/z_e^β independently gives
   ε=h^-1 log((r+d)/d) for β1 and ε=r/[hd(r+d)] for β2. Their products with
   Z have respectively finite limit1/h and positive divergence. The physical
   β2 scalar is36h²r²->0. Therefore the SAME future tail cannot approach an
   endpoint of the stated RG type in any conformal representation. This
   strengthens a particular negative diagnostic without classifying all ends
   or asserting that the supplied β2 metric is a native UDT model.

6. **Local emitter construction.** A C3 nondegenerate extension and convex
   normal neighborhood are stated, so geodesic flow and endpoint derivatives
   have the needed local regularity. For affine span1,
   F_s=-b(kbar_e,u_e)=E_*>0. Receiver endpoint derivative r'(0)=-N_*n gives
   F_x=N_*[-b(kbar_o,n)]>0, hence s'(0)<0. The physical frequency identity
   -g(x²kbar,u_e)=-b(kbar,u_e) verifies E_* with no missing x_e factor.
   Whole-ray rescaling gives B_*=B0/E_*. Temporal x keeps sufficiently local
   connecting segments interior. The construction supplies a chosen nearby
   source, not a remote source or receiver existence theorem.

7. **Pointwise versus population control.** Holding P constant, the metric's
   spatial Killing momentum and unit normalization give
   u=(-x sqrt(1+P²x²),Px²,0,0). They determine a free geodesic. At x=a with
   P=(1-a^-2)/2, γ=(a+a^-1)/2, and γ-Pa=1/a. Therefore the actual received
   frequency is1 and Z=1. Independently, incidence x_e=x+y(x) gives the
   displayed differentiated clock map. Each chosen receiver's endpoint is
   y(0)=(1-a)/(1+a)>0, so its own later emitter limit is interior. This confirms
   that each receiver can satisfy FCL while the event-indexed population
   violates the desired uniform conclusion through unbounded initial boosts.
   It does not refute compact bounded preparations. The parent code correctly
   differentiates with P held constant before making the population substitution.

## Physical fidelity and proposed next step

The synthesis respects the owner meaning: one geometry, ordinary proper clocks,
founding positional interpretation of c_E, no demand for an additional why,
circumstance-dependent comparisons, and GR FILTER ONLY. No new speed, light law,
source model, E=Ric identification, Omega-distance map or X_max is introduced.

The new local existence result genuinely narrows one earlier supplied
assumption. It is not allowed to erase global/source-specific availability.
The explicit x_e in[0.9,1.1], y=0 to y=2 control has no positive x_o; the
candidate retains that distinction. Technical extension of b is also explicit,
so the proof does not smuggle physical continuation beyond infinite proper time.

The matched-reference formula D_pos->log(N_*/N0_*) is valid only under the
stated same-ε operational matching. Independent source end times do not provide
that matching automatically. Even a nonzero contrast requires an attribution
argument, while identical geometry and query give zero contrast with the pole
intact. This retains the additional-effect requirement without identifying
ordinary cosmological kinematics as newly native physics.

The two future directions retain distinct events and preparations. Inverse-map
reciprocity does not identify them, and the existence of two separately prepared
one-way limits does not guarantee an available immediate echo. Local metric
SR form and late RG behavior are not finite-domain empirical GR certification.
The synthesis does not claim a solar threshold or manufacture its value.

Recommendation B is properly described as the parent's optional next
mathematical test: a declared fixed-emission preparation with incidence and
uniform bounds derived. It is not contributor consensus, RG adoption or a
completed distance law. I regard its quantifier audit as coherent with the
identified gap. A proposed successor would still need a concrete preparation,
budget and stopping scope; this reviewed recommendation does not execute it.

## Caveats and closure

No scientific repair is required for this frozen candidate. The appropriate
maximum claim is conditional diagnostics, bounded adverse controls, local
existence, and an optional next test. No native RG implication or full-premise
insufficiency theorem is established. Candidate section opening statements
that no script had run correctly describe its freeze time, not current status.

Omitted: full FCL proof replay, arbitrary conformal-extension classification,
generic global signals, actual fixed-emission distance theorem, finite-error
asymptote identification, empirical filters, protected material, all registry
proofs, different-model/human/formal verification. Parent controls show four
families/seven cases PASS in0.5244726039236411s; I checked saved hashes/output
and the listed algebra, not a new runtime execution. Final central integration
must be inspected and separately attested before this review can support that
edition. Review does not upgrade scientific grades or authorize adoption.
