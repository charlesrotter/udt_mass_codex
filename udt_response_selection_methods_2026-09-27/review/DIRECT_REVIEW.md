# Direct adversarial review

Verdict: **VERIFIED-WITH-CAVEATS**, for the explicitly conditional mathematics
and first-variation witness described below. No remaining mathematical defect
was found in the reviewed parent or canonical argument. This verdict supplies
neither UDT response-class membership, physical adoption nor canon. Final brief
and roadmap fidelity, if subsequently dispatched, are recorded separately.

Reviewer: `/root/selection_review`, fresh separate context, same inherited
Codex/GPT-6 runtime as parent; exact model identifier beyond that is not exposed.
No different-model or human-specialist review is claimed. Source-first argument
and exact code were frozen before candidate exposure in SOURCE_FIRST_FREEZE.json
at 2026-09-27T23:54:23.383456Z. Mathematical methods and SymPy are shared;
implementations and argument construction are separate. Candidate content was
then opened only after explicit parent dispatch. Direct evidence is necessarily
claim-exposed. No construction code was imported into the independent checks.

## Reviewed bytes and exposure order

1. Before exposure: work-order definitions, requested authority/method protocols,
   G301/G310/G311/G312 source audits, exact four registry rows, current G312
   reconciliation, founding F1–F4/W1 and W4–W6, and primary methods sources.
   Parent's scope reminder named the canonical-versus-DDR trace-sector seam but
   supplied no proof or coefficient result. SOURCE_FIRST.md gives the argument.
2. Parent CANDIDATE.md was inspected at SHA-256
   `51fc139e2d6de2b8ee25c20338fef2d8cefbf23cfdf1f00aec14402b57103dbc`.
3. `direct_checks.py` was written and run without opening either constructor's
   code. Parent check code/output were subsequently read for defect inspection,
   not reused as independent evidence.
4. Prior extension sections A and C plus the critical branch and CLOSEOUT were
   read for scope fidelity. The critical branch was not re-solved or reclassified.
5. Canonical CONSTRUCTION.md was inspected at SHA-256
   `e72b5deb23536882ace3fb7509959cce0ad6aaa6a7a4bf5c996970b5139c6bd4`,
   followed by its check code and result. Its complete derivatives and analytic
   constrained weak-closure witness were examined directly.
6. The current saved premise-verifier stdout, stderr and execution JSON were
   inspected. They record exit 0, no timeout, 409.752463877001 seconds, an explicit
   406-row PASS and zero-byte stderr. This is inspection of parent's saved run,
   **not an independent verifier rerun**.

Exact local input/output pins and commands are in DIRECT_REVIEW_RECORD.json.
Protected payloads were never opened. Edits were confined to the review directory.

## Findings, survivors and smallest repairs

| ID | Adversarial test | Disposition and surviving scope |
|---|---|---|
| R1 | Does on-shell DDR secretly provide identity divergence? | No. V1 and the explicit quantifier over arbitrary regular metric jets are correct. On DDR solutions all b give constant R; identity divergence of E itself selects b=-a/2. |
| R2 | Does the inverse variational test use the wrong source or confuse response with equation? | No. Densitization, covariant versus inverse metric variation, flat-background necessity, and nonlinear sufficiency are separated. The unrestricted Helmholtz obstruction selects the Einstein representative, while TF(E)=0 still allows its connected trace datum. |
| R3 | Does the canonical proof omit tensor components, densities, signs or metric derivatives? | No. Both complete functional derivatives are correct; the symmetric-index convention, weight-one Lie derivative, curvature first variation and compact-support integrations agree with independent reconstruction. Strong closure gives AC=-1, B=-A/2 with D free. |
| R4 | Is weak-closure necessity inferred from unconstrained jets? | No. The constructor supplies an actual local H=D_i=0 family with nonzero trace-gradient obstruction. Its local positivity and all-smearings argument are valid; details are below. |
| R5 | Does fixed canonical D silently erase DDR's trace datum or extend G301? | No. H3–H5 correctly distinguish the fixed-Lambda canonical action sector from DDR's integrated trace sector. The bare metric term is expressly outside original G301 flat/weight-one gates. |
| R6 | Is Q3 only a trace-equation mode with no metric lift? | No. Direct metric-jet reconstruction gives R^L=6 alpha box rho and all ten symmetric components of the full linearized response vanish for the stated scalar equation. Nonzero rho is not pure gauge. The witness is restricted to flat, fixed lambda=0 first variation. |
| R7 | Does the auxiliary rewrite divide away the critical branch? | No. Elimination divides only by nonzero alpha, never psi. At R=-1/(2alpha), the response remains g/(8alpha); the earlier branch and its loss-of-linear-response limits survive. No regular evolution claim is made there. |
| R8 | Do the method theorems or comparison controls supply native premises? | No. Locality, naturality, order, density/source typing, off-shell identity, phase space, canonical action and strong target remain additional hypotheses. GR is retained as a filter. |

No scientific repair is required for these reviewed bytes. The strongest survivor
is conditional representative/closure selection, plus a full flat scalar
first-variation witness for the already unadopted higher-order comparison.
The smallest repair for any later wording that upgrades this to native selection
would be to restore the class and trace-sector hypotheses, not alter an equation.

The reviewer found one **reviewer-check implementation defect**, not a candidate
defect: SymPy structural `==` compared two algebraically equal presentations of
the auxiliary scalar equation and returned false. The initial run was 28/29;
initial script/stdout/stderr are preserved as `initial_failed_direct_checks.*`.
The repair compares the simplified difference with zero. Unneeded nonzero
assumptions on R, lambda, rho, D and R3 were also removed; only alpha,A,N retain
nonzero assumptions for relevant division. An interim scalar-normalization check
was recognized as tautological and replaced by substitution of a single solved
Klein–Gordon Hessian jet into the independently reconstructed R^L. Final 29/29
checks pass. These repairs strengthen the check without changing candidate science.

## Direct mathematical examination

For R1–R2, the independent full ten-component bilinear calculation gives
`(a/2+b)[tr(u) k.v.k-tr(v) k.u.k]`, with the sign reversed under Fourier i k.
The candidate's concrete V3 is exactly `-2(a+2b)`. Nonconstant scalar metric jets
make the Bianchi coefficient nonvacuous. Necessity does not require assuming an
invariant action; it follows from the necessary Helmholtz condition. Sufficiency
is the explicit local Hilbert density. Trace-free variations are a different
variational problem; their existence does not make S itself an unrestricted
Euler–Lagrange source. Zero a,b is retained and fails nontrivial selection.

For R3, the kinetic h derivative follows by independently varying both lowering
metrics, the momentum trace and the determinant. The curvature derivative has
the positive Hessian-of-lapse term for covariant h variation. The density-weight
terms in both D derivatives are required. Antisymmetrization cancels every term
without lapse derivatives, including D and the full kinetic h derivative.
Independent curved, nondiagonal metric checks verify the remaining identity
modulo its explicit ordinary divergence. An omitted scalar-density connection
fails this check. Arbitrary divergence and trace-gradient momentum jets separate
the two strong coefficients. No symmetry-reduced experiment owns this quantifier.

For R4, an independent warped-product calculation gives, for
`h=diag(1,f(x)^2,1)`, `Ric_xx=-f''/f`, `Ric_yy=-f f''`, `Ric_zz=0` and
`R=-2f''/f`. With `pi^zz=f x`, the momentum constraint is zero: the only nonzero
momentum lies in a flat product direction and has no z dependence. Its trace
is `p=f x`, so density differentiation gives `nabla_x p=f`, not `(f x)'`.
The Hamiltonian constraint reduces to
`f''=[((A+B)x^2+D)/(2C)]f`. For C!=0, standard local existence for this smooth
linear ODE with f(0)=1,f'(0)=0 provides f>0 on a smaller interval. Compactly
supported nonzero N, with M=xN, yields
`-2C(A+2B) integral f N^2`, nonzero whenever C(A+2B)!=0. Thus no omitted
constraint-surface restriction rescues the original constraints. Conversely
C(A+2B)=0 eliminates the anomaly and leaves a multiple of D. Empty constraint
surfaces for some ultralocal constants are explicitly disclosed. This algebraic
iff does not prove a complete dynamics for added trace constraints or free lapse.

For R5, the six-component nondiagonal Legendre map independently reproduces
`pi^{ij}=sqrt(h)(K^{ij}-K h^{ij})/A` and
`L=N sqrt(h)[(K_ij K^{ij}-K^2+R3)/A-D]`. The stated spacetime dictionary and
Gauss–Codazzi convention yield Lambda=AD/2. Introducing this canonical action
is a comparison hypothesis, and unrestricted variation sets the response to
zero in that sector. DDR has only TF(E)=0 and permits E=lambda g. Matching
D across a family of sectors is not an off-shell equivalence of formulations.

For R6–R7, a separate exact jet calculation starts from
`h_ab,cd=-2alpha eta_ab rho_,cd`, computes Ric^L directly and obtains
`R^L=6alpha box rho`. The full response factors as
`-2alpha(eta_ab box-partial_a partial_b)(rho-6alpha box rho)`.
The unprolonged scalar equation normalizes R^L=rho and its differentiated
equation kills all ten response components. Pure-gauge R^L vanishes identically
for arbitrary gauge amplitude/covector, so the nonzero-rho witness is non-gauge.
The characteristic statement concerns this linear sector's principal operator;
no physical mass, energy sign, nonlinear lift or complete PDE property follows.
Auxiliary density and metric-response elimination agree, including the fixed
trace-sector `+2lambda` sign. The critical response is explicitly retained.

## Actual computations and omissions

- Source-first: `timeout 120s python3 .../review/source_first_checks.py`, exit 0,
  10/10 exact symbolic checks, Python 3.10.12 / SymPy 1.13.1.
- Direct: `timeout 120s python3 .../review/direct_checks.py`, final exit 0,
  29/29 exact symbolic checks, Python 3.10.12 / SymPy 1.13.1. Final observed
  subprocess wall time 0.42542537 seconds. Failed first-run streams are retained.
- Parent 56-check and constructor 34-check code/results were read. Their checks
  were not rerun in place because doing so would modify another worker's outputs;
  independent calculations above supply the load-bearing recomputation. Their
  pass counts remain attributed construction evidence, not additional independent
  reviewer passes. The constructor's discrepancy controls are finite algebraic
  diagnostics, not a blanket independent theorem or full mutation campaign.

No historical G301/all-pair package census was rerun. No new universal response
basis, all-metric theory classification, higher-order phase-space reconstruction,
global foliation/development, nonlinear stability, finite-amplitude family,
observational test, physical coupling/scale, boundary completion or native
emergence theorem was checked. The existing solver operators were untouched and
their tests were not replayed. General Noether/Helmholtz and Lovelock results were
checked for applicability boundaries, not independently reproved in full.

The method sources are pinned versions: Navarro/Navarro
[1005.2386v4](https://arxiv.org/html/1005.2386v4), Anderson/Pohjanpelto
[1202.5811v1](https://arxiv.org/html/1202.5811v1), Kouletsis
[gr-qc/9801019v1](https://arxiv.org/html/gr-qc/9801019v1), and metric f(R) variation
[1002.0617v4](https://arxiv.org/html/1002.0617v4). The ADM primary-paper abstract
[gr-qc/0405109](https://arxiv.org/abs/gr-qc/0405109) was inspected; this review's
explicit conventions, analytic geometry and independent Legendre checks own
the mapping, not an unexamined theorem attributed to that abstract.
