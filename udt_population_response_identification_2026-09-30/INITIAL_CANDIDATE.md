# PRI1 initial conditional candidate

**DRAFT; UNADOPTED KINETIC INTERFACE.** This connects the existing C1 population
proposal to an explicit observer construction and audits a possible direct DDR
identification. It does not derive a UDT population, response law or metric.
PCW1 did not identify a population moment with E; that identification is tested
here as a diagnostic possibility, not attributed to prior work or Charles.

## 1. Supplied objects and quantifiers

At an event let (V,g) be a time-oriented Lorentz4 vector space, signature(-+++).
Let ν be a nonzero nonnegative Borel measure on future nonzero null vectors k,
with finite second moment in one orthonormal frame. Put

    M_ab = ∫ k_a k_b dν,       k_a=g_ab k^b.

The finite second moment makes every component finite in every fixed Lorentz
frame. In particular M(v,v)≥0 for every v, M(u,u)>0 for timelike u, and
tr_g M=∫g(k,k)dν=0. No physical energy interpretation or conservation law follows
just from this definition. In the conventional kinetic interface M would be
called stress-energy; that name remains conditional here. Amplitudes, angular
distribution, spectral scale and their physical provenance are supplied data,
not fitted to clock shifts. No isotropy or geodesic population equation is
needed for the following pointwise theorem.

Write k=ω(1,m), ω>0, |m|=1, in a proof frame and let σ be the pushforward of
ω²dν to the direction sphere. It is finite and nonzero. “Not a single ray”
means that σ is not concentrated at one direction, up to measure-zero sets;
multiple frequencies along the same null direction still count as one ray.
The sphere is a null-direction label space, not the S² matter carrier or a
preferred spatial center. A proof frame is not a selected physical observer.

## 2. A constructive second-moment observer theorem

On the future unit hyperboloid H+ define Q(u)=M(u,u). If the population is not
on one null ray, Q has exactly one minimizer u_M. It is the unique future unit
timelike eigenvector of the mixed tensor M^a_b, with

    M^a_b u_M^b = -ρ u_M^a,       ρ=Q(u_M)>0.

**Existence.** Write u=(cosh r,sinh r n), r≥0, |n|=1. For c=n·m,

    Q(u)=¼e^(2r)A(n)+½C(n)+¼e^(-2r)B(n),
    A=∫(1-c)²dσ, C=∫(1-c²)dσ, B=∫(1+c)²dσ.

Each coefficient is nonnegative. A(n)=0 would force m=n almost everywhere.
Otherwise A is continuous on compact S² and has a strictly positive minimum a.
Thus Q≥a e^(2r)/4, uniformly over n. Sublevel sets on H+ are compact and Q
attains a minimum. This is an analytic all-direction coercivity argument, not
a numerical velocity cutoff or finite search.

**Uniqueness.** Along any unit-speed hyperbolic geodesic u(t), u''=u, and

    d²Q/dt² = 2M(u',u')+2M(u,u)>0.

Hence Q is strictly geodesically convex. H+ is geodesically convex and any two
points are joined by such a geodesic, so its minimum is unique. At a critical
point M(u,v)=0 for all v orthogonal to u. This is exactly M^a_b u^b=-ρu^a.
Conversely every unit timelike eigenvector is a critical point, so is that
unique minimum. The proof uses positivity of the supplied moment, not an
imported Einstein equation or an equation chosen for its desired solutions.

**Covariance and smoothness.** Transform g and ν together. The unique minimizer
transforms with them; no external frame enters the construction. Multiplying
ν by a positive constant rescales ρ but leaves u_M unchanged. On a region with
smooth g,M and the non-single-ray condition at every point, the assignment is
smooth: its constrained Hessian on a spatial tangent v is

    Hess Q(v,v)=2M(v,v)+2ρ g(v,v)>0.

The implicit-function theorem applies, and unique local assignments agree on
overlaps. No uniform bound through loss of nondegeneracy or a boundary of the
population domain is claimed. This is an algebraic state-dependent observer
construction u_M[g,ν], not a finite-jet metric-only response or a proof that
actual clocks follow this congruence. It need not be geodesic or hypersurface
orthogonal; ordinary proper clocks along a specified flow remain distinct
from a physical mechanism maintaining that flow.

## 3. Degeneracies and a quantitative two-beam control

For a single ray M=b ell_flat⊗ell_flat, b>0, choose u boosted along ell.
Then Q=b e^(-2r) in the normalization ell=(1,1,0,0): inf Q=0 is unattained.
There is no timelike rest minimizer. For M=0 every observer minimizes Q.
These are actual limits of the result, not rejected data with an invented repair.

For opposite unit-frequency rays k±=(1,±1,0,0) with weights A,B>0,

    Q(r)=A e^(-2r)+B e^(2r),
    r_M=¼log(A/B),       ρ=2sqrt(AB).

As B→0 at fixed A, r_M→+∞; no finite observer survives at the single-beam limit.
The construction has no uniform conditioning bound near that limit. These are
freely supplied comparison measures, not a physical two-beam model of UDT.

## 4. A unique criterion does not select a unique clock interpretation

If additionally the first moment J^a=∫k^a dν is finite and timelike, the
normalized current u_J=J/sqrt(-g(J,J)) is another covariant assignment. Finite
second moment alone does not guarantee finite first moment for an infinite
measure near k=0. The following finite atomic example needs no extra limit.

Use the two unit-frequency rays above with weights A=4,B=1. Then

    J=(5,3,0,0), u_J=(5/4,3/4,0,0), v_J=3/5,
    u_M=(3/(2sqrt2),1/(2sqrt2),0,0), v_M=1/3, ρ=4.

Both are future unit timelike, both are defined from the same g and population,
and they differ. The minimizer theorem fixes the second-moment criterion; it
does not derive its physical identification with comparison clocks merely from
covariance. There are other possible protocols too; this witness does not
classify them. No preferred observer law is introduced by a state-dependent
frame, but selecting a physical state or a comparison protocol remains a choice.

## 5. What C1 gains, and what moments cannot certify

If C1's full supplied radiation distribution is exactly isotropic relative to
some U with finite positive second moment, angular integration gives

    M_ab=ρ U_a U_b+(ρ/3)(g_ab+U_a U_b).

Its unique second-moment rest observer is U, so the construction recovers that
candidate flow without independently inserting its timelike direction. This
is a positive conditional observer-assignment result. It does not determine
the physical population from g or justify an actual clock/population coupling.

Conversely even isotropy of this second moment does not prove full radiation
isotropy. Take a smooth supplied angular factor

    1+ε P4(z),  P4(z)=(35z⁴-30z²+3)/8,  0<|ε|<1,

and any nonzero positive radial spectrum with finite needed moments. P4 has
range[-3/7,1] on[-1,1], so the factor is positive. The integrals
∫P4 dz=∫z P4 dz=∫z²P4 dz=0 vanish on[-1,1]. Azimuthal integration then shows
the first and second angular moments match their isotropic counterparts, while
the full distribution has nonzero fourth-order anisotropy. This is a diagnostic
counterexample, not a fitted spectrum or new UDT population. It can be made a
spatially homogeneous, time-independent collisionless distribution on supplied
Minkowski spacetime; that is a comparison, not a UDT flatness requirement.

C1's original Liouville/full-isotropy assumptions are therefore still required
for its conformal-Killing and clock-ratio conclusions. Zero second-moment flux,
or even isotropic second stress, does not supply them. No near-isotropy error
bound, selected expansion, CMB spectrum, Θ profile or positional curve follows.

## 6. The raw population moment cannot be the DDR response by itself

For every orthonormal timelike/spacelike pair (u,n), R9 has
H=2(u_flat⊗u_flat+n_flat⊗n_flat). The exact contraction is

    <M,H>_g = 2[M(u,u)+M(n,n)]
            = 2∫[(g(k,u))²+(g(k,n))²]dν > 0.

This holds for every pair for any nonzero positive finite null moment, including
the single-beam case. It already precludes the direct E=M identification under
DDR. Independently, tr_g M=0 implies TF(M)=M, while M(u,u)>0, so DDR would demand
the impossible M=0. Adding any qg is invisible to H and cannot change this; a
nonzero scalar multiple cannot make the contraction zero either. In an isotropic
rest frame the contraction is 8ρ/3, not zero.

This is a restriction on a diagnostic response identification, not a rejection
of populated spacetimes or C1. C1 previously proposed only observer assignment.
It does not say that matter/radiation must vanish in UDT. A possible balance
between a geometric response and a population contribution would be a different
proposal requiring identification of the geometric term, coupling and physical
population; neither a familiar GR balance nor its numerical coefficient is
derived or adopted by the failure of E=M. Conservation alone would not fill
those joins, as the existing R17/GCA1 argument already explains.

## 7. Population, measurement and response remain separate dependencies

The squared-clock L1 response is a metric derivative of an aggregate measurement,
not M merely because a population supplies its weights. The full variation is

    δC=∫D δD dμ_g + ½∫D² δ(dμ_g),   D=log Z[g,Q_g].

Using a physical ν_g changes the questions: how that state is held or transported
under g variation, how u_M and physical clocks change, and how population/query
labels are counted. A fixed positive second moment at one metric does not give
any of these derivatives. Differentiating only k_a k_b while freezing the null
shell, distribution, measure and observers would be an unsupported protocol.
If a collisionless state rule is supplied, its initial data and full linearized
transport also belong to that rule; on-shell conservation is not an off-shell
response identity. No such transport/clock-score derivative has been solved here.

For the unchanged fixed-label CES1 protocol, CCR1's tube/sign obstruction still
holds. For one physical population with its own metric variation, CCR1 is not
silently reapplied with a different query or the every-laboratory quantifier.
It is also not automatically evaded: cancellation must be derived under an
independently justified protocol, not obtained by selecting weights from D.
No smooth-volume representation or metric-only locality is implied by taking
population moments or by choosing their rest frame.

## 8. Decision brief and maximum return

The surviving constructive connection is population -> a covariant
second-moment observer assignment, with explicit degeneracies. The raw moment
is excluded as the standalone DDR response. These are separate statements;
neither picks a UDT physical law. The new calculation makes C1's observer role
concrete and prevents promoting that role into field-equation selection.

Recommend retaining this construction as a CONDITIONAL tool, with no physical
adoption. To use it as UDT's actual comparison assignment would require a
physically justified population supplied independently of the tested redshifts,
an identified clock protocol and a state/metric variation rule. A geometry-
population balance would additionally need its own justified response/coupling.
The no-change alternative is to continue the existing supplied geometric
queries; the different comparison-frame control demonstrates why covariance
alone cannot select one interpretation. Empirical population data or a native
derivation could later support or contradict an identification. No observations
or new numerical population campaign are authorized by this return.

This is not a theorem of complete UDT underdetermination or a proof that a new
postulate must exist. No field equation, physical scale, native light/matter,
X_max, empirical SR/GR recovery or extra positional prediction is established.
Stop for discussion after checks, independent review and central integration.
