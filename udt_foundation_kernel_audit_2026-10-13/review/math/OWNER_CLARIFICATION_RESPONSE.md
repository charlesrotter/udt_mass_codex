# FKA1 mathematical review — response to direct owner clarification

Reviewer `/root/fka_review_math`, same fresh review context as SOURCE_FIRST.
2026-10-14 UTC / 2026-10-13 local. This supplement precedes candidate, prior-proof
and sibling-review exposure. Read only shared OWNER_CLARIFICATION and corrected
WORK_ORDER beyond the previously disclosed sources. Original SOURCE_FIRST and
its pins are preserved; this supplement controls its interpretation where the
new owner statement corrects the prior framing. HEAD remains 67246b35.

## Accepted starting meaning and corrected review question

Charles directly states: “It is a UDT postulate that what we observe as c_E is in
fact a mutual slowing of separated clocks which we currently interpret as a
light travel time.” That intended physical identification is taken as a postulate
in FKA1. It is not a conclusion that must first pass an independently supplied
photon transport law. The question is which mathematical expressions and metric
consequences actually follow, retaining the original and later stated meanings.

In SOURCE_FIRST, the clock correspondence definition was propagation-neutral,
but the subsequent null-wavevector formula could be read as its compulsory
completion. It is not compulsory. All its static null-clock and expanding-metric
examples are conditional geometric representations only. They cannot define or
refute the postulate by importing a separate propagation mechanism. In particular,
the static inverse-lapse obstruction applies only after that static geometric
representation and its clock preparations have been supplied. It is not a first
objection to Charles's clarified premise.

The accepted meaning is stronger than an agnostic label saying that the source
has not chosen between clock slowing and propagation. The owner has chosen the
interpretation. The audit may still ask whether a proposed equation represents
it faithfully, what restrictions an equation adds, and what remains undetermined.
Neither the owner postulate nor a reviewer's acceptance of its status proves a
specific formula for the two-oriented-clock data or a unique metric.

## Minimal exact clock correspondence, without a propagation mechanism

Take two labelled ordinary proper-clock records, each with its own ordered
proper-time domain, `I_A` and `I_B`. These may be attached to worldlines when a
geometry is supplied; the operational record construction itself requires no
null-curve, particle, wavevector, wave equation or separate propagation speed.
Register which A-clock records appear in B's observation records. On a regular
branch represent this oriented event correspondence by

    F_AB : I_A -> I_B,    tau_B = F_AB(tau_A),    F_AB' > 0.

If a derivative exists, the rate at which A-clock ticks appear per unit B proper
time is `q_AB = d tau_A/d tau_B = 1/F_AB'`. Interchange emitter/observer roles to
form a second oriented correspondence

    F_BA : J_B -> J_A,    q_BA = 1/F_BA' > 0.

Domains, matching events and preparation are data. Mutual slowing has the local
mathematical expression `q_AB<1` and `q_BA<1` for the experiments/events intended
by the postulate; exact equality between the factors is an additional symmetric
preparation/meaning unless the postulate's intended interchange symmetry is
explicitly applied there. Discrete tick records can be used before differentiable
interpolation; differentiability is a regular-model restriction, not a new
physical propagation premise. These rate factors are dimensionless once clock
calibrations are stated.

It is not necessary that `J_B` be the same set of observation events as the range
of the first map. Even if composition is defined at matching intermediate
records, the second map is not required to equal the mathematical inverse of the
first. `F_AB^{-1}` recovers the original pairing; it is not automatically a new
opposite observation experiment. No contradiction follows from both derivatives
being greater than one.

A simple consistency witness is `I_A=I_B=J_A=J_B=[0,infinity)`, ordinary clocks
labelled by tau, and

    F_AB(tau) = alpha tau + beta,
    F_BA(sigma) = alpha sigma + gamma,
    alpha > 1, beta > 0, gamma > 0.

Both apparent tick rates equal `1/alpha<1`. Their composed event correspondence
is `alpha^2 tau + alpha beta + gamma`, which is strictly later in the original
clock's ordering than tau on this domain. Thus mutual slowing need not create
an event-order cycle in this record model. This is an exact propagation-free
consistency witness only: alpha, offsets, clock preparations and their connection
to separation are free-and-explored, not a derived UDT geometry or a global
causality proof. Its purpose is to defeat a premature algebraic contradiction,
not to fill missing physical choices with fitted functions.

The dimensions of `q` differ from those of `c_E` or `1/c_E`. Accepting that the
observed c_E phenomenon *is* the clock effect does not require an independent
physical explanation. Giving that postulate a predictive numerical expression
does require specifying which positional/ruler protocol, clock correspondence
and dimensional calibration report the observed c_E value. This is a question
about the mathematical representation and measurement definition of the accepted
postulate, not a demand to derive its reason from external propagation physics.

As a formalization diagnostic, a correspondence `F(tau)=tau+T` has unit tick
rate regardless of its positive offset T. An offset alone therefore does not
mathematically encode the derivative slowdown above. This does not refute the
postulated interpretation of light travel time; it identifies why replacing
that interpretation by a constant-delay map without further structure would be
an inadequate representation of mutually slowed received ticking.

## Composition and difference-dependence under the clarification

The June recorded quotation about differences and consistent composition must
still be tested, not discarded. In the clock-record construction, composition
of correspondences at matching events is well defined and the chain rule gives

    (F_BC o F_AB)'(tau_A)
       = F_BC'(F_AB(tau_A)) F_AB'(tau_A).

The corresponding tick factors multiply only with these matching evaluations.
This is automatic mathematical consistency of composed records. Identifying the
composition with an independently observed direct A-to-C record map requires
an additional physical/path-independence statement. Neither operation itself
supplies an additive scalar depth.

If a supplied positive scalar factor depends continuously on a signed additive
depth and obeys multiplicative composition on that signed domain, the exponential
functional-equation conclusion survives. But it is premature to identify both
oriented observations with positive and negative differences of the same static
endpoint scalar. That choice would impose inversion before assessing whether it
represents the mutual-slowing postulate.

A favorable alternative remains an accumulated nonnegative depth on ordered
compositions, with reciprocal algebra used to parameterize one map rather than
to reinterpret its opposite observation as its inverse. Another is a family of
two oriented event correspondences on shared geometry, with depth defined from
the actual records. The audit may construct and compare these representations
inside the authorized scope. Their faithful interpretation, domains, relation
to the quoted difference-dependence and metric consistency remain real questions;
their novelty is not a reason to reject them before investigation.

## What mutual clock slowing does and does not force about reciprocal pairs

There is an exact reciprocal normalization available for **any** positive pair
`(q_AB,q_BA)`. Write

    m = sqrt(q_AB q_BA),
    R = sqrt(q_AB/q_BA),
    (q_AB,q_BA) = m (R,R^(-1)).

The normalized pair has product one and

    (q_AB-q_BA)/(q_AB+q_BA)
       = (R-R^(-1))/(R+R^(-1))
       = tanh(log R).

This is an algebraic decomposition, not an implication that the actual clock
factors themselves have product one. For exact symmetric mutual slowing,
`q_AB=q_BA=q<1`, one has `m=q`, `R=1`, and this normalized contrast is zero. The
common slowing lives in m, which the contrast discards. Consequently a nonzero
kernel intended to describe symmetric mutual slowing cannot simply be justified
as the normalized difference of these two actual oriented tick factors. It must
use a different declared pair or readout. This is a warning about that particular
identification, not an objection to the existence or interpretation of the
postulated effect.

An alternative reciprocal embedding uses a single common slowdown factor q:
for example `(a,b)=(q^(-1/2),q^(1/2))` gives a reciprocal pair and
`(a-b)/(a+b)=(1-q)/(1+q)=tanh(-log(q)/2)`. Choosing instead `(q^(-1),q)` changes
the depth normalization and readout. Both are mathematically possible. Thus the
existence of a reciprocal encoding is straightforward; why a particular encoding
matches the metric coefficients, coframe components or physical readout is the
legitimate inference question. A square root can become compulsory once one has
specified the relation between a quadratic metric coefficient and a linear clock
or ruler factor, but that object assignment must be stated.

Likewise one can encode a chosen q by reciprocal temporal/radial coframe factors
and recover a diagonal reciprocal metric block. Such a construction may be a
useful candidate, and a later explicitly adopted time-length reciprocity premise
may license it conditionally. The mutual-clock interpretation by itself does
not identify the radial ruler law, determinant normalization, chart, areal-radius
restriction, angular sector, or positional profile. The recorded statement that
mutual symmetry *forces* a metric structural identity is therefore still a
mathematical claim to prove using a precise symmetry action and domain. It is
not disproved merely because one overly restrictive signed-clock interpretation
would fail.

## Updated candidate-review tests and legitimate stopping point

The candidate should begin with the accepted c_E interpretation, then explicitly
state its mathematical clock data and map them to any metric representation.
I will challenge either an unsupported positive implication **or** a premature
negative conclusion built from extra propagation/static/inverse-map assumptions.
Specific questions are:

- Are the two oriented records correctly distinguished from an inverse map?
- Which composition is given: matched record composition, path-independent
  direct comparison, signed scalar cocycle, or nonnegative accumulated depth?
- What joins clock factors to positional/ruler calibration and the metric?
- Which pair is reciprocal, by postulate, consequence or normalization? If
  normalization removes a common factor, is physical mutual slowing lost?
- Is the tanh formula an exact consequence for the declared pair/readout, and
  does that readout have the intended operational meaning?
- Do coordinate, sign and depth normalizations change only a representation or
  change the proposed physical observation?
- Are negative examples limited to their added hypotheses and positive examples
  limited to the structures they actually construct?

A return can legitimately report a precise conditional metric/pair/readout
chain and its remaining mathematical connection. It cannot report that the
postulated meaning of c_E is unestablished simply because independent propagation
physics was not derived, nor can it claim the postulate selects a unique full
geometry without a sufficiency argument. In-scope constructive alternatives
should be tested far enough to locate the actual join. No candidate verdict,
adoption, registry regrade, CANON edit or numerical workload occurs in this
supplement.
