# G303 external-review transmission record

Date: 2026-08-30

## Invalid first attempt

The session launched against `/tmp/udt_g303_review_13hsya3r` is invalid and discarded. Its isolated
runtime lacked SymPy and the reviewer accessed PyPI while trying to obtain it, violating the
authorized no-internet scope. The intake was mounted read-only and remained unchanged. No output
from that session certifies G303.

## Valid replacement

- authorized intake: `/tmp/udt_g303_review_5z7eyqxr`
- file count: `35`
- `REVIEW_SCOPE.json` SHA-256:
  `c993f40d705ebb9bd0ac3a50cbbe5b41f54bb8c82953cc40b3de7fb66a488eee`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `6b0347bea6bac82bd22a356b7a1847e2ea11173cada31de7bdf2874cd5d388d0`
- sealed runtime archive SHA-256:
  `34daa458f6c849d2fa1011129c45ab0849e9991acb63fb37a4fab3b7ff6f99a0`
- model/session: `gpt-5.4`, `01a05380-26df-7bf3-9506-f6d4f499f04f`
- final response SHA-256:
  `16430afe0674d00d2f17cbea08ed856972cb1d5b8f840d41d466711c013e6d1e`
- transcript SHA-256:
  `e3c0d9ba1b56d6e4fc8188d23e36ddf7abb34c59bb5a28c081455407277f5acb`
- verdict: `VERIFIED_WITH_CAVEATS`

The valid reviewer inspected only the intake, used the sealed SymPy/mpmath runtime, and reran all
four registered scripts in writable ephemeral storage. It retained the bounded science and called
for wording, mutation-test, and independence repairs.
