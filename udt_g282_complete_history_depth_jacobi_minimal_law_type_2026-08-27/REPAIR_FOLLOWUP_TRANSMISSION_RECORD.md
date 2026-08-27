# G282 R1 repair-only follow-up transmission record

Date: 2026-08-27

## Authorized intake

- intake: `/tmp/udt_g282_repair_followup_nmawds5j`
- physical files: 50
- manifest payloads: 48
- `REVIEW_SCOPE.json` SHA-256: `1901460c63530953ed20e70bb397b4c22178290a09e372d40497c174cfad0745`
- `REVIEW_MANIFEST.tsv` SHA-256: `8311b0775503e24e29f659bbddf37bf4c2961b5ae6b125f1d2cc70652289edac`
- detached seal SHA-256: `452d64dcf3fe8077a7e096ff6d67be298661cd74b91031846f47a4a37e493387`

Charles explicitly authorized read-only repair-only follow-up review by external Codex `gpt-5.4`.
The reviewer could verify only preregistered R1, the unchanged bounded landing, and registered
no-write replays in a writable ephemeral copy. It could not edit evidence or continue research.

## Isolation and return

- fresh reviewer session: `01a0448f-f582-7780-8aa6-6738dd18bca5`
- runtime: `/tmp/udt_g282_followup_external.8TgFWxTI`
- intake mounted read-only at `/intake`
- repository and protected packages not mounted
- web search disabled
- raw response SHA-256: `4d02a287d2569ceda2203e70bcc145bdf9af8ecf78dab0015df13df4f761beac`
- complete transcript SHA-256: `1e6cf779b68ab544b97f022b40af48e3e1a40839963b70002df3e48ef28c9a45`

`EXTERNAL_REPAIR_FOLLOWUP.md` preserves the exact response text with the repository's normal final
newline; the raw-response hash above belongs to the original no-final-newline return.

## Verdict

`REPAIR-NOT-ACCEPTED`

Every seal, payload, count, registered replay, mathematical witness, numerical result, premise
ledger, and scientific landing passed unchanged. One literal R1 wording defect remained:
`EVIDENCE_GATES.md` said the guard does not mutate or replay "evidence artifacts" but did not
separately spell out "derivation code" and "source-census artifacts" as required by the repair
preregistration. No scientific repair was requested.
