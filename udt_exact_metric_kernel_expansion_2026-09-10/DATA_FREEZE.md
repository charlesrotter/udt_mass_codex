# ER1 construction freeze — exact supplied metric and matched records

Prepared after disclosed mathematical exploration, before the parent's scientific checks.
FREEZE_RECEIPT.json records actual freeze time and hashes. The partner has its separate earlier
freeze and exposure record; neither is a blinded prediction or a new physical premise.

## Target and domain

For C2 functions on a supplied local coordinate patch (t,x,y,z), declare

    g = -N²(dt + beta_i dx^i)² + gamma_ij dx^i dx^j,
    N > 0, gamma symmetric positive definite, U = N^-1 partial_t.

N, beta and gamma are free-and-explored supplied functions. Signature, smoothness, observer
congruence, marking and common clock/ruler calibration are stated hypotheses. c_E=1 fixes
units, not shape, scale or a physical parameter. This is G179's conditional evaluation envelope;
G166 does not admit every such metric as a native UDT solution. No field equation is supplied.

The general claim concerns this entire declared smooth local class, not sampled metrics. Its
argument must be analytical; symbolic identities and witnesses check the argument. No assertion
of minimal data, unique physical observer, global metric, dynamics or physical realization.

## Frozen formulas and actual records

Let X_i = partial_i - beta_i partial_t and theta = dt + beta_i dx^i. Define vorticity by
w_ab = P_a^c P_b^d nabla_[c U_d], P_a^c = delta_a^c + U_a U^c (brackets include 1/2).
With U_flat = -N theta, predict

    F_ij = partial_i beta_j - partial_j beta_i
           - beta_i partial_t beta_j + beta_j partial_t beta_i,
    w(X_i,X_j) = -N F_ij/2,
    W = w_ab w^ab = N² gamma^ik gamma^jl F_ij F_kl / 4.

All temporal terms are retained. Lapse derivatives cancel only after this projection; N's value
and gamma's inverse still weight W. This says nothing about other kinematic/curvature components.

Use six constant directions v=e_i and e_i+e_j (i<j), original common labels, and actual surfaces
F_(a,v)(t,sigma)=(t,a+sigma v). K=partial_t=N U is the common comparison-clock tangent,
not the unit proper-clock tangent. Raw h is their pullback; G179 pointwise completion predicts

    T_v=N; m_v=N sqrt(gamma(v,v)); B_v=beta(v)/m_v; Phi_v=-log N.

Retain T (or Phi), m, B and original common labels/first derivatives. These extra records and
their common marking are supplied data, not outputs of the scalar alone. Reconstruct

    beta_i=m_i B_i, gamma_ii=m_i²/N²,
    gamma_ij=(m_(i+j)²-m_i²-m_j²)/(2N²).

Require smoothness, common positive T, positive m, reconstructed gamma positive definite and
m_(i+j) B_(i+j)=m_i B_i+m_j B_j. Within this explicitly marked six-record class, examine necessity
and sufficiency for local realization by these actual surfaces and a metric of the stated form.
This finite reconstruction is standard polarization with specified data, not a universal inverse
or all-pair completeness theorem. Values reconstruct pointwise geometry; common first jets are
needed for W. Cross-query matching, m retention and derivatives are not silently inferred.

Time-live normalization of the ruler germ is not automatically a two-dimensional coordinate
change retaining the original clock. For s(t,sigma)=integral_0^sigma m(t,u) du, ds=s_t dt+m dσ.
Check the full pullback, determinant -1, and changed fixed-s clock. Pair-germ evaluation remains
valid; a time-live global tape with the same clock needs additional compatibility. No contradiction
to G180's stated one-dimensional family result is claimed.

## Coupled exact witness and expected rejection controls

Use N=1+t+y, a=1+t+x², gamma=a² G0 with
G0=[[2,1,1],[1,3,1],[1,1,2]], beta=(r,bx+q t,0). Real constants r,b,q are supplied controls.
On |t|,|x|,|y|,|z|<1/4, N>1/2, a>3/4; G0 principal minors 2,5,7 prove SPD.
Predict F_xy=b-rq, W=N²(b-rq)²/(7a⁴). At origin r=1,b=3,q=1 gives W=4/7.
The rest-basis gamma varies in time and space and has mixed components. If used, its ordinary
three-dimensional coordinate-field curvature on fixed t at origin is predicted -40/7; that
diagnostic is not curvature of an integrable observer-rest hypersurface or a field equation.
An additional interior rational point (t,x,y,z)=(1/8,1/5,1/6,0) checks nonconstant weights.

Controls must reject ordinary spatial curl alone (predicts 9/7 at origin), dropping N/gamma
weights away from unit/flat values, wrong antisymmetrization sign/factor, discarding m or mixed
directions, assuming positive six diagonal lengths imply SPD, inconsistent sum shifts, treating
one event's record values as first jets, and ignoring s_t in a time-live tape change. The case
b=0,r=q=1 has zero ordinary spatial curl and W=1/7 at origin. It is an exact diagnostic, not a
selected physical state. Optional amplitude comparison beta->epsilon beta has
F_xy=epsilon b-epsilon²rq; if retained, give the exact omitted term, not an uncontrolled approximation.

## Execution and maximum conclusion

CPU SymPy exact algebra, finite matrices (4x4 metric, 3x3 rest form, 2x2 pair pullbacks); no grids,
random/fitted parameters, observations, GPU or long solve. Scientific subprocesses capped120s,
campaign hard return00:48:30 UTC. Save exact script/argv/versions/stdout/stderr/result/exit/hash.
Failures remain saved; changes after freeze require a named repair and unchanged initial bytes.
Parent direct exterior-derivative checks and the partner's construction are author evidence.
One later fresh context must inspect hypotheses/proof, independently recalculate load-bearing
geometry/record compatibility, and review continuity edits. It is not automatically a different
model, implementation or argument. Return VERIFIED-WITH-CAVEATS at most, UNPROMOTED; registry,
CANON, scientific sources, manuscript, protected payloads and later research are outside scope.
