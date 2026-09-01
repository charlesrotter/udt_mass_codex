# G318 external review transmission record

Date: 2026-09-01

Charles authorized transmitting the sealed 35-file intake at
`/tmp/udt_g318_review_4s9mehd7` to the external Codex reviewer (`gpt-5.4`) for fresh read-only
adversarial review.

## Authorized seals

- `REVIEW_SCOPE.json` SHA-256:
  `f31f9bf37b1d2d86fc3919466b2e19af05afabd86e4cc800c14453f28f8d6ef4`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `226c20ae969c3f29c5fe9745db36191921cba7ac9030412fdd01e970d6142ee2`
- detached seal SHA-256:
  `9c3077bcd10237c7c41bb1e9a09ff12c66774fce60f7a92741f4403f1c067ed6`

The sealed intake and authentication file were mounted read-only in an isolated bubblewrap
environment. Writable access was confined to disposable `/work` and `/return` mounts. Repository
and protected-package paths were not mounted. Shared network access existed only for Codex API
transport; web search remained disabled and browsing/downloads were prohibited.

## Authentication, replay, and audit

The fresh zero-context reviewer authenticated the manifest seal and all 33 manifest payloads by
byte count and SHA-256. It ran the four registered commands in a fresh writable copy and observed:

- 14,043 production assertions;
- 4,440 implementation-distinct assertions;
- 48/48 hostile catches;
- 27 independent Weyl instances, 16 atlas rows, and four center witnesses;
- package verification `PASS_INTERNAL__EXTERNAL_REVIEW_REQUIRED` at the sealed pre-review stage;
- all five generated artifacts byte-identical to the sealed versions.

An initial attempt to clear a proposed replay directory used a prohibited destructive command and
was rejected by the review tool before any filesystem action occurred. The reviewer immediately
used a new empty writable directory; all four registered replays then passed. This was a tooling
event, not an evidence or scientific defect.

The reviewer independently rederived the vector power law, physical eigenvalue ratios, scalar
ODE, integrated obstruction, `n=-2` center and first integral, exact period covariance, direct
physical constraints, spatial Ricci tensor, and electric and magnetic initial Weyl tensors. It
found no scientific defect inside the declared positive sign-definite constant-ratio, flat marked
`T^3`, diagonal-TT, one-coordinate family. Its exact verdict was:

```text
G318_ACCEPTED__NONCONSTANT_PSI_BRANCHING_AND_TIDAL_PERIODIC_FAMILY_UPHELD
```

The reviewer did not rerun the separate full-repository regression because repository access was
forbidden. It correctly treated that as non-load-bearing for the sealed scientific result.

## Preserved evidence hashes

Raw external artifacts:

- response: `a6bb47ff66d80f531d7bd6b1e7c26b712ad008f9a4c7ad5cb643ac3ed46363cc`
- CLI final: `f6c9e7c32b1eab933a05d39b3e775ff6b5363e6eff7a859d897f9fa4d03f3de8`
- transcript: `2f62fcdb974950c07e5731b04b3bc9bda91e076755b6c12247c5f844dc55461c`

Banked artifacts after transcript line-ending and trailing-whitespace normalization only:

- `EXTERNAL_REVIEW_RESPONSE.md`:
  `a6bb47ff66d80f531d7bd6b1e7c26b712ad008f9a4c7ad5cb643ac3ed46363cc`
- `EXTERNAL_REVIEW_TRANSCRIPT.txt`:
  `a67207a525cb6b33b87b35f13fc1aed316c33e566a75bb4870269b1c219ed36c`
