# SD1 source-first reconstruction

Fresh context `/root/signal_shape_review`, allocation 3/3, conservative start
2026-09-13T03:55:09Z; hard end 04:35:09Z. Configured parent attribution is
gpt-6-astra/xhigh; runtime model UNATTESTED, different-model UNTESTED. This is
source/method-exposed reconstruction, not blind discovery. The SD1 work order
already disclosed its Taylor/rank route, intended cases, and numerical gates.
At this seal no SD1 candidate, scientific implementation, or parent numerical
output has been read. BE1 candidate/result/C1 and G421/CSS3 and G423/CSS5 were read.
Parent top-level startup and 406-row audit are attributed, not repeated: saved
BE1 checks/premise406.json reports returncode 0, 400.19077900308184 seconds.
Local branch and HEAD checked as grok, 3ce1bcb806d506b21bb20eabd5b942df0613880c;
unrelated untracked paths were inspected by names only and preserved.

The question is local amplitude identifiability after fixed ideal initial L,Q
calibration in the known two-mode zero-phase family, at t_e=1, xi_A=7/10, on the
positive axial branch of G421. Metric and signal equations retain their
conditional scope; BE1 is an explicit CONDITIONAL UNPROMOTED dependency. The
layout/profile choices are free-and-explored and the two-mode axial restriction
is pinned-by-HABIT. No physical selection, acquisition, or empirical premise is
added. Numerical work is CPU only, one scientific subprocess and one library
thread, at most 180s/2048MiB per capture; no GPU, long solve, or subdelegation.

Write theta=21/40, k=3/4, c_j=cos(j theta), eta=a_2 and
a_1=(Q-c_2 eta)/c_1. c_1>0 supplies BE1 C1's rank hypothesis. Put
q=P_t(1,xi_A)=3Q/2 and r=P_txi(1,xi_A). Along fixed Q,

 beta = partial_eta r
      = (3/2) k [c_2 tan(theta)-2 sin(2theta)]
      = -(3/2) k tan(theta)[1+2 cos(theta)^2] < 0.

Let s=t-1=xi-xi_A along the ray and a=log N. Initial P=0 and the
profile equation imply P_tt=-q, so

 P(s)=q s+(r-q/2)s^2+O(s^3),
 a'(s)=-1/[4(1+s)]+(1+s)(P_t+P_xi)^2/4,
 a(s)-a(0)=(q^2-1)s/4+(1/8-q^2/8+q r/2)s^2+O(s^3).

Therefore the positive clock ratio R=N_o/N_e obeys
partial_eta log R=(q beta/2)d^2+O(d^3). If Q != 0, this gives local
discrimination at every fixed finite (Q,eta), for sufficiently small positive d.

The labelled log beam ratio W=log(D_y/D_z) from CSS3(11) is

 W=P(d)+log integral_0^d w(s)e^-P(s) ds
          -log integral_0^d w(s)e^P(s) ds,
 w=N^2/t,  w'(0)/w(0)=(q^2-3)/2.

Expansion of these positive integrals gives

 W=[r/3+q(1-q^2)/12]d^2+O(d^3),
 partial_eta W=(beta/3)d^2+O(d^3).

The target ruler contribution P(d) is essential: it cancels the leading
integral contribution and changes the quadratic derivative from -2 beta/3
to beta/3. Thus labelled beams locally distinguish eta even at Q=0, eta=0.
Initial-rate Jacobian rank plus this conditional one-dimensional derivative
supplies local rank; this is not a global inverse or a noise bound.

At Q=0 the entire profile is P=eta H and lambda-lambda0=eta^2 Lambda_H.
Hence R(eta)=R(-eta), D_y(eta)=D_z(-eta), exactly at every finite d>0.
The equal supplied y,z periods permit the axis-exchange isometry; unmarked
geometry and an unordered width pair/aspect ratio cannot recover that sign.
Labelled W changes sign. This does not imply that clock data fail to determine
|eta|: along the ray Lambda_H(d)=integral_0^d (1+s)(H_t+H_xi)^2 ds>0,
because H(s)=beta s^2+O(s^3), so for each d>0 the clock ratio is strictly
increasing in eta^2. Near d=0 its logarithmic derivative is
2 eta beta^2 d^3/3+O(d^4). At eta=0 it is exactly zero by evenness.

For each compact finite parameter neighborhood and sufficiently small d with
t bounded away from zero, the finite Bessel profiles and lapse are analytic.
Dividing width integrals by d removes their removable d=0 zero; their leading
value is positive. Logarithms and parameter derivatives therefore have analytic
remainders bounded on that compact neighborhood. The local inverse theorem
applies for sufficiently small positive d. No universal operating d, uniform
unbounded-amplitude/frequency limit, all-profile inversion, or robust inference
is asserted.

Independent check design sealed alongside this argument: evaluate Bessel
profiles with mpmath at 50 digits, but reconstruct the lapse on the ray through
the integrated full constraint, rather than importing BE1's closed quadratic
primitive or SD1 implementation. Integrate positive beam weights and their
analytic eta variations by independently generated Gauss nodes. Check two
orders, leading derivatives, exact sign-swap symmetry, and positivity on a
small frozen finite list. This is high-precision floating point, not certified
interval arithmetic. Direct review may add an explicitly outcome-exposed check;
any scientific code additions and failures will be preserved.
