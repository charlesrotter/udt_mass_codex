# ER1 — exact coupled metric/record expansion

Status: CONDITIONAL CANDIDATE, UNPROMOTED, fresh adversarial review pending.
Baseline grok 2d9f607fd0ff085aaaa93219028f6abb6d537091. Scope and discovery history are in
WORK_ORDER.md, DATA_FREEZE.md and the whiteboard freezes; source bytes are pinned separately.

## Result and source ceiling

Within a supplied smooth local Lorentzian metric, observer congruence and common comparison
marking, constant clock rate, stationary shift and flat rest-form coefficients are unnecessary
for KTI1's rotation extraction. An exact formula retains the time-live interaction. Six matched
directional completed records, augmented by their original ruler densities and common first
derivatives, suffice to recover that observer's local rotation. A finite compatibility test and
explicit metric realize those six record functions simultaneously in the declared class.

This is a statement about supplied configurations and typed records. G179 supplies the general
conditional coframe/pair evaluator; G166 explicitly leaves native time-live/mixed 3+1 assembly
open and forbids calling the unrestricted envelope the derived UDT solution space. The result
does not select the geometry, observer, events, pair population, physical instruments or field
law. G176's completed reciprocity remains a working foundational clarification, not canon.
G312 remains GR-filter-only; no Einstein equation enters. Standard polarization and differential
geometry are credited methods, not newly discovered physical laws.

## 1. Exact geometry, with every choice visible

On a supplied smooth local chart (t,x1,x2,x3), let

    g = -N² theta² + gamma_ij dx^i dx^j,
    theta = dt + beta_i dx^i,   N>0, gamma positive definite,
    U = N^-1 partial_t,   X_i = partial_i - beta_i partial_t.

The functions may depend on all four coordinates and are free-and-explored. The chart,
regularity, signature (-+++), observer and common marking are declared class choices, not new
physical premises or selected solutions. Units c_E=1 calibrate dimensions without selecting
a shape or scale. Pointwise g(U,U)=-1, g(U,X_i)=0 and g(X_i,X_j)=gamma_ij.
Gamma is the positive form on this observer's rest vectors. It is NOT the induced coordinate
slice metric g_ij=gamma_ij-N² beta_i beta_j; t=constant slices need not be spacelike.

Set P_a^c=delta_a^c+U_a U^c and w_ab=P_a^c P_b^d nabla_[c U_d], with bracket factor1/2.
The torsion-free connection cancels in the antisymmetric derivative. Since U_flat=-N theta,

    d(U_flat) = -dN wedge theta - N dtheta.

The first term vanishes on X_i,X_j. Direct evaluation of dtheta gives

    F_ij = partial_i beta_j - partial_j beta_i
           - beta_i partial_t beta_j + beta_j partial_t beta_i,
    w(X_i,X_j) = -N F_ij/2,
    W = w_ab w^ab = N² gamma^ik gamma^jl F_ij F_kl / 4.

This is an analytical identity for every metric in the stated local class, with the displayed
smoothness/positivity hypotheses. W is nonnegative because w is a two-form on a positive rest
space. In the basis X_i, gamma inverse performs the contraction. Lapse derivatives cancel for
this projection, while N's value and the rest form still weight W. No assertion is made that
lapse/spatial-form derivatives disappear from acceleration, shear or curvature.

For the stationary, unit-lapse, Euclidean-rest case this reduces to KTI1. In general, using
ordinary spatial curl alone discards a term bilinear in beta and its time derivative. The tensor
sign is checked separately because the quadratic W cannot detect an overall sign error.

## 2. What the completed records contain

For a fixed nonzero spatial vector v and base label a, use the actual surface

    F_(a,v)(t,sigma)=(t,a+sigma v).

Its columns (partial_t,v^i partial_i) commute and have rank two. These surfaces coexist in one
supplied geometry; no arbitrary independent pairwise geometries are silently glued. Their raw
pullback is

    h_v = [[-N², -N² beta(v)],
           [-N² beta(v), gamma(v,v)-N² beta(v)²]],
    det h_v = -N² gamma(v,v) < 0.

G179's pointwise completed-pair result then gives

    T_v=N,  m_v=N sqrt(gamma(v,v)),  B_v=beta(v)/m_v,
    Phi_v=-log N,
    H_v = [[-N²,-N² B_v],[-N² B_v,N^-2-N² B_v²]],  det H_v=-1.

Here H_v is the Gram matrix of the normalized pair germs. The common comparison-clock tangent
is K=partial_t=N U, not unit U. G216 gives T=dτ/dt=N. Relative endpoint depths alone do not
provide absolute T or the common transverse marking. A bare proper-clock column would have
T=1 and Phi=0; replacing K by U while retaining these records changes the query.

Neither a single scalar Phi nor a normalized H_v retains m_v relative to the original supplied
direction. Our augmented data keep that density and the original (t,x,v) identification.
Derivatives mean derivatives in this same common chart, including transverse derivatives;
along-pair samples alone do not automatically provide them. No instrument transfer is derived.

## 3. Finite simultaneous-realization recipe

Take D={e1,e2,e3,e1+e2,e1+e3,e2+e3}. Suppose smooth functions (T_v,m_v,B_v) on the same patch
are supplied with their common marking. Necessary and sufficient conditions for their realization
by the displayed g and these specific constant-direction surfaces are:

* a common positive T_v=N and positive m_v;
* the symmetric gamma reconstructed below is positive definite;
* m_(i+j) B_(i+j)=m_i B_i+m_j B_j for each i<j.

Indeed, put q_v=(m_v/N)² and b_v=m_v B_v. Necessity follows from evaluating a quadratic form
and a one-form on the six known vectors. For sufficiency define

    beta_i=b_i, gamma_ii=q_i,
    gamma_ij=(q_(i+j)-q_i-q_j)/2  (i<j).

The class conditions make g a smooth Lorentzian metric and K timelike. For each actual surface,
its pullback above reproduces T, m and B: positivity chooses the correct square root, polarization
reproduces all six q values, and sum coherence reproduces all six b values. This is also uniqueness
of the component reconstruction in this fixed chart and observer marking; it is not uniqueness
of physical geometry or selection of that marking. Restrict the surfaces to remain in the patch.

Differentiating these reconstruction identities on the common patch recovers the first metric
jet from full first jets of the records. In particular beta first derivatives, N and gamma values
give F and W. This is sufficient, deliberately redundant data; no minimality claim. Pointwise
values are insufficient for derivatives, and six individually positive lengths do not ensure
SPD. For example [[1,2,0],[2,1,0],[0,0,1]] is positive on all six D vectors but negative on e1-e2.
Arbitrary isolated jet arrays would additionally need the relevant compatibility equalities;
the statement here assumes actual smooth record functions on a common neighborhood.

This bounded reconstruction is standard linear/quadratic polarization. It is not a full inverse
theorem for arbitrary networks or the physical realization/selection of all pairs. G182's
distinction between intrinsic Gram data and supplied common immersion/coframe carry survives.

## 4. Time-live rulers require careful clock typing

At an event, rescaling the ruler column by1/m produces H_v. Along each fixed-t leaf, G180's
positive-density integral defines a tape. Across time, however, if

    s(t,sigma)=integral_0^sigma m(t,u) du,  alpha=s_t,

then ds=alpha dt+m dσ. The genuine two-dimensional transformed metric is

    h_(t,s) = -N²[(1-B_v alpha)dt+B_v ds]² + N^-2(ds-alpha dt)².

Its determinant is -1 but its fixed-s clock has

    T_fixed-s²=N²(1-B_v alpha)²-alpha²/N²,

when that tangent is timelike. All coefficients on the right are composed with the inverse tape
map. The original clock K becomes partial_t|s+alpha partial_s and retains its original norm.
The extra terms describe a coordinate change and, if fixed-s worldlines are chosen, a different
clock congruence. They are not a correction to the original kernel scalar or new physical law.
In general (partial_t,m^-1 partial_sigma) do not commute, so cannot be assumed to be one coordinate
basis across time. The original normalized germs remain valid pointwise.

Explicitly, g=-dt²+exp(2t)dx²+dy²+dz² and v=e1 give T=1,m=exp(t),B=0. With s=exp(t)sigma,

    h_(t,s)=[[-1+s²,-s],[-s,1]], det=-1,
    T_fixed-s=sqrt(1-s²) on |s|<1.

The original observer in this chart is partial_t+s partial_s and still has T=1. Thus a time-live
tape that also keeps the original clock requires extra compatibility, not just a one-dimensional
density integral. We do not claim G180's stated one-dimensional theorem is wrong or silently
extend it to all time-dependent pair charts.

## 5. Coupled exact witness and omissions

Choose supplied profiles

    N=1+t+y, a=1+t+x², gamma=a²[[2,1,1],[1,3,1],[1,1,2]],
    beta=(r,bx+q t,0).

On |t|,|x|,|y|,|z|<1/4, N>1/2,a>3/4; principal minors2,5,7 ensure positive gamma. The same
metric has variable lapse, time/spatial dependence in the rest form, mixed spatial coefficients,
and time/spatial shift variation. All six pair surfaces above are actual immersions in it.
The exact result is

    F_xy=b-rq, other independent F components zero,
    W=N²(b-rq)²/(7a⁴).

At the origin, r=q=1,b=3 gives W=4/7. Ordinary spatial curl alone gives9/7. Setting b=0 leaves
zero ordinary curl but W=1/7. Changing b leaves all six raw pair values at the origin unchanged,
yet changes W, so that event's values alone cannot own rotation. Keeping only Phi=-log N loses
the shift information even as a field. At the interior point (1/8,1/5,1/6,0), with r=q=1,b=3,
W=96100000000/185679617823 and all named variations are nonzero.

The coefficient-field gamma, treated purely as a Riemannian metric on the chosen coordinate
space at t=0, has scalar curvature -40/7 at the origin. This auxiliary diagnostic verifies that
we did not merely use a constant flat gamma in unusual linear coordinates. It is not curvature
of a hypersurface orthogonal to U or a field-equation check.

Under beta->epsilon beta, direct projection gives F_xy=epsilon b-epsilon²rq. A first-order
treatment omits the explicit order-epsilon² term. This exact polynomial identifies an interaction
that a frozen stationary slice or first-order calculation can miss; it establishes no nonlinear
dynamical development, amplification law, persistence or genericity.

The construction partner also supplies a stronger density-omission witness:

    g_lambda=-(dt+lambda x dy)²+lambda²(dx²+dy²+dz²), lambda>0.

For every constant v, T=1 and B_v=x v_y/|v| are lambda-independent, while m_v=lambda|v|.
Thus the entire six normalized pair-metric fields H_v agree for different lambda in the same
original coordinate labels. Direct metric projection/contraction gives W=1/(2lambda²): 1/2
for lambda1, 1/8 for lambda2. Omitting m can therefore obstruct W, not merely the metric's
component reconstruction. The profiles are mathematical controls, not a physical scale selector.

Other recorded controls reject missing mixed directions, non-SPD arrays, incoherent sum shifts,
unit-clock substitution, and omission of alpha from the time-live tape transformation.

## 6. Evidence, remaining restrictions and return point

Parent check_exact_geometry.py:40 exact symbolic identity/diagnostic checks and6 explicit mutants,
PASS, exit0, Python3.10.12/SymPy1.13.1, 3.37s. Partner initial67 and followup25 exact checks
PASS in separate saved scripts; these are construction evidence, not the required later review.
The full analytical arguments above own the quantifiers; passing finite tests do not prove them.
Freeze times, argv, stdout/stderr and hashes are saved. No parent scientific check has failed.
The source-pin filename mistake is a preserved packaging event, not a scientific repair.

Fresh adversarial review must examine full hypotheses, signs/factors, common-label and tape
typing, finite realization, omissions, the coupled witness, and source/roadmap fidelity. Review
does not promote G176, admit the envelope as native solutions, or validate physical instruments.

Completed here at candidate level: local exact geometry/readout expansion (roadmap1–2) and a
bounded actual simultaneous-realization recipe (stage3). Remaining: native assembly, physical
pair/calibration population, equation selection, nonlinear development and reach/persistence.
The next discussion must keep the conditional nonlinear line visible and identify its exact
equation/premise budget before any campaign. Neither this result nor the roadmap dispatches it.
