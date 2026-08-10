# Local verification record

Date: 2026-08-10

Status: `LOCAL_VERIFIED_LEAD`; fresh external adversarial review is pending.

## Scientific gates

- Preregistered before calculation: **PASS**, commit
  `a85f93f4cd648881831ce1ffb4673cbfbe7d22c7`.
- Bounded scope justified: **PASS**, all six supplied regular stationary C01--C06 lambda strata,
  arbitrary smooth stationary `phi`, both Maurer--Cartan signs.
- Exact symbolic reconstruction: **PASS**, 10/10 checks.
- Independent reconstruction: **PASS**, 72/72 Fraction/Dual checks; no SymPy and no import of the
  production controller.
- Exercised fail-closed mutations: **PASS**, 16/16 rejected.
- Premise audit: **PASS** for the bounded result; physical-path and downstream ownership remain
  explicitly open.
- Fresh external adversarial review: **PENDING**.

## Repository gates

- Source manifest: **PASS**, 12/12 Git blobs, sizes, and SHA-256 values.
- Current premise guards: **PASS**, 47.
- Frozen packages: **PASS**, six manifests, 127 members, 133 package paths.
- Current artifact paths: **PASS**, 1,114.
- Frontier: **PASS**, 306 rows, 101 distinct resolved targets.
- Startup and package Markdown links: **PASS**.
- Tests: **PASS**, 88 passed, 1 xfailed.
- Protected curvature-atlas contents read: **false**.
- Unexpected dirty paths: **none**.

The exact command, exit-code, stdout hash, and stderr hash record is in
`COMMAND_TRANSCRIPT.tsv`; raw streams are retained beside it.
