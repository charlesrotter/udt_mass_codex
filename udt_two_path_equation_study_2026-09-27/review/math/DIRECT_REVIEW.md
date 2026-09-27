# Direct substantive review — original candidate and native control

Reviewer: `quadratic_review`, separate source-first same-model context.
Date: 2026-09-27. Verdict on mathematical content: **VERIFIED-WITH-CAVEATS**
at the exact conditional scopes below. Initial wording/provenance repairs are
required and tracked; no physical adoption, whole-theory proof, or canon follows.

## Exposure and versions

The source-first report was frozen before receiving the parent's candidate:
`SOURCE_FIRST.md` SHA-256
`841ec257fab9308bbc9013aec03c36c8bdb55aec2e01c2b92abd69547a094b73`.
Its script/outputs/source pins are separately frozen in SOURCE_FIRST_FREEZE.sha256.
I did not read parent code or outputs before that freeze and have not imported
them for the direct checks. After the freeze I read these candidate bytes:

| Original direct input | SHA-256 |
|---|---|
| EXTENSION_CANDIDATE.md, now preserved as EXTENSION_REVIEW_INPUT.md | `8165d2027394aa444ff4c821c6ab6f1a89e9870226bc62f2b17a38293c56fd66` |
| DECISION_BRIEF.md, now preserved as DECISION_BRIEF_INITIAL.md | `65ba438e80e0543e11ebf7d5ddca2ce792ddc1a49950481db4fcb353bf0a01b3` |
| native/NATIVE_RESULT.md | `30a88a53c787001a147ce5dbc4fc1ce963744f8a191aa4a4be265448c7993084` |

These hashes were independently recomputed, including the preservation copies.
For the native review I additionally read founding.md F1-F4, W1, W4-W6,
sections 6-7, along with the already read current GR-filter authority and
G311 DDR theorem. I did not replay all historical source packages, inspect
protected payloads, or certify the original source table's entire bibliography.
The load-bearing finite-pair formulas, one-metric condition, completed-pair
calibration boundary, and local-response ownership boundary were checked directly.

The original direct inputs are reviewed here even though the parent subsequently
announced repairs. A focused re-review will pin the resulting current versions.

## Extension argument: tests aimed at breaking it

The bulk response E1 follows from compactly supported inverse-metric variation
and two integrations by parts. The tensor is symmetric, natural, generally
fourth order, and divergence-free. E2 is the **chosen DDR response equation**;
the explicit rejection of unrestricted action stationarity E=0 preserves the
trace datum. No physical boundary action or source has been silently supplied.
The fourth-jet/dimensionful-coupling departure from the G301 response class is
disclosed rather than treated as a native theorem.

I independently reconstructed the full four-dimensional connection, angular
Ricci entries, Hessian, response and divergence before reading this candidate.
Those 49 exact symbolic zero checks and three nonzero controls remain in the
source-first artifacts. E4-E8 agree with that reconstruction. The sign change
between my temporal-minus-radial difference and E5's radial-minus-temporal
difference is correct, not a discrepancy.

E5 gives R''=0 because alpha!=0 and f>0; it never divides by F. E6 is the full
general integral of the linear Euler equation for the curvature scalar, with
both homogeneous modes retained. In E7, all terms including the angular
`2/r` contribution to `f'+2f/r` are present. The coefficient `12alpha u` of r
forces u=0 on an open interval; independently the leading coefficient
`-(3/2)alpha u^2` also forces it. This is an interval polynomial argument, not
a finite sample or a scan. Then v=-4C and the angular equation forces
`(1+2alpha v)q=0`.

The two strata are necessary and sufficient in the declared positive-f primary
ansatz. Full component substitution proves both, including arbitrary q on the
critical stratum. At q!=0 the trace-free Ricci entries are proportional to
`diag(-q,-q,q,q)/r^4`, so the branch is genuinely non-Einstein. Its response is
`E=g/(8alpha)`, which is nonzero and pure trace. Thus neither deleting this
stratum nor imposing E=0 survives the explicit exact controls. For alpha=0,
the separately treated S=0 equation gives the ordinary Einstein family.

At fixed smooth bounded jets the operator limit alpha->0 is valid. The critical
family's scalar curvature diverges as -1/(2alpha), so it cannot have a
bounded-curvature limit. The candidate properly distinguishes these assertions.
Its generic primary return to an Einstein family does not establish equivalence
to GR in dynamic or nonspherical sectors and does not select the free constants.

## Exceptional linearization, independently checked

At a critical background, `R0=-1/(2alpha)`, `F0=0`, `L0=-1/(4alpha)`,
`C=1/(8alpha)` and R0 is constant. For covariant h=delta g and rho=delta R,

`delta(F Ric)=2alpha rho Ric`,
`delta[-(L/2)g]=+(1/(8alpha))h`,
`delta[(g box-nabla nabla)F]=2alpha(g box-nabla nabla)rho`.

The derivative-operator variations on the constant F0 vanish. Subtracting
`delta(Cg)=C h` at **fixed C** cancels the h term. This proves E9 componentwise:

`delta(E-Cg)=2alpha[rho Ric+(g box-nabla nabla)rho]`.

The proof does not require the background to be Einstein. All perturbations
whose scalar variation vanishes throughout the region have zero first-order
residual; E9 does not imply those perturbations survive at nonlinear order.
Gauge perturbations are among these directions, and no physical degree-of-
freedom count or ghost/stability assertion is inferred. The explicit critical
family also supplies nontrivial parameter variations with delta R=0.

Tracing E9 gives `(6alpha box-1)rho=0`. More generally this is the linearization
of the trace equation about a constant-scalar-curvature background solution
within the same C sector. If C varies, the right-hand side is `4 delta C`.
The scalar principal cone statement is a statement about this necessary scalar
operator for alpha!=0, not the principal system of all metric equations or an
independent physical propagation law. The candidate's no-lift/no-stability
limitations are necessary and correct.

`direct_review_check.py` independently checks an abstract arbitrary component
variation keeping arbitrary h, delta Ricci, Hessian rho, and box rho. It checks
the exact C h cancellation, the varying-C term, the trace, and the failure if
the C h contribution is omitted. This is formal exact first-variation algebra,
not a full metric-perturbation PDE existence or stability computation.

## Native control and quantifiers

Under the explicitly supplied static matched comparison,
`d tau_B/d tau_P=sqrt(f(B)/f(P))`; completed reciprocity gives
`q_PB=(d tau_B/d tau_P)^2=f(B)/f(P)`. The source's general pair composition
formula needs exact matched calibration and is not automatically valid for
arbitrary paths, moving observers or radiation transfer. The candidate keeps
that qualification and supplies the static Killing-time comparison directly.

For the free control profile f=1+(r/ell)^2 and reference radii ell,3ell with
terminal radius 2ell, I independently recomputed f values 2,10,5 and ratios
5/2,1/2 using exact rational arithmetic. The chart change has diagonal
Jacobian factors 1/sqrt(a),sqrt(a),1,1 from carried to base coordinates, hence
metric entries -5/a,a/5,r^2,r^2 sin^2(theta). The angular terms remain at
the same areal radius. Pair determinant stays -1, the full determinant is
unchanged, and both carried coordinate null directions return to base slope
dr/dx0=5. Proper clock/ruler conversion gives squared local normalized null
ratio 1 in both cases. The proposed bad second-cone substitutions have residuals
21/4 and -3/4, as claimed. The direct check includes a nonequatorial regular
angle with sin^2(theta)=3/4, providing an additional angular-carry control.

The local metric and its jets are literally the same supplied function in the
same base chart, so changing only a reference does not change that jet.
Local Metric Sufficiency consequently excludes any **surviving** reference
dependence of the specified universal local response at fixed jet, when both
queries are admitted and the response itself is query-independent. This is a
conditional implementation discriminator. The candidate correctly excludes
coordinate rewrites, invariant cancellations, finite-query observables, and
possible specified reference-selection rules from that narrow refutation.
It also distinguishes a response tensor from an equation's solution set:
multiplication by a nowhere-zero query factor does not change the latter.

No claim that both test queries are physically populated is needed or made.
The control is not a countermodel to the full UDT premises, and it does not
prove that a new postulate is necessary or that native equation discovery is
exhausted. The retained measured calibration is consistent with the owner's
fixed positional interpretation at this declared level; the mathematical
control does not independently prove that physical interpretation.

## Defects, survivors, and smallest repairs

1. **D1 — curvature type wording.** Original extension section C says
   "exceptional constant curvature R0". This is ambiguous/too strong if read
   as constant sectional curvature: q!=0 is non-Einstein and p/r can carry
   Weyl curvature. Survivor: constant **scalar** curvature at the critical
   response factor, with E9 unchanged. Repair: name scalar curvature explicitly.
2. **D2 — citation type.** The original final citation calls Sotiriou/Faraoni
   arXiv:0805.1726 a primary source; its abstract explicitly identifies it as a
   review. No mathematical defect follows, but the assigned primary-only source
   requirement should be met. Survivor: the correct variational formula. Repair:
   cite the primary Guarnizo/Castañeda/Tejeiro derivation
   [arXiv:1002.0617v4](https://arxiv.org/html/1002.0617v4), equations (3.8),
   (3.14), (3.25), already used independently in SOURCE_FIRST.md. A review may
   be retained only with its genre and non-load-bearing role correctly labeled.
3. **D3 — perturbation scope clarification.** E10's original "ANY constant-R
   background" should specify a background **solution**; its necessary tangent-
   solution interpretation uses that hypothesis. It should explicitly state
   the `4 delta C` term if the connected trace datum is varied. Survivor:
   E10 as written at fixed C; no changed equation needed.
4. **D4 — summary ceiling.** The original brief's "fully examined first
   extension candidate" is too broad without immediate static/diagnostic scope.
   Its "desired generic new static behavior" wording unnecessarily implies a
   target outcome although the work order did not freeze one. Survivor: exact
   scoped classification and necessary trace diagnostic. Repair: name those
   scopes and report the unchanged generic static family neutrally.

D1-D4 are source-preserving wording/provenance repairs; no change to the
mathematical result is requested. No contradiction was found between the
native control's quantifiers and its source equations.

## Checks, limits, and review grade

Source-first run: 49 exact symbolic zero checks plus three concrete nonzero
controls, exit 0. Direct run: **27 exact checks**, exit 0, Python 3.10.12 /
SymPy 1.13.1, under `timeout 120s`; stdout, stderr and DIRECT_CHECK_RESULT.json
are saved beside the independent direct script. Exact command:

`timeout 120s python3 udt_two_path_equation_study_2026-09-27/review/math/direct_review_check.py`

The parent reported 52 construction checks and timing; I have not audited its
script/count/timing and do not claim those as independent evidence. My own
implementations and proof checks above supply the review evidence. There is
fresh context, source-first argument, and code independence from parent/native
scripts; shared standard mathematics and SymPy remain. No different model,
unexposed final-candidate review, independent empirical confirmation, historical
full-source recertification, or global PDE analysis is claimed.

Pending parent repairs and focused re-review, the mathematical survivor is a
reviewed conditional native implementation discriminator plus one explicitly
unadopted quadratic-response classification. Full premise re-audit, packaging,
source-version checks, final wording, commit and push remain parent gates.

## Focused re-review after source-preserving repairs

Current inputs independently hashed after direct comparison with the preserved
originals:

| Repaired/current input | SHA-256 |
|---|---|
| EXTENSION_CANDIDATE.md | `c49e60aab6d14a459a7b948d64503345c580f2b9bdf4d991556381e79738d710` |
| DECISION_BRIEF.md | `5748b4e0a587a693bb8d8f9f45d9fccef865c5ff66ae6bd49651aa894d096a25` |
| native/NATIVE_RESULT.md, unchanged | `30a88a53c787001a147ce5dbc4fc1ce963744f8a191aa4a4be265448c7993084` |
| founding.md, direct-review source | `b4b0d9a9fdd093c992647195aca7579566a9e77a396071a699c1938888a49e75` |

The exact diffs resolve D1-D4: scalar-curvature language, primary derivation
citation with previous review exposure retained, solution/fixed-C perturbation
scope with varying-C term, and the bounded neutral decision summary. The added
paragraph explicitly keeps fourth-order DDR-response identification within the
unadopted hypothesis. Equations E1-E10 and the native mathematics are unchanged.
No new physical premise, fitted profile, response ownership, instability claim,
or second corrective term was introduced. The two original review inputs still
have their original hashes. The complete source-first six-file freeze checks
PASS after these additions.

The scientific checks were not repeated for these documentation-only repairs;
the preserved exact computations and independently inspected arguments remain
applicable. One checksum invocation used root-relative paths from the review
directory and failed with file-not-found errors; it made no change and was
reissued at the correct root. The correct hash and freeze-check invocations
exited 0. Parent reports the new full 406-row premise verifier PASS, exit 0;
that is attributed parent evidence, not an independent child replay.

**Final scoped verdict at the listed bytes: VERIFIED-WITH-CAVEATS; D1-D4
resolved, no remaining substantive defect found.** The surviving caveats are
the declared unadopted response choice, admitted-query qualification, static
positive-f interval restriction, absence of physical source/scale selection,
and the necessary-only linearized diagnostic. Review does not upgrade the
underlying premises, establish physical viability or canonize either path.
Subsequent packaging, final manifest completeness, commit, and push are not
certified by this review.
