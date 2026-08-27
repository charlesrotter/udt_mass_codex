# G281 external-review transmission record

Date: 2026-08-27

## Authorized intake

- intake: `/tmp/udt_g281_review_s5kxopj4`
- physical file count: `62`
- manifest payload rows: `60`
- `REVIEW_SCOPE.json` SHA-256:
  `0497ab95a1dca15a5b5b44dffa914446b91783f94958416b095ef3ae93a8897c`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `99f631e740fcb1cf74f60c67cf049539fdcdd1b18c61f1b8cd6292eeac7a29db`
- `REVIEW_MANIFEST.sha256` SHA-256:
  `394a4e85807dce814f7d7bc187fd4ccc980f346ead6cd3d0c6833a3e5d8ae8f1`

Charles authorized transmission to external Codex `gpt-5.4` for fresh read-only adversarial review.
The reviewer was restricted to the sealed intake and registered G281 checks in a writable ephemeral
copy. Evidence edits, research continuation, repository or protected-package access, and unsealed
observational or theoretical imports were forbidden.

## Execution

- model: `gpt-5.4`
- reasoning effort: `high`
- web search: disabled
- intake mount: read-only at `/intake`
- writable replay/output mounts only: `/work`, `/return`
- fresh session id: `01a04440-9047-7ab1-81fd-60af7cf5d232`
- raw response: `/tmp/udt_g281_external.wqVvr1BF/return/EXTERNAL_REVIEW_GPT54.md`
- raw response SHA-256:
  `9c9c7ad31529d8b10c7283488052a9f71c75501ad1191f00ba0915efb726e476`
- transcript: `/tmp/udt_g281_external.wqVvr1BF/transcript.txt`
- transcript SHA-256:
  `9a869c8ea4684562b9a1d49500e5c118ab3f297e718f3e0fa7c6f57d61a2077a`

## Return

Verdict: `ACCEPT-WITH-REPAIRS`.

The reviewer retained the complete bounded scientific landing. It verified all 60 payload hashes
and sizes, all three outer seals, 62 physical files, zero symlinks, the three intake-resident G281
replays, and the July two-factor optics replay. It requested only provenance/packaging repairs:

1. remove or seal the two live startup authorities claimed in the 34-source scope;
2. make metric-owned or physically selected history explicit in the route classification so G79
   cannot appear to be a six-gate near-pass merely because it was frozen before SNe;
3. distinguish intake-replayed evidence from repository-recorded G279/G280 checks whose scripts
   were not included in the intake;
4. repair the `CURRENT_SCIENTIFIC_PREMISES.md`/`.tsv` typo.

Scientific conclusion changes: none.

## Authorized repair-only follow-up

- corrected intake: `/tmp/udt_g281_review_ttt_plen`
- physical file count: `67`
- manifest payload rows: `65`
- `REVIEW_SCOPE.json` SHA-256:
  `9a89c65d4078887006fa398d8978cce47a71f8abeb3bae5591c759f7346c9b72`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `6641d3f315fb399d9ee1b8c597d6c57b969ae6c0ff5d651cbd716f717d829b57`
- `REVIEW_MANIFEST.sha256` SHA-256:
  `8113094bbf74682791ad7002ec942dd47ab0c77260f9e0392e695797b8de35fb`
- fresh session id: `01a04455-d987-7ab3-b584-d7880b6c154b`
- raw response:
  `/tmp/udt_g281_followup.TTLF1SMB/return/EXTERNAL_REPAIR_FOLLOWUP_GPT54.md`
- raw response SHA-256:
  `e4b262925f8f2a77e3feaf262586e0e53215b4bbf0f8ef1ed683f7632cf205fc`
- banked response: `EXTERNAL_REPAIR_FOLLOWUP_REVIEW.md`
- banked response SHA-256:
  `a60d20794411601d25450a5fe5ac276589f1a8868a24dcf1f10f7bd11ca0e133`
  (content-identical; the repository copy adds the conventional terminal newline)
- transcript: `/tmp/udt_g281_followup.TTLF1SMB/transcript.txt`
- transcript SHA-256:
  `a3162205137dcc526cd2f59840b395da8cb717d66f36e3f4b0913cc5f7a5cb71`

Charles authorized a read-only repair-only follow-up, including read-only authentication-file use
solely to launch the reviewer. The corrected intake was mounted read-only at `/intake`; runtime
writes were confined to an ephemeral `/work` copy and the response mount.

## Follow-up return

Verdict: `ACCEPT`.

The reviewer verified all three outer hashes, the detached seal, all 65 payload hashes and sizes,
67 physical files, zero symlinks, exact 32-source scope/manifest equality, repairs R1--R4, and all
four registered sealed commands. It found no remaining scoped defect. The bounded G281 scientific
landing did not change.
