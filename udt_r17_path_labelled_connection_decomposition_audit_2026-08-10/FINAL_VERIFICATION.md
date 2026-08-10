# Local verification record

Date: 2026-08-10

Status: `VERIFIED-WITH-CAVEATS`; fresh external adversarial review returned
`VERIFIED_AS_STATED`.

## Scientific gates

- Preregistered before calculation: **PASS**, commit
  `6293130b8b2a2256aff85cb5d376e42915b7c209`.
- Bounded scope justified: **PASS**, all six supplied stationary regular lambdas, arbitrary
  compatible second jets, both Maurer--Cartan signs.
- Complete symbolic reconstruction: **PASS**, 10/10 structure checks and all six curvature planes.
- Independent reconstruction: **PASS**, 300/300 exact Fraction/second-jet atomic checks; no SymPy
  and no production-controller import.
- Path functor and `O(2)` algebra: **PASS**, 7/7.
- Exercised mutation catches: **PASS**, 18/18 rejected.
- Fresh external adversarial review: **PASS**—independent reconstruction, no objections; raw
  received-byte SHA-256
  `c0f5b6a8c277081d37d1212e93124f9adde9ed364da068eb376a94a99e12b685`; the sole terminal-LF
  normalization gives committed-content SHA-256
  `395c069f60b0f1d4018a2080e9ecb7bb12b4efbbdb6b167064a80f0b6dff0213`.

## Repository gates

- Source manifest: **PASS**, 14/14 Git blobs, sizes, and SHA-256 values.
- Current premise guards: **PASS**, 49.
- Frozen packages: **PASS**, six manifests, 127 members, 133 package paths.
- Current artifact paths: **PASS**, 1,114.
- Frontier: **PASS**, 306 rows, 101 distinct resolved targets.
- Startup and package Markdown links: **PASS**.
- Tests: **PASS**, 89 passed, 1 xfailed (one new startup catch-proof added by this checkpoint).
- Protected curvature-atlas contents read: **false**.
- Unexpected dirty paths: **none**.

Exact commands, exit codes, and raw-stream hashes are in `COMMAND_TRANSCRIPT.tsv`.
