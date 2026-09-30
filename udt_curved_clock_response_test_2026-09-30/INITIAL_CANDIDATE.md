# CCR1: curved-background necessary condition for the supplied clock score

Initial conditional candidate; no physical adoption. This investigates the
unchanged L1 proposal C=(1/2)∫(log Z)²dμ with CES1's prepared clocks and fixed
product label measure. Exact Minkowski stationarity is NOT an assumption or a
pass criterion. The result below concerns actual stationarity of that proposed
score at a supplied, possibly curved metric. It does not identify UDT's response.

## 1. Scope and physical preparation

Let g be a smooth time-oriented Lorentz4 metric of signature −+++ and let the
CES1 preparation be well defined: emitter geodesic γ from a chosen event/frame;
receivers launched from exp_p(L n0) with parallel-transported initial frame and
positive physical rapidity η; ordinary proper clocks with fixed origins. Denote
receiver labels collectively by ξ=(L,η,n0), their fixed normalized measure by
dν(ξ), and emitter proper emission time by s. Use a nonnegative smooth normalized
w(s) of compact support K in an open finite interval I of positive emission times.
The measure is dμ=w(s)ds dν, with the same fixed physical counting interpretation
as CES1. All labels except their metric-dependent physical realization stay fixed.

Assume the future metric-null branch to each receiver has a smooth regular proper
arrival A(s,ξ), Z=∂s A>0 and D=log Z on a neighborhood of the compact label set.
No multiple-image sum, caustic or branch switch is admitted. The controlled sector
has a common smooth outgoing emission tube: baseline null rays from γ(s), labelled
by their actual emission direction θ and affine distance r, have a smooth injective
map (s,r,θ) into spacetime on I×(a,b)×S², with 0<a<b. Each query ray crosses this
shell once in its outgoing direction before reception and has no other intersection
with the supported perturbation. The closed support is disjoint from open
neighborhoods of the preparation paths and all relevant clock histories.

These are explicit geometric/method hypotheses. They hold for sufficiently small
regular laboratories discussed below, but are not asserted for arbitrary strongly
lensed populations or global spacetimes. θ is the null emission direction, which
can depend on s and ξ; it is not identified with receiver preparation direction n0.
S² here is the sphere of null directions at a laboratory event, not a matter carrier.
The tube does not impose spherical symmetry on g or select a cosmic center.

## 2. A genuine reciprocal metric variation on a curved background

Normalize each outgoing affine generator K by −g(K,u_e)=1 at its emission event.
Parallel transport the source unit tangent u_e along it to a field u on the tube.
Then −g(K,u)=1, and n=K−u is unit spacelike, orthogonal to u, with K=u+n.
Choose a smooth radial bump ρ supported in (a,b), ∫ρ(r)dr=1. For any smooth
α(s) compactly supported in I, let F=α(s)ρ(r)/2 and set

    h=F H(u,n),        H=2(u_flat⊗u_flat+n_flat⊗n_flat).

This is an actual compact reciprocal tensor variation, not an independent
adjustment of each clock query. It is direction-independent in its scalar
normalization even though the transported frame and geometry may vary with θ.
Its trace is zero and h(K,K)=4F=2αρ. To realize it by finite metrics, put

    P=g+u_flat²−n_flat²,
    gε=−exp(−2εF)u_flat²+exp(2εF)n_flat²+P

on the tube and gε=g outside. Smooth bump support makes the extension smooth;
signature and time orientation persist, and the reciprocal block determinant
is unchanged. The strain has units consistent with α a proper-time length and
ρ inverse length. No preferred physical perturbation, field solution, boundary
or new source is asserted by this off-shell variational test.

The metric is unchanged near every preparation path and clock history. Geodesic
and parallel-transport uniqueness therefore preserve the physical preparation,
worldlines and proper-time parametrizations exactly. Thus W_e=W_o=0 and rate
variations vanish by support. Reception still moves. No laboratory-frame
continuation at p is needed for these supported variations, which fix its metric.

For FCV1's affine parameter λ∈[0,1], write k=c(s,ξ)K on a query ray, so
ω_e=c, dr=c dλ and

    I[h]=(1/2)∫h(k,k)dλ=c α(s)=ω_e α(s).

Every query has the same normalized interior integral because it crosses the
entire normalized shell once. FCV1's full endpoint formula, with proper labels,
then gives

    δA=I/ω_o=Z α,              δD=(∂s δA)/Z=α'+D_s α.       (1)

This retains the derivative of Z, hence all baseline clock drift and ray-family
dependence. It does not hold the receiver event fixed. The resemblance to an
emission-time relabelling is only an algebraic first-variation identity: actual
emission proper-time labels and clocks are unchanged. A pure coordinate change
with endpoints carried would instead have FCV1's cancelling endpoint terms.
For nonzero α, I=ω_e α also excludes an endpoint-fixing compact pure gauge.

## 3. Curved stationarity condition and sign obstruction

Define the finite averages at each s:

    M(s)=∫D(s,ξ)dν,          J(s)=∫D(s,ξ)D_s(s,ξ)dν
                                =(1/2)∂s∫D(s,ξ)²dν.

Uniform regularity over compact labels justifies commuting derivatives and
these integrals. The fixed label measure has no extra variation; its physical
pushforward dependence is already in the full Q_g and formula(1). Thus

    δC[hα]=∫ w(s)[M(s)α'(s)+J(s)α(s)] ds.                  (2)

Stationarity against all compact reciprocal strains necessarily implies

    (w M)'=w J                                             (3)

as distributions on I. This is a necessary condition from a subset of metric
strains, not a sufficient field equation, a smooth volume response construction
or a selected population law. No independent variation of all five query labels
has been assumed; the constructed control α depends only on emission time.

Suppose M has one strict sign on a closed interval whose interior contains K,
with a neighborhood in I on which it stays away from zero. This includes uniform
positive received slowing D≥d*>0 for all queries on that interval. Put b=J/M
there, and solve the elementary linear ODE

    α0'+b α0=1.

For example, B(s)=∫_{s0}^s b(t)dt and
α0(s)=exp(−B(s))∫_{s0}^s exp(B(t))dt. Multiply by a smooth cutoff equal to1
on a neighborhood of K, compactly supported in the interval where this solution
is defined. In the scored region this is an admissible α with

    M α'+J α=M,       δC[hα]=∫w M ds ≠ 0.                  (4)

The opposite sign of the strain gives the opposite derivative. Consequently no
metric in this regular-tube, strict-sign-mean sector is stationary for the proposed
score. Curvature is unrestricted except by the stated regularity/support sector;
the proof uses no flat baseline, Einstein equation, expansion profile or small-
curvature substitution. The test direction is chosen to detect a derivative,
not inserted into the physical law or fitted as a target geometry.

A separate simple witness for uniformly positive D uses α=τ0 exp(κ(s−s0)) on
the scored interval, with a cutoff outside it and κ>sup|D_s|. Then δD>0 and
δC>0 pointwise. This alternative arose in both source-first reviewer discussions;
it checks the sign obstruction without using the integrating-factor construction.
The main mean-sign proof does not require every individual D to have that sign.

If M crosses zero, the division in(4) is unavailable. Equation(3) survives but
does not exclude that sector; it also does not establish stationarity against
the remaining strains. D≡0 gives a vacuous zero first variation of this squared
score. Neither mixed-sign cancellation nor that zero case selects UDT's geometry.

## 4. Ordinary small-laboratory recovery without global flatness

Keep any one smooth curved metric fixed near p. Take scaled copies of the CES1
protocol with physical separations L=ℓ L0 and emission times s=ℓ s0, fixed
dimensionless compact template ranges, the same normalized template weights,
and η in the same positive compact interval. This is a family of experiments,
not a rescaling of the universe or an adopted physical population. In physical
variables the probability densities acquire their normal Jacobians; no weights
are retuned to an outcome.

In Riemann normal coordinates at p, represent the rescaled metric by
gℓ(y)=g(ℓ y). The coordinate pullback carries an overall ℓ² which is removed
when expressing proper lengths/times in laboratory units; Z is unchanged by
that common normalization. On the fixed finite template domain,

    g0=η_Minkowski,       ∂ℓ gℓ|0=0.

Choose ℓ small enough that the whole template lies in a regular normal-coordinate
patch. Smooth dependence of preparation, parallel transport, timelike geodesics,
null arrivals and their derivatives on gℓ, plus the nondegenerate Minkowski
arrival branch and compact labels, yields

    Dℓ(s0,ξ0)=η+O(ℓ²) uniformly.                          (5)

This is a controlled local asymptotic statement for a fixed smooth metric and
template: the bound is Cℓ² on a sufficiently small interval, with C depending
on metric derivatives on the chosen patch and the finite template bounds. It is
not a numerical solar-system precision estimate, a universal curvature constant
or a physical value of ℓ. One may also use uniform convergence alone for the sign.
Because η≥η_->0, sufficiently small ℓ gives Dℓ≥η_-/2>0. A compact emission shell
strictly between source and receivers exists in the flat template with positive
support margins; regularity, single crossing and separation persist for these
small smooth perturbations. Thus these genuinely curved small labs satisfy the
hypotheses of the obstruction, rather than requiring an exactly flat universe.

For one fixed supplied ensemble the direct conclusion remains(4) whenever its
actual curved observations have the specified mean sign and tube. If the rule
were required to govern EVERY scaled laboratory independently, (5) would exclude
that stronger universal implementation on any smooth metric. That universal
quantifier is not silently added to L1: a uniquely justified cosmic population
could be a different proposal and is not rejected by arbitrary relabelling or
subsetting of it. No such population is provided or adopted here.

## 5. What changes scientifically

CES1's derivative remains correct but its exact-flat benchmark is no longer the
reason for this obstruction. The unchanged proposed score cannot be stationary
in the admitted regular sector with a strictly positive mean clock contrast,
including ordinary sufficiently small receding-clock laboratories in curved
spacetime. The problem is the unadopted identification of this clock score with
the physical stationary response, with its supplied population/preparation.
It is not an inconsistency of ordinary proper clocks, UDT positional geometry,
DDR, Local Metric Sufficiency, or GR-as-filter.

No physical curved solution with the intended additional positional effect has
been derived. This result cannot discard every possible ensemble, alternative
response, caustic sector or native UDT equation. It does not justify inventing
weights, subtracting GR, changing the score, or adding a source as an unlabeled
repair. It returns a substantive restriction on this particular proposed
connection, without a full-theory underdetermination or missing-postulate theorem.
Full dynamics, empirical GR precision, nontrivial positional curves, native scale,
X_max and matter/light emergence remain untested/open at their prior scopes.

## Discovery and verification state

FCV1 and CES1 were exposed. The parent developed the normalized tube, equation(3)
and integrating-factor obstruction during exploration; independent reviewer
messages then supplied matching necessary conditions and exponential controls
before this complete candidate was written. The candidate is not blind discovery.
Reviewers must seal their source-first records before direct candidate/code
exposure. Analytic hypotheses and the support construction carry the proof;
bounded symbolic checks only anchor algebra and must not replace them. A source-
preserving same-premise repair is allowed if substantive review finds a defect.
