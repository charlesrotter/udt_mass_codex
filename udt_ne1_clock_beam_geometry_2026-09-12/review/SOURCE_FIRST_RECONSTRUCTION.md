# NCB1 source-first reconstruction — sealed before candidate exposure

Reviewer `/root/ncb1_clock_beam_review`, fresh scoped context, 2026-09-12.
Runtime model/version UNATTESTED; different-model axis UNTESTED. No old reviewer
context or NCB1 parent scientific candidate/code/output opened. The question,
work order and source route names were exposed. Parent mandatory startup and
earlier same-session full397 PASS are attributed from SESSION_RECORD.json;
this reviewer independently found branch grok and HEAD
f9408abeeff016210cddbfd9da968d3753091c49 with unrelated untracked work preserved.
No protected payload was read. Sources and exact reviewed IDs G220/G312/G342/
G348/G394 were read; method protocols were read from disk. Current G312 GR
FILTER ONLY controls historical Einstein-branch ownership labels.

## Question and computation freeze

Apply G348 metric quotient-screen/Jacobi definitions and G220's supplied regular
null clock query to the supplied G394 NE1 metric, both longitudinal signs,
finite real amplitude e, and 0 < t_e < t_r < infinity. Markings, transverse
periods, k=3/4, and original datum are supplied by G394; longitudinal rays and
areal observers are declared restrictions, not derived selections. Exact
metric geometry only; no physical light, distance, response-law construction,
stability, generic-data assertion, or promotion. Fixed endpoints versus late
emission along a fixed coordinate lift are different comparisons.

Planned source-first computation: original symbolic diagonal-metric
Christoffels and R(X,k)k contraction, affine geodesic and parallel-screen
identities, vacuum trace cancellation, both screen Jacobi equations. CPU,
exact SymPy algebra, no grid/GPU, one library thread, <=180 s/2048 MiB per
scientific subprocess; at most eight reviewer runs across all stages.
Symbolic coverage zeros and identities are not independent proof counts.
Later numeric checks, if needed, use finite 64-bit or arbitrary-precision
samples as support only, never proof at infinity or interval certification.

## Independent metric and clock route

Write g=N^2(-dt^2+dxi^2)+b_y^2 dy^2+b_z^2 dz^2, a=log N,
b_y=sqrt(t)exp(P/2), b_z=sqrt(t)exp(-P/2), with NE1's full exact P,lambda.
For s=+1 or -1, put x(t)=x_e+s(t-t_e) and D_s=partial_t+s partial_xi.
The null constraint and original affine geodesic equation give

    h=dt/dv=N_e/N(t,x(t))^2,  k=h(partial_t+s partial_xi),
    omega=-g(k,n)=N_e/N,  omega_e=1,
    r=d tau_r/d tau_e=omega_e/omega_r=N_r/N_e.

The same clock slope follows from the endpoint incidence equation
t_r-t_e=L for fixed marked observer locations and the supplied lift.
Thus this endpoint law is valid despite spatially varying lapse; it is not
an unauthorized application of G220's time-only triangular example.
Against e=0 at matching t endpoints and marks,

    r/r0=exp[(lambda_r-lambda_e)/4].

The identity D_s lambda=t(D_s P)^2>=0 gives r/r0>=1 on each future leg.
For e!=0 and positive leg length the inequality is strict: an identically
zero D_s P on an open interval would analytically continue to a constant
P along the ray; decay forces that constant to zero, contrary to nonzero F
and a cosine with nonzero ray frequency. This proof uses analytic NE1 data.

## Independent Jacobi route and curvature

E_i=b_i^-1 partial_i are exactly parallel on the axial ray. A unit source
sky variation in screen i has conserved transverse momentum delta p_i=b_i,e.
At first order the longitudinal position/velocity are unchanged: the
transverse momenta enter longitudinal geodesic equations quadratically.
Therefore the fixed-affine screen map is diagonal with both entries

    D_i=(b_i,e b_i,r/N_e) int_[t_e,t_r] N(t,x(t))^2/b_i(t,x(t))^2 dt.

Each D_i is positive for t_r>t_e, has D_i(v_e)=0 and dot D_i(v_e)=1.
This is a rank-two infinitesimal position map, not a statement that the
entire rank-four phase map has been enumerated. No finite future conjugate
point occurs on these rays, but quotient cut ties remain possible.

Direct original Levi-Civita curvature yields

    T_i=-h^2[b_i^-1 D_s^2 b_i-2(D_s a)b_i^-1 D_s b_i].

This is derived from R(E_i,k)k, not defined by -D_i''/D_i. Set q=D_s P.
The NE1 constraints give D_s a=(t q^2-1/t)/4 and hence

    T_y=-h^2[q'/2+3q/(4t)-t q^3/4], T_z=-T_y,
    q'=D_s q.

The integral solution obeys dotdot D_i+T_i D_i=0 by differentiation.
The Wronskian and source normalization give reverse-direction magnitude
D_i,reverse=(N_e/N_r)D_i,forward on the same reversed segment, with the
corresponding past-directed reception-normalized ray. The area ratio is
(N_r/N_e)^2=r^2 as required by G348. A later causal return is another leg.

## Zero-amplitude and asymptotic attacks

At e=0, N=(3/4)t^-1/4 and

    D_y=D_z=(3/2)t_e^(3/4)(sqrt(t_r/t_e)-1)=v_r-v_e.

This is exactly G342's longitudinal limit with T=t^(3/4), reused control.
G394 already owns P=O(t^-1/2), lambda-lambda0=e^2 sigma t+O(1), sigma>0.
Those uniform bounds hold on x(t). With fixed t_e=1 and fixed e!=0,

    log(r/r0)/t_r -> e^2 sigma/4,
    log(D_i/D_i,0)/t_r -> e^2 sigma/2,
    log(det D/det D0)/t_r -> e^2 sigma.

For the beam statement, beta=e^2 sigma/2>0 and positive constants bound
N^2/b_i^2 above/below by exp(beta t)t^-3/2 for large t. Splitting the integral
at t/2 bounds it above by C exp(beta t)t^-3/2; the last fixed-length interval
gives the corresponding lower bound. The early interval is exponentially
smaller. Multiplication by b_i,r=Theta(sqrt t) gives
D_i=Theta(exp(beta t)/t), then the displayed logarithmic rate. The constants
depend on fixed e and source; no uniform e->0, t->infinity exchange is valid.
At t_e=1, D_y/D_z->1 because P_r->0 and the positive endpoint-dominated
integrals have integrand ratio exp(-2P)->1. Circularization of the two widths
would therefore not rescue background recovery.

For a FIXED supplied coordinate lift length L>0 and fixed emission location
x_e, put t_r=t_e+L and x_r=x_e+sL. Take F=D t^-1/2 cos(kt-delta)+O(t^-3/2),
F'=-kD t^-1/2 sin(kt-delta)+O(t^-3/2), k^2 D^2=2 sigma. Along this short leg,

    q=-e k D t^-1/2 sin(k t_e+s k x_e-delta+2k(t-t_e))+O(t^-3/2).

Integrating the exact nonnegative D_s lambda=tq^2 gives

    lambda_r-lambda_e
      =e^2 sigma[L-sin(2kL)/(2k)
         cos(2k t_e+2s k x_e-2delta+2kL)]+O(1/t_e).

For fixed nonzero e and L>0, L-|sin(2kL)|/(2k)>0. Thus r/r0 stays bounded
away from 1 at late emission; it generally oscillates, with constant limit
exp(e^2 sigma L/4)>1 when sin(2kL)=0. This neither diverges with t_e nor
converges generically. Since r0=((t_e+L)/t_e)^-1/4->1, the same persistence
relative to unity survives for r. Fixed coordinate L is not fixed proper
baseline or proper travel duration. e=0 and L=0 are distinct boundaries.

The fixed-order positive-real Bessel remainder and derivative hypotheses were
checked against NIST DLMF 10.17(i)-(iii), https://dlmf.nist.gov/10.17,
accessed 2026-09-12. This is a mathematical method, no extra physical premise.

## Ownership and omitted checks

G394 owns the exact metric/development and accumulating lambda, G342 the
background beam, G348 the general quotient/reciprocity theorem, G220 the
regular clock-query identity. Evaluating the nonzero-amplitude NE1 beam and
the two stated late-time comparisons is the distinct local join inspected
here. This is not an exhaustive novelty search. No full397 rerun, old source
numerical replay, general Gowdy theorem, nonaxial ray, finite beam, alternative
observer, physical apparatus or independent response-law closure is claimed.
This source-first argument shares the source geometry and standard methods;
fresh context and independently written implementation do not prove
different-model/library or premise independence.
