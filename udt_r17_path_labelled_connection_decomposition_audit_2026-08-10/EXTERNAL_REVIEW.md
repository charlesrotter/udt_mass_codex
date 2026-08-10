# External adversarial review adjudication

Date: 2026-08-10

## Intake boundary

The external `gpt-5.4` reviewer received one sealed, read-only 54-file intake:

- the 40-file pre-review package;
- only the exact 14 private sources frozen in `SOURCE_MANIFEST.tsv`;
- no other repository content; and
- no protected curvature-atlas content.

The raw return had no terminal line feed. `EXTERNAL_REVIEW_RAW.md` preserves its text with one
repository-normal terminal LF. The received-byte SHA-256 is
`c0f5b6a8c277081d37d1212e93124f9adde9ed364da068eb376a94a99e12b685`; the committed-content
SHA-256 is `395c069f60b0f1d4018a2080e9ecb7bb12b4efbbdb6b167064a80f0b6dff0213`.

## Verdict

```text
VERIFIED_AS_STATED
```

The reviewer independently reconstructed the coframe inversion, noncoordinate frame brackets,
Koszul connection, compatible scalar-jet commutators, four normal-connection coefficients, and all
six curvature components. It found no algebraic failure, type failure, or bounded-scope
overstatement.

## Adjudication

No correction is required. The external maximum defensible claim is the same as the preregistered
local landing: on the supplied regular stationary positive R17/W01 C01--C06 family, the metric
derives a complete projected metric connection on the normal bundle and an isometric
path-labelled transport functor after a path is supplied. It does not select a path, give generic
base descent, or supply the physical non-isometric observer arrow.

The package is therefore banked `VERIFIED-WITH-CAVEATS`, not canon and not a claim beyond the
declared stationary regular `R x S3` family.
