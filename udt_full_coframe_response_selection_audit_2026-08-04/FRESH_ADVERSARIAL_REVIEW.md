# Fresh adversarial review — preserved initial return

Date: 2026-08-04
Reviewer: fresh read-only external Codex `gpt-5.4`, high reasoning
Status: `FAIL_PACKAGING_AND_VERIFIER_INTEGRITY__NO_BLOCKING_MATHEMATICAL_ERROR`

This return is preserved unchanged in substance. Its required repairs are applied in the package
and adjudicated separately; the original failure is not overwritten by a later closure.

## FINAL_RULING: FAIL

## BLOCKING_ERRORS

- `verify_audit.py` hard-required `FRESH_ADVERSARIAL_REVIEW.md`, `SOURCE_MANIFEST.tsv`,
  `CATCH_PROOFS.tsv`, and `VERIFICATION_RESULT.json`, but those files were absent from the delivered
  package. The verifier was not replayable as shipped.
- `verify_audit.py` required the audit text to say the fresh review was complete, but
  `AUDIT_REPORT.md` still said `fresh semantic review pending`. The verifier and report were
  internally inconsistent on a load-bearing evidence gate.

## REQUIRED_REPAIRS

- Make verifier replay non-broken: either add the missing review/manifest/catch/result artifacts,
  or change no-write replay so it derives and checks them in memory instead of reading absent files.
- Synchronize packaged status claims: the audit report, verifier assertions, and packaged outputs
  need one consistent fresh-review state before banking.
- Add semantic catches for `SOURCE_ADJUDICATION.tsv`, P15–P18 premise rows,
  operator-home/provenance claims, and prior-versus-new provenance; current mutations mostly test
  status tokens and magic strings.

## NONBLOCKING_CAVEATS

- The reviewer found no blocking mathematical error in the core algebra. The failure was
  packaging/verifier integrity, not the 16-to-10 map, pullback theorem, `phi` pairing controls,
  `f(R)` control, `c/G` rank control, or nine-query reduction.
- The verdict is bounded. It supports
  `AVAILABLE_PLURAL_RESPONSES__NO_FOUNDATIONAL_SELECTION` only over the frozen eleven-class
  universe, not over all natural or future UDT operators.
- The zero/volume-response interpretation is weaker than the linear-algebra controls; it is a
  semantic realization judgment, not a separate exact theorem.

## INDEPENDENT_RECOMPUTATION

- Independent one-off SymPy recomputation gave rank `10` and nullity `6` for
  `X -> X^T eta + eta X`; the six canonical `eta`-skew generators span the kernel exactly.
- The response pullback `E -> alpha_E` has rank `10` and annihilates those six gauge generators, so
  the coframe pullback is injective and gauge-horizontal.
- For `H=diag(-1,1,0,0)`, `T_H=diag(2,2,0,0)`; the volume pairing is `0` and the anisotropic control
  pairing is `2`.
- For inverse-metric variation on 4D constant-curvature metrics, `f(R)=R^n` gives
  `E_n=((n-2)/4)R^n g`; the sampled `n=1` versus `n=3` determinant at `R=4,12` is `-384`.
- The package's `c,G` dimension system has coefficient rank `2` and augmented rank `3`, so `c_E`
  and `G_obs` alone do not determine an `L^-2` curvature coefficient.
- The nine normalized universal-query conditions have rank `9` with one-dimensional kernel equal
  to the metric line.

## SCOPE_AND_PREMISE_AUDIT

- P4 is treated honestly as prior, not as a new derivation. The package calls itself a
  `current-premise overlay`, and the July 29 P4 sources remain prior typed response-space work with
  no selected candidate.
- F01/F02 remain conditional and F04 remains carrier-conditional, matching their authorities.
- EH remains `CONDITIONAL_NOT_SELECTED`; Bach remains
  `UNIQUE_CONDITIONAL_ONLY_IF_PRE_SCALE_STRONG_CSN_RETAINED`; the carrier remains
  `POSIT_AND_CONDITIONAL`; bootstrap remains `WORKING_ON_SHELL_ADMISSIBILITY`.
- The eleven-class audit supports its bounded plurality/nonselection verdict.
- The reviewer inspected the current startup blocks and did not read the contents of the unrelated
  83 untracked curvature-atlas files.

## VERIFIER_AUDIT

- The main failure was replayability and synchronization, not algebraic checking.
- The verifier checked only the order of `SOURCE_ADJUDICATION.tsv`, not its semantic content.
- Most mutations were token-level and could miss semantic drift in P15/P17/P18, operator homes,
  EH/Bach/bootstrap/carrier/mass prose, or prior-versus-new provenance.
- Link, frozen-manifest, and test-count checks were useful hygiene but did not close those semantic
  gaps.
