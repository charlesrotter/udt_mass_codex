# GRS1 source-first adversarial assessment

Sealed source-first stage: 2026-09-28, before exposure to GRS1 candidate proof,
implementation, outputs or verdict. This is a conditional mathematical review;
it adopts no action, response architecture, physical premise or scientific grade.

## Identity, startup and exposure

Reviewer: `/root/grs1_review`, a separate Codex context. The developer identifies
the runtime as based on GPT-6 but exposes no exact serving-model identifier.
Treat this as fresh-context, same-model-or-unknown review, never a proved
different-model review. Independent argument: yes, reconstructed below after
reading the historical source arguments. Independent computation: not yet done
at this seal; the proposed exact metric check is stated below before coding.
Human and formal-proof review: unavailable.

Parent startup is attributed, not rerun: parent reports mandatory top-level
startup and synchronization at `45330a7bf4821a87ec70445ee47e1079c42a411f`.
Reviewer independently ran `git status --short --branch` and `git rev-parse
HEAD`: branch `grok...origin/grok`, that HEAD, no tracked modifications, unrelated
untracked paths plus this work package. Reviewer did not independently fetch.
Parent reports the full current premise audit running; no pass is claimed here.

Read: AGENTS.md; CROSS_MODEL_VERIFY.md; CLAUDE.md How we work, DRIVER TRIGGERS,
Repo discipline and orientation; triggered no-shortcuts/completeness-map skills;
GRS1 WORK_ORDER.md and LAUNCH.json; current GR authority record; G301 derivation
and audit report; G310 and G312 derivations. Queried only current registry status
and controlling-source fields for G301, G310, G312. Also consulted the primary
mathematical reference Navarro/Sancho, *On the naturalness of Einstein's
equation*, arXiv:0709.1928v2, via https://arxiv.org/pdf/0709.1928.
No protected payload, historical transcript, wide registry dump, GRS1 candidate
proof, producer code, producer result, or prior GRS1 verdict was read.

Before this seal the reviewer sent the parent the prospective R=0 witness and
the weight-zero classification distinction. Parent supplied no candidate proof
in return. Thus source-first means independence from the new candidate, not
independence from the published repository arguments or the named mathematics.

## Current ownership and orientation

The actual current authority record supersedes historical G312 adoption prose:
DDR and Local Metric Sufficiency are OWNER_ADOPTED_PROVISIONAL, not derived or
canon. GR is FILTER ONLY. Full GR principal-response overlap is not adopted.
G301's classification is verified mathematics within its frozen class, not
ownership of that class by UDT. The principal open gate is identifying the
physical response E as a nondegenerate member of that class. The bounded next
action is to test candidate identification arguments and their hypotheses,
without supplying that identification as a premise in disguise.

## A. What the reciprocal variation actually selects

At a regular Lorentz tangent space the reciprocal tangents are trace-free and
span all nine trace-free symmetric directions (the source's all-pair domain is
essential). The metric pairing is nondegenerate on that subspace. Thus

    <E,H(u,n)> = 0 for every orthonormal reciprocal pair
    iff TF(E)=0 iff E=lambda(x) g.

This is a condition on a supplied response E. It neither constructs E nor proves
that E is an Euler derivative of an action. Variational integrability would
itself require further conditions. Even after an action is supplied, restricting
its compactly supported metric variations to trace-free directions projects its
Euler derivative; it does not identify the functional.

For a covariant metric variation h=delta g, delta sqrt(|g|) is one-half the
volume density times tr_g(h). Hence trace-free h is infinitesimally
volume-preserving. It does not follow that arbitrary physically allowed metric
variations must be restricted in this way. Mathematically the restriction is a
well-defined comparison; physically identifying it with an action principle is
an additional interpretation of DDR, not a derivation of DDR or an action.

For any differentiable functional A, constant rescaling of A leaves its
stationarity condition unchanged. A volume functional has pure-trace first
variation and is invisible under this restricted variation. Boundary terms
with vanishing compactly supported variation are also invisible. These are
additional reasons why the restricted first variation cannot identify a unique
functional, even if a particular response equation has already been identified.
No volume-term coefficient or boundary law is adopted here.

## B. Independent comparison separating EH and R-squared

Use four-dimensional smooth Lorentz metrics and compactly supported variations.
Both comparison functionals below are explicitly UNADOPTED. With inverse-metric
variation, the scalar-curvature variation identity and two integrations by
parts give

    A1 = integral sqrt(|g|) R,
    E1_ab = Ric_ab - (R/2)g_ab;

    A2 = integral sqrt(|g|) R^2,
    E2_ab = 2R Ric_ab - (R^2/2)g_ab
            + 2(g_ab Box R - nabla_a nabla_b R).

The overall sign changes if E is defined by covariant-metric variation; the
zero set and trace-free stationarity do not. Their trace-free derivatives are

    TF(E1) = S := Ric-(R/4)g,
    TF(E2) = 2R S - 2 TF(Hess R).

An exact prospective witness, chosen independently before new producer-code
exposure, is

    g = -dt^2 + t(dx^2+dy^2+dz^2), t>0.

Writing a=sqrt(t), H=a'/a=1/(2t), the ordinary curvature identities predict

    R=6(H'+2H^2)=0,
    Ric_tt=3/(4t^2), Ric_ij=delta_ij/(4t).

Thus S=Ric is nonzero but E2=0. Direct coordinate recomputation from this metric,
not these identities, is proposed for the next review stage. This witness
separates the two trace-free stationarity equations; it does not prove A2 is an
admissible UDT response. No matter or source interpretation of this metric is
being used. R-squared also vanishes variationally on four-dimensional Einstein
metrics of constant scalar curvature, so overlap with that supplied solution
family alone cannot identify the EH functional.

Relevant failures of the R-squared comparison are explicit: its generic Euler
derivative is fourth order, has zero linearized response around flat space,
and as a covariant two-tensor has homothety weight -2. It fails the G301 response
weight/order and nondegenerate GR principal gates. It is local, metric-only,
natural and smooth at flat. In four dimensions the pure R-squared integral
needs no standalone length coefficient. Adding it to EH at a fixed common
normalization would require a relative coefficient with length-squared units.
Consequently absence of a dimensional coefficient is not by itself a proof of
the EH response weight. No claim that this comparison passes the unspecified
current GR filter is warranted.

## C. An alternative conditional classification route

The natural-tensor reference defines naturality using locality, smooth
dependence on metric families and local-diffeomorphism equivariance. Its
Theorem 4.1 classifies homogeneous tensors through orthogonal-equivariant maps
of normal tensors; Corollary 4.8 gives curvature-linearity for covariant rank
two and weight zero. This is a mathematical method, not a UDT premise.

Here is a direct finite-jet version sufficient for this task. Suppose E is a
natural symmetric covariant two-tensor on a smooth finite-jet domain including
flat jets, smooth at flat, with exact constant-homothety behavior

    E[c^2 g]=E[g], c>0.                         (weight zero)

Choose normal coordinates about the event and let f_t(x)=tx. The metric
g_t=t^(-2) f_t^*g has components g(tx); its normal jets of orders k>=2 scale
as t^k, while its value at the event is fixed. Naturality plus the displayed
weight gives

    F(t^2 z2, t^3 z3, ..., t^m zm)=t^2 F(z2,...,zm).

In particular F(0)=0. Differentiability at the flat jet and division by t^2,
followed by t approaching zero from above, imply

    F(z2,...,zm)=D_2 F(0)[z2].

The remainder is o(t^2) because the jet displacement is O(t^2). This argument
requires the domain to include the relevant dilation path to flat; it does not
apply to a formula defined only on curved/singular strata. All higher normal
jets disappear and the response is linear in the second normal jet, hence in
curvature. Unoriented Lorentz equivariance leaves Ric and Rg as the two
symmetric rank-two contractions, yielding E=a Ric+b Rg. Thus second metric
order can be a conclusion within this stronger regular homogeneous class;
it need not be separately stipulated there. Without the weight or smooth-flat
domain, Local Metric Sufficiency does not give this conclusion.

Now DDR gives a S=0. A separate a!=0 condition is necessary: a pure-trace
response bRg passes DDR identically and selects no metric shape. With a!=0,
contracted Bianchi implies R is constant on each connected solution region
and Ric=(R/4)g. This fixes neither the constant nor an action representative.
Off-shell divergence freedom would impose b=-a/2, but DDR on-shell does not
imply off-shell divergence freedom.

## D. Expected adversarial gates for the candidate

1. Do not equate coordinate covariance, a change of units, metric homothety,
   action scale invariance and covariant response weight. State which one is
   assumed and why its physical identification is owned or conditional.
2. Do not infer weight zero just from no new scale. Pure R-squared has no
   relative length coefficient and supplies a different weight.
3. Do not derive an action from a restriction on its possible variations.
4. Do not turn Local Metric Sufficiency into a choice of tensor type, jet
   order, smooth-flat behavior, homothety weight or principal nondegeneracy.
5. A GR solution-overlap check is weaker than a complete response/principal
   comparison; the actual current filter is not specified sufficiently here
   to certify candidate survival.
6. Do not count the constant scalar datum, a!=0, or compact-support treatment
   of boundary terms as a derived physical scale, global completion, or
   selected boundary law.

This stage finds a sound conditional mathematical route and an unclosed
physical identification. It does not prove that a new premise is necessary
for every future UDT route. The absence of a present argument is not a theorem
of non-derivability.

## Version pins and checks not yet done

Reviewer independently SHA-256 hashed these sources and compared against
LAUNCH.json; every displayed digest matched:

| Source | SHA-256 |
|---|---|
| AGENTS.md | c578b045cf3278804124e23a5408ff9634a9a2165f7d20223f654d76bffd8ec9 |
| CLAUDE.md | b7e524a5b06760e57877a408630228767ae9a394134095f9851bef5d06e17751 |
| CROSS_MODEL_VERIFY.md | 2b0509d933d731fbf3f72aa88777a54d3e48a94d4bae3d324087871777f9a007 |
| G301 EXACT_DERIVATION.md | 633b907b5384aa63d61d49db067dd4e608e6abd3bf3571e4267f91e5c74da8fb |
| G301 AUDIT_REPORT.md | f2197ee7a23a88017a9ac970f9a187a13113cf0bbcc1dcbd493588e9c53a1c5f |
| G310 EXACT_DERIVATION.md | a417b3cfa1cc6136429a14d3b330c1b8c25c73c9e946d6b6454d6ffae72c25a0 |
| G312 EXACT_DERIVATION.md | 90ae2841153754087e64ba14d0a61c408d0b5767b5c8ed9f558da0b49ab30ea4 |
| Current GR AUTHORITY_RECORD.md | 80daa0be6d3e1c0ac1b734fea089c4eb487f05bc1e1fbb2fabd69322ca89f28c |

Commands executed for this stage were read-only shell reads, `git status
--short --branch`, `git rev-parse HEAD`, a Python csv.DictReader query selecting
G301/G310/G312 status/source fields, and hashlib SHA-256 comparisons to
LAUNCH.json. The PDF was inspected through the web tool; it was not downloaded
or independently hash-pinned. Its version marker is arXiv:0709.1928v2.

No symbolic witness calculation, fresh G301 invariant-basis census, replay of
historical numerical checks, full current premise audit, formal proof assistant
verification, human-specialist check, source-law comparison, nonlinear
well-posedness proof or empirical GR-filter analysis was done at this seal.
The planned direct stage has at most two CPU threads/1.5 GiB, no GPU, no mesh;
the overall dispatch deadline is 16:50 UTC. This source-first note will remain
unchanged; later findings belong in a separate direct-review record.
