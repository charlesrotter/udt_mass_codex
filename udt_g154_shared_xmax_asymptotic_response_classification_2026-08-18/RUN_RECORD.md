# G154 run record

Date: 2026-08-18
Host kernel: `Linux 6.8.0-124-generic x86_64 GNU/Linux`
Python: `3.10.12`
SymPy: `1.13.1`
GPU: not used; exact symbolic and small independent CPU checks only

## Commands

```bash
python3 udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/derive_asymptotic_response.py \
  --output udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/DERIVATION_RESULT.json

python3 udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/verify_asymptotic_response_independent.py \
  --output udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/INDEPENDENT_RESULT.json

python3 udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/verify_package.py \
  --output udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/VERIFICATION_RESULT.json

python3 udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/run_catch_proofs.py \
  --output udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/CATCH_PROOF_RESULT.json

python3 udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/udt_g154_common_scale_checks.py

python3 udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/verify_external_common_scale_independent.py \
  --output udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/EXTERNAL_REVIEW_INDEPENDENT_RESULT.json

python3 verify_current_scientific_premises.py
python3 -m pytest tests/
git diff --check
```

## Raw gates

- production symbolic checks: `14/14 PASS`;
- independent stdlib/source checks: `16/16 PASS`;
- mutation catch proofs: `9/9 PASS`;
- supplied cold-review SymPy replay: `ALL CHECKS PASSED`, stdout byte-identical to supplied log;
- independent stdlib conformal/network replay: `12/12 PASS`;
- current premise verifier: `PASS` on 141-row registry;
- repository tests: `115 passed, 1 expected xfail`;
- `git diff --check`: clean.

The first independent tail grid ended at `q=1e-12`, too coarse to certify the deliberately slow
`q^(1/6)` quiet witness and `q^(-1/12)` divergent witness. It returned `FAIL` rather than loosening
the gates. The grid was extended, without changing formulas or thresholds, through `q=1e-60`; the
final raw tails are stored in `INDEPENDENT_RESULT.json`.

Fresh adversarial review then rejected the fixed-scale ownership claim as circular. The repair did
not change the response counterfamily. It added an exact normalized-composition/nonconstant-scale
countermodel and expanded the independent replay to reconstruct responses from pair-metric
`T,L`, cover both oscillatory duals, and check the two cancellation terms separately. All repaired
checks pass. The repair-only follow-up then returned `PASS` with no remaining algebraic or
premise-ownership defect inside the bounded scope.

The cold external review then strengthened the result from a pair counterfamily to network-level
nonselection under current identities. Its supplied SymPy script reproduced exactly. The first new
stdlib replay preserved a real `FAIL`: the slow `q^(-1/12)` witness grew by only 3.75 orders by
`q=1e-48`, below the preregistered four-order gate. Extending the identical grid to `q=1e-60`, with
no formula or tolerance change, produced the final `12/12 PASS`.

After banking G154 into the live premise registry, current-worktree source hashes necessarily
differed from the preregistered source snapshot. Both verifiers now replay every manifest source
from preregistration commit `f5946fa0`; no expected hash was changed.
