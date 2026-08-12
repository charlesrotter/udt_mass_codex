# G82 external-review adjudication preregistration

Date: 2026-08-12

Repository base before adjudication: `a9cffc66794707eb68042e372bdb47b1a182de63`

External landing: `VERIFIED_WITH_CAVEATS`

Frozen evidence identities:

- sealed review manifest SHA-256:
  `fe2a80592aa3236af5044f91675862be2989cc2209d5b9fefa66c87d6973ac5a`
- raw external review SHA-256:
  `fb99a23e261e55ce1567a3118feac80a7b239f0e61007841dbfb9f69f0e21ada`
- raw external transcript SHA-256:
  `7944ace16025aaeafb682e7dcbbcd19e4c364e646121da22a80ff3def3b0df66`

## Additions-only adjudication contract

The sealed 27-file intake and every preregistered G82 result remain unchanged. The adjudication will:

1. preserve the reviewer landing and evidence boundary verbatim;
2. independently replay all 26 review-manifest hashes in the live repository;
3. resolve the apparent commit-language caveat using Git ancestry only: `e36752ed...` is the declared
   calculation base, while `88afa190...` is the later commit that banked the preregistration;
4. preserve the reviewer's catch-harness and repository-gate caveats rather than enlarging what the
   sealed review itself established;
5. keep the maximum G82 conclusion at
   `G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY` and the scientific ceiling
   at `DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`;
6. add fail-closed verification for the raw evidence, chronology, sealed payloads, numerical values,
   authority boundary, current navigation, frozen manifests, tests, and protected metadata-only dirt.

No physical profile, endpoint, scale, `X_max`, SNe/CMB observable, `cmb_temp`, source, action,
matter, bootstrap closure, signalling law, or future signal may be promoted.
