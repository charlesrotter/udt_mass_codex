# NCR1 source-first reconstruction

Reviewer `/root/ncr1_directional_review`, fresh separate context, 2026-09-12.
Parent startup is attributed. Independently observed `grok` HEAD
`314704f5fb52174e7ef57c686bed02e106e3ab9a`; tracked status was clean, the
new package and pre-existing untracked entries remained visible. No protected
payload was opened. Assigned source hashes match SOURCE_PINS.json.

This was written without opening the new parent's candidate, implementation,
or outputs. Exposure: dispatch/question/WORK_ORDER/LAUNCH/SOURCE_PINS;
AGENTS and triggered shared protocols; G394 original metric and reviewed
clarification; current G312 authority and exact G220/G312/G394/G415 rows;
original G415 candidate, reviewed result and direct review; actual G415
BANKING_RECORD; G220 audit. Thus prior source verdicts and general methods
were exposed. Runtime model/version is UNATTESTED. This is not different-model,
different-premise, human-specialist, formal-proof or interval certification.

Question: retain the exact supplied metric at every finite real epsilon,
t_e=1, common initial orthonormal sky direction, same source label, areal
observers, and equal marked t_o. Receivers may have different labels. Study
frequency contraction, with G220 clock interpretation only on its regular
branch. No off-axis no-conjugacy extension is made. Current G312 FILTER ONLY
qualifies inherited equation ownership. The result is conditional metric
mathematics, unpromoted and not physical light or a selected cosmology.

## Exact equations reconstructed from the source metric

Write a=log N, b_y=sqrt(t) exp(P/2), b_z=sqrt(t) exp(-P/2), and let
(c,h_y,h_z) be a unit initial sky direction. Since t_e=1 has N_e=3/4 and
b_y(e)=b_z(e)=1 independently of epsilon, common omega_e=1 gives

    p(1)=(3/4)c, p_y=h_y, p_z=h_z, H(1)=3/4.

The two transverse Killing momenta are constant. Put

    q^2=p_y^2+p_z^2=1-c^2,
    Q=p_y^2 exp(-P)+p_z^2 exp(P),
    W=N^2 Q/t, H=sqrt(p^2+W)=-p_t, v=p/H.

The null Hamiltonian, solved for the future t momentum, yields exactly

    xi'=p/H,
    p'=-W_xi/(2H),
    y'=N^2 p_y/(t exp(P) H),
    z'=N^2 p_z/(t exp(-P) H),
    omega=H/N, R=1/omega.

For q>0, set eta=(p_z^2 exp(P)-p_y^2 exp(-P))/Q, |eta|<=1.
Then W_t/W=lambda_t/2-3/(2t)+eta P_t and
W_xi/W=lambda_xi/2+eta P_xi. Thus

    v'=-(1-v^2)/2 [(log W)_xi+v(log W)_t].

Writing r=atanh(v), this becomes the stable bounded-coefficient equation

    r'=-(lambda_xi+v lambda_t)/4+3v/(4t)
        -eta(P_xi+v P_t)/2,       xi'=tanh(r).       (A)

The original source identities lambda_t=t(P_t^2+P_xi^2),
lambda_xi=2t P_t P_xi are retained. In particular lambda_t>=|lambda_xi|.
None of this assumes conserved longitudinal momentum or time-only lapse.

The zero-amplitude control has conserved p and

    omega_0^2=c^2 t^(1/2)+q^2/t.

Define E=sqrt(t) omega. Nullness gives the especially useful readout

    E=sqrt(Q) cosh(r),
    R/R0=sqrt(c^2 t^(3/2)+q^2)/E.                  (B)

The axial q=0 branch is handled separately by the admitted G415 result;
atanh is not used at v=+/-1.

## A uniform late rapidity barrier

For each fixed epsilon!=0 the accepted positive-argument Bessel estimates,
including derivatives, imply uniformly in xi

    P_t+P_xi=-epsilon k D t^(-1/2) sin(kt+kxi-delta)+O(t^(-3/2)),
    P_t-P_xi=-epsilon k D t^(-1/2) sin(kt-kxi-delta)+O(t^(-3/2)),
    k^2 D^2=2 sigma>0.

All coefficients in (A) are bounded for t>=1 and uniformly in source phase,
sky azimuth and eta. For r sufficiently positive, v is uniformly close to
one, so (A) reads

    r'= -t(P_t+P_xi)^2/4 + O(1-v)+O(t^(-1/2)).

The constants may depend on fixed nonzero epsilon, never on q or eta. The
phase theta=kt+kxi-delta has derivative k(1+v). On any interval of fixed
length T=2pi/k while r>=M, choose M so v>=1-d for a sufficiently small d.
Then theta' lies between k(2-d) and 2k. Its advance is at least
2pi(2-d), hence at least one full 2pi turn if d<1. Therefore

    integral sin^2(theta) dt >= pi/(2k)

on that interval, using dt=dtheta/theta' >= dtheta/(2k). Choosing d small
and then t sufficiently large makes the integrated error less than half
the resulting fixed positive damping. Hence r(t+T)-r(t)<=-b<0 whenever
r stays above M throughout this late interval. The negative-r argument uses
theta=kt-kxi-delta, theta'=k(1-v), and gives r(t+T)-r(t)>=b when r<=-M.

To make the barrier implication explicit, let |r'|<=C. An excursion above
M starts at r=M (unless already above at the initial late time), cannot
gain more than CT in its first T, and every complete subsequent T interval
contained in that excursion has negative net increment. Consequently its
height is at most max(r(t_*),M)+CT. The analogous lower bound holds below
-M. On the finite [1,t_*] interval the same bounded derivative gives

    |r(t)| <= |r(1)|+C_epsilon     for every t>=1, q>0.  (C)

This deliberately loose form is enough. It does not claim r converges,
xi converges, or a constant late frequency prefactor. Large/small-amplitude
uniformity is not asserted.

Because q cosh(r(1))=1 and Q<=q^2 exp(|P|), (C) gives

    sqrt(t) omega <= C_epsilon

uniformly over the whole initial sky and source phase for q>0. Finite-time
continuous dependence, or the exact axial formula directly, includes q=0.
For each fixed q>0, Q>=q^2 exp(-|P|) supplies the lower bound as well:

    omega=Theta(t^(-1/2)),     R=Theta(t^(1/2)).      (D)

These statements depend on the explicit interval damping argument, not on
replacing the spatially varying lapse by its average.

## Directional consequences and exceptional directions

For every fixed direction with 0<|c|<1 and epsilon!=0,

    R/R0=Theta(t^(3/4)),
    lim log(R/R0)/t=0,
    lim log(R/R0)/log(t)=3/4.                         (E)

Constants can be uniform on sky bands bounded away from both axes and the
transverse equator. More strongly the sky-uniform upper bound in (C) gives

    R/R0 >= (c_*/C_epsilon) t^(3/4)

uniformly on either closed cone |c|>=c_*>0, including its axis. Thus mere
late contrast persistence has finite angular reach in this supplied
comparison; the exact axial positive exponential rate does not persist at
any fixed nonzero tilt. The axial rate is beta=epsilon^2 sigma/4.

The momenta alone supply a useful necessary angular narrowing bound:

    R/R0 <= exp(|P|/2) t^(3/4)/q,       t>=1, q>0.   (F)

If a direction at time t attains R/R0>=A exp(gamma t), gamma>0, then
q <= A^-1 exp(|P|/2)t^(3/4) exp(-gamma t). This is only a necessary
condition for an exponential-sized contrast, not sufficiency, an exact
transition profile, or an angular census theorem.

At c=0, the contrast is 1/E and (D) only gives Theta(1). It is incorrect to
extend (E) to this equator. At xi_e=m pi/k both P_xi and lambda_xi vanish
for all t; a purely transverse ray keeps xi fixed and p=0. Its
R/R0=1/sqrt(Q) ->1. At xi_e=(m+1/2)pi/k and p_y^2=p_z^2=1/2,
P=0, eta=0 and lambda_xi=0, so p=0 and R/R0=1 identically. These mixed-tilt
controls show why a universal all-sky strict contrast claim would fail.
Generic equatorial asymptotic classification, monotonicity, a finite-time
off-axis sign theorem, fixed-label reception, and off-axis conjugacy remain
unproved and outside the maximum asserted result.

## Evidence limits and chronology

The reconstruction is an analytic review argument from admitted source
formulas. The finite numerical contract is separate and will be frozen
before its outcomes. No numerical result proves (C)-(F). G394's full Ricci
construction and the full398 audit are not recomputed here; the parent owns
the current full398 run. Existing capture utilities are reused unchanged.
This review allocates one context only, conservatively from 21:00UTC to
no later than21:40UTC including direct review and final fidelity, within
the parent's 22:57:06UTC hard return. An actual source-stage seal will pin
this file before scientific findings are sent to the parent. Hashes record
correspondence, not independently signed chronology.
