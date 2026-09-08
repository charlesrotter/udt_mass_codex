# SM2 grouped initial adversarial review

Verdict: VERIFIED-WITH-CAVEATS for the candidate's exact optional local
mathematical class and universal quantifier. No load-bearing mathematical
defect or required scientific repair was found. The author preserved and
repaired an initial symbolic-harness false failure before direct review;
the parent conservatively counts that as the step's one repair allowance.
This review covers the unchanged initial mathematical candidate and both
harness versions. It neither promotes science nor adopts a physical source.

Reviewer `/root/sm2_tensor_review`, 2026-09-08 UTC. Actual baseline checked
twice: grok cc71a324a61bf2711a4b52c8ebee8a8e4d9b8269. Existing status-file
edits, unrelated untracked work and protected payloads were left untouched.
No remote synchronization was attempted in this explicitly pinned review.

## Pins and exposure

Initial candidate ../CANDIDATE_INITIAL.md SHA256:
fb016f86187e5b7a29cb934ed8e0cff9a8984fddd181b13bbcdee4c9fb190c17.
Initial author check_tensor.py SHA256:
652b67bd0b09057e0d9c43269857bd1484d3aced8c5d848547ae9b71ea845620.
Repaired author check_tensor_repaired.py SHA256:
3c4591000db6a2f673c6328b4778ca940fd9a3e82057c53031e8b3dc4589015d.
Repaired saved author stdout SHA256:
740d00e11cb8a1eb619227531d2d60ca02f0855be40c78ac8f19a69920b617a3.
All four independently matched the dispatch pins before direct review.

The source-first requirements/approach were sealed before any SM2 candidate,
author code, output or prior-verdict exposure:
SOURCE_FIRST_REQUIREMENTS.md SHA256
10f8926f5acd170a4f90af9e140a95cec7a29fa52563c1490ddb182383b4f04c.
Only seal completion and absence of a decisive source blocker were sent to
the author before candidate freeze. The reconstructed classification and
proof were withheld. The first independent checker was written and run
before direct candidate/code exposure; its run began01:52:45UTC. The parent
then supplied frozen candidate pins and disclosed the preserved author
harness failure/repair. The final explicit RED-path catch proof was written
after direct exposure and is identified as such.

SM1 initial candidate and review pins independently matched:
b9c883ebb807ea2aea6b6bc7487d407cc218a04c0c8852426ffa899a99dd7e8d,
55b8e25734f9cf4fdfea6cec39d71386bd7468869b1dbe67003289adb1047554.
SM1 REVIEWED_RESULT.md SHA256:
74a47c48adb2381f26df3dbe82cac2e28e4aac39a05e9d41ae9e01ce6ff02605.
The five directly load-bearing G312-adoption/G313/G315/G351/G352 source
hashes matched SOURCE_LEDGER.tsv; exact registry rows retain their own
conditional/adopted scopes. Historical source check counts were not replayed.
The parent's later addition of a G261 source pointer for planned SM3 was
disclosed during review; it is not a new dependency or premise of SM2.

| Independence axis | Actual record |
|---|---|
| Context | Fresh separate author/reviewer contexts |
| Model | Exact runtime identity UNKNOWN; different-model axis UNTESTED |
| Implementation | Independent Lorentz-generator linear system and Cartesian tensor differentiation; no author imports |
| Argument | Source-first reconstruction before target exposure; direct adversarial comparison afterward |
| Exposure | Definitions/class and reviewed SM1 known first; candidate, both author scripts and outputs read only in direct stage |
| Human specialist | UNTESTED |

## Classification and universal necessity

The optional class is sufficiently explicit: one smooth pointwise Lorentz-
natural symmetric covariant tensor prescription of g, nonzero future-raised
null q and n>0. It excludes external position/label/phase-value functions,
extra vectors or fields, curvature, derivatives and nonlocal inputs. It
does not assume linearity in n, positivity, energy meaning or physical
normalization. Fixed parameters of a prescription may remain unselected.

In a null frame with g(ell,k)=-1, invariance under screen rotations leaves
the four displayed components u,v,w,z. A null rotation fixing ell forces
u=0 from P(ell,e1+t ell), and then v=-z from P(e1+t ell,k'). The surviving
two-dimensional space is exactly span{g,q tensor q}. Both surviving tensors
are invariant under the full stabilizer. The proper orthochronous Lorentz
group acts transitively on the entire nonzero future null cone, including
its apparent amplitude freedom through boosts. Consequently there is no
additional scalar invariant of q at fixed g. The coefficients are A(n),
B(n), with any fixed prescription parameters retained. This argument covers
smooth nonpolynomial coefficient dependence; it is not a polynomial ansatz.
Orientation supplies no missed symmetric invariant because the stabilizer
argument already used the oriented/time-oriented group.

Independently, the exact linear equations for a general ten-component
symmetric matrix under one screen-rotation and two null-rotation generators
have rank8/nullity2. Screen rotations alone leave nullity4. A preferred-time
square is invariant under the latter incomplete test but fails a null
rotation. Thus a screen-rotation-only check would be a real false pass.
This finite representation calculation anchors the general little-group
argument; it does not replace the orbit and smoothness reasoning.

For P=A(n)g+B(n)qq, metric compatibility gives dA. Exactness and nullness of
q imply nabla_ell q=0, and SM1 supplies ell(n)=-n theta. The product rule
therefore gives the claimed divergence covector exactly:

    div(P) = A'(n) dn + [B(n)-n B'(n)] theta q.

Necessity across EVERY admitted product tube is established by actual flat
families, with no assumption that arbitrary adapted metrics obey vacuum.
The parallel family has theta=0 and permits n=n0+epsilon*x on a bounded
label patch small enough to be positive, smooth and finite. Its nonzero
transverse derivative forces A'(n0)=0. The point value n0 is arbitrary,
so A=A0 on the connected positive domain. The outgoing spherical family
has q=d(r-t), ell=partial_r in its adapted chart, J=r^2 sin(vartheta), and
theta=2/r. It is regular locally away from the vertex and angular poles.
The freely supplied phase-independent label density can be scaled to give
any chosen n0>0 at the retained event while remaining finite on that patch.
Thus B(n0)-n0 B'(n0)=0 at every positive n0, hence (B/n)'=0 and B=Cn.
The argument does not infer an all-n statement from a finite grid.

Conversely A0g+C nqq has zero divergence on every regular tube with
div(n ell)=0 and nabla_ell q=0, by direct tensor calculus. It does not need
the vacuum equation or the stronger phase-independent product. The candidate
correctly identifies this broader sufficiency as a geometric identity,
without extending the physically admitted vacuum response arena.

Therefore the full stated necessity AND sufficiency survive within the
declared input class and universal quantifier. On a particular zero-expansion
tube arbitrary B(n) can be compatible; the universal theorem must not be
reused to prohibit such a single-history choice. The candidate preserves
that distinction and does not require uniqueness of ordinary supplied data.

## Normalization, additional data and physical boundaries

The admitted simultaneous affine phase/spacing change leaves q fixed.
Fixed phase-independent passive label relabeling changes s and J by the
same absolute Jacobian and leaves n fixed, subject to SM1's orientation
caveat. Hence the classified tensor respects those actual gauges. Scaling
mu changes n and the null tensor part; it is data variation, not gauge.
No vanishing-at-zero-density requirement was included, so the independent
constant metric term is correctly retained. Its interpretation is open.

For a future unit observer U, the tensor contraction is

    P(U,U) = -A0 + C n[-U(phi)]^2,

whereas SM1/G352's current readout is n[-U(phi)]. Thus the rank-two
construction does not identify energy, a per-crossing value or the original
clock-rate readout. A physical normalization or metric source equation
does not follow from matching a familiar tensor form. This is consistent
with, and remains an explicit downstream limit on, the candidate.

An independently supplied scalar w with ell(w)=0 yields the sufficient
enlarged-class construction A0g+n wqq. Its divergence contribution is
n ell(w)q, which vanishes exactly for transported w when n>0 and q!=0.
In the local connected flow box w=W(phi,y) is freely supplied transport
data. Nonconstant examples exist. Folding w into the measure need not
preserve its phase-independent product or positivity; the candidate does
not claim either. It also correctly avoids an exhaustive classification
of this enlarged class. Declaring physical status or a coupling for w
would be a separate step, not ordinary value selection inside the present
mathematical comparison.

G312/G313/G315 retain their owner-provisional bounded vacuum response and
conditional lawful-data interpretation. Their scalar constancy cannot be
silently extended to a sourced comparison. G351/G352 supply conservation
and the chosen readout/product, not physical identification, independent
gravitational degrees of freedom or a metric-response equation. No source
positivity, cross-family addition, action, scale, population or canon follows.

## Independent recomputation, catch proof and harness repair

The independent_tensor_check.py SHA256 is
409185f0d4f23e12dd5129eafeaf843cff3aa358458fc4fb86845b664373870c.
It imports no author code and reads no author result. Its coordinate
calculation uses Cartesian Minkowski components and differentiates the FULL
contravariant tensor with q=d(sqrt(x^2+y^2+z^2)-t). The metric is constant,
so this is exactly covariant divergence with zero Christoffel symbols. It
does not implement the author's already-reduced coefficient formula as its
computed quantity. The reduced identity is compared against this independent
differentiation afterward.

Result:25/25 exact diagnostics, exit0,1.309719974seconds, maximum child
RSS49516KiB, empty stderr. Python3.10.12, SymPy1.13.1. At the independently
chosen event (x,y,z)=(1,2,2), r=3 and amplitude9, n=1:

- The nqq tensor has covariant divergence0.
- The n^2qq mutant has contravariant divergence
  (-2/3,-2/9,-4/9,-4/9), while the same nonlinear choice passes a parallel
  family. This is a concrete expansion-dependent false pass.
- A variable metric coefficient on the parallel n=2+x family produces
  divergence (0,1,0,0).
- The nonconstant transported weight2+x/r gives divergence0; replacing it
  by2+r gives (1,1/3,2/3,2/3).
- The preferred-time tensor fails null-rotation invariance with explicit
  nonzero01/10 matrix entries despite passing screen rotations.

The post-exposure guard_catchproof.py independently reintroduces five defects
into the corresponding zero-residual acceptance guards. Each guard actually
raises AssertionError, recorded as RED; five matching good controls pass.
The defects are n->n^2, constant metric coefficient->n, transported weight
->r, addition of a rotation-only invariant time tensor, and phase rescaling
without spacing rescaling. Result5/5 matching RED paths, exit0,
0.590604464seconds, RSS48776KiB, empty stderr. These are finite exact
mutation checks, not a completeness or numerical-certification theorem.

The original author script was replayed unchanged and again exited1 at
second_stabilizer_constraint. Its stderr is byte-identical to the preserved
original stderr. The defect is structural expression equality: expanded
t*v+t*z is not the same SymPy expression tree as t*(v+z), although their
algebraic difference is zero. The candidate's mathematics is unaffected.
The repaired script replaces that comparison and the analogous later
transport-coefficient comparison with simplified residual equality to zero.
It also replaces a formal unknown-function nonzero check with an explicit
quadratic A mutation. Those are scoped harness repairs, not changes to
the proposed theorem. Original code/failure output remain preserved.

Repaired author replay:14/14, exit0,0.225786668seconds, RSS47076KiB, empty
stderr; stdout byte-identical to the author's repaired saved stdout. This
is shared-code regression only. Its generic W derivative/inequality guards
test formal nonidentity, not nonzero values for every possible W or event.
The independent explicit transported/nontransported examples above avoid
that limitation. The analytic argument, not those guards, owns the quantifier.

All four numerical runs used the inspected existing capture utility with
512MiB address space,60s CPU/wall, and explicit OPENBLAS/OMP/MKL threads1.
No numerical child overlapped another in this context. Exact commands and
capture hashes are preserved in EXECUTION_RECORD.md and REVIEW_MANIFEST.tsv.

## Omissions and useful return

The parent actually completed the full349 premise audit; this reviewer read
its receipt rather than duplicating it. Receipt SHA256
d665a3ba872c4d06bd49d78dbb7af63bea07358cc4939693e107f125f84dd9c5;
registry SHA256 ccd1fd2752a5884dfa2864fc9f3904f9dcc7e22557f6d4057e92ec2c54caf81f.
The receipt does not preserve separate initial terminal streams or an exact
full-audit elapsed time. Historical scientific source checks, global PDE
theorems, caustics/singular measures, arbitrary derivative/curvature or
extra-field tensor classes, cross-family physics, metric constraints and
coupled existence were not replayed or established here. No observations,
network use, fitting, protected payload access or scientific promotion occurred.

The useful reviewed conditional input is exactly P=A0g+C nqq as the full
divergence-compatible family in SM2's optional universal algebraic class,
with A0,C unselected and a sufficient transported-weight enlargement outside
that class. No required scientific repair remains. SM3 may assess the
metric-response interface at this reviewed scope under the approved work
order; tensor conservation alone does not close or adopt that interface.
