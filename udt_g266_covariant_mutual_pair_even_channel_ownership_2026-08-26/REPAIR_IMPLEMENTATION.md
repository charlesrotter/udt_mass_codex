# G266 external-review repair implementation

Date: 2026-08-26
Repair preregistration commit: `44fc0a50`
Status: `ACCEPT_WITH_REPAIRS__REPAIR_FOLLOWUP_PENDING`

## External review record

The authorized fresh intake was `/tmp/udt_g266_review_06qaaprk`, with:

```text
REVIEW_SCOPE.json    1e619ec20f60119c369f4f82cfb2ceeb047f7bccd42622a87ad85634e92f3ec1
REVIEW_MANIFEST.tsv  dea208277a08ce6f1a7a65bdc6d41f707e9cb7dbe3e002ba1acd9824d5118cce
```

The reviewer returned `ACCEPT_WITH_REPAIRS`. `EXTERNAL_REVIEW_GPT54.md` is byte-identical to the
raw 6,347-byte review artifact and has SHA-256
`be450cae5a3e6b44f657ab8dd8827138925b626c3a9254b6da0aec419cd22ca9`.

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
unadopted or open. Startup authority is unchanged pending repair-only external acceptance.
