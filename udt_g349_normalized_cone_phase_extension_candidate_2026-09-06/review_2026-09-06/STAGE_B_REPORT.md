# Stage B — adversarial review of the normalized-cone candidate

Date: 2026-09-06. Reviewer: `/root/normalized_cone_adversarial_review`, fresh separate context. Exact runtime model: **UNKNOWN**. Candidate snapshot: `f14098737a7bd571aff79bef09ccffdc22135853`. Candidate directory: `udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/`. This report reviews its original 15 files, not the subsequently added review directory.

**Verdict: VERIFIED-WITH-CAVEATS for the exact local mathematical claim and conditional fixed-input original-cut readout statement. No substantive mathematical defect or unresolved objection was found. No scientific repair is required by this review.** The operational caveat is that `run_checks.py` is a capture runner, not an aggregate pass/fail gate; its exit 0 alone cannot certify the child results. The actual original and replayed child results were explicitly inspected and satisfy their stated expectations.

This verdict does not promote the candidate, alter a registry grade, supply G351/G352's premises or product realization, establish physical phase/content, or confer canon.

## 1. Authentication, chronology, and exposure

Stage A was completed before candidate disclosure, with report SHA-256

```text
6bb4d06722a009b7958495f7e4c5eb87669bd883cff8fdd5a519884ff6ffdce3
```

The parent authenticated and archived it byte-identically before authorizing Stage B. Its source-first proof, exposure list, finite control, and limitations are retained intact. Stage B began at approximately 17:19:49 UTC. The candidate target question had been exposed in Stage A; the candidate proof, code, saved outputs, README, and self-review had not.

In Stage B I read all 15 original files in full: the candidate argument; work order; README; premise/coverage ledger; review and provenance records; source and artifact manifests; three scripts; recorded exact result, capture runs, rational replay, and premise-verifier output. The new review directory was not read as scientific evidence. No earlier unpromoted candidate, protected payload, raw production array, or archive was inspected.

Authentication independently established:

- All 14 payloads match the original ARTIFACT_SHA256SUMS and their exact Git bytes at f1409873.
- ARTIFACT_SHA256SUMS itself matches Git at f1409873; SHA-256 is `6181adf15ba0342090d7df17665fae9ceab612d5ee389b5ba1d2631650d56368`.
- All 19 SOURCE_SHA256SUMS entries match both the candidate's declared source snapshot `5ef2f971805ee23383cad694c5cb058124614a5d` and review snapshot f1409873.
- Eighteen source entries still match live bytes. Historical AGENTS.md has SHA-256 `b9c4e7a0d90c66868281ced3e96da3a16a19797a91cb100b64b4b85620ff2f34` in both historical snapshots. Its live mismatch is the separately disclosed owner-requested method change, not a changed scientific premise.
- A final artifact-manifest replay again passed all 14 payloads and retained the original manifest hash.

Full hash details are in STAGE_B_AUTHENTICATION.json and STAGE_B_FINAL_PACKAGE_HASH_CHECK.txt. Hashing the registry is not a wide-row context query. I did not run another premise verifier. The parent's current verifier pass is recorded as parent-supplied evidence in Stage A; the candidate's saved verifier record was inspected as historical documentary evidence only.

Independence: separate context, established by this actual agent dispatch; different model, UNTESTED; runtime model, UNKNOWN; analytic argument, reconstructed source-first and frozen before disclosure; independent Stage-B computation, a Cartesian embedding/pullback-metric implementation of the explicit foliation witness. The source-first proof uses the same natural mathematical route as the eventual candidate, but was reconstructed before seeing it. Candidate-script replays remain same-code regression and are not independent general proofs.

## 2. Scope examined and analytic findings

The question is local at each point of a smooth locally embedded regular G349 source-cone branch, away from vertex and screen-rank loss, with its prescribed affine k retained. The target is a smooth neighborhood scalar with future nonzero null raised gradient, zero value on the retained cone, and equality of the **full ambient differential** to k-flat on that cone. Only fixed original-cut G352 readouts in a common extension domain are compared. Physical phase calibration, measure population, product selection, global cone coverage, finite observer histories, and physical interpretation are excluded.

### Sections 1–2: the geometric data and initial jet

The inference TN=k-perp is valid: G349 supplies k and two independent quotient-screen Jacobi directions; their three-dimensional span is orthogonal to k. The locally embedded regular-branch hypothesis makes this the tangent space of a smooth null hypersurface. This would not follow from an arbitrary rank-losing or merely two-dimensional endpoint map, but the candidate does not claim that broader domain.

A spacelike proof hypersurface S is transverse to nonzero null k. Its intersection C with the cone is a spacelike two-surface. The restricted covector beta_S is a nonzero conormal of C in S, hence locally a(y)d rho. The prescribed initial data phi=a(y)rho+rho^2 b(rho,y) have the required first jet for any smooth b. Shrinking where needed keeps d_S phi nonzero. No hidden cross-label integrability condition is needed: the tangential restriction of that first jet vanishes on TC, exactly as required for phi|C=0.

The future null completion has the correct sign for signature (-+++):

```text
P=Q+|Q|_h n_S-flat,
P-sharp=Q-sharp+|Q|_h n_S.
```

Its norm is zero and its normal component is positive future. For a fixed nonzero tangential Q there are two null completions, one future and one past; the stated future completion is unique. Thus it agrees with the full beta on C, not only a vanishing pullback. No normalization factor is introduced.

### Section 3: local projection and canonical exactness

For lambda=P_a dx^a and H=g^{ab}P_aP_b/2, the candidate's Hamilton equations give

```text
i_XH d lambda=-dH,
lambda(XH)=2H,
L_XH lambda=dH.
```

These signs are consistent. They can be checked directly from d lambda=dP_a wedge dx^a: contraction gives dot P_a dx^a-dot x^a dP_a=-dH. Cartan's identity then yields the displayed Lie derivative.

At flow time zero, the base-projection derivative spans TS plus P-sharp. The latter is transverse to S, so the derivative is invertible. The inverse-function theorem supplies a diffeomorphic local projected flow neighborhood. The candidate appropriately restricts to this local neighborhood and does not assume a global Cauchy surface, arbitrary finite-patch lifetime, or global absence of characteristic crossing.

Exactness is not merely inferred from a geodesic congruence. On the initial graph, lambda pulls back to d_S phi. Along the Hamilton flow, H is identically zero, so the derivative of the fixed-time pulled-back one-form is d(H composed with G_s)=0. Its flow-time component is lambda(XH)=2H=0. Therefore on the full four-dimensional parameter domain G-star lambda=d(phi(x)). Invertibility of the base projection then gives dTheta=P. The proof establishes an exact null differential on an ambient open set. Smooth local ODE and inverse-function hypotheses suffice; analyticity or an unjustified characteristic initial-value theorem on N is not being assumed.

### Section 4: exact normalization on the retained cone

On C, the full initial covector is exactly k-flat. The G349 lifted generator solves the same affine Hamilton/geodesic ODE. Local uniqueness with that same initial covector fixes the same parameter normalization and propagates equality along the short cone flow tube. Phi vanishes on C and H=0 along its characteristics, so Theta also vanishes along the tube. This addresses the necessary extension from the initial two-surface to a three-dimensional cone patch.

The affine necessity argument is correct: for K=(dTheta)-sharp with null norm on an ambient open set, Hessian symmetry gives nabla_K K=(1/2)d(g(K,K))=0. A nonaffine rescaling can therefore obstruct fixed-covector matching. G349 already supplies affine k, and the proof does not rescale it. The prohibition against substituting a pullback equality for ambient equality is mathematically essential and consistently maintained.

### Sections 5–6: freedom and readout dependence

The free initial remainder and normalized nonlinear reparameterizations establish nonuniqueness. The candidate does not claim that all extensions differ only by reparameterization. Its shifted-cone implicit example is valid on the stated local domain R>0,D>0 and genuinely changes nearby level surfaces. An independent reconstruction is given below.

For two extensions with equal full covectors at every relevant original-cut point, omega_i=-dTheta(u_i)=-g(k,u_i) is identical for every fixed supplied observer. Fixed metric and cut maps fix J_i; fixed mu fixes the absolutely continuous label density s; fixed positive spacing fixes the remaining scalar factor. Thus absolute Gamma_i agrees almost everywhere on the regular absolutely continuous part. On nonzero support, both give Gamma_j/Gamma_i=R_ji/A_ji. Weighted pushforwards also agree for the same maps, weights, and measure; the stated integrability condition remains necessary for finiteness.

There is no hidden derivation of product factorization here. The candidate explicitly retains G352's chosen continuous product, supplied cross-phase label identification, and fixed phase-independent measure conditions. It also excludes singular ordinary-density claims, ratios at zero density, and off-cone or finite-worldline predictions. Theta|N=0 is consistent with positive observer frequency because timelike observers are transverse to the null hypersurface. The proof does not confuse propagation along k with phase variation along an observer.

The distinction between mathematical source normalization and operational phase/frequency units is explicit in sections 1 and 7 and in the README/work order. No physical dimensionless phase or calibration is derived by assigning a scalar the geometric normalization of k. The readout comparison is conditional on the same normalization and spacing, as required.

## 3. Independent recomputation of the distinct-foliation witness

The candidate differentiates an implicit function. I instead parametrized its Cartesian embedding and reconstructed the metric-dual gradient. Let

```text
L=1+v^2+w^2,
m=(2v,1-v^2-w^2,2w)/L,
X(c,R,v,w)=(t=R-c, spatial=a c^2 e_x+R m),
D=1+2 a c m_x.
```

Exact differentiation of this explicit map gives

```text
det(dX)=4 R^2 D/L^2,
g_Rc=D,        g_RR=g_Rv=g_Rw=0.
```

On R>0,D>0 the map is locally invertible. Direct metric duality then gives grad(c)=D^-1 partial_R in these coordinates, whose Cartesian vector is (1,m)/D. It is null and future; at c=0 it is exactly (1,m), the prescribed outgoing cone tangent. This uses the embedding and pullback metric, not the candidate's implicit differentiation formula or stored output.

At a=1,c=1/10,R=1,v=w=0, the point is (9/10,1/100,1,0), and the covector is (-1,0,1,0). The base-cone covector is (-1,1/sqrt(10001),100/sqrt(10001),0). Their time-x normal wedge is -1/sqrt(10001), exactly nonzero. The same construction with c tending to zero gives such discrepancies arbitrarily near the original cone. Hence the nearby foliation changes; it is not only a scalar relabeling of the original foliation.

The independently authored stage_b_parametric_witness.py uses exact SymPy arithmetic and no candidate imports or saved-output inputs. Python 3.10.12 and SymPy 1.13.1 were observed. Its initial run failed at a structural matrix equality: algebraically equivalent rational expressions had different expression trees. The initial script and empty stdout/error traceback were preserved under their INITIAL filenames. The checker-only repair compares the simplified component differences; all four are exactly zero. The repaired run exited 0 in approximately 0.48 seconds. No candidate formula, theorem hypothesis, parameter, or tolerance changed. This failure/repair is reviewer test history, not a candidate defect or an omitted failed scientific result.

This exact witness strengthens the check of section 5 and its local invertibility domain. It is not evidence for arbitrary-metric existence, which rests on the reviewed analytic argument.

## 4. Replay, false-pass scrutiny, and operational caveat

The original check code was inspected before replay. The initial-jet tests, null completion, implicit gradient, ambient normalization, affine/nonaffine controls, finite cut Gram matrix, and observer contractions are finite exact checks, not a proof of the general construction. The selected counterexample rejection calls are nonvacuous on their actual fixed-dimensional inputs. The saved-input rational recomputation uses its own Cartesian Gram and observer contractions and does not import the symbolic checker or use saved outputs as calculation inputs. It shares the mathematical witness, so implementation separation is not independent theorem proof.

The live capture runner reproduced the exact saved baseline JSON, including its 53 assertions. Each registered mutation exited 1 at the intended assertion, with empty stdout and the expected AssertionError:

| Mutation | Actual terminal assertion |
|---|---|
| acceleration_zero | nonaffine_nonzero_component |
| pullback_only | matching_rejects_hidden_factor_two |
| omit_frequency | absolute_rate_second_cut |
| area_radius | metric_area_not_radius |

The baseline child took about 0.37 seconds; mutation children about 0.32–0.38 seconds; the runner about 1.82 seconds. The saved rational recomputation exited 0 in about 0.02 seconds and reproduced Jacobians 9,25; frequencies 1,2/3; rates 14/135,28/1125; and ratio 6/25. Every child was inspected by the review wrapper for the expected return code and exact terminal assertion, rather than accepting the runner's outer exit status.

**C1 — capture-runner exit status is not an aggregate verdict.** run_checks.py records subprocess outcomes and always proceeds to printing the capture when no subprocess timeout/launch exception interrupts it. It does not assert baseline success or mutant rejection. To demonstrate the implication, I executed the unchanged original runner source with only its __file__ directory redirected to a scratch helper. That deliberately defective helper failed the baseline and allowed all four mutant invocations to exit 0. The runner nevertheless exited 0 and accurately recorded those outcomes. The full record and helper are preserved in STAGE_B_CAPTURE_ONLY_PROBE.json, its stderr file, stage_b_capture_runner_probe.py, and runner_probe/check_exact.py.

This is a real false-pass route **if an operator treats runner exit 0 as overall verification**. It is not a failure of the runner's stated capture-only contract, not a defect in the actual saved/replayed results, and not a mathematical counterexample. No frozen code change is required to sustain this review's conclusion. The smallest optional source-preserving operational clarification in current usage/status documentation is:

> run_checks.py is capture-only: exit 0 means capture completed, not that the checks passed. Verify baseline exit 0 with the expected result, and each mutant's exit 1 at its intended AssertionError; an unrelated exception or timeout is not a successful defect catch.

An enforcing wrapper is an alternative future workflow choice, not required scientific repair in this bounded review. Its correctness should not be inferred from the present capture runner. The review's own wrapper explicitly checks the stated child conditions and preserves their raw streams.

## 5. Commands, resources, and preserved evidence

All authored or probe files and runtime outputs were confined to `/tmp/udt-cone-review-0WvbvE/`. All candidate and accepted-source reads were read-only. No Git mutation, new agent, GPU, production process, archive/disk operation, or protected-payload operation was performed. Children ran sequentially, with at most 60 seconds permitted per check, exact algebra only, no numerical tolerance or grid. Peak memory was not measured; the objects are small symbolic matrices/rationals and no memory certification is claimed.

Principal exact commands, from repository root:

```text
timeout 60s python3 /tmp/udt-cone-review-0WvbvE/stage_b_authenticate_and_replay.py > /tmp/udt-cone-review-0WvbvE/STAGE_B_REPLAY_SUMMARY.json 2> /tmp/udt-cone-review-0WvbvE/STAGE_B_REPLAY_STDERR.txt
timeout 60s python3 /tmp/udt-cone-review-0WvbvE/stage_b_parametric_witness.py > /tmp/udt-cone-review-0WvbvE/STAGE_B_PARAMETRIC_RESULT.json 2> /tmp/udt-cone-review-0WvbvE/STAGE_B_PARAMETRIC_STDERR.txt
timeout 60s python3 /tmp/udt-cone-review-0WvbvE/stage_b_capture_runner_probe.py > /tmp/udt-cone-review-0WvbvE/STAGE_B_CAPTURE_ONLY_PROBE.json 2> /tmp/udt-cone-review-0WvbvE/STAGE_B_CAPTURE_ONLY_PROBE_STDERR.txt
sha256sum -c udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/ARTIFACT_SHA256SUMS > /tmp/udt-cone-review-0WvbvE/STAGE_B_FINAL_PACKAGE_HASH_CHECK.txt
```

The parametric command was run before and after the documented checker repair. The initial files were preserved before rerun. The authentication/replay script records every child command, working directory, return code, elapsed time, stdout, and stderr in STAGE_B_CAPTURE_RUNNER.json and STAGE_B_SAVED_RECOMPUTATION.json. Its source specifies each sequential read-only `git show` authentication against both snapshots. STAGE_B_AUTHENTICATION.json contains every compared source/payload hash.

No full G349/G351/G352 production or repository suite was replayed. No global phase theorem, arbitrary nonlinear phase-gauge invariance, physical realization, observational law, source measure selection, or broader test census was attempted. Their omission matches the bounded mathematical question. Backup completeness and pre-reboot unsaved-state disposition remain **UNVERIFIED**. Remote freshness, externally trusted chronology, and different-model independence are not claimed by this reviewer.

## 6. Handoff and exact surviving conclusion

For each admitted regular point, the candidate validly constructs a local smooth null scalar matching the full already prescribed affine G349 covector, with no rescaling. The continuation is not unique and can alter neighboring foliations. With original cut maps, observers, finite label measure, positive common spacing, and G352's chosen product conditions fixed within a common extension domain, those extension choices do not alter original-cut local readouts. This is conditional local geometry and readout dependence, not physical phase/content realization.

There is no substantive repair request. C1 is an operational usage caveat with a concrete optional clarification; the original capture data, proof, source bytes, and mathematical conclusion survive it. This completes the authorized adversarial examination of the frozen original candidate. Any later documentation-only status clarification can receive focused fidelity review without reopening the mathematical construction, unless its wording changes a premise, quantifier, or scientific claim. Scientific promotion and owner decisions remain with Charles and the parent workflow.
