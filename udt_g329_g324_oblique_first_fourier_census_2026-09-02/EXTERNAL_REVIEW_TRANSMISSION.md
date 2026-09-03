# G329 external-review transmission record

Date: 2026-09-02

## Authorization and isolation

Charles authorized transmission of the sealed 43-file intake at
`/tmp/udt_g329_review_wtgo6r8r` to the external Codex reviewer (`gpt-5.4`) for fresh read-only
adversarial review, including read-only authentication-file use and shared network access solely to
launch the reviewer. The intake and authentication file were mounted read-only. The repository and
protected packages were not mounted. Registered replays and independent checks used a separate
writable ephemeral area. Web browsing, downloads, evidence edits, and research continuation were
prohibited.

External reviewer session: `01a064e9-3c12-7210-b9b1-6653e88571ec`.

## Authenticated intake

- `REVIEW_SCOPE.json`: `d87b71b0eedf41f3501ccff982fdd6062c6ac57fe3b512bd1d1c61e866bc4cfc`
- `REVIEW_MANIFEST.tsv`: `a19494b0f447e8d1e9148cef4447c50130f1b59e5da9d11592f4fa420c322679`
- detached manifest seal: `42ef7ecef32e194f81cb800c4721eeb05da5eae8687e1bc83e8af94af1faf533`
- manifest payload count: `41`
- local pre-review intake verification: `PASS`
- reviewer authentication: `41/41` payloads match
- reviewer post-replay payload mismatches: `0`

## Returned evidence

- preserved report: `EXTERNAL_REVIEW.md`
- report SHA-256: `54aa248f64413e8bb79437e16c3826b6872dc99a2b39e3d8b682fb6d9930a782`
- captured launch transcript SHA-256:
  `20f0bdbc70adbea318d964a32879123d4af2683f3d5e4ba2a776f92550a72b24`
- process exit: `0`
- exact verdict: `ACCEPT__G329_BOUNDED_OBLIQUE_CENSUS`

The full launch transcript remained in the ephemeral capture. The complete reviewer-authored report
is preserved byte-for-byte in this package.

## Scientific scope

The acceptance is limited to the complete all-ten-component primitive strict-oblique Fourier tile
on the fixed conditional G324 compact Taub quotient, modulo all periodic same-mode gauge, on compact
intervals inside `T>0`. It is not acceptance of full Fourier or nonlinear stability, endpoint
admissibility, physical occupancy, history selection, scale, or physical `X_max`. No UDT metric,
reciprocal-kernel, angular-sector, or field-equation formula changed.
