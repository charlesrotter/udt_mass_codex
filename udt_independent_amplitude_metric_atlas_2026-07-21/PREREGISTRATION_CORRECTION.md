# Pre-outcome amplitude-design correction

Date: 2026-07-21

Applies after historical preregistration commit: `a9a4b81`

No metric geometry or outcome had been evaluated when the preregistered amplitude-design
certification was run.

## Caught defect

The original text selected contiguous zero-based Sylvester `H32` columns `1..11`. Those columns are
pairwise orthogonal and have rank eleven, but they omit the fifth independent binary generator.
Their 32 rows therefore contain only 16 distinct eleven-sign vectors, each repeated twice. That
violates the separately preregistered requirement for 60 unique amplitude identities.

## Corrected design frozen before geometry

Replace only the selected Hadamard column list by the following zero-based columns, in this exact
order:

```text
1,2,4,8,16,3,5,6,7,9,10
```

Columns `1,2,4,8,16` supply the five independent binary generators. The remaining six are fixed
additional nonzero columns. All eleven columns remain pairwise orthogonal, the subdesign has rank
eleven, and all 32 sign rows are distinct.

Every other registered amplitude row, scale `3/4`, bank/point schedule, diagnostic, premise,
falsification gate, and scope ceiling remains unchanged. The original preregistration is retained
as historical evidence and is not silently rewritten.
