# G275 repair result

Date: 2026-08-26

Preregistration: commit `18f84136`

## Landing

`SCIENTIFIC_LANDING_RETAINED__REPAIRS_IMPLEMENTED__PENDING_EXTERNAL_FOLLOWUP`

The external reviewer retained the exact G275 theorem. R1--R3 change certification only.

## R1 — explicit nonrecursive manifest and containment

`REVIEW_SCOPE.json` now records both the total physical file count and the manifest-entry count.
It states explicitly that `REVIEW_MANIFEST.tsv` lists every physical file except itself because a
cryptographic self-hash would be recursive. The sealed package verifier reconstructs the complete
physical path set, proves that the listed set is exactly the physical set minus the manifest,
checks containment, and checks every listed byte count and SHA-256.

Fresh ephemeral mutations adding an unlisted file or changing a listed payload are rejected.

## R2 — sealed verifier fails closed

Inside a sealed review root, frozen sources resolve only from the intake's exact `sources/` copies.
A missing or mismatched source fails immediately. The historical Git fallback remains available
only in repository mode so the preregistered source snapshot remains replayable after live startup
documents change.

An ephemeral test changes a sealed source while lawfully refreshing only its outer review-manifest
entry. The inner source hash fails, and a fake `git` marker proves no Git fallback was invoked.

## R3 — executable mutation/scope ledger

The prior pre-baked predicates were replaced with actual operators and hostile alternatives for:

1. homothety leakage into projective state;
2. screen deletion;
3. vector-only composition despite hidden spatial carry;
4. per-anchor scale proliferation;
5. automatic `X_max=ell` on a finite populated domain;
6. treating an empty population as a zero supremum;
7. attaching a pure length from `c_E` alone;
8. recovering scale from a zero-weight datum.

The independent verifier now exercises an actual nonempty-domain supremum function: an empty domain
raises, while a populated zero-state domain has supremum zero. The exact original independent
assertion count remains 340,006.

## Scientific non-change

The exact bounded landing, 26 production checks, 20,000-case independent census, active-screen and
frame-carry coverage, absence of observational inputs, and all stated open boundaries are unchanged.
