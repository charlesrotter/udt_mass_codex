# G266 external-review repair implementation

Date: 2026-08-26
Repair preregistration commit: `44fc0a50`
Status: `REPAIRS_ACCEPTED`

## External review record

The authorized fresh intake was `/tmp/udt_g266_review_06qaaprk`, with:

```text
REVIEW_SCOPE.json    1e619ec20f60119c369f4f82cfb2ceeb047f7bccd42622a87ad85634e92f3ec1
REVIEW_MANIFEST.tsv  dea208277a08ce6f1a7a65bdc6d41f707e9cb7dbe3e002ba1acd9824d5118cce
```

The reviewer returned `ACCEPT_WITH_REPAIRS`. `EXTERNAL_REVIEW_GPT54.md` is byte-identical to the
raw 6,347-byte review artifact and has SHA-256
`be450cae5a3e6b44f657ab8dd8827138925b626c3a9254b6da0aec419cd22ca9`.

The authorized repair-only follow-up intake was `/tmp/udt_g266_repair_followup_dw4rfiaa`, with:

```text
REVIEW_SCOPE.json    2428350b0b9ff8f1dd021fb50e828b4e8617b38d3e9e0b8497f84bbbf3974f4e
REVIEW_MANIFEST.tsv  0f062c3011568936c99250f7e167bafc286683809ab18571f8ed2e9d4258e130
```

The reviewer returned the exact disposition `REPAIRS_ACCEPTED`. The raw 16-byte external artifact
had SHA-256 `060c312e7fb482d0e053e4e3ab82637086e5289d4f94cf19924f8513a64cb9c6`; the durable Markdown copy
normalizes the terminal newline and has SHA-256
`2341fe9ebce96341df2d3666523ef704cc49af071fa0c7480acbe94243cc952d`. The reviewer reproduced the
dependency-free replay with SymPy unavailable in both the sealed layout and a synthetic live
layout: 25 exact checks, 768 independent assertions, 8 mutation catches, and deliberate wrong-hash
rejection all passed.

## R1 — sealed source resolution

`verify_package.py` now resolves each frozen source against two exact candidates: the live
repository root and the sealed `private_sources/` root. It accepts a candidate only after its
SHA-256 matches `SOURCE_MANIFEST.tsv` and proves that a deliberately wrong registered hash is
rejected.

## R2 — dependency-free exact replay

`derive_even_channel_stdlib.py` implements the 25 named checks with standard-library exact rational
Laurent algebra and explicit exact chain-rule identities. It reads no recorded result. Its complete
JSON object equals both `DERIVATION_RESULT.json` and the SymPy reference result. The package verifier
uses this dependency-free result as its exact authority and additionally compares the SymPy result
when SymPy is installed.

## R3 — reciprocal-kernel invariant scope

The live result, exact derivation, audit, and lay explanation now restrict the invariant statement
to the determinant-one two-leg reciprocal kernel on the supplied relation. Smooth reversal-even
readouts formed only from that kernel are functions of `Gamma`; no claim is made about arbitrary
physical scalars of the complete metric.

## R4 — areal geometry versus physical distance

The premise and witness ledgers now distinguish the already-derived invariant areal-radius
descriptor `R` from the freely explored physical attachment `ds=dR`. The exact derivation, audit,
and lay report retain the geometric priority of areal radius without promoting `Delta R` to the
physical mutual distance.

## Frozen landing

No formula, check count, witness profile, selected alternative, or maximum scientific conclusion
changed. `sech(delta)`, `P_INF`, `P_MUT`, physical distance, and metric-history ownership remain
unadopted or open. The bounded result is eligible for startup promotion after the accepted
repair-only review.
