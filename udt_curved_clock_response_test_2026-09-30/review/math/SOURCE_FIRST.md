# CCR1 mathematical source-first review

Status: independently constructed conditional argument, before CCR1 producer
candidate/code or the other CCR1 reviewer. This is not a verdict on an unseen
candidate, an adopted physical law, or a general UDT obstruction.

## Identity, exposure and startup attribution

Reviewer: `/root/ccr_math`, a fresh separate subagent context on 2026-09-30.
The parent supplied the bounded question, source paths, startup facts and work
order; the review inherits the same model. No different-model, different-library,
human, outcome-blind observational, or formal-proof independence is claimed.
CES1 and FCV1 source derivations are exposed, as are current R18 L1/CES1 statements.
No CCR1 producer candidate/code or other CCR1 review has been opened before this
source-first seal. The source-first tube idea was in the dispatch; the calculations
and scope analysis below were reconstructed in this context.

I independently observed branch `grok`, HEAD
`252a717c380f1e7bb26266af2c8e8c962ccd4b2f`, no tracked changes, and the new CCR1
package plus the parent's unrelated untracked names. Parent startup attribution:
synchronized branch at that HEAD, 52 unrelated untracked names preserved, prior
actual full 406-row premise audit and current development guard passed. I did not
repeat synchronization or those repository-wide checks. No protected payload was
read. AGENTS.md and the applicable CLAUDE.md sections and four triggered protocols
were read from disk. Review mutations are confined to this `review/math` directory.

## Sources and question

The pinned source paths are recorded in SOURCE_PINS.json. The scientific inputs
are central R18 L1/CES1, CES1's PREPARATION.md and initial/reviewed result, and FCV1's
full variation derivation and reviewed result. The CCR1 work order permits
conditional curved-background mathematics, not a new physical premise, measure,
field equation, all-laboratory quantifier, or replacement functional.

L1's candidate functional is

    C[g;p,U,mu] = (1/2) integral D(q)^2 dmu(q),  D=log Z,
    dmu = w_s(s) ds dnu(L,eta,n).

The physically prepared clocks and fixed product label measure are exactly
CES1's. The metric and tube are free-and-explored mathematical inputs. Ordinary
proper clocks and the regular metric-null query are the supplied conditional
interface. The measure, population interpretation, and stationarity/DDR
identification remain UNADOPTED. c_E=1 is only a unit convention. Nothing below
requires the stationarity law to hold for every possible laboratory unless that
additional quantifier is expressly introduced in the small-laboratory corollary.

Question: does stationarity against every compact reciprocal strain survive on
a fixed smooth curved geometry in a regular emission-tube sector? The maximum
return here is a necessary condition and a sector obstruction, with uncovered
fixed-population possibilities left open.

## 1. Hypotheses and retained terms

Let K be the compact CES1 label support. Require a smooth future null arrival
branch on a neighborhood of K, A'(s)>0, uniform regularity, and commuting
derivatives. Parametrize both clocks by actual proper time. The source uses its
fixed physical emission time s. Suppose the relevant outgoing rays cross once
through a common regular emission tube

    X(s,theta,rho),  rho in (a,b),  0<a<b,

where l=partial_rho X is affine, -g(l,u_e)=1 at emission, and (s,theta,rho)
are smooth one-to-one spacetime coordinates on this tube (with sphere charts
as needed). Every query ray has some smooth theta=theta(s,L,eta,n). This theta
need not equal CES1's initial preparation direction n. The tube, including a
small support buffer, must miss all preparation curves, clock histories and
their neighborhoods over the relevant finite time intervals. Each admitted ray
must contain the common affine interval and intersect the support only once.
No caustic, returning ray, branch switch, or crossing clock history is hidden.

These are sufficient method hypotheses, not a theorem that arbitrary global
curved ensembles possess such a tube. The scaled local sector in section 5 does.

Support separation makes the initial preparation, parallel transport, physical
initial tangents and clock geodesics unchanged by uniqueness. Local proper rates
are unchanged as well. Therefore FCV1 gives W_e=W_o=0 and b_e=b_o=0, while the
proper arrival A DOES vary. Since both baseline labels are proper time along
the complete relevant curves, N_e=N_o=1 and the receiver-rate drift vanishes.
Source proper-time relocation also vanishes; it must not be added again.
The label measure is fixed, so delta mu=0. No metric-dependent spacetime
pushforward/Jacobian is substituted for dmu.

## 2. Explicit admissible tube strains and affine normalization

Parallel transport u_e along each emitted null geodesic to define a smooth
unit future u on the tube. Then -g(l,u)=1 throughout, and n_r=l-u satisfies

    g(n_r,n_r)=1,  g(u,n_r)=0,  l=u+n_r.

No global angular tangent frame is needed. With covectors lowered by g, let

    H = 2(u_flat tensor u_flat + n_r_flat tensor n_r_flat).

Its trace is zero and H(l,l)=4. Choose a smooth bump beta(rho), compactly
supported in (a,b), with integral beta d rho=1. For any smooth delay F(s,theta)
on the relevant compact labels, smoothly cut off outside a slightly larger
regular tube, set

    f = F(s,theta) beta(rho)/2,     h=f H.

Then the source-normalized ray integral is exactly

    (1/2) integral h(l,l) d rho = F(s,theta).

The strain is compact, smooth and reciprocal. It is the derivative of the
actual Lorentzian family obtained by replacing the u/n_r metric plane by

    -exp(-2 epsilon f) u_flat^2 + exp(2 epsilon f) n_r_flat^2

and preserving its orthogonal screen metric. Its plane determinant is unchanged.
This constructs an off-shell variation; it selects no physical center or scale.
Dimensions: F is a time/length delay, beta is inverse length, f is dimensionless.

To connect this construction to FCV1, let its endpoint-normalized tangent be
k=dx/dlambda, lambda in [0,1]. Write k=c l, so c=omega_e>0 and d rho=c d lambda.
Consequently

    I = (1/2) integral h(k,k) d lambda = c F,
    Z = omega_e/omega_o = c/omega_o,
    V = delta A = I/omega_o = Z F.

The ray-specific affine normalization cancels. Setting c to a universal endpoint
length before cancellation would be wrong on a curved background.

FCV1's full proper-clock formula now gives the exact first derivative

    Q=delta D=(1/Z) d(Z F(s,theta(q)))/ds
             = dF(s,theta(q))/ds + D_s F(s,theta(q)).        (1)

The s derivative holds L,eta,n fixed; it includes theta_s and the complete
baseline ray family. It does not hold a physical ray or reception event fixed.
The source-normalized tube cannot prescribe arbitrary independent values for
each five-dimensional q: rays with the same (s,theta) share F. This limitation
prevents an unjustified pointwise-in-q stationarity conclusion.

## 3. A necessary ensemble condition

It suffices to use the angularly constant subclass F=a(s), where a is arbitrary
smooth on the emission interval and cut off outside a larger interval. Define

    M(s)=integral D(s,L,eta,n) dnu,
    B(s)=(1/2) integral D(s,L,eta,n)^2 dnu.

Compact support and branch smoothness justify differentiating these integrals.
With fixed dnu, B'=integral D D_s dnu. Equation (1) implies

    delta C[a] = integral w_s(s) [ M(s) a'(s) + B'(s) a(s) ] ds.   (2)

Thus all-strain stationarity requires, distributionally on a neighborhood of
the complete emission support,

    (w_s M)' = w_s B'.                                      (3)

The test function may be nonzero at the edges of the weight support; it is
the spacetime variation that is compact. For smooth compactly supported w_s,
the integration-by-parts boundary term [w_s M a] vanishes, but the derivative
w_s' M must be retained. An omitted weight derivative changes the condition.
Equation (3) is necessary, not sufficient for stationarity under all strains.

The full angular tests give a stronger distributional condition. If the
pushforwards under q -> (s,theta(q)) admit smooth densities, define m as the
pushforward of D dnu, j as that of D theta_s dnu, and p as that of D D_s dnu.
Then

    partial_s(w_s m) + div_theta(w_s j) = w_s p.            (4)

Its integral over the sphere reduces to (3). It is equally valid as a
distributional pushforward identity when smooth densities are unavailable.
This review does not assume a query-to-angle diffeomorphism or a smooth local
4D response tensor in deriving the angularly constant condition.

## 4. Curved-background obstruction and its exact scope

If D>=d0>0 on all of K, compact regularity bounds |D_s|. Choose a positive
delay a(s)=a0 exp(K0(s-s0)) on a neighborhood of the emission support, with
K0>sup_K |D_s| and a0>0 (units as in section 2). Extend it smoothly with a
compact cutoff outside that neighborhood. Equation (1) then gives

    Q = a(s)(K0+D_s)>0,
    delta C = integral D a(s)(K0+D_s) dmu > 0.              (5)

This is a direct strain witness. It uses no Minkowski criterion and no weight
tuning. Negative D uniformly separated from zero similarly gives a nonzero
derivative of the other sign. The stronger sufficient condition is that M(s)
have a fixed sign bounded away from zero over the emission support: from (2),
choose K0 large enough that K0 M+B' has that sign everywhere. Pointwise D
need not have one sign for that version.

An additional sharp necessary edge condition follows from (3). Let s_* be an
actual finite boundary point of the support of a nonzero compact smooth w_s.
If M(s_*) were nonzero, continuity would make M nonzero nearby, and y=w_s M
would satisfy y'=(B'/M)y with bounded smooth coefficient and zero data on the
outside of the support. Uniqueness would force y=0 across the boundary,
contradicting the definition of s_*. Thus stationarity requires M(s_*)=0.
This is only a necessary condition and does not construct a surviving geometry.

The obstruction addresses the conjunction of squared contrast, this physical
preparation/measure, all-compact-reciprocal-strain stationarity, and the declared
regular tube/redshift sector. Ordinary recession in a strongly curved, finite
laboratory need not guarantee positive received D: gravitational and path
effects may change its sign. A fixed population with cancellations, loss of the
common-tube hypotheses, or other query architecture is not decided here.
No all-geometry or UDT no-go follows, and no stationary curved witness has
been constructed in the uncovered sector.

## 5. Scaled small laboratories in one fixed smooth curved metric

Fix a smooth metric g, an event p and frame, and compact dimensionless CES1
intervals sigma,ell in positive ranges, eta in [eta_-,eta_+] with eta_->0.
For each physical scale lambda>0 use s=lambda sigma, L=lambda ell and the
correspondingly scaled normalized s/L weights, leaving eta/n weights unchanged.
This is a family of physical query preparations, not the same single measure.

In normal coordinates at p, the rescaled metric coefficients g(lambda y) tend
to Minkowski coefficients in C^k on any fixed compact y-domain, with the usual
O(lambda^2) leading metric error for smooth bounded curvature. The relevant
unperturbed flat arrivals lie in one finite rescaled domain because eta_+ is
finite. Smooth dependence of preparation geodesics, parallel transport,
timelike/null geodesics, and uniformly transverse arrivals then gives, uniformly
on the compact dimensionless label domain,

    D_lambda(sigma,ell,eta,n) -> eta.

C^1 control of the rescaled arrival map is essential; C^0 metric convergence
alone would not justify a tick-ratio claim. For sufficiently small lambda,
D_lambda>=eta_-/2>0. A shell with fixed rescaled 0<a<b<ell_- and a time buffer
away from preparation gives the regular common tube and support separation;
these survive small smooth perturbations from the flat rescaled configuration.
The finite bound on D_s is for each lambda; K0 may depend on lambda without
introducing a physical law or scale. The strain remains an admissible test.

Therefore every fixed smooth curved metric has sufficiently small prepared
CES1 laboratories for which this candidate functional is not stationary.
This statement DOES NOT presume that the physical L1 population includes all
such laboratories. Only if the proposed law additionally requires stationarity
for every preparation in this shrinking family does it exclude every smooth
metric satisfying ordinary local clock recovery and these query hypotheses.
For a single fixed physical population, the surviving conclusion is section 4.
The proof relies on local smooth geometry, not exact global flatness.

## 6. Diagnostics, checks and limits

Analytic coverage: full arrival movement, endpoint displacements, proper-rate
terms, source-time protocol, fixed label measure, affine scaling, reciprocal
admissibility, support separation, common crossing, angular query degeneracy,
uniform branch regularity, and the extra all-laboratory quantifier are explicit.
The argument is exact first variation; there is no nonlinear stability,
finite-epsilon recovery, local-response smoothness, empirical GR precision,
matter/light emergence, selected scale, action or field-equation conclusion.
We did not rerun full CES1/FCV1 suites, numerical PDE solvers, data fits, or the
406-row premise audit. No such replay is needed to check the new analytic seam.

Independent exact anchors planned before execution: reciprocal-plane trace,
null contraction and finite determinant; affine scaling cancellation; direct
differentiation of a nonconstant arrival map versus (1); rejection of omitted
D_s and moving-angle terms; integration-by-parts condition and weight derivative;
positive-delay sign on a bounded illustrative readout. Exact controls are not
proofs of global tube existence or physical selection. The analytic argument
owns those stated hypotheses. Existing capture.py enforces one CPU process,
one thread, 60 seconds/512 MiB per check; no GPU, grid, or long solve. Output
stays within the CCR1 package's 20 MiB limit. Script and input hashes are frozen
before execution; result and report are sealed before direct candidate review.

Provisional source-first conclusion: a robust curved-space, sign-definite
clock-contrast obstruction survives without the extra exact-flat benchmark.
The necessary ensemble condition is available beyond that sign sector. A fixed
population with allowed cancellations remains unresolved. Any stronger claimed
no-go requires scrutiny of its quantifiers and tube hypotheses.
