# G328 external-review transmission record

Date: 2026-09-02

## Authorization and isolation

Charles authorized transmission of the sealed 42-file intake at
`/tmp/udt_g328_review_zk668qbe` to the external Codex reviewer (`gpt-5.4`) for fresh read-only
adversarial review, including read-only authentication-file use and network access solely to launch
the reviewer. The intake was mounted read-only. The repository and protected packages were not
mounted. A separate ephemeral writable copy was used for registered replays and reviewer-authored
checks. The reviewer was prohibited from editing evidence files or continuing the research.

External reviewer session: `01a06481-0d1a-73b3-bf1e-081ddab30e7e`.

## Authenticated intake

- `REVIEW_SCOPE.json`: `cf200f2704b4a729d8fbe828b6ae8c2b8efc333abc997b1d815d0dd894e43383`
- `REVIEW_MANIFEST.tsv`: `ce5dc552238749cf3dcf535c2f9355ee28b24dfb790cc1295db37c3d9346cac1`
- detached manifest seal: `0cc0f8ae92b0bc57e3c8747340337d4c0fa8a03cc998e64a0b88f87af71d48cc`
- manifest payload count: `40`
- local pre-review and post-review intake verification: `PASS`
- reviewer post-replay payload mismatches: `0`

## Returned evidence

- preserved report: `EXTERNAL_REVIEW.md`
- report SHA-256: `9fc5ed67f54643dc62be672a582d4d9650904dcab59c77f96e2467d271afa59a`
- captured launch transcript SHA-256:
  `f510d7e930cf65a7e4d12c6416a2b1e86a1c53f71d0b1bd5e22b20dad6733525`
- process exit: `0`
- exact verdict: `ACCEPT__G328_BOUNDED_TRANSVERSE_CENSUS`

The full transcript remained in the ephemeral launch capture. The complete authored reviewer report,
including its independent calculations and exact verdict, is preserved byte-for-byte in this
package.

## Scientific scope

The acceptance is limited to the complete primitive `y`-directed nonzero Fourier first-variation
tile on the registered G324 compact Taub quotients, modulo all periodic same-mode gauge and on
compact intervals inside `T>0`. It is not acceptance of the full Fourier spectrum, endpoint
admissibility, full linear stability, nonlinear stability, physical occupancy, history selection,
scale, or physical `X_max`. No UDT metric, reciprocal-kernel, angular-sector, or field-equation
formula changed.
