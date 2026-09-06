# Stage A — source-first local normalized-cone reconstruction

Date: 2026-09-06. Reviewer: `/root/normalized_cone_adversarial_review`, a separate agent context. Exact runtime model: **UNKNOWN**; a different model is not established. Repository HEAD independently observed as `f14098737a7bd571aff79bef09ccffdc22135853`, branch `grok`. This is a pinned read-only review; no checkout, fetch, pull, staging, commit, repository edit, GPU process, external disk operation, protected-payload inspection, or second verifier was performed.

Stage-A finding: the stated **local conditional existence theorem survives this source-first adversarial reconstruction**, with the full ambient covector normalization retained. Affineness is a necessary compatibility condition and is already supplied by G349. The extension is nonunique away from the cone. Nevertheless, two extensions with the same full covector on the retained cone give identical G352 original-cut local readouts when all the question's other data are fixed. This is an independently reconstructed mathematical argument, not a verdict on an inspected candidate or physical realization.

## 1. Freeze, scope, exposure, and independence

The dispatched question is: for every point q0 of a smooth locally embedded regular G349 source-cone branch N, away from its vertex and screen-rank loss, does some ambient neighborhood V admit a smooth scalar Theta such that

```text
g^{-1}(dTheta,dTheta)=0 on V,
(dTheta)^sharp is future and nonzero on V,
Theta=0 on N intersect V,
dTheta_q=k_q^flat as full ambient covectors for every q in N intersect V,
```

where k is the already prescribed affine tangent from source normalization k(p)=u+n and is not rescaled? The second question fixes the original cut maps, endpoint observers, finite label measure, common positive spacing, and chosen G352 product conditions, and asks whether two such extensions can give different original-cut local readouts.

The frame is metric-led. Supplied geometric data and the affine source normalization are pinned by the question and G349, rather than selected by this review. Smooth coordinate slices, initial-data extensions, Hamiltonian characteristics, and exact algebra are freely chosen mathematical methods. The eikonal equation is the question's mathematical target, not a newly adopted physical equation. There is no physical parameter, source population, carrier, action, field equation, detector, phase interpretation, selected scale, or X_max input. The conclusion ceiling is a local mathematical construction and a conditional fixed-cut dependence statement. No global optical function, physical phase, populated label measure, or product realization is derived.

Source exposure, in order:

1. On-disk AGENTS.md, including the parent's current uncommitted verification-cycle paragraph. It is method only.
2. Only the STARTUP_CURRENT blocks of LIVE.md and HANDOFF.md; CURRENT_RESEARCH_PROGRAM.md; CURRENT_SCIENTIFIC_PREMISES.md. Per explicit dispatch the parent owns the current full premise verifier; this reviewer neither runs it nor queries the wide registry.
3. CLAUDE.md sections How we work, DRIVER TRIGGERS, and Repo discipline; the complete verifier-before-record, completeness-map, no-shortcuts, and solution-space-not-imposition SKILL.md files; complete CROSS_MODEL_VERIFY.md; compact INDEX.md and MEMORY.md.
4. After the orientation report: G349 AUDIT_REPORT.md and EXACT_DERIVATION.md; G351 AUDIT_REPORT.md and EXACT_DERIVATION.md; G352 AUDIT_REPORT.md, EXACT_DERIVATION.md, and ADOPTION_RECORD.md. A truncated combined tool return for G351 was followed by a complete separate read.

All read file bytes are identified in STAGE_A_SOURCE_SHA256SUMS.txt. A targeted `git diff --name-only` against pinned HEAD returned no changes in these scientific/startup/protocol sources other than the separately disclosed AGENTS.md edit, which was excluded from that unchanged-source query. Historical pending-review headers in exact derivations were not used to overrule the current audit reports or registry ownership.

The normalized-cone candidate package was **not opened**. No candidate proof, script, README, output, or prior review was read. Its directory name was visible in the dispatch and repository status only. The parent supplied the target question, which is unavoidable target-claim exposure. No other unpromoted scientific candidate was read. Repository status displayed unrelated dirty/untracked paths, including protected paths; their contents were not inspected. Backup completeness and pre-reboot unsaved-state disposition remain **UNVERIFIED**. Remote freshness is not claimed by this pinned reviewer.

Independence axes: separate context, yes; exact model, UNKNOWN; different model, UNTESTED; argument, source-first reconstruction without candidate exposure; implementation, one small independently authored SymPy control with no repository imports. Accepted-source historical test counts and verdicts were encountered as documentary source content but were not re-certified or used as substitutes for the argument below.

## 2. What the accepted definitions actually provide

G349 exact derivation sections 1–2 supplies a smooth null-geodesic family from p with k(p)=u+n, -g(k,u)=1 initially, and affine geodesic parameter. For source-direction variations J_A it proves g(k,J_A)=0. On the retained screen-rank-two stratum, the two quotient-screen variations are independent. Therefore k,J_1,J_2 are three independent vectors orthogonal to k. On the stipulated locally embedded branch they span TN=k-perp. Thus N is a smooth null hypersurface, k is its nonzero future null normal and generator, and

```text
k^flat|TN=0,       nabla_k k=0.
```

This is a statement about the three-dimensional locally retained cone branch, not merely the two-dimensional endpoint cut. The full G349 finite map permits caustics and repeated sheets; those broader features do not invalidate the explicitly local regular-branch restriction here, nor do they disappear from G349 generally.

G351 exact derivation section 3 supplies, conditionally on its provisional conservation premise, dmu_ac=s(lambda)dlambda and regular metric sheet area dA_i=J_i dlambda, J_i>0, so n_i=s/J_i almost everywhere. A general finite measure can have a singular part and no ordinary full-measure density.

G352 exact derivation sections 1–2 and 6 uses the **ambient phase covector** to define omega_i=-dTheta(u_i)>0, and then, on its explicitly chosen continuous phase-independent product realization,

```text
Gamma_i=(omega_i/DeltaTheta) s/J_i,
nu_i(B)=integral_{X_i^{-1}(B)} (omega_i/DeltaTheta) dmu.
```

The latter is finite when the displayed weight is mu-integrable. The source explicitly supplies local observer worldline extensions and does not infer a global worldline or all phase-level crossings. Neither G351 nor the G352 adoption record derives the phase or product factorization. This review preserves those distinctions.

## 3. Necessary condition: affine normalization cannot be ignored

If K=(dTheta)^sharp and g(K,K)=0 on an ambient open set, symmetry of the Hessian gives

```text
(nabla_K K)_b = K^a nabla_a nabla_b Theta
              = K^a nabla_b nabla_a Theta
              = (1/2) nabla_b(g(K,K)) = 0.
```

If K agrees with a prescribed k on a smooth hypersurface containing its generator curves, their covariant derivatives along those curves agree. Hence necessarily nabla_k k=0 on N. Merely being a future null normal field is insufficient. A rescaling k_tilde=h k of an affine k gives

```text
nabla_{k_tilde} k_tilde = h k(h) k.
```

An arbitrary generator-dependent h can therefore obstruct the requested full normalization. A positive rescaling constant along each generator preserves affineness, but it changes the specified data unless it equals one. **No rescaling is used in the existence proof.**

The other elementary compatibility condition is k-flat annihilating TN, forced by Theta|N=0. G349 and the regular-branch hypothesis already provide it. Equality only after pullback to TN would lose all normalization information: both sides of that pullback equality vanish.

## 4. Local existence with the prescribed full covector

Fix q0 in the admitted branch. Choose a small smooth spacelike hypersurface S through q0. Since a nonzero null vector cannot be tangent to a spacelike hypersurface, k is transverse to S. The intersection C=S intersect N is a smooth spacelike two-surface, and its nearby k-flow fills the retained N patch after shrinking.

Let alpha=k-flat|TS along C. Because TN=k-perp, alpha annihilates TC. Alpha is nonzero: a nonzero null covector cannot annihilate the entire spacelike hyperplane TS. Choose a defining function x for C in S. Then alpha=a dx along C for a smooth nonzero a. Extend a smoothly off C in S and set f=x a_extended. Consequently

```text
f|C=0,                df|C=k-flat|TS.
```

This realizes the necessary first jet on C without imposing unsupported transverse integrability. The conormal condition makes its tangent derivatives compatible automatically. Higher-order terms in f normal to C are free mathematical continuation data.

Extend S to a local spacetime coordinate chart with S={t=0}. At every point near C in S, df is nonzero. Complete df to an ambient null covector P by choosing the unique root of

```text
H(x,P)=(1/2)g^{-1}(P,P)=0
```

whose raised vector is future. A spacelike S has timelike conormal, so the two nonzero null completions have opposite time orientations and the chosen root is smooth. Equivalently, the implicit derivative in the missing covector component is the nonzero component of P-sharp transverse to S. On C, the prescribed k-flat is exactly this unique future completion of df. Thus P=k-flat as full ambient covectors there; no scale adjustment has entered.

Use the Hamiltonian flow of H with this initial three-dimensional covector graph over S. At flow time zero, the derivative of the base-point map in the new flow direction is P-sharp, transverse to S. The inverse function theorem therefore makes the characteristic base-point map a diffeomorphism from a sufficiently small flow neighborhood onto an ambient neighborhood V. This is the local step that excludes characteristic crossing; no finite or global injectivity is asserted.

The canonical characteristic construction yields a smooth solution with initial value f. Its action increment along a characteristic is

```text
P(dot x)-H = 2H-H = H = 0,
```

since H remains zero. Thus Theta is f carried along characteristics. The canonical one-form restricted to the initial graph equals df, and its evolution restricted to H=0 preserves this exact initial differential; hence the resulting ambient differential is precisely the evolved momentum P. It follows that H(x,dTheta)=0. The initially future nonzero momentum stays future and nonzero after shrinking V. This also follows directly from smooth null geodesic flow and continuity.

For initial points in C, the Hamiltonian characteristic is the affine null geodesic with initial tangent k. The pre-existing G349 generator is the affine null geodesic with the **same full initial tangent**, so ordinary local geodesic uniqueness makes the characteristic and its tangent agree with that G349 generator. Along it Theta=f|C=0, and dTheta=k-flat. These generators fill N intersect V after shrinking, proving the full desired conclusion at q0. As q0 was arbitrary, every admitted point has such a neighborhood. Because dTheta is nonzero, the zero level set and N also coincide locally after a final shrink if desired.

The argument uses ordinary smooth inverse-function and ODE facts, not analyticity or an unjustified characteristic initial-value uniqueness theorem on N. The Cauchy surface is spacelike and noncharacteristic; N is a selected characteristic subset of its local solution. It establishes a general local conditional theorem, not a finite-example extrapolation.

## 5. Freedom, obstructions, and scope limits

Nonuniqueness is immediate. If Theta works and F is smooth with F(0)=0, F'(0)=1, and F'>0 near zero, then F(Theta) also works on a smaller neighborhood. Its differential on N is still k-flat. For example F(z)=z+a z^2 changes a transverse second derivative while retaining the complete cone first jet. This preserves the fixed normalization and is not the forbidden constant rescaling of k.

There is more continuation freedom than constant affine phase changes: f on S can be modified at second and higher order away from C. These data propagate through the same noncharacteristic construction. Off-cone derivatives are constrained by the eikonal equation and cannot be prescribed independently without compatibility; the present theorem does not give a global classification of every such freedom.

The relevant limits are precise:

- The vertex has no smooth cone normal agreeing with all direction-dependent k values. It is excluded.
- Screen-rank loss, a nonsmooth projected cone, or competing branches at one event is outside the local embedded regular-branch theorem. Different prescribed covectors at one event cannot all equal a single ambient differential.
- Nonaffine prescribed tangents can fail by section 3. G349's actual tangent avoids this obstruction.
- A sufficiently small neighborhood for each point is not one uniform neighborhood for an arbitrarily long or finite cone patch. Off-cone characteristic crossings, topology, or branch identifications can obstruct continuation or gluing. Finite-cover existence alone is not a gluing theorem.
- Future nonzero gradient is secured locally. Nonlinear F may cease to preserve it where F' vanishes or changes sign; those points are excluded by shrinking.
- This proof does not require changing source, observer, affine cut, or k, and does not infer physical phase units from the geometric normalization -g(k(p),u)=1.

## 6. Fixed original-cut G352 readouts

Let Theta_1 and Theta_2 both satisfy the full normalization at every relevant original-cut endpoint, with those endpoints lying in their common extension domain. For every fixed endpoint observer u_i,

```text
omega_i^(1)=-dTheta_1(u_i)=-g(k,u_i)=-dTheta_2(u_i)=omega_i^(2).
```

The area Jacobian J_i depends on the fixed metric, labelled cut map, and screen geometry, so it is unchanged. The same supplied measure has the same s, and DeltaTheta is fixed by the question. Consequently

```text
Gamma_i^(1)=Gamma_i^(2) almost everywhere on the regular ac component.
```

Their fixed-cut weighted pushforwards nu_i agree as well when measurable and integrable. The equality of densities does not require s>0, but dividing them or identifying transfer ratios does require nonzero density. Finite mu alone is not an integrability proof on a noncompact or unbounded-weight retained domain; G352's stated condition remains explicit.

Where the ratio is defined, both give Gamma_j/Gamma_i=R_ji A_ji^{-1}. The sameness statement is a dependence argument using G352's accepted formula and the fixed full first jet; it is not a new independent derivation of the product realization. Literal atomic crossing counts, finite worldline histories, arbitrary off-cone readouts, phase-dependent measure families, and changed cut maps remain outside it. In particular, Theta is zero along the cone's own null generators; G352's local rate uses a transverse timelike observer direction, not variation along k.

If only Theta|N=0 were required, b Theta with b>0 would preserve that level set but change omega and Gamma by b when spacing is held fixed. This is why the full ambient normalization is load-bearing. G352's harmless **common positive affine phase rescaling** changes both omega and spacing; that is a different comparison from the question's fixed-k, fixed-spacing comparison. The nonlinear F freedom above preserves the local original-cut first jet but is not a general invariance of fixed finite phase increments away from N.

## 7. Independent exact control and actual execution

Before computation, the reviewer stated the finite-control question, radial Minkowski regime r>0, exact CPU symbolic method, absent numerical grid/tolerances, no physical parameters, and the finite-witness conclusion ceiling. The script stage_a_exact_witness.py was authored via apply_patch only in the authorized scratch directory. Execution was:

```text
timeout 30s python3 /tmp/udt-cone-review-0WvbvE/stage_a_exact_witness.py > /tmp/udt-cone-review-0WvbvE/STAGE_A_EXACT_RESULT.json 2> /tmp/udt-cone-review-0WvbvE/STAGE_A_EXACT_STDERR.txt
```

It exited 0 in approximately 0.21 seconds with Python 3.10.12 and SymPy 1.13.1. Stderr is empty. In spherical Minkowski coordinates, with radial inverse metric diag(-1,1) and zero angular covector entries, it independently verified:

```text
Theta_0=r-t,                    Theta_a=(r-t)+a(r-t)^2,
both null norms = 0,
(dTheta_a-dTheta_0)|t=r = (0,0),
raised dTheta_0 = (1,1),
omega for u=(cosh eta,sinh eta) = exp(-eta),
omega_a-omega_0 on t=r = 0,
partial_t^2(Theta_a-Theta_0)=2a,
nabla_K K = (t,t) for K=t(1,1) on t=r>0.
```

The future domain for Theta_a is 1+2a(r-t)>0. The symbolic results witness exact matching, extension nonuniqueness, and a nonaffine obstruction. They do not establish the general theorem, uniqueness of any physical phase, or a classification of continuation freedom. No production script, prior result, grid, raw array, or GPU artifact was loaded or replayed. No new test harness or mutation-count claim is made.

## 8. Stage-A handoff ceiling

No local mathematical obstruction remains under the exact stated regularity, embeddedness, and affine-normal assumptions in this reconstruction. A candidate would still need to exhibit the noncharacteristic construction or an equally valid argument; merely invoking Frobenius for a direction field, prescribing characteristic data on N without a local existence argument, or checking a flat cone would not suffice. It must preserve the distinction between ambient covector equality and vanishing pullback, and must not infer arbitrary finite-patch/global extension or physical realization.

This is **Stage A only**, frozen before candidate exposure. Candidate comparison and final adversarial verdict remain pending Stage B. The parent owns the current premise-audit result and any subsequent banking. Review does not upgrade accepted-source grades, adopt G351/G352's supplied realization data, choose a physical phase or population, or confer canon.

Closure provenance update, received before the Stage-A freeze: the parent reports the current premise verifier exited 0 and passed all 335 rows, with output retrieved at 17:15:05 UTC from session 71643. This reviewer did not independently execute or inspect that verifier output. No exact registry query was necessary for this reconstruction. The parent also reports that its method-only commit moved working HEAD to b75fcc5e641702d0cae3e8740046513cbd4e8dd5, while the admitted scientific sources and candidate remain byte-identical to f1409873. The scientific source snapshot of this review remains f14098737a7bd571aff79bef09ccffdc22135853; the actual HEAD observation at the beginning of this report is an observation at startup, not a claim that shared HEAD could not subsequently move.
