# G223 repair preregistration

Date: 2026-08-22

Review landing: `ACCEPT_WITH_REPAIRS`.

## Frozen repairs

### R1 — read-only replay

- Add `--check-only` to both production implementations.
- In check-only mode, compute every registered assertion and construct the result payload in
  memory, but do not write `DERIVATION_RESULT.json`, `CONTROL_ATLAS.tsv`, or
  `INDEPENDENT_VERIFICATION.json`.
- Make `verify_package.py` invoke both scripts with `--check-only`.
- The full package verifier must succeed when the complete intake tree is filesystem read-only.

### R2 — independent fiber integration

Replace the vacuous assertion with exact `Fraction` arithmetic. For random positive `a`, two
independent fiber parameters `lambda_1,lambda_2`, and a base-dependent offset `s_0`, verify

\[
(a\lambda_2+s_0)-(a\lambda_1+s_0)=a(\lambda_2-\lambda_1).
\]

Retain the total exact-rational assertion count at 361,001 by replacing, not adding, the 1,000
vacuous controls.

### R3 — sealed source containment

- Reject absolute manifest paths and every path containing `..`.
- Resolve each frozen source and require it to remain below the verifier's `REPO` root.
- Record in `REVIEW_SCOPE.json` that sources are copied at repository-relative paths inside the
  intake root.
- Rebuild a fresh intake and run the package verifier after removing write permission from all
  intake files and directories.

## Invariants that must not change

- 7 sources;
- 21 symbolic checks;
- 20,000 independent overlap cases;
- 361,001 exact-rational assertions;
- 14 hostile payload mutations;
- the complete bounded G223 landing and every premise ceiling.

## Repair grade

Until a fresh sealed repair-only follow-up accepts all three repairs:

```text
ACCEPT_WITH_REPAIRS__REPAIR_REVIEW_PENDING
```

