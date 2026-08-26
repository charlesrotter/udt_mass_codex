# G261 evidence gates

1. **Preregistered:** PASS — `MAP.md`, `PREREGISTRATION.md`, and `PREMISE_LEDGER.tsv` were committed
   and pushed at `458e02e9` before execution.
2. **Bounded scope justified:** PASS — the question is ownership of ten explicit operator properties;
   it is not a solution-space census or history solve.
3. **Independent verification:** PASS WITH REPAIRS — the fresh external reviewer independently
   verified the sealed manifest and deterministic replays and returned `ACCEPT_WITH_REPAIRS`; the
   repair-only follow-up returned `ACCEPT_REPAIR` with no remaining R1--R4 defect.
   Internally, `verify_independent.py` is now explicitly limited to an artifact-independent,
   source-driven structural cross-check. It imports no production code, reads no production result,
   and reports 12,041 assertions over 2,000 profile-value/jet controls, but it is not claimed to be
   logically or epistemically independent.
4. **Premise audited:** PASS — W4 is `WORKING/POSIT_NOT_CANON`; all G259 class requirements remain
   individually typed; no observational, source, fit, `X_max`, GPU, or protected input enters.

Artifact mutation controls: the unmutated baseline passes and 10/10 actually applied mutations are
rejected. This is a regression guard, not scientific proof. The candidate variational-minimality
premise is explicitly `NOT_ADOPTED`.

Banking grade: `EXTERNALLY_REVIEWED_WITH_REPAIRS_ACCEPTED__NO_REMAINING_R1_R4_DEFECT`.
