# PCW1 local proposals — initial discovery, unadopted

Proposer `/root/pcw_local`, separate context, inherited model; not a reviewer.
HEAD independently checked: `ef00adf90d0389711289e4baed38bf00a047fd6d`, branch
`grok`; parent reports successful synchronization, baseline validation and prior
full406 audit. Protected/unrelated names were visible in status but payloads were
not read. Parent owns final audit/integration. Source/exposure pins and exact
diagnostics accompany this file. No physical adoption or completeness claim.

Question: can an actual ensemble of metric-clock observations, or its tidal
information, identify the response tested by DDR? Scope: smooth Lorentz4
regular clock branches, conventional null-clock interface, compact variations.
All additions below are **free-and-explored**. Diagnostic flat charts are
**pinned-by-HABIT** conveniences. No GPU, solve, fit or physical scale selection.

## L1. Clock-ensemble susceptibility as the reciprocal response

**Added physical relationship.** Let a specified ensemble have regular physical
queries (Q_g(q)), positive measure (d\mu_g(q)), and ordinary received ratios

\[
D_g(q)=\log Z[g,Q_g(q)],\quad
\mathcal C[g]=\tfrac12\int D_g(q)^2\,d\mu_g(q).
\]

Propose that reciprocal metric changes are stationary for this comparison
contrast: (\delta\mathcal C[H]=0). If its first variation admits a smooth
volume representation, define its response by

\[
\delta\mathcal C[h]=\int D\,\delta D[h],d\mu
 +\tfrac12\int D^2\,\delta(d\mu)
 =\int E^{ab}_{\mathcal C}h_{ab},dV_g.
\]

Then the existing all-pair DDR tests (\operatorname{TF}(E_{\mathcal C})=0).
This **new stationarity/response identification**, not inverse-map reciprocity,
would select admissible geometries. Each selected geometry still produces clocks
through the existing (Z=N_o(A)A'/N_e); no second redshift factor is added.

The integrand uses **raw net** received ratios, including SR and gravitational
shifts. There is no subtraction of a desired GR/positional template. Equal-weight
inverse descriptions give (D^2+(-D)^2=2D^2), not automatic cancellation.
Actual future return legs are separately evaluated. Stationarity is proposed;
minimum contrast, unique equilibrium and stable dynamics are not established.

**What is new relative to inspected work.** FCV1 supplies the complete derivative,
including endpoint/ray motion, but rules out a smooth volume response for one
nonzero query. Integrating a continuum of differently supported queries is an
explicit attempt to overcome that support issue. It is neither proof of smoothing
nor a native population law. FE1 uses an infinitesimal volume coefficient and
lands on Ricci; this proposal uses measured finite clock contrast. GRS/RMS
classify a response once its hypotheses are known; CRV/GCA do not identify this
ensemble. LKT remains the transport evaluator. SGE's stationary-clock restriction
survives: this functional does not manufacture two redshifted static return legs.

**Commitments and strongest objections.** Query preparation, duration/separation
distribution, ensemble measure and its metric dependence are new physical data,
not harmless averaging conventions. Overall positive normalization cannot select
a scale, while changing relative weights changes the equation. A finite range
usually produces a nonlocal response. To retain Local Metric Sufficiency as a
requirement for this local-response route, a justified local limit eliminating
independent population/history labels is mandatory; it is currently OPEN.

No finite normalized Lorentz-invariant uniform distribution exists on the entire
unit timelike hyperboloid: its invariant radial volume is proportional to
\(\sinh^2r\,dr\,d\Omega\). A preferred rest distribution or rapidity cutoff is
therefore an added choice, not “all observers.” A finite network also retains
ICN1's interior conformal blindness. Most seriously, this contrast penalizes
ordinary Doppler/gravity observations unless its protocol explains why that
penalty has the physical status proposed.

**First decisive calculation.** Freeze a query protocol and measure before any
geometry target. In flat space with comoving clocks, (D=0) gives
\(\delta\mathcal C=0\) identically and
\(\delta^2\mathcal C[h,h]=\int(\delta D[h])^2d\mu\): a first-variation pass
is vacuous, not field selection. Conversely, for
\(g_\epsilon=-e^{-2\epsilon}dt^2+e^{2\epsilon}dx^2+dy^2+dz^2\), keep the
straight coordinate clocks (x=0\), (x=b+vt\), (0<v<1\), fixed. Their
physical speed is (e^{2\epsilon}v\), so

\[
D_\epsilon=\operatorname{artanh}(e^{2\epsilon}v),\quad
\partial_\epsilon(D_\epsilon^2/2)|_0
=\frac{2v\operatorname{artanh}v}{1-v^2}>0.
\]

These are all flat geometries and ordinary geodesic clocks. Holding physical
rapidity fixed instead makes this variation zero. This is a **protocol ambiguity
witness**, not a gauge failure or a universal refutation: fixed coordinate
worldlines during a metric change describe different physical queries. A viable
proposal must identify which variation is physical and preserve tested SR before
any solar/galactic calculation. Only then test smoothing/locality and whether a
nonzero shape response survives. No target profile has been inserted; no useful
new clock prediction has yet been obtained. Recommendation: retain only as a
conditional response-design question, not a ready field equation.

## L2. Tidal magnitude rather than volume mean — adverse diagnostic

Clock-compass protocols can reconstruct curvature with specified preparation and
kinematic controls; this is an operational comparison, not UDT emergence
([Puetzfeld–Obukhov–Lämmerzahl](https://arxiv.org/abs/1805.10673)). Unlike the
Ricci volume mean, Weyl information includes vacuum tidal anisotropy. Propose a
response sensitive to its invariant magnitude:

\[
I=C_{abcd}C^{abcd},\quad J=C_{abcd}{}^*C^{abcd},\quad
W=(I^2+J^2)^{1/4},\qquad
\mathcal A_\beta[g]=\int\sqrt{|g|}(R+\beta W)\,d^4x.
\]

Identify DDR's response with this functional derivative wherever it exists.
Both the functional and its identification are **unadopted new physics**; the
Einstein term is an explicit comparison choice, not GR dynamics inferred from
W4. Orientation changes flip (J), leaving (W) unchanged. Dimensionless
\(\beta\) is free; (W\) and (R\) have dimension (L^{-2}\), so this adds no
length scale. It selects neither a galactic threshold nor physical (X_{max}).

This differs from FE1's Ricci-only response and GCA's analytic, dimensionful
\(R+\alpha R^2\): its possible escape from GRS/RMS is precisely failure of flat
regularity, not a refutation of their theorem. Tidal reconstruction supplies
measurability, not the physical reason to extremize this modulus. The latter
remains the strongest unexplained commitment.

**Decisive adverse calculation, already available analytically.** On a realizable
normal-jet Weyl family (C=\epsilon C_0\) with (I_0=48,J_0=0\),
\(W=4\sqrt3|\epsilon|\). The two one-sided derivatives differ; a smooth
ordinary Euler response at flat space is unavailable. Nonzero-curvature vacuum
plane waves also have (I=J=0\): this scalar cannot faithfully measure every
tidal field ([Pravda et al.](https://arxiv.org/abs/gr-qc/0209024)). These defects
precede a solar-system solve. Adding a smoothing scale changes the proposal and
forfeits this scale-free motivation; restricting away from flat/null strata
does not establish SR/gravitational-wave recovery. Recommendation: stop the
displayed universal proposal at this adverse result; preserve its narrower
question about response to tidal rather than volume information. This rejects
neither other tidal responses nor UDT's founding premises.
