# GRC1-A initial candidate: an operational radial clock/ruler restriction

**UNREVIEWED, CONDITIONAL, UNADOPTED.** Frozen for adversarial review at baseline
`grok 89b4b473bed869f5ca296e9bfc67559a3c9ceaff`. No registry, physical premise,
response identity, action, source or canon change is proposed by saving this.
The discovery sequence and first rejected route are in NOTES.md. This is a
research checkpoint, not another maintained scientific development.

## 1. Physical question and scope

Can the local reciprocal clock/ruler factor, read using a metric-defined radial
ruler, also give actual finite received ticking without an extra propagation
term? In a declared spherical sector this question has a precise, testable
answer. Imposing the proposed equality on both radial signal directions is a
real metric restriction; pair normalization alone does not impose it.

Supply a smooth time-oriented spherically symmetric Lorentz4 region

    g = h_AB dx^A dx^B + r² dOmega²,

where the spherical action/orbit foliation is supplied, h is Lorentz2 and r>0
is the areal radius, defined by its sphere area4pi r². The action need not be
unique in a highly symmetric metric; no uniqueness of a center is claimed.
Restrict to an open untrapped patch F=h^-1(dr,dr)>0. Smoothness is
sufficient here; no claim at horizons, r=0, null/constant dr, singularities or
global topology follows. Spherical symmetry and this patch are supplied regime
restrictions, not a selected cosmic center. Set c_E=1 by length time units.

Let K be the oriented Hodge dual of dr on the quotient, with future sign.
Then K(r)=0 and g(K,K)=-F. Specify test clocks on the integral curves of

    U = K/sqrt(F).

These are ordinary proper clocks held at constant areal radius. They are
generally accelerated. They are not PSW1's released clocks or a universal
observer population. The congruence is fixed by this metric and preparation;
no additional physical field is supplied.

The new trial, **NAR (null-affine areal reciprocity)**, is:

    For every sufficiently short regular radial affine null signal between
    these clocks, in BOTH radial directions, Z = sqrt(F_o/F_e).             (N)

Z=d tau_o/d tau_e is actual received ticking with the stated endpoint clocks.
F can be measured locally by area and proper radial rulers: if
n=grad(r)/sqrt(F), then n(r)=sqrt(F), so F=(dr/dell)² in the U rest space.
The construction does not call r proper or radar distance. K's normalization
comes from the areal metric geometry, not a chosen time-potential normalization.

This is a named unadopted physical connection. The founding reciprocal
representation, W1 completed tape, no preferred observer and W4 do not by
themselves establish (N). It is permitted exploratory physics, not native
physical selection already extracted from those commitments.

## 2. Exact finite discrepancy before imposing NAR

Let gamma be a future affine radial null ray staying in F>0, k its tangent,
omega=-g(k,U)>0. In the orthonormal radial pair,

    k = omega(U + sigma n), sigma=+1 or -1,
    E := -g(K,k) = sqrt(F) omega = sigma k(r) > 0.

The sign sigma is constant along such a ray because dr is spacelike and no
nonzero radial null vector can annihilate r. Ordinary null-clock propagation
from R6 gives Z=omega_e/omega_o. Therefore, exactly,

    Z = sqrt(F_o/F_e) E_e/E_o,
    M := log Z - (1/2)log(F_o/F_e)
       = - integral_gamma [r''/r'] d lambda.                              (1)

Here r'=k(r), r''=Hess_h r(k,k), using the affine equation. No field equation
has entered. Warped-product geometry gives

    Ric_g(k,k) = -2 Hess_h r(k,k)/r,

because the Lorentz2 quotient Ricci tensor is proportional to h. Consequently

    M = integral_gamma r Ric_g(k,k) / [2 k(r)] d lambda.                   (2)

The integrand is invariant under positive affine rescaling together with the
parameter measure. Frequency amplitude and affine normalization do not become
a physical scale. Eq.(2) is a conditional geometrical clock/ruler diagnostic;
one finite zero integral need not mean zero local curvature contraction.

## 3. Equivalence and selected geometric class

On the stated patch the following are locally equivalent:

1. NAR (N) holds for all sufficiently short radial signals, both directions.
2. r''=0 along every affine radial null geodesic.
3. Ric_g(k,k)=0 for both radial null directions.
4. Hess_h r=(Box_h r/2)h.
5. The Kodama vector K is Killing.
6. Locally g=-F(r)dt²+dr²/F(r)+r²dOmega², with arbitrary positive smooth F(r).

Proof of1↔2: (1) implies E is constant on every such signal iff NAR holds.
Since E=sigma r', this is r''=0. Every short ray can be queried by the U
congruence. Proof of2↔3 is the warped-product identity. For2↔4, in any
orthonormal quotient basis (e0,e1), zero Hessian contraction on e0±e1 implies
H01=0 and H11=-H00; this is exactly a pure-trace symmetric form.

For4↔5, the quotient volume form is parallel, so differentiating
K_flat=*dr gives the Killing symmetrization as the Hodge image of the
trace-free Hessian. In components, when H_AB=c h_AB,
∇_A K_B=c epsilon_BA, antisymmetric. Conversely the symmetric part vanishing
forces H to be pure trace in Lorentz2. Since K(r)=0, quotient Killing symmetry
extends to the full spherical metric.

From4,

    dF = 2 Hess_h r(grad r, .) = (Box_h r) dr,

so F depends only on r locally. Killing symmetry preserves grad r, hence K
commutes with grad r/F. Take these as the coordinate fields ∂t and ∂r.
Their scalar products give h_tt=-F, h_tr=0, h_rr=1/F, proving6. Direct
calculation proves the converse. These are local coordinate statements, not a
classification of extensions across the omitted strata.

This is a Birkhoff-type geometric argument, not a derivation of the Einstein
vacuum equation. The remaining radial function is unrestricted. For example,
F=1-2mu/r and F=1-2mu/r-kappa r² satisfy it on positive-F patches; so does
F=1-lambda r⁴. Parameters are free geometric controls, not source/mass/scale
predictions. F=1-lambda r⁴ has nonzero nonradial null Ricci for lambda!=0,
so NAR does not set all null Ricci contractions to zero or give Ric=Lambda g.

## 4. What the clocks actually imply

In class6, K=∂t, the local radial clock/ruler factors are sqrt(F),1/sqrt(F)
and the local completed depth is Phi_local=-log(sqrt(F)). NAR implies

    Phi_clock := -log Z = Phi_local(o)-Phi_local(e).                       (3)

LKT1 already owns this endpoint test in an actual zero-shift reciprocal
Lorentz2 sector and shows the time-derivative obstruction. The narrow new
construction is a covariant spherical ruler/clock preparation and an equivalent
radial-curvature/Kodama criterion. No novelty is claimed for the older theorem,
standard Kodama geometry, or general Birkhoff mathematics.

A static-clock outgoing shift and a future returning shift invert for these
stationary clocks at fixed radii. They cannot supply two simultaneous net
redshifted legs. Free or differently moving clocks have their own endpoint
Doppler factors; NAR does not assign their shifts to a positional contribution.
Likewise NAR fixes neither a matched reference geometry nor an added clock
contrast. In two supplied spherical metrics, corresponding areal radii and
Kodama radial/angular orthonormal frames define a clear tangent matching, but
the physical reference profile remains extra information. This can support
comparison experiments without silently selecting their reference.

NAR preserves radial screen expansion: the area factor is r² and the expansion
is 2r'/r, generally nonzero. Its condition r''=0 is zero additional radial
Ricci focusing in the spherical radial congruence, not zero optical expansion
or a matched-reference contrast.
Spherical symmetry removes radial optical shear. Nonradial optical effects,
angular curvature and arbitrary F(r) remain.

## 5. Two distinctions tested exactly

**Completed reciprocity is weaker.** Supply

    g=-q(t,r)dt²+dr²/q(t,r)+r²dOmega², q>0.

Its radial determinant is -1. For k±=(q^-1/2,±q^1/2),
Hess r(k±,k±)=±q_t/q. Therefore a time-dependent q can satisfy that reciprocal
normalization while violating NAR. With q(t)=1+t, te>-1, and two fixed-r clocks
separated by L>0, the outgoing ray has

    to=-1+sqrt((1+te)²+2L),
    Z=sqrt((1+te)/(1+to)).

The proposed NAR factor is its reciprocal and differs for L>0. This follows
by differentiating the actual null incidence map and including proper clock
intervals; independently, affine k=(1,q) gives the same frequency ratio.
Eq.(2) yields M=log(q_e/q_o), exactly the same discrepancy.

**One signal direction is weaker.** Supply the time-dependent metric

    g=-F(v,r)dv²+2dv dr+r²dOmega².

The future ingoing direction l=-∂r is affine and has r''=0 for arbitrary F.
The other null direction n=∂v+(F/2)∂r has Hess r(n,n)=F_v/2 and
Ric_g(n,n)=-F_v/r. Thus its two-direction NAR condition requires F_v=0.
This is a supplied geometric control, not an admitted source/flux model.
Inverse-map reciprocity alone does not equate the two future directions.

## 6. Preserved failed route: universal recurrent-null transport

The first proposal RNC required a parallel null line: ∇l=omega⊗l for all
tangent directions. It gives R(X,Y)l=domega(X,Y)l and scalar holonomy. Actual
null clock ratios still contain endpoint calibration:

    frequency_o/frequency_e=exp(-int omega) N_o/N_e,
    N=-g(l,U)>0.

The Walker witness g=2du dv+dx²+dy²+(k v²+b x²)du² has
l=∂v, omega=k v du and nonzero line curvature for k!=0. Its optical screen
expansion/shear vanish. Nonzero static gravitational shifts can occur in an
appropriate timelike patch; recurrence is not identical to zero redshift.

However, a recurrent line must be a common null invariant line of all
curvature endomorphisms. Direct Schwarzschild exterior recomputation gives

    R(e0,e1)=(2mu/r³)B01, R(e0,e2)=-(mu/r³)B02.

For mu!=0 the first boost's only null eigenlines are e0±e1; the second
preserves neither. The first boost's zero eigenspace is spacelike. Hence no
recurrent null line exists near that point. Nor can metrics with recurrent
null lines converge there in C²: normalize the lines against a smooth timelike
frame, take a convergent subsequence on the compact null-direction sphere, and
pass curvature invariance to the limit to get the same contradiction.

This defeats RNC as a universal law with that quiet recovery requirement.
It does not defeat UDT, direction-selected comparisons, weaker regularity
limits or physical redshift. Recurrence only along an actual affine ray is
already its geodesic equation and is not the tested universal restriction.
NAR was formed to retain scalar radial comparisons while releasing transverse
recurrence and preserving active spherical expansion.

## 7. Evidence, limits and recommendation

Three captured short exact checks are saved with stdout/stderr, commands,
versions, resource receipts and hashes: recurrence (10 grouped identities),
spherical (14), clock_map (7). The spherical check starts from original4D
metric/Christoffels and retains angular terms; the actual clock map is derived
from null incidence, separately from the affine-frequency calculation. They
are author checks with shared SymPy, not separate-context or empirical review;
counts are not independent findings or completeness. No floating tolerance,
field solve, numerical survey or fitted profile is used. The analytic arguments
above carry the universal local quantifiers.

Primary mathematical references inspected: Galaev arXiv:1004.1934 introduction
and arXiv:1611.01551 §4.2 for recurrence/Walker geometry; Abreu–Visser
arXiv:1004.1456 §§II–III, eqs(17),(24),(27),(30) for quotient Ricci/Kodama
geometry; Schmidt gr-qc/9709071 §4, eqs(4.3)–(4.4) for the pure-Hessian
Killing construction. Their Einstein equations, actions and energy/source
interpretations are not adopted. SOURCES.md gives URLs and inspected scope.

Retain NAR as a **reviewable conditional bridge and discriminator**, not native
selection. It restricts a physical clock/ruler relation and a declared spherical
metric class while remaining compatible with useful quiet geometries. Its
physical justification, general nonspherical extension, additional positional
attribution, actual population, chosen profile, scales, stability and global
asymptote remain open. A test of NAR is a test of this conjecture, not of all
UDT. The next productive synthesis is to compare this radial structural
condition with researcher B's independent all-frame matched extra-clock sign
condition while preserving their different clocks, quantifiers and reference
assumptions. Further algebra on arbitrary F alone would not select physics.
