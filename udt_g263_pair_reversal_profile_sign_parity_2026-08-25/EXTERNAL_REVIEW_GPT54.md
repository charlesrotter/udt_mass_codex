`ACCEPT_WITH_REPAIRS`

**Findings**
- The registered symbolic producer is not replayable in this sealed environment. [derive_parity.py](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/derive_parity.py:10) hard-depends on `sympy`, and rerunning `python3 derive_parity.py` failed with `ModuleNotFoundError`. The same run record also names `verify_current_scientific_premises.py` and `pytest tests/`, but neither exists anywhere under `/work`; see [RUN_RECORD.md](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/RUN_RECORD.md:10), [RUN_RECORD.md](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/RUN_RECORD.md:18), [RUN_RECORD.md](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/RUN_RECORD.md:19). This is a replay-packaging defect, not an algebra defect.
- The mutation harness is materially weak. [run_catch_proofs.py](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/run_catch_proofs.py:19) validates only a narrow subset of claims, and its registered mutations at [run_catch_proofs.py](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/run_catch_proofs.py:63) do not cover several load-bearing statements. I directly probed `validate()` and found substantive escapes: corrupting `separation.shared`, removing `pair_contrast_even` while preserving count 31, corrupting the positive/negative constant-jet `A` values, and weakening the `R_pair` narrative all still passed. That does not overturn the science, but it does mean the advertised 12/12 mutation catch is only a shallow artifact-regression guard.
- Qualification, not rejection basis: the bundled “independent” replay is implementation-distinct and does span negative `phi` via `s<1`, but it is not epistemically independent and it does not by itself cover every separator claim; the script says this explicitly at [verify_independent.py](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/verify_independent.py:99).

**Verdict**
The exact maximum bounded scientific landing that survives adversarial review is:

```text
PAIR_ARROW_REVERSAL_IS_EXACT_RECIPROCAL_INVOLUTION
__WHOLE_PROFILE_SIGN_CONJUGATION_IS_A_DISTINCT_METRIC_INVOLUTION
__SCALAR_DEPTH_INVERSION_SHARED_BUT_COMPLETE_CHANNEL_PARITIES_MIXED
```

I independently confirmed the load-bearing algebra in the stated bounded arena. In particular:
- `R_pair` and `C_phi` are both involutions but are distinct operations: `R_pair` fixes the ambient metric, while `C_phi` sends `g_phi` to `g_-phi`; the unchanged areal sphere blocks any promotion to a full coframe symmetry, consistent with [EXACT_DERIVATION.md](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/EXACT_DERIVATION.md:113).
- The shared scalar inversion claim is correct: endpoint reversal and whole-profile conjugation both invert the endpoint clock ratio, but only the latter changes the full metric history.
- Negative `phi` was not excluded. My replay covered `s=e^phi` with `s<1`, `s=1`, and `s>1`.
- The G201 zero-tide separator is correct: the conjugate family is not angularly quiet away from `Cr^2=0`, matching [EXACT_DERIVATION.md](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/EXACT_DERIVATION.md:217).
- The constant-jet signed-end table is correct only as a scoped illustrative subclass, exactly as stated at [EXACT_DERIVATION.md](/work/udt_g263_pair_reversal_profile_sign_parity_2026-08-25/EXACT_DERIVATION.md:244).
- No in-scope basis appears for promoting geometric mass aspect to physical mass, or for importing history, source, dynamics, universal loudness, or `X_max`.

**Checks Run**
- `python3 derive_parity.py` in `/work/udt_g263...`: failed, `ModuleNotFoundError: sympy`.
- `python3 verify_independent.py`: `PASS`, 1,000 cases, 29,000 exact assertions.
- `python3 run_catch_proofs.py`: `PASS`, 12/12 listed mutations caught.
- `python3 verify_package.py`: `PASS`.
- Independent exact-rational adversarial replay in `/work`: `PASS`, 27,408 exact checks over 1,000 cases; coverage `s<1: 421`, `s=1: 53`, `s>1: 526`; 1,000 shared-scalar inversion checks; 1,000 areal-sphere guard checks; 577 nonzero conjugate zero-tide witnesses.
- Independent mutation-escape probe of `run_catch_proofs.validate()`: 5 substantive escapes found.
- `diff -rq /intake/... /work/...`: only `__pycache__` differed, created by execution.
