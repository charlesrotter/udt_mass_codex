# G349 external-review transmission record

Date: 2026-09-04

Charles authorized the sealed 33-file intake at `/tmp/udt_g349_review_g918q7pr` for fresh
read-only adversarial review by external `gpt-5.6-sol`, including read-only authentication-file
use and shared host-network access solely to launch the reviewer. The intake contained 31 manifest
payloads plus `REVIEW_MANIFEST.tsv` and its detached seal.

The intake and authentication file remained mounted read-only. The reviewer copied the intake into
an isolated writable ephemeral work directory, ran checks only there, and returned its report from
an isolated return directory. External Codex session:
`01a06f86-c6ff-7a00-bd9d-d85380a068f8`.

Seals:

- `REVIEW_SCOPE.json`: `86a36ec9ae0c6c31fcb9216a1d7194d2457871be8dd30313e687eeaeab0a5fe3`
- `REVIEW_MANIFEST.tsv`: `c4fe70fd02e4f3da903e0c525e08a74e5c0e28615a0e92e03977c6ab174db4d0`
- `REVIEW_MANIFEST.sha256`: `253becb352c06af9bf57b68f0f53b5fcfbc687dde09153bfdff4e5f33fa31aae`
- exact external report SHA-256:
  `aadf46778a28a074550bb039139095ea3ef16a16c3deac1ec9903384334293c1`

Verdict:

```text
ACCEPT_WITH_CAVEATS_G349_FINITE_NULL_PATCH_AREA
```

The reviewer authenticated all 31 manifest payloads, reproduced the registered `18/18` aggregate
and its `44314/44314`, `14314/14314`, and `21/21` underlying results, and independently confirmed
the variable-cut Gram cancellation, spacelike auxiliary-metric cancellation, fold and
complex-square areas, and observer-density identity. It also supplied a decisive mixed
caustic/cut counterexample: ordinary endpoint-map rank can be two while transverse screen rank is
one and Lorentzian two-area is zero. That mandatory repair is preregistered separately and the
original report is retained byte-exact.
