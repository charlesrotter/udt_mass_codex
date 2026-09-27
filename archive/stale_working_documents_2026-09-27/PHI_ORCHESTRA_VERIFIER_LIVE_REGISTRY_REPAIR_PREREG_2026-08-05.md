# Phi-orchestra verifier live-registry repair preregistration

Date: 2026-08-05

Branch: `grok`

## Problem

The complete-pair phi/orchestra package verifier froze `CURRENT_SCIENTIFIC_PREMISES.tsv` as if it
were immutable evidence. The startup update intentionally advances that live premise registry to
route future sessions through the phi/orchestra result. The verifier therefore reports
`SOURCE_HASH_DRIFT` even though the immutable audit sources are unchanged.

## Authorized repair scope

Edit only `udt_complete_pair_phi_orchestra_audit_2026-08-05/verify_audit.py` and its generated
`VERIFICATION_RESULT.json`.

Required behavior:

- Keep every immutable evidence source exact-hash checked.
- Treat `CURRENT_SCIENTIFIC_PREMISES.tsv` as a live startup registry.
- Permit only the banked hash
  `0fa377cb50b775875dd8f2de95acb840f3d38183c71b54caef242a89cfc1fa13`
  or the preregistered startup-update hash
  `2da7b708495e4ef20f8833edbcb939d61c3ae8d0736bc916d9cfe4e5bf0eb5be`.
- Preserve the frozen-source mutation catch-proof against an immutable source.

## Out of scope

No equations, derivation result, status ledger, external review, research conclusion, or startup
orientation prose may be changed by this repair.

