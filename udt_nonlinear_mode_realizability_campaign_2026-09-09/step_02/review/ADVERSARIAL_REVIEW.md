# NR2 adversarial review — VERIFIED-WITH-CAVEATS

Mathematical verdict recorded 2026-09-09. UNPROMOTED conditional
candidate review; no banking, physical adoption, canon or full-integration claim.

The frozen NR2 iff statement survives. On each supplied registered compact
G324 split-lattice quotient and each T0>0, precisely the G327 eight-parameter
first variations satisfying

    Q = v_c dot u_s - v_s dot u_c = 0

are tangents, modulo legal periodic gauge, to the declared exact local families.
Necessity is NR1 at its reviewed mixed-C2 scope. Sufficiency constructs actual
jointly analytic spacetime/parameter families on a common neighborhood of the
whole compact slice. This classifies realizable tangents in this sector only;
it does not classify all nonlinear solutions or their physical realization.

No load-bearing defect was found. No candidate scientific repair is required.
The caveats below are part of the verdict, including method, independence,
chronology, source-review and full365 limitations.

## Snapshot, exact objects and exposure

Initial baseline personally verified: c9eeab5183d2aad62fb4ebb923f8eae962c0c6f3,
branch grok. Parent owns synchronization. During review the parent preserved
the frozen candidate at 31277b8dd201d2a8745324ba72fac6a6a2bec883; that exact
HEAD and the matching local origin/grok reference were personally checked.
All thirteen initial-candidate-manifest pins matched before direct review and
again after that checkpoint. All nine original source-manifest pins matched.
The full source packages were not re-proved or replayed by this reviewer.

| Frozen object | SHA-256 |
|---|---|
| INITIAL_CANDIDATE.md | 2af7b57e9323c895ffe98b4777aadd37721cd650bffd684954b85b1441e29e9d |
| check_nr2.py | 00468b6e96ff66056b5c012522f2a6f34a3c3179a9bc472f75b96c207eb46817 |
| review/STAGE_A_INDEPENDENT.md | 79a2179475659e853d2a16ab53e1e9bd6b039691a660028551ee11a165385620 |
| review/independent_coordinate_check.py | cadf8cd693e53570bd99b7f2cdb9d10dc90235948c04fe1167fed71323cb2590 |
| review/independent_evolution_interface.py | d0be2e7e10099846cfe73a7a8bb0867732beac043d3d590686fb2521fb8355c9 |

Reviewer is the actual separate `/root/nr2_review` context, exact model UNKNOWN.
Source-first Stage A and both independent implementations/runs were completed
before the parent's 16:23:49 UTC freeze announcement and before reading its
NR2 proof or code. The campaign log/dispatch already disclosed the intended
constraint completion and CK routes, and the complete NR1 review was read:
this is source-first, not hypothesis-blind. The NR1 reviewer right inverse is
not used as a proof input.

The source-first constraint argument and code are independently developed;
there are no candidate-code imports. However, the reviewer's independently
chosen upper-half-plane chart is the candidate chart after the coordinate
rescaling v=2c. This is **not a different chart method**. Both three-dimensional
codes use ordinary Levi-Civita reconstruction and SymPy 1.13.1, so shared
method/library risk remains. The separate four-dimensional rational metric-jet
and full covariant-divergence calculation adds a distinct implementation route
for the evolution and constraint-propagation interface. Different-model, human,
formal-proof and independent-library review are not established.

## Argument audit

1. **The exact initial metric and shape variables are valid.** The chart has
   determinant one and positive leading minor exp(2u), hence is positive
   definite for every real u,v. Its two shape matrices are traceless and
   self-adjoint in M. Thus K is an actual symmetric tensor. The dual coordinate
   weighting in V makes tr((M^-1 M')V) exactly twice p_u u'+p_v v', not just
   to quadratic order. This avoids an unproved higher-order correction to the
   global momentum integral. The independent coordinate calculation recovers
   the candidate curvature, all three momenta and Hamiltonian identically.

2. **The global condition is exactly Q=0.** Direct whole-period integration
   of p f'+r w' gives k LX Q/2. On this supplied split quotient, zero integral
   is necessary and sufficient for its periodic primitive. The fixed origin
   of that primitive supplies a coordinate convention; changing it shifts the
   freely allowed mean. With s=s0+epsilon^2 Psi+c(epsilon), the full axial
   momentum equation vanishes pointwise. No separate polarization condition
   is introduced. The explicitly balanced two-polarization datum has nonzero
   individual contributions that cancel. No amplitude is divided out, so the
   degenerate and zero-amplitude cases are covered.

3. **Hamiltonian completion and higher-order freedom are real.** The axial
   mixed-K coefficient kappa solves the actual H=2Lambda equation because
   s0=-2/(3T0) is nonzero. Compactness and small epsilon keep the denominator
   away from zero for any fixed supplied tangent and fixed analytic c,Lambda.
   Arbitrary analytic c=O(epsilon^2) and Lambda=O(epsilon^2) leave all first
   Cauchy data unchanged; the review explicitly recomputed that fact for
   arbitrary analytic tails, not only quadratic polynomials. These freedoms
   change the nonlinear data. Lambda stays spacetime constant for each family
   member. Chart nonlinearities and kappa generate higher harmonics and mean
   corrections; the exact family was not frozen to the linear tensor form.
   The construction is an existential witness, not a census of completions.

4. **The full inherited tangent matches.** At epsilon=0 the metric and K are
   the supplied Taub/Kasner data. Differentiating the full covariant K, including
   the metric used to lower its first index, gives

       delta gamma_AB = 2 b^2 H,
       delta K_AB = -b^2(Hdot+4H/(3T0)),
       delta gamma_XX = delta K_XX = delta gamma_XA = delta K_XA = 0.

   Thus both the field and its Gaussian normal derivative match G327. A mere
   spatial-metric match would have been insufficient. Lambda'(0)=0 is required
   by the declared tangent's delta R=0; no condition is imposed on its higher
   analytic derivatives. The smooth periodic gauge quotient inherits NR1's
   argument: parameter-dependent periodic flows remove an infinitesimal gauge
   term on a smaller common neighborhood. Nonperiodic rescalings or an extra
   first-order mode would change the problem.

5. **The analytic evolution is a legitimate CK system.** Direct Gaussian
   geometry, with K=-gamma_t/2, gives

       Ric_ij = Ric3_ij-K_ij,t+tau K_ij-2(K gamma^-1 K)_ij.

   Hence the six spatial equations yield the candidate's evolution, including
   -Lambda gamma in K_t. Its highest pure time coefficient is invertible.
   Introduce auxiliary A_kij=partial_k gamma_ij to reduce spatial order:
   A_kij,t=-2 partial_k K_ij. The defect A_kij-partial_k gamma_ij therefore has
   zero time derivative and zero initial value. Auxiliary variables remain
   actual spatial derivatives; the reduction introduces no spurious solution.
   Positive gamma makes coefficients analytic, and the coefficient of the
   first time derivative in the enlarged system is the identity. Epsilon is
   an additional mathematical variable with no epsilon derivative in the PDE,
   so the noncharacteristic theorem gives joint analytic dependence. This is
   an existence argument in an analytic subclass, not smooth continuous
   dependence, a Sobolev well-posedness theorem or stability.

6. **All original equations are recovered.** Under spatial evolution, direct
   general Gaussian identities give E_00=H-2Lambda and E_0i=-M_i for
   E=Ric-Lambda g. Thus exact initial constraints give E_00=E_0i=0. Write
   C=E_00, D_i=E_0i and F=E-(tr E)g/2. Since Lambda is spacetime constant,
   contracted Bianchi gives, including all lower-order terms,

       C_t = 2 div_gamma(D^sharp)+2 tau C,
       D_i,t = (1/2)partial_i C+tau D_i.

   One can verify this directly from F_00=C/2, F_0i=D_i and F_ij=C gamma_ij/2.
   The first-order system is homogeneous analytic and noncharacteristic in
   time, so zero data have the unique zero solution. No truncated tensor
   evolution is substituted for full Ricci. The independent full-coordinate
   generic-jet calculation checks signs, factors, every spatial component,
   and this covariant divergence with nonzero spatial connections.

7. **Common compact development and full spacetime tangent follow.** Initial
   data and the constant coframe descend under the supplied translations.
   Analytic uniqueness identifies local overlapping germs and deck translates.
   A finite initial-slice chart cover, with a smaller closed epsilon interval
   inside the analytic data neighborhood, supplies a common positive time
   interval. Shrinking preserves positivity and Lorentzian signature. No
   bound uniform over all amplitudes or near either singular/infinite endpoint
   is claimed. The background and its G327 derivative solve the respective
   analytic evolution problems with the same complete data. CK uniqueness
   for the background and differentiated linearized system identifies the
   family derivative with the complete G327 spacetime mode on this slab.

The mathematical method sources were personally opened: the analytic reduction
and Bianchi discussion in [Choquet-Bruhat, arXiv:1410.3490v1, sections 2--3](https://arxiv.org/pdf/1410.3490),
and the analytic coefficient/data, noncharacteristic and local uniqueness
statement in [the academic PDE notes, Theorem 4.1 and system (4.1), printed pages 38--40](https://www2.math.upenn.edu/~qze/notes/pde2.pdf).
The full general CK theorem is imported mathematics, not re-proved here.
The candidate-specific reduction, auxiliary consistency, parameter construction,
compact gluing and constraint propagation above are checked applications.

## Independent recomputation and guard audit

The pre-exposure coordinate run executed 15 predicates and rejected six actual
formula corruptions. It independently reconstructed all spatial geometry,
exact cotangent pairing, full gamma/K tangent, whole-period integral and the
two-polarization cancellation. The pre-exposure evolution run executed 11
predicates and rejected four additional corruptions. It uses a positive
non-diagonal rational metric and nonzero generic first/second spatial and time
jets. Its unconstrained test residuals are explicitly nonzero:

    H = -15744513949/62737594920,
    M = (-40099/980980, -617/226380, 152387/1471470).

These prevent its Ric00/H and Ric0i/M comparisons from being zero-against-zero
checks. All six independent pure second-time metric directions give the correct
spatial principal coefficient. Its Bianchi contraction includes nonzero spatial
connections, complementing the candidate's normal spatial-coordinate anchor.
These finite rational checks support the general written identities; they are
not a proof over all metric jets or of PDE existence.

Direct-review follow-up executed eight predicates: full constant-Lambda
spatial/time/mixed Ricci identities; arbitrary analytic higher-order scalar/mean
tangent preservation and evidence that both freedoms change data; plus two
packaging comparisons. It imports and reruns only the reviewer's own earlier
scripts; those repeated predicates are regression, not new independence.

The candidate was rerun literally: all 34 predicates passed and its scientific
stdout was byte-identical to the frozen output. Its three literal mutants were
rerun separately. `mean_sign` and `cross_velocity` failed specifically at
`completed_pointwise_momentum_constraint`; `hamiltonian_denominator` failed at
`completed_hamiltonian_constraint`. These were real arithmetic failures, not
timeouts or dependency failures. Independent corruptions also expose omitted
cotangent weighting, connection pairing, spatial curvature, cross-polarization
mean, lowering-metric tangent terms, Ric00 factor, Codazzi sign and Bianchi
trace terms. No false pass was found in these particular guards.

Neither 34 nor the review's counts mean that many independent mathematical
facts. Candidate transverse momentum zeros, trace/self-adjoint properties,
several tangent entries and symmetry-related tests are structural regressions.
Its finite examples do not establish all-data existence. The exact constraint
algebra and written analytic theorem application own the positive conclusion.
The NR1 review's incomplete harmonic-support check remains EXCLUDED; its repair
history is retained, and it is not used for NR2 sufficiency.

Every review run used Python 3.10.12, SymPy 1.13.1, CPU only, one library thread,
512 MiB address-space and 60-second limits through the unchanged run_capture.py.
At most two small captures overlapped. Capture durations were at most 2.426 s,
and maximum recorded child RSS was 62,748 KiB. Exact commands, stdout/stderr,
return codes, resource receipts and source hashes are preserved in this directory.

## History, omissions and disposition

The candidate's pre-freeze code was extended from 30 to 34 predicates to add
Bianchi contractions. The prior source was not hashed before that first run;
`pre_bianchi_check.py` is explicitly a later reconstruction, not an original
snapshot. The reviewer verified that it equals the disclosed removal from the
frozen code. This checks correspondence, not chronology or recovery of an
unsaved original. Earlier output remains retained. No reviewer-requested
candidate repair or scientific revision occurred.

An exploratory navigation attempt used a nonexistent guessed G323 pathname and
returned exit 2. The exact registry and G324 premise ledger then supplied the
needed split-lattice scope; no historical G323 payload became load-bearing.
No scientific computation failed, timed out or lost its capture in this review.
No protected payload or source/current/canon document was modified.

The reviewer personally read the campaign's `full365_resource_retry.json` and
stderr: exit 1 after 11.087 s, at G325 `replay_exact:DERIVATION_RESULT.json`.
Full365 remains NOT_PASSED; later unreached gates are not asserted. That receipt
is not repaired or waived. Earlier source-package reviews, their complete
historical repair chains, whole accepted-package replays, smooth well-posedness,
endpoints, other Fourier sectors and physical identification were not repeated
or extended here.

Defect: none found in the frozen claim at its stated scope.
Survivor: exact iff classification of realizable G327 tangents, with joint
analytic common-slab sufficiency and reviewed mixed-C2 necessity.
Minimum repair: none. Retain all stated scope, theorem, independence, history,
full365 and UNPROMOTED qualifications in downstream summaries.

No physical equation, field, source, action, carrier, selected scalar, lattice,
scale, history, physical content or observational claim is added by this review.
