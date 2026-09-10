# QC1 source-first adversarial reconstruction

Reviewer context: `/root/quiet_step1_review`, fresh separate agent context.
Exact model identifier UNKNOWN; different-model review UNTESTED. Date2026-09-10.
Pinned repository HEAD:2a3e64befd72b801cdd54e528d9a7c68362cdd7b, branch grok.
No Git mutation or synchronization performed by this reviewer. Parent reports
fresh synchronization; reviewer independently verifies only local HEAD/status.
Parent campaign/roadmap changes and protected/unrelated status names visible;
protected payloads not inspected or hashed. Own writes restricted to this review.

## Exposure and authority

Before this report: dispatch question, current bounded startup/registry rows,
AGENTS/CLAUDE/triggered protocols/CROSS_MODEL, work order, prior direction brief
and its reviewed R1/R2 scope corrections, G260 derivation, G312 current authority,
and historical LC1 geometric clock contract. Parent's proposed QC1 proof, code,
outputs and candidate have NOT been opened. Prior direction review contains no
proof of this bound. Its warnings about data dependence are known exposure.

Independent full365 execution fails unchanged at G325:
`AssertionError: replay_exact:DERIVATION_RESULT.json`.
This report is conditional mathematical exploration, UNPROMOTED. It does not
adopt C_ang=0 or Ric=Lambda g as a physical equation. Filter-only GR authority
and inherited historical-source caveats remain. No physical residual value,
instrument/transfer law, stability, nonspherical or dynamical claim follows.

Exact source SHA-256:

- G260 EXACT_DERIVATION.md:
  de32fc105dfe9cdbc964959a67c46a0eee58f95566b2df4f2ce115c48b6776da
- G312 current AUTHORITY_RECORD.md:
  80daa0be6d3e1c0ac1b734fea089c4eb487f05bc1e1fbb2fabd69322ca89f28c
- LC1 step_01/COMPARISON_CONTRACT.md:
  ac6cbaeb359713d90abb71b43e83a47bc2e7d669f878c01c1b1455cb1c8541e4
- This campaign WORK_ORDER.md:
  ebec3b67abd25fbc336a69fcbb6c0c153036816cbb5e074d6df91f024e00ac90

## Question, assumptions and method before checks

For every positive C2 F on fixed compact dimensionless areal-radius interval
I=[alpha,beta],0<alpha<=1<=beta, and every positive balanced comparison H
determined by two supplied anchor data, does continuous residual sup control
bound geometric readouts, allowing two independent signed anchor mismatches?
Anchor r0>0 and x=r/r0 are supplied normalization, not a selected physical scale.
Metric/symmetry restriction, interval, data and positive margins are declared
choices (`free-and-explored`); the exact G260 identity is source-pinned conditional
geometry (`pinned-by-THEORY` at that scope). No physical value is pinned by habit.
Method: solve the linear Euler identity exactly and apply finite-domain norm
estimates. No Taylor truncation, physical response law or outcome fitting.
Ordinary check budget: single thread,512MiB,60CPU/wall seconds, one reviewer CPU
slot; reuse existing run_capture.py with absolute output stem. No GPU.

## Independent exact argument

Write q(x)=C_ang[F](r0*x), so q=x^2 F_xx/2-F+1. Let
H=1+A*x^2+B/x. For supplied data d0=H(1),d1=H_x(1),
A=(d0-1+d1)/3 and B=(2*(d0-1)-d1)/3.
Set w=F-H and e0=w(1),e1=w_x(1). The identity is exactly
w_xx-2*w/x^2=2*q/x^2, without a new governing-law assumption.

Fundamental solutions x^2,x^-1 have Wronskian -3. Variation of constants gives

    w(x)=e0*h0(x)+e1*h1(x)+integral_1^x K(x,t)*q(t)dt,
    h0=(x^2+2/x)/3, h1=(x^2-1/x)/3,
    K(x,t)=(2/3)*(x^2/t^3-1/x).

This formula is valid on BOTH sides of the anchor. For x<1, K is negative on
[x,1], but the integral orientation reverses. The residual-to-w integral has
nonnegative oriented kernel. Its absolute kernel mass is

    k0(x)=(x^2+2/x-3)/3=h0(x)-1 >=0.

The x derivative K_x=(2/3)*(2*x/t^3+1/x^2) is positive, and K(x,x)=0.
Thus the derivative integral changes orientation for x<1, with absolute mass

    k1(x)=abs((2/3)*(x-x^-2))=abs(h0_x(x)).

For abs(q)<=epsilon, pointwise bounds follow:

    abs(w)<=abs(e0)*h0+abs(e1)*abs(h1)+epsilon*k0 = b0(x),
    abs(w_x)<=abs(e0)*abs(h0_x)+abs(e1)*h1_x+epsilon*k1 = b1(x),
    abs(w_xx)<=2*(b0(x)+epsilon)/x^2 = b2(x).

Here h1_x=(2*x+x^-2)/3>0. No derivative of q is required; continuity and F C2
suffice. On a fixed compact interval D_j=sup b_j are finite and linear in
abs(e0),abs(e1),epsilon. The D2 bound need not be sharp to be valid. For exact
data e0=e1=0 and constant residual q=epsilon the w and w_x kernel bounds are
attained at every x (with w_x sign reversed left of1); w_xx likewise saturates
the displayed residual-only b2. This can be checked independently from
F=H+epsilon*(h0-1).

## Geometric readout consequences

Assume F,H>=m>0 throughout I; let M_H=sup H and J_H=sup abs(H_x).
These are supplied finite data/domain constants, never silently uniform over
all comparison metrics. Natural readout bounds are:

    abs(sqrt(F)-sqrt(H)) <= D0/(2*sqrt(m)),
    abs(log(sqrt(F))-log(sqrt(H))) <= D0/(2*m),
    abs(d_r log(sqrt(F))-d_r log(sqrt(H)))
      <= (D1/m+J_H*D0/m^2)/(2*r0),
    abs(d_ellF log(sqrt(F))-d_ellH log(sqrt(H)))
      <= (D1/sqrt(m)+J_H*D0/(2*m^(3/2)))/(2*r0).

The last is comparison of each metric's radial orthonormal component at the
same supplied areal radius, since d_ell=sqrt(f)*d_r. It is NOT comparison at
equal proper distance unless another point-identification estimate is made.
Supported acceleration is c_E^2 times that component; c_E is calibration.

For static clock ratios Q_F(x,y)=sqrt(F(x)/F(y)), supplied common time
normalization and identical point identification give, by splitting numerator
and denominator,

    abs(Q_F-Q_H) <= D0/(2*m)+sqrt(M_H)*D0/(2*m^(3/2)).

An alternative relative/log ratio bound is abs(log(Q_F/Q_H))<=D0/m.
These are geometric proper-clock ratios, not a claimed photon transfer or
atomic instrument model. Exact anchor matching allows a sharper denominator
bound when y=1. Arbitrary finite errors must retain denominator error.

Using signature(-+++) and R^rho_sigma mu nu=partial_mu Gamma^rho_nu sigma
-partial_nu Gamma^rho_mu sigma+GammaGamma-GammaGamma, the orthonormal nonzero
independent Riemann components are

    R_0101=F_xx/(2*r0^2),
    R_0202=R_0303=F_x/(2*r0^2*x),
    R_1212=R_1313=-F_x/(2*r0^2*x),
    R_2323=(1-F)/(r0^2*x^2).

So their differences are bounded by D2/(2*r0^2),D1/(2*r0^2*alpha),
and D0/(r0^2*alpha^2), respectively. The electric tidal entries are only the
first two; geodesic-deviation acceleration adds a conventional -c_E^2 factor.
The comparison pairs the static orthonormal frames at the same radius; static
frames require positivity. No derivative of q beyond continuity enters tides.

## Early adversarial conclusions

The proposed fixed-domain implication appears provable. Main failure risks:
wrong left-anchor orientation, two unspecified homogeneous integration modes,
uncontrolled reference/data factors for nonlinear readouts, missing r0 units,
confusing coordinate/proper lapse gradient, and calling a pointwise or sampled
residual bound a continuous supremum certificate. Reference positivity cannot
be inferred from an arbitrary positive F and arbitrary anchor data without a
margin estimate. If H>=m_H>0 and D0<m_H, then F>=m_H-D0 supplies one such estimate.
Conversely positivity may simply be assumed for both profiles, as scoped.

No finite sample verifies a continuous residual bound absent regularity/error
information. No growing-domain, horizon or r0->0 uniformity follows. These are
mathematical controls, not observations. Review of parent's actual candidate
and an independently coded check remain pending when this source-first report
is saved. No verdict about the unseen candidate is implied.
