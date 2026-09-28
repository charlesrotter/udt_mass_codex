# FCV1 direct adversarial review

**VERIFIED-WITH-CAVEATS, conditional and unpromoted. No load-bearing defect or
required scientific repair found. Zero of the two permitted repair rounds used.**

Reviewer `/root/fcv1_review`, 2026-09-28. Candidate SHA256
`ed65323a439e1d509bc0241c6550a5485e3f1a496b06b6ab01eb34692443d1d4`.
All CANDIDATE_FREEZE.json entries and all source-first source pins were checked
against actual bytes. SOURCE_FIRST.md was sealed and reported before candidate
exposure. This verdict concerns the frozen conditional argument, not physical
adoption, source-grade promotion or canon. Final summaries/pointers have not yet
been reviewed. The full premise audit and parent operational closure are separate.

## Independence and exposure

| Axis | Actual record |
|---|---|
| Context | Separate reviewer context from the author; parent startup is attributed, branch/hash/status independently checked. |
| Model | Exact runtime model not exposed beyond Codex/GPT-6-family wording. Different-model review UNTESTED. |
| Argument | Source-first reconstruction from G220/FSL1, RMS1 and G310/current G312; dispatch exposed intended world-function route and interior-test idea. No independent origination claim for those ideas. |
| Implementation | Independent reviewer code with no producer imports; same Python/SymPy libraries. Later producer replay is regression only. |
| Prior verdict exposure | Prior source-package reviewed results were read. No new FCV1 proof, code or result before source-first seal. |
| Direct stage | Read frozen candidate and freeze, constructed and sealed additional controls, then read producer code/results and replayed them. |

The source-first record contains 18 exact checks (14 identities and four wrong
simplifications rejected). Before producer-code exposure, a further 12 checks
(nine identities and three wrong simplifications) were independently constructed.
DIRECT_INDEPENDENT_SEAL.json records that exposure boundary. The same nonlinear
inverse map appears in both producer and reviewer work, independently constructed
before code exposure; this does not imply different mathematical methods for that
particular control. Human, different-library and formal-proof review are absent.

## Argument audit

1. **Domain and metric variation.** A smooth geodesic branch with the stated
   nondegeneracy and commuting derivatives suffices. The world-function energy
   formula on affine [0,1] fixes the scale, including its factor one half.
   Integration by parts removes the affine geodesic Euler-Lagrange term while
   retaining endpoint motion. Nullness does not justify setting this variation
   to zero. The signs in J=I-g(k_e,W_e)+g(k_o,W_o), F_t=-N_o omega_o and
   V=J/(N_o omega_o) are correct.
2. **Full clock formula.** The proper-rate derivative is
   b=-h(u,u)/2-g(u,nabla_u W). Applying the product/chain rule to
   Z=N_o(A)A'/N_e gives equation(4), including both V' and receiver-rate drift.
   Equation(5) is valid when both baseline labels are proper time along their
   entire relevant curves, as stated. It does not hold if one merely normalizes
   the tangent at a single event and then drops nonzero lapse drift.
3. **Proper-time anchoring.** Equation(6) follows by differentiating the clock
   integral at a declared common origin. If source proper-time parametrization
   is instead maintained separately throughout the metric family, its movement
   belongs inside W_e; equation(6) must not be added a second time. The candidate
   treats these as explicit alternative protocols and does not double count.
4. **Covariance.** For h=L_xi g, W=-xi the null integral becomes the exact
   affine boundary term, J cancels and each b vanishes. Metric-only pullback at
   fixed coordinate curves represents a changed query, so its nonzero answer is
   not a failed gauge test. Nothing here supplies a metric-only divergence law.
5. **Inverse and composition.** Equation(7) has the necessary D'V/A' term at
   fixed receiver label. At the moving paired argument the inverse log-response
   is -Q. These are identities for any regular increasing incidence map; causal
   return is a separate query. The composition claim is the ordinary chain rule
   with the intermediate arrival and ray retained, not an omitted field law.
6. **Reciprocal witness.** The trace-free tangent really is t b(x) times G310's
   full factor-two H. The determinant is exactly -1. With smooth compact interior
   b, the endpoint neighborhoods and every endpoint metric jet remain unchanged.
   The ambient central null curve is a pregeodesic: the metric has no transverse
   derivatives on the tube, and in its two-dimensional Lorentz block a null
   curve's acceleration is parallel to its null tangent. Affine reparametrization
   therefore exists. Smooth small-family dependence about a finite flat segment
   supplies the selected regular branch; no global uniqueness is inferred.
   Both geodesic action variation and the null ODE give Q=2 integral b>0.
7. **Support argument.** A smooth compact perturbation disjoint from the compact
   baseline ray has positive separation from it, so sufficiently nearby label
   rays also miss its support. Thus differentiating in source label does not
   invalidate Q[h]=0. The sensitivity is supported on the ray and endpoints.
   If one smooth volume coefficient represented this nonzero functional for all
   compact h, its restriction off the ray would vanish by local testing and
   smoothness would force it to vanish on the ray too. The trace-free version
   follows by testing arbitrary trace-free h off the ray and using the trace-free
   compact witness. This establishes the section7 result on the displayed query;
   it is not an obstruction to a local field equation with nonlocal observables.

The general proof keeps arbitrary symmetric metric perturbations and worldline
motion in four dimensions. It does not claim that one ray detects every metric
component. Restricted examples support the claimed counterexample quantifiers;
they do not characterize all comparisons or physically admitted UDT solutions.

## Independent controls and producer replay

The initial source-first controls already checked a nonreciprocal interior metric
change, gauge cancellation, inverse argument movement, conformal clocks and the
fixed-label/proper-time distinction. The direct-stage independent controls add:

- Reciprocal family with L=3/2 and polynomial b=x^3(3/2-x)^3:
  B0=2187/17920, B1=6561/71680 and Q=2187/8960. The geodesic integral and
  independently formed null-ODE derivative agree; dropping G310's factor two
  fails. This is explicitly a polynomial algebra control, not the compact-bump
  endpoint-jet proof.
- A physically displaced Minkowski receiver
  z_o^epsilon(t)=(t,L+v t+epsilon a t^2). The incidence formula gives
  A=(s+L)/(1-v), V=a A^2/(1-v), b_o=-2avA/(1-v^2), hence
  Q=2aA/(1-v^2). Direct differentiation of the original Doppler ratio gives the
  same expression. At v=3/5,L=7/4,a=2/7,s=5/6, A=155/24 and Q=3875/672.
  Omitting either receiver clock normalization or arrival-slope variation fails.

The additional 12 checks passed in 0.237 seconds with 46,156 KiB peak RSS.
The later producer replay reproduced all 29 author identities and eight wrong
formulas rejected; its stdout is byte-identical to the frozen author stdout.
It ran in 0.542 seconds with 51,496 KiB peak RSS. Each captured run used one CPU
process, thread controls one, 60-second CPU/wall limits and 512 MiB address space.
Commands, stdout/stderr, resource records and hashes are preserved. These wrong
formula comparisons are finite diagnostic controls, not a mutation-coverage
theorem or proof of the generic result. Producer replay is not independence.

## Defect/survivor/repair assessment and limits

No load-bearing defect was found in the candidate. The attempted stronger
identification is rejected for the reasons the candidate gives: the derivative
of inverse/composition reciprocity is a universal identity, whereas the nonzero
single-measurement derivative is a query-dependent ray-supported functional.
Neither is identified with the specified physical local symmetric E constrained
by adopted DDR. The strongest survivor is the exact conditional observable
variation together with this precisely scoped failed direct join.

No scientific repair is required. The smallest permissible response to the
unclosed physical join is to retain it OPEN, as the candidate does. Supplying a
new averaging prescription, stationarity principle, field action or preferred
population would be a new task/premise, not an algebra repair. This review does
not assert that such additions are necessary or that another existing route
cannot work.

No microscopic light validation, observational confirmation, global/asymptotic
completion, caustic analysis, finite-perturbation error bound, nonlinear
stability, native UDT solution admission, source/matter physics or metric
reconstruction theorem is provided. Current G310/G312 grades remain controlling;
the examples do not become native cosmologies. Source mathematics was not
broadly re-proved, and the cited external method-credit paper was not independently
audited; all load-bearing formulas were explicitly derived here/from G220.
Full premise/packaging/startup preservation and final pointer fidelity remain
separate closure checks. Review supplies no adoption authority.
