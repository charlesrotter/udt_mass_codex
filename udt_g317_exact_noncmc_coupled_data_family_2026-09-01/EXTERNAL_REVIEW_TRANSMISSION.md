# G317 external review transmission record

Date: 2026-09-01

Charles authorized transmitting the sealed 36-file intake at
`/tmp/udt_g317_review_kj5tot22` to the external Codex reviewer (`gpt-5.4`) for fresh read-only
adversarial review.

## Authorized seals

- `REVIEW_SCOPE.json` SHA-256:
  `464adc40cf5ca2493a9e11a4208281997a09470b7ecb3a1b6ee48e0eb510a088`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `ec07bc8e532e3a1eb6c0ff918aed3c607f0518d506d253a8edc5fc15e76c7125`
- detached seal SHA-256:
  `88f4f547d85ba6049afc6716362a06f41db0d862cb15d269d425bd964df06413`

The sealed intake and authentication file were mounted read-only in an isolated bubblewrap
environment. Writable access was confined to disposable `/work` and `/return` mounts. Repository
and protected-package paths were not mounted. Shared network access existed only for Codex API
transport; web search remained disabled and browsing/downloads were prohibited.

## Authentication, replay, and audit

The fresh zero-context reviewer authenticated the manifest seal and all 34 manifest payloads by
byte count and SHA-256. It ran the four registered commands in a fresh writable copy and observed:

- 1,637 production assertions;
- 1,191 implementation-distinct assertions;
- 29/29 hostile catches;
- 48 family instances and 14 solution-space atlas rows;
- package verification `PASS_PRE_EXTERNAL_REVIEW`;
- all five generated artifacts byte-identical to the sealed versions.

An initial attempt to create the writable copy used a prohibited destructive command and was
rejected by the review tool before any replay occurred. The reviewer immediately used a fresh
`mktemp` directory instead; all four registered replays then passed. This was a tooling event, not
an evidence or scientific defect.

The reviewer independently rederived the vector equation and periodic mean subtraction, scalar
classification, direct physical constraints, non-CMC coupling, electric and magnetic Weyl split,
and `q`-sign axis relabelling. It found no metric, kernel, angular, observational, premise, or
protected-work change. Its exact verdict was:

```text
G317_ACCEPTED__EXACT_NONCMC_INTERLOCK_AND_TIDE_SPLIT_UPHELD
```

The reviewer correctly limited its provenance conclusion: sealed evidence authenticates the
intake but cannot independently reconstruct repository ancestry when repository access is
forbidden. That protocol limit does not alter the bounded scientific result.

## Preserved evidence hashes

Raw external artifacts:

- response: `33046e6de527c4f96abd9d70e4a85fb296f57bed1a21bd742925bcf8dd434b1c`
- CLI final: `ec4122d3c8b8f24d0b1afa57c03ba8327b10a5888e663e6dc8f44a36597b2b2b`
- transcript: `cbc389011de41489291a1d849eb15ee73a1019ed24d26074d98b7c4719ac7217`

Banked artifacts after transcript line-ending and trailing-whitespace normalization only:

- `EXTERNAL_REVIEW_RESPONSE.md`:
  `33046e6de527c4f96abd9d70e4a85fb296f57bed1a21bd742925bcf8dd434b1c`
- `EXTERNAL_REVIEW_TRANSCRIPT.txt`:
  `29a1d830a764983bc6148a0ac0d130c09964ef243cd02cce4d9cc22b1297ea5c`
