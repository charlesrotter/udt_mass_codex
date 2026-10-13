# Frozen candidate B — restrictions and an unadopted additive connection

Status: **CANDIDATE FOR REVIEW**. Exact arguments below were constructed and
self-checked in one context. No fresh review, physical adoption, or publication
has occurred. The synthetic premises are P1-P3 in NOTEBOOK.md.

## B1. The original composition inference fails

Give every observer the same map F(x)=x^3. It is continuous, F(0)=0, and
F(-x)=-F(x). Nevertheless,

    F(1+1)=8, whereas F(1)+F(1)=2.

More generally its additive defect is

    D(x,y) := F(x+y)-F(x)-F(y) = 3xy(x+y).

Thus even identical functional forms for all observers do not imply additivity.
This counterexample is a refutation of that implication, not a rejection of
every possible physical composition principle. A shared rule tells us which
map each observer uses; it does not specify how input and output compositions
are related.

The original proposal has two distinct links:

    shared F --unsupported--> H_ADD
    continuity + H_ADD --proved below--> F(x)=k*x.

The first link fails as a consequence of the admitted assumptions. The second
survives only with H_ADD stated explicitly. The proposal's physical-selection
interpretation therefore does not survive as an admitted conclusion.

## B2. Complete characterization under the toy premises

**Claim.** The maps admitted by P1-P3 are exactly the odd extensions of arbitrary
continuous functions g:[0,infinity)->R satisfying g(0)=0:

    F(x) = g(x)       for x >= 0,
           -g(-x)    for x < 0.

**Necessity.** For an admitted F, take g to be its restriction to the nonnegative
half-axis. Continuity and g(0)=0 follow from P1-P2, and P3 determines all negative
values by this formula.

**Sufficiency.** The displayed extension is continuous separately on the two
open half-axes. At zero, g(t)->0 as t decreases to zero; hence both one-sided
limits of F are zero, equal to F(0). The definition gives F(-x)=-F(x) for x>0
and x<0; at zero it follows from g(0)=0. Thus P1-P3 all hold.

This is a full characterization for this mathematical premise set, proved in
both directions. It is not a completeness claim about real UDT or possible
physical premises. It shows precisely that the nonnegative profile is free
subject to continuity and its value at zero; oddness then fixes the other half.

For example, all maps k*x (every real k), x^3, and sin(x) are admitted. Thus
neither a preferred slope, linearity, positivity on positive inputs, injectivity,
nor global monotonicity is selected. Differentiability at zero is not required:
the odd extension of g(t)=sqrt(t) is admitted and has difference quotient
1/sqrt(|x|) at nonzero x, which has no finite limit at zero. Even if one were to
supply a local derivative k separately, F(x)=k*x+a*x^3 would preserve it for
any real a and would be nonlinear for a!=0. These examples illustrate freedom;
the two-direction proof, rather than the examples, establishes the class.

## B3. Useful conditional survivor under H_ADD

**UNADOPTED H_ADD:** F(x+y)=F(x)+F(y) for every real x,y.
Its source and proposed physical interpretation are recorded before its use in
NOTEBOOK.md. No derivation of H_ADD from P1-P3 is claimed.

**Conditional theorem.** For a continuous F:R->R, H_ADD holds if and only if
there is a real k such that F(x)=k*x for every real x. Therefore P1-P3 plus
H_ADD select this mathematical family, without selecting k.

**Forward proof.** First, H_ADD at (0,0) gives F(0)=2F(0), hence F(0)=0.
At (x,-x) it gives F(-x)=-F(x). By finite repeated addition,
F(n*x)=n*F(x) for positive integers n; the zero and negative cases follow from
the preceding identities. Set k=F(1). For integers m and positive integers n,

    n*F(m/n)=F(m)=m*k,
    so F(m/n)=(m/n)*k.

For any real x, choose rationals q_j tending to x (density of the rationals).
Continuity at x gives

    F(x)=lim_j F(q_j)=lim_j k*q_j=k*x.

This establishes the result for every real x, not merely sampled values.

**Converse.** For any fixed real k, the map k*x is continuous and satisfies
k*(x+y)=k*x+k*y, F(0)=0 and oddness. Hence no real k is excluded, including k=0
and negative k. Positivity, invertibility, normalization, or observational
calibration would require additional conditions. No such conditions are admitted.

The physical join remains open: which prepared comparison intervals compose,
why their inputs compose by ordinary addition, and why their outputs should
also compose by ordinary addition. The elementary theorem cannot answer those
questions. B1 shows the needed join is not implied by shared form plus P1-P3.

## B4. Finite point checks cannot establish global H_ADD

**Claim.** Fix any real k, any finite list of exact additivity tests at pairs
(a_i,b_i), and any finite list of pointwise values c_j taken from the line k*x.
There is a continuous odd nonlinear F that matches that line at every c_j and
passes every listed additivity test. It can also have F'(0)=k.

**Construction and proof.** Let T be the finite set of distinct strictly positive
absolute values among all a_i, b_i, a_i+b_i and c_j. Use the convention that an
empty product is 1. For any nonzero real epsilon define

    h(x) = x^3 * product over t in T of (x^2-t^2),
    F_epsilon(x) = k*x + epsilon*h(x).

The polynomial h is odd and vanishes at zero and at every positive or negative
argument represented in T. Thus F_epsilon equals k*x at every point used in
the stipulated tests and calibrations, so every such additive check returns
zero defect. Also h'(0)=0, hence F_epsilon'(0)=k.

The degree of h is 3+2*|T|, with leading coefficient 1. Since epsilon!=0,
F_epsilon has degree at least 3 and is nonlinear. It is continuous and odd, so
it satisfies P1-P3, but B3 implies it cannot satisfy H_ADD globally.

Quantifiers matter: the construction depends on the finite set. It does not
claim that one nonlinear F passes all possible tests, or that measurements are
point evaluations, or that approximate observations refute exact additivity.
A nonzero exact additive defect can disprove H_ADD, but finitely many zero
defects cannot prove its universal statement within this admitted class.

## Review scope and next decision

The closest inspected predecessor is the supplied NOTEBOOK.md; external search
and real scientific-source inspection were excluded. The arithmetic identity,
half-axis extension, rational-to-real passage, converse, and finite-test
construction have been self-checked, including zero and negative arguments,
k=0, negative k, empty T and repeated tested arguments. No numerical evidence,
independent implementation, different-model check, or separate reviewer exists.

The result reduces the stated uncertainty in two ways: it characterizes the
admitted freedom and isolates the exact extra connection that would impose
linearity. It also supplies a precise limit on pointwise verification. It does
not select a physical law. Return now for the dispatch's candidate-review
checkpoint; more examples cannot close the missing physical join.

A future reviewer should try to break the quantified extension proof, the use
of continuity in B3, and the finite-test construction in B4, then confirm that
the compressed conclusion retains H_ADD. A physical continuation would need a
source-based justification or a concrete discriminating preparation for the
composition connection. No such continuation or adoption is started here.
