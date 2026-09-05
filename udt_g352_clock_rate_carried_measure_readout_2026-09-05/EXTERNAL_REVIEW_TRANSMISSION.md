# G352 external-review transmission record

Date: 2026-09-05

Charles authorized the sealed 38-file intake at `/tmp/udt_g352_review_oma8w_jf`, containing 36
manifest payloads plus `REVIEW_MANIFEST.tsv` and its detached seal, for a fresh read-only external
`gpt-5.6-sol` adversarial review. The authorized hashes were:

- `REVIEW_SCOPE.json`: `90458838b1f95c1d8e370331199a65eae2cf71c47af2e8e5062ff69b9d6db2e1`
- `REVIEW_MANIFEST.tsv`: `bc8247c6fdaa6c6a50762a092f457475b5efa288571d0ab8fba8c5500004e29d`
- `REVIEW_MANIFEST.sha256`: `f2b84cf89137588d09bf75e376e10b13e315c013935ed27204530b2f035878d3`

The intake and authentication file were mounted read-only. Shared host-network access was used only
to contact the Codex API. The reviewer was prohibited from browsing, downloading, editing evidence,
continuing the research, accessing the repository/protected packages, universalizing `p=1`, or
selecting a physical interpretation or scale.

## Launch record

1. Session `01a07338-26f0-7cf1-ae12-48ecb0e2c0d7` could not resolve the API host because the
   isolated launcher lacked the host resolver mount. It produced no scientific review.
2. The launcher alone was repaired to mount `/run/systemd/resolve` read-only. The sealed intake was
   unchanged. Session `01a0733a-72be-7a80-ab7a-ff0c445ffd6e` authenticated the intake and began the
   audit but was interrupted by the execution outage before producing a report.
3. Session `01a0733c-7f3c-7671-adba-b5b4221c49c1` completed the fresh review of the unchanged intake.
   Its return directory was `/tmp/udt_g352_external_return_HsQWXGuG`; its captured transcript was
   `/tmp/udt_g352_external_capture_rac0IIw1/external_review_transcript.txt`.

The returned `EXTERNAL_REVIEW_RESPONSE.md` is 19,008 bytes with SHA-256
`b83f2b0b69ad3ecef065bd99b00ae6ce53d0c1032ae0aafa10ddfca808362bdc`. The copied repository file is
byte-identical. The terminal verdict was:

```text
REPAIR_G352_BOUNDED_CLOCK_RATE_READOUT
```

The review retained the conditional `R A^-1` algebra but required the repairs preregistered in
`R2_PREREGISTRATION_EXTERNAL_REVIEW_REPAIRS.md`.
