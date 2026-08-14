# R5 verifier chord-transform correction — preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_FIRST_VERIFIER_FAILURE__BEFORE_RERUN`

The first SciPy replay stopped before a result file on the centered random-density A/B comparison at
rank 118. The saved projector overlap was `0.9999999999999998`; the independent path rounded the
corresponding overlap to a value at or above one. Applying

```text
sqrt(max(0, 1-overlap))
```

therefore returned `1.4901161193847656e-08` on the saved path and zero on the independent path even
though the load-bearing overlap agreed at machine precision.

The chord distance contains no information beyond projector overlap and is ill-conditioned at
overlap one. Freeze this verifier-only correction:

1. continue to compare projector overlap independently under the preregistered gap-conditioned
   tolerance;
2. verify the saved chord exactly as the deterministic transform of the saved overlap;
3. do not count chord roundoff as a second independent projector discrepancy;
4. change no production output, singular spectrum, subspace, gap rule, count, premise, or maximum
   conclusion.

Any later failure outside this exact correction stops again before a verification result.
