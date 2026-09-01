# G312 external review transmission

Date: 2026-09-01

Charles authorized transmission of the sealed 32-file intake at
`/tmp/udt_g312_review_i45wed8b` to the external Codex reviewer (`gpt-5.4`) for fresh read-only
adversarial review.

## Seals

- `REVIEW_SCOPE.json`: `f8e053e2baa086d851dce0493ec713953baee7e99e626e5a9fb150270333dc5d`
- `REVIEW_MANIFEST.tsv`: `f1dadc07caa44b28bf5e3e27d28f9a5d7225e56b03261935e42970ffaaebc98e`
- detached manifest seal: `1e465f1279c888b4d302fdc87f5a86c425612340be7ac34588a12dff65a04e85`

The intake and authentication file were mounted read-only. Shared network access was used only to
launch the reviewer. The reviewer was denied repository, protected-package, internet, and unsealed
observational access and was forbidden to edit evidence, continue the research, or adopt either
candidate premise.

## Frozen return

- `EXTERNAL_REVIEW_RESPONSE.md` SHA-256:
  `8bffb36acbae9f23320f5df7e399fa92ace465d9763dabe6b3c3c71b8ef791a1`
- `EXTERNAL_REVIEW_TRANSCRIPT.txt` SHA-256:
  `f98f3a27584ec39ec0e547c8a522b78a38cbe09d815eda1aee6eb0fa81aab804`

## Verdict

```text
G312_REPAIRABLE_DEFECTS__LANDING_RETAINED
```

The reviewer independently retained the two-premise scientific boundary and reproduced the three
registered scientific checks. It found one packaging defect: `verify_package.py` requires
`build_review_intake.py`, but the intake builder omitted that file from the sealed package.
