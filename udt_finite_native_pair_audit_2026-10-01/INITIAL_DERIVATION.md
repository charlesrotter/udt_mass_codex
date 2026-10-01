# FNA1 fixed initial derivation — typed finite representation

Candidate for adversarial review, not native physical admission. Construction
uses the supplied FPC1 space forms and its actual prepared-clock experiment.
Positive/zero/negative curvature remain free comparisons. Parent worked out
the null-family pullback and ambient transport before reading a peer proof.
Peer brief concordance about a receiver-anchored ribbon and the static-chart
boundary was received before this written freeze; full source-first proofs/code
have not been read. The source-first peer also independently obtained the boost
entries below. Independent-context and same-model exposure are recorded separately.

## 1. Primary metric representation, with its real domain

Let sectional curvature be kappa=+k² or -k², k>0 supplied. In the regular static
patch about a chosen geodesic observer, the full four-metric is

    g=-f(dx0)²+f^-1 dr²+r²(dtheta²+sin²theta dvarphi²),
    f=1-kappa r²>0, x0=c_E t,
    phi_stat=-log(f)/2.

It has exactly F4's declared areal-sphere readout, with founded radial coframe
D(phi_stat)=diag(sqrt(f),1/sqrt(f)), determinant-one radial normalization,
and full volume density r²sin(theta) in these length-time coordinates. F2's
pairing is preserved, and F3 composes on ordered depth; proper distance L is
not thereby an additive depth. The spherical coordinate pole/center is treated
with local Cartesian angular charts. phi_stat is smooth as a function of r²
near r=0 and vanishes there. Constant curvature makes each geodesic-centered
laboratory equivalent by isometry; this does not infer constant curvature from
observer equivalence or adopt G212's stronger all-germ isotropy premise.

The full metric, including the sphere, is the previously checked quadric metric.
No Einstein equation, source or action is used to obtain this representation.
For kappa=0 use the ordinary Minkowski limit separately. One familiar metric
form is a supplied solution of a representation problem, not a selected UDT law.

For positive curvature put alpha=kL, w=tan(alpha), p=sec(alpha), m=w/k.
At preparation B0 has areal radius sin(alpha)/k. At the actual first reception,
its areal radius is m=tan(alpha)/k. Hence that event lies inside A's static f>0
patch only for alpha<pi/4, whereas the first clock branch exists for alpha<pi/2.
The first null ray crosses that chart's horizon when m>=1/k. Extending sqrt(f)
or real phi_stat past that patch is invalid. The ambient construction below
continues smoothly using the supplied Lorentz geometry and local coframes;
it does not derive a global UDT extension law from the primary chart.

Even within the patch the different clock queries must not be identified:

    phi_stat(B0)=log p,
    phi_stat(B_first)=-log(1-w²)/2,
    Phi_clock=-log p.

The free receiver's clock leg is not the static coordinate clock. At the patch
boundary phi_stat(B_first) diverges while p=sqrt(2) remains finite. Thus these
are demonstrably different typed readouts, not inconsistent signs of one scalar.

## 2. Construct the pair from the actual signal family

Use the signed quadric inner product <X,X>=1/kappa in its appropriate five-
dimensional ambient signature. At A0 let X0 be the position, U its future unit
clock, and n the prepared radial spatial unit. X0,U,n are mutually orthogonal,
with norms1/kappa,-1,+1. Two additional unit screen directions are retained.
For a nearby emission proper time s, let b(s) be FPC1's already geometrically
determined actual reception map on fixed A,B geodesics. Define

    D(s)=B(b(s))-A(s),
    F(s,lambda)=A(s)+lambda D(s), 0<=lambda<=1.

This is the family of actual affinely parametrized null chords, not a rank-two
matrix chosen to have the desired clock coefficient. D²=0 and A·D=0 keep each
chord on the quadric. F_s and F_lambda give the full immersion germ, including
its nonzero shift. At lambda=0, F_s=U_A; at lambda=1, F_s=b' U_B.

At s=0 set p=b'(0)>0 and define the positive affine-span density

    m=-<U,D>,  D=m(U+n),  p²=1+kappa m².

For positive curvature m=tan(kL)/k and p=sec(kL); for negative curvature
m=tanh(kL)/k and p=sech(kL), with0<m<1/k. Flat space has m=L,p=1.
The receiver tangent at first reception follows by differentiating its geodesic:

    p U_B=p²U+kappa m X0+kappa m² n.

Consequently J=F_s=(1-lambda)U+lambda p U_B has

    h00=<J,J>=-A(lambda),
    A(lambda)=1+kappa m² lambda(2-lambda),
    h01=<J,D>=-m,  h11=<D,D>=0,  det h=-m².

For all0<=lambda<=1, A lies between1 and p², both positive. Thus the full pair
is regular rank two even though its affine coordinate tangent is null. G179
requires h00<0 and det h<0, not h11>0. The clock-orthogonal ruler is spacelike:
L_lambda²=h11-h01²/h00=m²/A>0. Smooth dependence and compactness supply a
nearby-emission regular strip for each fixed finite experiment; no uniform window
at the asymptotic boundary is claimed. The actual ambient screen is retained;
its absence from this radial germ follows from the constructed invariant plane.

W1/G176–G179 now determine, rather than fit,

    T=sqrt(A), beta=m/A, L_lambda=m/sqrt(A),
    completed density=sqrt(-det h)=m,
    h_completed=[[-A,-1],[-1,0]], beta_completed=1/A,
    Phi(lambda)=-log(A)/2, chi(lambda)=(1-A)/(1+A).

At the emission end A=1 and Phi=0; at reception A=p² and

    T_B=p, Phi_B=-log p, chi_B=(1-p²)/(1+p²), q_pair=p².

Thus the actual null family explicitly fills the full-pair-plane slot left
unconstructed by G220's clock-leg compatibility identity in this supplied planar
experiment. The shift must remain: setting it to zero while retaining h11=0
would destroy regularity. Conversely q_pair is not a second local signal speed.
No extra redshift function was attached after the pullback.

The coordinate lambda is dimensionless; m has length units, whereas T and Phi
are dimensionless. The integral of m d lambda along this fixed-emission family
is m, not the initial spacelike L or the null proper length (which is zero).
Calling this completed tape a universal physical distance or X_max would be an
additional assignment. For varying s the density is m(s)=-<A',D> and generally
depends on s; at preparation m'(0)=p²-1. Therefore m(s)d lambda is not in general
an exact spacetime differential holding s fixed. G180 integrates it on a given
one-parameter family only. A genuine new spatial coordinate rho=m(s)lambda
adds m'(s)lambda ds to d rho and changes fixed-rho clock tangents; silently
dropping that term would corrupt the comparison. Completion here is a calibrated
coframe/density statement, not an unproved two-coordinate gauge transformation.

## 3. Full path-labelled transport and W5

Along X(lambda)=X0+lambda D, a vector V initially tangent to the quadric is
parallel when its ambient derivative is normal:

    dV/dlambda=-kappa <D,V> X(lambda),
    P V=V-kappa <D,V>(X0+D/2).

<D,V> stays constant. This solves the connection equation, preserves all inner
products and tangency, and transports D to itself. It is an independently
constructed full metric isometry, not an assumed boost inferred from p alone.
Take source tetrad (U,n,e2,e3) and target tetrad

    U_B=(p²U+kappa m X0+kappa m²n)/p,
    n_B=(n-kappa m X0)/p, e2,e3.

n_B is the radial direction parallel-transported along the preparation and then
along B; the screen vectors are ambient constant and tangent. In these declared
endpoint frames the full morphism is

    Lambda=[[Gamma,S,0,0],[S,Gamma,0,0],[0,0,1,0],[0,0,0,1]],
    Gamma=(p+1/p)/2, S=(1/p-p)/2.

It preserves eta4 and the future orientation. Its signed radial rapidity is
delta=-log p. The future outgoing null column(1,1,0,0) has frequency multiplier
Gamma+S=1/p, recovering Z=p from full transport. W5's projective clock column is

    bold_chi=(S/Gamma,0,0)=((1-p²)/(1+p²),0,0).

Here its signed radial component equals chi_clock because the actual path and
frames are aligned in this invariant plane. This closes that equality for this
experiment, not for arbitrary paths/screens. An endpoint spatial frame rotation
rotates the vector; full nonradial composition still needs frame/direction carry
(G274). The frame morphism is not the diagonal D(phi_stat), and its physical
normalized projective coordinate is not sin(kL), kL, or areal radius times k.

The inverse Lambda belongs to reversed mathematical transport of the same event
pair. The independently emitted reverse first signal uses another future path
and has the same p in its oriented propagation frames. The later echo has q from
FPC1 at different events. Neither is identified with the inverse map. Compositions
must keep actual path labels and middle frames; a radial scalar identity does
not prove global endpoint exactness or absence of curvature holonomy.

## 4. Information and angular checks beyond the radial scalar

The full metric and screen warp are retained before restriction. As an explicit
nonradial diagnostic at a regular static coordinate point, use supplied columns

    J0=(1,0,v/r,0), J1=(0,1,w/r,u/(r sin theta)), v²<f.

They give h00=-f+v², h01=vw and h11=1/f+w²+u². Both angular directions are
visible; W1 normalizes the full determinant and keeps the shift. This is a
separate supplied diagnostic germ, not a new clock population or the actual
radial null branch. Deleting the sphere's terms changes the output.

For local metric information, six declared pairs (e0,ei), (e0,ei+ej) for i<j
give g00,g0i,gii and gij=[h11(i+j)-gii-gjj]/2. These known germs reconstruct
all ten symmetric components. They are regular for the static metric and a
sufficiently small open neighborhood of it. Each (m,h_completed) reconstructs
its raw h by diag(1,m)^T h_completed diag(1,m), so the same rank-ten information
survives W1, as G213 already proves. This is tomography of supplied data, not
generation of their values or physical selection of that six-query population.

The current G201/G260 local primary angular expressions give

    A_parallel=(r² f''-r f')/2=0,
    A_perp=1-f+r f'/2=0

for f=1-kappa r². This is the already known zero-angular-amplitude family,
not evidence that the sphere can be removed or a new field equation. It selects
no sign or kappa. The full4D **imported Ric=0 comparison** instead has

    E0=r f'+f-1=-3 kappa r²,
    E1=r f'+r² f''/2=-3 kappa r².

Thus nonzero curvature is not that exact vacuum comparator. Its local flat limit
does not establish W3's complete quiet field-law/source recovery, tested solar
phenomenology or a full UDT parent equation. No old reciprocal-loudness slogan is
adopted in place of the current angular ownership controls.

## 5. Native audit ceiling

The constructed supplied geometry has a primary F4 representation where that
chart is regular; the actual finite signal family supplies an explicit regular
W1 pair with density/shift, actual clock depth and full path-labelled W5 transport.
The latter continues beyond the emitter static patch without changing any local
clock law. These are substantive conditional representation results. They do
not prove the whole geometry satisfies every physical UDT requirement or that
its sign/scale/global realization is selected by the native premises.

G298/G300 retain the distinction between the enriched causal relation and a
uniquely owned physical rank-two projection/query family. A radial example can
hide their transverse separator. The ribbon here is tied explicitly to the
supplied signal family; another spatial germ/projection remains a different
query, not a rival scalar at this same full input. No universal unique physical
projection is inferred. Later received-tick clarification already fixes the
observable; it does not license erasing remaining transverse/global input types.

W3's law-level recovery and additional-effect requirement remain unestablished
by this representation; DDR's response identification remains open. All three
curvature signs pass the local representation construction while their first
clock shifts differ. Passing this audit therefore cannot by itself select the
desired sign, shape or physical k. Identifying the finite first/echo/chart limits
with X_max would likewise exceed the result. This does not prove the full
clarified postulates insufficient, require a new premise, or reject UDT.
