# ND1 — static angular/response discriminator

Status: INITIAL CANDIDATE / UNREVIEWED / UNPROMOTED, 2026-09-09.
No physical response or filter is adopted. The current G312 authority record
overrides stronger historical W3 and equation-adoption wording in sources.

## Starting definitions and exact question

Let I be a connected open interval in (0,infinity), f in C2(I), f>0, and

    g = -f dt² + f^-1 dr² + r²(dtheta² + sin²(theta) dphi²).

Time units absorb the fixed clock/ruler calibration c_E; no physical scale is
chosen. Angular charts avoid coordinate poles; statements are tensorial on
the spherical patch. All four metric directions and sphere curvature remain.
Define the Ricci endomorphism M=g^-1 Ric and the symmetric covariant tensors

    S = Ric - (R/4)g,
    Q = g [M² - (tr(M²)/4) I].

Q is exactly G312's existing local Ricci-square counterresponse. It has
curvature weight TWO and a degenerate flat first variation, not the full
G301 weight-one/principal class. It is not UDT's adopted response. G310/G311
DDR for a specified symmetric E imposes TF(E)=0, not E=Ric by definition.
Both S and Q are already trace-free, so their DDR equations are S=0 and Q=0.

Keep separate the geometric G260 readout/filter

    C_ang = A_parallel + A_perp = r² f''/2 - f + 1.

The word filter here means the declared exact test C_ang=0 on this supplied
static class, not an observed tolerance or a universally adopted quiet law.
G260 already proves its family f=1+a r²+b/r. That result is reused, not new.

## ND1-IDENTITY — full tensor factorization in this class

The complete-metric Ricci endomorphism is diag(A,A,B,B), with

    A = -f''/2 - f'/r,
    B = (1-f)/r² - f'/r,
    R = 2(A+B),       C_ang = r²(B-A).

These follow equivalently from G260's full 4D Einstein components and trace.
Writing s=(A-B)/2, the mixed S is diag(s,s,-s,-s), whereas mixed Q is
diag((A²-B²)/2,(A²-B²)/2,(B²-A²)/2,(B²-A²)/2). Therefore exactly

    Q = (A+B) S = (R/2) S.

This tensor identity is restricted to the two-double-eigenvalue ansatz. It
is NOT an identity for arbitrary four-dimensional curvature.

## ND1-CLASS — complete connected-interval Q=0 classification

Within the stated domain, Q=0 if and only if f belongs to one of the families

    E: f=1+a r²+b/r,       a,b constant;
    Z: f=1+b/r+d/r²,       b,d constant,

restricted to an interval on which f>0. Their intersection is
f=1+b/r (a=d=0). Constants and domains are supplied data, not selected values.

Proof. The factorization gives (A-B)(A+B)=0 everywhere. Where A=B, the ODE
r²(f-1)''-2(f-1)=0 has exponents 2,-1 and gives family E on that region.
Where A differs from B, A+B=0 gives

    f''+4 f'/r+2(f-1)/r²=0,

whose exponents are -1,-2, giving family Z on every connected component of
U={r in I: A(r) differs from B(r)}. On such a component,

    A=-d/r⁴,    B=d/r⁴,    A-B=-2d/r⁴,

with a fixed nonzero d. A component cannot have an endpoint inside I:
continuity would require A-B=0 there, but its limit is -2d/r_endpoint⁴,
which is nonzero at a positive finite endpoint. Hence U is empty or equals
I (connectedness). If empty, the E ODE holds everywhere; otherwise the Z
ODE holds everywhere with constant coefficients. This excludes unexamined
smooth switching between the factors. C2 regularity suffices. Direct
substitution proves the converse. No finite sample proves this exhaustion.

## ND1-FILTER — what cancellation can and cannot distinguish

On E, A=B=-3a and C_ang=0; R=-12a is constant. On Z,

    R=0,       C_ang=2d/r².

Therefore intersecting Q-DDR solutions with C_ang=0 removes exactly the
additional Z members with d!=0 and leaves the entire E family. It does not
select a=0, absolute scale, or the response architecture: all E members
solve both S=0 and Q=0. G260 already owns the fact that angular cancellation
does not alone imply Ricci-flatness. The extra datum d is not identified as
charge, source or carried content; it is a supplied metric coefficient.

In particular, shared balanced background metrics cannot distinguish S and
Q as response formulas. The conditional filter constrains candidate solution
metrics here, not the unique law generating them. This comparison does not
prove nonselection by all admitted UDT structure in every domain.

## ND1-PAIR — radial blindness is not all-pair balance

At any regular event use an orthonormal frame. For E=Ric the clock/radial
reciprocal contraction is 2(-A+A)=0 for EVERY f. The clock/angular contraction
is 2(B-A)=2 C_ang/r². Subtracting the trace term does not change either
reciprocal contraction, so the same statements hold for S. On Z with d!=0,
the angular contraction is 4d/r⁴ and is nonzero. Radial-only testing would
falsely pass S-DDR, which G311 requires on all admissible pairs.

For Q, however, EVERY contraction vanishes on Z, since the full tensor Q
vanishes. The nonzero native angular readout C_ang does not contradict
Q-DDR: these are different quantities unless an additional connection is
established. Q cannot be rejected by silently defining its balance to mean
the geometric C_ang test. This separation is the load-bearing interpretive
boundary, not merely a check of a successful example.

## Evidence and novelty limits

Analytic factorization plus Euler-ODE/connectedness argument are the proposed
proof. Small exact tensor-jet checks are computational support, not proof of
connected-interval completeness. The reused G260 tensor utility makes those
checks shared-code regression relative to its source; new independent reviewer
calculation is separately reported. Original source packages are not rewritten.

New to this candidate: the entire Q solution class in this supplied ansatz,
its branch-switching exclusion and its exact intersection with the G260
filter. G260 cancellation, G311 full-pair shape, and G312's degeneracy/solution-
overlap counterexample are established inputs, not new discoveries. No claim
of novelty in general relativity/mathematics, or no-go beyond this test class.

No generic dynamics, local Cauchy existence, physical content, source, action,
carrier, general GR equivalence, accepted grade or canon conclusion follows.
All four claims require direct separate-context review before downstream use.
