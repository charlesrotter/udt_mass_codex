# External-review adjudication

Date: 2026-08-11

Raw-return SHA-256:
`bfcf3423a05bcfd17c1aee5aa91ea8d139dfee72376d22b30ff7d14e0f5bb9c8`

Repository Markdown copy SHA-256:
`f7b04fe9a916c28f2485019a11f570a98b6dabc94d83cc374c6dad15142dc503`.
The sole byte difference is the repository copy's terminating newline; `diff` confirms no content
difference.

External verdict: `VERIFIED_WITH_CAVEATS`.

Final package grade: **VERIFIED-WITH-CAVEATS**.

## Accepted result

The reviewer independently replayed the sealed 37-file payload, reproduced all 18 fits, the 443
compared leaves, the exact 9-check retyping, the independent P1 reconstruction, all 14 registered
scope catches, and the 38-check prereview package return. It independently upheld both registered
landings:

```text
BASELINE_REPRODUCED__NATIVE_RETYPE_ALGEBRAICALLY_IDENTICAL
AND
NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION
```

No scientific formula, ownership ruling, premise stamp, or numerical result is changed by review.

## Accepted caveat and repair

The reviewer correctly found that the float branch of the recursive replay comparator coerced the
candidate through `float(...)` before comparison and could therefore accept a stringified numeric
leaf. The correction was preregistered before mutation in
`EXTERNAL_REVIEW_CORRECTION_PREREGISTRATION.md`.

The repaired comparator now rejects nonnumeric and boolean values in a reference-float slot before
numeric comparison and requires exact integer typing for reference-integer slots. Exercised catches
reject a stringified float and a boolean while retaining an integer JSON number as a valid numeric
representation of an exactly integral reference float.

Post-repair returns:

```text
18 fits / 443 leaves / max numeric difference 0.0
9/9 exact query-equivalence checks
independent P1 reconstruction unchanged and within every tolerance
14/14 prior scope catches
3/3 new type controls
43 package checks
```

## Evidence grade

The correction closes the mechanical caveat but does not promote the science above
`VERIFIED-WITH-CAVEATS`: the frozen scalar SNe universe is complete and exactly reproduced, while
the physical complete SNe query, pair immersion, screen-area map, and time-live orchestra history
remain open. The external catch harness is regression evidence, not a second independent physical
derivation.

The source manifest remains the immutable prereview snapshot. Because the live premise registry
legitimately receives the append-only G64/G65 rows when this result is banked, the final replay
verifiers check its registered bytes at commit `307144b5`; all other 18 source rows continue to
check directly against the current paths.

## Next justified use

Retain the SNe return as a conditional low-redshift compatibility anchor. A later complete geometry
may be projected through this observer query and compared with the P1-like relation, but P1 must not
be copied into a centered CMB lapse or used to select the missing upstream geometry.
