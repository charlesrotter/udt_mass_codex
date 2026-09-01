# G313 external-review transmission record

Date: 2026-09-01

Charles authorized transmission of the sealed 37-file intake at
`/tmp/udt_g313_review_0ll_kju0` to an external Codex `gpt-5.4` reviewer under the stated
read-only restrictions.

## Seals

- `REVIEW_SCOPE.json`: `95a496eda8e89cc5ad5e5df47ab8e79b1e7f298a8eb69909aa915849b2329bed`
- `REVIEW_MANIFEST.tsv`: `ac43b9a5d695540dcb1c288b55df6ea0f583400a2b18c9786f7cda1632dcb6a8`
- detached manifest seal: `233041f4d3727955cfa650244d13808fbb06cedb2002d662e46be0b17679882e`

## Isolation

- intake mounted read-only at `/intake`;
- repository and protected packages were not mounted;
- writable execution was limited to ephemeral `/work` and `/return`;
- authentication was mounted read-only solely to launch the reviewer;
- shared network was used solely for the Codex API; web search was disabled;
- evidence files were not writable and the reviewer was prohibited from continuing the research.

Two pre-model launch failures are retained in the external runtime: one obsolete CLI flag and one
missing resolver bind. Neither altered the intake. The successful reviewer independently reran the
four registered package checks in an ephemeral copy.

## Return

- response SHA-256: `d090b95fb6b1b441e0e1e94b70394534550ba5b334bcbc54c557e750d310daa6`
- transcript SHA-256: `d9ff74d8890034a46af2f69ebb2c76a7be430c3c106a79a084a32a66d09a8f59`
- verdict: `G313_REPAIRABLE_DEFECTS__SCIENTIFIC_LANDING_RETAINED`

The four defects are preregistered in `REPAIR_PREREGISTRATION.md`. No scientific claim is changed
before or by that registration.
