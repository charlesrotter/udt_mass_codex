# Audit report — complete-coframe calibration transport from scratch

Date: 2026-08-10
Preregistration commit: `8425e2a2`
Final grade: `VERIFIED-WITH-CAVEATS`
External verdict: `CONDITIONAL_PAIR_FAMILY_RESULT_ONLY`

## Result

The from-scratch derivation closes the scalar transport question on a supplied regular calibrated
observer-pair family, while sharply locating the remaining open joint.

The declared smooth local linear positive calibration-line transports form an affine connection
family. Composition and reversal alone do not select a member. Canonical metric-compatible
transport—including Levi-Civita, metric-compatible torsionful connections, and complete-coframe
absolute parallelism—is isometric and therefore carries zero reciprocal magnitude.

Once one regular calibrated pair family is supplied, its complete induced Lorentzian two-metric
`h` determines

```text
phi_pair=(1/4) log[(-det h)/h_00^2],
alpha_pair=d phi_pair
          =(1/4)d log(-det h)-(1/2)d log(-h_00).
```

This is not a frozen or diagonal result. Arbitrary time, angular, screen, shift, and mixing
dependence enters through the complete pair Jacobian before the reciprocal readout. On one common
calibrated family, three-observer scalar reset telescopes identically. Independently rebuilt pair
tapes can retain an offset obstruction and need a lawful transition.

## Honest landing

```text
CONDITIONAL_PAIR_FAMILY_RESULT_ONLY__
LOCAL_LINEAR_POSITIVE_LINE_TRANSPORTS_ARE_AN_AFFINE_CONNECTION_FAMILY__
CANONICAL_METRIC_AND_COMPLETE_COFRAME_TRANSPORTS_ARE_ISOMETRIC_ZERO__
SUPPLIED_REGULAR_CALIBRATED_PAIR_FAMILY_INDUCES_EXACT_FULL_COFRAME_dPHI_PAIR__
PHYSICAL_PAIR_FAMILY_TRANSITION_BRANCH_PATH_AND_GLOBAL_OWNER_OPEN.
```

This replaces the question “which extra scalar reset equation is missing?” with the narrower
question “what native on-shell/global rule constructs one coherent physical calibrated pair
family, or lawful transitions among such families?” It does not answer that remaining question.

## Scope and exclusions

Derived scope:

- smooth local linear positive-line transports;
- regular pair stratum `h_00<0`, `det h<0`;
- supplied calibrated pair family and matched calibration;
- exact time-live and complete-mixing algebra;
- local endpoint descent and matched-family telescoping.

Still open:

- physical pair/query/family selection;
- branch, path, winding, and global-completion ownership;
- transitions between independently rebuilt pair families;
- null, rank-changing, cut-locus, and nonlocal strata;
- action, source, carrier, matter, mass, bootstrap closure, `X_max` profile, CMB spectrum,
  signalling, and dynamics.

## Four evidence gates

1. **Preregistered:** yes, commit `8425e2a2` before derivation output.
2. **Full space or bounded scope justified:** yes, full preregistered smooth local linear
   positive-line class and arbitrary regular full-coframe pair metric; global/nonlocal/degenerate
   strata explicitly excluded.
3. **Independent load-bearing verification:** yes, a separate standard-library rational
   reconstruction passed `63/63`; external `gpt-5.4` reran it and the `24/24` production checks.
4. **Premises audited:** yes, source manifest, premise ledger, type guards, `15/15` catch-proofs,
   and external cold review.

## Evidence map

- `EXACT_DERIVATION.md` — complete derivation and typed scope;
- `TRANSPORT_FAMILY_ATLAS.tsv` — classified transport families;
- `derive_calibration_transport.py` / `DERIVATION_RESULT.json` — exact symbolic checks;
- `verify_calibration_transport_independent.py` / `INDEPENDENT_VERIFICATION_RESULT.json` —
  independent standard-library reconstruction;
- `run_catch_proofs.py` / `CATCH_PROOF_RESULT.json` — fail-closed mutation guards;
- `EXTERNAL_REVIEW_RAW.md` and `EXTERNAL_REVIEW.md` — cold review and adjudication;
- `STATUS_LEDGER.tsv` — claim-by-claim epistemic scope;
- `NEXT_STEP.md` — bounded continuation.
