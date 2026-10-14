# FKA1 independent analytic checks

Reviewer `/root/fka_review_math`, 2026-10-14 UTC. These are explicit exact
hand derivations performed during direct review of the frozen INITIAL_CANDIDATE.
No old checker, candidate checking implementation or saved scientific result was
executed as confirmation. Candidate formulas were visible in this direct phase;
independence is a separate context and argument/check route, not blinding,
different-model review or a second software implementation. The independent
source-first and clarification editions remain unchanged.

No scientific process, numerical approximation or solver was needed. Resource
use was ordinary review plus file/status/hash inspection. There are no convergence
tolerances, sampled-grid claims or unreported numerical failures in these checks.
The proofs and exact residual values below are the check evidence.

## M1. Original Gram equations and companion freedom

At an event in signature (-,+,+,+), let a be timelike and b independent. Write
`A=-g(a,a)>0`, `B=g(a,b)`, `C=g(b,b)`. Orthogonal projection gives

    b_perp = b + (B/A) a,
    g(a,b_perp) = B + (B/A)(-A) = 0,
    g(b_perp,b_perp) = C+B^2/A > 0.

The strict inequality follows from positive definiteness of the timelike
orthogonal complement and b_perp nonzero, not from assuming b itself spacelike.
Thus `h=[[-A,B],[B,C]]` has

    det h = -AC-B^2 < 0,
    T=sqrt(A), beta=-B/A, L^2=C+B^2/A,
    T^2 L^2=AC+B^2=-det h.

Expanding `-T^2(dy+beta dσ)^2+L^2 dσ^2` gives exactly the three original Gram
entries `(-A,B,C)`. Reciprocal completion at fixed a asks
`sqrt(A) sqrt(C+B^2/A)/m=1`. Positivity gives the unique
`m=sqrt(AC+B^2)` and `L_s=1/sqrt(A)`. Hence

    chi = (1-A)/(1+A),       Phi = -log(A)/2.

Every step follows from the original metric contractions plus the declared
completion condition. No desired scalar was inserted in h.

For a new companion `b_new=k b+l a`, `k != 0`,

    B_new=kB-lA,
    C_new=k^2 C+2klB-l^2 A,
    A C_new+B_new^2=k^2(AC+B^2).

Thus `m_new=|k|m`, `T_new=T`, `chi_new=chi`, with shift information changed as
required. The same result for a companion outside the original two-plane follows
from its own positive orthogonal norm: chi depends only on A after completion.
This proves companion independence for a fixed calibrated a, not independence
from a, nor a unique physical companion/plane.

Since every Lorentz g and every timelike a locally admit a nonzero orthogonal
b, this normalization exists without imposing an equation on g. If an independent
physical ruler fixes m in advance, its agreement with this value is instead a
nontrivial compatibility condition. The candidate preserves exactly that limit.

## M2. Independent 4D shifted/clock witness

Use flat g=diag(-1,1,1,1) and the actual affine immersion

    F(y,σ)=(5y+σ, 3y+2σ, 2σ, 0).

Its independent tangents are `a=(5,3,0,0)`, `b=(1,2,2,0)`. Direct contractions,
before any completion, give

    g(a,a)=-25+9=-16,
    g(a,b)=-5+6=1,
    g(b,b)=-1+4+4=7,
    h=[[-16,1],[1,7]],       det h=-113.

All three original Gram residuals against these entries are zero. In particular,
the third spatial-coordinate contribution 4 is present in h11. Then

    T=4, beta=-1/16, L^2=113/16, m=sqrt(113),
    h_s=[[-16,1/sqrt(113)],[1/sqrt(113),7/113]],
    det h_s=-1, beta_s=-1/(16sqrt(113)), chi=-15/17.

Multiplying `diag(1,m) h_s diag(1,m)` returns h exactly. The projected companion
is `b_perp=b+a/16=(21/16,35/16,2,0)`. Its direct norm is
`(-441+1225)/256+4=113/16`, matching L^2 without extracting it from the determinant.

For an operational clock record choose
`z_o(b)=(5b/4,3b/4,0,0)`, so `U_o=(5/4,3/4,0,0)` has norm -1, and take b=4y.
Then q(y)=z_o(4y)=(5y,3y,0,0), q'=4U_o=a. The original ordinary proper-clock
equation independently gives `Z=4`, and the derived chi is `(1-Z^2)/(1+Z^2)`.
This is an exact encoding of the supplied correspondence, not a prediction of 4.

With y'=2y and the same ambient surface, the new coordinate clock tangent is
a/2: `T'=2`, `m'=sqrt(113)/2`, `chi'=-3/5`. This is a different calibrated query
if one then treats y' as the old source proper clock. Passive ambient coordinate
changes that also transform the original physical a do not change g(a,a).

More generally, an arbitrary common label t on corresponding source/target
events gives clock norms `T_e=d tau_e/dt` and `T_o=d tau_o/dt`. The measured
ratio is `Z=T_o/T_e`, invariant under common increasing t relabeling. Choosing
t=source proper time sets T_e=1 and makes T_o=Z. A common physical unit change,
with metric and proper-clock numbers converted consistently, also leaves Z
unchanged. This separates units/covariance from changing a physical clock leg.

## M3. Local clock-germ existence without propagation

For any supplied smooth increasing b=f(y), smooth future unit ordinary-clock
curve z_o(b), and supplied smooth Lorentz g, set q=z_o composed with f. The chain
rule gives q'=f' U_o, so its original norm is `-(f')^2`. On a short interval
choose a smooth nonzero orthogonal spacelike W and use

    F(y,σ)=exp_{q(y)}(σ W(y)).

At σ=0 the differential has columns (q',W), with Gram matrix
`diag(-(f')^2,g(W,W))`. Its rank is two, first entry negative, determinant
strictly negative. Those are open conditions, hence they persist on a small
neighborhood of every regular base point. This proves a local immersion germ;
compact subintervals admit suitably small tubular neighborhoods if required.
It asserts no global embedding, unique plane, connecting path or physical ruler.

Applying M1 gives `T=f'=Z` independently of W and therefore the clock encoding.
The existence proof uses no null ray or independent photon mechanism. It also
works for every smooth increasing f, which is why it cannot select the physical
f or prove that one completion is the unique realization of the founding words.

## M4. Conditional null-family identity by a variational route

Supply a smooth family F(y,λ) of nonzero affine null geodesic segments, with
fixed λ endpoints 0 and 1 and source proper-time parameter y. Let K=F_λ,
J=F_y. The geodesic energy functional for each member is

    E(y)=1/2 integral_0^1 g(K,K)dλ=0.

Its exact first variation is

    E'(y)=[g(K,J)]_0^1 - integral_0^1 g(nabla_K K,J)dλ.

Affine geodesy makes the integral zero, while nullness makes E' zero. Hence
`g(K,J)` has equal endpoint values. The same argument on every subsegment
shows it is constant along that member. At the endpoints `J_e=U_e`,
`J_o=Z U_o`. Defining positive contractions `omega_i=-g(K_i,U_i)` gives
`omega_e=Z omega_o` and `Z=omega_e/omega_o`. This is geometry of the declared
family, not an independent propagation ontology for the founding premise.

At reception direct contractions give

    h00=-Z^2, h01=-Z omega_o, h11=0,
    det h=-Z^2 omega_o^2,
    m=Z omega_o, beta_s=1/Z^2,
    h_s=[[-Z^2,-1],[-1,0]].

The nonzero shift is essential. Erasing h01 while leaving h11=0 gives determinant
zero, outside the admitted stratum. Along the full ray det h remains negative
because h11=0 and g(K,J) is a nonzero constant, but J need not stay timelike in
a general curved family. Thus the endpoint completion theorem does not by itself
prove a whole-ray clock-leg theorem. The candidate states this restriction.

## M5. Different original-equation null/control and exact coordinate trap

Use flat 1+1 g=-dt^2+dx^2. Source A(y)=(y,0); receiver trajectory
`x=4-(3/5)t`. Take `0<=y<=1` and

    d(y)=(20-3y)/8>0,
    F(y,λ)=(y+λd(y), λd(y)),   0<=λ<=1.

At λ=1 the receiver condition is exact:
`d = 4-(3/5)(y+d)`. The original affine and null residuals are
`F_λλ=(0,0)` and `g(F_λ,F_λ)=-d^2+d^2=0`.
Writing a=d'=-3/8, direct tangent contractions give

    K=(d,d), J=(1+λa,λa),
    h00=-(1+2λa)=-(1-3λ/4), h01=-d, h11=0,
    det h=-d^2.

Here `1-3λ/4` lies in [1/4,1], so the entire strip is regular. Receiver proper
unit tangent is U_o=(5/4,-3/4), with norm -1. At reception
`J_o=(5/8,-3/8)=U_o/2`; hence Z=1/2 directly from proper clocks. Contractions
give `omega_e=d`, `omega_o=2d`, agreeing with M4. Endpoint kernel is chi=3/5.
This approaching-clock control tests the sign and calibration; it is not a
claim about an isolated UDT positional contribution or a whole-postulate model.

The density is m=d(y), so `d(m dλ)=(-3/8) dy wedge dλ`, not zero. A genuine
new coordinate s=λd(y) instead satisfies

    ds=d dλ+λd' dy,
    F(y,s)=(y+s,s),
    g_pullback=-dy^2-2dy ds.

The new coordinate Gram matrix is `[[-1,-1],[-1,0]]`, whose y-coordinate
clock norm is 1, rather than the old `sqrt(1-3λ/4)`. There is no physical
contradiction: holding s fixed is a different tangent. The actual endpoint
clock tangent is `partial_y+d' partial_s`; its original norm is
`-1-2d'=-1/4`, preserving Z=1/2. Retaining that tangent preserves the physical
readout. Treating m dλ as ds while discarding λd' dy would incorrectly mix two
different clock calibrations. This explicit coordinate computation is a stronger
check than only observing non-closedness of the density one-form.

## M6. Explorer witnesses and historical conditional algebra

Recomputing the candidate's shifted witness from original tangent columns
`(2,0)` and `(1,3)` gives h=[[-4,-2],[-2,8]], det=-36, T=2, beta=1/2,
L=3, m=6, beta_s=1/12. Dividing the mixed/spatial entries by 6/36 gives
h_s=[[-4,-1/3],[-1/3,2/9]]. Its null condition for w=ds/dy is
`-4-(2/3)w+(2/9)w^2=0`, or `(w-6)(w+3)=0`. Thus the two coordinate null
slopes are 6 and -3, not the calibration factor T/L_s=4. The orthogonal proper
ruler is 3dσ=ds/2. All reported entries and signs agree.

For the candidate's receding flat control, d=(5+3y)/2 gives d'=3/2 and
`h00=-(1+3λ)`, h01=-d, h11=0, det=-d^2 by the same original contractions,
not by starting from a target h. At the receiver J=(5/2,3/2) and ordinary unit
U=(5/4,3/4), so Z=2, chi=-3/5. Density curl is +3/2 as stated.

For the evolving control `-dt^2/t^2+t^2 dx^2`, t>0, proper time is log t.
Nullness gives `|dx/dt|=1/t^2`. Fixed separation L therefore implies
`1/t_e-1/t_o=L` and `t_o=t_e/(1-Lt_e)` on 0<Lt_e<1. Differentiate log t_o
against log t_e to obtain `Z=1/(1-Lt_e)>1`. Reflection in x gives the same
result for the separately prepared opposite observation. It proves existence
of this conditional mutual-slowing geometry and defeats a universal static
obstruction. It does not derive its physical profile or identify an isolated
positional contribution.

Finally, for P=diag(u,v), direct multiplication gives
`P^T K P=[[0,uv],[uv,0]]` while `P^T eta P=diag(-u^2,v^2)`. Preserving K
requires uv=1; preserving eta would instead require u=v=1 for positive u,v.
These are different conditions on different forms. Continuous signed additive
composition makes u=exp(k delta), with v its inverse. By contrast ordinary
conversion covariance `v c_E=c_E u` gives v=u. These exact implications agree
with the July source's explicit premise split.

June's endpoint ratio f(b)/f(a) composes for every positive f. Difference-only
dependence plus continuity gives `f(phi)=C exp(k phi)`, C>0. A specified clock
normalization is needed to set C=1, and a nonidentity character to exclude k=0.
Nothing in this functional equation proves that swapping observer clocks swaps
time and radial coframe slots. The deep historical defense assumes precisely
that slot action; its exponential identity is valid after the action is supplied.

## M7. Finite-interval precision — parent-transmitted objection

After M1–M6 were written but before this record froze, the parent reported the
other review's finite/infinitesimal wording objection to candidate section 2.
This is not claimed as an independently discovered objection. Its mathematical
verification here is independent and exact: choose `f(y)=2y+y^2` on [0,1].
Then `Z(y)=2+2y>0`, but the finite interval ratio is

    (f(1)-f(0))/(1-0)=3,

which is neither endpoint value Z(0)=2 nor Z(1)=4. The exact general statement is

    Delta b = integral_y0^y1 Z(u)du,
    Delta b/Delta y = (1/Delta y) integral_y0^y1 Z(u)du.

Thus the candidate's description of equal tick intervals by pointwise Z needs
the word infinitesimal/local, or the stated finite average. All its subsequent
derivative identities survive. Constant-Z examples already have exact finite
ratios. The coordinator's promised source-preserving wording repair is adequate;
no new physical premise or rerun of M1–M6 is needed for that change.

## Check disposition

All candidate equations tested in M1–M6 agree exactly. M7 requires a narrow
finite-interval prose repair, independently verified after parent notification.
Original metric/null/
proper-clock equations independently support the examples; no scalar-only test
was used to certify its own physical clock input. The scoped historical defect
is a missing representation implication, not an algebra error in the conditional
reciprocal construction. No general no-go, whole-metric uniqueness theorem,
global clock realization, empirical truth or canon claim was tested or certified.
