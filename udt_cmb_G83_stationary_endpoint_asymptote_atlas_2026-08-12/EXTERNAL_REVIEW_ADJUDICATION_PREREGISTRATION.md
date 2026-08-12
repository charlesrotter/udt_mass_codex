# G83 external-review adjudication preregistration

Date: 2026-08-12

Repository base before adjudication: `21fa25a5325e18590c8e8a9640e16b361a9af661`

External landing: `VERIFIED_WITH_CAVEATS`

Frozen evidence identities:

- sealed review manifest SHA-256:
  `364a7284a92577fa2189e8288853b2af4bb9f5eacef9289be85e22c5ed4678e9`
- raw external review SHA-256:
  `9a9aae6604ae96bec595140501755db64ec5694710454f2672cc19b7bcb23e7e`
- raw external transcript SHA-256:
  `bb0fd3149f748893dffecda6ab5a4f2e82c442e138f7394398de3a8f663d488b`

## Additions-only adjudication contract

The sealed 41-file intake, its 40 manifest payloads, and every preregistered G83 result remain
unchanged. The adjudication will:

1. preserve the reviewer landing and evidence boundary without strengthening it;
2. independently replay all 40 review-manifest hashes in the live repository;
3. resolve the sealed-intake Git-provenance caveat using repository ancestry only: prove that
   `e4a3082290123dcdb06b74bb5a5f6e26315c9933` banked the preregistration before its direct child
   `6b07caec44918aa54ba014c024e78ac586da1112` banked the calculation;
4. preserve the disclosed limitation that the Radau replay changes solver family but shares the
   geometry implementation;
5. preserve the maximum conclusion
   `BOUNDED_STATIONARY_ENDPOINT_ASYMPTOTE_CANDIDATE_ATLAS`;
6. add fail-closed verification for the raw evidence, sealed payloads, chronology, reproduced
   census and scalar identities, authority boundary, current navigation, frozen manifests, tests,
   and protected metadata-only dirt.

No physical profile, scale `R`, source surface, observer-pair separation operator, `X_max` value,
CMB statement, action, matter source, bootstrap closure, local-signalling law, or time-live dynamics
may be promoted.
