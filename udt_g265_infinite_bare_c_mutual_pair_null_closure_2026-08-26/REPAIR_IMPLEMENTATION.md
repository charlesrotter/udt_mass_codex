# G265 external-review repair implementation

Date: 2026-08-26
Preregistration commit: `51601515`
Status: `REPAIRS_ACCEPTED`

## External review record

Authorized sealed intake:

```text
/tmp/udt_g265_review_w_tgukdw
```

Registered digests:

```text
REVIEW_SCOPE.json    584cd5984196b7bd6dcc38635ca47c3b7f59371b313134b186102a5d662e1e5f
REVIEW_MANIFEST.tsv  db48377fb3840b5c3df3968fe8039c379c63bc6c83ee12e5d5c850f083087599
```

The external GPT-5.4 reviewer returned `ACCEPT_WITH_REPAIRS`. The exact runtime output was written
to:

```text
/tmp/udt_g265_external_review_5bHfq9O7/EXTERNAL_REVIEW_GPT54.md
```

The banked `EXTERNAL_REVIEW_GPT54.md` preserves the raw reviewer output exactly, apart from adding
the repository-standard terminal newline. The raw file is 5,115 bytes with SHA-256
`b93e959fd8110bb828dec6335386cc8d155049bd55d4ca6a2de1c5190daa1e76`; the banked file is 5,116
bytes with SHA-256 `1d7275f2337a9f74601c9b82e64001dd52393f3d9d3abdd39794c28561f4c5a9`.

## Implemented repairs

### R1 — exact replay/result alignment

`derive_closure.py` now emits every field and the exact bounded landing registered in
`DERIVATION_RESULT.json`. No formula, check, witness, numerical result, or scientific conclusion was
changed.

### R2 — fail-closed verifier

`verify_package.py` now compares the complete live and recorded JSON objects for equality. It also
creates an in-memory landing mutant and proves that the exact-result gate rejects it. No evidence
file is mutated.

### R3 — premise-status wording

`LAY_REPORT.md`, `EXACT_DERIVATION.md`, and `AUDIT_REPORT.md` now say explicitly that:

- infinite bare `c` is a proposed provenance interpretation;
- the signed/even distinction is derived algebra;
- `sech(delta)` is a candidate physical projection;
- mutual-distance ownership remains proposed and open; and
- no startup semantic regrade follows from G265 alone.

### R4 — evidence grade

The fresh external report is banked. `EVIDENCE_GATES.md` and `STATUS_LEDGER.tsv` record the external
accept-with-repairs result while retaining repair-follow-up status. No startup authority file or
premise registry has been promoted.

## Follow-up ceiling

A repair-only reviewer may verify only R1--R3 and the unchanged bounded G265 landing. Scientific
expansion, premise adoption, startup promotion, time-live derivation, profile selection, or
canonization is outside the repair path.

## Follow-up result

The authorized sealed 35-file repair-only GPT-5.4 follow-up returned `REPAIRS_ACCEPTED`. It verified
all 33 payload hashes, reproduced `18/18`, `63/63`, and `8/8`, confirmed complete live/recorded JSON
equality, independently caught an altered recorded landing, and accepted the repaired premise
wording. The bounded static-radial classification may enter startup authority with caveats. Neither
`P_INF`, `P_MUT`, nor the `sech(delta)` physical projection was adopted.

`EXTERNAL_REPAIR_FOLLOWUP_GPT54.md` preserves the raw 1,969-byte review exactly apart from the
repository-standard terminal newline. The raw SHA-256 is
`fad76ea8544fa91a9040946cc7e8c1032664b122f08132335047edaf1760c569`; the banked 1,970-byte file
has SHA-256 `82cdd14c484ee843d09dbb7075420a94b629649800318b4c630829a99884ace7`.
