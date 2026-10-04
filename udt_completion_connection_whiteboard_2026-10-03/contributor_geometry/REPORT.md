# CCW1 geometry contributor — source-first candidate connections

Status: analytic contributor draft, not independently reviewed or adopted. RG remains UNADOPTED. This is a fixed whiteboard artifact, not another maintained scientific development. Author: `/root/ccw_geometry`, a fresh contributor context with the inherited Codex model (GPT-6 family; exact backend identifier not exposed). No different-model or human-review claim.

## Scope and provenance

I independently observed branch `grok`, HEAD `28efe475b8453698475d9bfe6e674a6cca71a3c7`, and no tracked diff before writing this report. The parent supplies the same-session startup, remote refresh, full406, normal and 57 maintenance-check evidence described in WORK_ORDER and BASELINE; I did not repeat those checks. The 76 older untracked names were visible as names only and were not inspected, hashed or changed. Only this contributor directory is written.

The source-first read began with D1/R1/R4/R6/R7/R8 and R16FCW/R16CPW/R16FCL/R18 in UDT_DEVELOPMENT, followed by the exact sources below. No sibling report, parent CCW1 candidate, reviewer report or new diagnostic output was read. Prior FCL/FCW/FSL/LKT reviewed results and their listed source proofs were exposed; independence means a fresh argument about this connection, not blindness to established evidence. Read portions and hashes are in SEAL.json.

The metric-led question is whether the supplied native comparison structure connects to RG and to an actual family. All geometry is four-dimensional, signature (-+++); proper time is expressed in length units, c_E=1. The admitted source hypotheses are pinned-by-THEORY only within their conditional theorems. The diagnostic completion, emitter placement, initial motion, boundary point and null branch below are free-and-explored, not physically selected. No Einstein equation, response identification, action, matter law, population, X_max scale, Omega-distance identification or presentation-phi identification enters.

The concrete return is two conditional connections. Neither derives RG from the complete founding premises. Conversely, their absence from the inspected derivations is not a theorem that the complete premises are insufficient.

## Connection 1: RG has an invariant curvature/clock consequence

This extends FCW's homogeneous curvature consequence to a general regular completion and joins it to FCL's receiver theorem and the existing G220/G176 clock-leg readout.

### Exact geometric calculation

Supply FCL's C3 data `g=x^-2 b`, `x=Omega>0`, with b nondegenerate at a future spacelike boundary point p, `x(p)=0`, and nonzero timelike dx. Write `q=b^ab x_a x_b` and

    kappa(p) = -q(p) > 0.

The already admitted conformal connection difference is

    C^a_bc = -x^-1 (delta^a_b x_c + delta^a_c x_b - b_bc x^a).

Substitution into the definition of Ricci, keeping all four dimensions, gives

    Ric[g]_ab = Ric[b]_ab + 2 x^-1 Hess_b(x)_ab
                  + (x^-1 Box_b x - 3 x^-2 q) b_ab,
    R[g] = x^2 R[b] + 6 x Box_b x - 12 q.                 (G1)

The C3/nondegeneracy hypotheses bound the first two terms near p. Therefore every physical curve approaching this p has

    R[g] -> 12 kappa(p) > 0.                             (G2)

This is a geometric identity, not the Einstein equation or a choice of cosmological constant. For a b-orthonormal frame with a regular limit, the corresponding g-orthonormal frame is x times it, and the same formula gives `Ric[g](xE_a,xE_b) -> 3 kappa eta_ab`. The scalar assertion G2 does not require a frame choice. Kappa may vary from boundary point to boundary point; no globally constant curvature parameter has been derived.

Under any regular positive change `x'=a x`, `b'=a^2 b`, one has `dx'=a dx` at p and hence `-b'^{-1}(dx',dx')=-b^{-1}(dx,dx)`. Kappa is invariant there, although FCL's residue in x is gauge-dependent.

### Join to one ordinary free clock and the scalar kernel

Now add FCL's one finite-data unit timelike geodesic receiver approaching p and its regular interior-emitter null family. In its normal collar, `b=-N^2 dx^2+h`, so `kappa(p)=N(p)^-2`. FCL proves both a finite proper-time remainder and a positive limiting rescaled frequency:

    tau = -N(p) log(x/x_ref) + C_tau + o(1),
    x Z -> 1/B_* > 0.

Consequently, with `H_*=sqrt(kappa(p))`,

    Z exp(-H_* tau) -> A,        0 < A < infinity,
    log Z / tau -> H_* = sqrt(lim R[g]/12).               (G3)

The amplitude A depends on the proper-time origin, x normalization and emitter/branch data in their cancelling physical combination. The exponent is independent of regular conformal gauge. No claim that the instantaneous derivative `d log Z/dtau` converges is needed or made.

G220/G176's same-correspondence clock leg has `Phi_clock=-log Z` and `chi_clock=tanh(Phi_clock)`, hence exactly

    1+chi_clock = 2/(1+Z^2).

Thus

    exp(2 H_* tau) (1+chi_clock) -> 2/A^2.                (G4)

This is a precise connection to the existing scalar kernel on that clock leg. It does not construct the full pair plane or identify chi_clock with W5's projective-vector norm. It does not equate x with distance, phi or X_max. The physical proper clock stays ordinary; the clock ratio compares signals emitted at successively later interior times and received later by this same receiver.

### A decisive adverse test already available

For FCW's supplied beta2 control, let `z=1-h eta`, `Omega=z^2`, `h>0`. Its exact physical scalar is `R[g]=36 h^2 z^2 -> 0` on every comoving future curve as z decreases to zero. G2 therefore excludes ANY C3 completion in which that same physical future curve approaches a point with nondegenerate conformal metric and nonzero timelike defining-function gradient. The contradiction uses the physical scalar, so it does not require the new conformal factor to be a regular gauge multiple of FCW's displayed factor.

This is a narrower, invariant extension of FCW's previous displayed-gauge check, not a classification of all conformal extensions. It says nothing against null/degenerate/less regular completions, extensions where that physical future does not approach such a point, or divergent redshift itself. Beta2 remains a supplied control, not an admitted native UDT solution. Its divergent slowing is therefore a decisive counterexample to inferring RG solely from divergent slowing, within that proposed inference.

### Strongest counterarguments and smallest test

The crucial direction is RG -> G1–G4, not conversely. Positive limiting scalar curvature and a clock exponent do not supply a C3 extension, its causal type, global rays, physical preparation or the intended additional positional effect. Ordinary supplied positive-curvature cosmological kinematics pass these checks. Interior bumps still preserve the endpoint invariants while changing the interior. Inferring native RG or a new UDT contribution from a pass would be the defective step.

The smallest decisive geometry test for any proposed native asymptotic family is to compute its physical `R[g]` along the proposed late curve before fitting Omega or a distance profile. A zero/nonpositive/nonexistent finite scalar limit rules out an RG endpoint of this type on that curve. A positive limit only survives this necessary test; it is not certification. On an already admitted RG family, compare the same receiver's G3 exponent to `sqrt(R_*/12)` with the source normalization and quantifiers fixed. No numerical program is necessary for the present identities.

## Connection 2: local null geometry constructs the missing family near p

FCL supplies a regular ray family. G220 already owns the world-function/implicit-incidence method. Combining that method with FCL's endpoint regularity constructs a local family for a deliberately placed emitter. This is new coverage of the boundary attachment, not a new null-clock law.

Retain RG and the SAME receiver assumed to approach p. FCL gives in its normal chart

    r(x)=(x,y(x)),   y(x)-y(p)=O(x^2[1+log(x0/x)]),
    dy/dx=O(x[1+log(x0/x)]).

The receiver therefore extends as a C1 unparametrized conformal curve to p, with `r'(0)=partial_x=-N(p)n_p`, a past timelike vector when x increases. This conclusion does not assume a bounded receiver velocity; it uses FCL's proved estimate.

Take a sufficiently small convex normal neighborhood in a C3 local extension of b through p. Its existence is local differential geometry; if the original formulation only supplies a one-sided C3 collar, a local C3 nondegenerate continuation for this construction is an explicit technical extension hypothesis to be checked, not an extra physical region. Choose q inside the physical side on a short past null generator from p. Since dx is timelike in this small collar, x is monotone on each future null segment and the q-to-p segment stays on the physical side except at p.

Choose an ordinary smooth timelike emitter e(s) through q, with s its g-proper time and a short compact s interval bounded away from x=0. It may be freely falling: finite interior timelike initial data determine a local g-geodesic. No preferred emitter velocity is required. Its location and finite data are supplied preparation, not consequences of the native kernel.

Let sigma_b be the world function of this convex normal neighborhood and set

    F(s,x) = sigma_b(e(s),r(x)),   e(s_*)=q.

Use an affine parameter of span one on the limiting future null geodesic q->p, with nonzero tangents kbar_e,kbar_o. G220's endpoint derivative identity yields

    F_s(s_*,0) = -b(kbar_e,u_e) = E > 0,
    F_x(s_*,0) = b(kbar_o,-N(p)n_p) = N(p) B_0 > 0,
    B_0 = -b(kbar_o,n_p) > 0.

The nonzero F_s gives a unique local C1 incidence map `s=s(x)` through `(s_*,0)` by the implicit-function theorem, with

    s'(0) = -N(p) B_0/E < 0.                             (G5)

For each sufficiently small x>0, this is the unique local future null segment from that emitter to the actual receiver event r(x). Convex normality rules out conjugacy and multiple local branches; temporal orientation persists by continuity. The segments lie in x>0 because the collar's temporal defining function is monotone along them. Smooth endpoint dependence of the local geodesic and the ordinary interior clocks gives the regularity needed by R6 at each interior event. The endpoint tangents have a finite nonzero limit. Only C1 extension at x=0 is claimed; the interior family has the higher regularity available from the C3 data.

The physical tangent is `k=x^2 kbar`, so the limiting physical emission frequency for the span-one conformal parameter is precisely `E=-b(kbar_e,u_e)>0`. Rescaling each entire ray by its own positive emission frequency normalizes omega_e=1 and has a finite nonzero limit. Thus `B_*=B_0/E`; the family meets FCL's stated endpoint preparation. Differentiating the actual incidence map independently reproduces its residue:

    Z = (d tau/dx)/(ds/dx),
    x Z -> N(p)/(N(p)B_*) = 1/B_* > 0.                  (G6)

This is a check of the source/receiver normalization and orientation, not an independent confirmation of G176. It also shows the limiting emission event is approached from earlier source times as the receiver moves toward x=0.

### What this supplies and what remains supplied

For each receiver already satisfying FCL's endpoint hypothesis, one can arrange an ordinary local emitter and a regular null family near p. Thus a separate global ray-existence theorem is unnecessary for this restricted local existence witness. There is no claim about a specified far-away source, a prescribed emission history, rays outside the convex neighborhood, caustic avoidance globally, uniform populations, later return availability, or physical source abundance. The receiver's own existence/approach to p remains supplied. This does not turn the boundary into a finite-time reception event.

The strongest objection is quantifier reversal: choosing q on p's past null cone is allowed for an existence witness but cannot prove that an independently fixed physical source emits into this branch. The smallest repair is to retain the explicit existential preparation quantifier. Similarly, a fixed-emission distance experiment varies a receiver population and is not described by the function s(x). G5–G6 cannot be advertised as a universal distance pole.

The smallest decisive next proof check is a finite-regularity audit of the C3 extension/normal-neighborhood/world-function steps and G5's two endpoint signs. That is a bounded analytic review. A remote-source version would instead need a specified source and a caustic/branch continuation argument; local existence is not authority to launch that campaign.

## Native implications, proposal boundary and review needs

The source-owned native comparison framework supplies the ordinary metric clocks, Levi-Civita/null-incidence calculation, and the matched reciprocal clock scalar once a geometry and comparison are supplied. RG adds a strong physical trial: a regular spacelike conformal endpoint. No inspected R1/R4 composition or normalization step provides its nonzero timelike gradient or C3 extension. One must not turn a bounded comparison scalar into a defining function for a full four-metric without a demonstrated regular conformal extension.

The useful candidate gain is therefore G1–G6: an invariant curvature/clock compatibility condition, a curvature obstruction covering beta2's same future curve, and a local construction of an emitter family under RG. Physical admission of RG and its attribution to an additional UDT positional contribution remain UNADOPTED/OPEN. Reciprocity still reverses the same comparison map; no two distinct future signal routes are identified.

Analytic checks performed: contraction of the conformal connection difference to Ricci/scalar; normal-collar evaluation `kappa=N^-2`; regular-gauge cancellation; limiting logarithm/amplitude algebra; exact tanh conversion; beta1 sign and beta2 scalar checks using FCW's saved analytic family; world-function endpoint signs and frequency normalization. No symbolic/numerical diagnostic program was run, and no finite sampling is claimed as proof. The attempted registry query first used the wrong column key and returned only headers; the corrected query read selected fields for G176/G220/G269/G272/G274/G312. No result was inferred from the empty first query.

Required before a reviewed synthesis: fresh adversarial inspection of G1's signs and G5's regularity/quantifiers, then exact source/version binding and the parent closure gates. No independent review verdict on this report is claimed. Unavailable checks: different model, human specialist, formal proof assistant, independent computational implementation, empirical attribution, full-postulate consequence/completeness audit and global null continuation. No central file, registry, CANON, historical source or protected payload was changed.
