# NE1 — fading profile does not imply recovery of the marked vacuum geometry

Initial candidate, 2026-09-09. UNPROMOTED; direct review PENDING.
One exact nonlinear-development result, not a stability or physical-content theorem.
This candidate was written before new reviewer scientific disclosure. The author
already knew the standard mathematical route described in WORK_ORDER.md; no
claim of discovering a new general Gowdy theorem or of a blind author argument.

## 1. Scope and supplied data

The active bounded vacuum equation is S_ab=Ric_ab-R g_ab/4=0, OWNER-PROVISIONAL
through G310/G312, not a bare-metric derivation or canon. G303's connected
integrability gives Ric=Lambda g, dLambda=0. Work in Lambda=0. On the supplied
split translation T3, X has period 2pi and y,z have supplied positive periods.
Use the unit initial spatial metric at background T=1, signature -+++ and
K=-(1/2)L_n gamma. These are initial data and normalizations, not new laws.

The starting datum is SE1's flat-metric, variable-rate construction:

    q=e cos X, gamma=I,
    K^i_j=diag(1/3-3q²/4, -2/3-q, -2/3+q).                 (1)

SE1 explicitly used e=1/6. Here we also examine the analytic family with
arbitrary real finite e, including its zero-amplitude limit; the extension
is checked here and is not attributed to SE1's previously reviewed quantifier.
For every e, H=(tr K)²-tr K²=0 and M_X=-partial_X(Kyy+Kzz)=0;
the other momenta vanish. These hold everywhere on the whole compact slice.
No freely specified higher-order completion is added to (1).

The claim concerns this plus-polarized one-mode family and its supplied
marked T2 orbits, not all G327 directions, arbitrary symmetry-breaking data,
other quotients, or a preferred cosmology. It does not require that UDT
uniquely select the legitimate initial configuration. Nor does it supply
that selection. No carrier, action, source, instrument or boundary law is used.

## 2. Full exact development and data matching

Set xi=4X/3, with period 8pi/3, and k=3/4. Let t>0 be normalized orbit area.
The following is a candidate exact metric, not a truncation at first order:

    g = exp(lambda/2)t^(-1/2)(-dt²+dxi²)
        +t[exp(P)dy²+exp(-P)dz²],
    a=lambda/4-(log t)/4, N=exp(a), n=N^(-1)partial_t.      (2)

Direct original-metric Ricci reconstruction (check_original_metric.py), or
the standard polarized-Gowdy reduction, gives the sufficient full equations

    P_tt+t^(-1)P_t-P_xixi=0,
    lambda_t=t(P_t²+P_xi²), lambda_xi=2t P_t P_xi.         (3)

No discarded Ricci components remain. For transparency, in the a notation:

    Ric_tt=-a_tt+a_xixi-P_t²/2+a_t/t+1/(2t²),
    Ric_txi=-P_t P_xi/2+a_xi/t,
    Ric_xixi=a_tt-a_xixi-P_xi²/2+a_t/t,
    Ric_yy=exp(-2a+P)(tP_tt-tP_xixi+P_t)/2,
    Ric_zz=-exp(-2a-P)(tP_tt-tP_xixi+P_t)/2.              (4)

The remaining components are identically zero or symmetric duplicates.
Substituting (3), a_t=-1/(4t)+t(P_t²+P_xi²)/4 and a_xi=tP_tP_xi/2,
including their compatible derivatives, annihilates every component in (4).
This checks the original admitted equation, not only a selected profile ODE.

Let F solve F''+F'/t+k²F=0, F(1)=0, F'(1)=3/2. Explicitly,

    F(t)=A_k J0(kt)+B_k Y0(kt),
    A_k=-(3pi/4)Y0(k), B_k=(3pi/4)J0(k),
    P=e F(t)cos(k xi), lambda0=4 log(3/4),
    L(t)=t²(F'²+k²F²)/2+t F F'/2-9/8,
    lambda=lambda0+e²[L(t)+t F F' cos(2k xi)/2].          (5)

The Bessel Wronskian gives the stated initial derivative. The ODE gives
L'=t(F'²+k²F²)/2 and (tFF'/2)'=t(F'²-k²F²)/2. Thus (5) satisfies
BOTH constraints in (3), with L(1)=0 and lambda(1,xi)=lambda0. All functions
are real analytic and periodic in xi for t>0. In particular the integral
of lambda_xi around the circle vanishes; no nonperiodic drift was hidden.

At t=1, N=3/4, P=0 and nP=2q. The pullback by xi=4X/3 gives gamma=I.
Since a_t=-1/4+9q²/16 there, K^X_X=-a_t/N=1/3-3q²/4; the other entries
are exactly -2/3-q and -2/3+q. This matches the FULL initial pair (1), not
just its linear transverse block. The original and areal normals coincide
on this slice; away from it the areal normal generally accelerates and is
not SE1's continued Gaussian geodesic normal.

Formula (5) gives a smooth Lorentzian metric on every finite positive-t slab,
and hence on (0,infinity) x T3. Compactness and bounded metric/lapse on each
closed finite slab ensure no causal curve can terminate inside a finite slab;
the t-slices provide a Cauchy development there. This is an explicit actual
development, not a formal time jet or a successful numerical relaxation.
Conditional local uniqueness up to diffeomorphism, as recorded in G303/G315,
identifies it locally with the development of the same initial pair in a
different legal gauge. No assertion of a maximal extension, geodesic
completeness, behavior at t=0, smooth stability or general global theorem
is needed. No extra endpoint admissibility condition is imposed.

## 3. Recovering the accepted first-order mode

At e=0, t=T^(4/3), xi=4X/3 transform (2) exactly into

    g0=-dT²+T^(-2/3)dX²+T^(4/3)(dy²+dz²).                (6)

Since lambda-lambda0 is exactly order e² at fixed t, the first variation has
delta g_yy=2T^(4/3)h(T)cos X=-delta g_zz, h=F(T^(4/3))/2,
and no other components. Direct conversion gives

    h_TT+h_T/T+T^(2/3)h=0, h(1)=0, h_T(1)=1.            (7)

This is precisely the supplied unit-normalized plus/cosine member of G327,
with z=3T^(4/3)/4. It is not the complete eight-constant sector. Its profile
and normalized first derivative decay with envelope T^(-2/3) at first order.
For e!=0, T=t^(3/4) is only a background comparison label, not proper time.
Treating lambda as unchanged beyond first order produces Ric_tt=-P_t²/2
and fails the original equation. First-order decay and nonlinear backresponse
therefore are compatible, not contradictory results.

## 4. A geometric comparison and a forced cumulative response

Use the supplied period-normalized transverse Killing generators. Their
orbit-area density rho=sqrt(g_yy g_zz)=t is a scalar once this marking is
specified; equivalently use orbit area divided by the supplied coordinate
period product. Define the timelike area-gradient norm and fractional rate

    Z=-g^ab partial_a rho partial_b rho=N^(-2),
    H_rho=n(log rho)=sqrt(Z)/t.                           (8)

Compare with (6) at the SAME rho and marking, not at equal coordinate/proper
time chosen independently in the two spacetimes. The exact ratios are

    Z/Z0=exp[-(lambda-lambda0)/2],
    H_rho/H_rho0=exp[-(lambda-lambda0)/4].                (9)

These are geometric for the declared orbit-area comparison; a coordinate
change does not remove them. The marking/foliation is supplied, not physically
selected. They are not a proof concerning every unmarked diffeomorphism-
invariant notion of asymptotic closeness. H_rho is orbit-area expansion, not
the full volume expansion, which is

    theta=div n=N^(-1)[3/(4t)+t(P_t²+P_xi²)/4].          (10)

For fixed k>0 the standard real-positive-argument Bessel asymptotics yield

    F=D t^(-1/2) cos(kt-delta)+O(t^(-3/2)),
    F'=-kD t^(-1/2) sin(kt-delta)+O(t^(-3/2)),
    D²=2(A_k²+B_k²)/(pi k)>0.                           (11)

The constant phase includes the usual pi/4 shift. A_k and B_k cannot both
vanish because their canonical Wronskian is nonzero. Put
sigma=k(A_k²+B_k²)/pi=k²D²/2>0. This is a computed response coefficient,
NOT the connected scalar Lambda, an absolute scale, c_E, or a new law.
Equation (5) and (11) imply L=sigma t+O(1), tFF'=O(1), so, for each fixed
nonzero e, uniformly in xi,

    P=O(t^(-1/2)) ->0,
    lambda-lambda0=e² sigma t+O(1),
    Z/Z0 ->0, H_rho/H_rho0 ->0.                          (12)

Constants depend on fixed amplitude, wavelength and normalization; this is
not a uniform small-amplitude-infinite-time perturbation estimate. At each
finite t the first-order limit still holds. The e->0 and t->infinity limits
of (9) do not commute. Exact e=0 preserves (6). Arbitrarily small nonzero
members of this specified family have (12); no generic-data claim follows.

Thus fading in the selected profile does NOT imply recovery of the original
marked geometry. Once the whole initial pair (1) is supplied, the quadratic
metric response in (3) is imposed by the SAME equation; it is not an invented
coupling or extra physically chosen response term.

## 5. Curvature check, not just a metric-profile diagnostic

Let e_y,e_z be the unit vectors along the supplied orthogonal Killing fields,
and use the areal n. Because Ric=0, set E_y=C(e_y,n,e_y,n) and similarly E_z.
Original Riemann reconstruction gives

    (E_y-E_z)/Z = -P_xixi-P_t/(4t)
                  +t P_t³/4+3t P_t P_xi²/4,
    D_tidal=(E_y-E_z)/H_rho²
           =t²[-P_xixi-P_t/(4t)+tP_t³/4+3tP_tP_xi²/4].  (13)

This is a dimensionless curvature contrast for the declared normal/directions,
not a curvature norm, conserved energy, instrument law, or frame-free complete
curvature classifier. Its Taub value is zero. At xi=0 and extrema t_j of F,
F'(t_j)=0, hence D_tidal=e k² t_j² F(t_j). From (11), F' has zeros in
successive neighborhoods of the alternating cosine extrema, and at those
zeros F(t_j)=(-1)^j D t_j^(-1/2)(1+O(1/t_j)), up to indexing. This follows
by opposite derivative signs on either side of each large phase multiple
of pi, followed by (11); the derivative-zero equation forces sin phase
to be O(1/t_j). Consequently D_tidal has alternating unbounded subsequences
for e!=0, even though P tends uniformly to zero. This is relative tidal
non-recovery, NOT divergent absolute curvature or physical instability.

Convention check: the linear orthonormal tidal coefficient is
-h_T/(3T)+T^(2/3)h. G327 equation (15) uses background-normalized coordinate
components; restoring the first-order transverse basis variation adds
4h/(9T²), exactly its coefficient. Omitting this distinction gives a false
disagreement. At the original e=1/6 initial xi=0 point, (13) yields
E_y-E_z=-5/48 and D_tidal=-15/256, consistent with SE1's full electric tensor.

## 6. Checks, mathematical methods and remaining limits

Author original metric check: 32 predicates, including all 16 Ricci entries,
full initial gamma/K, constraints, tidal contrast and volume expansion.
Identically zero off-sector components, symmetry duplicates and trivial
transverse derivatives are coverage/regression, NOT independent evidence.
Two actual mutations fail: keeping a at its Taub value, and dropping the
quadratic K completion. Profile check: 13 predicates; identities, Bessel
ODEs, initial data, linear coordinate/basis conversion; dropping lambda's
spatial term fails the momentum constraint. Algebraic normalizations and
basis bookkeeping are not independent re-proofs of G327.

Numerical values are illustrative 60/90-digit SAME-LIBRARY mpmath checks,
not interval certification or proof of asymptotics. For e=1/6 at t=100,
max|P| is about .0271 but H_rho/H_rho0 is .4960–.5002; at t=1000 these
are .00996 and .0008754–.0008771. No fitted observation or physical timescale
is attached. Proof of (12)–(13) uses the analytic formulas and standard
Bessel estimates, not these finitely sampled numbers.

Primary methods: Jurke, gr-qc/0210022 equations (1)–(5), only its metric/PDE
reduction; NIST DLMF 10.5.2 and 10.17.3–4 (and derivative expansions) for
canonical Wronskian and fixed-order positive-argument asymptotics. Their
hypotheses are satisfied here. No broader Gowdy completeness theorem or
physical interpretation is imported. METHOD_SOURCES.md gives exact links.

SE1's full-Weyl scalar A is not asserted to be controlled by (8) or (13).
This is not a conclusion about the LG2 gluing collar, other polarizations,
arbitrary inhomogeneity, generic persistence/failure, stability, matter,
light, or an observed UDT universe. G303/G315's theorem caveats survive where
their gauge-uniqueness statement is used. NR2 is background provenance, not
needed as a hidden nonlinear existence premise for explicit metric (5).
Full365 still FAILS at G325; new result remains unpromoted. Review is pending.
