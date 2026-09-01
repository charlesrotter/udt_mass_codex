# G311 external review transmission

Date: 2026-09-01

Charles authorized transmission of the sealed 34-file intake at
`/tmp/udt_g311_review_mw9zyh9c` to the external Codex reviewer (`gpt-5.4`) for fresh read-only
adversarial review.

## Seals

- `REVIEW_SCOPE.json`: `088e09bee62f2fefe0ff4fbbb7d8f84a414687802ad493255ea5d487332b21f3`
- `REVIEW_MANIFEST.tsv`: `1a6d2b013659ac9b86abd7c420b64e7545d4f174cc29fa267031cc5574790c96`
- detached manifest seal: `5dde341fd027038e6ea58c25c0043c5f3c3dfd85843369ea7771c2268c5f5f26`

The intake and authentication file were mounted read-only. Shared network access was used only to
launch the reviewer. The reviewer was denied repository, protected-package, internet, and unsealed
observational access and was forbidden to edit evidence or continue the research.

## Frozen return

- `EXTERNAL_REVIEW_RESPONSE.md` SHA-256:
  `c3f85e0ba89928305722579aa69fbd9ef92002d10dcc329638e13411fc2bcdcd`
- `EXTERNAL_REVIEW_TRANSCRIPT.txt` SHA-256:
  `1820284ebac65fc9dc1fbba9b15016d74506267fa26e530577e4e5598e69f8b9`

## Verdict

```text
G311_REPAIRABLE_DEFECTS
```

The reviewer independently upheld the bounded scientific landing and found three certification
defects: one undeclared SymPy dependency, one aggregate verifier that requires forbidden repository
ancestry access, and one shared-code hostile harness that must be described as regression evidence
rather than independent confirmation.
