# CRV1 source-first adversarial reconstruction

2026-09-28. Reviewer `/root/crv1_review`, fresh separate context. Runtime describes
Codex/GPT-6 family; exact backend/model identity is not exposed. Different-model,
different-library, human-specialist and formal-proof review are not established.

Top-level startup/synchronization is attributed to parent and LAUNCH.json. The
reviewer independently checked branch `grok`, HEAD
`43775d36836a88deca5303be870a67f6e259cff9`, tracked-clean status, and visible
untracked pathnames before working. Protected payloads were not opened. This
reviewer writes only `review/`. On-disk AGENTS, specified CLAUDE sections,
verifier-before-record, no-shortcuts, completeness-map and CROSS_MODEL_VERIFY
were read. The four dispatched scientific sources and work order were read;
source hashes are in SOURCE_FIRST_PINS.json. Instructions supply method, not
scientific premises. Parent's current premise audit was pending at review launch;
its eventual result must be separately reported, not inferred from this review.

No producer candidate, proof, code or output has been opened at this stage.
Exposure includes the parent task/question, the prior packages' reviewed-result
verdicts, and a later parent message that a local completion criterion/witness
was drafted. The actual reconstruction below preceded candidate exposure. The
parent supplied the Anderson–Pohjanpelto reference during this stage; it was not
independently discovered by this reviewer. Its primary arXiv theorem text was
then independently inspected. This is not a wholly blind literature search.

## Source ownership

G312 current authority owns GR FILTER ONLY and owner-provisional DDR and Local
Metric Sufficiency. Locality does not determine tensor type, weight, jet order,
or a complete architecture. On the specified regular all-pair domain DDR gives
TF(E)=0; it supplies no formula for E. GRS1/RMS1 retain all naturality, finite-jet,
flat regularity/flattening-ray, exact homothety and nonzero-shape conditions of
their conditional route. The interpretation of c_E remains unchanged. Neither
those sources nor the present weak comparison examples identify native response.

## Independently reconstructed implications

For a fixed smooth Lorentz4 metric, use its Levi-Civita connection and write
E=S+f g with tracefree symmetric S. Put j_b=∇^a S_ab. Metric compatibility gives

    div E = j + df.

Hence on a contractible local region there exists a smooth scalar completion f
with div E=0 exactly when dj=0. Necessity is d²f=0 and sufficiency is the local
Poincare lemma; f is unique up to a constant on a connected region. If using the
full trace τ=tr(E), the equation is dτ=-4j. On a general global domain, exactness
of j, not merely closedness, is required. This theorem concerns a fixed metric.
It does not construct a uniform natural finite-jet scalar f[g]; integrating a
closed one-form can produce a nonlocal primitive. A candidate must preserve
this distinction before using a natural-operator inverse theorem.

For the full conditional RMS1 response S=a(Ric-Rg/4), constant a,

    j=(a/4)dR,  f=-aR/4+C,  E=a(Ric-Rg/2)+Cg.

This gives an explicit local-natural completion with universal parameter C.
For each individual fixed metric, the primitive's integration constant could
instead be chosen by global/history data; that choice would need separate
scrutiny against Local Metric Sufficiency. The identity does not demand a new
native action or establish any of RMS1's physical identification hypotheses.

On an actual DDR solution S=0, div S=0 holds simply because the tensor field
vanishes throughout the solution region. It is not an off-shell identity for
the operator S[g]. Nor does it force div E=0, since E=f g there. E=Rg is a local
natural pure-trace comparison whose DDR condition holds identically but whose
divergence is dR. E=Ric has nontrivial shape sensitivity and off-shell divergence
(1/2)dR, even though its DDR solutions force constant R by Bianchi. These are
structural illustrations, not UDT-admitted alternatives or GR-filter passes.

## Exact obstruction independently computed from metric data

Metric/sign/chart/profile are free-and-explored UNADOPTED comparison choices.
Take coordinates (t,x,y,z), t>0,y>0 and

    g = diag(-1,t^4,1,y^4).

Let A=4/t² and B=-4/y² be the two product-factor scalar curvatures. The original
reviewer script computes the Christoffels, Ricci and full covariant divergences
directly from the metric, without producer imports. It obtains R=A+B and
Q=Ric_ab Ric^ab=(A²+B²)/2. For S=Q(Ric-Rg/4), independent product algebra gives

    j_t=(3A²-2AB+B²) A'/8,
    j_y=(A²-2AB+3B²) B'/8,
    (dj)_ty=(A-B) A' B'/2.

Direct metric computation agrees. At t=1,y=2,

    j=(-57,0,27/8,0),   (dj)_ty=-20.

Thus this S has no divergence-free scalar-trace completion on any neighborhood
of that point. This is stronger than failure of a guessed f; every smooth f is
excluded there. The trial is a symmetric natural smooth second-order local
metric tensor, but its homothety weight is -4, outside RMS1's weight-zero class.
No claim is made that the trial law is UDT-admitted, realizes DDR on this witness,
or survives a GR comparison. It refutes only the broad structural implication
from natural local metric dependence to automatic trace completion.

`source_first_exact.py` passed 21 explicit exact assertions, including nonzero
controls for missing Q-gradient, reversed curl orientation, and wrong-sign
linear completion. The run used Python 3.10.12/SymPy 1.13.1, one CPU process,
49,160 KiB peak RSS, 0.456 seconds, under 60 seconds/512 MiB; stdout/stderr and
machine result are preserved. No floating-point tolerance, grid, fitting, GPU,
or physical parameter choice is used. Counts are not coverage guarantees.

## Variational discriminator and qualified converse

For a local pure-metric diffeomorphism-invariant action, compactly supported
metric variations generated by a vector field imply the off-shell divergence
identity for its full Euler response. The proof must vary the full metric,
account for density and index convention, and integrate by parts. Constrained
tracefree variations instead determine only the projected response. A proposed
E's density-valued linearization must satisfy the Helmholtz/formal-self-adjoint
conditions to be a local Euler expression; covariance alone is not that test.

An overly strong statement that conservation never yields an action would be
wrong. Anderson–Pohjanpelto, Theorem 1, treats natural symmetric metric tensor
densities of differential order at most three, fixed arbitrary signature, and
an off-shell divergence identity. It gives local variationality; the everywhere
smooth four-dimensional case admits a natural scalar-density Lagrangian. Apply
it only after converting the response to the correct density/index type and
checking the operator domain, smoothness, order and identities. It supplies no
native conservation premise. Reference supplied by parent, theorem independently
read: https://arxiv.org/html/1202.5811v1 . Its full proof was not independently
reconstructed here; no arbitrary-order converse is claimed.

The explicit aG+Cg completion has the familiar EH plus volume comparison action,
with coefficient/sign determined by the chosen metric-variation convention.
Existence of that comparison action is distinct from unique functional selection,
physical normalization and native UDT identification. Total divergences and
variationally trivial terms also prevent naive action uniqueness.

## Provisional disposition and omissions

The local trace-completion criterion and the conditional aG+Cg completion are
sound within the hypotheses just stated. Automatic off-shell conservation from
DDR/locality is not established. No counterexample to native UDT or to the
full RMS1 conditional route has been supplied. No new physical premise is
shown necessary. This is a source-first reconstruction, not a direct verdict
on the unopened producer candidate.

Not replayed: prior GRS1/RMS1 full packages, all-pair DDR proof, full registry
audit, global cohomology, classification of all natural primitives/actions,
Anderson–Pohjanpelto's complete proof, empirical GR-filter testing, sourced
physics, nonlinear stability, human or formal verification. Common SymPy is
not library independence. Independent original metric choice and covariant
implementation provide a separate computational route within those limits.
