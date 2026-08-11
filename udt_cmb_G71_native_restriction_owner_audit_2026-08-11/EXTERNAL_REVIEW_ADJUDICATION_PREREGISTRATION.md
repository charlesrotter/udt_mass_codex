# G71 external-review adjudication — preregistration

Date: 2026-08-11

Base commit: `b1df6fe7dc7c634c0c02067b8f8e6919ae6235d2`

Reviewed manifest: `REVIEW_MANIFEST.tsv`

Reviewed manifest SHA-256:
`451d472956183346a145f2c2c2c2213b48194a4665556dcff97c14afa95b6e6b`

External landing: `VERIFIED_WITH_CAVEATS`

Raw return SHA-256:
`222f43b1348a33acd6db775f212dcc54e06d557c89ab0aa5c3a120154ed2065f`

Transcript SHA-256:
`0e4672ecceb2a562b58ba09772307add30bd8431856c90033cac1bcbcb4650b1`

## Frozen reviewed layer

All 44 paths in `REVIEW_MANIFEST.tsv` remain byte-identical. Do not rewrite the reviewed atlas,
ledger, report, derivation, scripts, manifests, or verification records.

## Review finding to adjudicate

The reviewer independently upheld the six-target scientific landing, all 44 hashes, 12 exact
fraction trials, 200 numerical trials, and 13/13 semantic mutations. It found one evidence-hygiene
caveat: the six `OWNER_TARGET_LEDGER.tsv` evidence tokens are literal and verified, but the 21
`SOURCE_TARGET_ATLAS.tsv` `decisive_evidence` cells are human-readable paraphrase labels rather than
literal source tokens. The atlas is therefore not mechanically self-citing.

## Additions-only correction contract

1. Preserve the original 44 reviewed paths unchanged.
2. Preserve the raw external return and complete transcript byte-for-byte.
3. Add a separate 21-row literal-citation overlay rather than editing `SOURCE_TARGET_ATLAS.tsv`.
4. Each overlay row must identify the same source identity, a literal source token, and its exact
   line number; every token must verify against the frozen source.
5. Do not change any owner status unless the literal source contradicts the reviewed classification.
6. Add fail-closed checks for missing/duplicate sources, nonliteral tokens, wrong line numbers,
   status drift, reviewed-hash drift, and protected-path access.
7. Re-run package, premise, frozen-manifest, current-path, frontier, link, and test gates from the
   live checkout.
8. Update startup navigation only after the correction verifies.

Maximum conclusion: additions-only external-review adjudication. No source, endpoint, profile,
observable, CMB spectrum, fit, action, bootstrap law, `X_max` value, signalling law, or downstream
physics may be derived or selected.
