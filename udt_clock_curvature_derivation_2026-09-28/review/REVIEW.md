# CRD1 independent adversarial review

Verdict: **VERIFIED-WITH-CAVEATS**, confined to the conditional geometric
construction and stated closure boundary. No load-bearing algebraic defect was
found. Equations (2)-(6) and (9)-(10) survive independent argument and the exact
checks below. This does not establish a native UDT field equation, physical
observer/query population, complete response-class membership, or canon.

Reviewer: `/root/crd_review`, separate context, 2026-09-28. Exact initial
candidate pins independently checked:

* `INITIAL_DERIVATION.md`:
  `e896d9e7044ed936c82c4c2d5f83a97bf00f8a6732997c0d57e0442413324201`.
* `INITIAL_LAY_BRIEF.md`:
  `fdb5c5448f81c020df644b68e095210e829fde46ffacce958310e181368e33b2`.

The 27-file construction manifest and source-first seal are verified separately
in the review integrity record. Checksums establish correspondence, not truth.

## Argument and hypothesis review

The supplied regular pair has three retained functions N,L,b. The source-first
review independently derived `K=R[h]/2=u(H)+H^2-n(a)-a^2`, with
`a=[N_x-(Nb)_t]/(NL)` and `H=L_t/(NL)`, before seeing the candidate.
The candidate's convention `T_h=-K` matches. Its connection, frame commutator,
and both null nonaffinity equations follow directly from that geometry. Expanding
`B_+=H+a`, `B_-=H-a` proves (4), without commuting u and n or identifying
directional rates at different events. The frequency equation follows from an
affine geodesic and its contraction with the specified unit observer.

G176 contributes the WORKING completed-pair calibration, not a response law.
`Phi=-log N`, `M=log(NL)` imply `a=-n(Phi)-b_t/L` and `H=u(Phi+M)`.
These substitutions give (5), preserving all functions. Treating `m dx` as
an exact coordinate differential with unchanged time/observer requires `m_t=0`;
the candidate correctly states this restriction. Intrinsic lapse depth, terminal
comparison-clock depth, and integrated received-clock depth are kept distinct.
In particular, (4) does not assert a single endpoint scalar reproducing every
null comparison. G402's additional integrability conditions are not bypassed.

Under the explicitly additional restriction `b=0,m=1`, direct coordinate
curvature gives `R[h]=F_tt-(F^-1)_ss`, `F>0`. If the curvature is a prescribed
derivative-free forcing, the principal matrix is `diag(1,F^-2)`, positive
definite. Therefore it is not a standalone hyperbolic scalar Cauchy evolution.
**This does not rule out the equation's role as a constraint inside a larger
system.** A derivative-dependent closing law may change its principal type;
computing the curvature from F itself makes the equation an identity. The
cosh mode is a linearized principal-type control, not nonlinear instability
or a conclusion about causal UDT dynamics. These limits should accompany the
final lay return; they preserve the initial result rather than repair its science.

The Gauss sign and ambient-versus-induced distinction are correct. The supplied
flat-ambient immersion has `II(u,u)=X`, `II(n,n)=-X`, `II(u,n)=0`, so both
null normal accelerations vanish while the extrinsic tide correction remains
-1. It refutes the inference that both intrinsic null directions being ambient
geodesics makes pair and ambient sectional curvature equal. Its free unit
scale is only a control, not a physical scale, center, or X_max input.

The optical sentence has the correct sign. For an affine null k and a connecting
Jacobi field J with `[k,J]=0`, Ricci commutation gives
`nabla_k^2 J=R(k,J)k=-R(J,k)k`. Thus `D''=-O D` applies to **transverse Jacobi
data in the parallel screen quotient** with
`O_AB=g(e_A,R(e_B,k)k)`. It is not the equation for an arbitrary unconstrained
four-component Jacobi matrix. This standard hypothesis should be explicit in
the final text. The statement adds no optical population or physical ownership.

For (9), write `M^a_b=nabla_b U^a`. Commutation gives

```
U^c nabla_c M^a_b
 = nabla_b A^a - (nabla_b U^c)(nabla_c U^a)
   + U^c R^a_dcb U^d
 = nabla_b A^a - M^a_c M^c_b - T^a_b.
```

This proves the stated identity for the declared curvature convention, with no
field equation. For affine k, metric compatibility and `nabla_k k=0` likewise
give (10). Supplied observer acceleration/deformation and legitimate initial or
query data need not be promoted to independent physical fields or ruled out as
failures of uniqueness.

The scientific stop is supported by the exact current authority, independently
of these checks. DDR is owner-adopted provisional and gives `TF(E)=0` on its
registered domain. Neither the pair curvature nor the observer-dependent tidal
operator is thereby identified with the natural metric-only response E.
Current G312 leaves the response-class membership route unclosed under GR as a
filter. The ENTIRE G301 conditional class plus `a!=0` still gives trace-free
Ricci and constant regional scalar curvature by Bianchi. The candidate does
not silently adopt this class, deny legitimate data, or infer that an independent
closure is impossible or a new physical premise is necessary.

## Independent checks and preserved failure

All arithmetic below is exact; no numerical tolerance or empirical fit was used.

* Source-first `source_first_coordinate_check.py`: generic original-coordinate
  2x2 Christoffel/Ricci scalar, exact `R_coordinate-2K=0`; calibration identities
  pass. Approximately 0.71 seconds, 49,196 KiB RSS.
* `direct_pair_check.py`: generic bidirectional interlock; all four components
  of the two null nonaffinity equations; original-curvature reciprocal F
  restriction; its linearized principal part. Actual wrong-formula rejections:
  omit shift time derivative, omit changing tape measure, and use the hyperbolic
  linearized sign. Approximately 0.97 seconds, 50,124 KiB RSS.
* `direct_ambient_check.py`: attempted generic multivariate rational symbolic
  simplification reached the 1.5 GiB address-space limit at the residual
  cancellation stage. Exit 1, `MemoryError`, 38.23 seconds, 1,562,596 KiB RSS.
  Initial code and all failure outputs are preserved. No symbolic 4D success
  or scientific failure is inferred from this computational resource limit.
* Bounded replacement `direct_ambient_point_check.py`: a distinct metric
  `g=rho^2 eta`, `rho=1+t+xy+z^2`, and a spacetime-dependent rationally
  normalized boosted observer with `p=(t+2x+3y+5z)/20`. All 16 components of
  (9) are exactly zero at each of three declared rational points; all 16 tide
  components are nonzero there. Unit-observer, future-null and frequency
  transport checks pass. Reversing the tidal sign and dropping `M^2` each
  actually fail at every point. The immersion metric and II are also computed
  symbolically. Approximately 2.67 seconds, 51,728 KiB RSS. These finite jets
  check implementation; the general commutation argument supplies the theorem.

Python 3.10.12 and SymPy 1.13.1. Each captured calculation used one process,
single-thread environment and a 300-second/1,536-MiB cap. No GPU or mesh.
The distinct four-metric and observer were selected before reading the author's
scientific implementations. Captures retain exact commands, stdout/stderr,
versions, parameters, shapes and resource records.

Author scripts, check plan and retained hyperbolic normal-form repair were read
only after these independent runs completed. Their real wrong-formula tests
were inspected; no evidence of vacuous comparison was found in this scope.
Their scripts were not replayed here because the independent load-bearing
checks were complete. The parent full premise audit was not duplicated:
its actual captured record and output were inspected, exit 0, 407.520 seconds,
120,192 KiB RSS, with the 406-row guard pass. Exact selected current registry
rows were then read; no scientific source regrading was inferred.

## Exposure and independence limits

The sealed source-first note was written at 14:23:35 UTC without parent
candidate, scientific code/results, CGW1 synthesis, or CRD1 verdict exposure.
It saw the assigned target, work order, current premise summary, G176/G220/G310
sources, G310 adoption and G312 authority, and method protocols. Source hashes
and runtime identity are in `SOURCE_FIRST_SOURCES.sha256` and
`SOURCE_FIRST_EXPOSURE.json`.

The direct stage saw the frozen candidate and lay brief, parent's author-test
summary and targeted interpretation questions. Before the direct-stage candidate
read, a `list_agents` status query incidentally displayed brief completed CGW
agent summaries. No CGW synthesis, proof, code or outputs were opened or used.
This incidental exposure occurred after the source-first seal. It does not
justify calling the entire direct stage blind.

The runtime describes Codex based on GPT-6; no exact model revision is exposed
and no different-model independence is claimed. Fresh context, source-first
argument and separately authored coordinate implementation are real distinct
axes. Formal proof, different-model review, human specialist review, full source
package replay and generic four-dimensional symbolic cancellation are UNTESTED.

One output-label caveat: importing the unchanged source-first helper caused
`direct_pair_check.stdout` to include that helper's original
`candidate_exposure:false` label. It describes the helper's source-first origin,
not the direct-stage session, which had read the candidate. The present exposure
record controls that interpretation; the two stages are not conflated.

No source, protected payload, author evidence, registry, CANON or unrelated file
was modified. This review wrote only `review/`; no staging or commit was done.
The two clarity qualifications above are the only recommended final-text changes.
They do not widen the theorem or grant scientific acceptance.
