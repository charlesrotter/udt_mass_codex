# External review record

Reviewer: external Codex `gpt-5.4`, high reasoning, read-only sandbox
Date: 2026-08-10
Grade: `VERIFIED_WITH_CORRECTIONS`

## Sealed intake

- intake: `/tmp/udt_g56_global_descent_review_20260810_869iie7e`
- files: 48 total;
- pinned sources: exactly 20;
- `INTAKE_MANIFEST.sha256` SHA-256:
  `6c840ed04c4815fe4a17fda828b4b8db419a73a99825185018a43870b724e8ec`.

## Exact correction

The reviewer required one cell change:

```text
R17/D05: OPEN_OWNER -> OWNED_EXACT
```

The full path-labelled `SO(2)` projector-alignment bitorsor and its balanced representative-free
composition are metric-owned. R17/D06 remains `OPEN_OWNER`: one calibration-bearing representative,
scalar calibration density, and physical reset remain unowned.

Consequential counts are `OWNED_EXACT=16`, `OPEN_OWNER=36`; R17 has four exact axes and two open
axes. No other cell changed. R18 D04-D07 remain exact only in the explicitly recorded clock-only
sense.

## Verifier correction

The review also found that the first “independent” verifier only checked hard-coded sets against the
generated atlas and that production scripts could not run inside the sealed read-only layout.
Corrections applied:

- the independent verifier now reads and checks the pinned branch, transition, surface, middle,
  G55, and profile sources before reconstructing the atlas;
- production, independent, and catch scripts now support `--check-only` without writes;
- pinned-source loading supports the sealed `sources/` layout;
- the corrected independent source reconstruction passes 96/96 and catches pass 22/22.

## Raw identities

- raw review SHA-256:
  `0ad62082826300c7cd8289aca38fb1649ae1dafb2f1773c4778512e4dfa64faf`;
- transcript SHA-256:
  `ec6cd66f618c670019e697f861317456faf3aa9dbdc742f5bb6da803f99fb149`;
- transcript exit: `0`.

After applying the exact correction, a fresh 49-file sealed intake at
`/tmp/udt_g56_global_descent_review_20260810_cg9tpf6n` reproduced all three corrected scripts in
read-only `--check-only` mode. Its `INTAKE_MANIFEST.sha256` SHA-256 is
`f6219446d72aa050e07659c9b721cf3a9c2e37690863f4cb42bb60b92da015b7`.

The reviewer independently accepted the R17 global foliation, lawful path holonomy, R18 clock-only
scope, R23 isometric-only status, R24 set-valued status, R04 aggregate correction, R15 local-only
scope, and the bounded `NO_COMPLETE_DESCENT_SELECTOR_IN_PINNED_CORPUS` landing.
