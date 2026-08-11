# External-review correction preregistration

Date: 2026-08-11

External raw-return SHA-256:
`bfcf3423a05bcfd17c1aee5aa91ea8d139dfee72376d22b30ff7d14e0f5bb9c8`

External verdict: `VERIFIED_WITH_CAVEATS`.

## Finding frozen before mutation

The reviewer reproduced the scientific and ownership returns, but found that
`replay_m3_unchanged.py::compare` accepts a stringified numeric replay leaf when the frozen
reference leaf is a Python `float`, because the replay leaf is passed through `float(replay)` before
comparison. This can hide a JSON leaf-type mismatch while preserving numerical equality.

## Bounded repair

1. Require a replay leaf corresponding to a reference `float` to be a numeric JSON scalar of exact
   Python type `float` or `int`, excluding `bool`; reject strings and all other types before numeric
   comparison.
2. Preserve the existing exact handling of booleans, nulls, strings, integers, mappings, and lists.
3. Add exercised catches proving that a stringified float and a boolean in a float slot are rejected,
   while an integer-valued JSON numeric in a float slot remains a lawful numeric representation.
4. Do not change data, cuts, covariance, profile menu, fitting code, tolerances, formulas, premises,
   scientific landing, or source ownership.

## Certification contract

- the new type catches pass;
- all 18 frozen fits and all 443 leaves still compare with maximum absolute numeric difference `0.0`;
- the independent P1 reconstruction and `9/9` symbolic equivalence return are unchanged;
- all prior 14 scientific/scope catches still pass;
- the source manifest remains unchanged and valid;
- repository tests and premise guards remain at baseline;
- protected curvature-atlas files and the stopped native-on-shell draft remain untouched.

Maximum conclusion: the external caveat is repaired mechanically. It cannot strengthen the scoped
scientific verdict beyond `VERIFIED-WITH-CAVEATS`.
