# G350 external-review transmission record

Date: 2026-09-05

Charles authorized the sealed 39-file intake at `/tmp/udt_g350_review_959fhvn8` for fresh
read-only adversarial review by external `gpt-5.6-sol`, including read-only authentication-file
use and shared host-network access solely to launch the reviewer. The intake contained 37 manifest
payloads plus `REVIEW_MANIFEST.tsv` and its detached seal.

The first launch authenticated all 37 payloads, but its host-side session ended before scientific
review or a verdict. It produced no report and is retained only as interrupted launch chronology.
The unchanged, already authorized intake was launched again. The intake and authentication file
remained mounted read-only; the reviewer copied the intake into an isolated writable ephemeral
directory, ran checks only there, and returned its report from an isolated return directory.
Completed external Codex session: `01a071c8-b680-71f0-80b7-8c7d0e38ae24`.

Seals:

- `REVIEW_SCOPE.json`: `2f057a29de3eeee3ba246bc983a404d8660648783284c5d720a4eb8178cd8b9c`
- `REVIEW_MANIFEST.tsv`: `cd3cda040f934f2ab22c0b456b6bfada834d74bc45d8597b3116fce5628eb2d2`
- `REVIEW_MANIFEST.sha256`: `4f2e1c34c2e05668e41290ad25820b8b883fe03a2528f49a4cb4999d0f1a3029`
- exact external report SHA-256:
  `f31bef79fe98a7c6e265366e1549c5509ccc32bf162e0abc405db715f37f57d9`

Verdict:

```text
ACCEPT_WITH_CAVEATS_G350_FREQUENCY_AREA_OWNERSHIP_BOUNDARY
```

The reviewer authenticated all 37 manifest payloads, reproduced the `23/23` aggregate and its
`120010/120010`, `35295/35295`, and `25/25` registered outputs, and independently rederived the
continuous positive character theorem. It accepted the central nonuniqueness, observer-typing,
conditional-conservation, source, caustic, and per-label ownership boundary. It required precision
repairs to provenance language, functional-domain quantification, observer/coboundary/caustic
typing, and evidence labels. Those repairs are frozen separately before execution.
