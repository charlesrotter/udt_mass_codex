# FKA1 Explorer B candidate — geometry, calibration and clock identification

Status: unreviewed analytic candidate for fresh adversarial review. Initial
editions remain unchanged. No canon edit, physical-premise adoption/revocation or
registry regrade is proposed by this file. Source snapshot is grok
`67246b3528c8fbc363b98c1d06794517e8109f65`.

## Result and what changed after comparison

The strongest favorable chain survives. A supplied complete metric and regular
pair germ give a complete two-dimensional metric. At the fixed clock
calibration, the later adopted G176 completed-pair premise uniquely fixes its
reciprocal ruler density. The stipulated normalized contrast is exactly a
hyperbolic tangent. For an independently supplied regular null-signal
correspondence, the metric and proper clocks determine a received tick ratio;
using that correspondence's source proper time to label the target clock leg
identifies its completed kernel with that ratio without a fitted extra function.

This is a conditional evaluator and a valid physical-clock compatibility
construction. It is not the shorter claim that the original mutual-slowing
words alone determine the reciprocal metric, its physical pair, or its received
clock rates. The time/time to time/length substitution was already identified
by the June 18 reviewer. The current development already retains the crucial
qualifications; this audit replicates and traces that seam rather than
discovering it for the first time.

The useful new presentation here is an explicit fixed-clock-normalization
proposition, a nonzero-shift flat control with all calibrations retained, and a
general reconstruction showing where spatial information remains after the
scalar is formed. These calculations do not provide a new physical selection
law. They sharpen which surviving claims can be stated without overreach.

## 1. Source and exposure record

The initial approach and reconstruction were frozen at
2026-10-14T00:17:07Z, with their hashes in INITIAL_FREEZE.json. I then read
COMPARISON_PACKET.md and COMPARISON_SOURCE_PINS.json and the instructed source
chain. No sibling explorer work or parent scientific candidate was read.
The parent subsequently requested complementary emphasis on the complete
pullback/calibration chain and the controls in sections 4–6 below. It did not
provide their calculations.

Actual comparison coverage:

* relativistic_metric_rederivation_results.md lines 1–240: §§0,1a–1c and
  additionally the exposed general-metric discussion in §§2a–2b. That extra
  discussion is historical argument under audit, not an added premise.
* The preserved independent reviewer script was read through all 209 lines;
  the intended A/B sections and accidentally broader C–F exposure are disclosed.
  The deep reciprocity script was read in full. Neither was run or imported.
* CANON.md only C-2026-06-18-1 and C-2026-08-06-1 substantive blocks; heading
  search exposed other entry titles. No canon entry was changed.
* July 15 derivation §§0–3 and its MAP through G4; no later wall/action extension
  was used. July 22 owner clarification/report and August 5 exact ownership
  derivation were read in full.
* G176 adoption/exact derivation, G179 exact derivation, G180 exact derivation,
  G220 exact derivation and G253 audit report were read in full.
* Current UDT_DEVELOPMENT.md definitions D1 and R1–R7, including their later
  qualified subsections. No R8 or subsequent chapter argument was opened.

All 21 files in the comparison pin set match their supplied SHA-256 hashes,
independently checked in COMPARISON_EXPOSURE_PINS.json. That hash check includes
some files not substantively read and is not claimed as full-file review.
Authority/startup and initial source exposures remain those in the initial
editions. Same inherited model, separate context, staged exposure; not
different-model independence. No numerical/symbolic scientific worker was
launched and no author or old reviewer code was used as new evidence. All
calculations below are exact hand derivations for later independent review.

## 2. Historical premise seam, with the strongest defense retained

June 18 §1a defines a clock comparison as f(phi_B)/f(phi_A), then imposes
difference-dependence. With positivity and regularity this yields f=C exp(k phi).
Composition of such ratios is already automatic, as the preserved reviewer A
correctly notes. Choosing the depth sign and scale can set nonzero k=-1;
calibration is also needed to set C=1. A nonidentity condition excludes k=0.
This is sound conditional algebra. It does not show that this ratio represents
both actual opposite received-clock experiments.

The pivotal sentence in §1b equates “each sees the other's clock run slow” with
f(phi)h(phi)=1, h=sqrt(g_rr). Its own ledger calls that a named analog choice.
The earlier reviewer B explicitly distinguishes equal/symmetric time-to-time
comparison from inverse time-to-length pairing and classifies both inverse
pairing and slot identification as assumptions. The deep reviewer offers the
strongest defense: once the exponential is known, assigning depth reversal to
an exchange of the temporal and radial slots gives A(-phi)=1/A(phi). But the
slot exchange is still assumed. It is not forced by swapping the two observers
in an actual signal experiment. Time–length swap is also not automatically a
physical isometry of the Lorentzian interval.

The historical canon adopted a conditional claim with a P8 slot caveat and
later made the product chart-scoped. That is relevant authority/provenance,
not mathematical proof of the contested implication. This audit does not
silently amend either adoption. The current maintained R1–R2 is more explicit:
dual action, composition, regularity, nonidentity, depth convention and the
Lorentzian readout are separate inputs.

The July 15 source supplies a clean favorable conditional replacement. For a
positive diagonal P=diag(u,v), preserving the independently declared dual
evaluation form K=[[0,1],[1,0]] gives P^T K P=uvK, hence uv=1. Continuous
additive composition gives exponential factors. A separately declared
Lorentzian quadratic readout gives the reciprocal metric block. Ordinary
conversion-map covariance instead gives u=v; that is the source's own
competing interpretation. The short owner quotation about reciprocal c does
not, by arithmetic inversion alone, distinguish them. Their physical
interpretation/adoption must remain visible.

K and eta=diag(-1,1) are different forms. The diagonal exponential matrix
preserves K but changes eta at nonzero depth. A basis equivalence with a boost
does not preserve both forms unchanged. The August 5 audit and current R7
already say this; no new transport obstruction is claimed here.

## 3. Full pullback and the fixed-clock-normalization proposition

Supply a smooth Lorentz metric g, a rank-two pair germ with tangent columns
a=J_0 and b=J_1, and the calibrated clock parameter y^0 defining a. Require a
timelike and b linearly independent. Dimension-match time using c_E; the
following formulas set c_E=1 only in these units.

The induced entries are h_00=g(a,a), h_01=g(a,b), h_11=g(b,b). This is metric
evaluation, equivalently h=J^T E^T eta_4 E J in any supplied coframe. No channel
is deleted before the pullback. Define

    T=sqrt(-g(a,a))>0,
    beta=g(a,b)/g(a,a),
    b_perp=b-beta a,
    L=sqrt(g(b_perp,b_perp))>0.

The orthogonal complement of a timelike vector is positive definite, so L>0
on this stratum. Since b=beta a+b_perp and g(a,b_perp)=0,

    h=-T^2(dy^0+beta dσ)^2+L^2 dσ^2,
    L^2=h_11-h_01^2/h_00,
    -det h=T^2 L^2.

This is an independently organized Gram decomposition of the source's same
three-entry algebra. Shift beta is retained. Its absence from det h does not
remove it from the metric or from null propagation.

At this fixed clock label, rescale only the auxiliary spatial differential by
ds=m dσ, m>0. The factors become T_s=T, L_s=L/m, beta_s=beta/m. The G176
WORKING_FOUNDATIONAL_CLARIFICATION supplies T_s L_s=1 as the physical
completed-pair condition. It follows exactly and uniquely that

    m=T L=sqrt(-det h),
    L_s=1/T,       det h_s=-1,
    Phi=-log T=-1/2 log(-h_00).

**Fixed-clock proposition.** Every regular Lorentz pair metric with the stated
clock leg has this unique positive normalization. Therefore existence of a
normalized representative alone imposes no additional ambient metric equation
within that regular stratum. The G176 premise selects which ruler calibration
is called the completed reciprocal query. If an independently prepared ruler
calibration is fixed beforehand, requiring it to equal m is a substantive
physical compatibility condition; its satisfaction cannot be proved by simply
renaming a newly constructed ruler coordinate. No such independent ruler
agreement or observer preparation is supplied by the algebra alone.

For a smooth one-parameter family, integration of m>0 gives s(σ) uniquely up
to origin and orientation. For a genuinely two-variable chart, ds=m(y,σ)dσ
while holding y fixed is an exact spacetime differential only if m_y=0.
Allowing s(y,σ) introduces a dy term and changes the coordinate formulas. The
current R4 already limits G180 to family descent and states this distinction.

Under a matched ambient coordinate change or a Lorentz coframe gauge change,
h is unchanged. Under auxiliary spatial relabeling σ=k σ_tilde, k>0, m scales
by k and m dσ is the same one-form. Those are covariance statements at the
same calibrated clock query. Under clock relabeling y'=lambda y, lambda>0,
with the same surface and auxiliary σ,

    T'=T/lambda,    m'=m/lambda,
    Phi'=Phi+log lambda.

This is not residual nonuniqueness after fixing the query. It demonstrates
why the clock label/calibration is a load-bearing input to its scalar, and why
the scalar is not a function of an unlabelled metric alone. A local proper-time
clock label has T=1; a nontrivial relational target leg can have T≠1 when
labelled by another clock's proper time.

## 4. Proper ruler length and complete metric reconstruction

For the supplied local clock direction, the orthogonal spatial ruler increment
has norm

    d ell=L dσ=ds/T.

This is the rest-space projection relative to that clock leg. A finite physical
ruler measurement would still require its stated synchronization/protocol.
Even locally it is generally not equal to the normalized coordinate ds. A
constant-y displacement instead has squared norm h_11 dσ^2 and is not the
orthogonal ruler when beta≠0; it can even be nonspacelike for a large shift.
The G176 designation of a physical reciprocal ruler coordinate does not make
all these different increments identical.

In the benchmark's time-orthogonal radial presentation, T=e^-phi, L=e^phi,
m=1, so ds=dr while d ell=e^phi dr. Thus the normalized reciprocal tape
recovers the areal radial parameter on that query, not automatically ordinary
proper radial length. This distinction does not contradict G176; it records
the precise ruler calibration that G176 chose.

The normalized metric, including its shift, is

    h_s=[[-T^2, -T^2 beta_s],
         [-T^2 beta_s, T^-2-T^2 beta_s^2]].

Retaining m as well as h_s recovers the entire auxiliary pullback:

    C=diag(1,m),       h=C^T h_s C.

Conversely every T>0,m>0,beta_s real reconstructs a regular pair metric in
this clock chart. The record (T,beta_s,m), or (Phi,beta_s,m), is therefore an
exact parameterization of this stratum; Phi alone is not.

For a transparent general positive-spatial-sector control, supply

    g=-N^2(dt+a_i dx^i)^2+H_ij dx^i dx^j,

where N>0 and H is any positive definite 3-metric. On coordinate clock leg
∂_t and spatial leg v, the completed data are

    T=N,    beta=a(v),    m(v)=N sqrt(H(v,v)),
    Phi=-log N,    beta_s(v)=a(v)/m(v).

At that event, all positive H share the same scalar when N is fixed. The full
valued directional records nevertheless recover H(v,v)=m(v)^2/N^2 and
a(v)=m(v)beta_s(v). The polarization identity
H(v,w)=[H(v+w,v+w)-H(v,v)-H(w,w)]/2 recovers H, and linearity recovers a.
This is a representation/reconstruction statement on supplied queries, not
selection of their values or a physical observer population. It is consistent
with current R5 and does not present spatial alternatives as rival completed
scalar kernels.

## 5. Exact nonzero-shift control, retaining every calibration

Use flat Minkowski metric on a local patch and pair embedding

    X^0=2y+σ,       X^1=3σ,       X^2=X^3=0.

This is a mathematical control, not an admitted native positional cosmology.
The pair tangents (2,0,0,0) and (1,3,0,0) are independent and the first is
timelike. Direct contractions give

    h=[[-4,-2],[-2,8]],      det h=-36,
    T=2,  beta=1/2,  L=3,  m=6,
    h_s=[[-4,-1/3],[-1/3,2/9]],      det h_s=-1.

Shift is nonzero: beta_s=1/12. The completed scalar and stipulated contrast are

    Phi=-log 2,       chi=(1/2-2)/(1/2+2)=-3/5.

The orthogonal spatial ruler has d ell=3 dσ=ds/2. Constant-y coordinate
separation has length sqrt(8)dσ instead, illustrating the shift distinction.

Relabel only the clock by y'=2y. Then X^0=y'+σ and the same geometry/surface
has

    h'=[[-1,-1],[-1,8]],      det h'=-9,
    T'=1, beta'=1, L'=3, m'=3,
    h_s'=[[-1,-1/3],[-1/3,8/9]],     Phi'=0, chi'=0.

Each fixed query has exactly one reciprocal normalization. The different
scalars result from the explicitly different clock labels. They are not
competing outputs under an unchanged G176 definition.

For actual fixed-σ observers at σ=0 and σ=d>0, both are inertial and at rest
in the physical Minkowski frame. Outgoing null travel gives
2(y_B-y_A)+d=3d, hence y_B-y_A=d. Returning future null travel gives
2(y_A,receive-y_B,emit)-d=3d, hence a delay 2d in y. In both directions the
arrival derivative is one. Since both proper clocks have d tau=2dy,

    Z_AB=Z_BA=1.

Thus local Phi=-log2 in the first calibration is not the matched physical
clock-comparison depth, which is zero here. The comparison chooses a different
clock leg, as G220 requires. Delay asymmetry in the shifted chart does not
create a tick-rate asymmetry.

This control also limits a signal-speed interpretation. In the first completed
coordinates the null slopes satisfy

    dy/ds=-beta_s +/- L_s/T=-1/12 +/- 1/4,

so ds/dy is +6 or -3. The scalar ratio q_pair=T/L_s=4 is neither of these
shifted coordinate speeds. Local orthonormal measurements still give c_E=1.
Current R4's conditional-ratio wording is therefore essential. No causality or
superluminal physical claim follows from any of these coordinate values.

All displayed values were checked by direct hand multiplication and rational
arithmetic. These checks are analytic, not a claimed new executable verifier.

## 6. The chosen scalar and the favorable actual-clock bridge

At completed calibration, the stipulated normalized contrast is

    chi=(L_s-T)/(L_s+T)
       =(T^-1-T)/(T^-1+T)
       =tanh(-log T)=tanh Phi.

No second response profile remains after the pair, normalization and this
readout are fixed. Alternative odd/bounded functions in the initial edition
were tests of what bare inversion symmetry selects; they are different
readout definitions, not alternative outputs of this unchanged definition.
The strongest claim here is exact algebra with typed inputs.

Now supply actual proper-clock worldlines and a regular future null incidence
family with arrival map tau_o=A(tau_e). The positive slope
Z=A'=d tau_o/d tau_e is the physical received interval ratio; its reciprocal
is the received cadence ratio for equal emitted proper-clock cadence. The
metric determines Z conditional on those inputs. For affine null tangent k,
this is Z=omega_e/omega_o with omega=-g(k,U)>0; common affine scale cancels.
This is exactly the null-clock interface already retained by G220 and R6.

With source proper time y=tau_e as the comparison label, the target clock leg
is a=Z U_o, so g(a,a)=-Z^2. For any independent supplied second tangent
completing a regular pair, its completed clock factor is therefore T=Z and

    Phi_clock=-log Z,
    chi_clock=tanh(-log Z),
    Z=sqrt((1-chi_clock)/(1+chi_clock)).

This is useful: an actual null-clock ratio has an exact representation in the
completed scalar, and no fitted post-readout clock correction is needed. It is
not circular when Z is first obtained independently from the metric incidence
problem. It would become circular if defining this target leg using Z were
then claimed to predict Z without solving or supplying the correspondence.
This construction supplies neither the second tangent nor a unique full pair
surface; it establishes the clock-leg compatibility, just as the source says.

For the benchmark and stationary endpoints e,o, direct pulse propagation gives
Z=N_o/N_e=exp(phi_e-phi_o), hence log(1+z)=Phi_e-Phi_o on the matched local
endpoint presentation. Its comparison depth is Phi_clock=phi_o-phi_e. Those
signs agree with both G220 and G253. Actual opposite future signals on that
static preparation have reciprocal Z values; moving/time-dependent preparations
need not. Current R6–R7 already retains this distinction and the additional
direction data required for general transport.

## 7. Minimal chain and verdict for each link

| Link | What survives | Limit/classification |
|---|---|---|
| Owner mutual received slowdown → time/radial inverse factors | No implication established by the inspected argument | June 18 substitutes a named analog interpretation; old reviewer already flagged it. |
| Positive difference-dependent multiplicative scalar → exponential | Exact under regularity and the stated composition domain | Operational scalar identification, nonidentity and depth convention remain explicit. |
| Dual evaluation pairing + positive diagonal action → uv=1 | Exact | Independent interpretation/premise; not arithmetic of c alone or actual two-future-clock theorem. |
| Reciprocal character + Lorentzian readout → reciprocal 1+1 block | Exact conditional construction | Does not select angular completion, symmetry, profile or all ambient metric histories. |
| Supplied g and calibrated J → full h | Exact metric pullback | g, query and causal stratum are supplied. |
| Full h + G176 → m, Phi | Unique conditional normalization at fixed clock label | Later WORKING_FOUNDATIONAL_CLARIFICATION; no revocation, no derivation from bare g. |
| Completed pair + normalized-contrast definition → tanh Phi | Exact algebraic identity | Dimensionless scalar compression; density and shift still contain information. |
| g + actual clocks + regular null branch → Z | Exact conditional physical-clock law | Null propagation/clock interface and actual query are hypotheses. |
| Same correspondence's target clock leg → Phi_clock=-log Z | Exact compatibility identity | Not independent verification of G176, protocol selection or complete pair-plane construction. |

The public-facing result should retain this mixed status. Saying simply
“the kernel fails” discards correct algebra and the clock bridge; saying simply
“the kernel follows from the original postulates” hides the premise seam and
supplied physical inputs.

## 8. Return judgment, current integration and open next probe

The current D1/R1–R7 already owns most of the honest qualification: supplied
depth, dual-action premise, calibrated query, G176 status, retained shift and
density, family-only normalization, conditional clock law and future-return
distinction. These should survive any integration. Historical editions should
not be rewritten to simulate that later precision, and CANON requires its own
owner sign-off. The actual added value is a compact source trace explaining
why the earliest equivalence is conditional, plus the explicit calibration and
proper-ruler distinction if useful in R4's argument.

The stopping point is scientifically meaningful after fresh review: a precise
unestablished founding implication with surviving conditional metric, kernel
and physical-clock constructions. No large numerical survey could resolve
whether the original words authorize a time–length dual pairing; that is a
meaning/premise question. More exact examples cannot promote that choice.

One concrete in-scope mathematical probe could matter if an objection remains:
choose an independently specified operational ruler and source/receiver event
correspondence, then test whether their pullback's m equals that actual ruler
calibration before relabeling it. It distinguishes physical compatibility from
existence of a normalized coordinate. Without that specified physical protocol,
the result should remain conditional rather than inventing one. This is not a
request to adopt a new premise or automatically launch a successor campaign.

Fresh review should challenge the Gram reconstruction, the shift/calibration
control, whether the named historical inference is truly unsupported at its
actual source scope, and whether the favorable clock bridge has been preserved
without suggesting unique selection. It should also challenge the return
decision: identify a concrete same-premise derivation that could still bridge
the founding words before asking for more calculation. No active registry
grade, source adoption or full-theory verdict is changed here.
