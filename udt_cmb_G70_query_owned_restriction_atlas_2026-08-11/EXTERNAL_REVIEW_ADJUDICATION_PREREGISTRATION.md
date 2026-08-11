# G70 external-review adjudication preregistration

Date: 2026-08-11

Reviewed commit: `03bc4328ace92269b9f01e19f2c627fd002fc544`

Reviewed manifest: `REVIEW_MANIFEST.tsv`

Reviewed manifest SHA-256:
`c2edde31e1a9781dc5cadfd53d8f36edfafbeb481c912a50226daecfe4c301fc`

Authorized intake: `34` sealed read-only files: the manifest plus its exact `33` hashed paths.

External reviewer: Codex `gpt-5.4`, fresh ephemeral context, high reasoning, approval `never`,
read-only sandbox, web search disabled.

External landing: `VERIFIED_WITH_CAVEATS`.

## Frozen adjudication contract

Before adding or changing any adjudication wording:

1. preserve every file hashed by the reviewed manifest byte-identically;
2. preserve the raw reviewer return and complete successful-run transcript byte-identically;
3. reproduce their SHA-256 values:
   - raw return: `edc759e8dd04a85bd4a6adac68bc933ad63384d5972cb39a93be7fa201857813`;
   - transcript: `72768bb9ec86d26cc6517ac8e6fbb7676499dc9295b6b6ae2838ca16d12fff02`;
4. retain the strict scientific landing `IDENTIFIABILITY_NUMERICALLY_UNRESOLVED`;
5. retain `R05_KNOWN_SOURCE_PLUS_CARRY` only as a bounded conditional algebraic sufficiency result;
6. retain all physical source, endpoint/profile, carry-readout, action, bootstrap, `X_max`, and
   signalling ownership as stated in the reviewed package;
7. treat the review caveat only as a repository-provenance limitation of a deliberately sealed
   non-git intake unless a live-checkout replay finds an actual repository defect;
8. rerun the live repository gates, including the seven protected untracked-path metadata check,
   without opening or modifying those protected paths;
9. add an additions-only adjudication layer; do not rewrite the reviewed manifest or any reviewed
   G70 evidence file;
10. make no new scientific calculation, fit, source assumption, endpoint/profile selection, or
    downstream CMB claim.

Maximum allowed adjudication: `EXTERNALLY_VERIFIED_WITH_REPOSITORY_PROVENANCE_CAVEAT_CLOSED_LOCALLY`
if and only if the live repository replay passes. Otherwise preserve the review caveat and report
the exact failing gate.
