# PCW1 initial synthesis — physical connections for discussion

**UNADOPTED PROPOSALS.** Three specialist contexts proposed five connections.
Their initial notes, exact diagnostic checks and cyclic peer challenges are
preserved. This synthesis ranks research questions, not physical truth. It
adds no field equation to UDT and proves no full-theory underdetermination.
Novelty is relative to the cited inspected work, not the entire literature.

## First candidate: the response of a collection of clock comparisons

The missing link is the physical meaning of the response constrained by DDR.
L1 proposes that it is the response of a physically specified collection of
received-clock comparisons to a change in geometry. For regular queries Q_g(q),
positive measure dμ_g(q), and raw net received ratio Z, put

\[
D_g(q)=\log Z[g,Q_g(q)],\qquad
\mathcal C[g]=\tfrac12\int D_g(q)^2\,d\mu_g(q).
\]

The new physical conjecture is stationarity of C under reciprocal metric
strains. If the full derivative exists and has a smooth volume representation,

\[
\delta\mathcal C[h]=\int D\,\delta D[h]\,d\mu
 +\tfrac12\int D^2\,\delta(d\mu)
 =\int E_{\mathcal C}^{ab}h_{ab}\,dV_g,
\]

DDR would give TF(E_C)=0. This is a proposed identification, not a consequence
of inverse-map reciprocity. D includes ordinary Doppler and gravitational
shifts; no additional redshift factor or subtraction of a GR target is allowed.
For inverse descriptions both D and its variation change sign, so squaring does
not cancel their contributions. Actual future return legs are different queries.

FCV1 already derived a single comparison's full metric variation and showed why
one nonzero ray-supported derivative cannot be a smooth volume response. L1
asks whether a physically justified continuum of such derivatives supplies one.
FE1 instead identifies an infinitesimal volume response and recovers Ricci.
The new content is the ensemble-response identification and stationarity rule,
including its query/measure specification. Averaging alone proves neither
smoothing nor finite-local-jet dependence; smooth and local are different claims. The integral and its differentiated
terms must be finite with a justified interchange of differentiation and
integration; normalization alone does not bound an unbounded clock contrast.

This is the closest proposal to UDT's clock-comparison starting point, but its
physical justification is incomplete. A uniform finite measure on all timelike
unit observers is unavailable: the invariant hyperboloid volume contains
sinh²(r) dr dΩ and diverges. A physical rest distribution is additional state
information, while a cutoff or chosen weighting would be an added model choice.
Local Metric Sufficiency remains a requirement if E_C is offered as its local
response; a genuinely justified local limit or different explicit global role
would have to be demonstrated, not assumed.

The initial SR diagnostic exposes the earliest decision. For flat
g_ε=−e^(−2ε)dt²+e^(2ε)dx²+dy²+dz² and fixed straight coordinate clocks
x=0, x=b+vt (0<v<1), D_ε=atanh(e^(2ε)v). Thus

\[
\partial_\epsilon(D_\epsilon^2/2)|_0
 ={2v\operatorname{atanh}v\over1-v^2}>0.
\]

Keeping physical rapidity fixed instead gives zero. These variations have
different physical protocols; this is not a coordinate-invariance violation.
At a comoving flat baseline D=0, first variation is zero trivially, so that pass
would establish no geometry selection. A full ensemble need not equal this
one-query witness, but its preparation and weights cannot be left unspecified.

**Recommended bounded next question:** Can one explicitly physically justified
protocol and ensemble yield a nonvacuous reciprocal response while preserving
ordinary SR and satisfying the proposed locality requirement? Freeze the
protocol, finite integrable measure, variation and branch before evaluating a
target geometry. Use a covariantly prepared Minkowski ensemble with nonzero
Doppler contrasts, physically fixed initial rapidities/separations and compact
interior metric variations, carrying the full ray, endpoint and measure terms.
Reject that candidate if it needs tuned weights, a GR subtraction, an unsupported
locality claim, or an unphysical penalty for ordinary relative motion. Do not
proceed to a galaxy or redshift fit until this calculation survives. This is a
concrete proposal-construction/test question; the needed protocol has not yet
been supplied, and this whiteboard does not authorize a successor campaign.

## Second candidate: radiation identifies the cosmic comparison clocks

C1 proposes an external conventional kinetic interface: a finite positive
massless population travels collisionlessly on metric null geodesics and is
exactly isotropic for one timelike congruence U throughout an open region,
with f=F(ω/Θ), ω=−g(U,k), Θ>0 and nonconstant smooth F. The physical comparison
clocks are identified with that population's rest flow. Isotropy is over all
directions for the selected U at each event, not every boosted observer.
Θ is a spectral scale; a Planck spectrum, radiation origin and thermal history
are not assumed. A physical rest frame is not a preferred spacetime center.

Liouville transport then implies β=U/Θ is conformal Killing:
∇_(a β_b)=ψg_ab. Equivalently shear vanishes, a=−DlogΘ and
div(U)/3=−UlogΘ. Along the corresponding regular null comparison,
Z=Θ_e/Θ_o. This is the established isotropic-radiation connection, not new
mathematics: [Clarkson–Barrett](https://arxiv.org/pdf/gr-qc/9906097).
G402/CGW1 already contain the relevant conformal-Killing clock class. The added
idea is its physical population/observer identification, not a new restriction
on that class for supplied U.

A preserved exact control is
g=−dt²+A²(t)[dx²+dy²+exp(2κx)dz²], U=∂t and Θ=1/A.
For arbitrary smooth positive A, scalar curvature is
6A''/A+6(A'/A)²−2κ²/A², yet the regular radial clock maps have
Z=A_o/A_e independent of κ. These supplied geometries are not native-admitted
solutions. They expose this proposal's remaining freedom, not all-UDT freedom.

**Rank secondary.** On any independently motivated metric/population, evaluate
the original Liouville residual and conformal-Killing condition before computing
Z. An expanding comparison already realizes the relationship; the proposal does
not establish an additional positional effect beyond that or select A, curvature,
a response equation, CMB features or X_max. It offers an observer-assignment
test, not the requested missing distance law. It also admits ordinary static gravitational redshift: for a timelike Killing
field ξ=N U and Θ=c/N, β=ξ/c is Killing and Z=N_o/N_e. Thus expansion is
not a universal consequence either. Θ and the population must be independently
specified, not reconstructed from the very Z being tested. Nearly isotropic data require an
additional controlled approximation; exact isotropy here is only a trial premise.

## Third candidate: microscopic vacuum response

M1 asks whether a specified causal renormalized quantum stress contributes the
response DDR constrains. A concrete external semiclassical comparison is

\[
\mathrm{TF}\left(G_{ab}+U_{ab}[g]
 -{8\pi G_{\rm obs}\over c_E^4}
 \langle T_{ab}\rangle^{\rm ren}_{\omega,g}\right)=0,
\]

where U explicitly includes declared counterterm responses. Quantum fields,
state selection, renormalization, Einstein response and this identification are
all additional physics. This is not native matter emergence. New constants such
as ℏ and particle masses permit dimensional lengths, but do not select geometry.
It differs from GCA1's local curvature comparison by adding a state-dependent
physical response; it is recognizably semiclassical gravity.

In the invariant de Sitter slice, the anomaly stress is proportional to
H⁴g; its trace-free part vanishes for every admissible H. The other invariant
responses are also pure trace. Thus this shortcut does not determine H. If every term is conserved, E=λg further implies dλ=0; the remaining
freedom is a connected integration constant, not arbitrary trace history.
Fixing that constant or imposing a full trace equation is additional input. The imported result and state dependence
are discussed by [Mottola–Vaulin](https://arxiv.org/pdf/gr-qc/0604051).
Outside that slice, the decisive issue is whether an explicitly admissible state
rule gives the same response for histories with the same local metric jet.
Arbitrary states are not a counterexample to a rule admitting only one state.
A difference in the trace-free response would obstruct the proposed local DDR
identification; a pure-trace difference alone is invisible to its shape equation.
No actual selected-state comparison has yet been performed. Changing
to a global role would need a separately formulated proposal.

**Defer as a primary route.** It carries more unadopted physics than L1 and no
demonstrated scale selector. The first calculation should test its state/locality
claim, not start a particle or cosmology simulation.

## Two screened alternatives and what survives

L2 proposed a scale-free tidal term W=[(C²)²+(C* C)²]^(1/4) in an unadopted
R+βW metric functional. For a realizable Weyl family εC_0 with invariants
I_0=48,J_0=0, W=4√3|ε|. For β≠0, the flat derivative needed by an ordinary
smooth Euler response fails. Vacuum plane-wave tides can also have I=J=0, so
these scalars miss some tidal information; see [Pravda et al.](https://arxiv.org/abs/gr-qc/0209024).
Stop the displayed universal proposal; β=0 is the old Einstein comparison.
Other tidal responses remain possible. No smoothing term is invented as a rescue.

M2 proposed exact agreement of quantum photon phase cones with the metric cone
for every polarization. The imported leading spinor-QED correction is
n_ij−δ_ij=−αλ_C²(13R_kk δ_ij−4R_kikj)/(180π)+….
A nonzero Ricci-flat screen diag(q,−q) has opposite phase corrections; the
screen trace of the bracket is 22R_kk. The strict phase-equality proposal fails
against that imported tidal response. HSS section7.2, Eq.7.31 supplies a
realizable Schwarzschild critical-orbit screen in its stated affine convention;
the saved matrix check itself does not recompute that geometry. This is not an observational exclusion of
UDT or a claim that its founding causal cone is inconsistent. The weak-curvature,
low-frequency geometric-optics approximation does not fix the high-frequency
causal front. [Hollowood–Shore–Stanley](https://arxiv.org/pdf/0905.0771) supplies
the QED equation and this phase/causality distinction. Its parameters and omitted
orders are recorded in the micro initial proposal. Causal compatibility remains
an interface question, not a geometry selector.

The whiteboard therefore offers specific physical connections and early failure
tests, not a new accepted postulate or a completed positional prediction.
The small-scale question was useful: it exposed constraints and hidden physical
inputs, but did not show that mathematics alone selects UDT's geometry.
