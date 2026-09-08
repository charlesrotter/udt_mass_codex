# VS1 source-first reconstruction, sealed before candidate exposure

Reviewer: `/root/vs1_adversarial_review`, separate fresh context, 2026-09-08.
Exact exposed model identifier: UNKNOWN. Different-model, human-specialist and
formal-proof review: UNTESTED. Parent dispatch and work order disclosed the
question, expected classes of outcomes, source pointers, and resource limits;
no candidate proof, code, result, or verdict has been read at this seal.

Baseline personally inspected: grok HEAD
4ffd6a4d2a30d7d6c8e0fdb79dae548769c2d717. Protected and unrelated untracked
work is present and untouched. Parent performed synchronization; this reviewer
does not mutate shared Git. Parent's bounded full356 audit is in progress and
will be reused only after its receipt is inspected. No numerical child has run.

## Controlling source definitions and limits

G312, with the subsequent owner adoption, gives the bounded vacuum equation
S=Ric-(R/4)g=0. G313 applies contracted Bianchi on a smooth connected regular
four-dimensional Lorentzian region to give Ric=Lambda g, with Lambda constant
but unselected. This is conditional mathematics under OWNER_ADOPTED_PROVISIONAL
premises; the optional nonvacuum source model is excluded.

G131's shared-open-domain reduced control is invariant under a positive
conformal factor. G176/G180 are a different completed-pair type: at identical
auxiliary embeddings m_hat=Omega^2 m and Phi_hat=Phi-log(Omega). Neither a
physical query population nor a physical scale is selected. Same event/query
identification is supplied, and no all-isometry classification is sought.

## Independently reconstructed mathematical requirements

Write sigma=Omega^-1>0 and use Ric=(Lambda)g, k=Lambda/3. With the conventional
coordinate Ricci sign giving positive Ricci for the round sphere, connection
change must reproduce

  Ric_hat = Ric + 2 sigma^-1 Hess(sigma)
             + [sigma^-1 Box(sigma)-3 sigma^-2 |d sigma|_g^2] g.

The exact nonlinear condition is therefore Hess(sigma)=psi g, where
psi=Box(sigma)/4. No small-factor expansion or sign assumption on the gradient
is used. Conversely this condition with sigma>0 gives S_hat=0 directly.

Divergence gives d psi=-k d sigma: divergence(Hess sigma) equals
d Box(sigma)+Ric(grad sigma, .), while divergence(psi g)=d psi.
Thus a=psi+k sigma is constant. All solutions correspond to parallel triples
(sigma,p,psi) of a rank-six linear connection through

  d sigma=p,
  nabla p=psi g,
  d psi=-k p.

Equivalently use (sigma,p,a) with da=0 and nabla p=(a-k sigma)g.
ODE uniqueness along every piecewise smooth path proves that evaluation at an
interior event is injective. Consequently the vector space of scalar solutions
has dimension at most SIX, and the positive solutions near that event are the
positive-value part of that space. This is finite determination, not arbitrary
six-component admissibility. Constants supply one solution dimension.

Curvature compatibility necessarily annihilates p through the Weyl tensor.
The precise index sign should be verified against the adopted Ricci convention;
the invariant statement is W(...,grad sigma)=0. This condition at one event is
not a sufficient local realization theorem. Even all smooth curvature jets at
one event are not an automatic replacement for neighborhood compatibility.

An exact smooth realization criterion can be stated by parallel transport:
the initial triple must be fixed by transport around every based loop in the
chosen neighborhood. Necessity is immediate. For sufficiency transport it to
each point along any path; loop invariance makes this independent of the path,
and smooth dependence on radial coordinate paths gives a smooth parallel
section. Alternatively radial transport on a star-shaped chart must satisfy
the full parallel equations throughout that chart. Neither criterion claims
that finitely many algebraic curvature conditions characterize admissibility.

If v -> W(...,v) is injective at one event, injectivity persists locally by
nonzero minors; p=0 throughout a small neighborhood, hence sigma is constant
there. ODE uniqueness then extends that same constant solution on the connected
solution domain. This condition is sufficient, not a genericity claim or a
necessary criterion for rigidity. Lorentzian null kernels cannot be discarded.

The resulting constant target scalar must be

  Lambda_hat = Lambda sigma^2 + 6 sigma psi - 3 |p|_g^2
             = 6 a sigma - Lambda sigma^2 - 3 |p|_g^2.

Its differential vanishes under the prolonged equations, with no division by
Lambda, |p|^2, or p. A separately prescribed Lambda_hat imposes this quadratic
constraint on admissible seed data. For constant sigma=b>0, Lambda_hat=b^2
Lambda. Free and fixed target scalar comparisons must remain separate.

## Actual local controls and adversarial risks

On flat Minkowski g=eta every solution is locally

  sigma=(a/2) eta_ab x^a x^b + b_a x^a + c,
  Lambda_hat=6ac-3 eta^ab b_a b_b,

on an open positive region. This follows by integrating the full prolonged
system, so gives actual local solutions and attains the six-dimensional bound.
It includes nonconstant null-affine Ricci-flat rescalings; zero norm must never
be mistaken for zero covector. It also shows one scale value cannot determine
the full local profile. These are geometric controls, not physical adoption.

Adversarial targets: trace-free versus full Ricci confusion; wrong sign in
d psi; lost quadratic gradient term; target scalar accidentally fixed;
pointwise Weyl compatibility promoted to sufficient existence; six-dimensional
upper bound promoted to six freely admissible values for arbitrary g; null
gradient discarded; completed depth conflated with reduced controls; global
conclusions drawn from positive local patches; and same-formula tests called
independent proof.

## Frozen review checks and resources

After initial candidate freeze, inspect the proof and all claimed checks,
independently compute original coordinate Ricci from metric derivatives for
several explicit positive flat-conformal metrics, and include deliberately
wrong profiles/formulas whose residuals must be nonzero. Use standard-library
exact rational arithmetic with direct Christoffel differentiation, avoiding
the conformal-Ricci formula as the check's implementation. Compare scalar,
tensor, positivity and null cases. Finite exact checks remain examples and
implementation checks, not the proof of universal quantifiers.

Fully inspect the existing run_capture.py helper before use; one CPU child,
512MiB address space, 60s CPU/wall, BLAS/OMP/MKL threads1. No child until the
full356 premise receipt is available. At most one grouped same-premise repair
and focused re-review; preserve failures and initial sources. Stop within the
dispatch's60-minute reviewer budget or at a load-bearing unresolved objection.

## Source version seal

SHA256:

- G131 EXACT_DERIVATION: 6fe4ed7fd5e2bb7d4370f810e09dda20d3588056d35032edd9e2b9cad01bebba
- G176 EXACT_DERIVATION: df53a5b3c52d0bd24496d060637dc158a4f2c7cdd17226c9446ea0d338d27831
- G180 EXACT_DERIVATION: 3e81642bacf30a9e94df3db4c041f6b6ae94af91b87d9f51c044116ed2afa7b6
- G312 EXACT_DERIVATION: 90ae2841153754087e64ba14d0a61c408d0b5767b5c8ed9f558da0b49ab30ea4
- G313 AUDIT_REPORT: b7df75cee891ed23dcf4796aba0a3d25e101ee89e4c1add95c8ef842987e418e
- G310 ADOPTION_RECORD: 4eb7d0a1130dcff997bc5180f420b633e2dcbbb5072d098997ba3672b38d8ab5
- G312 ADOPTION_RECORD: ebeae075307e7a325a840f4c2d9dcd973c18d9a3be21e6e6eccacce1ae8856f1
- WORK_ORDER: cf28eb68d885ae5a0ca08c36d39c0b1c1718c346bbb8a7a985df71a90c671023
- QUESTION: 3c8ab4279239d5e9da6794481e09028d54d45313784f3f95561c1658972de263
- AGENTS: 322d867b49fdd6254e4f671ce8b100c56d6b4709035e37dec22259ecdb7af07c
- CROSS_MODEL_VERIFY: 2b0509d933d731fbf3f72aa88777a54d3e48a94d4bae3d324087871777f9a007

Read startup/current/CLAUDE and applicable five skill protocols from disk;
historical source packages were not replayed. Exact model identity remains
UNKNOWN despite runtime branding. This file is an independent source-first
argument, not an accepted result and not a candidate verdict.
